"""
Phân tích thang ngữ cảnh (validation, 29.102 đơn vị) từ dự đoán đã lưu — không cần GPU.
  1. Bảng tổng hợp: Macro-F1, accuracy, F1/recall Ineffective, tỷ lệ đoán Ineffective, Δ so với L1 [CI bootstrap theo bài].
  2. 10 ca Ineffective "tự tin mà sai": P(Ineffective) dưới từng mức; số ca đổi nhãn.
  3. So công bằng số ca đổi nhãn: hạ ngưỡng L1 tới khi L1 gắn cờ Ineffective đúng bằng tỷ lệ của mô hình kia.
  4. F1 theo loại đơn vị.
Đầu vào: Week11_Person3…/val_predictions_{L0,L1,PA}.csv + week11_context_levels/results/<KEY>/…/val_predictions_<KEY>.csv
Chạy từ thư mục gốc repo:  python week11_context_levels/analyze_context_levels.py
"""
import glob
import os
import sys
import zipfile

import numpy as np
import pandas as pd
from sklearn.metrics import f1_score, recall_score

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P3 = os.path.join(ROOT, "Week11_Person3_DeBERTa_OfficialTest/outputs/week11_person3")
RES = os.path.join(ROOT, "week11_context_levels/results")
OUT = os.path.join(ROOT, "outputs")
TRAIN_CSV = "C:/Users/Admin/Desktop/MLA_OLD/data/persuade_raw/persuade_corpus_2.0_train.csv"
LEVELS = [("L0", "L0 — chỉ đơn vị"), ("L1", "L1 — ±1 đơn vị (khóa)"), ("PA", "Prompt-Aware — L1 + tên đề"),
          ("L1w2", "L1 ±2 — ±2 đơn vị"), ("L1para", "L1-para — cả đoạn"), ("L2", "L2 — L1 + bài nguồn"),
          ("L3", "L3 — cả bài, 3 epoch"), ("L3_7ep", "L3 — cả bài, 7 epoch")]
N_BOOT = 2000


def load_preds():
    preds = {m: pd.read_csv(os.path.join(P3, f"val_predictions_{m}.csv")) for m in ["L0", "L1", "PA"]}
    for z in glob.glob(os.path.join(RES, "results_*.zip")):
        key = os.path.basename(z)[len("results_"):-len(".zip")]
        if "QUICK" in key or "UNORDERED" in key:
            continue
        with zipfile.ZipFile(z) as zf:
            zf.extractall(os.path.join(RES, key))
        f = glob.glob(os.path.join(RES, key, "*", f"val_predictions_{key}.csv"))
        if f:
            preds[key] = pd.read_csv(f[0])
    ref = preds["L1"]
    for k, p in preds.items():   # mọi file phải cùng thứ tự đơn vị và cùng nhãn
        assert (p["row_idx"].values == ref["row_idx"].values).all(), k
        assert (p["true_label"].values == ref["true_label"].values).all(), k
    return preds


def boot_delta(ess, y, a, b, seed=42):
    codes = pd.Series(ess).astype("category").cat.codes.values
    members = [np.flatnonzero(codes == k) for k in range(codes.max() + 1)]
    rng = np.random.default_rng(seed)
    d = []
    for _ in range(N_BOOT):
        idx = np.concatenate([members[k] for k in rng.integers(0, len(members), len(members))])
        d.append(f1_score(y[idx], b[idx], average="macro") - f1_score(y[idx], a[idx], average="macro"))
    return np.percentile(d, [2.5, 97.5])


def ten_cases(preds):
    cases = pd.read_csv(os.path.join(OUT, "threshold_case_flips.csv"))
    u = pd.read_csv(TRAIN_CSV, usecols=["discourse_text", "discourse_effectiveness"], dtype=str)
    u = u.dropna(subset=["discourse_effectiveness", "discourse_text"])
    u["discourse_text"] = u["discourse_text"].str.strip()
    txt = u[u["discourse_text"].str.len() > 0].reset_index(drop=True)["discourse_text"]
    rid = preds["L1"]["row_idx"].values
    pos = []
    for _, c in cases.iterrows():
        hit = [k for k, i in enumerate(rid) if txt[i].startswith(str(c["snippet"])[:40])]
        assert len(hit) == 1, c["case_id"]
        pos.append(hit[0])
    rows = []
    for (cid, typ), k in zip(cases[["case_id", "discourse_type"]].values, pos):
        r = {"case": cid, "type": typ}
        for m in preds:
            r[f"P_ineff_{m}"] = round(preds[m]["pred_proba_0"].values[k], 3)
            r[f"pred_{m}"] = ["Ineff", "Adeq", "Eff"][preds[m]["pred_label"].values[k]]
        rows.append(r)
    return pd.DataFrame(rows), np.array(pos)


def main():
    preds = load_preds()
    ref = preds["L1"]
    y, ess = ref["true_label"].values, ref["essay_id_comp"].values
    p1 = ref["pred_proba_0"].values
    cases, pos = ten_cases(preds)

    rows = []
    for key, name in LEVELS:
        if key not in preds:
            continue
        p = preds[key]["pred_label"].values
        share = (p == 0).mean()
        # ngưỡng L1 cho cùng tỷ lệ gắn cờ Ineffective -> số ca đổi của L1 ở mức báo động ngang nhau
        theta = np.quantile(p1, 1 - share)
        r = {"model": key, "name": name, "macro_f1": round(f1_score(y, p, average="macro"), 4),
             "accuracy": round((p == y).mean(), 4), "f1_ineffective": round(f1_score(y == 0, p == 0), 4),
             "recall_ineffective": round(recall_score(y == 0, p == 0), 4),
             "pred_ineffective_share": round(share, 4),
             "cases_flipped_of_10": int((p[pos] == 0).sum()),
             "L1_cases_flipped_at_same_flag_rate": int((p1[pos] >= theta).sum())}
        if key != "L1":
            lo, hi = boot_delta(ess, y, ref["pred_label"].values, p)
            r["delta_vs_L1"] = round(f1_score(y, p, average="macro") - f1_score(y, ref["pred_label"].values, average="macro"), 4)
            r["ci95_vs_L1"] = f"[{lo:+.4f}, {hi:+.4f}]"
        rows.append(r)
        print(r, flush=True)
    tab = pd.DataFrame(rows)
    tab.to_csv(os.path.join(OUT, "context_levels_validation_summary.csv"), index=False)
    cases.to_csv(os.path.join(OUT, "context_levels_10_cases.csv"), index=False)

    bt = []
    for t in sorted(ref["discourse_type"].unique()):
        m = ref["discourse_type"].values == t
        r = {"discourse_type": t, "n": int(m.sum())}
        for key, _ in LEVELS:
            if key in preds:
                p = preds[key]["pred_label"].values
                r[f"macroF1_{key}"] = round(f1_score(y[m], p[m], average="macro"), 4)
                r[f"F1ineff_{key}"] = round(f1_score(y[m] == 0, p[m] == 0), 4)
        bt.append(r)
    bt = pd.DataFrame(bt)
    bt.to_csv(os.path.join(OUT, "context_levels_by_discourse_type.csv"), index=False)
    print("\n", tab.to_string(index=False))
    print("\n", cases[["case", "type"] + [c for c in cases.columns if c.startswith("P_ineff")]].to_string(index=False))
    print("\n", bt.to_string(index=False))


if __name__ == "__main__":
    main()
