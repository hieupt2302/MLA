"""
RANDOM FOREST FEATURE SET B TRÊN OFFICIAL TEST (bản sửa tuần 11)

Vì sao sửa: bản trước (Random Forest 100 cây, depth 30, TF-IDF 10k, min_df=3, chỉ 1 đặc trưng độ dài
chưa chuẩn hóa, huấn luyện trên toàn bộ 144.289 đơn vị) KHÔNG phải mô hình RF Feature Set B đã
chọn trên validation ở tuần 9 (01_Data_Pipeline_Classical_Baseline.py). Protocol tuần 10 yêu cầu
chấm đúng RF Feature Set B, nên script này dựng lại y nguyên cấu hình tuần 9:
  - TF-IDF 15.000 đặc trưng, ngram (1,2), min_df=2, sublinear_tf
  - one-hot discourse_type
  - 5 đặc trưng cấu trúc (char_len, word_count, essay_wc, position_ratio, length_ratio), StandardScaler
  - RandomForest(n_estimators=200, max_depth=35, min_samples_split=5, class_weight='balanced', seed 42)
  - huấn luyện trên đúng 115.187 đơn vị train (cùng split với DeBERTa), không dùng validation.
Kiểm tra trước: Macro-F1 validation phải tái tạo ~0.5230 (số tuần 9) thì mới chấm test.
Không có bước chọn siêu tham số nào dùng tập test.

Phiên bản: dùng scikit-learn==1.6.1 (môi trường Colab tuần 9). Với 1.6.1: val Macro-F1 0.5261, acc 77.34%
(tuần 9: 0.5230 / 77.22%). Với 1.9.0, Macro-F1 gần như giữ nguyên (val 0.5273, test 0.5106) nhưng RF
dự đoán Ineffective nhiều hơn hẳn (acc val 70.15%) -> số chính thức lấy từ 1.6.1.

Chạy: python Person1/run_rf_official_test.py --train_csv <train.csv> --test_csv <test.csv>
"""
import argparse
import json
import os
import sys
import time

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import numpy as np
import pandas as pd
import scipy.sparse as sp
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, cohen_kappa_score, f1_score, precision_recall_fscore_support
from sklearn.preprocessing import OneHotEncoder, StandardScaler

LABEL2ID = {"Ineffective": 0, "Adequate": 1, "Effective": 2}
VAL_PRED = "Week11_Person3_DeBERTa_OfficialTest/outputs/week11_person3/val_predictions_L1.csv"
WEEK9_VAL_MACRO_F1 = 0.5230
SEED = 42


def load_units(path):
    """Cùng quy tắc lọc với notebook 07 -> chỉ số dòng = row_idx trong các file dự đoán DeBERTa."""
    cols = ["essay_id_comp", "full_text", "discourse_start", "discourse_text", "discourse_type",
            "discourse_effectiveness", "essay_word_count"]
    df = pd.read_csv(path, usecols=cols, dtype=str, low_memory=False)
    df = df.dropna(subset=["discourse_effectiveness", "discourse_text"]).copy()
    df["discourse_text"] = df["discourse_text"].astype(str).str.strip()
    df = df[df["discourse_text"].str.len() > 0].reset_index(drop=True)
    df["row_idx"] = np.arange(len(df))
    df["label"] = df["discourse_effectiveness"].map(LABEL2ID).astype(int)
    df["essay_word_count"] = pd.to_numeric(df["essay_word_count"], errors="coerce")
    df["discourse_start"] = pd.to_numeric(df["discourse_start"], errors="coerce")
    return df


def handcrafted(df):
    """Giống hệt extract_handcrafted_features() ở 01_Data_Pipeline_Classical_Baseline.py."""
    disc = df["discourse_text"].fillna("")
    full = df["full_text"].fillna("")
    char_len = disc.str.len().values.reshape(-1, 1)
    word_count = disc.str.split().str.len().fillna(0).values.reshape(-1, 1)
    essay_wc = df["essay_word_count"].fillna(pd.Series(word_count.ravel(), index=df.index)).values.reshape(-1, 1)
    essay_char_len = full.str.len().clip(lower=1).values.reshape(-1, 1)
    start = df["discourse_start"].fillna(0).values.reshape(-1, 1)
    position_ratio = np.clip(start / essay_char_len, 0.0, 1.0)
    length_ratio = np.clip(word_count / np.clip(essay_wc, 1.0, None), 0.0, 1.0)
    return np.hstack([char_len, word_count, essay_wc, position_ratio, length_ratio]).astype(float)


def metrics(y, p):
    prec, rec, f1c, _ = precision_recall_fscore_support(y, p, labels=[0, 1, 2], zero_division=0)
    return {"Macro-F1": round(f1_score(y, p, average="macro"), 4), "Accuracy (%)": round(100 * accuracy_score(y, p), 2),
            "F1 Ineffective": round(f1c[0], 4), "F1 Adequate": round(f1c[1], 4), "F1 Effective": round(f1c[2], 4),
            "Recall Ineffective": round(rec[0], 4), "Precision Ineffective": round(prec[0], 4),
            "QWK": round(cohen_kappa_score(y, p, weights="quadratic"), 4)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--train_csv", default="persuade_corpus_2.0_train.csv")
    ap.add_argument("--test_csv", default="persuade_corpus_2.0_test.csv")
    ap.add_argument("--output_dir", default="outputs")
    ap.add_argument("--tolerance", type=float, default=0.01, help="sai lệch tối đa so với Macro-F1 validation tuần 9")
    args = ap.parse_args()
    t0 = time.time()

    units = load_units(args.train_csv)
    val_idx = pd.read_csv(VAL_PRED, usecols=["row_idx"])["row_idx"].values
    is_val = np.zeros(len(units), bool)
    is_val[val_idx] = True
    tr, va = units[~is_val].reset_index(drop=True), units[is_val].reset_index(drop=True)
    te = load_units(args.test_csv)
    print(f"train {len(tr):,} | val {len(va):,} | test {len(te):,}")
    assert len(tr) == 115187 and len(va) == 29102 and len(te) == 93677

    tfidf = TfidfVectorizer(max_features=15000, min_df=2, ngram_range=(1, 2), sublinear_tf=True)
    ohe = OneHotEncoder(sparse_output=True, handle_unknown="ignore")
    scaler = StandardScaler()
    X_tr = sp.hstack([tfidf.fit_transform(tr["discourse_text"]), ohe.fit_transform(tr[["discourse_type"]]),
                      sp.csr_matrix(scaler.fit_transform(handcrafted(tr)))], format="csr")

    def transform(d):
        return sp.hstack([tfidf.transform(d["discourse_text"]), ohe.transform(d[["discourse_type"]]),
                          sp.csr_matrix(scaler.transform(handcrafted(d)))], format="csr")

    rf = RandomForestClassifier(n_estimators=200, max_depth=35, min_samples_split=5,
                                class_weight="balanced", random_state=SEED, n_jobs=-1)
    rf.fit(X_tr, tr["label"].values)
    fit_s = time.time() - t0

    p_va = rf.predict(transform(va))
    m_va = metrics(va["label"].values, p_va)
    print("Validation:", m_va)
    if abs(m_va["Macro-F1"] - WEEK9_VAL_MACRO_F1) > args.tolerance:
        raise SystemExit(f"Không tái tạo được RF tuần 9 ({m_va['Macro-F1']} vs {WEEK9_VAL_MACRO_F1}) -> KHÔNG chấm test.")

    t1 = time.time()
    proba_te = rf.predict_proba(transform(te))
    p_te = rf.classes_[proba_te.argmax(1)]
    m_te = metrics(te["label"].values, p_te)
    print("Official test:", m_te)

    os.makedirs(args.output_dir, exist_ok=True)
    rows = [{"Hệ thống": "Random Forest (Feature Set B)", "Tập": "Validation (29.102)", **m_va},
            {"Hệ thống": "Random Forest (Feature Set B)", "Tập": "Official Test (93.677)", **m_te,
             "Runtime (s)": round(fit_s + time.time() - t1, 1)}]
    pd.DataFrame(rows).to_csv(os.path.join(args.output_dir, "official_test_rf_actual_result.csv"), index=False)
    pd.DataFrame({"row_idx": te["row_idx"], "essay_id_comp": te["essay_id_comp"], "discourse_type": te["discourse_type"],
                  "true_label": te["label"], "pred_label": p_te, "pred_proba_0": proba_te[:, 0].round(6),
                  "pred_proba_1": proba_te[:, 1].round(6), "pred_proba_2": proba_te[:, 2].round(6)}
                 ).to_csv(os.path.join(args.output_dir, "test_predictions_rf_feature_set_b.csv"), index=False)
    with open(os.path.join(args.output_dir, "official_test_rf_run_metadata.json"), "w", encoding="utf-8") as f:
        json.dump({"config": "Feature Set B + RF(200, depth 35, min_samples_split 5, balanced, seed 42)",
                   "train_units": len(tr), "val_units": len(va), "test_units": len(te),
                   "week9_val_macro_f1": WEEK9_VAL_MACRO_F1, "reproduced_val_macro_f1": m_va["Macro-F1"],
                   "sklearn_version": sklearn.__version__,
                   "finished_at": time.strftime("%Y-%m-%d %H:%M:%S")}, f, ensure_ascii=False, indent=2)
    print(f"Xong sau {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
