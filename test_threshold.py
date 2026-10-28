import pandas as pd
import numpy as np
from sklearn.metrics import f1_score, classification_report

df = pd.read_csv('outputs/context_ablation_predictions.csv')
y_true = df['true_label'].values
y_pred_argmax = df['pred_label'].values

p0 = df['pred_proba_0'].values
p1 = df['pred_proba_1'].values
p2 = df['pred_proba_2'].values

print("Default Argmax Macro-F1:", f1_score(y_true, y_pred_argmax, average='macro'))
print("Default Ineffective F1:", f1_score(y_true, y_pred_argmax, average=None)[0])
print("Default Adequate F1:", f1_score(y_true, y_pred_argmax, average=None)[1])
print("Default Effective F1:", f1_score(y_true, y_pred_argmax, average=None)[2])

best_macro = 0
best_th = 0
results = []
for th in np.arange(0.10, 0.45, 0.02):
    # If p0 >= th, predict 0, else pick argmax between 1 and 2
    preds = np.where(p0 >= th, 0, np.where(p2 > p1, 2, 1))
    macro = f1_score(y_true, preds, average='macro')
    ineff_f1 = f1_score(y_true, preds, average=None)[0]
    results.append((th, macro, ineff_f1))
    if macro > best_macro:
        best_macro = macro
        best_th = th

for th, macro, ineff_f1 in results[::2]:
    print(f"Threshold {th:.2f}: Macro-F1 = {macro:.4f}, Ineff F1 = {ineff_f1:.4f}")

print(f"\n>>> Optimal Threshold {best_th:.2f} -> Best Macro-F1: {best_macro:.4f} <<<")

# Check Case 8 with threshold tuning!
# Case 8: "Some kids will ask there parents to transfer school"
case8_idx = df[df['discourse_type'] == 'Claim'].index
for idx in case8_idx:
    # let's find the one with p0 ~ 0.1236
    if abs(df.loc[idx, 'pred_proba_0'] - 0.1236) < 0.005 and df.loc[idx, 'true_label'] == 0:
        print(f"\nCase 8 found at row {idx}!")
        print(f"P0: {df.loc[idx, 'pred_proba_0']}, Argmax pred: {df.loc[idx, 'pred_label']}")
        for t in [0.33, 0.20, 0.15, 0.10]:
            p_label = 0 if df.loc[idx, 'pred_proba_0'] >= t else (2 if df.loc[idx, 'pred_proba_2'] > df.loc[idx, 'pred_proba_1'] else 1)
            print(f"At threshold {t:.2f} -> Prediction becomes: {p_label} (0=Ineffective!)")
        break
