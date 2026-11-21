from pathlib import Path
import argparse
import sys
sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "build"))
import make_visuals as data

def main():
    parser = argparse.ArgumentParser(description="Trace RF outputs and length recall; no training.")
    parser.add_argument("--no-raw", action="store_true")
    args = parser.parse_args()
    raw = data.raw_optional("test", args.no_raw)
    e = data.example("test", 47059, raw)
    record = f" (raw record {e['raw_record']:,})" if e['raw_record'] is not None else ""
    print(f"① TRACE  test row_idx {int(e['row_idx']):,}" + record)
    data.print_wrapped(f"   prompt: {e['prompt_name']} | type: {e['discourse_type']}")
    print(f"   essay words: {int(e['essay_word_count']):,} -> {e['length_q']}")
    if e['text']:
        data.print_wrapped(f'   text: "{e["text"]}"')
    else:
        print("   Note: raw CSV unavailable/skipped; slim sample has no unit text.")
    print(f'   label: "{data.LABELS[int(e["label"])]}" -> id {int(e["label"])}')
    print("   (Ineffective=0, Adequate=1, Effective=2)")
    rf = data.probability_row("test", "rf_feature_set_b", e['row_idx'])
    l1 = data.probability_row("test", "L1", e['row_idx'])
    correct = "correct" if rf.pred_label == e['label'] else "incorrect"
    data.print_wrapped(f"   RF FS-B P(Ineff/Adeq/Eff) = {data.probability_text(rf)}"
                      f" -> predicts {data.LABELS[int(rf.pred_label)]} ({correct})")
    print(f"   DeBERTa L1 (locked) P(Ineff) = {l1.pred_proba_0:.3f}"
          f" -> predicts {data.LABELS[int(l1.pred_label)]}")
    raw = data.raw_optional("train", args.no_raw)
    if raw is None:
        r = data.table("D4_identifier_integrity.csv").query("file == 'train+val annotated'").iloc[0]
        n, distinct = int(r.units), int(r.distinct_discourse_id)
        note = " (from saved table D4)"
    else:
        n, distinct, note = len(raw), raw.discourse_id.nunique(), ""
    print(f"\n② ID CHECK  train+val annotated units {n:,} | distinct discourse_id {distinct:,}")
    print("   -> join on row_idx" + note)
    print("\n③ INEFFECTIVE RECALL BY ESSAY-LENGTH QUARTILE (official test, saved predictions)")
    print("   quartile          gold Ineff   RF recall   DeBERTa L1 recall")
    rows = data.recalls()
    for q,n,rfrec,l1rec,caught in rows:
        print(f"   {q:<19} {n:>9,}   {rfrec:>7.1%}          {l1rec:>7.1%}")
    q,n,rfrec,l1rec,caught = rows[-1]
    print(f"   RF catches {caught:,} of {n:,} gold Ineffective units in the longest essays")

if __name__ == "__main__":
    main()
