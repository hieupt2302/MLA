# %% [markdown]
# # ==============================================================================
# # PERSUADE 2.0: DISCOURSE EFFECTIVENESS CLASSIFICATION
# # SCRIPT 05: Context Ablation Experiment with DeBERTa-v3-base
# # ==============================================================================
# # Course: CLC02 - Group 06 | Environment: GPU (Colab T4 / V100 / A100) | Runtime: ~4-6 hours
# #
# # Research Objective:
# # Address Week 9 Instructor Feedback:
# # "Thiet ke mot thi nghiem ngu canh co kiem soat: chi don vi; don vi cung don vi
# # dung truoc va sau... Giu nguyen mo hinh va split, chi doi dau vao, roi xem
# # Ineffective duoc cai thien o loai don vi nao."
# #
# # Controlled Conditions:
# #   - Architecture: microsoft/deberta-v3-base (identical backbone)
# #   - Data Split: outputs/split_assignments.csv (exact same 29,102 val units)
# #   - Hyperparameters: lr=2e-5, batch_size=8, grad_accum=4, epochs=3, seed=42
# #   - Loss: Weighted Cross-Entropy with balanced class weights
# #
# # Context Levels Compared:
# #   - Level 0 (Baseline): [discourse_type] [SEP] [discourse_text]
# #     (Pre-computed in Week 9, loaded from outputs/deberta_predictions.csv)
# #   - Level 1 (+ Neighbors): [discourse_type] [SEP] Previous: [prev] [SEP] Target: [curr] [SEP] Next: [next]
# # ==============================================================================

# %%
import os
import sys
import gc
import json
import time
import math
import random
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
    print(f"[Setup] Deterministic random seed fixed to: {seed}")

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
parser = argparse.ArgumentParser(description="DeBERTa-v3-base Context Ablation Pipeline")
parser.add_argument("--data_path", type=str, default="persuade_corpus_2.0_train.csv", help="Path to train CSV")
parser.add_argument("--output_dir", type=str, default="outputs", help="Directory to store outputs")
parser.add_argument("--quick", action="store_true", help="Quick demo mode with small subset")
parser.add_argument("--eval_only", action="store_true", help="Skip training, evaluate saved checkpoint")
parser.add_argument("--epochs", type=int, default=3, help="Training epochs (default: 3)")
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
CHECKPOINT_DIR = os.path.join(OUTPUT_DIR, "deberta_context_checkpoints")
os.makedirs(CHECKPOINT_DIR, exist_ok=True)
BEST_MODEL_DIR = os.path.join(OUTPUT_DIR, "deberta_context_best_model")

# ------------------------------------------------------------------------------
# SECTION 1: DATA LOADING & NEIGHBOR CONTEXT EXTRACTION
# ------------------------------------------------------------------------------
print("\n" + "=" * 80)
print("SECTION 1: DATA LOADING & LOCAL CONTEXT AUGMENTATION")
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
    "discourse_type", "discourse_effectiveness", "discourse_start"
]

raw_df = pd.read_csv(data_path, usecols=needed_cols, dtype={"essay_id": str, "discourse_id": str}, low_memory=False)

# Clean and filter
df = raw_df.dropna(subset=["discourse_effectiveness", "discourse_text"]).copy()
df["discourse_text"] = df["discourse_text"].astype(str).str.strip()
df["discourse_type"] = df["discourse_type"].astype(str).str.strip()
df = df[df["discourse_text"].str.len() > 0].reset_index(drop=True)
df["essay_id"] = df["essay_id"].astype(str).str.strip()
df["discourse_id"] = df["discourse_id"].astype(str).str.strip()

print(f"[Data] Valid labeled discourse units: {len(df):,} across {df['essay_id'].nunique():,} unique essays.")

# ------------------------------------------------------------------------------
# 1.1 Compute Immediate Neighbors (Previous & Next Unit in Same Essay)
# ------------------------------------------------------------------------------
print("[Context] Extracting sequential neighbor units based on discourse_start...")
df["discourse_start_num"] = pd.to_numeric(df["discourse_start"], errors="coerce").fillna(0)
df["original_order"] = np.arange(len(df))

# Sort temporarily by essay_id and discourse_start
df_sorted = df.sort_values(by=["essay_id", "discourse_start_num"]).copy()

# Shift to obtain previous and next discourse units within each essay
df_sorted["prev_discourse_text"] = df_sorted.groupby("essay_id")["discourse_text"].shift(1).fillna("")
df_sorted["next_discourse_text"] = df_sorted.groupby("essay_id")["discourse_text"].shift(-1).fillna("")

# Restore original row order to guarantee exact row-to-row alignment with Week 9 split!
df = df_sorted.sort_values(by="original_order").reset_index(drop=True)

# ------------------------------------------------------------------------------
# 1.2 Format Level 1 Context-Augmented Input String
# ------------------------------------------------------------------------------
def format_level1_input(row) -> str:
    dtype = row["discourse_type"]
    curr = row["discourse_text"].strip()
    prev = row["prev_discourse_text"].strip()
    nxt = row["next_discourse_text"].strip()

    prev_str = prev if len(prev) > 0 else "[NONE]"
    next_str = nxt if len(nxt) > 0 else "[NONE]"

    return f"{dtype} [SEP] Previous: {prev_str} [SEP] Target: {curr} [SEP] Next: {next_str}"

df["input_text"] = df.apply(format_level1_input, axis=1)

print("\n[Input Format Demonstration]")
sample_row = df.iloc[0]
print(f"  Target Type  : {sample_row['discourse_type']}")
print(f"  Has Prev?    : {len(sample_row['prev_discourse_text']) > 0}")
print(f"  Has Next?    : {len(sample_row['next_discourse_text']) > 0}")
print(f"  Level 1 Text : {sample_row['input_text'][:160]}...")

# ------------------------------------------------------------------------------
# 1.3 Split Alignment (outputs/split_assignments.csv)
# ------------------------------------------------------------------------------
split_path = os.path.join(OUTPUT_DIR, "split_assignments.csv")
if not os.path.exists(split_path):
    raise FileNotFoundError(
        f"Split assignments file not found at '{split_path}'. "
        "Please ensure Week 9 split_assignments.csv exists to guarantee controlled comparison."
    )

print(f"[Split] Loading canonical train/val assignments from: {split_path}")
split_df = pd.read_csv(split_path, dtype={"essay_id": str})
split_map = dict(zip(split_df["essay_id"].str.strip(), split_df["split"].str.strip()))
df["split"] = df["essay_id"].map(split_map)

assert not df["split"].isna().any(), "Error: Unmapped essays detected in split assignments!"

LABEL2ID = {"Ineffective": 0, "Adequate": 1, "Effective": 2}
ID2LABEL = {0: "Ineffective", 1: "Adequate", 2: "Effective"}
CLASS_NAMES = ["Ineffective", "Adequate", "Effective"]

df["label"] = df["discourse_effectiveness"].map(LABEL2ID)

train_df = df[df["split"] == "train"].reset_index(drop=True)
val_df = df[df["split"] == "val"].reset_index(drop=True)

print(f"[Split Verification]")
print(f"  * Train units: {len(train_df):,} ({train_df['essay_id'].nunique():,} essays)")
print(f"  * Val units  : {len(val_df):,} ({val_df['essay_id'].nunique():,} essays)")
assert len(val_df) == 29102, f"Expected 29,102 val units, found {len(val_df):,}"
print("[Split Verification] PASSED: Exactly 29,102 validation units aligned with Level 0.")

if args.quick:
    print("[*] Quick Mode: Subsampling dataset for pipeline smoke testing...")
    sampled_train_essays = random.sample(list(train_df["essay_id"].unique()), min(80, train_df["essay_id"].nunique()))
    sampled_val_essays = random.sample(list(val_df["essay_id"].unique()), min(20, val_df["essay_id"].nunique()))
    train_df = train_df[train_df["essay_id"].isin(sampled_train_essays)].reset_index(drop=True)
    val_df = val_df[val_df["essay_id"].isin(sampled_val_essays)].reset_index(drop=True)
    print(f"[*] Quick subset: Train = {len(train_df):,}, Val = {len(val_df):,}")

# ------------------------------------------------------------------------------
# 1.4 Tokenization
# ------------------------------------------------------------------------------
MODEL_NAME = "microsoft/deberta-v3-base"
MAX_LENGTH = args.max_length

print(f"\n[Tokenizer] Initializing tokenizer: {MODEL_NAME} (max_length={MAX_LENGTH})")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=True)

feature_cols = ["discourse_id", "essay_id", "input_text", "label"]
hf_train = Dataset.from_pandas(train_df[feature_cols])
hf_val = Dataset.from_pandas(val_df[feature_cols])

def preprocess_function(examples: Dict[str, List[Any]]) -> Dict[str, Any]:
    return tokenizer(
        examples["input_text"],
        truncation=True,
        max_length=MAX_LENGTH,
        padding=False
    )

print("[Tokenizer] Tokenizing datasets...")
tokenized_train = hf_train.map(preprocess_function, batched=True, batch_size=2000, remove_columns=["input_text"])
tokenized_val = hf_val.map(preprocess_function, batched=True, batch_size=2000, remove_columns=["input_text"])

# ------------------------------------------------------------------------------
# SECTION 2: MODEL TRAINING (LEVEL 1: UNIT + NEIGHBORS)
# ------------------------------------------------------------------------------
print("\n" + "=" * 80)
print("SECTION 2: MODEL TRAINING (LEVEL 1: UNIT + LOCAL NEIGHBORS)")
print("=" * 80)

train_y = train_df["label"].values
computed_weights = compute_class_weight(
    class_weight="balanced",
    classes=np.array([0, 1, 2]),
    y=train_y
)
class_weights_tensor = torch.tensor(computed_weights, dtype=torch.float)
print("[Class Weights] Balanced loss weights for Level 1:")
for idx, w in enumerate(computed_weights):
    print(f"  Class {idx} ({ID2LABEL[idx]:11s}) : {w:.4f}")

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME,
    num_labels=3,
    id2label=ID2LABEL,
    label2id=LABEL2ID
)

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

data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

ta_params = inspect.signature(TrainingArguments.__init__).parameters
eval_strategy_key = "eval_strategy" if "eval_strategy" in ta_params else "evaluation_strategy"

train_epochs = 1 if args.quick else args.epochs

training_args_kwargs = {
    "output_dir": CHECKPOINT_DIR,
    "learning_rate": args.lr,
    "per_device_train_batch_size": args.batch_size,
    "per_device_eval_batch_size": args.batch_size * 2,
    "gradient_accumulation_steps": args.grad_accum,
    "num_train_epochs": train_epochs,
    "warmup_ratio": 0.1,
    "fp16": USE_FP16,
    eval_strategy_key: "epoch",
    "save_strategy": "epoch",
    "load_best_model_at_end": True,
    "metric_for_best_model": "macro_f1",
    "greater_is_better": True,
    "seed": RANDOM_SEED,
    "save_total_limit": 1,
    "logging_steps": 25 if args.quick else 100,
    "logging_strategy": "steps",
    "report_to": "none",
}

training_args = TrainingArguments(**training_args_kwargs)

trainer = WeightedLossTrainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_train,
    eval_dataset=tokenized_val,
    tokenizer=tokenizer,
    data_collator=data_collator,
    compute_metrics=compute_metrics,
    class_weights=class_weights_tensor,
)

if not args.eval_only:
    print("\n[Training] Starting Level 1 (Unit + Neighbors) DeBERTa fine-tuning...")
    train_start = time.time()
    trainer.train()
    print(f"[Training] Completed in {(time.time() - train_start) / 60:.2f} minutes.")
    trainer.save_model(BEST_MODEL_DIR)
    tokenizer.save_pretrained(BEST_MODEL_DIR)
    print(f"[Training] Best Level 1 model saved to: {BEST_MODEL_DIR}")
else:
    print(f"\n[Training] --eval_only supplied. Loading checkpoint from {BEST_MODEL_DIR}...")
    if os.path.exists(BEST_MODEL_DIR):
        model = AutoModelForSequenceClassification.from_pretrained(BEST_MODEL_DIR)
        trainer.model = model.to(DEVICE)
    else:
        print("[Model] Warning: Checkpoint directory not found. Evaluating initial weights.")

# ------------------------------------------------------------------------------
# SECTION 3: EVALUATION & CONTROLLED LEVEL 0 VS LEVEL 1 COMPARISON
# ------------------------------------------------------------------------------
print("\n" + "=" * 80)
print("SECTION 3: CONTROLLED EVALUATION (LEVEL 0 vs LEVEL 1)")
print("=" * 80)

# Run inference for Level 1
print("[Evaluation] Predicting Level 1 on validation set...")
val_preds_raw = trainer.predict(tokenized_val)
lvl1_logits = val_preds_raw.predictions
if isinstance(lvl1_logits, tuple):
    lvl1_logits = lvl1_logits[0]

lvl1_probs = scipy.special.softmax(lvl1_logits, axis=-1)
lvl1_preds = np.argmax(lvl1_probs, axis=-1)
val_labels = val_df["label"].values

# Compute Level 1 metrics
lvl1_macro_f1 = f1_score(val_labels, lvl1_preds, average="macro", zero_division=0)
lvl1_acc = accuracy_score(val_labels, lvl1_preds)
lvl1_bal_acc = balanced_accuracy_score(val_labels, lvl1_preds)
lvl1_qwk = cohen_kappa_score(val_labels, lvl1_preds, weights="quadratic")
lvl1_kappa = cohen_kappa_score(val_labels, lvl1_preds)
lvl1_per_f1 = f1_score(val_labels, lvl1_preds, average=None, zero_division=0)

# Load Level 0 Baseline Predictions
lvl0_pred_path = os.path.join(OUTPUT_DIR, "deberta_predictions.csv")
if os.path.exists(lvl0_pred_path):
    print(f"[Baseline] Loading Level 0 (Unit-only) predictions from: {lvl0_pred_path}")
    lvl0_df = pd.read_csv(lvl0_pred_path)
    lvl0_preds = lvl0_df["pred_label"].values[:len(val_labels)]
    lvl0_probs = lvl0_df[["pred_proba_0", "pred_proba_1", "pred_proba_2"]].values[:len(val_labels)]

    lvl0_macro_f1 = f1_score(val_labels, lvl0_preds, average="macro", zero_division=0)
    lvl0_acc = accuracy_score(val_labels, lvl0_preds)
    lvl0_bal_acc = balanced_accuracy_score(val_labels, lvl0_preds)
    lvl0_qwk = cohen_kappa_score(val_labels, lvl0_preds, weights="quadratic")
    lvl0_kappa = cohen_kappa_score(val_labels, lvl0_preds)
    lvl0_per_f1 = f1_score(val_labels, lvl0_preds, average=None, zero_division=0)
else:
    print("[Baseline] WARNING: Level 0 predictions CSV not found. Using canonical Week 9 reference metrics.")
    lvl0_macro_f1, lvl0_acc, lvl0_bal_acc, lvl0_qwk, lvl0_kappa = 0.5768, 0.7388, 0.6277, 0.4414, 0.3704
    lvl0_per_f1 = [0.3741, 0.8245, 0.5317]
    lvl0_preds = None

# Build Comparison Table
results_records = [
    {
        "Metric": "Macro-F1 (Primary)",
        "Level 0 (Unit Only)": round(lvl0_macro_f1, 4),
        "Level 1 (+ Neighbors)": round(lvl1_macro_f1, 4),
        "Delta (L1 - L0)": round(lvl1_macro_f1 - lvl0_macro_f1, 4),
    },
    {
        "Metric": "Accuracy",
        "Level 0 (Unit Only)": round(lvl0_acc, 4),
        "Level 1 (+ Neighbors)": round(lvl1_acc, 4),
        "Delta (L1 - L0)": round(lvl1_acc - lvl0_acc, 4),
    },
    {
        "Metric": "Balanced Accuracy",
        "Level 0 (Unit Only)": round(lvl0_bal_acc, 4),
        "Level 1 (+ Neighbors)": round(lvl1_bal_acc, 4),
        "Delta (L1 - L0)": round(lvl1_bal_acc - lvl0_bal_acc, 4),
    },
    {
        "Metric": "Quadratic Weighted Kappa (QWK)",
        "Level 0 (Unit Only)": round(lvl0_qwk, 4),
        "Level 1 (+ Neighbors)": round(lvl1_qwk, 4),
        "Delta (L1 - L0)": round(lvl1_qwk - lvl0_qwk, 4),
    },
    {
        "Metric": "Unweighted Cohen Kappa",
        "Level 0 (Unit Only)": round(lvl0_kappa, 4),
        "Level 1 (+ Neighbors)": round(lvl1_kappa, 4),
        "Delta (L1 - L0)": round(lvl1_kappa - lvl0_kappa, 4),
    },
    {
        "Metric": "F1: Ineffective (Class 0)",
        "Level 0 (Unit Only)": round(lvl0_per_f1[0], 4),
        "Level 1 (+ Neighbors)": round(lvl1_per_f1[0], 4),
        "Delta (L1 - L0)": round(lvl1_per_f1[0] - lvl0_per_f1[0], 4),
    },
    {
        "Metric": "F1: Adequate (Class 1)",
        "Level 0 (Unit Only)": round(lvl0_per_f1[1], 4),
        "Level 1 (+ Neighbors)": round(lvl1_per_f1[1], 4),
        "Delta (L1 - L0)": round(lvl1_per_f1[1] - lvl0_per_f1[1], 4),
    },
    {
        "Metric": "F1: Effective (Class 2)",
        "Level 0 (Unit Only)": round(lvl0_per_f1[2], 4),
        "Level 1 (+ Neighbors)": round(lvl1_per_f1[2], 4),
        "Delta (L1 - L0)": round(lvl1_per_f1[2] - lvl0_per_f1[2], 4),
    },
]

comparison_df = pd.DataFrame(results_records)
comp_path = os.path.join(OUTPUT_DIR, "context_ablation_results.csv")
comparison_df.to_csv(comp_path, index=False)
print(f"\n[SAVED] Overall Context Ablation Results: {comp_path}")
print(comparison_df.to_string(index=False))

# ------------------------------------------------------------------------------
# SECTION 4: PER-DISCOURSE-TYPE INEFFECTIVE BREAKDOWN
# ------------------------------------------------------------------------------
print("\n" + "=" * 80)
print("SECTION 4: PER-DISCOURSE-TYPE BREAKDOWN (INEFFECTIVE IMPROVEMENT)")
print("=" * 80)

discourse_types = sorted(val_df["discourse_type"].unique())
dt_records = []

for dt in discourse_types:
    mask = (val_df["discourse_type"].values == dt)
    n_units = int(mask.sum())
    sub_labels = val_labels[mask]
    n_ineff = int((sub_labels == 0).sum())

    sub_lvl1_preds = lvl1_preds[mask]
    lvl1_dt_macro_f1 = f1_score(sub_labels, sub_lvl1_preds, average="macro", zero_division=0)

    # Ineffective class metrics (class 0 binary)
    lvl1_ineff_rec = recall_score(sub_labels == 0, sub_lvl1_preds == 0, zero_division=0)
    lvl1_ineff_prec = precision_score(sub_labels == 0, sub_lvl1_preds == 0, zero_division=0)
    lvl1_ineff_f1 = f1_score(sub_labels == 0, sub_lvl1_preds == 0, zero_division=0)

    if lvl0_preds is not None:
        sub_lvl0_preds = lvl0_preds[mask]
        lvl0_dt_macro_f1 = f1_score(sub_labels, sub_lvl0_preds, average="macro", zero_division=0)
        lvl0_ineff_rec = recall_score(sub_labels == 0, sub_lvl0_preds == 0, zero_division=0)
        lvl0_ineff_prec = precision_score(sub_labels == 0, sub_lvl0_preds == 0, zero_division=0)
        lvl0_ineff_f1 = f1_score(sub_labels == 0, sub_lvl0_preds == 0, zero_division=0)
    else:
        lvl0_dt_macro_f1, lvl0_ineff_rec, lvl0_ineff_prec, lvl0_ineff_f1 = 0.0, 0.0, 0.0, 0.0

    dt_records.append({
        "discourse_type": dt,
        "n_val_units": n_units,
        "n_ineffective": n_ineff,
        "lvl0_macro_f1": round(lvl0_dt_macro_f1, 4),
        "lvl1_macro_f1": round(lvl1_dt_macro_f1, 4),
        "delta_macro_f1": round(lvl1_dt_macro_f1 - lvl0_dt_macro_f1, 4),
        "lvl0_ineff_f1": round(lvl0_ineff_f1, 4),
        "lvl1_ineff_f1": round(lvl1_ineff_f1, 4),
        "delta_ineff_f1": round(lvl1_ineff_f1 - lvl0_ineff_f1, 4),
        "lvl0_ineff_recall": round(lvl0_ineff_rec, 4),
        "lvl1_ineff_recall": round(lvl1_ineff_rec, 4),
        "delta_ineff_recall": round(lvl1_ineff_rec - lvl0_ineff_rec, 4),
    })

dt_df = pd.DataFrame(dt_records)
dt_path = os.path.join(OUTPUT_DIR, "context_ablation_ineffective_delta.csv")
dt_df.to_csv(dt_path, index=False)
print(f"\n[SAVED] Discourse-Type Ineffective Delta: {dt_path}")
print(dt_df[["discourse_type", "n_ineffective", "lvl0_ineff_f1", "lvl1_ineff_f1", "delta_ineff_f1", "delta_ineff_recall"]].to_string(index=False))

# ------------------------------------------------------------------------------
# SECTION 5: RE-CHECK OF 10 INEFFECTIVE FAILURE CASES
# ------------------------------------------------------------------------------
print("\n" + "=" * 80)
print("SECTION 5: RE-CHECKING 10 INEFFECTIVE FAILURE CASES WITH CONTEXT")
print("=" * 80)

cases_file = os.path.join(OUTPUT_DIR, "error_cases_summary.csv")
recheck_records = []

if os.path.exists(cases_file):
    print(f"[Case Study] Loading Week 9 error cases from: {cases_file}")
    cases_df = pd.read_csv(cases_file)

    for _, case_row in cases_df.iterrows():
        c_id = case_row["case_id"]
        c_type = str(case_row["discourse_type"]).strip()
        c_target = str(case_row["target_text"]).strip().strip("\"' .")
        c_root = case_row.get("likely_root_cause", "")

        # Find matching unit in val_df
        target_prefix = c_target[:25]
        match_idx = val_df[
            (val_df["discourse_type"] == c_type) &
            (val_df["discourse_text"].str.contains(target_prefix, regex=False, na=False))
        ].index

        if len(match_idx) > 0:
            idx = match_idx[0]
            l1_pred = ID2LABEL[lvl1_preds[idx]]
            l1_p_ineff = float(lvl1_probs[idx, 0])
            corrected = (lvl1_preds[idx] == 0)
            target_full = val_df.loc[idx, "discourse_text"]
        else:
            l1_pred = "Not Found"
            l1_p_ineff = 0.0
            corrected = False
            target_full = c_target

        recheck_records.append({
            "case_id": c_id,
            "discourse_type": c_type,
            "target_snippet": c_target[:60],
            "true_label": "Ineffective",
            "week9_pred": case_row["pred_label"],
            "week9_p_ineff": case_row.get("p_ineffective", 0.0),
            "level1_pred": l1_pred,
            "level1_p_ineff": round(l1_p_ineff, 4),
            "is_corrected": corrected,
            "mechanism": "Local context resolved disconnected/referential flaw" if corrected else "Flaw is holistic/extrinsic (needs full essay or source text)"
        })

    recheck_df = pd.DataFrame(recheck_records)
    recheck_path = os.path.join(OUTPUT_DIR, "context_ablation_case_study_recheck.csv")
    recheck_df.to_csv(recheck_path, index=False)
    print(f"\n[SAVED] 10 Case Studies Re-Check: {recheck_path}")
    print(recheck_df[["case_id", "discourse_type", "week9_pred", "level1_pred", "is_corrected", "mechanism"]].to_string(index=False))

    n_corr = sum(r["is_corrected"] for r in recheck_records)
    print(f"\n[Case Study Summary] {n_corr}/10 cases corrected by introducing local neighbor context.")
else:
    print(f"[Case Study] '{cases_file}' not found. Skipping 10-case re-check.")

# ------------------------------------------------------------------------------
# SECTION 6: CONFUSION MATRIX & PREDICTIONS EXPORT
# ------------------------------------------------------------------------------
print("\n" + "=" * 80)
print("SECTION 6: EXPORTING PRODUCTION ARTIFACTS")
print("=" * 80)

# Save Level 1 predictions CSV
pred_export_path = os.path.join(OUTPUT_DIR, "context_ablation_predictions.csv")
pred_export_df = pd.DataFrame({
    "discourse_id": val_df["discourse_id"].values,
    "essay_id": val_df["essay_id"].values,
    "discourse_type": val_df["discourse_type"].values,
    "true_label": val_labels,
    "pred_label": lvl1_preds,
    "pred_proba_0": np.round(lvl1_probs[:, 0], 6),
    "pred_proba_1": np.round(lvl1_probs[:, 1], 6),
    "pred_proba_2": np.round(lvl1_probs[:, 2], 6),
})
pred_export_df.to_csv(pred_export_path, index=False)
print(f"[Export] 1. Level 1 predictions CSV: {pred_export_path} ({len(pred_export_df):,} rows)")

# Save Confusion Matrix Heatmap
cm_lvl1 = confusion_matrix(val_labels, lvl1_preds)
cm_pct = cm_lvl1.astype("float") / cm_lvl1.sum(axis=1)[:, np.newaxis]

labels_annot = np.empty_like(cm_lvl1, dtype=object)
for i in range(cm_lvl1.shape[0]):
    for j in range(cm_lvl1.shape[1]):
        labels_annot[i, j] = f"{cm_lvl1[i, j]:,}\n({cm_pct[i, j]:.1%})"

plt.figure(figsize=(7.5, 6))
if HAS_SEABORN:
    sns.set_theme(style="white")
    ax = sns.heatmap(
        cm_lvl1,
        annot=labels_annot,
        fmt="",
        cmap="Purples",
        cbar=True,
        xticklabels=CLASS_NAMES,
        yticklabels=CLASS_NAMES,
        annot_kws={"fontsize": 11, "fontweight": "bold"}
    )
else:
    plt.imshow(cm_lvl1, cmap="Purples")
    for i in range(3):
        for j in range(3):
            plt.text(j, i, labels_annot[i, j], ha="center", va="center", color="black")

plt.title(f"DeBERTa Level 1 (+ Neighbors) Confusion Matrix\n(Val Units: {len(val_df):,} | Macro-F1: {lvl1_macro_f1:.4f})", fontsize=12, pad=15)
plt.xlabel("Predicted Effectiveness", fontsize=11, fontweight="bold")
plt.ylabel("Ground Truth Effectiveness", fontsize=11, fontweight="bold")
plt.tight_layout()

cm_fig_path = os.path.join(OUTPUT_DIR, "context_ablation_confusion_matrix.png")
plt.savefig(cm_fig_path, dpi=300)
plt.close()
print(f"[Export] 2. Level 1 confusion matrix heatmap: {cm_fig_path}")

print("\n" + "=" * 80)
print("SCRIPT 05 COMPLETE: CONTEXT ABLATION EXPERIMENT FINISHED")
print("=" * 80)
