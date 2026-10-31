"""
Tổng hợp kết quả các notebook mở rộng ngữ cảnh (08 L1±2, 09 L2, 10 L3, 12 L1-para) và LOPO chạy lại (11).
Đọc results/*.zip (tải từ Colab), ghi bảng tổng hợp vào outputs/ và in ra màn hình.
Chạy từ thư mục gốc repo:  python week11_context_levels/summarize_context_levels.py
"""
import glob
import json
import os
import sys
import zipfile

import numpy as np
import pandas as pd
from sklearn.metrics import f1_score

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "outputs")
P3 = os.path.join(ROOT, "Week11_Person3_DeBERTa_OfficialTest/outputs/week11_person3")
ZIPS = (glob.glob(os.path.join(ROOT, "week11_context_levels/results/results_*.zip"))
        + glob.glob(os.path.join(ROOT, "week11_lopo_rerun/results/results_*.zip")))
ORDER = ["L1w2", "L1para", "L2", "L3"]
NAMES = {"L1w2": "L1 ±2 (2 đơn vị trước + 2 sau)", "L1para": "L1-para (cả đoạn chứa đơn vị)",
         "L2": "Level 2 (L1 + đoạn bài đọc nguồn)", "L3": "Level 3 (cả bài, đánh dấu đơn vị)"}


def unzip_all():
    dirs = {}
    for z in ZIPS:
        if "_QUICK" in z:
            continue
        key = os.path.basename(z)[len("results_"):-len(".zip")]
        dest = os.path.join(os.path.dirname(z), key)
        with zipfile.ZipFile(z) as zf:
            zf.extractall(dest)
        sub = [d for d in glob.glob(os.path.join(dest, "*")) if os.path.isdir(d)]
        dirs[key] = sub[0] if sub else dest
    return dirs


def main():
    dirs = unzip_all()
    print("Kết quả có:", sorted(dirs))
    rows, extra = [], {}
    ref = {m: pd.read_csv(os.path.join(P3, f"val_predictions_{m}.csv")) for m in ["L0", "L1", "PA"]}
    y = ref["L1"]["true_label"].values
    for m in ["L0", "L1", "PA"]:
        p = ref[m]["pred_label"].values
        rows.append({"model": m, "name": {"L0": "L0 (chỉ đơn vị)", "L1": "L1 (± 1 đơn vị) — hệ thống khóa",
                                          "PA": "Prompt-Aware (L1 + tên đề)"}[m],
                     "macro_f1": round(f1_score(y, p, average="macro"), 4), "accuracy": round((p == y).mean(), 4),
                     "f1_ineffective": round(f1_score(y == 0, p == 0), 4), "source": "notebook 07 (A100, tuần 11)"})
    for key in ORDER:
        if key not in dirs:
            continue
        d = dirs[key]
        s = json.load(open(os.path.join(d, f"summary_{key}.json"), encoding="utf-8"))
        cmp = pd.read_csv(os.path.join(d, f"compare_{key}_vs_L0_L1.csv"))
        hist = json.load(open(os.path.join(d, f"train_history_{key}.json"), encoding="utf-8"))
        allrow = cmp[cmp["subset"] == "all"].set_index("baseline")
        r = {"model": key, "name": NAMES[key], "macro_f1": s["macro_f1"], "accuracy": s["accuracy"],
             "f1_ineffective": s["f1_ineffective"], "source": f"notebook {key} (L4, tuần 11)",
             "train_minutes": hist.get("train_minutes")}
        for b, tag in [("L1 (tuần 11)", "L1"), ("L0 (tuần 11)", "L0")]:
            if b in allrow.index:
                r[f"delta_vs_{tag}"] = allrow.loc[b, "delta"]
                r[f"ci_vs_{tag}"] = f"[{allrow.loc[b, 'ci_low']:+.4f}, {allrow.loc[b, 'ci_high']:+.4f}]"
        ev = hist.get("epoch_evals") or hist.get("history") or []
        r["val_macro_f1_by_epoch"] = [round(e.get("eval_macro_f1", e.get("macro_f1", np.nan)), 4) for e in ev]
        rows.append(r)
        extra[key] = cmp
        for f in glob.glob(os.path.join(d, "*by_type*.csv")) + glob.glob(os.path.join(d, "source_effect*.json")):
            extra[f"{key}:{os.path.basename(f)}"] = f
    tab = pd.DataFrame(rows)
    tab.to_csv(os.path.join(OUT, "context_levels_validation_summary.csv"), index=False)
    print(tab.to_string(index=False))
    for k, v in extra.items():
        print("\n==", k)
        if isinstance(v, pd.DataFrame):
            print(v.to_string(index=False))
        elif v.endswith(".csv"):
            print(pd.read_csv(v).to_string(index=False))
        else:
            print(open(v, encoding="utf-8").read())
    # gom bảng so sánh chi tiết (mọi tập con) vào một file
    if extra:
        pd.concat([v for v in extra.values() if isinstance(v, pd.DataFrame)]).to_csv(
            os.path.join(OUT, "context_levels_bootstrap_vs_L0_L1.csv"), index=False)
    # LOPO chạy lại
    if "LOPO_L0" in dirs:
        res = pd.read_csv(os.path.join(dirs["LOPO_L0"], "lopo_deberta_rerun_results.csv"))
        res.to_csv(os.path.join(OUT, "lopo_deberta_rerun_results.csv"), index=False)
        os.makedirs(os.path.join(ROOT, "week11_lopo_rerun/outputs"), exist_ok=True)
        for f in glob.glob(os.path.join(dirs["LOPO_L0"], "predictions_fold*.csv")):
            pd.read_csv(f).to_csv(os.path.join(ROOT, "week11_lopo_rerun/outputs", os.path.basename(f)), index=False)
        print("\n== LOPO chạy lại\n", res.to_string(index=False))


if __name__ == "__main__":
    main()
