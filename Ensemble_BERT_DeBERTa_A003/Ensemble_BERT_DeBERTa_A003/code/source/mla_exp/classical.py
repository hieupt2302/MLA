import itertools
import pickle
import re
import time
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd
from joblib import Memory
from scipy import sparse
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.calibration import CalibratedClassifierCV
from sklearn.dummy import DummyClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.frozen import FrozenEstimator
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, StratifiedGroupKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler, normalize
from sklearn.svm import LinearSVC

from .common import digest, environment, read_json, sha256, softmax, write_json
from .data import load_frame
from .evaluation import metrics, operating_point, write_predictions


def run_dir(config, name):
    if not re.fullmatch(r"[A-Za-z0-9_-]+", name):
        raise ValueError("Run name must contain letters, digits, underscores or hyphens")
    return Path(config["output_root"]) / "runs" / name


def input_signature(row, context):
    fields = ["discourse_text", "discourse_type"] + (["left_context", "right_context", "assignment"] if context else [])
    return digest([str(row.get(field, "")) for field in fields])


@lru_cache(maxsize=24)
def _embedding_file(array_path, metadata_path, array_mtime, metadata_mtime):
    metadata = read_json(metadata_path)
    if sha256(array_path) != metadata["array_sha256"]:
        raise ValueError("Embedding cache was modified")
    return metadata, {key:i for i,key in enumerate(metadata["segment_ids"])}, np.load(array_path, mmap_mode="r")


def cached_embeddings(root, name, frame, expected_signature=None):
    folder = Path(root) / "embeddings" / name
    output = None
    for split, indexes in frame.groupby("split").groups.items():
        array_path, metadata_path = folder / f"{split}.npy", folder / f"{split}.json"
        metadata, positions, matrix = _embedding_file(str(array_path), str(metadata_path), array_path.stat().st_mtime_ns, metadata_path.stat().st_mtime_ns)
        if expected_signature is not None and metadata["model_signature"] != expected_signature:
            raise ValueError("Embedding tokenizer/checkpoint/pooling mismatch")
        if output is None:
            output = np.empty((len(frame), matrix.shape[1]), dtype=np.float32)
        for position in indexes:
            row = frame.loc[position]
            index = positions.get(row.segment_id)
            if index is None or metadata["input_hashes"][index] != input_signature(row, metadata["context"]):
                raise ValueError("Embedding/input cache mismatch")
            output[frame.index.get_loc(position)] = matrix[index]
    return output


class Features(BaseEstimator, TransformerMixin):
    def __init__(self, max_features=15000, min_df=2, context=False, embedding_root=None, embedding_run=None, embedding_weight=1.0):
        self.max_features, self.min_df, self.context = max_features, min_df, context
        self.embedding_root, self.embedding_run, self.embedding_weight = embedding_root, embedding_run, embedding_weight

    @staticmethod
    def length(frame):
        return np.log1p(frame.discourse_text.str.split().str.len().to_numpy()).reshape(-1, 1)

    @staticmethod
    def context_text(frame):
        return frame.assignment + " " + frame.left_context + " " + frame.right_context

    def fit(self, frame, y=None):
        # Explicit allowlist: labels, holistic scores and demographic fields
        # never enter the text/features, even when present in the dataframe.
        self.words_ = TfidfVectorizer(ngram_range=(1, 2), max_features=self.max_features, min_df=self.min_df, sublinear_tf=True, dtype=np.float32)
        self.words_.fit(frame.discourse_text)
        self.types_ = OneHotEncoder(handle_unknown="ignore", dtype=np.float32).fit(frame[["discourse_type"]])
        self.length_ = StandardScaler(with_mean=False).fit(self.length(frame))
        if self.context:
            self.context_ = TfidfVectorizer(ngram_range=(1, 2), max_features=self.max_features, min_df=self.min_df, sublinear_tf=True, dtype=np.float32).fit(self.context_text(frame))
        if self.embedding_run:
            self.embedding_signature_ = read_json(Path(self.embedding_root) / "embeddings" / self.embedding_run / "fit.json")["model_signature"]
            self.embedding_ = StandardScaler().fit(cached_embeddings(self.embedding_root, self.embedding_run, frame, self.embedding_signature_))
        return self

    def transform(self, frame):
        blocks = [self.words_.transform(frame.discourse_text), self.types_.transform(frame[["discourse_type"]]), sparse.csr_matrix(self.length_.transform(self.length(frame)), dtype=np.float32)]
        if self.context:
            blocks.append(self.context_.transform(self.context_text(frame)))
        if self.embedding_run:
            embedding = normalize(self.embedding_.transform(cached_embeddings(self.embedding_root, self.embedding_run, frame, self.embedding_signature_)))
            blocks.append(sparse.csr_matrix(embedding * self.embedding_weight, dtype=np.float32))
        return sparse.hstack(blocks, format="csr", dtype=np.float32)


def model_pipeline(config, method, context=False, embedding_run=None):
    feature = Features(config["max_features"], config["min_df"], context, config["output_root"], embedding_run)
    model = LogisticRegression(max_iter=3000, random_state=42) if method == "lr" else LinearSVC(max_iter=10000, random_state=42, dual="auto")
    memory=None
    if embedding_run:
        folder=Path(config['output_root'])/'embeddings'/embedding_run
        array,record=folder/'fit.npy',folder/'fit.json'
        metadata,_,_=_embedding_file(str(array),str(record),array.stat().st_mtime_ns,record.stat().st_mtime_ns)
        namespace=digest([metadata['model_signature'],metadata['array_sha256'],sha256(__file__)])
        memory=Memory(Path(config['output_root']).parent/'feature_cache'/namespace,mmap_mode='r',verbose=0)
    return Pipeline([("features", feature), ("model", model)],memory=memory)


def raw_probabilities(model, frame):
    if hasattr(model, "predict_proba"):
        p = model.predict_proba(frame)
    else:
        p = softmax(model.decision_function(frame))
    if list(model.classes_) != [0, 1, 2]:
        raise ValueError("Model classes must match 0,1,2")
    return p


def choose_lr_calibration(config, name):
    """Revisit probability calibration using validation, before selection lock."""
    directory=run_dir(config,name)
    if (Path(config['output_root'])/'selection.lock.json').exists(): raise RuntimeError('Selection frozen')
    metadata=read_json(directory/'metadata.json')
    if metadata['method']!='lr': return {'skipped':'LR-only calibration choice'}
    with (directory/'model.pkl').open('rb') as file: artifact=pickle.load(file)
    validation=load_frame(config['data_root'],'validation',config)
    options={'raw':metrics(validation.label,raw_probabilities(artifact['model'],validation)),
             'sigmoid':metrics(validation.label,artifact['calibrator'].predict_proba(validation))}
    selected=max(options,key=lambda key:options[key]['macro_f1'])
    artifact['probability_mode']=selected
    with (directory/'model.pkl').open('wb') as file: pickle.dump(artifact,file)
    write_json(directory/'calibration_choice.json',{'selected':selected,'selected_on':'validation_macro_f1','options':options})
    metadata['model_sha256']=sha256(directory/'model.pkl'); metadata['probability_mode']=selected
    write_json(directory/'metadata.json',metadata)
    for split in ['calibration','validation']: predict(config,name,split)
    return {'run':name,'selected':selected,'macro_f1':options[selected]['macro_f1']}


def train(config, args):
    root = Path(config["output_root"])
    if (root / "selection.lock.json").exists():
        raise RuntimeError("Selection frozen: training is closed")
    directory = run_dir(config, args.run)
    directory.mkdir(parents=True, exist_ok=True)
    fit = load_frame(config["data_root"], "fit", config)
    validation = load_frame(config["data_root"], "validation", config)
    calibration = load_frame(config["data_root"], "calibration", config)
    started = time.perf_counter()
    if args.method == "dummy":
        model = DummyClassifier(strategy="prior").fit(np.zeros((len(fit), 1)), fit.label)
        artifact = {"model": model, "calibrator": None, "dummy": True}
        params, cv_score = {}, None
    else:
        pipeline = model_pipeline(config, args.method, args.context, args.embedding_run)
        grid = {"model__C": config["c_grid"], "model__class_weight": config["class_weights"]}
        if args.embedding_run:
            grid["features__embedding_weight"] = config["embedding_weights"]
        task_aware = args.embedding_run and read_json(root / "embeddings" / args.embedding_run / "fit.json")["task_aware"]
        if task_aware:
            best_score, model, params = -1, None, None
            history = []
            for values in itertools.product(*grid.values()):
                selected = dict(zip(grid, values))
                candidate = model_pipeline(config, args.method, args.context, args.embedding_run).set_params(**selected).fit(fit, fit.label)
                score = metrics(validation.label, raw_probabilities(candidate, validation))["macro_f1"]
                history.append({"params": selected, "validation_macro_f1": score})
                if score > best_score:
                    best_score, model, params = score, candidate, selected
            write_json(directory / "search.json", {"selection": "held-out validation; encoder trained on fit; no CV claim", "candidates": history})
            cv_score = None
        else:
            cv = list(StratifiedGroupKFold(3, shuffle=True, random_state=config["seed"]).split(fit, fit.label, fit.group_id))
            for train_index, val_index in cv:
                if set(fit.iloc[train_index].label) != {0, 1, 2}:
                    raise ValueError("A CV fit fold is missing a class")
                if set(fit.iloc[train_index].group_id) & set(fit.iloc[val_index].group_id):
                    raise ValueError("CV group leakage")
            search = GridSearchCV(pipeline, grid, scoring="f1_macro", cv=cv, n_jobs=config.get('cv_jobs',1), error_score="raise", return_train_score=False,verbose=2)
            search.fit(fit, fit.label)
            model, params, cv_score = search.best_estimator_, search.best_params_, float(search.best_score_)
            pd.DataFrame(search.cv_results_).to_csv(directory / "cv_search.csv", index=False)
        calibrator = CalibratedClassifierCV(FrozenEstimator(model), method="sigmoid").fit(calibration, calibration.label)
        artifact = {"model": model, "calibrator": calibrator, "dummy": False, 'probability_mode':'sigmoid'}
        if args.method == 'lr':
            options = {'raw':metrics(validation.label, raw_probabilities(model,validation)),
                       'sigmoid':metrics(validation.label, calibrator.predict_proba(validation))}
            artifact['probability_mode'] = max(options,key=lambda key:options[key]['macro_f1'])
            write_json(directory/'calibration_choice.json',{'selected':artifact['probability_mode'],'selected_on':'validation_macro_f1','options':options})
    with open(directory / "model.pkl", "wb") as file:
        pickle.dump(artifact, file)
    family = ("hybrid_" if args.embedding_run else "context_" if args.context else "") + args.method
    metadata = {"family": family, "method": args.method, "seed": args.seed, "context": args.context, "embedding_run": args.embedding_run,
                "params": params, "cv_macro_f1": cv_score, 'cv_jobs':config.get('cv_jobs',1) if cv_score is not None else None,'feature_cache':bool(args.embedding_run),"train_seconds": time.perf_counter() - started, "environment": environment(),
                "data_split_digest": read_json(Path(config["data_root"]) / "audit.json")["split_digest"], "model_sha256": sha256(directory / "model.pkl")}
    write_json(directory / "metadata.json", metadata)
    for split in ["calibration", "validation"]:
        predict(config, args.run, split)
    return read_json(directory / "metrics_validation.json")


def freeze_selection(config, runs):
    root = Path(config["output_root"])
    lock = root / "selection.lock.json"
    if lock.exists():
        previous = read_json(lock)
        if set(previous.get('requested_runs', previous['runs'])) != set(runs):
            raise RuntimeError("Cannot alter already-frozen selection")
        return previous
    snapshots = {}
    pending = list(runs)
    while pending:
        name = pending.pop(0)
        if name in snapshots:
            continue
        directory = run_dir(config, name)
        metadata = read_json(directory / "metadata.json")
        if metadata.get("pilot"):
            raise ValueError("Pilot cannot enter final test leaderboard")
        files = [directory / "metadata.json"]
        files += list(directory.glob("*.pkl")) + [p for p in [directory / "selection.json", directory / "temperature.json", directory / "operating_point.json",directory/'calibration_choice.json'] if p.exists()]
        files += [p for p in (directory / "best").rglob("*") if p.is_file()]
        files += list((directory / "best").glob("*.safetensors"))
        files += list((directory / "best").glob("*.json")) + list((directory / "best").glob("*.txt")) + list((directory / "best").glob("*.model"))
        snapshots[name] = {str(path.relative_to(root)): sha256(path) for path in files}
        pending.extend(metadata.get('members', []))
        if metadata.get('base_run'): pending.append(metadata['base_run'])
        if metadata.get('embedding_run'):
            embedding = read_json(root / 'embeddings' / metadata['embedding_run'] / 'fit.json')
            if embedding.get('source_run'): pending.append(embedding['source_run'])
    state = {"config_digest": digest(config), "split_digest": read_json(Path(config["data_root"]) / "audit.json")["split_digest"],
             "runs": list(snapshots), "requested_runs": list(runs), "artifacts": snapshots, "environment": environment()}
    state['prepared_sha256']=read_json(Path(config['data_root'])/'audit.json').get('prepared_sha256',{})
    scores = {name:read_json(run_dir(config,name)/'metrics_validation.json')['macro_f1'] for name in runs if (run_dir(config,name)/'metrics_validation.json').exists()}
    eligible = {name:score for name,score in scores.items() if read_json(run_dir(config,name)/'metadata.json').get('seed',42)==42}
    state['validation_champion'] = max(eligible, key=eligible.get) if eligible else None
    write_json(lock, state)
    return state


def verify_lock(config, name):
    root = Path(config["output_root"])
    lock = read_json(root / "selection.lock.json")
    audit=read_json(Path(config['data_root'])/'audit.json')
    if lock['config_digest']!=digest(config) or lock['split_digest']!=audit['split_digest'] or lock.get('prepared_sha256',{})!=audit.get('prepared_sha256',{}):
        raise RuntimeError('Configuration/data changed after selection freeze')
    if lock['environment'].get('code_digest') and lock['environment']['code_digest']!=environment()['code_digest']:
        raise RuntimeError('Experiment code changed after test selection freeze')
    if name not in lock["runs"]:
        raise RuntimeError("Run was not in frozen selection")
    for path, expected in lock["artifacts"][name].items():
        if sha256(root / path) != expected:
            raise RuntimeError("Model artifact changed after test selection was frozen")


def predict(config, name, split):
    directory = run_dir(config, name)
    if split == "test":
        verify_lock(config, name)
    metadata = read_json(directory / "metadata.json")
    if metadata["family"] in ["neural", "ensemble", "llm"]:
        if metadata["family"] == "neural":
            from .neural import predict as predict_other
        elif metadata["family"] == "ensemble":
            from .fusion import predict as predict_other
        else:
            from .llm import predict as predict_other
        return predict_other(config, name, split)
    frame = load_frame(config["data_root"], split, config)
    # Only deserialize artifacts produced by this experiment, never downloaded
    # third-party pickle files.
    with open(directory / "model.pkl", "rb") as file:
        artifact = pickle.load(file)
    started = time.perf_counter()
    batch_times=[]
    if artifact["dummy"]:
        p = artifact["model"].predict_proba(np.zeros((len(frame), 1)))
    else:
        probabilities=[]
        for offset in range(0,len(frame),128):
            batch=frame.iloc[offset:offset+128]; tick=time.perf_counter()
            probabilities.append(raw_probabilities(artifact['model'],batch) if artifact.get('probability_mode')=='raw' else artifact['calibrator'].predict_proba(batch))
            batch_times.append(time.perf_counter()-tick)
        p=np.concatenate(probabilities)
    duration = time.perf_counter() - started
    if split == "calibration":
        write_json(directory / "operating_point.json", operating_point(frame.label, p))
    policy = read_json(directory / "operating_point.json")
    raw_p = None if artifact['dummy'] else raw_probabilities(artifact['model'],frame)
    extras={} if raw_p is None else {'raw_pred_label':raw_p.argmax(axis=1)}
    if metadata.get('embedding_run'):
        embedding=read_json(Path(config['output_root'])/'embeddings'/metadata['embedding_run']/f'{split}.json')
        row_flags=embedding.get('row_truncation',{})
        if row_flags:
            if embedding['segment_ids']!=frame.segment_id.tolist(): raise ValueError('Embedding truncation row order mismatch')
            for key in ['target_truncated','context_truncated']:
                if len(row_flags[key])!=len(frame): raise ValueError('Embedding truncation coverage mismatch')
                extras[key]=row_flags[key]
    write_predictions(directory / f"predictions_{split}.csv.gz", frame, p, name, metadata["seed"], flag_ineffective=p[:, 0] >= policy["threshold"],**extras)
    result = metrics(frame.label, p)
    result["inference_seconds"] = duration
    result["examples_second"] = len(frame) / duration if duration else None
    if batch_times:
        result['performance']={'seconds':duration,'examples_second':len(frame)/duration,
            'batch_size':128,'batch_latency_p50':float(np.quantile(batch_times,.5)),
            'batch_latency_p95':float(np.quantile(batch_times,.95)),'phase':'classification with cached embeddings, including vectorizer/scaler'}
    if metadata.get("embedding_run"):
        embedding = read_json(Path(config["output_root"]) / "embeddings" / metadata["embedding_run"] / f"{split}.json")
        result["feature_encoder_seconds"] = embedding["seconds"]
        result["end_to_end_seconds"] = duration + embedding["seconds"]
    if not artifact["dummy"]:
        result["raw_classifier_metrics"] = metrics(frame.label, raw_p)
        if metadata['method']=='svm':
            scores=artifact['model'].decision_function(frame)
            score_frame=pd.DataFrame(scores,columns=['score_0','score_1','score_2'])
            score_frame.insert(0,'segment_id',frame.segment_id)
            score_frame.to_csv(directory/f'decision_scores_{split}.csv.gz',index=False)
            result['raw_classifier_metrics']['probability_note']='Softmax of decision scores is uncalibrated; primary probabilities use held-out sigmoid calibration.'
    write_json(directory / f"metrics_{split}.json", result)
    return result


def lopo(config):
    frame = load_frame(config["data_root"], "development", config)
    results = []
    for prompt in sorted(frame.prompt_name.unique()):
        fit = frame.loc[frame.prompt_name.ne(prompt)]
        held = frame.loc[frame.prompt_name.eq(prompt)]
        if set(fit.label) != {0, 1, 2}:
            continue
        for method in ["lr", "svm"]:
            model = model_pipeline(config, method).set_params(model__C=1.0, model__class_weight="balanced").fit(fit, fit.label)
            results.append({"prompt": prompt, "method": method, "essays": held.group_id.nunique(), **metrics(held.label, raw_probabilities(model, held))})
        write_json(Path(config["output_root"]) / "lopo.json", results)
    return results
