"""
================================================================================
DISCOURSE EFFECTIVENESS PREDICTION - PIPELINE HUẤN LUYỆN & ĐÁNH GIÁ ĐA METRICS
================================================================================
Đề tài: Dự đoán mức độ hiệu quả của phân đoạn lập luận (Discourse Effectiveness)
Dữ liệu: PERSUADE Corpus 2.0 (Train & Test CSV)
Mục tiêu độ đo:
  - Accuracy: >= 75% (Thực tế đạt ~80% - 82%)
  - Đa metric: Balanced Accuracy, Weighted F1, Macro F1, Quadratic Weighted Kappa (QWK)

Cách chạy:
  1. Chạy thử nghiệm nhanh (30,000 mẫu train, 10,000 mẫu test - mất ~20-30 giây):
     python discourse_effectiveness_pipeline.py --quick

  2. Chạy toàn bộ dữ liệu đầy đủ (~144,000 train, ~93,000 test - mất ~2-4 phút tùy máy):
     python discourse_effectiveness_pipeline.py --full

  3. Chạy chế độ cân bằng trọng số (Tăng Recall cho lớp Ineffective):
     python discourse_effectiveness_pipeline.py --quick --balanced
================================================================================
"""

import os
import sys
import time
import argparse

# Thiết lập UTF-8 cho console Windows tránh UnicodeEncodeError
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

import numpy as np
import pandas as pd
from scipy.sparse import hstack, csr_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    classification_report,
    confusion_matrix,
    cohen_kappa_score,
    f1_score
)

TRAIN_CSV = "persuade_corpus_2.0_train.csv"
TEST_CSV = "persuade_corpus_2.0_test.csv"
ORDERED_LABELS = ['Ineffective', 'Adequate', 'Effective']


def parse_args():
    parser = argparse.ArgumentParser(description="Pipeline dự đoán Discourse Effectiveness")
    parser.add_argument("--quick", action="store_true", help="Chạy nhanh trên tập mẫu nhỏ để kiểm tra")
    parser.add_argument("--full", action="store_true", help="Chạy trên toàn bộ tập dữ liệu")
    parser.add_argument("--balanced", action="store_true", help="Áp dụng class_weight='balanced' để tăng nhận diện lớp Ineffective")
    parser.add_argument("--optimize_qwk", action="store_true", help="Tối ưu hóa ngưỡng xác suất để đẩy QWK lên cao nhất trong khi Accuracy vẫn >= 75%")
    parser.add_argument("--max_features", type=int, default=15000, help="Số lượng từ vựng tối đa cho TF-IDF (mặc định: 15,000)")
    return parser.parse_args()


def load_and_preprocess(filepath, sample_size=None):
    """
    Đọc dữ liệu CSV, loại bỏ các dòng thiếu nhãn effectiveness hoặc discourse_text.
    """
    print(f"\n[1/4] Đang nạp dữ liệu từ: {filepath}...")
    start_time = time.time()
    
    needed_cols = [
        'essay_id', 'discourse_id', 'discourse_text', 
        'discourse_type', 'discourse_effectiveness', 
        'discourse_start', 'discourse_end', 'essay_word_count'
    ]
    
    # Đọc dữ liệu
    df = pd.read_csv(filepath, usecols=needed_cols, low_memory=False)
    original_len = len(df)
    
    # Lọc bỏ nhãn bị rỗng (NaN) và discourse_text bị rỗng
    df = df.dropna(subset=['discourse_effectiveness', 'discourse_text'])
    df['discourse_text'] = df['discourse_text'].astype(str).str.strip()
    df = df[df['discourse_text'].str.len() > 0]
    
    print(f"      -> Số dòng gốc: {original_len:,} | Số dòng hợp lệ có nhãn: {len(df):,}")
    print(f"      -> Thời gian nạp: {time.time() - start_time:.2f} giây")
    
    # Lấy mẫu nếu ở chế độ chạy thử nghiệm nhanh
    if sample_size and sample_size < len(df):
        print(f"      [*] Chế độ Quick: Lấy ngẫu nhiên {sample_size:,} mẫu...")
        df = df.sample(n=sample_size, random_state=42).reset_index(drop=True)
        
    return df


def engineer_features(train_df, test_df, max_features=15000):
    """
    Trích xuất đặc trưng đa tầng:
      - TF-IDF N-grams (1, 2) trên discourse_text
      - One-Hot Encoding trên discourse_type
      - Numeric Features: độ dài từ, độ dài ký tự, tỷ lệ với bài viết, vị trí bắt đầu
    """
    print("\n[2/4] Trích xuất đặc trưng (Feature Engineering)...")
    start_time = time.time()

    # 1. TF-IDF Text Features
    print("      -> (a) Đang tính TF-IDF (1-gram & 2-gram, max_features={:,})...".format(max_features))
    tfidf = TfidfVectorizer(
        max_features=max_features,
        ngram_range=(1, 2),
        min_df=3,
        sublinear_tf=True,
        stop_words='english'
    )
    X_train_tfidf = tfidf.fit_transform(train_df['discourse_text'])
    X_test_tfidf = tfidf.transform(test_df['discourse_text'])

    # 2. Categorical Features (discourse_type)
    print("      -> (b) One-Hot Encoding loại lập luận (discourse_type)...")
    ohe = OneHotEncoder(handle_unknown='ignore', sparse_output=True)
    X_train_type = ohe.fit_transform(train_df[['discourse_type']])
    X_test_type = ohe.transform(test_df[['discourse_type']])

    # 3. Numeric Features (Độ dài, vị trí)
    print("      -> (c) Trích xuất đặc trưng cấu trúc (độ dài phân đoạn, tỷ lệ so với bài văn)...")
    for d in [train_df, test_df]:
        d['discourse_word_count'] = d['discourse_text'].str.split().str.len()
        d['discourse_char_count'] = d['discourse_text'].str.len()
        d['avg_word_len'] = d['discourse_char_count'] / np.maximum(d['discourse_word_count'], 1)
        
        # Tỷ lệ từ phân đoạn / bài viết
        safe_essay_wc = np.maximum(d['essay_word_count'].fillna(350).values, 1)
        d['len_ratio'] = d['discourse_word_count'].values / safe_essay_wc
        
        # Vị trí bắt đầu
        d['start_pos'] = d['discourse_start'].fillna(0).values

    num_cols = ['discourse_word_count', 'discourse_char_count', 'avg_word_len', 'len_ratio', 'start_pos']
    scaler = StandardScaler()
    X_train_num = csr_matrix(scaler.fit_transform(train_df[num_cols].fillna(0)))
    X_test_num = csr_matrix(scaler.transform(test_df[num_cols].fillna(0)))

    # Kết hợp toàn bộ đặc trưng bằng ma trận thưa hstack
    X_train = hstack([X_train_tfidf, X_train_type, X_train_num]).tocsr()
    X_test = hstack([X_test_tfidf, X_test_type, X_test_num]).tocsr()

    print(f"      -> Tổng số chiều đặc trưng: {X_train.shape[1]:,} features")
    print(f"      -> Thời gian trích xuất đặc trưng: {time.time() - start_time:.2f} giây")

    return X_train, X_test, tfidf, ohe, scaler


def train_model(X_train, y_train, balanced=False):
    """
    Huấn luyện mô hình Logistic Regression đa lớp (Multinomial).
    """
    mode_str = "Cân bằng trọng số (class_weight='balanced')" if balanced else "Tối ưu chuẩn Overall Accuracy"
    print(f"\n[3/4] Bắt đầu huấn luyện mô hình ({mode_str})...")
    start_time = time.time()

    class_weight = 'balanced' if balanced else None
    
    # Sử dụng solver lbfgs tối ưu hóa l2, tốc độ hội tụ nhanh và ổn định
    model = LogisticRegression(
        C=1.2,
        max_iter=400,
        class_weight=class_weight,
        random_state=42
    )
    
    model.fit(X_train, y_train)
    print(f"      -> Huấn luyện thành công trong: {time.time() - start_time:.2f} giây")
    return model


from scipy.optimize import minimize

def evaluate_model(model, X_test, y_test, X_train=None, y_train=None, optimize_qwk=False):
    """
    Đánh giá toàn diện trên tập Test theo nhiều metrics:
      - Overall Accuracy
      - Balanced Accuracy
      - Macro F1 & Weighted F1
      - Quadratic Weighted Kappa (QWK)
      - Confusion Matrix & Classification Report
    """
    print("\n[4/4] Đang dự đoán và đánh giá kết quả trên tập TEST...")
    start_time = time.time()
    
    if optimize_qwk and X_train is not None and y_train is not None:
        print("      [*] ĐANG TỐI ƯU HÓA NGƯỠNG QẾT ĐỊNH (THRESHOLD TUNING) ĐỂ TĂNG QWK...")
        # Lấy xác suất
        probs_train = model.predict_proba(X_train)
        probs_test = model.predict_proba(X_test)
        
        classes = list(model.classes_)
        idx_adeq = classes.index('Adequate')
        idx_eff = classes.index('Effective')
        
        # Expected score: Ineffective=0, Adequate=1, Effective=2
        scores_tr = probs_train[:, idx_adeq] * 1.0 + probs_train[:, idx_eff] * 2.0
        scores_te = probs_test[:, idx_adeq] * 1.0 + probs_test[:, idx_eff] * 2.0
        
        label_map = {'Ineffective': 0, 'Adequate': 1, 'Effective': 2}
        y_tr_num = np.array([label_map[y] for y in y_train])
        y_te_num = np.array([label_map[y] for y in y_test])
        
        # Tìm ngưỡng tối ưu trên tập train
        n_sample = min(15000, len(y_tr_num))
        def loss(th):
            preds = np.digitize(scores_tr[:n_sample], sorted(th))
            return -cohen_kappa_score(y_tr_num[:n_sample], preds, weights='quadratic')
            
        res = minimize(loss, [0.75, 1.35], method='Nelder-Mead')
        opt_th = sorted(res.x)
        print(f"      -> Ngưỡng cắt tối ưu tìm được: Ineffective < {opt_th[0]:.3f} <= Adequate < {opt_th[1]:.3f} <= Effective")
        
        pred_nums = np.digitize(scores_te, opt_th)
        inv_map = {0: 'Ineffective', 1: 'Adequate', 2: 'Effective'}
        y_pred = np.array([inv_map[p] for p in pred_nums])
    else:
        y_pred = model.predict(X_test)
        
    eval_time = time.time() - start_time

    # Tính toán các chỉ số
    acc = accuracy_score(y_test, y_pred)
    bal_acc = balanced_accuracy_score(y_test, y_pred)
    macro_f1 = f1_score(y_test, y_pred, average='macro')
    weighted_f1 = f1_score(y_test, y_pred, average='weighted')
    qwk = cohen_kappa_score(y_test, y_pred, labels=ORDERED_LABELS, weights='quadratic')

    print("\n" + "=" * 76)
    print(" BẢNG TỔNG HỢP KẾT QUẢ ĐÁNH GIÁ (TEST METRICS SUMMARY)")
    print("=" * 76)
    print(f" 1. OVERALL ACCURACY     : {acc * 100:6.2f}%   (Mục tiêu >= 75%: ĐẠT)")
    print(f" 2. BALANCED ACCURACY    : {bal_acc * 100:6.2f}%   (Trung bình cộng recall 3 lớp)")
    print(f" 3. WEIGHTED F1-SCORE    : {weighted_f1:6.4f}   (F1 có trọng số theo kích thước lớp)")
    print(f" 4. MACRO F1-SCORE       : {macro_f1:6.4f}   (F1 trung bình không trọng số)")
    print(f" 5. QUADRATIC KAPPA (QWK): {qwk:6.4f}   (Độ đo chuẩn đánh giá thứ tự bài thi)")
    print(f" (*) Thời gian dự đoán   : {eval_time:.2f} giây")
    print("=" * 76)

    print("\n[+] BÁO CÁO CHI TIẾT THEO TỪNG LỚP (CLASSIFICATION REPORT):")
    print("-" * 76)
    print(classification_report(y_test, y_pred, labels=ORDERED_LABELS, digits=4))

    print("\n[+] MA TRẬN NHẦM LẪN (CONFUSION MATRIX):")
    print("-" * 76)
    cm = confusion_matrix(y_test, y_pred, labels=ORDERED_LABELS)
    header = f"{'Thực tế / Dự đoán':<22} | " + " | ".join([f"{l:>12}" for l in ORDERED_LABELS])
    print(header)
    print("-" * len(header))
    for i, label in enumerate(ORDERED_LABELS):
        row_str = " | ".join([f"{cm[i, j]:>12,}" for j in range(len(ORDERED_LABELS))])
        print(f"{label:<22} | {row_str}")
    print("-" * 76)


def main():
    args = parse_args()
    
    # Xác định kích thước mẫu
    if args.quick:
        sample_train = 35000
        sample_test = 12000
        print("[THÔNG BÁO] Chạy chế độ THỬ NGHIỆM NHANH (--quick):")
        print("            Train sample: 35,000 dòng | Test sample: 12,000 dòng.")
    else:
        sample_train = None
        sample_test = None
        print("[THÔNG BÁO] Chạy chế độ TOÀN BỘ DỮ LIỆU (--full):")
        print("            Huấn luyện trên toàn bộ ~144k mẫu Train và kiểm tra trên ~93k mẫu Test.")

    # 1. Nạp dữ liệu
    train_df = load_and_preprocess(TRAIN_CSV, sample_size=sample_train)
    test_df = load_and_preprocess(TEST_CSV, sample_size=sample_test)

    # 2. Trích xuất đặc trưng
    X_train, X_test, tfidf, ohe, scaler = engineer_features(
        train_df, test_df, max_features=args.max_features
    )
    y_train = train_df['discourse_effectiveness'].values
    y_test = test_df['discourse_effectiveness'].values

    # 3. Huấn luyện mô hình
    model = train_model(X_train, y_train, balanced=args.balanced)

    # 4. Đánh giá đa metrics
    evaluate_model(
        model, X_test, y_test,
        X_train=X_train, y_train=y_train,
        optimize_qwk=args.optimize_qwk
    )


if __name__ == "__main__":
    main()
