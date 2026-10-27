"""Paired 20-essay routing pilot using already-executed LLM predictions."""
from pathlib import Path
import numpy as np
import pandas as pd
from mla_exp.common import read_json,write_json
from mla_exp.evaluation import metrics,bootstrap


def review_route(config,run_id):
    out=Path(config['output_root'])/'runs'/run_id
    out.mkdir(parents=True,exist_ok=False)
    llm_source=Path(config['source_b']);base_source=Path(config['source_best'])
    lm=read_json(llm_source/'metadata.json');bm=read_json(base_source/'metadata.json')
    assert lm['pilot'] and not bm.get('pilot'), 'Expected LLM pilot and full baseline'
    llm=pd.read_csv(llm_source/'predictions_validation.csv.gz')
    base=pd.read_csv(base_source/'predictions_validation.csv.gz')
    assert not base.segment_id.duplicated().any() and not llm.segment_id.duplicated().any()
    baseline=base.set_index('segment_id').loc[llm.segment_id].reset_index()
    assert baseline.segment_id.tolist()==llm.segment_id.tolist()
    assert baseline.label.tolist()==llm.label.tolist()
    assert baseline.group_id.tolist()==llm.group_id.tolist()
    assert llm.group_id.nunique()==20
    columns=['p_0','p_1','p_2'];p=baseline[columns].to_numpy();q=llm[columns].to_numpy()
    baseline_metrics=metrics(llm.label,p)
    entropy=-(np.clip(p,1e-12,1)*np.log(np.clip(p,1e-12,1))).sum(1)
    order=np.lexsort((llm.segment_id.astype(str).to_numpy(),-entropy))
    trials=[]
    for fraction in [.02,.05,.10]:
        count=max(1,int(np.ceil(len(llm)*fraction)));selected=order[:count]
        mixed=p.copy();mixed[selected]=q[selected]
        score=metrics(llm.label,mixed)
        paired=bootstrap(llm,mixed,repeats=2000,other=p)
        trials.append({'fraction':fraction,'routed':count,'metrics':score,'paired_gain_bootstrap_95':paired,
                       'gain_macro_f1':score['macro_f1']-baseline_metrics['macro_f1']})
    best=max(trials,key=lambda x:x['gain_macro_f1'])
    probability=p.copy();probability[order[:best['routed']]]=q[order[:best['routed']]]
    result=llm.copy()
    result[columns]=probability;result['pred_label']=probability.argmax(1);result['model']=run_id
    result['llm_used']=False
    result.loc[order[:best['routed']],'llm_used']=True
    # The full model's warning flag is not valid for replacement probabilities.
    result=result.drop(columns=['flag_ineffective'],errors='ignore')
    result.to_csv(out/'predictions_validation.csv.gz',index=False,compression='gzip')
    report={'base_source':str(base_source),'llm_source':str(llm_source),'same_validation_ids':True,
            'baseline_metrics':baseline_metrics,'llm_metrics':metrics(llm.label,q),'trials':trials,'selected':best,
            'limitations':'20 essays; selection and evaluation share this pilot. LLM probabilities conditional on three label tokens, without separate calibration. Not evidence of full-validation or test benefit.'}
    write_json(out/'routing_review.json',report)
    write_json(out/'metrics_validation.json',best['metrics'])
    write_json(out/'metadata.json',{'family':'llm_routing_pilot','pilot':True,'validation_essays':20,
                                  'base_source':str(base_source),'llm_source':str(llm_source),'config':config})
    print('PAIRED_LLM_ROUTING',report,flush=True)
    return report
