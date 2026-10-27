"""Colab-only measurement from raw text to final probabilities, without caches."""
import pickle
import time
from pathlib import Path
from unittest.mock import patch

import numpy as np

from .common import check_probabilities, digest, environment, read_json, sha256, softmax, write_json
from .classical import run_dir, raw_probabilities, verify_lock
from .data import load_frame


class Pipeline:
    def __init__(self, config):
        from .neural import gpu
        self.device=gpu(); self.config=config
        self.runs={}; self.encoders={}; self.llm_errors=0; self.llm_rows=0

    def load(self, name):
        import torch
        from transformers import AutoModelForSequenceClassification, AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
        if name in self.runs: return
        if (Path(self.config['output_root'])/'selection.lock.json').exists(): verify_lock(self.config,name)
        directory=run_dir(self.config,name); meta=read_json(directory/'metadata.json')
        record={'meta':meta}; self.runs[name]=record
        family=meta['family']
        if family=='neural':
            record.update(model=AutoModelForSequenceClassification.from_pretrained(directory/'best').to(self.device).eval(),
                          tokenizer=AutoTokenizer.from_pretrained(directory/'best'),
                          config=dict(self.config,**{key:meta['identity'][key] for key in ['max_length','batch_size','amp_dtype']}),
                          temperature=read_json(directory/'temperature.json')['temperature'])
        elif family in ['ensemble','llm']:
            choice=read_json(directory/'selection.json'); record['choice']=choice
            for member in choice.get('members',[choice.get('base_run')]): self.load(member)
            if family=='llm':
                record['tokenizer']=AutoTokenizer.from_pretrained(self.config['llm_model'],revision=choice['model_revision'],padding_side='right')
                choices=[record['tokenizer'].encode(letter,add_special_tokens=False) for letter in 'ABC']
                if any(len(value)!=1 for value in choices): raise ValueError('Label choices must each be one token')
                record['choices']=[value[0] for value in choices]
                quant=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type='nf4',bnb_4bit_compute_dtype=torch.float16)
                record['model']=AutoModelForCausalLM.from_pretrained(self.config['llm_model'],revision=choice['model_revision'],quantization_config=quant,device_map={'':0},attn_implementation='sdpa').eval()
        else:
            with (directory/'model.pkl').open('rb') as stream: record['artifact']=pickle.load(stream)
            if meta.get('embedding_run'): self.load_embedding(meta['embedding_run'])

    def load_embedding(self, name):
        from transformers import AutoModel, AutoTokenizer
        from .neural import amp_dtype
        if name in self.encoders: return
        record=read_json(Path(self.config['output_root'])/'embeddings'/name/'fit.json')
        if record.get('source_run') and (Path(self.config['output_root'])/'selection.lock.json').exists(): verify_lock(self.config,record['source_run'])
        source=run_dir(self.config,record['source_run'])/'best' if record.get('source_run') else record['encoder']
        cfg=dict(self.config,amp_dtype=record['hardware']['amp_dtype'])
        if record.get('source_run'):
            identity=read_json(Path(source).parent/'metadata.json')['identity']
            cfg.update({key:identity[key] for key in ['max_length','batch_size','amp_dtype']})
        tokenizer=AutoTokenizer.from_pretrained(source); model=AutoModel.from_pretrained(source).to(self.device).eval()
        weights={p.name:sha256(p) for p in Path(source).glob('*.safetensors')} if record.get('source_run') else None
        signature=digest({'encoder':record['encoder'],'revision':getattr(model.config,'_commit_hash',None),'weights':weights,
                          'pooling':record['pooling'],'context':record['context'],'max_length':cfg['max_length'],
                          'vocab':digest(tokenizer.get_vocab()),'amp_dtype':str(amp_dtype(cfg)),
                          'tokenizer_config':digest(tokenizer.init_kwargs),'encoding_sha256':sha256(Path(__file__).with_name('encoding.py'))})
        if signature!=record['model_signature']: raise ValueError('Live encoder differs from training embedding identity')
        self.encoders[name]={'model':model,'tokenizer':tokenizer,'config':cfg,'record':record}

    def embedding(self, name, frame):
        import torch
        from .neural import batches, amp_dtype
        endpoint=self.encoders[name]; record=endpoint['record']; values=[]
        with torch.inference_mode():
            for inputs,mask,_,_ in batches(frame,endpoint['tokenizer'],endpoint['config'],record['context']):
                with torch.autocast('cuda',dtype=amp_dtype(endpoint['config'])):
                    hidden=endpoint['model'](**{key:value.to(self.device) for key,value in inputs.items()}).last_hidden_state.float()
                if record['pooling']=='cls': vector=hidden[:,0]
                else:
                    mask=mask.to(self.device).unsqueeze(-1)
                    vector=(hidden*mask).sum(axis=1)/mask.sum(axis=1).clamp(min=1)
                values.append(vector.cpu().numpy())
        return np.concatenate(values)

    def predict(self, name, frame, computed=None):
        import torch
        from .neural import batches, amp_dtype
        if computed is None: computed={}
        key=('prediction',name)
        if key in computed: return computed[key]
        record=self.runs[name]; family=record['meta']['family']
        if family=='neural':
            scores=[]
            with torch.inference_mode():
                for inputs,_,_,_ in batches(frame,record['tokenizer'],record['config'],record['meta']['context']):
                    with torch.autocast('cuda',dtype=amp_dtype(record['config'])):
                        logits=record['model'](**{key:value.to(self.device) for key,value in inputs.items()}).logits
                    scores.append(logits.float().cpu().numpy())
            p=softmax(np.concatenate(scores)/record['temperature'])
        elif family=='ensemble':
            choice=record['choice']
            p=sum(weight*self.predict(member,frame,computed) for member,weight in zip(choice['members'],choice['weights']))
        elif family=='llm':
            from .llm import uncertain, messages, label_scores, blend
            choice=record['choice']; base=self.predict(choice['base_run'],frame,computed)
            indexes=uncertain(base,choice['fraction']); scores=[]; statuses=[]
            self.llm_rows+=len(indexes)
            for start in range(0,len(indexes),2):
                ids=indexes[start:start+2]
                try:
                    texts=[record['tokenizer'].apply_chat_template(messages(record['tokenizer'],frame.iloc[int(i)],choice['shots']),tokenize=False,add_generation_prompt=True) for i in ids]
                    inputs=record['tokenizer'](texts,padding=True,return_tensors='pt').to(self.device)
                    if inputs.input_ids.shape[1]>3072: raise ValueError('LLM input exceeds locked token budget')
                    with torch.inference_mode(): values=label_scores(record['model'],inputs,record['choices'])
                    if not np.isfinite(values).all(): raise ValueError('Nonfinite logits')
                    scores.extend(values); statuses.extend(['ok']*len(ids))
                except (RuntimeError,ValueError):
                    torch.cuda.empty_cache(); self.llm_errors+=len(ids)
                    scores.extend([[0,0,0]]*len(ids)); statuses.extend(['llm_error_fallback']*len(ids))
            p=blend(base,indexes,softmax(scores),np.asarray(statuses),choice['weight'])
        else:
            artifact=record['artifact']; embedding=record['meta'].get('embedding_run')
            if artifact['dummy']: p=artifact['model'].predict_proba(np.zeros((len(frame),1)))
            else:
                if embedding and ('embedding',embedding) not in computed: computed[('embedding',embedding)]=self.embedding(embedding,frame)
                def fresh_embeddings(root,requested,rows,expected_signature=None):
                    if requested!=embedding or len(rows)!=len(frame) or not np.array_equal(rows.segment_id,frame.segment_id): raise ValueError('Live feature alignment mismatch')
                    if expected_signature!=self.encoders[embedding]['record']['model_signature']: raise ValueError('Live feature identity mismatch')
                    return computed[('embedding',embedding)]
                with patch('mla_exp.classical.cached_embeddings',fresh_embeddings) if embedding else patch('mla_exp.classical.cached_embeddings',side_effect=RuntimeError('Unexpected embedding lookup')):
                    p=raw_probabilities(artifact['model'],frame) if artifact.get('probability_mode')=='raw' else artifact['calibrator'].predict_proba(frame)
        computed[key]=check_probabilities(p)
        return computed[key]


def benchmark(config, name, split='test', batch_size=128, repeats=10):
    import torch
    from .neural import hardware
    if split=='test': verify_lock(config,name)
    frame=load_frame(config['data_root'],split,config)
    sample=frame.sample(n=min(len(frame),batch_size*repeats),random_state=2026).reset_index(drop=True)
    started=time.perf_counter(); pipeline=Pipeline(config); pipeline.load(name)
    torch.cuda.synchronize(); load_seconds=time.perf_counter()-started
    pipeline.predict(name,sample.iloc[:min(8,len(sample))]); torch.cuda.synchronize()
    pipeline.llm_errors=pipeline.llm_rows=0; torch.cuda.reset_peak_memory_stats(); times=[]; outputs=[]
    for offset in range(0,len(sample),batch_size):
        batch=sample.iloc[offset:offset+batch_size]; torch.cuda.synchronize(); tick=time.perf_counter()
        outputs.append(pipeline.predict(name,batch)); torch.cuda.synchronize(); times.append(time.perf_counter()-tick)
    result={'run':name,'split':split,'phase':'raw text to final probabilities, resident models, no saved embeddings or predictions',
            'rows':len(sample),'batch_size':batch_size,'measured_batches':len(times),'warmup_rows':min(8,len(sample)),
            'model_load_seconds':load_seconds,'seconds':sum(times),'examples_second':len(sample)/sum(times),
            'batch_latency_p50':float(np.quantile(times,.5)),'batch_latency_p95':float(np.quantile(times,.95)),
            'batch_seconds':times,'sample_ids_digest':digest(sample.segment_id.tolist()),'hardware':hardware(),
            'llm_routed_rows':pipeline.llm_rows,'llm_errors':pipeline.llm_errors,
            'protocol':'Fixed seed 2026 input batches. Conditional entropy routing ranks within each population batch; rounded coverage may differ from the full-test quality benchmark. Labels are not scored or used for selection.',
            'environment':environment()}
    result['hardware'].pop('amp_dtype',None)
    result['neural_amp_dtypes']={run:record['config']['amp_dtype'] for run,record in pipeline.runs.items() if record['meta']['family']=='neural'}
    result['embedding_amp_dtypes']={run:record['config']['amp_dtype'] for run,record in pipeline.encoders.items()}
    if any(record['meta']['family']=='llm' for record in pipeline.runs.values()): result['llm_compute_dtype']='torch.float16'
    if pipeline.runs[name]['meta']['family']!='llm':
        import pandas as pd
        saved=pd.read_csv(run_dir(config,name)/f'predictions_{split}.csv.gz').set_index('segment_id').loc[sample.segment_id,['p_0','p_1','p_2']].to_numpy()
        difference=float(np.abs(saved-np.concatenate(outputs)).max())
        result['max_abs_probability_difference_from_saved']=difference
        if difference>.02: raise RuntimeError('Live pipeline differs from saved predictions by more than 0.02')
    write_json(run_dir(config,name)/f'uncached_performance_{split}.json',result)
    return result
