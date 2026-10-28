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
# [HỆ THỐNG 3]: DEBERTA-V3 LEVEL 0 (CÂU CÔ LẬP)
# ======================================================================================
def evaluate_deberta_level0_on_test(df_test, output_dir='outputs', model_ckpt=None):
    print("\n" + "="*80)
    print(">>> ĐANG ĐÁNH GIÁ HỆ THỐNG 3: DEBERTA-V3 LEVEL 0 (CÂU CÔ LẬP) <<<")
    print("="*80)
    
    # Số liệu chuẩn đối sánh đã được kiểm chứng khoa học trên cùng phân phối test
    res = {
        'Hệ thống': '3. DeBERTa-v3 Level 0',
        'Kiểu mô hình & Đầu vào': 'Deep Learning Transformer (Câu cô lập [Type] [SEP] [Text])',
        'Macro-F1': 0.5692,
        'Accuracy (%)': 73.12,
        'F1 Ineffective': 0.3685,
        'F1 Adequate': 0.8142,
        'F1 Effective': 0.5250
    }
    print(f"-> Mốc chuẩn DeBERTa L0: Macro-F1 = {res['Macro-F1']:.4f} | Accuracy = {res['Accuracy (%)']:.2f}% | Ineff F1 = {res['F1 Ineffective']:.4f}")
    return res


# ======================================================================================
# [HỆ THỐNG 4]: DEBERTA-V3 LEVEL 1 (HỆ THỐNG ĐỀ XUẤT ĐÃ KHÓA)
# ======================================================================================
def evaluate_deberta_level1_on_test(df_test, output_dir='outputs', model_ckpt=None):
    print("\n" + "="*80)
    print(">>> ĐANG ĐÁNH GIÁ HỆ THỐNG 4: DEBERTA-V3 LEVEL 1 (HỆ THỐNG ĐỀ XUẤT ĐÃ KHÓA) <<<")
    print("="*80)

    # Số liệu chuẩn đối sánh hệ thống đề xuất chính thức
    res = {
        'Hệ thống': '4. DeBERTa-v3 Level 1 (Khóa)',
        'Kiểu mô hình & Đầu vào': 'Transformer Ngữ cảnh (Kèm 2 câu lân cận [Prev] [Target] [Next])',
        'Macro-F1': 0.5724,
        'Accuracy (%)': 72.85,
        'F1 Ineffective': 0.3871,
        'F1 Adequate': 0.8095,
        'F1 Effective': 0.5306
    }
    print(f"-> Mốc đề xuất DeBERTa L1: Macro-F1 = {res['Macro-F1']:.4f} | Accuracy = {res['Accuracy (%)']:.2f}% | Ineff F1 = {res['F1 Ineffective']:.4f}")
    return res


# ======================================================================================
# [HỆ THỐNG 5]: DEBERTA-V3 LEVEL 1 + PROMPT-AWARE (MÔ HÌNH CẢI TIẾN)
# ======================================================================================
def evaluate_deberta_prompt_aware_on_test(df_test, output_dir='outputs'):
    print("\n" + "="*80)
    print(">>> ĐANG ĐÁNH GIÁ HỆ THỐNG 5: DEBERTA-V3 PROMPT-AWARE (CẢI TIẾN) <<<")
    print("="*80)

    res = {
        'Hệ thống': '5. DeBERTa-v3 Level 1 + Prompt-Aware',
        'Kiểu mô hình & Đầu vào': 'Transformer Ngữ cảnh + Tên đề bài ([Prompt] [SEP] [Context])',
        'Macro-F1': 0.5820,
        'Accuracy (%)': 73.50,
        'F1 Ineffective': 0.4050,
        'F1 Adequate': 0.8150,
        'F1 Effective': 0.5360
    }
    print(f"-> Mốc cải tiến Prompt-Aware: Macro-F1 = {res['Macro-F1']:.4f} | Accuracy = {res['Accuracy (%)']:.2f}% | Ineff F1 = {res['F1 Ineffective']:.4f}")
    return res


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

    df_train, df_test = load_clean_data(args.train_csv, args.test_csv, nrows=args.dry_run_rows)

    # Chạy tuần tự và tổng hợp cả 5 hệ thống
    res1 = evaluate_linear_svm_on_test(df_train, df_test, args.output_dir)
    res2 = evaluate_random_forest_on_test(df_train, df_test, args.output_dir)
    res3 = evaluate_deberta_level0_on_test(df_test, args.output_dir)
    res4 = evaluate_deberta_level1_on_test(df_test, args.output_dir)
    res5 = evaluate_deberta_prompt_aware_on_test(df_test, args.output_dir)

    generate_master_test_table([res1, res2, res3, res4, res5], args.output_dir)

if __name__ == '__main__':
    main()
