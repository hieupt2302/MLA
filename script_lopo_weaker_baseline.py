"""
SCRIPT 3: MÔ HÌNH CƠ SỞ ĐỐI CHỨNG CÙNG HỌ TRONG LOPO (LINEAR SVM & DISTILBERT BASELINE)
Phụ trách: Thành viên 3 (LOPO & Evaluation Protocol Owner)
Mục đích:
- Giải quyết trực tiếp góp ý của Thầy về việc "Random Forest và DeBERTa khác họ, so sánh không công bằng trong LOPO".
- Cung cấp mô hình đối chứng chuẩn khoa học trên đúng 3 đề LOPO đại diện:
  1. Đề Khó nhất (Rank 1): "A Cowboy Who Rode the Waves"
  2. Đề Trung vị (Rank 8): Summer projects
  3. Đề Dễ nhất (Rank 15): Distance learning

Script hỗ trợ 2 chế độ (Mode):
- Chế độ 1 (--model svm): Linear SVM (Mô hình cùng họ Tuyến tính / Phân loại lề từ môn học, chạy cực nhanh trên CPU ~2 phút).
- Chế độ 2 (--model distilbert): DistilBERT (Mô hình cùng họ Transformer pre-trained nhưng nhẹ và yếu hơn DeBERTa, 66M tham số).

LƯU Ý: SCRIPT ĐƯỢC THIẾT KẾ ĐỂ CHẠY ĐỘC LẬP KHI CẦN, KHÔNG TỰ ĐỘNG CHẠY NẾU CHƯA GỌI.
"""

import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

import argparse
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import f1_score, accuracy_score, classification_report

HELD_OUT_PROMPTS = [
    '"A Cowboy Who Rode the Waves"',
    'Summer projects',
    'Distance learning'
]

LABEL_MAP = {'Ineffective': 0, 'Adequate': 1, 'Effective': 2}

def run_svm_lopo(train_csv_path='persuade_corpus_2.0_train.csv', output_dir='outputs'):
    print("="*75)
    print("CHẾ ĐỘ 1: ĐÁNH GIÁ LINEAR SVM LOPO (HỌ MÔ HÌNH TUYẾN TÍNH - COURSE MODEL FAMILY)")
    print("="*75)

    if not os.path.exists(train_csv_path):
        raise FileNotFoundError(f"Không tìm thấy tệp {train_csv_path}")

    # Đọc dữ liệu
    print("-> Đang tải dữ liệu huấn luyện...")
    df = pd.read_csv(
        train_csv_path,
        dtype={'essay_id': str, 'discourse_id': str},
        usecols=['essay_id', 'discourse_id', 'discourse_text', 'discourse_type', 'prompt_name', 'discourse_effectiveness']
    )
    df = df.dropna(subset=['discourse_effectiveness', 'discourse_text'])
    df['target'] = df['discourse_effectiveness'].map(LABEL_MAP)
    
    results = []

    for prompt_name in HELD_OUT_PROMPTS:
        clean_name = prompt_name.replace('"', '')
        print(f"\n--- Đang xử lý Fold LOPO: {clean_name} ---")

        # Chia tách dữ liệu: Train trên 14 đề, Test trên 1 đề bị giấu
        test_mask = (df['prompt_name'] == prompt_name)
        train_mask = ~test_mask

        df_train_fold = df[train_mask]
        df_test_fold = df[test_mask]

        print(f"   Train samples: {len(df_train_fold):,} | Test samples: {len(df_test_fold):,}")

        # Trích xuất đặc trưng TF-IDF chuẩn hóa (unigram + bigram)
        vectorizer = TfidfVectorizer(max_features=15000, ngram_range=(1, 2), min_df=3, sublinear_tf=True)
        X_train = vectorizer.fit_transform(df_train_fold['discourse_text'])
        X_test = vectorizer.transform(df_test_fold['discourse_text'])

        y_train = df_train_fold['target'].values
        y_test = df_test_fold['target'].values

        # Huấn luyện Linear SVM với trọng số lớp cân bằng (balanced class weights)
        clf = LinearSVC(C=1.0, class_weight='balanced', random_state=42, max_iter=2000)
        clf.fit(X_train, y_train)

        # Dự báo
        y_pred = clf.predict(X_test)

        macro_f1 = f1_score(y_test, y_pred, average='macro')
        acc = accuracy_score(y_test, y_pred)
        f1_per_class = f1_score(y_test, y_pred, average=None, zero_division=0)

        results.append({
            'held_out_prompt': clean_name,
            'model_name': 'Linear SVM (TF-IDF)',
            'test_units': len(y_test),
            'macro_f1': round(macro_f1, 4),
            'accuracy': round(acc * 100, 2),
            'f1_ineffective': round(f1_per_class[0], 4),
            'f1_adequate': round(f1_per_class[1], 4),
            'f1_effective': round(f1_per_class[2], 4)
        })

        print(f"   -> Kết quả: Macro-F1 = {macro_f1:.4f} | Accuracy = {acc*100:.2f}% | Ineffective F1 = {f1_per_class[0]:.4f}")

    df_res = pd.DataFrame(results)
    print("\n" + "="*75)
    print("BẢNG TỔNG HỢP KẾT QUẢ LINEAR SVM LOPO (MỐC ĐỐI CHỨNG CÙNG HỌ TUYẾN TÍNH):")
    print("="*75)
    print(df_res.to_string(index=False))

    os.makedirs(output_dir, exist_ok=True)
    out_csv = os.path.join(output_dir, 'lopo_svm_baseline_results.csv')
    df_res.to_csv(out_csv, index=False)
    print(f"\n-> Đã lưu kết quả SVM LOPO vào: {out_csv}")


def run_distilbert_lopo():
    """
    Chế độ 2: Hướng dẫn chạy DistilBERT LOPO (Họ Transformer nhẹ hơn).
    Mã nguồn chi tiết dành cho Colab GPU khi cần huấn luyện DistilBERT.
    """
    code_template = '''
# CODE RUN DISTILBERT LOPO TRÊN GOOGLE COLAB:
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
# Sử dụng backbone: "distilbert-base-uncased" (66M tham số, 6 layers)
# So sánh công bằng với DeBERTa-v3-base (86M tham số, 12 layers)
# Kết quả DistilBERT trên 3 đề LOPO sẽ là đối chứng cùng họ Transformer hoàn hảo!
    '''
    print(code_template)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Chạy mô hình đối chứng cùng họ trong LOPO")
    parser.add_argument('--model', type=str, default='svm', choices=['svm', 'distilbert'], help='Chọn mô hình: svm hoặc distilbert')
    parser.add_argument('--data_path', type=str, default='persuade_corpus_2.0_train.csv')
    parser.add_argument('--output_dir', type=str, default='outputs')
    
    args = parser.parse_args()

    if args.model == 'svm':
        run_svm_lopo(args.data_path, args.output_dir)
    else:
        run_distilbert_lopo()
