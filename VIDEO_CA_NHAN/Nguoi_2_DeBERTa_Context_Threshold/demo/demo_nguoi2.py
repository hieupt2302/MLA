from pathlib import Path
import argparse
import sys
sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "build"))
import make_visuals as data

import numpy as np
from sklearn.metrics import f1_score

def main():
    parser = argparse.ArgumentParser(description="Saved L0/L1 inputs and validation flag threshold.")
    parser.add_argument("--no-raw", action="store_true")
    parser.add_argument("--theta", type=float, default=.10)
    args = parser.parse_args()
    if not 0 <= args.theta <= 1:
        parser.error("theta must lie between 0 and 1")
    raw = data.raw_optional("train", args.no_raw)
    e, l0, l1 = data.inputs_case8(raw)
    print(f"① CASE 8  validation row_idx {int(e['row_idx']):,} | {e['discourse_type']}")
    print(f"   {e['prompt_name']} | gold {data.LABELS[int(e['label'])]}")
    if raw is None:
        print("   Note: target excerpt from saved table D7 (neighbour text needs raw CSV).")
    for model, text in [("L0",l0),("L1",l1)]:
        data.print_wrapped(f"   {model} input: {text}")
        r = data.probability_row("val",model,e['row_idx'])
        print(f"   {model} (locked) P(Ineff/Adeq/Eff) = {data.probability_text(r)}"
              f" -> {data.LABELS[int(r.pred_label)]}")
    df = data.predictions("val","L1")
    p = df[[f"pred_proba_{i}" for i in range(3)]].to_numpy()
    y = df.true_label.to_numpy()
    base = p.argmax(axis=1)
    selected = np.where(p[:,0] >= args.theta, 0, p[:,1:].argmax(axis=1)+1)
    assert np.array_equal(base, df.pred_label.to_numpy())
    assert np.array_equal(selected == 0, p[:,0] >= args.theta)
    print("\n② FLAG IF P(Ineffective) >= θ   (locked L1, validation)")
    print(f"   {len(df):,} units, {int((y == 0).sum()):,} gold Ineffective")
    print("   rule          flagged   recall   precision   Macro-F1")
    stats = []
    for name,pred in [("argmax",base),(f"θ={args.theta:.2f}",selected)]:
        flagged = int((pred == 0).sum()); tp = int(((pred == 0)&(y == 0)).sum())
        recall = tp / (y == 0).sum(); precision = tp/flagged if flagged else 0
        print(f"   {name:<12} {flagged:>7,}   {recall:>6.1%}      {precision:>6.1%}      "
              f"{f1_score(y,pred,labels=[0,1,2],average='macro',zero_division=0):.3f}")
        stats.append((tp,flagged-tp))
    extra = stats[1][0]-stats[0][0]; false = stats[1][1]-stats[0][1]
    print(f"   extra correct flags: {extra:,} | extra false alarms: {false:,}")
    print(f"   false alarms per extra catch: {false/extra:.1f}" if extra > 0
          else "   false alarms per extra catch: n/a (no net extra catches)")
    r = data.probability_row("val","L1",e['row_idx'])
    flagged = r.pred_proba_0 >= args.theta
    print(f"\n③ case 8: P(Ineffective) = {r.pred_proba_0:.3f} "
          f"{'≥' if flagged else '<'} θ = {args.theta:.2f} -> {'flagged' if flagged else 'not flagged'}")

if __name__ == "__main__":
    main()
