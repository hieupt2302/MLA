"""
TỔNG HỢP BẢNG OFFICIAL TEST (bản sửa tuần 11) — CHỈ ĐỌC KẾT QUẢ THẬT, KHÔNG CHÉP CỨNG SỐ NÀO

Bản cũ của file này chép cứng số DeBERTa "kỳ vọng" (0.5692 / 0.5724 / 0.5820) và ghi vào
outputs/official_test_final_summary.csv như kết quả. Bản này chỉ ghép các file kết quả thật:
  - RF Feature Set B   : outputs/official_test_rf_actual_result.csv + outputs/test_predictions_rf_feature_set_b.csv
  - Linear SVM         : outputs/official_test_svm_actual_result.csv (hệ thống bổ sung, không có file dự đoán)
  - DeBERTa L0/L1/PA   : Week11_Person3_DeBERTa_OfficialTest/outputs/official_test_deberta_results.csv
                         + week11_person3/test_predictions_{L0,L1,PA}.csv
và tính bootstrap ghép cặp theo bài cho DeBERTa so với RF. Không chạy lại mô hình nào, không đụng tới nhãn test
ngoài việc tính lại chỉ số từ dự đoán đã lưu.

Chạy: python script_official_test_evaluation.py
"""
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import numpy as np
import pandas as pd
from sklearn.metrics import f1_score

OUT = "outputs"
P3 = "Week11_Person3_DeBERTa_OfficialTest/outputs"
N_BOOT = 1000


def main():
    rf = pd.read_csv(f"{OUT}/official_test_rf_actual_result.csv")
    rf = rf[rf["Tập"].str.startswith("Official Test")].iloc[0]
    svm = pd.read_csv(f"{OUT}/official_test_svm_actual_result.csv").iloc[0]
    deb = pd.read_csv(f"{P3}/official_test_deberta_results.csv")

    rows = [
        {"Hệ thống": "Random Forest (Feature Set B)", "Vai trò": "chính (protocol tuần 10)",
         "Macro-F1": rf["Macro-F1"], "Accuracy (%)": rf["Accuracy (%)"], "F1 Ineffective": rf["F1 Ineffective"],
         "F1 Adequate": rf["F1 Adequate"], "F1 Effective": rf["F1 Effective"], "QWK": rf["QWK"],
         "Recall Ineffective": rf["Recall Ineffective"]},
    ]
    roles = {"3": "chính (protocol tuần 10)", "4": "chính — hệ thống được khóa", "5": "thăm dò (thêm ở tuần 11)"}
    for _, r in deb.iterrows():
        rows.append({"Hệ thống": r["Hệ thống"].split(". ", 1)[1], "Vai trò": roles[r["Hệ thống"][0]],
                     "Macro-F1": r["Macro-F1"], "Accuracy (%)": r["Accuracy (%)"], "F1 Ineffective": r["F1 Ineffective"],
                     "F1 Adequate": r["F1 Adequate"], "F1 Effective": r["F1 Effective"], "QWK": r["QWK"],
                     "Recall Ineffective": r["Recall Ineffective"]})
    rows.append({"Hệ thống": "Linear SVM (TF-IDF, train 144.289 đơn vị)", "Vai trò": "bổ sung (không có trong protocol)",
                 "Macro-F1": svm["Macro-F1"], "Accuracy (%)": svm["Accuracy (%)"], "F1 Ineffective": svm["F1 Ineffective"],
                 "F1 Adequate": svm["F1 Adequate"], "F1 Effective": svm["F1 Effective"], "QWK": np.nan,
                 "Recall Ineffective": np.nan})
    summary = pd.DataFrame(rows)
    summary.to_csv(f"{OUT}/official_test_final_summary.csv", index=False)
    summary[summary["Vai trò"].str.startswith("chính")].to_csv(
        f"{OUT}/official_test_final_3_systems_summary.csv", index=False)
    print(summary.to_string(index=False))

    # Bootstrap ghép cặp theo bài: DeBERTa − RF
    rfp = pd.read_csv(f"{OUT}/test_predictions_rf_feature_set_b.csv")
    preds = {"RF": rfp["pred_label"].values}
    for k in ["L0", "L1", "PA"]:
        d = pd.read_csv(f"{P3}/week11_person3/test_predictions_{k}.csv")
        assert (d["row_idx"].values == rfp["row_idx"].values).all(), f"{k}: thứ tự dòng lệch với RF"
        assert (d["true_label"].values == rfp["true_label"].values).all()
        preds[k] = d["pred_label"].values
    y = rfp["true_label"].values
    ess = rfp["essay_id_comp"].astype("category").cat.codes.values
    n = ess.max() + 1
    order = np.argsort(ess, kind="stable")
    bounds = np.searchsorted(ess[order], np.arange(n + 1))
    rng = np.random.default_rng(42)
    pairs = [("L0", "RF"), ("L1", "RF"), ("PA", "RF")]
    boots = {p: [] for p in pairs}
    for _ in range(N_BOOT):
        idx = np.concatenate([order[bounds[k]:bounds[k + 1]] for k in rng.integers(0, n, n)])
        for a, b in pairs:
            boots[(a, b)].append(f1_score(y[idx], preds[a][idx], average="macro")
                                 - f1_score(y[idx], preds[b][idx], average="macro"))
    out = []
    for (a, b), v in boots.items():
        v = np.array(v)
        out.append({"So sánh": f"{a} − {b}",
                    "delta_macro_f1": round(f1_score(y, preds[a], average="macro") - f1_score(y, preds[b], average="macro"), 4),
                    "ci95_low": round(np.percentile(v, 2.5), 4), "ci95_high": round(np.percentile(v, 97.5), 4),
                    "p_one_sided_delta_le_0": round((v <= 0).mean(), 4), "n_bootstrap": N_BOOT})
    pd.DataFrame(out).to_csv(f"{OUT}/official_test_bootstrap_deberta_vs_rf.csv", index=False)
    print(pd.DataFrame(out).to_string(index=False))


if __name__ == "__main__":
    main()
