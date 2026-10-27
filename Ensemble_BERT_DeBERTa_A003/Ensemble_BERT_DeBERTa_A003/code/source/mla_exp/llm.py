"""Conditional open-weight reranking. Three label logits, no generated parsing."""
import math
import time
from pathlib import Path

import numpy as np

from .classical import input_signature, run_dir
from .common import digest, environment, read_json, sha256, softmax, write_json
from .data import load_frame
from .fusion import member_probabilities
from .evaluation import metrics, operating_point, write_predictions

RUBRIC = ('Evaluate only the annotated argument segment in its essay context. '
          'A = Ineffective: unclear, unsupported or poorly connected reasoning. '
          'B = Adequate: understandable and relevant, with sufficient but ordinary support. '
          'C = Effective: clear, well-supported, persuasive and well-connected reasoning. '
          'Respect the discourse type. Do not infer quality from student demographics. '
          'Return exactly one letter A, B, or C.')


def uncertain(p, fraction):
    entropy = -(np.asarray(p) * np.log(np.clip(p, 1e-12, 1))).sum(axis=1)
    # Input rows are sorted by segment ID; stable sorting resolves entropy ties.
    return np.argsort(-entropy, kind='stable')[:int(math.ceil(len(p) * fraction))]


def examples(config):
    fit = load_frame(config['data_root'], 'fit', config)
    result = []
    for label in range(3):
        candidates = fit.loc[fit.label.eq(label)].copy()
        candidates['order'] = candidates.segment_id.map(lambda key: digest([42, key]))
        result.append(candidates.sort_values('order').iloc[0].to_dict())
    return result


def messages(tokenizer, row, shots):
    def shorten(text, limit, tail=False):
        ids = tokenizer.encode(str(text), add_special_tokens=False)
        if len(ids) > limit:
            ids = ids[:limit//2] + ids[-(limit-limit//2):] if tail else ids[:limit]
        return tokenizer.decode(ids)
    def content(item, example=False):
        return ('Discourse type: ' + str(item['discourse_type']) + '\nTarget segment: ' +
                shorten(item['discourse_text'], 160 if example else 1400, True) +
                ('\nAssignment: ' + shorten(item.get('assignment', ''), 64) +
                 '\nBefore: ' + shorten(item.get('left_context', ''), 192, True) +
                 '\nAfter: ' + shorten(item.get('right_context', ''), 192) if not example else ''))
    result = [{'role': 'system', 'content': RUBRIC}]
    for shot in shots:
        result.extend([{'role': 'user', 'content': content(shot, True)},
                       {'role': 'assistant', 'content': 'ABC'[int(shot['label'])]}])
    result.append({'role': 'user', 'content': content(row)})
    return result


def label_scores(model, inputs, choices):
    import torch
    lengths = inputs.attention_mask.sum(axis=1)-1
    positions, inverse = torch.unique(lengths, sorted=True, return_inverse=True)
    logits = model(**inputs, use_cache=False, logits_to_keep=positions).logits
    # Right padding is unchanged; each row selects its last actual prompt token.
    return logits[torch.arange(len(lengths), device=lengths.device), inverse][:, choices].float().cpu().numpy()


def score_rows(config, frame, indices, shots, cache_name):
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
    from .neural import gpu, hardware
    gpu()
    root = Path(config['output_root']) / 'llm_cache'
    root.mkdir(parents=True, exist_ok=True)
    cache = root / (cache_name + '.json')
    identity = digest({'model': config['llm_model'], 'rubric': RUBRIC, 'shots': shots,
                       'prompt_code_sha256': sha256(__file__), 'max_target_tokens': 1400})
    old = read_json(cache) if cache.exists() else {'identity': identity, 'rows': {}}
    if old['identity'] != identity: raise ValueError('LLM cache prompt/model mismatch')
    missing = [int(i) for i in indices if frame.iloc[i].segment_id not in old['rows']]
    started = time.perf_counter()
    times = []
    if missing:
        torch.cuda.reset_peak_memory_stats()
        revision = config.get('llm_revision') or old.get('model_revision')
        if config.get('llm_revision') and old.get('model_revision') and config['llm_revision'] != old['model_revision']:
            raise ValueError('LLM cache checkpoint revision mismatch')
        tokenizer = AutoTokenizer.from_pretrained(config['llm_model'], padding_side='right',revision=revision)
        choices = [tokenizer.encode(letter, add_special_tokens=False) for letter in 'ABC']
        if any(len(choice) != 1 for choice in choices): raise ValueError('Label options must be single tokenizer tokens')
        quant = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type='nf4', bnb_4bit_compute_dtype=torch.float16)
        model = AutoModelForCausalLM.from_pretrained(config['llm_model'], revision=revision, quantization_config=quant, device_map={'': 0}, attn_implementation='sdpa').eval()
        old['model_revision'] = getattr(model.config, '_commit_hash', None)
        old['hardware'] = hardware()
        write_json(cache, old)
        for start in range(0, len(missing), 2):
            indexes = missing[start:start+2]
            tick = time.perf_counter()
            inputs = None
            try:
                texts = [tokenizer.apply_chat_template(messages(tokenizer, frame.iloc[i], shots), tokenize=False, add_generation_prompt=True) for i in indexes]
                inputs = tokenizer(texts, padding=True, return_tensors='pt').to('cuda')
                if inputs.input_ids.shape[1] > 3072: raise ValueError('LLM input exceeds locked token budget')
                with torch.inference_mode():
                    scores = label_scores(model, inputs, [c[0] for c in choices])
                if not np.isfinite(scores).all(): raise ValueError('Non-finite LLM logits')
                for i, score in zip(indexes, scores):
                    row = frame.iloc[i]
                    old['rows'][row.segment_id] = {'hash': input_signature(row, True), 'scores': score.tolist(), 'status': 'ok'}
            except (RuntimeError, ValueError) as error:
                if isinstance(error, RuntimeError) and 'out of memory' in str(error).lower(): torch.cuda.empty_cache()
                for i in indexes:
                    row = frame.iloc[i]
                    old['rows'][row.segment_id] = {'hash': input_signature(row, True), 'scores': None, 'status': 'llm_error_fallback', 'error': str(error)[:500]}
            finally:
                del inputs
            torch.cuda.synchronize(); times.append(time.perf_counter()-tick)
            if start % 50 == 0:
                write_json(cache, old); print(f'LLM {cache_name}: {start+len(indexes)}/{len(missing)}', flush=True)
        old['model_revision'] = getattr(model.config, '_commit_hash', None)
        old['hardware'] = hardware()
        old['seconds_per_call']=max(old.get('seconds_per_call',0),(time.perf_counter()-started)/len(missing))
        del model; torch.cuda.empty_cache()
        write_json(cache, old)
    scores, statuses = [], []
    for i in indices:
        row = frame.iloc[int(i)]; entry = old['rows'][row.segment_id]
        if entry['hash'] != input_signature(row, True): raise ValueError('LLM cache input mismatch')
        scores.append(entry['scores'] or [0, 0, 0]); statuses.append(entry['status'])
    return softmax(scores), np.asarray(statuses), {'seconds': time.perf_counter()-started, 'new_calls': len(missing),
            'seconds_per_call':old.get('seconds_per_call'),
            'batch_latency_p50': float(np.quantile(times,.5)) if times else None,
            'batch_latency_p95': float(np.quantile(times,.95)) if times else None, 'hardware': old.get('hardware')}


def blend(base, indexes, values, statuses, weight):
    p = base.copy(); good = statuses == 'ok'
    p[np.asarray(indexes)[good]] = (1-weight)*p[np.asarray(indexes)[good]] + weight*values[good]
    return p


def train(config, args):
    started=time.perf_counter()
    root = Path(config['output_root'])
    if (root / 'selection.lock.json').exists(): raise RuntimeError('Selection frozen')
    if not args.members or len(args.members) != 1: raise ValueError('LLM training requires --members BASE_RUN')
    directory = run_dir(config, args.run); directory.mkdir(parents=True, exist_ok=True)
    frame = load_frame(config['data_root'], 'validation', config)
    base = member_probabilities(config, args.members[0], 'validation', frame)
    maximum = uncertain(base, max(config['llm_fractions']))
    history = []
    for shot_count in [0, 3]:
        shots = examples(config) if shot_count else []
        values, statuses, performance = score_rows(config, frame, maximum, shots, f'{args.run}_validation_{shot_count}')
        positions = {int(index): j for j, index in enumerate(maximum)}
        for fraction in config['llm_fractions']:
            indexes = uncertain(base, fraction); selected = [positions[int(i)] for i in indexes]
            for weight in config['ensemble_weights']:
                p = blend(base, indexes, values[selected], statuses[selected], weight)
                history.append({'shots': shots, 'fraction': fraction, 'weight': weight, 'metrics': metrics(frame.label,p), 'performance':performance})
    base_score = metrics(frame.label, base)['macro_f1']
    test_count=read_json(Path(config['data_root'])/'audit.json')['splits']['test']['segments']
    for candidate in history:
        per_call=candidate['performance'].get('seconds_per_call')
        candidate['estimated_test_seconds']=per_call*math.ceil(test_count*candidate['fraction']) if per_call is not None else None
    budget=getattr(args,'llm_test_budget_seconds',None)
    affordable=[candidate for candidate in history if candidate['estimated_test_seconds'] is not None and (budget is None or candidate['estimated_test_seconds']<=budget)]
    best = max(affordable or history, key=lambda entry: entry['metrics']['macro_f1'])
    choice = {k: best[k] for k in ['shots','fraction','weight']}
    choice['model_revision']=read_json(root/'llm_cache'/f'{args.run}_validation_{len(best["shots"])}.json').get('model_revision')
    choice.update({'base_run':args.members[0], 'improves_validation':bool(affordable) and best['metrics']['macro_f1'] > base_score,
        'test_budget_seconds':budget,'estimated_test_seconds':best['estimated_test_seconds'],'history':history})
    write_json(directory/'selection.json', choice)
    write_json(directory/'metadata.json', {'family':'llm','seed':42,'base_run':args.members[0],'model':config['llm_model'],
               'pilot':not choice['improves_validation'],'train_seconds':time.perf_counter()-started,'environment':environment()})
    if choice['improves_validation']:
        predict(config,args.run,'calibration'); predict(config,args.run,'validation')
    else:
        write_json(directory/'metrics_validation.json', best['metrics'])
    return choice


def predict(config, name, split):
    directory = run_dir(config,name); choice = read_json(directory/'selection.json')
    frame = load_frame(config['data_root'],split,config)
    base = member_probabilities(config,choice['base_run'],split,frame)
    indexes = uncertain(base,choice['fraction'])
    values, statuses, performance = score_rows(dict(config,llm_revision=choice.get('model_revision')),frame,indexes,choice['shots'],f'{name}_{split}_{len(choice["shots"])}')
    p = blend(base,indexes,values,statuses,choice['weight'])
    if split == 'calibration': write_json(directory/'operating_point.json',operating_point(frame.label,p))
    policy = read_json(directory/'operating_point.json')
    used = np.zeros(len(frame),dtype=bool); used[indexes] = True
    status = np.full(len(frame),'ok',dtype=object); status[indexes] = statuses
    write_predictions(directory/f'predictions_{split}.csv.gz',frame,p,name,42,llm_used=used,status=status,flag_ineffective=p[:,0]>=policy['threshold'])
    performance.update({'phase':'conditional LLM branch with cached base predictions',
                        'routed_rows':len(indexes),'all_rows':len(frame),
                        'cache_hits':len(indexes)-performance['new_calls']})
    result = metrics(frame.label,p); result.update({'llm_coverage':float(used.mean()),'llm_routed_rows':int(used.sum()),'llm_errors':int((statuses!='ok').sum()),'performance':performance,
        'component_performance':{choice['base_run']:read_json(run_dir(config,choice['base_run'])/f'metrics_{split}.json').get('performance',{})}})
    write_json(directory/f'metrics_{split}.json',result)
    return result
