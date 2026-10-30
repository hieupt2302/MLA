"""
========================================================================================
SCRIPT ĐÁNH GIÁ NGHIỆM THU TẬP KIỂM TRA CHÍNH THỨC (OFFICIAL TEST BENCHMARK MASTER)
Tệp: script_official_test_evaluation.py
Phụ trách: Thành viên 3 (LOPO & Evaluation Protocol Owner)

MỤC ĐÍCH KHOA HỌC:
Thực hiện yêu cầu bắt buộc số 2 trong nhận xét Tuần 10 của Thầy Khánh:
"Chấm cả mốc trong lần chạy test duy nhất: chấm cùng lượt RF (Feature Set B),
 DeBERTa Level 0 và Level 1; ghi rõ L0 và L1 không phân biệt được trên validation.
 Bảng test có ba dòng (nay mở rộng thêm Linear SVM đối chứng cùng họ và Prompt-Aware)."

CẤU TRÚC MÃ NGUỒN TỔNG HỢP:
- [HỆ THỐNG 1]: Linear SVM (TF-IDF Baseline - Course Model Family)
- [HỆ THỐNG 2]: Random Forest (Feature Set B - Tree Ensemble Baseline)
- [HỆ THỐNG 3]: DeBERTa-v3 Level 0 (Isolated Unit Transformer)
- [HỆ THỐNG 4]: DeBERTa-v3 Level 1 (Contextual ±1 Sentence Transformer - Locked Model)
- [HỆ THỐNG 5]: DeBERTa-v3 Prompt-Aware (Contextual + Prompt Name Improved Model)
- [TỔNG HỢP]:   Xuất bảng CSV tổng hợp chính thức: outputs/official_test_final_summary.csv
========================================================================================
"""

import os
import sys

# Đảm bảo xuất UTF-8 an toàn trên Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

import argparse
import time
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score, accuracy_score, precision_recall_fscore_support
import scipy.sparse as sp

# Cố định ánh xạ nhãn
LABEL_MAP = {'Ineffective': 0, 'Adequate': 1, 'Effective': 2}
INV_LABEL_MAP = {0: 'Ineffective', 1: 'Adequate', 2: 'Effective'}
RANDOM_SEED = 42

def load_clean_data(train_csv_path, test_csv_path, nrows=None):
    """Đọc dữ liệu train và test với ép kiểu chuỗi ID nghiêm ngặt"""
    print("="*80)
    print("BƯỚC 1: ĐỌC DỮ LIỆU HUẤN LUYỆN VÀ KIỂM THỬ CHÍNH THỨC")
    print("="*80)
    print(f"-> Đang đọc tập Train: {train_csv_path}...")
    df_train = pd.read_csv(
        train_csv_path,
        nrows=nrows,
        dtype={'essay_id': str, 'discourse_id': str},
        usecols=['essay_id', 'discourse_id', 'discourse_text', 'discourse_type', 'discourse_effectiveness', 'discourse_start']
    ).dropna(subset=['discourse_effectiveness', 'discourse_text'])

    print(f"-> Đang đọc tập Test: {test_csv_path}...")
    df_test = pd.read_csv(
        test_csv_path,
        nrows=nrows,
        dtype={'essay_id': str, 'discourse_id': str},
        usecols=['essay_id', 'discourse_id', 'discourse_text', 'discourse_type', 'discourse_effectiveness', 'discourse_start']
    ).dropna(subset=['discourse_effectiveness', 'discourse_text'])

    df_train['target'] = df_train['discourse_effectiveness'].map(LABEL_MAP)
    df_test['target'] = df_test['discourse_effectiveness'].map(LABEL_MAP)

    print(f"-> Số mẫu Train: {len(df_train):,} | Số mẫu Test: {len(df_test):,}")
    return df_train, df_test


# ======================================================================================
# [HỆ THỐNG 1]: LINEAR SVM BASELINE (HỌ MÔ HÌNH TUYẾN TÍNH MÔN HỌC)
# ======================================================================================
def evaluate_linear_svm_on_test(df_train, df_test, output_dir='outputs'):
    print("\n" + "="*80)
    print(">>> ĐANG ĐÁNH GIÁ HỆ THỐNG 1: LINEAR SVM (TF-IDF BASELINE) <<<")
    print("="*80)
    
    saved_csv = os.path.join(output_dir, 'official_test_svm_actual_result.csv')
    if os.path.exists(saved_csv):
        print(f"-> Đã có sẵn kết quả thực nghiệm từ {saved_csv}:")
        df_saved = pd.read_csv(saved_csv)
        row = df_saved.iloc[0]
        res = {
            'Hệ thống': '1. Linear SVM (TF-IDF Baseline)',
            'Kiểu mô hình & Đầu vào': 'Tuyến tính / Phân loại lề (TF-IDF 15k từ)',
            'Macro-F1': float(row['Macro-F1']),
            'Accuracy (%)': float(row['Accuracy (%)']),
            'F1 Ineffective': float(row['F1 Ineffective']),
            'F1 Adequate': float(row['F1 Adequate']),
            'F1 Effective': float(row['F1 Effective'])
        }
        print(f"   Macro-F1 = {res['Macro-F1']:.4f} | Accuracy = {res['Accuracy (%)']:.2f}% | Ineff F1 = {res['F1 Ineffective']:.4f}")
        return res

    t0 = time.time()
    vec = TfidfVectorizer(max_features=15000, ngram_range=(1, 2), min_df=3, sublinear_tf=True)
    X_train = vec.fit_transform(df_train['discourse_text'])
    X_test = vec.transform(df_test['discourse_text'])
    y_train = df_train['target'].values
    y_test = df_test['target'].values

    clf = LinearSVC(C=1.0, class_weight='balanced', random_state=RANDOM_SEED, max_iter=2000)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    macro_f1 = f1_score(y_test, y_pred, labels=[0, 1, 2], average='macro', zero_division=0)
    acc = accuracy_score(y_test, y_pred)
    f1_per_class = f1_score(y_test, y_pred, labels=[0, 1, 2], average=None, zero_division=0)
    elapsed = time.time() - t0

    print(f"-> Hoàn thành trong {elapsed:.1f}s | Macro-F1 = {macro_f1:.4f} | Accuracy = {acc*100:.2f}% | Ineff F1 = {f1_per_class[0]:.4f}")
    return {
        'Hệ thống': '1. Linear SVM (TF-IDF Baseline)',
        'Kiểu mô hình & Đầu vào': 'Tuyến tính / Phân loại lề (TF-IDF 15k từ)',
        'Macro-F1': round(macro_f1, 4),
        'Accuracy (%)': round(acc * 100, 2),
        'F1 Ineffective': round(f1_per_class[0], 4),
        'F1 Adequate': round(f1_per_class[1], 4),
        'F1 Effective': round(f1_per_class[2], 4)
    }


# ======================================================================================
# [HỆ THỐNG 2]: RANDOM FOREST BASELINE (FEATURE SET B)
# ======================================================================================
def evaluate_random_forest_on_test(df_train, df_test, output_dir='outputs'):
    print("\n" + "="*80)
    print(">>> ĐANG ĐÁNH GIÁ HỆ THỐNG 2: RANDOM FOREST (FEATURE SET B) <<<")
    print("="*80)

    saved_csv = os.path.join(output_dir, 'official_test_rf_actual_result.csv')
    if os.path.exists(saved_csv):
        print(f"-> Đã có sẵn kết quả thực nghiệm từ {saved_csv}:")
        df_saved = pd.read_csv(saved_csv)
        row = df_saved.iloc[0]
        res = {
            'Hệ thống': '2. Random Forest (Feature Set B)',
            'Kiểu mô hình & Đầu vào': 'Rừng cây quyết định (Bag-of-words + Role + Len)',
            'Macro-F1': float(row['Macro-F1']),
            'Accuracy (%)': float(row['Accuracy (%)']),
            'F1 Ineffective': float(row['F1 Ineffective']),
            'F1 Adequate': float(row['F1 Adequate']),
            'F1 Effective': float(row['F1 Effective'])
        }
        print(f"   Macro-F1 = {res['Macro-F1']:.4f} | Accuracy = {res['Accuracy (%)']:.2f}% | Ineff F1 = {res['F1 Ineffective']:.4f}")
        return res

    t0 = time.time()
    tfidf = TfidfVectorizer(max_features=10000, ngram_range=(1, 2), min_df=3, sublinear_tf=True)
    X_train_text = tfidf.fit_transform(df_train['discourse_text'])
    X_test_text = tfidf.transform(df_test['discourse_text'])

    ohe = OneHotEncoder(handle_unknown='ignore')
    X_train_type = ohe.fit_transform(df_train[['discourse_type']])
    X_test_type = ohe.transform(df_test[['discourse_type']])

    train_lens = sp.csr_matrix(df_train['discourse_text'].apply(lambda x: len(str(x).split())).values[:, None])
    test_lens = sp.csr_matrix(df_test['discourse_text'].apply(lambda x: len(str(x).split())).values[:, None])

    X_train = sp.hstack([X_train_text, X_train_type, train_lens])
    X_test = sp.hstack([X_test_text, X_test_type, test_lens])
    y_train = df_train['target'].values
    y_test = df_test['target'].values

    rf = RandomForestClassifier(n_estimators=100, max_depth=30, class_weight='balanced', random_state=RANDOM_SEED, n_jobs=-1)
    rf.fit(X_train, y_train)
    y_pred = rf.predict(X_test)

    macro_f1 = f1_score(y_test, y_pred, labels=[0, 1, 2], average='macro', zero_division=0)
    acc = accuracy_score(y_test, y_pred)
    f1_per_class = f1_score(y_test, y_pred, labels=[0, 1, 2], average=None, zero_division=0)
    elapsed = time.time() - t0

    print(f"-> Hoàn thành trong {elapsed:.1f}s | Macro-F1 = {macro_f1:.4f} | Accuracy = {acc*100:.2f}% | Ineff F1 = {f1_per_class[0]:.4f}")
    return {
        'Hệ thống': '2. Random Forest (Feature Set B)',
        'Kiểu mô hình & Đầu vào': 'Rừng cây quyết định (Bag-of-words + Role + Len)',
        'Macro-F1': round(macro_f1, 4),
        'Accuracy (%)': round(acc * 100, 2),
        'F1 Ineffective': round(f1_per_class[0], 4),
        'F1 Adequate': round(f1_per_class[1], 4),
        'F1 Effective': round(f1_per_class[2], 4)
    }


# ======================================================================================
# [HỆ THỐNG 3, 4, 5]: DEBERTA-V3 LEVEL 0 / LEVEL 1 / PROMPT-AWARE
# Số liệu THỰC TẾ do notebook 07_person3_prompt_aware_official_test.ipynb chấm trên Colab GPU
# (cùng một lượt test, có khóa OFFICIAL_TEST_LOCK.json). Không dùng số gõ tay.
# ======================================================================================
DEBERTA_SYSTEMS = [
    ('3. DeBERTa-v3 Level 0', 'Deep Learning Transformer (Câu cô lập [Type] [SEP] [Text])'),
    ('4. DeBERTa-v3 Level 1 (Khóa)', 'Transformer Ngữ cảnh (Kèm 2 câu lân cận [Prev] [Target] [Next])'),
    ('5. DeBERTa-v3 Level 1 + Prompt-Aware', 'Transformer Ngữ cảnh + Tên đề bài ([Prompt] [SEP] [Context])'),
]


def load_deberta_test_results(output_dir='outputs'):
    print("\n" + "="*80)
    print(">>> ĐANG NẠP HỆ THỐNG 3–5: DEBERTA-V3 L0 / L1 / PROMPT-AWARE (TỪ NOTEBOOK 07) <<<")
    print("="*80)

    saved_csv = os.path.join(output_dir, 'official_test_deberta_results.csv')
    if not os.path.exists(saved_csv):
        print(f"-> CHƯA CÓ {saved_csv}. Hãy chạy notebook 07_person3_prompt_aware_official_test.ipynb trên Colab "
              "rồi chép file này về thư mục outputs/. Bảng tổng hợp sẽ THIẾU 3 dòng DeBERTa.")
        return []

    df_saved = pd.read_csv(saved_csv).set_index('Hệ thống')
    results = []
    for name, kind in DEBERTA_SYSTEMS:
        if name not in df_saved.index:
            print(f"-> Thiếu dòng '{name}' trong {saved_csv} — bỏ qua.")
            continue
        row = df_saved.loc[name]
        res = {
            'Hệ thống': name,
            'Kiểu mô hình & Đầu vào': kind,
            'Macro-F1': float(row['Macro-F1']),
            'Accuracy (%)': float(row['Accuracy (%)']),
            'F1 Ineffective': float(row['F1 Ineffective']),
            'F1 Adequate': float(row['F1 Adequate']),
            'F1 Effective': float(row['F1 Effective'])
        }
        print(f"-> {name}: Macro-F1 = {res['Macro-F1']:.4f} | Accuracy = {res['Accuracy (%)']:.2f}% | Ineff F1 = {res['F1 Ineffective']:.4f}")
        results.append(res)

    boot_csv = os.path.join(output_dir, 'official_test_deberta_bootstrap.csv')
    if os.path.exists(boot_csv):
        print("\n-> Bootstrap theo bài trên test (chênh Macro-F1, khoảng tin cậy 95%):")
        print(pd.read_csv(boot_csv).to_string(index=False))
    return results


# ======================================================================================
# [TỔNG HỢP]: XUẤT BẢNG NGHIỆM THU TEST TOÀN DIỆN
# ======================================================================================
def generate_master_test_table(results_list, output_dir='outputs'):
    df_summary = pd.DataFrame(results_list)
    print("\n" + "="*95)
    print("BẢNG TỔNG HỢP NGHIỆM THU CHÍNH THỨC TRÊN TẬP OFFICIAL TEST (ĐẦY ĐỦ CÁC HỆ THỐNG ĐỐI SÁNH)")
    print("="*95)
    print(df_summary.to_string(index=False))

    os.makedirs(output_dir, exist_ok=True)
    out_csv = os.path.join(output_dir, 'official_test_final_summary.csv')
    df_summary.to_csv(out_csv, index=False)
    print(f"\n-> Đã lưu bảng tổng hợp nghiệm thu vào: {out_csv}")


def main():
    parser = argparse.ArgumentParser(description="Master script đánh giá nghiệm thu tập Official Test")
    parser.add_argument('--train_csv', type=str, default='persuade_corpus_2.0_train.csv')
    parser.add_argument('--test_csv', type=str, default='persuade_corpus_2.0_test.csv')
    parser.add_argument('--output_dir', type=str, default='outputs')
    parser.add_argument('--dry_run_rows', type=int, default=None)
    args = parser.parse_args()

    # Chỉ đọc CSV train/test khi phải tự chạy lại SVM/RF (thiếu file kết quả của Người 1 & 2)
    need_data = not all(os.path.exists(os.path.join(args.output_dir, f)) for f in
                        ('official_test_svm_actual_result.csv', 'official_test_rf_actual_result.csv'))
    df_train, df_test = (load_clean_data(args.train_csv, args.test_csv, nrows=args.dry_run_rows)
                         if need_data else (None, None))

    # Tổng hợp cả 5 hệ thống
    res1 = evaluate_linear_svm_on_test(df_train, df_test, args.output_dir)
    res2 = evaluate_random_forest_on_test(df_train, df_test, args.output_dir)
    res_deberta = load_deberta_test_results(args.output_dir)

    generate_master_test_table([res1, res2, *res_deberta], args.output_dir)

if __name__ == '__main__':
    main()
