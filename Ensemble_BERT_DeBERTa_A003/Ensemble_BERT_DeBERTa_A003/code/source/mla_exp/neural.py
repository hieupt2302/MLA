import math
import os
import random
import shutil
import time
from pathlib import Path

import numpy as np
from scipy.optimize import minimize_scalar

from .classical import input_signature, run_dir
from .backup import checkpoint_due
from .common import digest, environment, read_json, sha256, softmax, write_json
from .data import load_frame, small_fit
from .encoding import encode
from .evaluation import metrics, operating_point, write_predictions


def gpu():
    import importlib.util
    import torch
    try:
        colab = importlib.util.find_spec("google.colab") is not None
    except ModuleNotFoundError:
        colab = False
    if not colab or not Path('/content').exists() or not torch.cuda.is_available():
        raise RuntimeError("Neural/LLM compute requires a Colab CUDA runtime; local GPU fallback is disabled")
    return torch.device("cuda")


def hardware(config=None):
    import torch
    return {"gpu": torch.cuda.get_device_name(0), "vram_bytes": torch.cuda.get_device_properties(0).total_memory,
            "peak_vram_bytes": torch.cuda.max_memory_allocated(), "torch_cuda": torch.version.cuda,'amp_dtype':str(amp_dtype(config))}


def seed_all(seed):
    import torch
    random.seed(seed); np.random.seed(seed); torch.manual_seed(seed); torch.cuda.manual_seed_all(seed)


def batches(frame, tokenizer, config, context, indexes=None):
    import torch
    from torch.utils.data import DataLoader, Dataset
    class Rows(Dataset):
        def __len__(self): return len(frame) if indexes is None else len(indexes)
        def __getitem__(self, i):
            row = frame.iloc[i if indexes is None else indexes[i]]
            inputs, target, flags = encode(tokenizer, row, context, config["max_length"])
            return inputs, target, flags, int(row.label)
    def collate(rows):
        inputs, masks, flags, labels = zip(*rows)
        padded = tokenizer.pad(list(inputs), padding=True, return_tensors="pt")
        size = padded["input_ids"].shape[1]
        target = torch.tensor([mask + [False] * (size - len(mask)) for mask in masks], dtype=torch.bool)
        return padded, target, flags, torch.tensor(labels, dtype=torch.long)
    return DataLoader(Rows(), batch_size=config["batch_size"], shuffle=False, num_workers=0, collate_fn=collate)


def amp_dtype(config=None):
    import torch
    if config and config.get('amp_dtype'):
        return {'torch.float16':torch.float16,'torch.bfloat16':torch.bfloat16}[config['amp_dtype']]
    return torch.bfloat16 if torch.cuda.is_bf16_supported(including_emulation=False) else torch.float16


def infer(model, tokenizer, frame, config, context):
    import torch
    device = gpu()
    model.eval()
    torch.cuda.reset_peak_memory_stats()
    scores, flags, times = [], [], []
    torch.cuda.synchronize(); started = time.perf_counter()
    with torch.inference_mode():
        for inputs, target_mask, batch_flags, _ in batches(frame, tokenizer, config, context):
            tick = time.perf_counter()
            with torch.autocast("cuda", dtype=amp_dtype(config)):
                result = model(target_mask=target_mask.to(device), **{k: v.to(device) for k, v in inputs.items()}).logits
            if not torch.isfinite(result).all():
                raise RuntimeError("Non-finite neural predictions")
            scores.append(result.float().cpu().numpy()); flags.extend(batch_flags)
            torch.cuda.synchronize(); times.append(time.perf_counter() - tick)
    elapsed = time.perf_counter() - started
    return np.concatenate(scores), flags, {"seconds": elapsed, "examples_second": len(frame) / elapsed,
                                           "batch_latency_p50": float(np.quantile(times, 0.5)), "batch_latency_p95": float(np.quantile(times, 0.95)), "hardware": hardware(config)}


def temperature(scores, labels):
    from sklearn.metrics import log_loss
    result = minimize_scalar(lambda log_t: log_loss(labels, softmax(scores / math.exp(log_t)), labels=[0, 1, 2]), bounds=(-3, 3), method="bounded")
    return float(math.exp(result.x))


def checkpoint(directory, model, tokenizer, optimizer, scheduler, scaler, epoch, cursor, step, seed, best_score, history, train_peak_vram_bytes=0, train_seconds=0):
    import torch
    import uuid
    generation = f"step_{step:08d}_epoch_{epoch:02d}_cursor_{cursor:08d}_"+uuid.uuid4().hex[:10]
    destination = directory / "checkpoints" / generation
    temporary = directory / "checkpoints" / ("." + generation)
    temporary.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(temporary / "model", safe_serialization=True); tokenizer.save_pretrained(temporary / "model")
    torch.save({"optimizer": optimizer.state_dict(), "scheduler": scheduler.state_dict(), "scaler": scaler.state_dict(), "epoch": epoch, "cursor": cursor,
                "step": step, "seed": seed, "best_score": best_score, "history": history, "python_rng": random.getstate(), "numpy_rng": np.random.get_state(),
                "torch_rng": torch.get_rng_state(), "cuda_rng": torch.cuda.get_rng_state_all(),'train_peak_vram_bytes':train_peak_vram_bytes,
                'train_seconds':float(train_seconds)}, temporary / "training.pt")
    if destination.exists():
        shutil.rmtree(temporary)
    else:
        temporary.rename(destination)
    write_json(directory / "resume.json", {"checkpoint": str(destination), "step": step, "epoch": epoch, "cursor": cursor, 'train_seconds':float(train_seconds)})
    write_json(directory / "progress.json", {"step": step, "epoch": epoch, "cursor": cursor, "best_validation_macro_f1": best_score, "updated_epoch": time.time(), "checkpoint": str(destination)})
    # Mirror to Drive when mounted. The remote collector also retrieves each
    # immutable checkpoint generation; no credentials are copied to the VM.
    drive = Path(directory.parents[1] / "drive_checkpoint_root.txt")
    if drive.exists():
        mirror = Path(drive.read_text().strip()) / directory.name / destination.name
        if mirror.parent.exists():
            shutil.copytree(destination, mirror, dirs_exist_ok=True)
    return destination


def train(config, args):
    import torch
    from transformers import AutoTokenizer, get_linear_schedule_with_warmup
    from span_model import SpanClassifier as AutoModelForSequenceClassification
    device = gpu(); seed_all(args.seed)
    root = Path(config["output_root"])
    if (root / "selection.lock.json").exists(): raise RuntimeError("Selection frozen")
    directory = run_dir(config, args.run); directory.mkdir(parents=True, exist_ok=True)
    if args.resume and (directory/'resume.json').exists():
        saved_amp=read_json(directory/'metadata.json')['identity']['amp_dtype']
        if config.get('amp_dtype') not in [None,saved_amp]: raise ValueError('Resume precision differs from checkpoint')
        config=dict(config,amp_dtype=saved_amp)
    config=dict(config,amp_dtype=str(amp_dtype(config)))
    fit = load_frame(config["data_root"], "fit", config)
    if args.pilot: fit = small_fit(fit, 42)
    validation = load_frame(config["data_root"], "validation", config)
    # Pilot ranking uses the same deterministic validation essays, not a
    # row sample that favors essays with many segments.
    if args.pilot:
        groups = sorted(validation.group_id.unique(), key=lambda x: digest([42, x]))[:200]
        validation = validation.loc[validation.group_id.isin(groups)].reset_index(drop=True)
    identity = {"encoder": args.encoder, "context": args.context, "seed": args.seed, "lr": args.lr, "balanced": args.balanced, "pilot": args.pilot,
                "max_length": config["max_length"], 'batch_size':config['batch_size'],'effective_batch_size':config['effective_batch_size'],'epochs':1 if args.pilot else config['epochs'],
                "split_digest": read_json(Path(config["data_root"]) / "audit.json")["split_digest"]}
    identity['prepared_sha256']=read_json(Path(config['data_root'])/'audit.json').get('prepared_sha256',{})
    identity['pooling']=config['pooling']; identity['revision']=config['revision']
    identity['amp_dtype']=str(amp_dtype(config))
    identity['encoding_sha256']=sha256(Path(__file__).with_name('encoding.py'))
    start_epoch, cursor, step, best_score, history = 0, 0, 0, -1.0, []
    source, resume_state = args.encoder, None
    if args.resume and (directory / "resume.json").exists():
        old = read_json(directory / "metadata.json")
        if old["identity"] != identity: raise ValueError("Resume configuration/data differs")
        source = str(Path(read_json(directory / "resume.json")["checkpoint"]) / "model")
        resume_state = torch.load(Path(source).parent / "training.pt", map_location="cpu", weights_only=False)
    tokenizer = AutoTokenizer.from_pretrained(source, **({'revision':config['revision']} if source==args.encoder else {}))
    model = AutoModelForSequenceClassification.from_pretrained(source, num_labels=3, id2label={0:"Ineffective",1:"Adequate",2:"Effective"}, label2id={"Ineffective":0,"Adequate":1,"Effective":2}).to(device)
    model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={'use_reentrant':False})
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=0.01)
    accumulation = max(1, config["effective_batch_size"] // config["batch_size"])
    epochs = 1 if args.pilot else config["epochs"]
    total_micro = math.ceil(len(fit) / config["batch_size"])
    total_steps = math.ceil(total_micro / accumulation) * epochs
    scheduler = get_linear_schedule_with_warmup(optimizer, int(total_steps * 0.1), total_steps)
    scaler = torch.amp.GradScaler("cuda", enabled=amp_dtype(config) == torch.float16)
    if resume_state:
        optimizer.load_state_dict(resume_state["optimizer"]); scheduler.load_state_dict(resume_state["scheduler"]); scaler.load_state_dict(resume_state["scaler"])
        start_epoch, cursor, step = resume_state["epoch"], resume_state["cursor"], resume_state["step"]
        best_score, history = resume_state["best_score"], resume_state["history"]
        random.setstate(resume_state["python_rng"]); np.random.set_state(resume_state["numpy_rng"])
        torch.set_rng_state(resume_state["torch_rng"]); torch.cuda.set_rng_state_all(resume_state["cuda_rng"])
    weights = None
    if args.balanced:
        counts = np.bincount(fit.label, minlength=3)
        weights = torch.tensor(len(fit) / (3 * counts), dtype=torch.float32, device=device)
    criterion = torch.nn.CrossEntropyLoss(weight=weights)
    comparison_group = digest({k:v for k,v in identity.items() if k != "seed"})[:16]
    metadata = {"family":"neural", "seed":args.seed, "encoder":args.encoder, "context":args.context, "pilot":args.pilot, "identity":identity,
                "comparison_group":comparison_group, "environment":environment(), "encoder_revision":getattr(model.config,"_commit_hash",None)}
    write_json(directory / "metadata.json", metadata)
    started, saved_at = time.perf_counter(), time.monotonic()
    saved_step = step
    prior_seconds=float(resume_state.get('train_seconds',0)) if resume_state else 0
    train_peak=int(resume_state.get('train_peak_vram_bytes',0)) if resume_state else 0
    scores,performance=None,None
    for epoch in range(start_epoch, epochs):
        model.train(); optimizer.zero_grad(set_to_none=True)
        torch.cuda.reset_peak_memory_stats()
        permutation = np.random.default_rng(args.seed + epoch).permutation(len(fit))
        consumed = cursor if epoch == start_epoch else 0
        indexes = permutation[consumed:]
        loader = batches(fit, tokenizer, config, args.context, indexes)
        micros_left = len(loader)
        for batch_index, (inputs, target_mask, _, labels) in enumerate(loader):
            group_start = (batch_index // accumulation) * accumulation
            divisor = min(accumulation, micros_left - group_start)
            with torch.autocast("cuda", dtype=amp_dtype(config)):
                logits = model(target_mask=target_mask.to(device), **{k:v.to(device) for k,v in inputs.items()}).logits
                loss = criterion(logits.float(), labels.to(device)) / divisor
            if not torch.isfinite(loss): raise RuntimeError("Non-finite loss; training aborted")
            scaler.scale(loss).backward()
            consumed += len(labels)
            if (batch_index + 1) % accumulation == 0 or batch_index + 1 == micros_left:
                scaler.unscale_(optimizer); torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
                scale = scaler.get_scale(); scaler.step(optimizer); scaler.update()
                if scaler.get_scale() >= scale: scheduler.step()
                optimizer.zero_grad(set_to_none=True); step += 1
                train_peak=max(train_peak,torch.cuda.max_memory_allocated())
                if step % 50 == 0:
                    print(f"{args.run}: epoch={epoch+1} step={step}/{total_steps} loss={float(loss.detach()) * divisor:.4f}", flush=True)
                    write_json(directory / "progress.json", {"step":step,"total_steps":total_steps,"epoch":epoch,"cursor":consumed,"seconds":time.perf_counter()-started})
                if checkpoint_due(step, saved_step, time.monotonic() - saved_at, config["checkpoint_steps"], config["checkpoint_minutes"] * 60):
                    checkpoint(directory, model, tokenizer, optimizer, scheduler, scaler, epoch, consumed, step, args.seed, best_score, history,train_peak,prior_seconds+time.perf_counter()-started)
                    saved_step, saved_at = step, time.monotonic()
        scores, _, performance = infer(model, tokenizer, validation, config, args.context)
        score = metrics(validation.label, softmax(scores))["macro_f1"]
        history.append({"epoch":epoch+1,"validation_macro_f1":score,"performance":performance})
        if score > best_score:
            best_score = score
            model.save_pretrained(directory / "best", safe_serialization=True); tokenizer.save_pretrained(directory / "best")
        checkpoint(directory, model, tokenizer, optimizer, scheduler, scaler, epoch+1, 0, step, args.seed, best_score, history,train_peak,prior_seconds+time.perf_counter()-started)
        saved_step, saved_at = step, time.monotonic()
        cursor = 0
        if len(history) > 1 and history[-1]['validation_macro_f1'] <= max(x['validation_macro_f1'] for x in history[:-1]):
            print('EARLY_STOP', history, flush=True)
            break
    metadata.update({"train_seconds":prior_seconds+time.perf_counter()-started,"train_segments":len(fit),'optimizer_steps':step,'train_peak_vram_bytes':train_peak,"history":history,"hardware":hardware(config)})
    write_json(directory / "metadata.json", metadata)
    if args.pilot and scores is None: scores,_,performance=infer(model,tokenizer,validation,config,args.context)
    del model, optimizer, scheduler, scaler
    torch.cuda.empty_cache()
    if args.pilot:
        write_predictions(directory/'predictions_validation.csv.gz',validation,softmax(scores),args.run,args.seed)
        np.save(directory/'logits_validation.npy',scores)
        result = metrics(validation.label,softmax(scores))
        result['performance'] = performance
        result['pilot_essays'] = int(validation.group_id.nunique())
        write_json(directory/'metrics_validation.json',result)
        return result
    calibration = load_frame(config["data_root"], "calibration", config)
    model = AutoModelForSequenceClassification.from_pretrained(directory / "best").to(device)
    scores, _, _ = infer(model, tokenizer, calibration, config, args.context)
    write_json(directory / "temperature.json", {"temperature":temperature(scores, calibration.label)})
    del model; torch.cuda.empty_cache()
    predict(config,args.run,"calibration"); predict(config,args.run,"validation")
    return read_json(directory / "metrics_validation.json")


def predict(config, name, split):
    import torch
    from transformers import AutoTokenizer
    from span_model import SpanClassifier as AutoModelForSequenceClassification
    directory = run_dir(config,name); metadata = read_json(directory / "metadata.json")
    frame = load_frame(config["data_root"],split,config)
    config = dict(config, max_length=metadata['identity']['max_length'],batch_size=metadata['identity']['batch_size'],amp_dtype=metadata['identity']['amp_dtype'])
    tokenizer = AutoTokenizer.from_pretrained(directory / "best")
    model = AutoModelForSequenceClassification.from_pretrained(directory / "best").to(gpu())
    scores, flags, performance = infer(model,tokenizer,frame,config,metadata["context"])
    p = softmax(scores / read_json(directory / "temperature.json")["temperature"])
    if split == "calibration": write_json(directory / "operating_point.json",operating_point(frame.label,p))
    policy = read_json(directory / "operating_point.json")
    write_predictions(directory / f"predictions_{split}.csv.gz",frame,p,name,metadata["seed"],flag_ineffective=p[:,0]>=policy["threshold"],
                      target_truncated=[f["target_truncated"] for f in flags],context_truncated=[f["context_truncated"] for f in flags])
    result = metrics(frame.label,p); result["performance"] = performance
    result["truncation"] = {key:float(np.mean([f[key] for f in flags])) for key in ["target_truncated","context_truncated"]}
    write_json(directory / f"metrics_{split}.json",result)
    np.save(directory / f"logits_{split}.npy",scores)
    del model; torch.cuda.empty_cache()
    return result


def embed(config,args):
    import torch
    from transformers import AutoModel, AutoTokenizer
    device = gpu(); frame = load_frame(config["data_root"],args.split,config)
    folder = Path(config["output_root"]) / "embeddings" / args.run
    if args.checkpoint:
        source_metadata = read_json(Path(args.checkpoint).parent/'metadata.json')
        config = dict(config, max_length=source_metadata['identity']['max_length'],batch_size=source_metadata['identity']['batch_size'],amp_dtype=source_metadata['identity']['amp_dtype'])
    elif (folder/'fit.json').exists():
        config=dict(config,amp_dtype=read_json(folder/'fit.json')['hardware']['amp_dtype'])
    source = args.checkpoint or args.encoder
    tokenizer = AutoTokenizer.from_pretrained(source); model = AutoModel.from_pretrained(source).to(device).eval()
    weight_hashes = {p.name:sha256(p) for p in Path(source).glob("*.safetensors")} if args.checkpoint else None
    signature = digest({"encoder":args.encoder,"revision":getattr(model.config,"_commit_hash",None),"weights":weight_hashes,"pooling":"cls" if args.checkpoint else "target_mean",
                        "context":args.context,"max_length":config["max_length"],"vocab":digest(tokenizer.get_vocab()),'amp_dtype':str(amp_dtype(config)),
                        'tokenizer_config':digest(tokenizer.init_kwargs),'encoding_sha256':sha256(Path(__file__).with_name('encoding.py'))})
    folder = Path(config["output_root"]) / "embeddings" / args.run; folder.mkdir(parents=True,exist_ok=True)
    target, metadata_path = folder / f"{args.split}.npy", folder / f"{args.split}.json"
    hashes = [input_signature(row,args.context) for _,row in frame.iterrows()]
    if target.exists() and metadata_path.exists():
        previous = read_json(metadata_path)
        if previous["model_signature"] == signature and previous["input_hashes"] == hashes and previous["array_sha256"] == sha256(target):
            del model; torch.cuda.empty_cache(); return {"cache_hit":True,"n":len(frame)}
    temporary = target.with_suffix(".partial.npy")
    matrix = np.lib.format.open_memmap(temporary,mode="w+",dtype=np.float32,shape=(len(frame),model.config.hidden_size))
    flags, cursor = [],0; started=time.perf_counter()
    with torch.inference_mode():
        for inputs, mask, batch_flags, _ in batches(frame,tokenizer,config,args.context):
            with torch.autocast("cuda",dtype=amp_dtype(config)):
                hidden = model(**{k:v.to(device) for k,v in inputs.items()}).last_hidden_state.float()
            if args.checkpoint:
                vectors = hidden[:,0]
            else:
                mask = mask.to(device).unsqueeze(-1)
                vectors = (hidden * mask).sum(axis=1) / mask.sum(axis=1).clamp(min=1)
            if not torch.isfinite(vectors).all(): raise RuntimeError("Non-finite embeddings")
            values = vectors.cpu().numpy(); matrix[cursor:cursor+len(values)] = values; cursor += len(values); flags.extend(batch_flags)
            if cursor % 1000 < config["batch_size"]: print(f"{args.run} embeddings {args.split}: {cursor}/{len(frame)}",flush=True)
    matrix.flush(); del matrix; temporary.replace(target)
    record = {"model_signature":signature,"context":args.context,"task_aware":bool(args.checkpoint),"pooling":"cls" if args.checkpoint else "target_mean",
              'encoder':args.encoder,
              "source_run":Path(args.checkpoint).parent.name if args.checkpoint else None,
              "segment_ids":frame.segment_id.tolist(),"input_hashes":hashes,"array_sha256":sha256(target),"seconds":time.perf_counter()-started,"hardware":hardware(config),
              "row_truncation":{key:[bool(f[key]) for f in flags] for key in ["target_truncated","context_truncated"]},
              "truncation":{key:float(np.mean([f[key] for f in flags])) for key in ["target_truncated","context_truncated"]}}
    write_json(metadata_path,record)
    del model; torch.cuda.empty_cache()
    return {"n":len(frame),"seconds":record["seconds"],"signature":signature}


def smoke(config, encoder, steps=100):
    import torch
    from transformers import AutoTokenizer
    from span_model import SpanClassifier as AutoModelForSequenceClassification
    device=gpu(); seed_all(42)
    tokenizer=AutoTokenizer.from_pretrained(encoder,revision=config['revision']); model=AutoModelForSequenceClassification.from_pretrained(encoder,num_labels=3).to(device)
    optimizer=torch.optim.AdamW(model.parameters(),lr=2e-5)
    model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={'use_reentrant':False})
    scaler=torch.amp.GradScaler('cuda',enabled=amp_dtype()==torch.float16)
    rows=load_frame(config["data_root"],"fit",config).head(config["batch_size"] * 4)
    loader=list(batches(rows,tokenizer,config,True))
    prior_head={key:value.detach().cpu().clone() for key,value in model.classifier.state_dict().items()}
    started=time.perf_counter(); model.train()
    for index in range(steps):
        inputs,target_mask,_,labels=loader[index%len(loader)]
        optimizer.zero_grad(set_to_none=True)
        with torch.autocast("cuda",dtype=amp_dtype()): loss=model(target_mask=target_mask.to(device), **{k:v.to(device) for k,v in inputs.items()},labels=labels.to(device)).loss
        if not torch.isfinite(loss): raise RuntimeError("GPU smoke has non-finite loss")
        scaler.scale(loss).backward(); scaler.unscale_(optimizer)
        torch.nn.utils.clip_grad_norm_(model.parameters(),1); scaler.step(optimizer); scaler.update()
    assert any(not torch.equal(value.detach().cpu(),prior_head[key]) for key,value in model.classifier.state_dict().items()), 'Head did not update'
    torch.cuda.synchronize(); seconds=time.perf_counter()-started
    result={"encoder":encoder,"steps":steps,"seconds":seconds,"seconds_microbatch":seconds/steps,"hardware":hardware(),"environment":environment()}
    # Verify continuation of an actual CUDA optimizer update, rather than just
    # checking that a checkpoint file can be opened.
    probe=Path(config['output_root'])/'runs'/'smoke_resume_contract'
    probe.mkdir(parents=True,exist_ok=True)
    write_json(probe/'metadata.json',{'family':'neural','pilot':True,'seed':42,'purpose':'GPU resume contract'})
    scheduler=torch.optim.lr_scheduler.LambdaLR(optimizer,lambda _:1.0)
    checkpoint_path=checkpoint(probe,model,tokenizer,optimizer,scheduler,scaler,0,len(rows),steps,42,-1.0,[])
    saved=torch.load(checkpoint_path/'training.pt',map_location='cpu',weights_only=False)
    if saved['step']!=steps or saved['cursor']!=len(rows) or saved['seed']!=42: raise RuntimeError('Resume cursor/step/seed mismatch')
    resumed=AutoModelForSequenceClassification.from_pretrained(checkpoint_path/'model').to(device)
    resumed.gradient_checkpointing_enable(gradient_checkpointing_kwargs={'use_reentrant':False}); resumed.train()
    resumed_optimizer=torch.optim.AdamW(resumed.parameters(),lr=2e-5)
    resumed_optimizer.load_state_dict(saved['optimizer'])
    resumed_scaler=torch.amp.GradScaler('cuda',enabled=amp_dtype()==torch.float16); resumed_scaler.load_state_dict(saved['scaler'])
    inputs,target_mask,_,labels=loader[0]
    compared=[]
    for candidate,opt,scale in [(model,optimizer,scaler),(resumed,resumed_optimizer,resumed_scaler)]:
        torch.set_rng_state(saved['torch_rng']); torch.cuda.set_rng_state_all(saved['cuda_rng'])
        opt.zero_grad(set_to_none=True)
        with torch.autocast('cuda',dtype=amp_dtype()): loss=candidate(target_mask=target_mask.to(device), **{k:v.to(device) for k,v in inputs.items()},labels=labels.to(device)).loss
        scale.scale(loss).backward(); scale.unscale_(opt); torch.nn.utils.clip_grad_norm_(candidate.parameters(),1)
        scale.step(opt); scale.update()
        compared.append({key:value.detach().float().cpu().clone() for key,value in candidate.named_parameters() if 'classifier' in key})
    if not compared[0] or any(not torch.allclose(compared[0][key],compared[1][key],atol=1e-5,rtol=1e-4) for key in compared[0]):
        raise RuntimeError('Resumed next optimizer update differs from uninterrupted update')
    result['checkpoint_resume_verified']={'step':steps,'cursor':len(rows),'seed':42,'next_classifier_update_close':True}
    del resumed,resumed_optimizer,resumed_scaler,saved,compared
    import subprocess,sys
    frozen=subprocess.check_output([sys.executable,'-m','pip','freeze'],text=True)
    (Path(config['output_root'])/'runtime_requirements_gpu.txt').write_text(frozen,encoding='utf-8')
    write_json(Path(config["output_root"])/"gpu_smoke.json",result)
    del model,optimizer; torch.cuda.empty_cache(); return result
