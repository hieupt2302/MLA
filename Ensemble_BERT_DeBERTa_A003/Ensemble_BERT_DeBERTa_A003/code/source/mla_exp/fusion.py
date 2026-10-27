from pathlib import Path
import time

import numpy as np
import pandas as pd

from .classical import predict as predict_member, run_dir, verify_lock
from .common import check_probabilities, environment, read_json, write_json
from .data import load_frame
from .evaluation import metrics, operating_point, write_predictions


def member_probabilities(config,name,split,frame):
    if split == 'test': verify_lock(config, name)
    directory = run_dir(config,name)
    path = directory / f"predictions_{split}.csv.gz"
    if not path.exists(): predict_member(config,name,split)
    predictions = pd.read_csv(path)
    if predictions.segment_id.duplicated().any() or set(predictions.segment_id) != set(frame.segment_id):
        raise ValueError("Member coverage differs from evaluation partition")
    aligned = predictions.set_index("segment_id").loc[frame.segment_id]
    if not np.array_equal(aligned.label.to_numpy(),frame.label.to_numpy()): raise ValueError("Member label mismatch")
    return check_probabilities(aligned[["p_0","p_1","p_2"]].to_numpy())


def train(config,args):
    started=time.perf_counter()
    directory=run_dir(config,args.run); directory.mkdir(parents=True,exist_ok=True)
    if (Path(config["output_root"])/"selection.lock.json").exists(): raise RuntimeError("Selection frozen")
    if not args.members or len(args.members)<2: raise ValueError("Ensemble requires at least two members")
    validation=load_frame(config["data_root"],"validation",config)
    values=[member_probabilities(config,name,"validation",validation) for name in args.members]
    candidates=([[a,1-a] for a in config["ensemble_weights"]] if len(values)==2 else [[1/len(values)]*len(values)])
    history=[]
    for weights in candidates:
        p=sum(weight*value for weight,value in zip(weights,values))
        score=metrics(validation.label,p)
        history.append({"weights":weights,"metrics":score})
    best=max(history,key=lambda x:(x["metrics"]["macro_f1"],x["metrics"]["recall_ineffective"]))
    write_json(directory/"selection.json",{"members":args.members,"weights":best["weights"],"search":history})
    write_json(directory/"metadata.json",{"family":"ensemble","seed":args.seed,"members":args.members,"pilot":False,
               "train_seconds":time.perf_counter()-started,"environment":environment()})
    predict(config,args.run,"calibration"); predict(config,args.run,"validation")
    return read_json(directory/"metrics_validation.json")


def predict(config,name,split):
    directory=run_dir(config,name); choice=read_json(directory/"selection.json")
    frame=load_frame(config["data_root"],split,config)
    values=[member_probabilities(config,member,split,frame) for member in choice["members"]]
    p=sum(weight*value for weight,value in zip(choice["weights"],values))
    if split=="calibration": write_json(directory/"operating_point.json",operating_point(frame.label,p))
    policy=read_json(directory/"operating_point.json")
    write_predictions(directory/f"predictions_{split}.csv.gz",frame,p,name,42,flag_ineffective=p[:,0]>=policy["threshold"])
    result=metrics(frame.label,p)
    result["members"]=choice["members"]; result["weights"]=choice["weights"]
    result["component_performance"]={member:read_json(run_dir(config,member)/f"metrics_{split}.json").get("performance",{}) for member in choice["members"]}
    write_json(directory/f"metrics_{split}.json",result)
    return result
