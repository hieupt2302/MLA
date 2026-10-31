"""
SCRIPT 1 (bản sửa tuần 11): TÁCH ĐỘ DÀI KHỎI TRÌNH ĐỘ — ĐIỂM HOLISTIC × NHÓM ĐỘ DÀI
Phụ trách: Thành viên 1 (Data & Confound Owner)

Trả lời yêu cầu bắt buộc số 3 trong Nhan_xet_Week10: "Tính tỷ lệ lỗi theo bốn nhóm độ dài
trong cùng một mức điểm holistic" + "một câu: trong cùng điểm, lỗi có tăng theo độ dài không".

VÌ SAO PHẢI SỬA BẢN CŨ
- File CSV gốc đã từng bị mở/lưu bằng Excel: cột `discourse_id` bị làm tròn kiểu khoa học
  (1.62263E+12) -> 144.289 đơn vị có nhãn chỉ còn 728 giá trị discourse_id khác nhau.
- Bản cũ ghép dự đoán validation với điểm holistic/số từ qua `discourse_id`
  (sau drop_duplicates), nên mỗi đơn vị bị gán điểm và độ dài của MỘT BÀI KHÁC.
  Bảng cũ (lỗi ~26% phẳng ở mọi ô) là sản phẩm của phép ghép sai, không phải kết quả.
- Bản này ghép theo VỊ TRÍ: mọi file dự đoán validation có cùng thứ tự dòng với bảng
  đơn vị có nhãn (đã kiểm tra bằng essay_id_comp + discourse_start + discourse_type + nhãn),
  và file dự đoán tuần 11 có sẵn `row_idx` = chỉ số dòng trong bảng đó.

ĐẦU RA (thư mục outputs/)
- holistic_score_x_length_quartile_error_rates.csv : bảng dài — mô hình × tập × điểm × nhóm độ dài,
  kèm N đơn vị, N bài, tỷ lệ lỗi, khoảng tin cậy 95% bootstrap theo bài.
- length_quartile_marginal_error_by_model.csv      : tỷ lệ lỗi theo nhóm độ dài khi KHÔNG kiểm soát điểm.
- length_within_score_regression.csv               : hồi quy logistic lỗi ~ điểm (biến phân loại) + nhóm độ dài,
  sai số chuẩn cụm theo bài.

Chạy:  python Person1/script_holistic_length_table.py --train_csv <train.csv> [--test_csv <test.csv>]
Thời gian: ~1 phút (CPU).
"""

import argparse
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

LABEL2ID = {"Ineffective": 0, "Adequate": 1, "Effective": 2}
# Ranh giới tứ phân vị độ dài bài, tính trên 29.102 đơn vị validation ở tuần 10 (pd.qcut theo đơn vị).
# Giữ cố định để so được với bảng 3.2 tuần 10 và áp nguyên cho tập test.
QUARTILE_EDGES = [-np.inf, 315, 422, 566, np.inf]
QUARTILE_LABELS = ["Q1 (<=315)", "Q2 (316-422)", "Q3 (423-566)", "Q4 (>=567)"]

P3 = "Week11_Person3_DeBERTa_OfficialTest/outputs/week11_person3"
VAL_MODELS = {
    # tên hiển thị: (đường dẫn, cột nhãn dự đoán, ánh xạ nhãn nếu là chữ)
    "RF Feature Set B (tuần 9)": ("outputs/strongest_baseline_predictions.csv", "discourse_effectiveness_pred", LABEL2ID),
    "DeBERTa L1 (lượt chạy tuần 10)": ("outputs/context_ablation_predictions.csv", "pred_label", None),
    "DeBERTa L0 (tuần 11, mô hình đã chấm test)": (f"{P3}/val_predictions_L0.csv", "pred_label", None),
    "DeBERTa L1 (tuần 11, mô hình đã chấm test)": (f"{P3}/val_predictions_L1.csv", "pred_label", None),
}
TEST_MODELS = {
    "DeBERTa L1 (tuần 11, mô hình đã chấm test)": f"{P3}/test_predictions_L1.csv",
}
N_BOOT = 1000
RNG = np.random.default_rng(42)


def load_units(path):
    """Cùng quy tắc lọc với notebook 07 -> chỉ số dòng trùng `row_idx` trong file dự đoán."""
    cols = ["essay_id_comp", "discourse_start", "discourse_type", "discourse_text",
            "discourse_effectiveness", "holistic_essay_score", "essay_word_count"]
    df = pd.read_csv(path, usecols=cols, dtype=str, low_memory=False)
    df = df.dropna(subset=["discourse_effectiveness", "discourse_text"]).copy()
    df["discourse_text"] = df["discourse_text"].astype(str).str.strip()
    df = df[df["discourse_text"].str.len() > 0].reset_index(drop=True)
    df["label"] = df["discourse_effectiveness"].map(LABEL2ID).astype(int)
    df["holistic_essay_score"] = pd.to_numeric(df["holistic_essay_score"]).astype(int)
    df["essay_word_count"] = pd.to_numeric(df["essay_word_count"])
    df["length_q"] = pd.cut(df["essay_word_count"], QUARTILE_EDGES, labels=QUARTILE_LABELS)
    df["q_idx"] = df["length_q"].cat.codes
    return df


def attach_predictions(units, pred_path, pred_col, label_map, row_idx_ref):
    """Gắn dự đoán vào đúng đơn vị và kiểm tra khớp trước khi dùng."""
    p = pd.read_csv(pred_path, dtype=str)
    assert len(p) == len(row_idx_ref), f"{pred_path}: {len(p)} dòng, cần {len(row_idx_ref)}"
    if "row_idx" in p.columns:
        assert (p["row_idx"].astype(int).values == row_idx_ref).all(), f"{pred_path}: row_idx lệch thứ tự"
        assert (p["essay_id_comp"].values == units.loc[row_idx_ref, "essay_id_comp"].values).all()
    sub = units.loc[row_idx_ref].copy()
    assert (p["discourse_type"].values == sub["discourse_type"].values).all(), f"{pred_path}: discourse_type lệch"
    true_col = "true_label" if "true_label" in p.columns else "discourse_effectiveness_true"
    true = p[true_col].map(label_map).values if label_map else p[true_col].astype(int).values
    assert (true == sub["label"].values).all(), f"{pred_path}: nhãn gold lệch"
    pred = p[pred_col].map(label_map).values if label_map else p[pred_col].astype(int).values
    sub["pred"] = pred
    sub["error"] = (pred != sub["label"].values).astype(int)
    return sub.reset_index(drop=True)


def essay_bootstrap_ci(cell):
    """CI 95% cho tỷ lệ lỗi, lấy mẫu lại theo bài (các đơn vị trong cùng bài không độc lập)."""
    g = cell.groupby("essay_id_comp")["error"].agg(["sum", "count"])
    if len(g) < 2:
        return np.nan, np.nan
    s, c = g["sum"].values, g["count"].values
    idx = RNG.integers(0, len(g), size=(N_BOOT, len(g)))
    rates = s[idx].sum(1) / c[idx].sum(1)
    return np.percentile(rates, 2.5), np.percentile(rates, 97.5)


def score_x_length_table(d, model, split):
    rows = []
    for (score, q), cell in d.groupby(["holistic_essay_score", "length_q"], observed=True):
        lo, hi = essay_bootstrap_ci(cell)
        rows.append({"model": model, "split": split, "holistic_essay_score": score, "length_quartile": q,
                     "n_units": len(cell), "n_essays": cell["essay_id_comp"].nunique(),
                     "error_rate_pct": round(100 * cell["error"].mean(), 2),
                     "ci95_low_pct": round(100 * lo, 2), "ci95_high_pct": round(100 * hi, 2)})
    return rows


def marginal_table(d, model, split):
    rows = []
    for q, cell in d.groupby("length_q", observed=True):
        rows.append({"model": model, "split": split, "length_quartile": q, "n_units": len(cell),
                     "n_essays": cell["essay_id_comp"].nunique(),
                     "mean_holistic_score": round(cell.drop_duplicates("essay_id_comp")["holistic_essay_score"].mean(), 2),
                     "pct_ineffective": round(100 * (cell["label"] == 0).mean(), 2),
                     "pct_effective": round(100 * (cell["label"] == 2).mean(), 2),
                     "error_rate_pct": round(100 * cell["error"].mean(), 2),
                     # Tỷ lệ lỗi là nhầm lẫn Adequate <-> Effective (bảng phân rã lỗi nhóm dài nhất)
                     "pct_errors_adequate_vs_effective": round(100 * (
                         (cell["error"] == 1) & cell["label"].isin([1, 2]) & cell["pred"].isin([1, 2])
                     ).sum() / max(cell["error"].sum(), 1), 2)})
    return rows


def regression(d, model, split):
    """lỗi ~ C(điểm) + q_idx (0..3); hệ số q_idx = thay đổi log-odds lỗi khi lên 1 nhóm độ dài, giữ nguyên điểm."""
    rows = []
    groups = d["essay_id_comp"].astype("category").cat.codes
    specs = [("không kiểm soát điểm", "error ~ q_idx"),
             ("có kiểm soát điểm", "error ~ C(holistic_essay_score) + q_idx"),
             # Bài dài trong cùng mức điểm có nhiều đơn vị Effective hơn -> tách phần do thành phần nhãn
             ("kiểm soát điểm + nhãn gold + loại đơn vị",
              "error ~ C(holistic_essay_score) + C(label) + C(discourse_type) + q_idx")]
    for name, formula in specs:
        fit = smf.glm(formula, data=d, family=sm.families.Binomial()).fit(
            cov_type="cluster", cov_kwds={"groups": groups})
        b, (lo, hi) = fit.params["q_idx"], fit.conf_int().loc["q_idx"]
        rows.append({"model": model, "split": split, "spec": name, "coef_q_idx_logodds": round(b, 4),
                     "odds_ratio_per_quartile": round(np.exp(b), 3), "or_ci95_low": round(np.exp(lo), 3),
                     "or_ci95_high": round(np.exp(hi), 3), "p_value": round(fit.pvalues["q_idx"], 4), "n_units": len(d)})
    # Riêng từng mức điểm có đủ 4 nhóm độ dài
    for score in (3, 4):
        ds = d[d["holistic_essay_score"] == score]
        g = ds["essay_id_comp"].astype("category").cat.codes
        fit = smf.glm("error ~ q_idx", data=ds, family=sm.families.Binomial()).fit(
            cov_type="cluster", cov_kwds={"groups": g})
        b, (lo, hi) = fit.params["q_idx"], fit.conf_int().loc["q_idx"]
        rows.append({"model": model, "split": split, "spec": f"chỉ bài điểm {score}", "coef_q_idx_logodds": round(b, 4),
                     "odds_ratio_per_quartile": round(np.exp(b), 3), "or_ci95_low": round(np.exp(lo), 3),
                     "or_ci95_high": round(np.exp(hi), 3), "p_value": round(fit.pvalues["q_idx"], 4), "n_units": len(ds)})
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--train_csv", default="persuade_corpus_2.0_train.csv")
    ap.add_argument("--test_csv", default=None, help="tùy chọn: phân tích mô tả thêm trên test (không chọn mô hình)")
    ap.add_argument("--output_dir", default="outputs")
    args = ap.parse_args()

    units = load_units(args.train_csv)
    ref = pd.read_csv(VAL_MODELS["DeBERTa L1 (tuần 11, mô hình đã chấm test)"][0], usecols=["row_idx"])["row_idx"].values
    print(f"Đơn vị có nhãn: {len(units):,} | validation: {len(ref):,}")

    cells, marg, reg = [], [], []
    for model, (path, col, lmap) in VAL_MODELS.items():
        d = attach_predictions(units, path, col, lmap, ref)
        cells += score_x_length_table(d, model, "validation")
        marg += marginal_table(d, model, "validation")
        reg += regression(d, model, "validation")
        print(f"[OK] {model}: lỗi tổng {100 * d['error'].mean():.2f}%")

    if args.test_csv:
        tunits = load_units(args.test_csv)
        for model, path in TEST_MODELS.items():
            tref = pd.read_csv(path, usecols=["row_idx"])["row_idx"].values
            d = attach_predictions(tunits, path, "pred_label", None, tref)
            cells += score_x_length_table(d, model, "official_test")
            marg += marginal_table(d, model, "official_test")
            reg += regression(d, model, "official_test")
            print(f"[OK] {model} (test): lỗi tổng {100 * d['error'].mean():.2f}%")

    os.makedirs(args.output_dir, exist_ok=True)
    outs = {"holistic_score_x_length_quartile_error_rates.csv": cells,
            "length_quartile_marginal_error_by_model.csv": marg,
            "length_within_score_regression.csv": reg}
    for name, rows in outs.items():
        pd.DataFrame(rows).to_csv(os.path.join(args.output_dir, name), index=False, encoding="utf-8")
        print(f"-> {os.path.join(args.output_dir, name)}")

    reg_df = pd.DataFrame(reg)
    print("\n" + reg_df.to_string(index=False))


if __name__ == "__main__":
    main()
