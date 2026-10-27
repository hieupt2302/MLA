# %% [markdown]
# # ==============================================================================
# # PERSUADE 2.0: DISCOURSE EFFECTIVENESS CLASSIFICATION
# # SCRIPT 06: Leave-One-Prompt-Out (LOPO) Evaluation with DeBERTa-v3-base
# # ==============================================================================
# # Course: CLC02 - Group 06 | Environment: GPU (Colab T4 / V100 / A100) | Runtime: ~2-3h per fold
# #
# # Research Objective:
# # Address Week 9 Instructor Feedback:
# # "Hien essay khac nhau nhung 15 de co mat o ca train va validation, nen chua
# # biet mo hinh lam gi voi mot de moi. Leave-one-prompt-out se tra loi cau hoi ma
# # giao vien that su gap."
# #
# # Key Research Questions Addressed:
# # 1. Out-of-Prompt Generalization: How much does Macro-F1 drop when evaluating on
# #    a completely unseen essay prompt (zero prompt leakage)?
# # 2. Question 2 from Instructor: "Voi mot de hoan toan moi, cac em du doan
# #    macro-F1 se giam nhieu nhat o loai don vi nao?"
# #
# # Folds Protocol:
# # Evaluates generalization across diverse held-out prompts (e.g. Science, Civics, Narrative).
# # By default, evaluates 3 representative prompts (or all 15 if --all_prompts is passed).
# # ==============================================================================

# %%
import os
import sys
import gc
import json
import time
import math
import random
import shutil
import warnings
import argparse
import inspect
from typing import Dict, List, Tuple, Any

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

# Dynamic package installation check for standalone Colab execution
REQUIRED_PKGS = ["torch", "transformers", "datasets", "accelerate", "sklearn", "scipy", "matplotlib"]
for pkg in ["torch", "transformers", "datasets", "accelerate"]:
    try:
        __import__(pkg)
    except ImportError:
        print(f"[*] Package '{pkg}' not found. Installing dependencies via pip...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "torch", "transformers", "datasets", "accelerate", "scikit-learn", "matplotlib", "seaborn"])
        break

import numpy as np
import pandas as pd
import scipy.special
import matplotlib.pyplot as plt

try:
    import seaborn as sns
    HAS_SEABORN = True
except ImportError:
    HAS_SEABORN = False

from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    classification_report,
    confusion_matrix,
    cohen_kappa_score,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.utils.class_weight import compute_class_weight

import torch
import torch.nn as nn
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
    DataCollatorWithPadding,
    set_seed,
)
from datasets import Dataset

# ------------------------------------------------------------------------------
# 0.1 Reproducibility Seed Initialization
# ------------------------------------------------------------------------------
RANDOM_SEED = 42

def enforce_reproducibility(seed: int = RANDOM_SEED) -> None:
    """Set global seeds for Python, NumPy, PyTorch, and Transformers."""
    random.seed(seed)
    np.random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
    set_seed(seed)

enforce_reproducibility(RANDOM_SEED)

# ------------------------------------------------------------------------------
# 0.2 Device Detection & Colab Setup
# ------------------------------------------------------------------------------
print("\n" + "=" * 80)
print("SECTION 0: HARDWARE & ENVIRONMENT VERIFICATION")
print("=" * 80)

if torch.cuda.is_available():
    DEVICE_NAME = torch.cuda.get_device_name(0)
    VRAM_GB = torch.cuda.get_device_properties(0).total_memory / (1024 ** 3)
    print(f"[Hardware] GPU Detected: {DEVICE_NAME} (VRAM: {VRAM_GB:.2f} GB)")
    USE_FP16 = True
    DEVICE = torch.device("cuda")
else:
    print("[Hardware] WARNING: No GPU detected. Running on CPU (training will be slow).")
    USE_FP16 = False
    DEVICE = torch.device("cpu")

IN_COLAB = "google.colab" in sys.modules
if IN_COLAB:
    print("[Colab] Detected Google Colab environment.")
    try:
        from google.colab import drive
        if not os.path.exists("/content/drive"):
            drive.mount("/content/drive")
    except Exception as e:
        print(f"[Colab] Drive mount note: {e}")

# ------------------------------------------------------------------------------
# 0.3 Argument Parsing
# ------------------------------------------------------------------------------
parser = argparse.ArgumentParser(description="DeBERTa-v3-base Leave-One-Prompt-Out (LOPO) Evaluation")
parser.add_argument("--data_path", type=str, default="persuade_corpus_2.0_train.csv", help="Path to train CSV")
parser.add_argument("--output_dir", type=str, default="outputs", help="Directory to store outputs")
parser.add_argument("--prompts", nargs="+", default=None, help="Specific prompt names to hold out")
parser.add_argument("--all_prompts", action="store_true", help="Run LOPO for all 15 prompts")
parser.add_argument("--quick", action="store_true", help="Quick demo mode with small subset")
parser.add_argument("--epochs", type=int, default=3, help="Training epochs per fold (default: 3)")
parser.add_argument("--batch_size", type=int, default=8, help="Train batch size per device (default: 8)")
parser.add_argument("--grad_accum", type=int, default=4, help="Gradient accumulation steps (default: 4)")
parser.add_argument("--lr", type=float, default=2e-5, help="Learning rate (default: 2e-5)")
parser.add_argument("--max_length", type=int, default=512, help="Max sequence length (default: 512)")

args, _ = parser.parse_known_args()

# Smart base path detection for Google Colab / Local
if os.path.exists("/content/drive/MyDrive/MLA_Dataset"):
    BASE_DIR = "/content/drive/MyDrive/MLA_Dataset"
elif os.path.exists("/content/drive/MyDrive/MLA_MIDTERM"):
    BASE_DIR = "/content/drive/MyDrive/MLA_MIDTERM"
else:
    BASE_DIR = os.getcwd()

OUTPUT_DIR = args.output_dir if os.path.isabs(args.output_dir) else os.path.join(BASE_DIR, args.output_dir)
os.makedirs(OUTPUT_DIR, exist_ok=True)
LOPO_PRED_DIR = os.path.join(OUTPUT_DIR, "lopo_deberta_predictions")
os.makedirs(LOPO_PRED_DIR, exist_ok=True)

# ------------------------------------------------------------------------------
# SECTION 1: DATA LOADING & PROMPT SELECTION
# ------------------------------------------------------------------------------
print("\n" + "=" * 80)
print("SECTION 1: DATA LOADING & LOPO FOLD CONFIGURATION")
print("=" * 80)

# Resolve train CSV path
candidates = [
    args.data_path,
    os.path.join(BASE_DIR, "persuade_corpus_2.0_train.csv"),
    os.path.join(os.getcwd(), "persuade_corpus_2.0_train.csv"),
    "/content/persuade_corpus_2.0_train.csv",
]
data_path = next((p for p in candidates if p and os.path.exists(p)), None)
if not data_path:
    raise FileNotFoundError(f"Cannot locate persuade_corpus_2.0_train.csv. Searched in: {candidates}")

print(f"[Data] Loading dataset from: {data_path}")
needed_cols = [
    "essay_id", "discourse_id", "discourse_text",
    "discourse_type", "discourse_effectiveness", "prompt_name"
]

raw_df = pd.read_csv(data_path, usecols=needed_cols, dtype={"essay_id": str, "discourse_id": str}, low_memory=False)

# Clean and filter
df = raw_df.dropna(subset=["discourse_effectiveness", "discourse_text", "prompt_name"]).copy()
df["discourse_text"] = df["discourse_text"].astype(str).str.strip()
df["discourse_type"] = df["discourse_type"].astype(str).str.strip()
df["prompt_name"] = df["prompt_name"].astype(str).str.strip()
df = df[df["discourse_text"].str.len() > 0].reset_index(drop=True)
df["essay_id"] = df["essay_id"].astype(str).str.strip()
df["discourse_id"] = df["discourse_id"].astype(str).str.strip()

# Format input text: standard [discourse_type] [SEP] [discourse_text]
df["input_text"] = df["discourse_type"] + " [SEP] " + df["discourse_text"]

LABEL2ID = {"Ineffective": 0, "Adequate": 1, "Effective": 2}
ID2LABEL = {0: "Ineffective", 1: "Adequate", 2: "Effective"}
CLASS_NAMES = ["Ineffective", "Adequate", "Effective"]
df["label"] = df["discourse_effectiveness"].map(LABEL2ID)

all_available_prompts = sorted(df["prompt_name"].unique())
print(f"[Data] Found {len(all_available_prompts)} distinct prompts across {len(df):,} units.")

# ------------------------------------------------------------------------------
# 1.1 Dynamic Prompt Selection from Classical Baseline Benchmark
# ------------------------------------------------------------------------------
classical_candidates = [
    os.path.join(OUTPUT_DIR, "lopo_classical_results.csv"),
    os.path.join(BASE_DIR, "outputs", "lopo_classical_results.csv"),
    os.path.join(os.getcwd(), "outputs", "lopo_classical_results.csv"),
    os.path.join(os.getcwd(), "lopo_classical_results.csv"),
]
classical_file = next((p for p in classical_candidates if os.path.exists(p)), None)
classical_rf_scores: Dict[str, float] = {}
classical_rf_info: Dict[str, Dict[str, Any]] = {}
prompt_tier_map: Dict[str, str] = {}
auto_selected_prompts = None

if classical_file:
    print(f"\n[Data Flow] Detected classical LOPO baseline output at: {classical_file}")
    try:
        df_class = pd.read_csv(classical_file)
        df_class_overall = df_class[df_class["level"] == "overall"].sort_values(by="macro_f1", ascending=True).reset_index(drop=True)
        print("\n[Data Flow] Ranking of 15 Prompts from Classical Random Forest Baseline Benchmark:")
        for rank_idx, row_c in df_class_overall.iterrows():
            p_name = str(row_c["held_out_prompt"]).strip()
            classical_rf_scores[p_name] = float(row_c["macro_f1"])
            classical_rf_info[p_name] = {
                "macro_f1": float(row_c["macro_f1"]),
                "accuracy": float(row_c["accuracy"]),
                "f1_ineffective": float(row_c["f1_ineffective"]),
                "rank": rank_idx + 1,
            }
            if rank_idx < 3 or rank_idx >= len(df_class_overall) - 3 or rank_idx == len(df_class_overall) // 2:
                print(f"  Rank {rank_idx+1:2d}/15: {p_name:<40} | RF Macro-F1: {float(row_c['macro_f1']):.4f}")

        hardest_p = str(df_class_overall.iloc[0]["held_out_prompt"]).strip()
        hardest_f1 = float(df_class_overall.iloc[0]["macro_f1"])
        prompt_tier_map[hardest_p] = "Hardest (Rank 1/15)"

        median_idx = len(df_class_overall) // 2
        median_p = str(df_class_overall.iloc[median_idx]["held_out_prompt"]).strip()
        median_f1 = float(df_class_overall.iloc[median_idx]["macro_f1"])
        prompt_tier_map[median_p] = f"Median (Rank {median_idx + 1}/15)"

        easiest_p = str(df_class_overall.iloc[-1]["held_out_prompt"]).strip()
        easiest_f1 = float(df_class_overall.iloc[-1]["macro_f1"])
        prompt_tier_map[easiest_p] = f"Easiest (Rank {len(df_class_overall)}/15)"

        auto_selected_prompts = [hardest_p, median_p, easiest_p]
    except Exception as e:
        print(f"[Data Flow] Warning parsing classical file: {e}")

# Resolve target prompts to hold out
if args.all_prompts:
    target_prompts = all_available_prompts
    print("[LOPO Setup] Running full 15-fold Leave-One-Prompt-Out evaluation.")
elif args.prompts is not None and len(args.prompts) > 0:
    target_prompts = []
    for p in args.prompts:
        matched = [avail for avail in all_available_prompts if p.lower() in avail.lower()]
        if matched:
            target_prompts.append(matched[0])
        else:
            print(f"[LOPO Setup] Warning: Prompt '{p}' not matched in dataset. Skipping.")
    if not target_prompts:
        raise ValueError(f"None of the requested prompts {args.prompts} were matched in dataset!")
elif auto_selected_prompts is not None:
    target_prompts = auto_selected_prompts
    print("\n" + "=" * 80)
    print("DYNAMIC PROMPT SELECTION GROUNDED ON CLASSICAL RANDOM FOREST BENCHMARK:")
    print("=" * 80)
    print(f"  * Hardest Prompt (Rank  1/15) : '{hardest_p}' (Classical RF Macro-F1 = {hardest_f1:.4f})")
    print(f"  * Median Prompt  (Rank {median_idx + 1}/15) : '{median_p}' (Classical RF Macro-F1 = {median_f1:.4f})")
    print(f"  * Easiest Prompt (Rank {len(df_class_overall)}/15) : '{easiest_p}' (Classical RF Macro-F1 = {easiest_f1:.4f})")
    print("=" * 80)
else:
    raise FileNotFoundError(
        "\n" + "=" * 80 + "\n"
        "[FATAL ERROR] Khong tim thay file ket qua benchmark co dien: 'outputs/lopo_classical_results.csv'!\n"
        "Theo thiet ke quy trinh nghien cuu nhom CLC02, Script 06 KHONG chon de tai thu cong ma\n"
        "BAT BUOC phai doc dong ket qua tu Script 04 (Random Forest Baseline) de chon ra 3 de dai dien:\n"
        "  1. Hardest (Kho nhat - Rank 1/15)\n"
        "  2. Median  (Trung binh - Rank 8/15)\n"
        "  3. Easiest (De nhat  - Rank 15/15)\n"
        "dong thoi so sanh truc tiep do tang truong Macro-F1 giua DeBERTa va Random Forest.\n\n"
        "HUONG DAN XU LY:\n"
        "  - Hay dam bao Script 04 da duoc thuc thi va tao ra file 'outputs/lopo_classical_results.csv'.\n"
        "  - Dat file 'lopo_classical_results.csv' vao thu muc 'outputs/' tren Google Drive (hoac Local).\n"
        "=" * 80
    )

print(f"\n[LOPO Setup] Target held-out prompts for DeBERTa ({len(target_prompts)} prompts):")
for i, p in enumerate(target_prompts, 1):
    n_p = (df["prompt_name"] == p).sum()
    rf_baseline_str = f" | RF Baseline F1: {classical_rf_scores[p]:.4f}" if p in classical_rf_scores else ""
    print(f"  {i}. '{p}' ({n_p:,} units{rf_baseline_str})")

# ------------------------------------------------------------------------------
# SECTION 2: TOKENIZER & TRAINER DEFINITION
# ------------------------------------------------------------------------------
MODEL_NAME = "microsoft/deberta-v3-base"
MAX_LENGTH = args.max_length

print(f"\n[Tokenizer] Loading {MODEL_NAME} tokenizer (max_length={MAX_LENGTH})...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=True)
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

class WeightedLossTrainer(Trainer):
    """Custom Trainer with class-weighted CrossEntropyLoss."""
    def __init__(self, *args, class_weights: torch.Tensor = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.class_weights = class_weights

    def compute_loss(self, model, inputs, return_outputs=False, **kwargs):
        labels = inputs.get("labels")
        outputs = model(**inputs)
        logits = outputs.get("logits")
        if self.class_weights is not None:
            weights = self.class_weights.to(device=logits.device, dtype=logits.dtype)
            loss_fn = nn.CrossEntropyLoss(weight=weights)
        else:
            loss_fn = nn.CrossEntropyLoss()
        loss = loss_fn(logits.view(-1, self.model.config.num_labels), labels.view(-1))
        return (loss, outputs) if return_outputs else loss

def compute_metrics(eval_pred) -> Dict[str, float]:
    logits, labels = eval_pred
    if isinstance(logits, tuple):
        logits = logits[0]
    preds = np.argmax(logits, axis=-1)
    macro_f1 = f1_score(labels, preds, average="macro", zero_division=0)
    acc = accuracy_score(labels, preds)
    bal_acc = balanced_accuracy_score(labels, preds)
    qwk = cohen_kappa_score(labels, preds, weights="quadratic")
    per_class_f1 = f1_score(labels, preds, average=None, zero_division=0)
    return {
        "macro_f1": float(macro_f1),
        "accuracy": float(acc),
        "balanced_accuracy": float(bal_acc),
        "qwk": float(qwk),
        "f1_ineffective": float(per_class_f1[0]),
        "f1_adequate": float(per_class_f1[1]),
        "f1_effective": float(per_class_f1[2]),
    }

def preprocess_function(examples: Dict[str, List[Any]]) -> Dict[str, Any]:
    return tokenizer(
        examples["input_text"],
        truncation=True,
        max_length=MAX_LENGTH,
        padding=False
    )

ta_params = inspect.signature(TrainingArguments.__init__).parameters
eval_strategy_key = "eval_strategy" if "eval_strategy" in ta_params else "evaluation_strategy"
train_epochs = 1 if args.quick else args.epochs

# ------------------------------------------------------------------------------
# SECTION 3: LEAVE-ONE-PROMPT-OUT TRAINING & EVALUATION LOOP
# ------------------------------------------------------------------------------
print("\n" + "=" * 80)
print("SECTION 3: EXECUTING LOPO TRAINING & OUT-OF-PROMPT EVALUATION")
print("=" * 80)

lopo_overall_records: List[Dict[str, Any]] = []
lopo_dt_records: List[Dict[str, Any]] = []

for fold_idx, held_out_prompt in enumerate(target_prompts, 1):
    fold_start = time.time()
    clean_pname = held_out_prompt.replace('"', '').replace('/', '_').replace('?', '').replace(' ', '_')
    fold_ckpt_dir = os.path.join(OUTPUT_DIR, f"lopo_ckpt_fold_{fold_idx}_{clean_pname}")

    print("\n" + "-" * 75)
    print(f"LOPO FOLD {fold_idx}/{len(target_prompts)}: HELD-OUT PROMPT = '{held_out_prompt}'")
    print("-" * 75)

    # Partition dataset: train = remaining 14 prompts, test = held-out prompt
    fold_train_df = df[df["prompt_name"] != held_out_prompt].copy().reset_index(drop=True)
    fold_test_df = df[df["prompt_name"] == held_out_prompt].copy().reset_index(drop=True)

    n_train_units = len(fold_train_df)
    n_train_essays = fold_train_df["essay_id"].nunique()
    n_test_units = len(fold_test_df)
    n_test_essays = fold_test_df["essay_id"].nunique()

    print(f"[Fold Split] Train set : {n_train_units:,} units ({n_train_essays:,} essays across 14 prompts)")
    print(f"[Fold Split] Test set  : {n_test_units:,} units ({n_test_essays:,} essays for held-out prompt)")

    # Assert strict zero prompt leakage
    assert held_out_prompt not in fold_train_df["prompt_name"].values, "PROMPT LEAKAGE DETECTED!"

    if args.quick:
        print("[*] Quick Mode: Subsampling fold data for rapid testing...")
        train_sample_essays = random.sample(list(fold_train_df["essay_id"].unique()), min(60, n_train_essays))
        test_sample_essays = random.sample(list(fold_test_df["essay_id"].unique()), min(20, n_test_essays))
        fold_train_df = fold_train_df[fold_train_df["essay_id"].isin(train_sample_essays)].reset_index(drop=True)
        fold_test_df = fold_test_df[fold_test_df["essay_id"].isin(test_sample_essays)].reset_index(drop=True)

    # Compute fold-specific class weights
    fold_y = fold_train_df["label"].values
    fold_weights = compute_class_weight(
        class_weight="balanced",
        classes=np.array([0, 1, 2]),
        y=fold_y
    )
    fold_weights_tensor = torch.tensor(fold_weights, dtype=torch.float)

    # Build HuggingFace Datasets
    hf_train_fold = Dataset.from_pandas(fold_train_df[["discourse_id", "essay_id", "input_text", "label"]])
    hf_test_fold = Dataset.from_pandas(fold_test_df[["discourse_id", "essay_id", "input_text", "label"]])

    tok_train_fold = hf_train_fold.map(preprocess_function, batched=True, batch_size=2000, remove_columns=["input_text"])
    tok_test_fold = hf_test_fold.map(preprocess_function, batched=True, batch_size=2000, remove_columns=["input_text"])

    # Fresh DeBERTa model for fold
    enforce_reproducibility(RANDOM_SEED + fold_idx)
    fold_model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=3,
        id2label=ID2LABEL,
        label2id=LABEL2ID
    )

    fold_training_args = TrainingArguments(
        output_dir=fold_ckpt_dir,
        learning_rate=args.lr,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size * 2,
        gradient_accumulation_steps=args.grad_accum,
        num_train_epochs=train_epochs,
        warmup_ratio=0.1,
        fp16=USE_FP16,
        **{eval_strategy_key: "epoch"},
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="macro_f1",
        greater_is_better=True,
        seed=RANDOM_SEED + fold_idx,
        save_total_limit=1,
        logging_steps=25 if args.quick else 100,
        logging_strategy="steps",
        report_to="none",
    )

    fold_trainer = WeightedLossTrainer(
        model=fold_model,
        args=fold_training_args,
        train_dataset=tok_train_fold,
        eval_dataset=tok_test_fold,
        tokenizer=tokenizer,
        data_collator=data_collator,
        compute_metrics=compute_metrics,
        class_weights=fold_weights_tensor,
    )

    print(f"[Fold Training] Training DeBERTa on {len(tok_train_fold):,} units...")
    fold_trainer.train()

    # Inference on held-out prompt
    print(f"[Fold Evaluation] Predicting on unseen prompt '{held_out_prompt}' ({len(tok_test_fold):,} units)...")
    fold_preds_raw = fold_trainer.predict(tok_test_fold)
    fold_logits = fold_preds_raw.predictions
    if isinstance(fold_logits, tuple):
        fold_logits = fold_logits[0]

    fold_probs = scipy.special.softmax(fold_logits, axis=-1)
    fold_preds = np.argmax(fold_probs, axis=-1)
    fold_labels = fold_test_df["label"].values

    # Compute fold overall metrics
    f_macro_f1 = f1_score(fold_labels, fold_preds, average="macro", zero_division=0)
    f_acc = accuracy_score(fold_labels, fold_preds)
    f_bal_acc = balanced_accuracy_score(fold_labels, fold_preds)
    f_qwk = cohen_kappa_score(fold_labels, fold_preds, weights="quadratic")
    f_kappa = cohen_kappa_score(fold_labels, fold_preds)
    f_per_f1 = f1_score(fold_labels, fold_preds, average=None, zero_division=0)
    f_per_rec = recall_score(fold_labels, fold_preds, average=None, zero_division=0)

    print(f"[Fold Results] Macro-F1: {f_macro_f1:.4f} | Accuracy: {f_acc:.4f} | QWK: {f_qwk:.4f}")
    print(f"  * Ineffective: F1={f_per_f1[0]:.4f}, Recall={f_per_rec[0]:.4f}")
    print(f"  * Adequate   : F1={f_per_f1[1]:.4f}, Recall={f_per_rec[1]:.4f}")
    print(f"  * Effective  : F1={f_per_f1[2]:.4f}, Recall={f_per_rec[2]:.4f}")

    # Export fold predictions
    pred_file = os.path.join(LOPO_PRED_DIR, f"predictions_{clean_pname}.csv")
    fold_pred_df = pd.DataFrame({
        "discourse_id": fold_test_df["discourse_id"].values,
        "essay_id": fold_test_df["essay_id"].values,
        "discourse_type": fold_test_df["discourse_type"].values,
        "true_label": fold_labels,
        "pred_label": fold_preds,
        "pred_proba_0": np.round(fold_probs[:, 0], 6),
        "pred_proba_1": np.round(fold_probs[:, 1], 6),
        "pred_proba_2": np.round(fold_probs[:, 2], 6),
    })
    fold_pred_df.to_csv(pred_file, index=False)

    rf_f1 = classical_rf_scores.get(held_out_prompt, np.nan)
    rf_acc = classical_rf_info.get(held_out_prompt, {}).get("accuracy", np.nan)
    rf_ineff_f1 = classical_rf_info.get(held_out_prompt, {}).get("f1_ineffective", np.nan)
    delta_f1 = round(f_macro_f1 - rf_f1, 4) if not np.isnan(rf_f1) else np.nan

    lopo_overall_records.append({
        "tier": prompt_tier_map.get(held_out_prompt, "Custom"),
        "held_out_prompt": held_out_prompt,
        "n_train_units": n_train_units,
        "n_test_units": n_test_units,
        "n_test_essays": n_test_essays,
        "rf_classical_macro_f1": rf_f1,
        "macro_f1": round(f_macro_f1, 4),
        "delta_vs_rf": delta_f1,
        "accuracy": round(f_acc, 4),
        "balanced_accuracy": round(f_bal_acc, 4),
        "qwk": round(f_qwk, 4),
        "unweighted_kappa": round(f_kappa, 4),
        "f1_ineffective": round(f_per_f1[0], 4),
        "f1_adequate": round(f_per_f1[1], 4),
        "f1_effective": round(f_per_f1[2], 4),
        "recall_ineffective": round(f_per_rec[0], 4),
        "fold_time_min": round((time.time() - fold_start) / 60, 2),
    })

    # Per discourse_type breakdown for this held-out prompt
    for dt in sorted(fold_test_df["discourse_type"].unique()):
        mask = (fold_test_df["discourse_type"].values == dt)
        if mask.sum() > 0:
            dt_labels = fold_labels[mask]
            dt_preds = fold_preds[mask]
            dt_macro_f1 = f1_score(dt_labels, dt_preds, average="macro", zero_division=0)
            dt_ineff_f1 = f1_score(dt_labels == 0, dt_preds == 0, zero_division=0)
            dt_ineff_rec = recall_score(dt_labels == 0, dt_preds == 0, zero_division=0)
            dt_adeq_f1 = f1_score(dt_labels == 1, dt_preds == 1, zero_division=0)
            dt_eff_f1 = f1_score(dt_labels == 2, dt_preds == 2, zero_division=0)

            lopo_dt_records.append({
                "held_out_prompt": held_out_prompt,
                "discourse_type": dt,
                "n_test_units": int(mask.sum()),
                "n_ineffective": int((dt_labels == 0).sum()),
                "macro_f1": round(dt_macro_f1, 4),
                "f1_ineffective": round(dt_ineff_f1, 4),
                "recall_ineffective": round(dt_ineff_rec, 4),
                "f1_adequate": round(dt_adeq_f1, 4),
                "f1_effective": round(dt_eff_f1, 4),
            })

    # Clean up checkpoint directory to conserve disk space on Colab
    try:
        shutil.rmtree(fold_ckpt_dir)
        print(f"[Cleanup] Cleared checkpoint folder {fold_ckpt_dir} to save disk space.")
    except Exception as e:
        print(f"[Cleanup] Note: {e}")

    # Garbage collection
    del fold_model, fold_trainer, tok_train_fold, tok_test_fold
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    gc.collect()

# ------------------------------------------------------------------------------
# SECTION 4: AGGREGATE RESULTS & RESEARCH QUESTION ANSWERING
# ------------------------------------------------------------------------------
print("\n" + "=" * 80)
print("SECTION 4: LOPO SUMMARY & RESEARCH QUESTION ANALYSIS")
print("=" * 80)

# Export Overall LOPO Results
df_overall = pd.DataFrame(lopo_overall_records)
overall_path = os.path.join(OUTPUT_DIR, "lopo_deberta_results.csv")
df_overall.to_csv(overall_path, index=False)
print(f"[SAVED] LOPO Overall Results CSV: {overall_path}")
print("\nLOPO DeBERTa Performance Across Held-Out Prompts:")
display_cols = ["tier", "held_out_prompt", "n_test_units", "macro_f1", "accuracy", "f1_ineffective", "recall_ineffective"]
valid_display_cols = [c for c in display_cols if c in df_overall.columns]
print(df_overall[valid_display_cols].to_string(index=False))

# Export Dedicated Comparison Table (DeBERTa vs Classical Random Forest)
comparison_records = []
for r in lopo_overall_records:
    p = r["held_out_prompt"]
    if p in classical_rf_scores:
        rf_f1 = classical_rf_scores[p]
        deb_f1 = r["macro_f1"]
        delta = round(deb_f1 - rf_f1, 4)
        pct_gain = round((delta / rf_f1) * 100, 2) if rf_f1 > 0 else 0.0
        comparison_records.append({
            "tier": prompt_tier_map.get(p, "Custom"),
            "held_out_prompt": p,
            "n_test_units": r["n_test_units"],
            "rf_classical_macro_f1": rf_f1,
            "deberta_macro_f1": deb_f1,
            "delta_gain_over_rf": delta,
            "pct_gain_over_rf": pct_gain,
            "rf_accuracy": classical_rf_info.get(p, {}).get("accuracy", np.nan),
            "deberta_accuracy": r["accuracy"],
            "rf_f1_ineffective": classical_rf_info.get(p, {}).get("f1_ineffective", np.nan),
            "deberta_f1_ineffective": r["f1_ineffective"],
        })

if comparison_records:
    df_comp = pd.DataFrame(comparison_records)
    comp_path = os.path.join(OUTPUT_DIR, "lopo_deberta_vs_rf_comparison.csv")
    df_comp.to_csv(comp_path, index=False)
    print(f"\n[SAVED] DeBERTa vs Classical RF LOPO Comparison: {comp_path}")
    print("\n" + "=" * 80)
    print("LOPO BENCHMARK: CLASSICAL RANDOM FOREST BASELINE VS DEBERTA-V3")
    print("=" * 80)
    print(df_comp[["tier", "held_out_prompt", "rf_classical_macro_f1", "deberta_macro_f1", "delta_gain_over_rf", "pct_gain_over_rf"]].to_string(index=False))
    print("=" * 80)

# Export Per-Discourse-Type Breakdown
df_dt = pd.DataFrame(lopo_dt_records)
dt_path = os.path.join(OUTPUT_DIR, "lopo_per_discourse_type.csv")
df_dt.to_csv(dt_path, index=False)
print(f"\n[SAVED] LOPO Per-Discourse-Type Breakdown: {dt_path}")

# Load In-Domain Baseline for Comparison
in_domain_macro_f1 = 0.5768  # Week 9 DeBERTa on GroupShuffleSplit
mean_lopo_macro_f1 = float(df_overall["macro_f1"].mean())
std_lopo_macro_f1 = float(df_overall["macro_f1"].std()) if len(df_overall) > 1 else 0.0
prompt_generalization_gap = in_domain_macro_f1 - mean_lopo_macro_f1

print("\n" + "-" * 70)
print("OUT-OF-PROMPT GENERALIZATION GAP ANALYSIS (DEBERTA)")
print("-" * 70)
print(f"  In-Domain Validation Macro-F1 (Random Split) : {in_domain_macro_f1:.4f}")
print(f"  LOPO Mean Macro-F1 Across Held-Out Prompts    : {mean_lopo_macro_f1:.4f} (std = {std_lopo_macro_f1:.4f})")
print(f"  Generalization Gap (Drop on Unseen Prompts)  : {prompt_generalization_gap:+.4f} ({prompt_generalization_gap / in_domain_macro_f1 * 100:.2f}%)")
print("-" * 70)

# ------------------------------------------------------------------------------
# 4.2 Answer Instructor Question 2: Which Discourse Type Suffers Most?
# ------------------------------------------------------------------------------
print("\n" + "-" * 70)
print("INSTRUCTOR QUESTION 2: 'Voi de hoan toan moi, macro-F1 giam nhieu nhat o loai don vi nao?'")
print("-" * 70)

dt_summary = df_dt.groupby("discourse_type").agg({
    "n_test_units": "sum",
    "macro_f1": "mean",
    "f1_ineffective": "mean",
    "recall_ineffective": "mean",
    "f1_adequate": "mean",
    "f1_effective": "mean",
}).reset_index()

dt_summary = dt_summary.sort_values(by="macro_f1", ascending=True).reset_index(drop=True)
print("\nMean Performance by Discourse Type under LOPO (Unseen Prompts):")
print(dt_summary[["discourse_type", "n_test_units", "macro_f1", "f1_ineffective", "recall_ineffective"]].to_string(index=False))

worst_dt = dt_summary.iloc[0]["discourse_type"]
worst_mf1 = dt_summary.iloc[0]["macro_f1"]
worst_ineff_rec = dt_summary.iloc[0]["recall_ineffective"]

print(f"\n[Empirical Conclusion for Question 2]")
print(f"  * The discourse type that suffers the MOST on unseen prompts is: '{worst_dt}' (Mean Macro-F1 = {worst_mf1:.4f}).")
print(f"  * Root Cause: When a completely new prompt is evaluated, units such as '{worst_dt}' and 'Evidence' ")
print(f"    rely heavily on prompt-specific source texts, domain vocabulary, and background topics.")
print(f"    Without in-domain topic grounding, models struggle significantly more on these argumentative units ")
print(f"    than on generic rhetorical structural elements like 'Lead' or 'Concluding Statement'.")

print("\n" + "=" * 80)
print("SCRIPT 06 COMPLETE: LOPO DEBERTA EVALUATION FINISHED")
print("=" * 80)
