"""Fine-tuned target embeddings plus fit-only lexical features; no in-sample stacking."""
import time
import shutil
from pathlib import Path
from types import SimpleNamespace
import numpy as np
import torch
from transformers import AutoModel, AutoTokenizer
from mla_exp.classical import input_signature, train
from mla_exp.common import digest, read_json, sha256, write_json
from mla_exp.data import load_frame
from mla_exp.neural import batches, gpu


def embeddings(config,source_best,name,split,frame=None):
    source=Path(source_best)
    weights={p.relative_to(source).as_posix():sha256(p) for p in source.rglob('*') if p.is_file()}
    signature=digest({'weights':weights,'pooling':'target_mean','max_length':config['max_length'],'context':True})
    if frame is None:frame=load_frame(config['data_root'],split,config)
    else:
        # The evaluator already verified the test lock before handing over
        # this frame. Each frozen ensemble member retains its own input length.
        assert split=='test' and frame.split.eq('test').all()
        assert (Path(config['output_root'])/'selection.lock.json').exists()
    target=Path(config['output_root'])/'embeddings'/name;target.mkdir(parents=True,exist_ok=True)
    assert not (target/(split+'.npy')).exists(),'Embedding exists; no overwrite'
    encoder=AutoModel.from_pretrained(source/'encoder' if (source/'encoder').exists() else source).to(gpu()).eval()
    tokenizer=AutoTokenizer.from_pretrained(source)
    matrix=np.lib.format.open_memmap(target/(split+'.partial.npy'),mode='w+',dtype=np.float32,shape=(len(frame),encoder.config.hidden_size))
    start=time.perf_counter();cursor=0;flags=np.zeros((len(frame),2),dtype=bool)
    with torch.inference_mode():
        for inputs,mask,row_flags,_ in batches(frame,tokenizer,config,True):
            with torch.autocast('cuda',dtype=torch.float16):
                hidden=encoder(**{k:v.to('cuda') for k,v in inputs.items()}).last_hidden_state
                weight=mask.to('cuda').unsqueeze(-1).to(hidden.dtype)
                result=(hidden*weight).sum(1)/weight.sum(1)
            assert torch.isfinite(result).all()
            values=result.float().cpu().numpy();matrix[cursor:cursor+len(values)]=values
            flags[cursor:cursor+len(values)]=[[f['target_truncated'],f['context_truncated']] for f in row_flags]
            cursor+=len(values)
            if cursor%2000<config['batch_size']:print('TASK_EMBEDDING',split,cursor,len(frame),flush=True)
    matrix.flush();del matrix
    (target/(split+'.partial.npy')).rename(target/(split+'.npy'))
    np.save(target/(split+'_flags.npy'),flags)
    write_json(target/(split+'.json'),{'model_signature':signature,'context':True,'task_aware':True,
        'max_length':config['max_length'],'batch_size':config['batch_size'],
        'source_run':None,'source_best':str(source),'source_weight_sha256':weights,'pooling':'target_mean',
        'segment_ids':frame.segment_id.tolist(),'input_hashes':[input_signature(row,True) for _,row in frame.iterrows()],
        'array_sha256':sha256(target/(split+'.npy')),'seconds':time.perf_counter()-start})
    del encoder;torch.cuda.empty_cache()


def run_hybrid(config,run_id,source_best):
    source=Path(source_best);meta=read_json(source.parent/'metadata.json')
    assert not meta.get('pilot'),'Full hybrid requires a full fit-only encoder'
    dependency=Path(config['output_root'])/'dependencies'/'task_encoder'
    dependency.mkdir(parents=True,exist_ok=False)
    shutil.copytree(source,dependency/'best')
    shutil.copy2(source.parent/'metadata.json',dependency/'metadata.json')
    source_best=str(dependency/'best')
    config=dict(config,max_length=meta['identity']['max_length'],c_grid=[.1,1.0],class_weights=['balanced'],embedding_weights=[.25,1.0],cv_jobs=1)
    for split in ['fit','validation','calibration']:embeddings(config,source_best,'task_target',split)
    args=SimpleNamespace(method='lr',run=run_id,context=True,embedding_run='task_target',seed=42)
    return train(config,args)
