"""
SCRIPT 2 (bản sửa tuần 11): HẠ NGƯỠNG LỚP INEFFECTIVE TRÊN FILE XÁC SUẤT ĐÃ LƯU — BAO NHIÊU CA ĐỔI?
Phụ trách: Thành viên 2

Trả lời bước 5 trong "Một lượt đi qua để luyện interview" (Nhan_xet_Week10):
"hạ ngưỡng quyết định cho lớp Ineffective trên file xác suất đã lưu, xem bao nhiêu ca đổi".

Quy tắc: dự đoán Ineffective nếu P(Ineffective) >= theta, ngược lại lấy argmax giữa Adequate/Effective.
Mốc so sánh là argmax gốc (KHÔNG có "ngưỡng mặc định 0.33").
Chỉ dùng validation; không chọn ngưỡng trên test.

Sửa so với bản cũ:
- Ca 8 trước đây được "tìm" bằng bộ lọc Claim & 0.11 < P < 0.13 rồi lấy dòng đầu tiên -> có thể là ca khác.
  Nay 10 ca được xác định bằng đúng đoạn văn bản (ghép theo vị trí dòng, không dùng discourse_id
  vì cột này đã bị Excel làm tròn).
- Báo cáo số ca đổi nhãn (trong 10 ca và trên toàn bộ 29.102 đơn vị) và cái giá về Macro-F1.

Chạy: python script_threshold_tuning_and_case8.py --train_csv <train.csv>
"""
import argparse
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import numpy as np
import pandas as pd
from sklearn.metrics import f1_score, precision_recall_fscore_support

P3 = "Week11_Person3_DeBERTa_OfficialTest/outputs/week11_person3"
PRED_FILES = {
    "DeBERTa L1 (lượt chạy tuần 10 — mô hình của 10 ca)": "outputs/context_ablation_predictions.csv",
    "DeBERTa L1 (tuần 11 — mô hình đã chấm test)": f"{P3}/val_predictions_L1.csv",
}
CASES_CSV = "outputs/context_ablation_case_study_recheck.csv"
THRESHOLDS = [0.05, 0.08, 0.10, 0.12, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50]


def decide(proba, theta):
    if theta is None:
        return proba.argmax(1)
    return np.where(proba[:, 0] >= theta, 0, np.where(proba[:, 2] > proba[:, 1], 2, 1))


def locate_cases(train_csv, val_row_idx):
    df = pd.read_csv(train_csv, usecols=["discourse_text", "discourse_effectiveness", "discourse_type"], dtype=str)
    df = df.dropna(subset=["discourse_effectiveness", "discourse_text"]).copy()
    df["discourse_text"] = df["discourse_text"].astype(str).str.strip()
    df = df[df["discourse_text"].str.len() > 0].reset_index(drop=True)
    val = df.loc[val_row_idx].reset_index(drop=True)          # vị trí i = dòng i của file dự đoán
    cases = pd.read_csv(CASES_CSV)
    pos = []
    for _, c in cases.iterrows():
        hit = val.index[val["discourse_text"].str.startswith(c["target_snippet"].strip())
                        & (val["discourse_type"] == c["discourse_type"])
                        & (val["discourse_effectiveness"] == "Ineffective")]
        assert len(hit) == 1, f"ca {c['case_id']}: tìm thấy {len(hit)} dòng"
        pos.append(hit[0])
    cases["val_pos"] = pos
    return cases


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--train_csv", default="persuade_corpus_2.0_train.csv")
    ap.add_argument("--output_dir", default="outputs")
    args = ap.parse_args()

    ref = pd.read_csv(PRED_FILES["DeBERTa L1 (tuần 11 — mô hình đã chấm test)"], usecols=["row_idx"])["row_idx"].values
    cases = locate_cases(args.train_csv, ref)

    sweep, case_rows = [], []
    for model, path in PRED_FILES.items():
        p = pd.read_csv(path)
        y = p["true_label"].values
        proba = p[["pred_proba_0", "pred_proba_1", "pred_proba_2"]].values
        base = decide(proba, None)
        for theta in [None] + THRESHOLDS:
            pred = decide(proba, theta)
            prec, rec, f1c, _ = precision_recall_fscore_support(y, pred, labels=[0, 1, 2], zero_division=0)
            cp = pred[cases["val_pos"].values]
            sweep.append({
                "model": model, "rule": "argmax" if theta is None else f"P(Ineff) >= {theta:.2f}",
                "ineff_precision_pct": round(100 * prec[0], 2), "ineff_recall_pct": round(100 * rec[0], 2),
                "ineff_f1": round(f1c[0], 4), "macro_f1": round(f1_score(y, pred, average="macro"), 4),
                "n_pred_ineffective": int((pred == 0).sum()),
                "n_units_changed_vs_argmax": int((pred != base).sum()),
                "n_gold_ineff_newly_caught": int(((pred == 0) & (base != 0) & (y == 0)).sum()),
                "n_false_alarms_added": int(((pred == 0) & (base != 0) & (y != 0)).sum()),
                "cases_flipped_to_ineffective_of_10": int((cp == 0).sum()),
            })
        if "tuần 10" in model:
            for _, c in cases.iterrows():
                pi = proba[c["val_pos"], 0]
                assert abs(pi - c["level1_p_ineff"]) < 5e-4, f"ca {c['case_id']}: P lệch {pi} vs {c['level1_p_ineff']}"
                case_rows.append({"case_id": c["case_id"], "discourse_type": c["discourse_type"],
                                  "snippet": c["target_snippet"], "p_ineff_L1": round(pi, 4),
                                  "max_theta_that_flips": round(pi, 4)})

    os.makedirs(args.output_dir, exist_ok=True)
    out = pd.DataFrame(sweep)
    out.to_csv(os.path.join(args.output_dir, "ineffective_threshold_tuning_table.csv"), index=False)
    pd.DataFrame(case_rows).to_csv(os.path.join(args.output_dir, "threshold_case_flips.csv"), index=False)
    print(out.to_string(index=False))
    print(pd.DataFrame(case_rows).to_string(index=False))


if __name__ == "__main__":
    main()
