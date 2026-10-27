import argparse
import json
from pathlib import Path

from .common import read_json


def main(argv=None):
    parser = argparse.ArgumentParser(description="PERSUADE hybrid experiments; real benchmarks run on Colab")
    parser.add_argument("--config", default=str(Path(__file__).parents[1] / "config.json"))
    sub = parser.add_subparsers(dest="command", required=True)
    prep = sub.add_parser("prepare"); prep.add_argument("--download", action="store_true")
    train = sub.add_parser("train")
    train.add_argument("--method", choices=["dummy", "lr", "svm", "neural", "ensemble", "llm"], required=True)
    train.add_argument("--run", required=True)
    train.add_argument("--context", action="store_true")
    train.add_argument("--embedding-run")
    train.add_argument("--encoder", default="google-bert/bert-base-uncased")
    train.add_argument("--seed", type=int, default=42)
    train.add_argument("--lr", type=float, default=2e-5)
    train.add_argument("--balanced", action="store_true")
    train.add_argument("--pilot", action="store_true")
    train.add_argument('--max-length', type=int)
    train.add_argument('--batch-size',type=int)
    train.add_argument('--epochs',type=int,choices=[1,2,3])
    train.add_argument('--cv-jobs',type=int,choices=[1,2,4])
    train.add_argument('--amp-dtype',choices=['float16','bfloat16'])
    train.add_argument('--llm-test-budget-seconds',type=float)
    train.add_argument("--resume", action="store_true")
    train.add_argument("--members", nargs="+")
    emb = sub.add_parser("embed")
    emb.add_argument("--run", required=True); emb.add_argument("--encoder", default="google-bert/bert-base-uncased")
    emb.add_argument("--checkpoint"); emb.add_argument("--split", default="fit", choices=["fit", "validation", "calibration", "test"])
    emb.add_argument("--context", action="store_true")
    pred = sub.add_parser("predict"); pred.add_argument("--run", required=True); pred.add_argument("--split", required=True, choices=["validation", "calibration", "test"])
    ev = sub.add_parser("evaluate"); ev.add_argument("--run", required=True); ev.add_argument("--split", required=True, choices=["validation", "calibration", "test"])
    freeze = sub.add_parser("freeze"); freeze.add_argument("--runs", nargs="+", required=True)
    sub.add_parser("report"); sub.add_parser("lopo")
    perf=sub.add_parser('benchmark'); perf.add_argument('--run',required=True)
    perf.add_argument('--split',choices=['validation','test'],default='test')
    perf.add_argument('--batch-size',type=int,default=128); perf.add_argument('--repeats',type=int,default=10)
    sub.add_parser('audit-summary')
    calibration=sub.add_parser('choose-calibration'); calibration.add_argument('--run',required=True)
    remote = sub.add_parser("remote"); remote.add_argument("--resume", action="store_true"); remote.add_argument("--cpu-only", action="store_true")
    smoke = sub.add_parser("smoke"); smoke.add_argument("--encoder", default="google-bert/bert-base-uncased"); smoke.add_argument("--steps", type=int, default=100)
    args = parser.parse_args(argv)
    config = read_json(args.config)
    # Only train changes encoder window; predict/embed restore it from metadata.
    # The common split/test lock is always based on the original config.
    if args.command == 'train' and args.max_length:
        config = dict(config, max_length=args.max_length)
    if args.command=='train' and args.batch_size:
        config=dict(config,batch_size=args.batch_size)
    if args.command=='train' and args.epochs:
        config=dict(config,epochs=args.epochs)
    if args.command=='train' and args.cv_jobs:
        config=dict(config,cv_jobs=args.cv_jobs)
    if args.command=='train' and args.amp_dtype:
        config=dict(config,amp_dtype='torch.'+args.amp_dtype)
    if args.command == "prepare":
        from .data import prepare
        result = prepare(config["data_root"], config, args.download)
    elif args.command == "train":
        if args.method in ["dummy", "lr", "svm"]:
            from .classical import train
        elif args.method == "neural":
            from .neural import train
        elif args.method == "ensemble":
            from .fusion import train
        else:
            from .llm import train
        result = train(config, args)
    elif args.command == "embed":
        from .neural import embed
        result = embed(config, args)
    elif args.command == "predict":
        from .classical import predict
        result = predict(config, args.run, args.split)
    elif args.command == "evaluate":
        if args.split=='test':
            from .classical import verify_lock
            verify_lock(config,args.run)
        from .evaluation import evaluate_file
        directory = Path(config["output_root"]) / "runs" / args.run
        result = evaluate_file(directory / f"predictions_{args.split}.csv.gz", directory / f"metrics_{args.split}.json", config["bootstrap_repeats"], config["minimum_slice_size"], config["minimum_slice_class_size"],config['data_root'])
    elif args.command == "freeze":
        from .classical import freeze_selection
        result = freeze_selection(config, args.runs)
    elif args.command == "report":
        from .evaluation import report
        result = report(config["output_root"])
    elif args.command=='benchmark':
        from .performance import benchmark
        if args.batch_size<1 or args.repeats<2: parser.error('benchmark requires positive batch size and at least two measured batches')
        result=benchmark(config,args.run,args.split,args.batch_size,args.repeats)
    elif args.command=='choose-calibration':
        from .classical import choose_lr_calibration
        result=choose_lr_calibration(config,args.run)
    elif args.command=='audit-summary':
        from .data import refresh_audit
        result=refresh_audit(config['data_root'])
    elif args.command == "lopo":
        from .classical import lopo
        result = lopo(config)
    elif args.command == "remote":
        from .remote import run
        result = run(config, args.config, args.resume, args.cpu_only)
    else:
        from .neural import smoke
        result = smoke(config, args.encoder, args.steps)
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
