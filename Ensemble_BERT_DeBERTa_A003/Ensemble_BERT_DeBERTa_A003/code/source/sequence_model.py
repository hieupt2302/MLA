"""Frozen RoBERTa segment representations + independent or BiLSTM heads."""
import json
import copy
import time
from pathlib import Path

import numpy as np
import torch
from torch import nn
from transformers import AutoModel, AutoTokenizer

from mla_exp.common import digest, softmax, write_json
from mla_exp.data import load_frame, small_fit
from mla_exp.evaluation import metrics, write_predictions
from mla_exp.neural import batches, gpu, seed_all


class SequenceHead(nn.Module):
    def __init__(self, width, contextual):
        super().__init__()
        self.contextual = contextual
        self.lstm = nn.LSTM(width, width//2, batch_first=True, bidirectional=True) if contextual else None
        self.classifier = nn.Linear(width, 3)

    def forward(self, vectors, lengths):
        if self.contextual:
            # Packing prevents padded segments from changing backward context.
            packed = nn.utils.rnn.pack_padded_sequence(vectors, lengths.cpu(), batch_first=True, enforce_sorted=False)
            encoded,_ = self.lstm(packed)
            vectors,_ = nn.utils.rnn.pad_packed_sequence(encoded, batch_first=True, total_length=vectors.shape[1])
        return self.classifier(vectors)


def encode_frame(frame, encoder, tokenizer, config, return_flags=False):
    vectors=[];flags=[]
    encoder.eval()
    with torch.inference_mode():
        for inputs,mask,row_flags,_ in batches(frame,tokenizer,config,False):
            flags.extend(row_flags)
            with torch.autocast('cuda',dtype=torch.float16):
                hidden=encoder(**{k:v.to('cuda') for k,v in inputs.items()}).last_hidden_state
                weights=mask.to('cuda').unsqueeze(-1).to(hidden.dtype)
                vector=(hidden*weights).sum(1)/weights.sum(1)
            assert torch.isfinite(vector).all()
            vectors.append(vector.float().cpu())
    values=torch.cat(vectors)
    return (values,flags) if return_flags else values


def essay_batches(frame, vectors, size, shuffle=False, seed=42):
    essays=[g.sort_values(['discourse_start','discourse_end','segment_id']).index.to_numpy() for _,g in frame.groupby('group_id',sort=True)]
    if shuffle:
        order=np.random.default_rng(seed).permutation(len(essays));essays=[essays[i] for i in order]
    for start in range(0,len(essays),size):
        groups=essays[start:start+size]
        length=torch.tensor([len(g) for g in groups])
        x=nn.utils.rnn.pad_sequence([vectors[g] for g in groups],batch_first=True).to('cuda')
        y=nn.utils.rnn.pad_sequence([torch.tensor(frame.loc[g,'label'].to_numpy(),dtype=torch.long) for g in groups],batch_first=True,padding_value=-100).to('cuda')
        yield x,y,length,groups


def predict(head,frame,vectors):
    scores=np.empty((len(frame),3),dtype=np.float32);head.eval()
    with torch.inference_mode():
        for x,y,lengths,groups in essay_batches(frame,vectors,8):
            logits=head(x,lengths).float().cpu().numpy()
            for i,index in enumerate(groups):scores[index]=logits[i,:len(index)]
    assert np.isfinite(scores).all()
    return scores


def train_sequence(config, run_id, contextual=True):
    device=gpu();seed_all(42)
    destination=Path(config['output_root'])/'runs'/run_id;destination.mkdir(parents=True,exist_ok=False)
    pilot=config.get('mode','pilot')=='pilot'
    fit=load_frame(config['data_root'],'fit',config)
    if pilot:fit=small_fit(fit,42)
    val=load_frame(config['data_root'],'validation',config)
    if pilot:
        groups=sorted(val.group_id.unique(),key=lambda x:digest([42,x]))[:200]
        val=val.loc[val.group_id.isin(groups)].reset_index(drop=True)
    tokenizer=AutoTokenizer.from_pretrained(config['encoder'],revision=config['revision'])
    encoder=AutoModel.from_pretrained(config['encoder'],revision=config['revision']).to(device)
    started=time.perf_counter();width=encoder.config.hidden_size
    fv=encode_frame(fit,encoder,tokenizer,config);vv=encode_frame(val,encoder,tokenizer,config)
    # All encoder vectors are frozen and labels remain loss targets only.
    np.save(destination/'embeddings_fit.npy',fv.numpy());np.save(destination/'embeddings_validation.npy',vv.numpy())
    write_json(destination/'embedding_ids.json',{'fit':fit.segment_id.tolist(),'validation':val.segment_id.tolist(),'encoder_frozen':True,'revision':config['revision']})
    del encoder;torch.cuda.empty_cache()
    head=SequenceHead(width,contextual).to(device)
    optimizer=torch.optim.AdamW(head.parameters(),lr=1e-3,weight_decay=.01)
    counts=np.bincount(fit.label,minlength=3)
    loss_fn=nn.CrossEntropyLoss(weight=torch.tensor(len(fit)/(3*counts),dtype=torch.float32,device=device),ignore_index=-100)
    x,y,lengths,_=next(essay_batches(fit,fv,2))
    def step(candidate,opt):
        opt.zero_grad(set_to_none=True)
        loss=loss_fn(candidate(x,lengths).reshape(-1,3),y.reshape(-1))
        assert torch.isfinite(loss);loss.backward();nn.utils.clip_grad_norm_(candidate.parameters(),1);opt.step()
    initial=copy.deepcopy(head.state_dict())
    step(head,optimizer)
    assert any(not torch.equal(v,initial[k]) for k,v in head.state_dict().items())
    state={'head':copy.deepcopy(head.state_dict()),'optimizer':copy.deepcopy(optimizer.state_dict())}
    clone=SequenceHead(width,contextual).to(device);clone.load_state_dict(state['head'])
    clone_opt=torch.optim.AdamW(clone.parameters(),lr=1e-3,weight_decay=.01);clone_opt.load_state_dict(state['optimizer'])
    step(head,optimizer);step(clone,clone_opt)
    assert all(torch.allclose(v,clone.state_dict()[k],atol=1e-6,rtol=1e-4) for k,v in head.state_dict().items())
    print('SEQUENCE_CUDA_RESUME_PASS',contextual,flush=True)
    del clone,clone_opt,state
    head.load_state_dict(initial);optimizer=torch.optim.AdamW(head.parameters(),lr=1e-3,weight_decay=.01)
    history=[];best=-1;best_state=None
    for epoch in range(1 if pilot else config['epochs']):
        head.train()
        for x,y,lengths,_ in essay_batches(fit,fv,8,True,42+epoch):
            optimizer.zero_grad(set_to_none=True);loss=loss_fn(head(x,lengths).reshape(-1,3),y.reshape(-1))
            assert torch.isfinite(loss);loss.backward();nn.utils.clip_grad_norm_(head.parameters(),1);optimizer.step()
        scores=predict(head,val,vv);result=metrics(val.label,softmax(scores));history.append({'epoch':epoch+1,**result})
        print('SEQUENCE_EPOCH',json.dumps(history[-1]),flush=True)
        torch.save({'model':head.state_dict(),'optimizer':optimizer.state_dict(),'python_rng':__import__('random').getstate(),
                    'numpy_rng':np.random.get_state(),'rng':torch.get_rng_state(),'cuda_rng':torch.cuda.get_rng_state_all(),
                    'epoch':epoch+1,'cursor':len(fit),'width':width,'contextual':contextual,'config':config,
                    'scheduler':None,'scaler':None,'precision':'float32 head, float16 frozen encoder','history':history},
                   destination/f'training_epoch_{epoch+1:02d}.pt')
        if result['macro_f1']>best:
            best=result['macro_f1'];best_state=copy.deepcopy(head.state_dict())
        elif not pilot:break
    head.load_state_dict(best_state)
    scores=predict(head,val,vv);scale=1.;policy=None
    if not pilot:
        from mla_exp.neural import temperature
        from mla_exp.evaluation import operating_point
        calibration=load_frame(config['data_root'],'calibration',config)
        encoder=AutoModel.from_pretrained(config['encoder'],revision=config['revision']).to(device)
        cv=encode_frame(calibration,encoder,tokenizer,config)
        del encoder;torch.cuda.empty_cache()
        cs=predict(head,calibration,cv);scale=temperature(cs,calibration.label)
        cp=softmax(cs/scale);policy=operating_point(calibration.label,cp)
        write_predictions(destination/'predictions_calibration.csv.gz',calibration,cp,run_id,42,flag_ineffective=cp[:,0]>=policy['threshold'])
        write_json(destination/'metrics_calibration.json',metrics(calibration.label,cp))
        write_json(destination/'temperature.json',{'temperature':scale})
        write_json(destination/'operating_point.json',policy)
    vp=softmax(scores/scale);result=metrics(val.label,vp)
    extra={'flag_ineffective':vp[:,0]>=policy['threshold']} if policy else {}
    write_predictions(destination/'predictions_validation.csv.gz',val,vp,run_id,42,**extra)
    write_json(destination/'metrics_validation.json',result)
    write_json(destination/'metadata.json',{'family':'frozen_encoder_sequence','pilot':pilot,'contextual':contextual,'epochs':len(history),'revision':config['revision'],'train_segments':len(fit),'validation_segments':len(val),'history':history,'seconds':time.perf_counter()-started,'config':config})
    torch.save({'model':head.state_dict(),'width':width,'contextual':contextual,'purpose':'selected best head for inference; separate training_epoch_XX.pt files contain matching optimizer/RNG states'},destination/'head_checkpoint.pt')
    return result
