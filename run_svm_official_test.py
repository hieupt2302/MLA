"""
RUN LINEAR SVM ON OFFICIAL TEST SET (93,677 SAMPLES)
Họ mô hình cơ sở đối chứng cùng họ tuyến tính / phân loại lề (Course Model Family Baseline)
"""
import time
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import f1_score, accuracy_score, classification_report

LABEL_MAP = {'Ineffective': 0, 'Adequate': 1, 'Effective': 2}
INV_LABEL_MAP = {0: 'Ineffective', 1: 'Adequate', 2: 'Effective'}

start_time = time.time()
print("1. Đang nạp dữ liệu train và test...")
df_train = pd.read_csv('persuade_corpus_2.0_train.csv', 
                       dtype={'essay_id': str, 'discourse_id': str},
                       usecols=['essay_id', 'discourse_id', 'discourse_text', 'discourse_type', 'discourse_effectiveness'])
df_train = df_train.dropna(subset=['discourse_effectiveness', 'discourse_text'])

df_test = pd.read_csv('persuade_corpus_2.0_test.csv',
                      dtype={'essay_id': str, 'discourse_id': str},
                      usecols=['essay_id', 'discourse_id', 'discourse_text', 'discourse_type', 'discourse_effectiveness'])
df_test = df_test.dropna(subset=['discourse_effectiveness', 'discourse_text'])

print(f"Train samples: {len(df_train):,} | Test samples: {len(df_test):,}")

print("\n2. Trích xuất đặc trưng TF-IDF (15,000 features, unigram + bigram)...")
tfidf = TfidfVectorizer(max_features=15000, ngram_range=(1, 2), min_df=3, sublinear_tf=True)
X_train = tfidf.fit_transform(df_train['discourse_text'])
X_test = tfidf.transform(df_test['discourse_text'])

y_train = df_train['discourse_effectiveness'].map(LABEL_MAP).values
y_test = df_test['discourse_effectiveness'].map(LABEL_MAP).values

print("\n3. Huấn luyện Linear SVM (balanced class weight)...")
clf = LinearSVC(C=1.0, class_weight='balanced', random_state=42, max_iter=2000)
clf.fit(X_train, y_train)

print("\n4. Dự đoán trên tập Test (93,677 mẫu)...")
y_pred = clf.predict(X_test)

macro_f1 = f1_score(y_test, y_pred, labels=[0, 1, 2], average='macro')
acc = accuracy_score(y_test, y_pred)
f1_per_class = f1_score(y_test, y_pred, labels=[0, 1, 2], average=None)

elapsed = time.time() - start_time
print("\n" + "="*70)
print(f"KẾT QUẢ THỰC TẾ CỦA LINEAR SVM TRÊN OFFICIAL TEST (Hoàn thành trong {elapsed:.1f}s):")
print("="*70)
print(f"Macro-F1:            {macro_f1:.4f}")
print(f"Accuracy:            {acc*100:.2f}%")
print(f"F1 Ineffective:      {f1_per_class[0]:.4f}")
print(f"F1 Adequate:         {f1_per_class[1]:.4f}")
print(f"F1 Effective:        {f1_per_class[2]:.4f}")

os.makedirs('outputs', exist_ok=True)
df_res = pd.DataFrame([{
    'Hệ thống': 'Linear SVM (TF-IDF Baseline)',
    'Macro-F1': round(macro_f1, 4),
    'Accuracy (%)': round(acc * 100, 2),
    'F1 Ineffective': round(f1_per_class[0], 4),
    'F1 Adequate': round(f1_per_class[1], 4),
    'F1 Effective': round(f1_per_class[2], 4),
    'Runtime (s)': round(elapsed, 1)
}])
df_res.to_csv('outputs/official_test_svm_actual_result.csv', index=False)
print("Đã lưu kết quả thực tế vào: outputs/official_test_svm_actual_result.csv")
