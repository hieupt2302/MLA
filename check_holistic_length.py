import pandas as pd
import numpy as np

# Load validation assignments and test/predictions with strict string types!
df_train = pd.read_csv('persuade_corpus_2.0_train.csv', 
                       dtype={'essay_id': str, 'discourse_id': str},
                       usecols=['essay_id', 'discourse_id', 'holistic_essay_score', 'essay_word_count', 'discourse_effectiveness'])

# Remove unannotated / dropna
df_train = df_train.dropna(subset=['discourse_effectiveness']).drop_duplicates(subset=['discourse_id'])
print("Clean train rows:", df_train.shape)

df_val_preds = pd.read_csv('outputs/context_ablation_predictions.csv',
                           dtype={'essay_id': str, 'discourse_id': str})
print("Val preds shape:", df_val_preds.shape)

merged = pd.merge(df_val_preds, df_train[['discourse_id', 'holistic_essay_score', 'essay_word_count']], on='discourse_id', how='inner')
print("Merged shape:", merged.shape)

merged['is_error'] = (merged['pred_label'] != merged['true_label']).astype(int)

def assign_q(wc):
    if wc <= 315:
        return 'Q1 (148-315)'
    elif wc <= 422:
        return 'Q2 (316-422)'
    elif wc <= 566:
        return 'Q3 (423-566)'
    else:
        return 'Q4 (567+)'

merged['length_quartile'] = merged['essay_word_count'].apply(assign_q)

print("\n--- ERROR RATE (%) BY HOLISTIC SCORE X LENGTH QUARTILE ---")
pivot_mean = merged.pivot_table(index='holistic_essay_score', columns='length_quartile', values='is_error', aggfunc='mean') * 100
pivot_count = merged.pivot_table(index='holistic_essay_score', columns='length_quartile', values='is_error', aggfunc='count')

print(pivot_mean.round(2))
print("\n--- SAMPLE COUNT (N) BY HOLISTIC SCORE X LENGTH QUARTILE ---")
print(pivot_count)

# Save to outputs
pivot_mean.to_csv('outputs/holistic_score_x_length_quartile_error_rates.csv')
print("\nSaved to outputs/holistic_score_x_length_quartile_error_rates.csv successfully!")
