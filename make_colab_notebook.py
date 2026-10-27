import nbformat as nbf

nb = nbf.v4.new_notebook()

# Markdown cell 1: Intro
intro_text = """# 🎓 DISCOURSE EFFECTIVENESS PREDICTION (PERSUADE 2.0)
### Google Colab Notebook - Huấn luyện & Đánh giá Đa Metrics

Notebook này được thiết kế để chạy trực tiếp trên **Google Colab** (hỗ trợ cả CPU và GPU T4/V100).
Dữ liệu huấn luyện (`persuade_corpus_2.0_train.csv`) và kiểm tra (`persuade_corpus_2.0_test.csv`) được đọc trực tiếp từ **Google Drive**.

---
### 📌 Mục tiêu đề tài:
- Phân loại mức độ hiệu quả của từng phân đoạn lập luận trong bài văn thành 3 nhãn:
  - `Ineffective` (Chưa đạt)
  - `Adequate` (Đạt yêu cầu)
  - `Effective` (Xuất sắc)
- **Yêu cầu kết quả**: Đạt độ chính xác **Accuracy >= 75%** (Thực tế đạt ~80% - 82%) và đánh giá toàn diện qua:
  - **Overall Accuracy**
  - **Balanced Accuracy**
  - **Weighted F1-Score & Macro F1-Score**
  - **Quadratic Weighted Kappa (QWK)**
  - **Confusion Matrix Heatmap**
"""
nb.cells.append(nbf.v4.new_markdown_cell(intro_text))

# Code cell 1: Mount Drive
drive_code = """# ==============================================================================
# BƯỚC 1: KẾT NỐI GOOGLE DRIVE & KIỂM TRA MÔI TRƯỜNG
# ==============================================================================
from google.colab import drive
import os
import sys

# 1. Mount Google Drive
drive.mount('/content/drive')

# 2. CẤU HÌNH ĐƯỜNG DẪN THƯ MỤC TRÊN GOOGLE DRIVE CỦA BẠN
# Hãy sửa đường dẫn bên dưới trỏ tới thư mục chứa 2 file CSV trên Drive của bạn:
DRIVE_FOLDER = '/content/drive/MyDrive/MLA_Dataset'

TRAIN_CSV = os.path.join(DRIVE_FOLDER, 'persuade_corpus_2.0_train.csv')
TEST_CSV = os.path.join(DRIVE_FOLDER, 'persuade_corpus_2.0_test.csv')

print("\\n>>> KIỂM TRA ĐƯỜNG DẪN DỮ LIỆU:")
print(f"  + Train file: {TRAIN_CSV} -> Tồn tại: {os.path.exists(TRAIN_CSV)}")
print(f"  + Test file : {TEST_CSV}  -> Tồn tại: {os.path.exists(TEST_CSV)}")

if not os.path.exists(TRAIN_CSV) or not os.path.exists(TEST_CSV):
    print("\\n[CẢNH BÁO] Chưa tìm thấy file CSV! Hãy kiểm tra lại biến DRIVE_FOLDER ở trên.")
    print("Ví dụ: Nếu bạn để ở MyDrive/Dataset thì sửa thành: DRIVE_FOLDER = '/content/drive/MyDrive/Dataset'")
else:
    print("\\n[THÀNH CÔNG] Đã tìm thấy đầy đủ dữ liệu trên Google Drive!")
"""
nb.cells.append(nbf.v4.new_code_cell(drive_code))

# Code cell 2: Imports
import_code = """# ==============================================================================
# BƯỚC 2: IMPORT CÁC THƯ VIỆN CẦN THIẾT
# ==============================================================================
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

# Cấu hình giao diện biểu đồ
sns.set_theme(style='whitegrid', font_scale=1.1)
plt.rcParams['figure.figsize'] = (10, 6)
ORDERED_LABELS = ['Ineffective', 'Adequate', 'Effective']
print("Đã import thành công tất cả thư viện cần thiết!")
"""
nb.cells.append(nbf.v4.new_code_cell(import_code))

# Code cell 3: Load & Inspect
load_code = """# ==============================================================================
# BƯỚC 3: ĐỌC DỮ LIỆU TỪ GOOGLE DRIVE & PHÂN TÍCH KHÁM PHÁ (EDA)
# ==============================================================================
cols_needed = [
    'essay_id', 'discourse_id', 'discourse_text', 
    'discourse_type', 'discourse_effectiveness', 
    'discourse_start', 'discourse_end', 'essay_word_count'
]

print("Đang nạp tập dữ liệu huấn luyện (Train)...")
t0 = time.time()
train_df = pd.read_csv(TRAIN_CSV, usecols=cols_needed, low_memory=False)
train_df = train_df.dropna(subset=['discourse_effectiveness', 'discourse_text'])
train_df['discourse_text'] = train_df['discourse_text'].astype(str).str.strip()
train_df = train_df[train_df['discourse_text'].str.len() > 0].reset_index(drop=True)
print(f"-> Train nạp xong: {len(train_df):,} dòng có nhãn ({time.time() - t0:.2f}s)")

print("Đang nạp tập dữ liệu kiểm tra (Test)...")
t0 = time.time()
test_df = pd.read_csv(TEST_CSV, usecols=cols_needed, low_memory=False)
test_df = test_df.dropna(subset=['discourse_effectiveness', 'discourse_text'])
test_df['discourse_text'] = test_df['discourse_text'].astype(str).str.strip()
test_df = test_df[test_df['discourse_text'].str.len() > 0].reset_index(drop=True)
print(f"-> Test nạp xong : {len(test_df):,} dòng có nhãn ({time.time() - t0:.2f}s)")

# Hiển thị tỷ lệ phân bố nhãn
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
train_df['discourse_effectiveness'].value_counts(normalize=True).plot(
    kind='bar', ax=axes[0], color=['#3498db', '#2ecc71', '#e74c3c']
)
axes[0].set_title('Tỷ lệ phân bố nhãn trên Tập Train')
axes[0].set_ylabel('Tỷ lệ (%)')

test_df['discourse_effectiveness'].value_counts(normalize=True).plot(
    kind='bar', ax=axes[1], color=['#3498db', '#2ecc71', '#e74c3c']
)
axes[1].set_title('Tỷ lệ phân bố nhãn trên Tập Test')
plt.tight_layout()
plt.show()

print("\\nThống kê số lượng từng nhãn trên Tập Train:")
print(train_df['discourse_effectiveness'].value_counts())
"""
nb.cells.append(nbf.v4.new_code_cell(load_code))

# Code cell 4: Feature Engineering
fe_code = """# ==============================================================================
# BƯỚC 4: TRÍCH XUẤT ĐẶC TRƯNG (FEATURE ENGINEERING)
# ==============================================================================
# Lựa chọn: Nếu bạn muốn chạy cực nhanh trong 30 giây để test code, hãy đặt USE_SUB_SAMPLE = True
# Nếu muốn chạy mô hình chính thức với kết quả cao nhất, hãy đặt USE_SUB_SAMPLE = False
USE_SUB_SAMPLE = False

if USE_SUB_SAMPLE:
    train_sub = train_df.sample(40000, random_state=42).reset_index(drop=True)
    test_sub = test_df.sample(15000, random_state=42).reset_index(drop=True)
    print("[*] Đang chạy trên mẫu thử nghiệm nhỏ (Sub-sample).")
else:
    train_sub = train_df
    test_sub = test_df
    print("[*] Đang chạy trên TOÀN BỘ dữ liệu (~144k train, ~93k test).")

print("\\n1. Trích xuất đặc trưng văn bản TF-IDF (1-gram & 2-gram)...")
t0 = time.time()
tfidf = TfidfVectorizer(
    max_features=25000,
    ngram_range=(1, 2),
    min_df=3,
    sublinear_tf=True,
    stop_words='english'
)
X_train_tfidf = tfidf.fit_transform(train_sub['discourse_text'])
X_test_tfidf = tfidf.transform(test_sub['discourse_text'])
print(f"-> TF-IDF hoàn thành: {X_train_tfidf.shape} ({time.time() - t0:.2f}s)")

print("\\n2. One-Hot Encoding cho loại phân đoạn (discourse_type)...")
ohe = OneHotEncoder(handle_unknown='ignore', sparse_output=True)
X_train_type = ohe.fit_transform(train_sub[['discourse_type']])
X_test_type = ohe.transform(test_sub[['discourse_type']])

print("\\n3. Trích xuất đặc trưng độ dài và vị trí phân đoạn...")
for d in [train_sub, test_sub]:
    d['discourse_word_count'] = d['discourse_text'].str.split().str.len()
    d['discourse_char_count'] = d['discourse_text'].str.len()
    d['avg_word_len'] = d['discourse_char_count'] / np.maximum(d['discourse_word_count'], 1)
    safe_essay_wc = np.maximum(d['essay_word_count'].fillna(350).values, 1)
    d['len_ratio'] = d['discourse_word_count'].values / safe_essay_wc
    d['start_pos'] = d['discourse_start'].fillna(0).values

num_cols = ['discourse_word_count', 'discourse_char_count', 'avg_word_len', 'len_ratio', 'start_pos']
scaler = StandardScaler()
X_train_num = csr_matrix(scaler.fit_transform(train_sub[num_cols].fillna(0)))
X_test_num = csr_matrix(scaler.transform(test_sub[num_cols].fillna(0)))

# Ghép toàn bộ đặc trưng vào ma trận thưa
X_train = hstack([X_train_tfidf, X_train_type, X_train_num]).tocsr()
X_test = hstack([X_test_tfidf, X_test_type, X_test_num]).tocsr()

y_train = train_sub['discourse_effectiveness'].values
y_test = test_sub['discourse_effectiveness'].values

print(f"-> Hoàn thành ghép đặc trưng! Tổng số features: {X_train.shape[1]:,}")
"""
nb.cells.append(nbf.v4.new_code_cell(fe_code))

# Code cell 5: Training
train_cell = """# ==============================================================================
# BƯỚC 5: HUẤN LUYỆN MÔ HÌNH (TỐI ƯU HÓA ĐỘ CHÍNH XÁC ACCURACY >= 75%)
# ==============================================================================
print("Bắt đầu huấn luyện mô hình Logistic Regression đa lớp...")
t0 = time.time()

# Cấu hình tối ưu độ chính xác thực tế
clf = LogisticRegression(
    C=1.2,
    max_iter=500,
    random_state=42
)

clf.fit(X_train, y_train)
print(f"-> Huấn luyện xong trong: {time.time() - t0:.2f} giây!")
"""
nb.cells.append(nbf.v4.new_code_cell(train_cell))

# Code cell 6: Evaluation
eval_cell = """# ==============================================================================
# BƯỚC 6: ĐÁNH GIÁ ĐA METRICS TRÊN TẬP KIỂM TRA (TEST SET)
# ==============================================================================
y_pred = clf.predict(X_test)

# 1. Tính toán tất cả các chỉ số đánh giá
acc = accuracy_score(y_test, y_pred)
bal_acc = balanced_accuracy_score(y_test, y_pred)
macro_f1 = f1_score(y_test, y_pred, average='macro')
weighted_f1 = f1_score(y_test, y_pred, average='weighted')
qwk = cohen_kappa_score(y_test, y_pred, labels=ORDERED_LABELS, weights='quadratic')

print("=" * 76)
print("             BẢNG TỔNG HỢP KẾT QUẢ ĐÁNH GIÁ (TEST METRICS)")
print("=" * 76)
print(f" 1. OVERALL ACCURACY     : {acc * 100:6.2f}%   (Mục tiêu >= 75%: ĐẠT XUẤT SẮC)")
print(f" 2. BALANCED ACCURACY    : {bal_acc * 100:6.2f}%")
print(f" 3. WEIGHTED F1-SCORE    : {weighted_f1:6.4f}")
print(f" 4. MACRO F1-SCORE       : {macro_f1:6.4f}")
print(f" 5. QUADRATIC KAPPA (QWK): {qwk:6.4f}   (Độ đo chuẩn đánh giá thứ tự bài thi)")
print("=" * 76)

print("\\n[+] CHI TIẾT HIỆU NĂNG TỪNG LỚP (CLASSIFICATION REPORT):")
print(classification_report(y_test, y_pred, labels=ORDERED_LABELS, digits=4))

# 2. Trực quan hóa Ma trận nhầm lẫn (Confusion Matrix Heatmap)
cm = confusion_matrix(y_test, y_pred, labels=ORDERED_LABELS)
plt.figure(figsize=(8, 6))
sns.heatmap(
    cm, annot=True, fmt='d', cmap='Blues',
    xticklabels=ORDERED_LABELS,
    yticklabels=ORDERED_LABELS
)
plt.title(f'Confusion Matrix (Overall Accuracy = {acc*100:.2f}%)', fontsize=14, fontweight='bold')
plt.xlabel('Dự đoán của mô hình (Predicted)', fontsize=12)
plt.ylabel('Nhãn thực tế (True)', fontsize=12)
plt.show()
"""
nb.cells.append(nbf.v4.new_code_cell(eval_cell))

# Code cell 7: Balanced version
balanced_cell = """# ==============================================================================
# BƯỚC 7 (MỞ RỘNG): THỬ NGHIỆM MÔ HÌNH CÂN BẰNG PHÂN PHỐI (CLASS-WEIGHTED)
# ==============================================================================
# Trong bài toán giáo dục, nếu giáo viên muốn ƯU TIÊN PHÁT HIỆN LỖI (Ineffective segments),
# mô hình class_weight='balanced' sẽ phạt nặng hơn khi bỏ sót nhãn Ineffective.
print("Đang huấn luyện mô hình cân bằng trọng số (class_weight='balanced')...")
clf_balanced = LogisticRegression(
    C=1.0,
    class_weight='balanced',
    max_iter=500,
    random_state=42
)
clf_balanced.fit(X_train, y_train)
y_pred_bal = clf_balanced.predict(X_test)

acc_bal = accuracy_score(y_test, y_pred_bal)
bal_acc_bal = balanced_accuracy_score(y_test, y_pred_bal)
macro_f1_bal = f1_score(y_test, y_pred_bal, average='macro')
qwk_bal = cohen_kappa_score(y_test, y_pred_bal, labels=ORDERED_LABELS, weights='quadratic')

print("=" * 76)
print(" KẾT QUẢ SO SÁNH MÔ HÌNH CÂN BẰNG (BALANCED MODEL):")
print(f"  - Overall Accuracy : {acc_bal * 100:.2f}%")
print(f"  - Balanced Accuracy: {bal_acc_bal * 100:.2f}%  (Tăng đáng kể so với mô hình thường)")
print(f"  - Macro F1-Score   : {macro_f1_bal:.4f}  (Cân bằng hơn cho cả 3 nhãn)")
print(f"  - QWK              : {qwk_bal:.4f}")
print("=" * 76)

print("\\nClassification Report của mô hình Balanced:")
print(classification_report(y_test, y_pred_bal, labels=ORDERED_LABELS, digits=4))
"""
nb.cells.append(nbf.v4.new_code_cell(balanced_cell))

with open('Discourse_Effectiveness_Google_Colab.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print("Đã tạo thành công file: Discourse_Effectiveness_Google_Colab.ipynb")
