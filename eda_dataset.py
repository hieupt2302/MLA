"""
EDA_DATASET.PY
Script phân tích và khám phá tập dữ liệu PERSUADE 2.0 (Discourse Effectiveness Prediction).
Chạy lệnh: python eda_dataset.py
"""

import os
import sys

# Thiết lập UTF-8 cho console Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

import pandas as pd
import numpy as np

TRAIN_PATH = "persuade_corpus_2.0_train.csv"
TEST_PATH = "persuade_corpus_2.0_test.csv"

def inspect_dataset():
    print("=" * 80)
    print(" BẮT ĐẦU PHÂN TÍCH TẬP DỮ LIỆU PERSUADE CORPUS 2.0")
    print(" Đề tài: Discourse Effectiveness Prediction")
    print("=" * 80)

    for name, path in [("TẬP HUẤN LUYỆN (TRAIN)", TRAIN_PATH), ("TẬP KIỂM TRA (TEST)", TEST_PATH)]:
        if not os.path.exists(path):
            print(f"[CẢNH BÁO] Không tìm thấy file: {path}")
            continue

        print(f"\n>>> Đang đọc thông tin từ {name} ({path})...")
        cols_to_read = [
            'essay_id', 'discourse_id', 'discourse_type', 
            'discourse_effectiveness', 'discourse_text', 'essay_word_count'
        ]
        
        df = pd.read_csv(path, usecols=cols_to_read)
        total_rows = len(df)
        unique_essays = df['essay_id'].nunique()
        labeled_df = df.dropna(subset=['discourse_effectiveness'])
        labeled_rows = len(labeled_df)
        unlabeled_rows = total_rows - labeled_rows

        print(f"  + Tổng số phân đoạn (discourse units): {total_rows:,}")
        print(f"  + Tổng số bài văn (unique essays): {unique_essays:,}")
        print(f"  + Số phân đoạn CÓ NHÃN: {labeled_rows:,} ({labeled_rows/total_rows*100:.2f}%)")
        print(f"  + Số phân đoạn KHÔNG CÓ NHÃN (NaN): {unlabeled_rows:,} ({unlabeled_rows/total_rows*100:.2f}%)")

        print("\n  [+] Phân bố các nhãn hiệu quả (discourse_effectiveness):")
        counts = labeled_df['discourse_effectiveness'].value_counts()
        percents = labeled_df['discourse_effectiveness'].value_counts(normalize=True) * 100
        for label in counts.index:
            print(f"      - {label:<12}: {counts[label]:>8,} dòng ({percents[label]:>5.2f}%)")

        print("\n  [+] Phân bố các thể loại lập luận (discourse_type):")
        type_counts = labeled_df['discourse_type'].value_counts()
        for dtype, count in type_counts.items():
            print(f"      - {dtype:<22}: {count:>8,} dòng ({count/labeled_rows*100:>5.2f}%)")

        print("\n  [+] Mẫu dữ liệu thực tế:")
        sample = labeled_df[['discourse_type', 'discourse_effectiveness', 'discourse_text']].head(2)
        for idx, row in sample.iterrows():
            clean_text = str(row['discourse_text']).strip()[:100].replace('\n', ' ')
            print(f"      * [{row['discourse_type']}] -> Nhãn: {row['discourse_effectiveness']}")
            print(f"        Văn bản: \"{clean_text}...\"")

    print("\n" + "=" * 80)
    print(" KẾT LUẬN & NHẬN XÉT QUAN TRỌNG VỀ ĐỘ ĐO ACCURACY:")
    print(" 1. Nhãn 'Adequate' chiếm áp đảo (~78.5% tập Train và ~80.4% tập Test).")
    print(" 2. Nhãn 'Effective' chiếm ~15-17%, và 'Ineffective' chỉ chiếm ~4.5%.")
    print(" 3. Một mô hình chuẩn học trích xuất đặc trưng có thể dễ dàng đạt Accuracy >= 75% - 81%.")
    print(" 4. Để giải quyết toàn diện đề tài, ta cần quan tâm thêm Weighted F1, Macro F1,")
    print("    và Quadratic Weighted Kappa (QWK) bên cạnh Accuracy.")
    print("=" * 80)

if __name__ == "__main__":
    inspect_dataset()
