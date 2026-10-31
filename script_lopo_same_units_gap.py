"""
KHOẢNG CÁCH NGOẠI ĐỀ CỦA DEBERTA TRÊN CÙNG MỘT TẬP ĐƠN VỊ (tuần 11)

Bảng 6.x cũ so DeBERTa LOPO (chấm trên TẤT CẢ đơn vị của đề, vd. 5.158) với DeBERTa in-domain
(chấm trên phần validation của đề, vd. 1.030) -> hai tập đánh giá khác nhau, không có khoảng tin cậy.

Ở đây: mô hình LOPO đã dự đoán mọi đơn vị của đề bị giấu, kể cả các đơn vị thuộc bài nằm trong
validation. Ta giữ đúng các đơn vị validation đó và so với dự đoán in-domain (cùng đầu vào Level 0)
trên chính các đơn vị ấy -> so sánh có ghép cặp, bootstrap theo bài.

Chạy: python script_lopo_same_units_gap.py --train_csv <train.csv>
"""
import argparse
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import numpy as np
import pandas as pd
from sklearn.metrics import f1_score

LABEL2ID = {"Ineffective": 0, "Adequate": 1, "Effective": 2}
PROMPTS = {'"A Cowboy Who Rode the Waves"': "A_Cowboy_Who_Rode_the_Waves",
           "Summer projects": "Summer_projects", "Distance learning": "Distance_learning"}
P3 = "Week11_Person3_DeBERTa_OfficialTest/outputs/week11_person3"
IN_DOMAIN = {"DeBERTa L0 in-domain (tuần 9)": "outputs/deberta_predictions.csv",
             "DeBERTa L0 in-domain (tuần 11)": f"{P3}/val_predictions_L0.csv"}
N_BOOT = 2000


def macro(y, p):
    return f1_score(y, p, labels=[0, 1, 2], average="macro", zero_division=0)


def paired_bootstrap(essay, y, a, b, rng):
    """Macro-F1(a) - Macro-F1(b), lấy mẫu lại theo bài."""
    ess = pd.Series(essay).astype("category").cat.codes.values
    n = ess.max() + 1
    members = [np.flatnonzero(ess == k) for k in range(n)]
    deltas = []
    for _ in range(N_BOOT):
        idx = np.concatenate([members[k] for k in rng.integers(0, n, n)])
        deltas.append(macro(y[idx], a[idx]) - macro(y[idx], b[idx]))
    return np.percentile(deltas, [2.5, 97.5])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--train_csv", default="persuade_corpus_2.0_train.csv")
    ap.add_argument("--output_dir", default="outputs")
    args = ap.parse_args()
    rng = np.random.default_rng(42)

    # Bảng đơn vị LOPO: notebook 06 lọc dropna(discourse_effectiveness) rồi giữ thứ tự file gốc
    raw = pd.read_csv(args.train_csv, usecols=["essay_id_comp", "discourse_type", "discourse_text",
                                               "discourse_effectiveness", "prompt_name"], dtype=str)
    lab = raw.dropna(subset=["discourse_effectiveness"]).copy()
    lab["label"] = lab["discourse_effectiveness"].map(LABEL2ID)

    # Bảng đơn vị validation (cùng quy tắc lọc với notebook 07, row_idx)
    units = lab.dropna(subset=["discourse_text"]).copy()
    units["discourse_text"] = units["discourse_text"].astype(str).str.strip()
    units = units[units["discourse_text"].str.len() > 0].reset_index(drop=True)
    val_idx = pd.read_csv(f"{P3}/val_predictions_L0.csv", usecols=["row_idx"])["row_idx"].values
    val = units.loc[val_idx].reset_index(drop=True)
    val_essays = set(val["essay_id_comp"])

    rows = []
    for prompt, tag in PROMPTS.items():
        lp = pd.read_csv(f"outputs/lopo_deberta_predictions/predictions_{tag}.csv")
        fold = lab[lab["prompt_name"] == prompt].reset_index(drop=True)
        assert len(fold) == len(lp), f"{prompt}: {len(fold)} vs {len(lp)}"
        assert (fold["discourse_type"].values == lp["discourse_type"].values).all()
        assert (fold["label"].values == lp["true_label"].values).all()
        fold["lopo_pred"] = lp["pred_label"].values
        in_val = fold[fold["essay_id_comp"].isin(val_essays)].reset_index(drop=True)

        vmask = (val["prompt_name"] == prompt).values
        vsub = val[vmask].reset_index(drop=True)
        # Ghép đơn vị validation của đề với dòng LOPO tương ứng (cùng bài, cùng thứ tự trong bài)
        vsub["k"] = vsub.groupby("essay_id_comp").cumcount()
        in_val["k"] = in_val.groupby("essay_id_comp").cumcount()
        m = vsub.merge(in_val[["essay_id_comp", "k", "discourse_type", "label", "lopo_pred"]],
                       on=["essay_id_comp", "k"], suffixes=("", "_lopo"))
        assert len(m) == len(vsub) and (m["discourse_type"] == m["discourse_type_lopo"]).all() \
            and (m["label"] == m["label_lopo"]).all(), f"{prompt}: ghép đơn vị lệch"
        y, lopo = m["label"].values, m["lopo_pred"].values

        rec = {"held_out_prompt": prompt.strip('"'), "n_units_same_set": len(m), "n_essays": m["essay_id_comp"].nunique(),
               "lopo_macro_f1_all_units": round(macro(fold["label"].values, fold["lopo_pred"].values), 4),
               "lopo_macro_f1_same_units": round(macro(y, lopo), 4)}
        for name, path in IN_DOMAIN.items():
            p = pd.read_csv(path)
            assert len(p) == len(val) and (p["true_label"].values == val["label"].values).all()
            ind = p["pred_label"].values[vmask]
            lo, hi = paired_bootstrap(m["essay_id_comp"].values, y, lopo, ind, rng)
            key = "w9" if "tuần 9" in name else "w11"
            rec[f"indomain_{key}_macro_f1"] = round(macro(y, ind), 4)
            rec[f"gap_lopo_minus_{key}"] = round(macro(y, lopo) - macro(y, ind), 4)
            rec[f"gap_{key}_ci95"] = f"[{lo:+.4f}, {hi:+.4f}]"
        rows.append(rec)
        print(rec)

    os.makedirs(args.output_dir, exist_ok=True)
    pd.DataFrame(rows).to_csv(os.path.join(args.output_dir, "lopo_deberta_gap_same_units.csv"), index=False)


if __name__ == "__main__":
    main()
