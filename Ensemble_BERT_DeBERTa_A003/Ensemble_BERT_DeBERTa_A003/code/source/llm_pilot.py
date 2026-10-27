"""Qwen non-thinking constrained label probabilities; fit-only demonstrations."""
import json
import time
from pathlib import Path
import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from mla_exp.common import digest, softmax, write_json
from mla_exp.data import load_frame
from mla_exp.evaluation import metrics, write_predictions


def text(row):
    return f"Type: {row.discourse_type}\nTarget: {row.discourse_text}\nPrompt: {row.assignment[:500]}\nBefore: {row.left_context[-600:]}\nAfter: {row.right_context[:600]}"


def run_llm(config,run_id,shots=0):
    root=Path(config['output_root'])/'runs'/run_id;root.mkdir(parents=True,exist_ok=False)
    tokenizer=AutoTokenizer.from_pretrained(config['encoder'],revision=config['revision'])
    model=AutoModelForCausalLM.from_pretrained(config['encoder'],revision=config['revision'],device_map='auto',
        quantization_config=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type='nf4',bnb_4bit_compute_dtype=torch.float16,bnb_4bit_use_double_quant=True),
        attn_implementation='sdpa').eval()
    classes=[tokenizer.encode(str(i),add_special_tokens=False) for i in range(3)]
    assert all(len(ids)==1 for ids in classes),'Candidate labels require sequence likelihood, not single-token approximation'
    fit=load_frame(config['data_root'],'fit',config)
    val=load_frame(config['data_root'],'validation',config)
    groups=sorted(val.group_id.unique(),key=lambda x:digest([42,x]))[:20]
    val=val.loc[val.group_id.isin(groups)].reset_index(drop=True)
    system='Classify the effectiveness of the target discourse in a student argumentative essay. 0=Ineffective, 1=Adequate, 2=Effective. Return exactly one digit, without explanation. Judge the target; the surrounding text supplies context.'
    examples=[]
    if shots:
        assert shots==3
        for label in range(3):
            row=fit.loc[fit.label.eq(label)].sort_values('segment_id').iloc[0]
            examples.extend([{'role':'user','content':text(row)},{'role':'assistant','content':str(label)}])
    started=time.perf_counter();scores=[];truncated=[]
    torch.cuda.reset_peak_memory_stats()
    for row in val.itertuples(index=False):
        messages=[{'role':'system','content':system}]+examples+[{'role':'user','content':text(row)}]
        prompt=tokenizer.apply_chat_template(messages,tokenize=False,add_generation_prompt=True,enable_thinking=False)
        tokens=tokenizer(prompt,return_tensors='pt',add_special_tokens=False)
        # Never silently chop target/demonstrations: skip enlargement and report failure.
        if tokens['input_ids'].shape[1]>4096:raise ValueError('LLM input exceeds locked 4096-token budget')
        with torch.inference_mode():
            logits=model(**{k:v.to(model.device) for k,v in tokens.items()}).logits[0,-1]
        scores.append(logits[[ids[0] for ids in classes]].float().cpu().numpy())
        truncated.append(False)
        if len(scores)%20==0:print('LLM_PILOT',shots,len(scores),'/',len(val),flush=True)
    probability=softmax(np.asarray(scores))
    result=metrics(val.label,probability)
    result['performance']={'seconds':time.perf_counter()-started,'examples_second':len(val)/(time.perf_counter()-started),'peak_vram_bytes':torch.cuda.max_memory_allocated()}
    write_predictions(root/'predictions_validation.csv.gz',val,probability,run_id,42)
    write_json(root/'metrics_validation.json',result)
    write_json(root/'metadata.json',{'family':'llm','pilot':True,'shots':shots,'encoder':config['encoder'],'revision':config['revision'],'label_token_ids':classes,'scoring':'conditional normalized probability over digit label tokens; not free-generation parsing','validation_essays':20,'fit_only_demonstrations':True,'config':config})
    print('LLM_METRICS',json.dumps(result));return result
