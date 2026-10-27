"""Locked evaluation of an existing standard classifier or a new span checkpoint."""
import json
import time
import shutil
from pathlib import Path
import numpy as np
import pandas as pd
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from mla_exp.common import digest, now, read_json, sha256, softmax, write_json
from mla_exp.data import load_frame
from mla_exp.neural import batches, gpu
from mla_exp.evaluation import metrics, operating_point, write_predictions, evaluate_file
from span_model import SpanClassifier


def snapshot_model(source,destination):
    """Copy inference artifacts without modifying the selected training run."""
    source=Path(source);destination=Path(destination);destination.mkdir(parents=True,exist_ok=False)
    metadata=read_json(source/'metadata.json')
    for name in ['metadata.json','temperature.json','operating_point.json','selection.json','model.pkl','head_checkpoint.pt']:
        if (source/name).exists():shutil.copy2(source/name,destination/name)
    if (source/'best').exists():shutil.copytree(source/'best',destination/'best')
    if metadata.get('embedding_run'):
        embedding=read_json(source.parent.parent/'embeddings'/metadata['embedding_run']/'fit.json')
        trained_encoder=Path(embedding['source_best'])
        shutil.copytree(trained_encoder,destination/'fine_tuned_encoder')
        shutil.copy2(trained_encoder.parent/'metadata.json',destination/'encoder_metadata.json')
        write_json(destination/'embedding_provenance.json',embedding)
    if metadata.get('family')=='frozen_encoder_sequence':
        from transformers import AutoModel
        cfg=metadata['config']
        encoder=AutoModel.from_pretrained(cfg['encoder'],revision=cfg['revision'])
        encoder.save_pretrained(destination/'pretrained_encoder',safe_serialization=True)
        AutoTokenizer.from_pretrained(cfg['encoder'],revision=cfg['revision']).save_pretrained(destination/'pretrained_encoder')
        del encoder
    if metadata.get('family')=='ensemble':
        choice=read_json(source/'selection.json')
        for i,member in enumerate(choice['members']):snapshot_model(member,destination/'members'/str(i))
    write_json(destination/'snapshot_manifest.json',{'source':str(source),'files':{str(p.relative_to(destination)):sha256(p) for p in destination.rglob('*') if p.is_file()},
               'paths':'Original metadata retains remote source paths; member snapshots are stored under members/<index> and pretrained frozen encoder under pretrained_encoder.'})


def lock_member(source, config, destination):
    source=Path(source)
    metadata=read_json(source/'metadata.json')
    if metadata.get('pilot'):raise ValueError('Pilot cannot be evaluated as a full model')
    if not any((source/name).exists() for name in ['best','model.pkl','selection.json','head_checkpoint.pt']):raise ValueError('Missing trained model')
    artifacts=[p for p in (source/'best').rglob('*') if p.is_file()]
    if (source/'model.pkl').exists():artifacts.append(source/'model.pkl')
    if (source/'head_checkpoint.pt').exists():artifacts.append(source/'head_checkpoint.pt')
    if (source/'selection.json').exists():
        artifacts.append(source/'selection.json')
        for member in read_json(source/'selection.json')['members']:
            member=Path(member)
            artifacts += [p for p in (member/'best').rglob('*') if p.is_file()]
            artifacts += [p for p in member.glob('*.json')]
            if (member/'model.pkl').exists():artifacts.append(member/'model.pkl')
            if (member/'head_checkpoint.pt').exists():artifacts.append(member/'head_checkpoint.pt')
    artifacts += [source/'metadata.json',source/'operating_point.json']
    if (source/'temperature.json').exists():artifacts.append(source/'temperature.json')
    elif not metadata.get('method') in ['lr','svm']:
        raise ValueError('Neural/ensemble inference requires locked temperature')
    dependencies=[source]
    if metadata.get('family')=='ensemble':dependencies += [Path(m) for m in read_json(source/'selection.json')['members']]
    for member in dependencies:
        dependency=read_json(member/'metadata.json')
        if dependency.get('embedding_run'):
            provenance=member.parent.parent/'embeddings'/dependency['embedding_run']/'fit.json'
            artifacts.append(provenance)
            encoder=Path(read_json(provenance)['source_best'])
            artifacts.append(encoder.parent/'metadata.json')
            artifacts += [p for p in encoder.rglob('*') if p.is_file()]
    record={'source':str(source),'files':{str(p):sha256(p) for p in artifacts},'config_digest':digest(config),
            'split_digest':read_json(Path(config['data_root'])/'audit.json')['split_digest'],
            'selected_on':'validation; checkpoint and calibration locked before test'}
    target=Path(destination)/'member_selection.lock.json'
    assert not target.exists(),'Cannot replace locked selection'
    write_json(target,record)
    return record


def infer_member(source,frame,config):
    source=Path(source);meta=read_json(source/'metadata.json')
    if meta.get('family')=='frozen_encoder_sequence':
        from sequence_model import SequenceHead,encode_frame,predict
        cfg=meta['config'];started=time.perf_counter()
        tokenizer=AutoTokenizer.from_pretrained(cfg['encoder'],revision=cfg['revision'])
        from transformers import AutoModel
        encoder=AutoModel.from_pretrained(cfg['encoder'],revision=cfg['revision']).to(gpu())
        vectors,flags=encode_frame(frame,encoder,tokenizer,cfg,return_flags=True);del encoder;torch.cuda.empty_cache()
        state=torch.load(source/'head_checkpoint.pt',map_location='cpu',weights_only=False)
        head=SequenceHead(state['width'],state['contextual']).to('cuda');head.load_state_dict(state['model'])
        scores=predict(head,frame,vectors);del head;torch.cuda.empty_cache()
        p=softmax(scores/read_json(source/'temperature.json')['temperature']);elapsed=time.perf_counter()-started
        return p,flags,{'seconds':elapsed,'examples_second':len(frame)/elapsed,'context':'ordered gold segments, frozen encoder','peak_vram_bytes':torch.cuda.max_memory_allocated()}
    if meta.get('family')=='ensemble':
        choice=read_json(source/'selection.json')
        a,flags,pa=infer_member(choice['members'][0],frame,config)
        b,bflags,pb=infer_member(choice['members'][1],frame,config)
        assert len(flags)==len(bflags)==len(frame), 'Ensemble truncation coverage mismatch'
        flags=[{key:bool(fa[key] or fb[key]) for key in ['target_truncated','context_truncated']}
               for fa,fb in zip(flags,bflags)]
        mixture=choice['weight']*a+(1-choice['weight'])*b
        p=softmax(np.log(np.clip(mixture,1e-12,1))/choice['temperature'])
        elapsed=pa['seconds']+pb['seconds']
        return p,flags,{'seconds':elapsed,'examples_second':len(frame)/elapsed,'members':[pa,pb],
                       'truncation_policy':'Flagged when any ensemble member truncates target/context'}
    if meta.get('method') in ['lr','svm']:
        import pickle
        from mla_exp.classical import raw_probabilities
        started=time.perf_counter()
        flags=[{'target_truncated':False,'context_truncated':False}]*len(frame)
        with (source/'model.pkl').open('rb') as file:artifact=pickle.load(file)
        if meta.get('embedding_run') and frame.split.eq('test').all():
            from hybrid_model import embeddings
            feature=artifact['model'].named_steps['features']
            embedding_record=read_json(Path(feature.embedding_root)/'embeddings'/meta['embedding_run']/'fit.json')
            source_best=embedding_record.get('source_best')
            if not source_best:raise ValueError('This evaluator requires a task-aware source checkpoint for test embeddings')
            identity=read_json(Path(source_best).parent/'metadata.json')['identity']
            config=dict(config,max_length=embedding_record.get('max_length',identity['max_length']),batch_size=embedding_record.get('batch_size',identity['batch_size']))
            embeddings(config,source_best,meta['embedding_run'],'test',frame=frame)
            feature.embedding_root=config['output_root']
            measured=np.load(Path(config['output_root'])/'embeddings'/meta['embedding_run']/'test_flags.npy')
            assert measured.shape==(len(frame),2)
            flags=[{'target_truncated':bool(a),'context_truncated':bool(b)} for a,b in measured]
        p=raw_probabilities(artifact['model'],frame) if artifact.get('probability_mode')=='raw' else artifact['calibrator'].predict_proba(frame)
        elapsed=time.perf_counter()-started
        return p,flags,{'seconds':elapsed,'examples_second':len(frame)/elapsed,'cached_embedding_cost_excluded':True}
    config=dict(config,max_length=meta['identity']['max_length'],batch_size=meta['identity']['batch_size'])
    tokenizer=AutoTokenizer.from_pretrained(source/'best')
    is_span=(source/'best/span_head.json').exists()
    factory=SpanClassifier if is_span else AutoModelForSequenceClassification
    model=factory.from_pretrained(source/'best').to(gpu()).eval()
    values=[];flags=[];started=time.perf_counter()
    torch.cuda.reset_peak_memory_stats()
    with torch.inference_mode():
        for inputs,mask,row_flags,_ in batches(frame,tokenizer,config,meta['context']):
            kwargs={k:v.to('cuda') for k,v in inputs.items()}
            if is_span:kwargs['target_mask']=mask.to('cuda')
            with torch.autocast('cuda',dtype=torch.float16):logits=model(**kwargs).logits
            assert torch.isfinite(logits).all()
            values.append(logits.float().cpu().numpy());flags.extend(row_flags)
    elapsed=time.perf_counter()-started
    peak=torch.cuda.max_memory_allocated();del model;torch.cuda.empty_cache()
    p=softmax(np.concatenate(values)/read_json(source/'temperature.json')['temperature'])
    return p,flags,{'seconds':elapsed,'examples_second':len(frame)/elapsed,'peak_vram_bytes':peak}


def evaluate_locked_member(source,config,output):
    output=Path(output);output.mkdir(parents=True,exist_ok=False)
    lock=lock_member(source,config,output)
    # This output owns the test lock; it does not modify any source model run.
    config=dict(config)
    audit=read_json(Path(config['data_root'])/'audit.json')
    write_json(output/'selection.lock.json',{'config_digest':digest(config),'split_digest':audit['split_digest'],
                                           'prepared_sha256':audit['prepared_sha256']})
    root_lock=Path(config['output_root'])/'selection.lock.json'
    if not root_lock.exists():
        write_json(root_lock,read_json(output/'selection.lock.json'))
    else:
        assert read_json(root_lock)['config_digest']==digest(config)
    frame=load_frame(config['data_root'],'test',config,output=output)
    write_json(output/'test_access.json',{'opened_at':now(),'segments':len(frame),'essays':int(frame.group_id.nunique()),
                                        'selection_lock':'member_selection.lock.json','tuning_after_test_permitted':False})
    for path,expected in lock['files'].items():assert sha256(path)==expected,'Source changed after lock'
    snapshot_model(source,output/'frozen_model')
    p,flags,performance=infer_member(source,frame,config)
    policy=read_json(Path(source)/'operating_point.json')
    write_predictions(output/'predictions_test.csv.gz',frame,p,output.name,42,
                      flag_ineffective=p[:,0]>=policy['threshold'],
                      target_truncated=[f['target_truncated'] for f in flags],
                      context_truncated=[f['context_truncated'] for f in flags])
    result=dict(metrics(frame.label,p),performance=performance)
    write_json(output/'metrics_test.json',result)
    write_json(output/'metadata.json',{'family':'locked_evaluation','pilot':False,'source':str(source),'config':config,
                                     'selection_source':'member_selection.lock.json','test_tuning_permitted':False})
    evaluated=evaluate_file(output/'predictions_test.csv.gz',output/'evaluation_test.json',repeats=2000,data_root=config['data_root'])
    print('FINAL_TEST',json.dumps(result),flush=True)
    return evaluated


def choose_ensemble(source_a,source_b,config,output):
    """Use validation weights; calibrate the mixture on separate calibration."""
    from mla_exp.neural import temperature
    output=Path(output);output.mkdir(parents=True,exist_ok=False)
    val=load_frame(config['data_root'],'validation',config)
    calibration=load_frame(config['data_root'],'calibration',config)
    def saved_probabilities(source,split,frame):
        rows=pd.read_csv(Path(source)/('predictions_'+split+'.csv.gz'))
        assert not rows.segment_id.duplicated().any() and set(rows.segment_id)==set(frame.segment_id)
        rows=rows.set_index('segment_id').loc[frame.segment_id].reset_index()
        assert np.array_equal(rows.label.to_numpy(),frame.label.to_numpy())
        assert np.array_equal(rows.group_id.to_numpy(),frame.group_id.to_numpy())
        from mla_exp.common import check_probabilities
        return check_probabilities(rows[['p_0','p_1','p_2']].to_numpy())
    va=saved_probabilities(source_a,'validation',val);vb=saved_probabilities(source_b,'validation',val)
    candidates=[]
    for weight in [.25,.5,.75]:
        result=metrics(val.label,weight*va+(1-weight)*vb)
        candidates.append({'weight':weight,'metrics':result})
    selected=max(candidates,key=lambda row:row['metrics']['macro_f1'])
    ca=saved_probabilities(source_a,'calibration',calibration);cb=saved_probabilities(source_b,'calibration',calibration)
    mixture=selected['weight']*ca+(1-selected['weight'])*cb
    scale=temperature(np.log(np.clip(mixture,1e-12,1)),calibration.label)
    calibrated=softmax(np.log(np.clip(mixture,1e-12,1))/scale)
    policy=operating_point(calibration.label,calibrated)
    vp=softmax(np.log(np.clip(selected['weight']*va+(1-selected['weight'])*vb,1e-12,1))/scale)
    write_json(output/'selection.json',{'members':[str(source_a),str(source_b)],'weight':selected['weight'],'search':candidates,'temperature':scale,'operating_point':policy,'selected_without_test':True,'selection_predictions':'Existing validation/calibration CSVs with exact ID/group/label alignment; no repeated GPU inference','prediction_sha256':{str(Path(source)/('predictions_'+split+'.csv.gz')):sha256(Path(source)/('predictions_'+split+'.csv.gz')) for source in [source_a,source_b] for split in ['validation','calibration']}})
    write_json(output/'metadata.json',{'family':'ensemble','pilot':False,'seed':42,'members':[str(source_a),str(source_b)],'config':config})
    write_json(output/'temperature.json',{'temperature':scale})
    write_json(output/'operating_point.json',policy)
    write_predictions(output/'predictions_validation.csv.gz',val,vp,output.name,42,flag_ineffective=vp[:,0]>=policy['threshold'])
    write_predictions(output/'predictions_calibration.csv.gz',calibration,calibrated,output.name,42,flag_ineffective=calibrated[:,0]>=policy['threshold'])
    write_json(output/'metrics_validation.json',metrics(val.label,vp))
    snapshot_model(source_a,output/'frozen_members'/'0')
    snapshot_model(source_b,output/'frozen_members'/'1')
    return metrics(val.label,vp)
