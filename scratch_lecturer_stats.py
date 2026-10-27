import os
import sys
import pandas as pd
import numpy as np

# Set stdout encoding
sys.stdout.reconfigure(encoding='utf-8')

print("Reading dataset...")
df = pd.read_csv('persuade_corpus_2.0_train.csv', usecols=['discourse_type', 'discourse_effectiveness', 'prompt_name', 'discourse_text', 'assignment', 'essay_word_count', 'ell_status'])
df_labeled = df.dropna(subset=['discourse_effectiveness']).copy()

print("="*60)
print("1. TỶ LỆ INEFFECTIVE / ADEQUATE / EFFECTIVE THEO LOẠI LUẬN ĐIỂM")
print("="*60)
ct = pd.crosstab(df_labeled['discourse_type'], df_labeled['discourse_effectiveness'], margins=True)
ct_pct = (pd.crosstab(df_labeled['discourse_type'], df_labeled['discourse_effectiveness'], normalize='index') * 100).round(2)

print("\n--- SỐ LƯỢNG (COUNTS) ---")
print(ct.to_string())

print("\n--- TỶ LỆ PHẦN TRĂM (%) ---")
print(ct_pct.to_string())

print("\n" + "="*60)
print("2. ĐỘ DÀI TRUNG BÌNH (SỐ TỪ) CỦA DISCOURSE THEO HIỆU QUẢ")
print("="*60)
df_labeled['word_count'] = df_labeled['discourse_text'].apply(lambda x: len(str(x).split()))

overall_len = df_labeled.groupby('discourse_effectiveness')['word_count'].agg(['count', 'mean', 'median', 'std', 'min', 'max']).round(2)
print("\n--- TỔNG THỂ THEO NHÃN ---")
print(overall_len.to_string())

print("\n--- CHI TIẾT THEO LOẠI LUẬN ĐIỂM VÀ NHÃN (MEAN WORDS) ---")
pivot_len = df_labeled.pivot_table(index='discourse_type', columns='discourse_effectiveness', values='word_count', aggfunc='mean').round(2)
print(pivot_len.to_string())

print("\n" + "="*60)
print("3. TỶ LỆ INEFFECTIVE THEO TỪNG ĐỀ BÀI (PROMPT_NAME)")
print("="*60)
prompt_ct = pd.crosstab(df_labeled['prompt_name'], df_labeled['discourse_effectiveness'], normalize='index') * 100
prompt_cnt = df_labeled.groupby('prompt_name')['discourse_effectiveness'].count()
prompt_summary = pd.DataFrame({
    'Total_Discourses': prompt_cnt,
    'Ineffective_%': prompt_ct['Ineffective'].round(2),
    'Adequate_%': prompt_ct['Adequate'].round(2),
    'Effective_%': prompt_ct['Effective'].round(2)
}).sort_values('Ineffective_%', ascending=False)
print(prompt_summary.to_string())

print("\n" + "="*60)
print("4. TỶ LỆ INEFFECTIVE THEO HỌC SINH ELL (ENGLISH LANGUAGE LEARNER)")
print("="*60)
ell_ct = pd.crosstab(df_labeled['ell_status'], df_labeled['discourse_effectiveness'], normalize='index') * 100
ell_cnt = df_labeled.groupby('ell_status')['discourse_effectiveness'].count()
ell_summary = pd.DataFrame({
    'Total_Discourses': ell_cnt,
    'Ineffective_%': ell_ct['Ineffective'].round(2),
    'Adequate_%': ell_ct['Adequate'].round(2),
    'Effective_%': ell_ct['Effective'].round(2)
})
print(ell_summary.to_string())
