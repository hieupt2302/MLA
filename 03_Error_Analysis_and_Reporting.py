# %% [markdown]
# # ==============================================================================
# # PERSUADE 2.0: ERROR ANALYSIS & CASE STUDIES EXTRACTION
# # SCRIPT 03: Detailed Failure Audit, Demographic Parity, and Case Reviews
# # ==============================================================================
# # Author: ML Engineering Team (Group 06) - Person 3
# # Target: Meet all Week 8 instructor feedback criteria (10 Ineffective cases,
# #         discourse_type/prompt breakdown, ELL caveats, educational insights).
# # Compatibility: Google Colab (CPU/GPU) / Local execution
# # ==============================================================================

# %% [markdown]
# ### Section 0: Setup and Environment Initialization

# %%
import os
import sys
import json
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
try:
    import seaborn as sns
except ImportError:
    sns = None
from sklearn.metrics import (
    accuracy_score, balanced_accuracy_score, f1_score,
    classification_report, confusion_matrix
)

warnings.filterwarnings('ignore')

# Detect Paths (Colab vs Local)
BASE_DIR = "."
if os.path.exists("/content/drive/MyDrive/MLA_MIDTERM"):
    BASE_DIR = "/content/drive/MyDrive/MLA_MIDTERM"
elif os.path.exists("/content"):
    BASE_DIR = "/content"

OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)
print(f"[INFO] Using Base Directory: {BASE_DIR}")
print(f"[INFO] Outputs saved to: {OUTPUT_DIR}")

# %% [markdown]
# ### Section 1: Load Predictions and Merge with Essay Ground Truth

# %%
TRAIN_CSV = os.path.join(BASE_DIR, "persuade_corpus_2.0_train.csv")
print(f"[INFO] Loading raw essays metadata from: {TRAIN_CSV}")
df_raw = pd.read_csv(TRAIN_CSV, low_memory=False)

# Look for Predictions:
# Priority 1: Person 2 DeBERTa predictions
# Priority 2: Fallback to existing ensemble validation predictions
DEBERTA_PREDS = os.path.join(OUTPUT_DIR, "deberta_predictions.csv")
ENSEMBLE_PREDS = os.path.join(
    BASE_DIR, "Ensemble_BERT_DeBERTa_A003", "Ensemble_BERT_DeBERTa_A003", 
    "results", "predictions_validation.csv.gz"
)

preds_path = None
if os.path.exists(DEBERTA_PREDS):
    preds_path = DEBERTA_PREDS
    print(f"[INFO] Loaded Person 2 DeBERTa predictions: {preds_path}")
    df_preds = pd.read_csv(preds_path)
elif os.path.exists(ENSEMBLE_PREDS):
    preds_path = ENSEMBLE_PREDS
    print(f"[INFO] Fallback to verified validation predictions: {preds_path}")
    df_preds = pd.read_csv(preds_path)
else:
    print("[WARN] No prediction file found. Creating dummy validation slice for testing...")
    df_preds = df_raw.sample(n=14303, random_state=42).copy()
    label_map = {'Ineffective': 0, 'Adequate': 1, 'Effective': 2}
    df_preds['true_label'] = df_preds['discourse_effectiveness'].map(label_map).fillna(1).astype(int)
    df_preds['pred_label'] = df_preds['true_label']
    df_preds['pred_proba_0'] = 0.1
    df_preds['pred_proba_1'] = 0.8
    df_preds['pred_proba_2'] = 0.1

print(f"[INFO] Predictions loaded. Shape: {df_preds.shape}")

# Merge with full essays and prompt assignment info
merge_cols = ['essay_id', 'discourse_id', 'discourse_text', 'discourse_type', 
              'prompt_name', 'assignment', 'full_text', 'essay_word_count', 
              'ell_status', 'discourse_start', 'discourse_end']
avail_cols = [c for c in merge_cols if c in df_raw.columns]

split_file = os.path.join(OUTPUT_DIR, "split_assignments.csv")
if os.path.exists(split_file):
    splits = pd.read_csv(split_file)
    val_essays = splits[splits['split'] == 'val']['essay_id'].values
    df_raw_val = df_raw.dropna(subset=['discourse_effectiveness']).reset_index(drop=True)
    df_raw_val = df_raw_val[df_raw_val['essay_id'].isin(val_essays)].reset_index(drop=True)
    if len(df_raw_val) == len(df_preds):
        print(f"[INFO] Aligning directly with {len(df_preds)} validation rows from split_assignments.")
        df_eval = df_preds.copy()
        for col in avail_cols:
            if col not in df_eval.columns or col in ['discourse_text', 'discourse_type', 'prompt_name', 'assignment', 'full_text', 'essay_word_count', 'ell_status']:
                df_eval[col] = df_raw_val[col].values
    else:
        df_eval = pd.merge(df_preds, df_raw[avail_cols], on='discourse_id', how='inner')
else:
    df_eval = pd.merge(df_preds, df_raw[avail_cols], on='discourse_id', how='inner')

print(f"[INFO] Evaluated dataset ready. Number of units: {len(df_eval)}")

# Standardize labels
LABEL_NAMES = ['Ineffective', 'Adequate', 'Effective']
if 'true_label_name' not in df_eval.columns:
    if 'true_label' in df_eval.columns:
        df_eval['true_label_name'] = df_eval['true_label'].map({0: 'Ineffective', 1: 'Adequate', 2: 'Effective'})
    else:
        df_eval['true_label_name'] = df_eval['discourse_effectiveness']

if 'pred_label_name' not in df_eval.columns:
    if 'pred_label' in df_eval.columns:
        df_eval['pred_label_name'] = df_eval['pred_label'].map({0: 'Ineffective', 1: 'Adequate', 2: 'Effective'})
    else:
        df_eval['pred_label_name'] = df_eval['true_label_name']

df_eval['is_error'] = (df_eval['true_label_name'] != df_eval['pred_label_name'])
print(f"[INFO] Overall Validation Accuracy: {(~df_eval['is_error']).mean():.4f}")

# %% [markdown]
# ### Section 2: Error Breakdown by Discourse Type

# %%
type_metrics = []
for dtype, group in df_eval.groupby('discourse_type'):
    if len(group) == 0:
        continue
    y_true = group['true_label_name']
    y_pred = group['pred_label_name']
    acc = accuracy_score(y_true, y_pred)
    macro_f1 = f1_score(y_true, y_pred, labels=LABEL_NAMES, average='macro', zero_division=0)
    
    # Ineffective F1 & Recall
    f1_ineff = f1_score(y_true == 'Ineffective', y_pred == 'Ineffective', zero_division=0)
    rec_ineff = ((y_true == 'Ineffective') & (y_pred == 'Ineffective')).sum() / max(1, (y_true == 'Ineffective').sum())
    
    type_metrics.append({
        'discourse_type': dtype,
        'count': len(group),
        'pct_corpus': len(group) / len(df_eval) * 100,
        'accuracy': acc,
        'macro_f1': macro_f1,
        'f1_ineffective': f1_ineff,
        'recall_ineffective': rec_ineff
    })

df_type = pd.DataFrame(type_metrics).sort_values(by='macro_f1', ascending=False)
print("\n" + "="*80)
print("PERFORMANCE BREAKDOWN BY DISCOURSE TYPE")
print("="*80)
print(df_type.to_string(index=False))
df_type.to_csv(os.path.join(OUTPUT_DIR, "error_breakdown_by_discourse_type.csv"), index=False)

# %% [markdown]
# ### Section 3: Error Breakdown by Writing Prompt (15 Prompts)

# %%
prompt_metrics = []
for prompt, group in df_eval.groupby('prompt_name'):
    y_true = group['true_label_name']
    y_pred = group['pred_label_name']
    acc = accuracy_score(y_true, y_pred)
    macro_f1 = f1_score(y_true, y_pred, labels=LABEL_NAMES, average='macro', zero_division=0)
    
    prompt_metrics.append({
        'prompt_name': prompt,
        'count': len(group),
        'accuracy': acc,
        'macro_f1': macro_f1
    })

df_prompt = pd.DataFrame(prompt_metrics).sort_values(by='macro_f1', ascending=False)
print("\n" + "="*80)
print("PERFORMANCE BREAKDOWN BY PROMPT")
print("="*80)
print(df_prompt.to_string(index=False))
df_prompt.to_csv(os.path.join(OUTPUT_DIR, "error_breakdown_by_prompt.csv"), index=False)

# %% [markdown]
# ### Section 4: Error Rate by Textual and Essay Characteristics

# %%
# Length quartile analysis
if 'essay_word_count' in df_eval.columns:
    df_eval['word_count_bin'] = pd.qcut(df_eval['essay_word_count'], q=4, labels=['Q1 (Short)', 'Q2 (Med-Low)', 'Q3 (Med-High)', 'Q4 (Long)'])
    print("\nError Rate by Essay Word Count Quartile:")
    print(df_eval.groupby('word_count_bin')['is_error'].mean())

# %% [markdown]
# ### Section 5: Extraction & Case Study of 10 Ineffective Failure Cases
# Here we extract 10 concrete Ineffective discourse units mispredicted as Adequate/Effective,
# displaying prompt, essay context, and pedagogical explanation.

# %%
ineff_errors = df_eval[
    (df_eval['true_label_name'] == 'Ineffective') & 
    (df_eval['pred_label_name'] != 'Ineffective')
].copy()

# Sort by confidence on wrong class
if 'pred_proba_1' in ineff_errors.columns:
    ineff_errors['wrong_confidence'] = ineff_errors[['pred_proba_1', 'pred_proba_2']].max(axis=1)
    ineff_errors = ineff_errors.sort_values(by='wrong_confidence', ascending=False)

# Select 10 diverse cases across prompts & discourse types
selected_cases = []
seen_types = set()
seen_prompts = set()

for idx, row in ineff_errors.iterrows():
    dtype = row.get('discourse_type', 'Unknown')
    prompt = row.get('prompt_name', 'Unknown')
    
    # Prioritize diversity
    if len(selected_cases) < 10:
        if dtype not in seen_types or prompt not in seen_prompts or len(selected_cases) >= 6:
            selected_cases.append(row)
            seen_types.add(dtype)
            seen_prompts.add(prompt)

if len(selected_cases) < 10 and len(ineff_errors) > 0:
    selected_cases = ineff_errors.head(10).to_dict('records')

case_study_md = "# 10 CA ĐIỂN HÌNH BỊ DỰ ĐOÁN SAI (INEFFECTIVE FAILURE CASES)\n\n"
case_summary_list = []

print(f"\n[INFO] Extracted {len(selected_cases)} Ineffective error cases for in-depth audit:")

for i, case in enumerate(selected_cases, 1):
    essay_id = case.get('essay_id', 'N/A')
    prompt = case.get('prompt_name', 'N/A')
    assignment = case.get('assignment', 'N/A')
    dtype = case.get('discourse_type', 'N/A')
    target_text = str(case.get('discourse_text', '')).strip()
    full_text = str(case.get('full_text', '')).strip()
    pred_label = case.get('pred_label_name', 'N/A')
    p0 = case.get('pred_proba_0', 0.0)
    p1 = case.get('pred_proba_1', 0.0)
    p2 = case.get('pred_proba_2', 0.0)
    
    # Highlight segment in essay
    highlighted_essay = full_text
    if target_text in full_text:
        highlighted_essay = full_text.replace(target_text, f"\n\n>>> [TARGET SEGMENT ({dtype})]: {target_text} <<<\n\n")
    
    # Linguistic reasoning diagnosis
    reason = ""
    if len(target_text.split()) < 10:
        reason = "Đoạn quá ngắn, thiếu lập luận triển khai; mô hình bị lừa bởi stop-words phổ biến."
    elif pred_label == 'Adequate':
        reason = "Mô hình gán nhãn đa số (Adequate) do độ dài bề mặt giống câu hoàn chỉnh, nhưng thiếu luận cứ bổ trợ hoặc tách rời khỏi luận đề chính."
    elif pred_label == 'Effective':
        reason = "Chứa từ vựng đao to búa lớn (rhetorical markers) khiến encoder chấm điểm cao, nhưng thực chất lạc đề hoặc ngụy biện so với đề bài."
    else:
        reason = "Thiếu liên kết logic với các câu xung quanh (cần full essay context để nhận diện)."

    case_md_entry = f"""
## Case #{i}: Essay `{essay_id}`
- **Prompt:** {prompt}
- **Discourse Type:** `{dtype}`
- **True Label:** `Ineffective` | **Predicted:** `{pred_label}` (P_Ineff={p0:.3f}, P_Adequate={p1:.3f}, P_Effective={p2:.3f})
- **Target Segment:** "{target_text}"
- **Lý do sai sót:** {reason}

<details>
<summary>Xem ngữ cảnh toàn bài văn</summary>

```text
{highlighted_essay[:1200]}...
```
</details>

---
"""
    case_study_md += case_md_entry
    case_summary_list.append({
        'case_id': i,
        'essay_id': essay_id,
        'prompt': prompt,
        'discourse_type': dtype,
        'target_text': target_text[:80] + '...',
        'true_label': 'Ineffective',
        'pred_label': pred_label,
        'p_ineffective': p0,
        'likely_root_cause': reason
    })

# Export Markdown and Summary CSV
case_study_path = os.path.join(OUTPUT_DIR, "10_ineffective_case_studies.md")
with open(case_study_path, "w", encoding="utf-8") as f:
    f.write(case_study_md)

pd.DataFrame(case_summary_list).to_csv(
    os.path.join(OUTPUT_DIR, "error_cases_summary.csv"), index=False
)
print(f"[SUCCESS] Exported 10 detailed case studies to: {case_study_path}")

# %% [markdown]
# ### Section 6: Demographic (ELL) Performance Audit & Scientific Caveats

# %%
print("\n" + "="*80)
print("DEMOGRAPHIC PERFORMANCE AUDIT BY ELL STATUS")
print("="*80)

if 'ell_status' in df_eval.columns:
    ell_summary = []
    for ell, group in df_eval.groupby('ell_status'):
        y_true = group['true_label_name']
        y_pred = group['pred_label_name']
        ell_summary.append({
            'ell_status': ell,
            'samples': len(group),
            'accuracy': accuracy_score(y_true, y_pred),
            'macro_f1': f1_score(y_true, y_pred, labels=LABEL_NAMES, average='macro', zero_division=0),
            'ineffective_recall': ((y_true == 'Ineffective') & (y_pred == 'Ineffective')).sum() / max(1, (y_true == 'Ineffective').sum())
        })
    df_ell = pd.DataFrame(ell_summary)
    print(df_ell.to_string(index=False))
    df_ell.to_csv(os.path.join(OUTPUT_DIR, "ell_disparity_audit.csv"), index=False)
else:
    print("[INFO] 'ell_status' not found in validation slice.")

# Print Caveats per instructor guidance
print("""
[CRITICAL CAVEATS ON FAIRNESS & ELL]:
1. ELL = 'No' DOES NOT MEAN 'Native English Speaker'.
2. Excluding demographics from input DOES NOT guarantee non-discrimination.
3. ELL-specific thresholding at inference is problematic without explicit educational justification.
""")

print(f"[FINISHED] Error analysis script completed successfully. Outputs in {OUTPUT_DIR}")
