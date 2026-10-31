"""
Sinh các notebook Colab cho phần mở rộng ngữ cảnh (tuần 11, hướng bổ sung) + LOPO chạy lại.

  08_L1w2_context.ipynb    L1 ±2: 2 đơn vị trước + 2 đơn vị sau (thay vì 1 + 1)
  09_L2_source_text.ipynb  Level 2: L1 + đoạn văn bản nguồn liên quan nhất (4 đề có nguồn)
  10_L3_whole_essay.ipynb  Level 3: cả bài vào mô hình, đánh dấu từng đơn vị, phân loại từng đơn vị
  ../week11_lopo_rerun/11_lopo_rerun_L0.ipynb  LOPO L0 chạy lại (mục B16)

Mọi notebook: cùng split với tuần 9–11 (validation = 29.102 đơn vị, lấy theo row_idx của
val_predictions_L1.csv), chỉ đánh giá trên validation, KHÔNG chấm official test (test đã mở một lần).
Chạy: python week11_context_levels/build_notebooks.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def nb(cells):
    return {
        "cells": [
            {"cell_type": t, "metadata": {}, "source": s.strip("\n").splitlines(keepends=True),
             **({"outputs": [], "execution_count": None} if t == "code" else {})}
            for t, s in cells
        ],
        "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                     "language_info": {"name": "python"}, "accelerator": "GPU"},
        "nbformat": 4, "nbformat_minor": 5,
    }


SETUP = r'''
# ===== 1. MÔI TRƯỜNG =====
# transformers 5.x làm DeBERTa-v3 train hỏng (đã kiểm chứng tuần 11) -> bắt buộc 4.x.
# Trên Colab CLI: `colab install transformers==4.57.6` rồi `colab restart-kernel` trước khi chạy notebook.
import importlib.metadata
TV = importlib.metadata.version("transformers")
assert TV.startswith("4."), f"Cần transformers 4.x, đang có {TV}"

import os, gc, json, time, random, hashlib, math, zipfile, copy
from datetime import datetime, timezone
import numpy as np
import pandas as pd
import requests
import torch
import torch.nn as nn
import transformers
from sklearn.metrics import (accuracy_score, balanced_accuracy_score, cohen_kappa_score, f1_score,
                             precision_score, recall_score)
from sklearn.utils.class_weight import compute_class_weight

torch.backends.cuda.matmul.allow_tf32 = True
torch.backends.cudnn.allow_tf32 = True
QUICK = os.environ.get("QUICK", "0") == "1"      # chạy thử: vài chục bài, 1 epoch — KHÔNG dùng số này
GPU = torch.cuda.get_device_name(0)
USE_BF16 = torch.cuda.is_bf16_supported()
print(f"transformers {TV} | torch {torch.__version__} | {GPU} | bf16={USE_BF16} | QUICK={QUICK}")
print(f"VRAM {torch.cuda.get_device_properties(0).total_memory / 2**30:.1f} GB")
'''

DATA = r'''
# ===== 2. DỮ LIỆU + SPLIT =====
WORK = "/content"
DATA_DIR = f"{WORK}/data"
OUT_DIR = f"{WORK}/out_{KEY}" + ("_QUICK" if QUICK else "")
os.makedirs(DATA_DIR, exist_ok=True); os.makedirs(OUT_DIR, exist_ok=True)
TRAIN_CSV = f"{DATA_DIR}/persuade_corpus_2.0_train.csv"
TRAIN_URL = "https://drive.usercontent.google.com/download?id=13phHyDzIsb0MHyJr6q-B-qIa9P2tM135&export=download&confirm=t"
TRAIN_SHA256 = "f61319edd8bf16a982711ea0399fad59c05afaec05cdf0767f16a2c05c467e23"
LABEL2ID = {"Ineffective": 0, "Adequate": 1, "Effective": 2}
ID2LABEL = {v: k for k, v in LABEL2ID.items()}


def log(msg):
    line = f"[{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC] [{KEY}] {msg}"
    print(line, flush=True)
    with open(f"{OUT_DIR}/run_log.txt", "a", encoding="utf-8") as f:
        f.write(line + "\n")


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 22), b""):
            h.update(block)
    return h.hexdigest()


if not os.path.exists(TRAIN_CSV):
    t0 = time.time()
    with requests.get(TRAIN_URL, stream=True, timeout=120) as r:
        r.raise_for_status()
        with open(TRAIN_CSV + ".part", "wb") as f:
            for block in r.iter_content(chunk_size=1 << 22):
                f.write(block)
    os.replace(TRAIN_CSV + ".part", TRAIN_CSV)
    log(f"Tải train CSV xong sau {time.time() - t0:.0f}s")
assert sha256_of(TRAIN_CSV) == TRAIN_SHA256, "SHA-256 của train CSV không khớp"


def load_units():
    # Cùng quy tắc lọc với notebook 07 -> row_idx trùng với val_predictions_*.csv tuần 11
    cols = ["essay_id_comp", "full_text", "discourse_start", "discourse_end", "discourse_text",
            "discourse_type", "discourse_effectiveness", "prompt_name"]
    df = pd.read_csv(TRAIN_CSV, usecols=cols, dtype=str, low_memory=False)
    df = df.dropna(subset=["discourse_effectiveness", "discourse_text"]).copy()
    for c in ["discourse_text", "discourse_type", "essay_id_comp"]:
        df[c] = df[c].astype(str).str.strip()
    df = df[df["discourse_text"].str.len() > 0].reset_index(drop=True)
    df["row_idx"] = np.arange(len(df))
    df["prompt_name"] = df["prompt_name"].fillna("").str.replace('"', "", regex=False).str.strip()
    df["label"] = df["discourse_effectiveness"].map(LABEL2ID).astype(int)
    df["start"] = pd.to_numeric(df["discourse_start"], errors="coerce").fillna(0).astype(int)
    df["end"] = pd.to_numeric(df["discourse_end"], errors="coerce").fillna(0).astype(int)
    # Đơn vị trước/sau trong cùng bài (theo essay_id_comp, sắp theo vị trí) — như notebook 07
    s = df.sort_values(["essay_id_comp", "start", "row_idx"], kind="mergesort")
    g = s.groupby("essay_id_comp")["discourse_text"]
    for k in (1, 2):
        s[f"prev{k}"] = g.shift(k).fillna("")
        s[f"next{k}"] = g.shift(-k).fillna("")
    return s.sort_values("row_idx").reset_index(drop=True)


units = load_units()
assert len(units) == 144289, len(units)
REF = pd.read_csv(f"{WORK}/val_predictions_L1.csv")          # dự đoán L1 tuần 11 trên validation
REF_L0 = pd.read_csv(f"{WORK}/val_predictions_L0.csv")
units["split"] = np.where(units["row_idx"].isin(set(REF["row_idx"])), "val", "train")
assert units.groupby("essay_id_comp")["split"].nunique().max() == 1, "Một bài nằm ở cả train và val"
train_df = units[units["split"] == "train"].reset_index(drop=True)
val_df = units[units["split"] == "val"].reset_index(drop=True)
assert len(train_df) == 115187 and len(val_df) == 29102
assert (val_df["row_idx"].values == REF["row_idx"].values).all()
assert (val_df["label"].values == REF["true_label"].values).all()
log(f"Train {len(train_df):,} đơn vị / {train_df.essay_id_comp.nunique():,} bài | "
    f"Val {len(val_df):,} đơn vị / {val_df.essay_id_comp.nunique():,} bài (khớp split tuần 9–11)")

FULL_VAL = val_df  # giữ bản đầy đủ để so sánh
if QUICK:
    rng = np.random.RandomState(0)
    pick = lambda d, k: d[d.essay_id_comp.isin(rng.choice(d.essay_id_comp.unique(), k, replace=False))]
    train_df = pick(train_df, 80).reset_index(drop=True)
    val_df = pick(val_df, 30).reset_index(drop=True)
    log(f"QUICK: train {len(train_df)} / val {len(val_df)} đơn vị")
'''

EVAL = r'''
# ===== 3. HÀM ĐÁNH GIÁ =====
def metrics_dict(y, pred):
    f1c = f1_score(y, pred, labels=[0, 1, 2], average=None, zero_division=0)
    return {"macro_f1": f1_score(y, pred, labels=[0, 1, 2], average="macro", zero_division=0),
            "accuracy": accuracy_score(y, pred), "balanced_accuracy": balanced_accuracy_score(y, pred),
            "qwk": cohen_kappa_score(y, pred, weights="quadratic"),
            "f1_ineffective": f1c[0], "f1_adequate": f1c[1], "f1_effective": f1c[2],
            "recall_ineffective": recall_score(y == 0, pred == 0, zero_division=0),
            "precision_ineffective": precision_score(y == 0, pred == 0, zero_division=0)}


def macro(y, p):
    return f1_score(y, p, labels=[0, 1, 2], average="macro", zero_division=0)


def paired_bootstrap(essays, y, base, new, n_boot=2000, seed=42):
    """Δ Macro-F1 (new − base), lấy mẫu lại theo bài."""
    codes = pd.Series(essays).astype("category").cat.codes.values
    members = [np.flatnonzero(codes == k) for k in range(codes.max() + 1)]
    rng = np.random.default_rng(seed)
    d = []
    for _ in range(n_boot):
        idx = np.concatenate([members[k] for k in rng.integers(0, len(members), len(members))])
        d.append(macro(y[idx], new[idx]) - macro(y[idx], base[idx]))
    d = np.array(d)
    return {"delta": round(macro(y, new) - macro(y, base), 4), "ci_low": round(np.percentile(d, 2.5), 4),
            "ci_high": round(np.percentile(d, 97.5), 4), "p_one_sided_le0": round(float((d <= 0).mean()), 4),
            "n_units": len(y), "n_essays": len(members), "n_boot": n_boot}


def save_predictions(probs, name):
    out = val_df[["row_idx", "essay_id_comp", "discourse_type", "prompt_name"]].copy()
    out["true_label"] = val_df["label"].values
    out["pred_label"] = probs.argmax(1)
    for c in range(3):
        out[f"pred_proba_{c}"] = np.round(probs[:, c], 6)
    path = f"{OUT_DIR}/val_predictions_{name}.csv"
    out.to_csv(path, index=False)
    log(f"Lưu {path}")
    return out


def compare_with_reference(pred, name, subsets=None):
    """So với L0 / L1 tuần 11 trên CÙNG đơn vị validation, bootstrap theo bài."""
    ref1 = REF.set_index("row_idx").loc[val_df["row_idx"], "pred_label"].values
    ref0 = REF_L0.set_index("row_idx").loc[val_df["row_idx"], "pred_label"].values
    y, ess = val_df["label"].values, val_df["essay_id_comp"].values
    subsets = subsets or {"all": np.ones(len(y), bool)}
    rows = []
    for sname, m in subsets.items():
        if m.sum() == 0:
            continue
        for bname, base in [("L1 (tuần 11)", ref1), ("L0 (tuần 11)", ref0)]:
            r = paired_bootstrap(ess[m], y[m], base[m], pred[m], n_boot=200 if QUICK else 2000)
            rows.append({"model": name, "subset": sname, "baseline": bname,
                         "macro_f1_model": round(macro(y[m], pred[m]), 4),
                         "macro_f1_baseline": round(macro(y[m], base[m]), 4), **r})
    df = pd.DataFrame(rows)
    df.to_csv(f"{OUT_DIR}/compare_{name}_vs_L0_L1.csv", index=False)
    print(df.to_string(index=False))
    return df
'''

HF_TRAIN = r'''
# ===== 4. TRAIN (cùng công thức L0/L1/PA tuần 11: deberta-v3-base, lr 2e-5, 3 epoch, warmup 0.1,
#           batch hiệu dụng 32, class weight balanced, chọn epoch tốt nhất theo Macro-F1 validation) =====
from datasets import Dataset
from transformers import (AutoModelForSequenceClassification, AutoTokenizer, DataCollatorWithPadding, Trainer,
                          TrainingArguments, set_seed)

CFG = dict(model_name="microsoft/deberta-v3-base", max_length=512, eff_batch=32, lr=2e-5, epochs=3,
           warmup_ratio=0.1, seed=42)
if QUICK:
    CFG.update(epochs=1)


def seed_all(seed):
    random.seed(seed); np.random.seed(seed); os.environ["PYTHONHASHSEED"] = str(seed)
    torch.manual_seed(seed); torch.cuda.manual_seed_all(seed); set_seed(seed)


class WeightedLossTrainer(Trainer):
    def __init__(self, *args, class_weights=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.class_weights = class_weights

    def compute_loss(self, model, inputs, return_outputs=False, **kwargs):
        labels = inputs["labels"]
        outputs = model(**{k: v for k, v in inputs.items() if k != "labels"})
        logits = outputs.logits
        loss = nn.CrossEntropyLoss(weight=self.class_weights.to(logits.device, logits.dtype))(
            logits.view(-1, 3), labels.view(-1))
        return (loss, outputs) if return_outputs else loss


def hf_metrics(eval_pred):
    logits, labels = eval_pred
    logits = logits[0] if isinstance(logits, tuple) else logits
    m = metrics_dict(labels, np.argmax(logits, -1))
    return {"macro_f1": m["macro_f1"], "accuracy": m["accuracy"], "f1_ineffective": m["f1_ineffective"]}


def pick_batch(model, effective, max_len):
    """Batch GPU lớn nhất (ước của batch hiệu dụng) vừa VRAM ở max_len; batch hiệu dụng giữ nguyên."""
    dtype = torch.bfloat16 if USE_BF16 else torch.float16
    total = torch.cuda.get_device_properties(0).total_memory
    for bs in (32, 16, 8):
        if effective % bs:
            continue
        try:
            torch.cuda.empty_cache(); torch.cuda.reset_peak_memory_stats()
            ids = torch.randint(5, 1000, (bs, max_len), device="cuda")
            with torch.autocast("cuda", dtype=dtype):
                model(input_ids=ids, attention_mask=torch.ones_like(ids)).logits.float().sum().backward()
            model.zero_grad(set_to_none=True)
            peak = torch.cuda.max_memory_allocated()
            log(f"Thử batch {bs} x {max_len}: đỉnh VRAM {peak / 2**30:.1f}/{total / 2**30:.1f} GB")
            if peak < 0.85 * total:
                return bs, effective // bs
        except torch.cuda.OutOfMemoryError:
            log(f"Batch {bs} tràn VRAM")
        model.zero_grad(set_to_none=True); torch.cuda.empty_cache()
    return 8, effective // 8


def truncation_report(tok, texts, target_texts, name):
    """Tỷ lệ đầu vào bị cắt ở max_length và tỷ lệ phần Target bị cắt mất."""
    n = len(texts)
    ids = tok(list(texts), truncation=False, add_special_tokens=True)["input_ids"]
    lens = np.array([len(x) for x in ids])
    over = lens > CFG["max_length"]
    # Target bị cắt nếu phần trước Target + Target đã vượt max_length
    cut_target = 0
    for t, tgt, o in zip(texts, target_texts, over):
        if o:
            head = t[: t.find(tgt) + len(tgt)] if tgt in t else t
            cut_target += len(tok(head)["input_ids"]) > CFG["max_length"]
    log(f"[{name}] độ dài token p50/p90/p99 = {np.percentile(lens, [50, 90, 99]).round().tolist()} | "
        f"bị cắt {over.mean():.2%} | Target bị cắt {cut_target / n:.2%}")


def train_and_predict(text_col, name):
    seed_all(CFG["seed"])
    tok = AutoTokenizer.from_pretrained(CFG["model_name"], use_fast=True)
    truncation_report(tok, val_df[text_col].values, val_df["discourse_text"].values, name)

    def to_hf(d):
        ds = Dataset.from_pandas(d[[text_col, "label"]].rename(columns={text_col: "text", "label": "labels"}),
                                 preserve_index=False)
        ds = ds.map(lambda b: tok(b["text"], truncation=True, max_length=CFG["max_length"]),
                    batched=True, batch_size=2000, remove_columns=["text"])
        return ds.map(lambda b: {"length": [len(x) for x in b["input_ids"]]}, batched=True)

    hf_train, hf_val = to_hf(train_df), to_hf(val_df)
    weights = compute_class_weight("balanced", classes=np.array([0, 1, 2]), y=train_df["label"].values)
    model = AutoModelForSequenceClassification.from_pretrained(
        CFG["model_name"], num_labels=3, id2label=ID2LABEL, label2id=LABEL2ID).cuda()
    per_dev, accum = pick_batch(model, CFG["eff_batch"], CFG["max_length"])
    log(f"[{name}] batch GPU {per_dev} x grad_accum {accum} = {per_dev * accum} | class weights {np.round(weights, 4).tolist()}")
    args = TrainingArguments(
        output_dir=f"{WORK}/ckpt_{name}", learning_rate=CFG["lr"],
        per_device_train_batch_size=per_dev, per_device_eval_batch_size=128,
        gradient_accumulation_steps=accum, num_train_epochs=CFG["epochs"], warmup_ratio=CFG["warmup_ratio"],
        bf16=USE_BF16, fp16=not USE_BF16, tf32=True,
        group_by_length=True, length_column_name="length", dataloader_num_workers=4,
        eval_strategy="epoch", save_strategy="epoch", load_best_model_at_end=True,
        metric_for_best_model="macro_f1", greater_is_better=True, save_total_limit=1,
        seed=CFG["seed"], logging_steps=10 if QUICK else 200, report_to="none")
    trainer = WeightedLossTrainer(model=model, args=args, train_dataset=hf_train, eval_dataset=hf_val,
                                  data_collator=DataCollatorWithPadding(tok), processing_class=tok,
                                  compute_metrics=hf_metrics, class_weights=torch.tensor(weights, dtype=torch.float))
    t0 = time.time()
    trainer.train()
    minutes = (time.time() - t0) / 60
    hist = [h for h in trainer.state.log_history if "eval_macro_f1" in h]
    for h in hist:
        log(f"[{name}] epoch {h['epoch']:.0f}: val Macro-F1 {h['eval_macro_f1']:.4f} | F1 Ineff {h['eval_f1_ineffective']:.4f}")
    log(f"[{name}] train xong sau {minutes:.1f} phút | best val Macro-F1 {trainer.state.best_metric:.4f}")
    # transformers 4.57: khi group_by_length=True, predict() cũng dùng LengthGroupedSampler -> thứ tự dự đoán bị xáo.
    # Ép suy luận theo đúng thứ tự dataset, rồi kiểm tra nhãn trả về khớp từng dòng với val_df.
    from torch.utils.data import SequentialSampler
    trainer._get_eval_sampler = lambda ds, *a, **k: SequentialSampler(ds)
    pred_out = trainer.predict(hf_val)
    assert (pred_out.label_ids == val_df["label"].values).all(), "Thứ tự dự đoán lệch với val_df"
    logits = pred_out.predictions
    logits = logits[0] if isinstance(logits, tuple) else logits
    probs = torch.softmax(torch.tensor(logits, dtype=torch.float32), -1).numpy()
    # Lúc train, đánh giá gom batch theo độ dài; ở đây batch tuần tự -> padding khác -> bf16 lệch rất nhỏ, vài đơn vị đổi argmax.
    # Lệch thứ tự thật (lỗi B28) làm Macro-F1 tụt ~0,25, nên dung sai 0,005 vẫn bắt được lỗi đó.
    gap = metrics_dict(val_df["label"].values, probs.argmax(1))["macro_f1"] - trainer.state.best_metric
    log(f"[{name}] Macro-F1 dự đoán cuối − best_metric lúc train = {gap:+.5f}")
    assert abs(gap) < 0.005, f"Macro-F1 của dự đoán cuối lệch best_metric {gap:+.4f}"
    json.dump({"name": name, "cfg": CFG, "batch_gpu": per_dev, "grad_accum": accum, "train_minutes": round(minutes, 1),
               "epoch_evals": hist, "best_metric": trainer.state.best_metric, "gpu": GPU, "transformers": TV,
               "class_weights": weights.tolist(), "quick": QUICK},
              open(f"{OUT_DIR}/train_history_{name}.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    del trainer, model
    gc.collect(); torch.cuda.empty_cache()
    import shutil; shutil.rmtree(f"{WORK}/ckpt_{name}", ignore_errors=True)
    return probs
'''

FINISH = r'''
# ===== XUẤT KẾT QUẢ =====
m = metrics_dict(val_df["label"].values, PROBS.argmax(1))
summary = {"model": KEY, **{k: round(float(v), 4) for k, v in m.items()}, "n_val_units": len(val_df),
           "quick": QUICK, "gpu": GPU, "transformers": TV, "finished_at": datetime.now(timezone.utc).isoformat()}
json.dump(summary, open(f"{OUT_DIR}/summary_{KEY}.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
log(f"KẾT QUẢ {KEY} (validation): " + " | ".join(f"{k} {v}" for k, v in summary.items() if isinstance(v, float)))
bundle = f"{WORK}/results_{KEY}" + ("_QUICK" if QUICK else "") + ".zip"
with zipfile.ZipFile(bundle, "w", zipfile.ZIP_DEFLATED) as zf:
    for fn in sorted(os.listdir(OUT_DIR)):
        zf.write(f"{OUT_DIR}/{fn}", f"{os.path.basename(OUT_DIR)}/{fn}")
print("Đã đóng gói:", bundle, os.path.getsize(bundle), "bytes")
'''

# ---------------------------------------------------------------- L1 ±2
L1W2_INTRO = r'''
# Notebook 08 — L1 ±2: ngữ cảnh 2 đơn vị trước + 2 đơn vị sau (tuần 11, hướng bổ sung)

**Câu hỏi:** L1 (1 đơn vị trước + 1 sau) cho mức tăng nhỏ so với L0. Mở rộng cửa sổ lên ±2 đơn vị có tăng thêm không?

**Đầu vào:** `type [SEP] Previous 2: … [SEP] Previous: … [SEP] Target: … [SEP] Next: … [SEP] Next 2: …`
Mỗi đoạn ngữ cảnh được cắt tối đa 600 ký tự (~130 token) để phần Target không bị đẩy ra ngoài giới hạn 512 token;
notebook in tỷ lệ đầu vào/Target bị cắt.

**Giữ nguyên so với L1 tuần 11:** mô hình, siêu tham số, split, cách chọn epoch (Macro-F1 validation).
Chỉ đánh giá trên validation (29.102 đơn vị); so với L1/L0 tuần 11 trên cùng đơn vị, bootstrap theo bài.
**Không chấm official test.**

Tốc độ (không đổi công thức): batch GPU lớn nhất vừa VRAM × grad_accum = 32, group_by_length, bf16, TF32.
'''

L1W2_BUILD = r'''
# ===== 3b. DỰNG ĐẦU VÀO L1 ±2 =====
CAP = 600


def cap(s):
    return s if len(s) <= CAP else s[:CAP].rsplit(" ", 1)[0]


def none(s):
    return s if s else "[NONE]"


for d in (train_df, val_df):
    d["text_L1w2"] = (d["discourse_type"] + " [SEP] Previous 2: " + d["prev2"].map(cap).map(none)
                      + " [SEP] Previous: " + d["prev1"].map(cap).map(none)
                      + " [SEP] Target: " + d["discourse_text"]
                      + " [SEP] Next: " + d["next1"].map(cap).map(none)
                      + " [SEP] Next 2: " + d["next2"].map(cap).map(none))
print(val_df["text_L1w2"].iloc[3][:700])
'''

L1W2_RUN = r'''
PROBS = train_and_predict("text_L1w2", KEY)
save_predictions(PROBS, KEY)
CMP = compare_with_reference(PROBS.argmax(1), KEY)
'''

# ---------------------------------------------------------------- L1 cả đoạn
PARA_INTRO = r'''
# Notebook 12 — L1-para: đơn vị cùng toàn bộ đoạn văn chứa nó (tuần 11, hướng bổ sung)

**Nguồn ý tưởng:** nhận xét tuần 9 của thầy đề xuất thang ngữ cảnh "chỉ đơn vị; đơn vị cùng đơn vị đứng trước và sau;
**đơn vị cùng toàn bộ đoạn**; đơn vị cùng đề bài". Notebook này làm mức "toàn bộ đoạn".

**Đoạn văn:** `full_text` được tách đoạn ở các dấu xuống dòng; đoạn chứa đơn vị là đoạn chứa vị trí `discourse_start`.
Trung bình mỗi đoạn có 2,45 đơn vị (trung vị 2); 12% đơn vị đứng một mình trong đoạn.

**Đầu vào:** `type [SEP] Target: <đơn vị> [SEP] Paragraph: <đoạn, đơn vị đích được bao bởi « … »>`.
Target đặt trước để không bao giờ bị cắt; đoạn dài hơn 2.000 ký tự được cắt quanh đơn vị (±1.000 ký tự).

Cùng mô hình, siêu tham số, split và cách chọn epoch như L1. Chỉ validation; so với L1/L0 tuần 11 trên cùng đơn vị.
**Không chấm official test.**
'''

PARA_BUILD = r'''
# ===== 3b. DỰNG ĐẦU VÀO L1-para =====
import re, bisect
BREAK = re.compile(r"\n+")


def paragraph_of(ft, s, e):
    """Đoạn chứa vị trí s; đơn vị đích [s, e) được bao bởi « »."""
    breaks = list(BREAK.finditer(ft))
    starts = [0] + [m.end() for m in breaks]
    ends = [m.start() for m in breaks] + [len(ft)]
    i = max(0, bisect.bisect_right(starts, s) - 1)       # đoạn cuối cùng bắt đầu trước s
    a, b = starts[i], max(ends[i], min(e, len(ft)))      # đơn vị vắt qua dấu xuống dòng: kéo dài tới hết đơn vị
    lo, hi = a, b
    if hi - lo > 2000:                       # đoạn quá dài: giữ ±1.000 ký tự quanh đơn vị
        lo, hi = max(a, s - 1000), min(b, e + 1000)
    return (ft[lo:s] + " « " + ft[s:min(e, hi)] + " » " + ft[min(e, hi):hi]).strip()


for d in (train_df, val_df):
    paras = [paragraph_of(ft, s, e) for ft, s, e in zip(d["full_text"], d["start"], d["end"])]
    d["text_L1para"] = d["discourse_type"] + " [SEP] Target: " + d["discourse_text"] + " [SEP] Paragraph: " + pd.Series(paras, index=d.index)
    log(f"{'train' if d is train_df else 'val'}: số từ của đoạn p50/p90 = "
        f"{np.percentile([len(p.split()) for p in paras], [50, 90]).round().tolist()}")
print(val_df["text_L1para"].iloc[3][:900])
'''

PARA_RUN = r'''
PROBS = train_and_predict("text_L1para", KEY)
save_predictions(PROBS, KEY)
CMP = compare_with_reference(PROBS.argmax(1), KEY)
'''

# ---------------------------------------------------------------- L2
L2_INTRO = r'''
# Notebook 09 — Level 2: thêm văn bản nguồn (tuần 11, hướng bổ sung)

**Câu hỏi:** với đề dựa vào bài đọc, đưa đoạn bài đọc liên quan vào đầu vào có giúp mô hình đánh giá đơn vị (nhất là Evidence) tốt hơn L1 không?

**Nguồn có được** (CSV PERSUADE chỉ có *tên* bài đọc):
- Toàn văn: *Car-free cities*, *Does the electoral college work?* — `train_prompts.csv` của cuộc thi Kaggle LLM-Detect AI Generated Text.
- Chỉ có bản tóm tắt ~100 từ do GPT-4 viết: *The Face on Mars*, *A Cowboy Who Rode the Waves* — `sources.csv` của bộ Kaggle nbroad/persaude-corpus-2.
- Không có: *Exploring Venus*, *Facial action coding system*, *Driverless cars* và 8 đề độc lập → đầu vào giữ y hệt L1.

**Đầu vào:** `type [SEP] Source: <đoạn nguồn> [SEP] Previous: … [SEP] Target: … [SEP] Next: …`
Đoạn nguồn = đoạn bài đọc có độ tương đồng TF-IDF cao nhất với đơn vị (đề có toàn văn) hoặc bản tóm tắt (đề chỉ có tóm tắt), cắt tối đa 90 từ.

**Đánh giá:** chỉ validation. So với L1 tuần 11 trên cùng đơn vị, tách theo nhóm đề (toàn văn / tóm tắt / không có nguồn).
Nhóm *không có nguồn* có đầu vào giống L1, nên chênh lệch ở đó cho biết dao động giữa hai lần train;
hiệu ứng của nguồn = (chênh ở đề có nguồn) − (chênh ở đề không có nguồn). **Không chấm official test.**
'''

L2_BUILD = r'''
# ===== 3b. DỰNG ĐẦU VÀO LEVEL 2 =====
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

SOURCES = json.load(open(f"{WORK}/source_texts.json", encoding="utf-8"))
for p, v in SOURCES.items():
    log(f"Nguồn: {p} | {v['kind']} | {len(v['paragraphs'])} đoạn | {v['origin']}")
SRC_WORDS = 90


def cap_words(s, n=SRC_WORDS):
    w = s.split()
    return " ".join(w[:n])


def source_snippets(d):
    snip = pd.Series("", index=d.index)
    for p, v in SOURCES.items():
        m = (d["prompt_name"] == p).values
        if not m.any():
            continue
        paras = v["paragraphs"]
        if v["kind"] == "full_text":
            vec = TfidfVectorizer(stop_words="english", sublinear_tf=True).fit(paras)
            sim = linear_kernel(vec.transform(d.loc[m, "discourse_text"]), vec.transform(paras))
            snip[m] = [cap_words(paras[i]) for i in sim.argmax(1)]
        else:
            snip[m] = cap_words(" ".join(paras))
    return snip


def none(s):
    return s if s else "[NONE]"


for d in (train_df, val_df):
    d["source_snippet"] = source_snippets(d)
    l1 = (" [SEP] Previous: " + d["prev1"].map(none) + " [SEP] Target: " + d["discourse_text"]
          + " [SEP] Next: " + d["next1"].map(none))
    has = d["source_snippet"].str.len() > 0
    d["text_L2"] = np.where(has, d["discourse_type"] + " [SEP] Source: " + d["source_snippet"] + l1,
                            d["discourse_type"] + l1)
    log(f"{'train' if d is train_df else 'val'}: {has.mean():.1%} đơn vị có đoạn nguồn")
KIND = {p: v["kind"] for p, v in SOURCES.items()}
val_df["source_kind"] = val_df["prompt_name"].map(KIND).fillna("none")
print(val_df.groupby("source_kind").size())
ex = val_df[val_df.source_kind == "full_text"].iloc[0]
print(ex["text_L2"][:900])
'''

L2_RUN = r'''
PROBS = train_and_predict("text_L2", KEY)
save_predictions(PROBS, KEY)
k = val_df["source_kind"].values
CMP = compare_with_reference(PROBS.argmax(1), KEY, subsets={
    "all": np.ones(len(k), bool),
    "source: full text (2 đề)": k == "full_text",
    "source: GPT-4 summary (2 đề)": k == "gpt4_summary",
    "source: any (4 đề)": k != "none",
    "no source (11 đề, đầu vào = L1)": k == "none",
})
# Hiệu ứng của nguồn = chênh (L2 − L1) ở đề có nguồn − chênh ở đề không có nguồn, bootstrap theo bài
ref1 = REF.set_index("row_idx").loc[val_df["row_idx"], "pred_label"].values
y, ess, pred = val_df["label"].values, val_df["essay_id_comp"].values, PROBS.argmax(1)
src, nos = k != "none", k == "none"
codes = pd.Series(ess).astype("category").cat.codes.values
members = [np.flatnonzero(codes == c) for c in range(codes.max() + 1)]
rng = np.random.default_rng(7); dd = []
for _ in range(200 if QUICK else 2000):
    idx = np.concatenate([members[c] for c in rng.integers(0, len(members), len(members))])
    a, b = idx[src[idx]], idx[nos[idx]]
    dd.append((macro(y[a], pred[a]) - macro(y[a], ref1[a])) - (macro(y[b], pred[b]) - macro(y[b], ref1[b])))
did = {"did_source_effect": round((macro(y[src], pred[src]) - macro(y[src], ref1[src]))
                                  - (macro(y[nos], pred[nos]) - macro(y[nos], ref1[nos])), 4),
       "ci_low": round(np.percentile(dd, 2.5), 4), "ci_high": round(np.percentile(dd, 97.5), 4)}
json.dump(did, open(f"{OUT_DIR}/source_effect_diff_in_diff.json", "w"), indent=2)
log(f"Hiệu ứng nguồn (diff-in-diff vs L1): {did}")
# Theo loại đơn vị trên đề có nguồn (Evidence là nơi giả thuyết dự đoán có tác dụng)
rows = []
for t in sorted(val_df.discourse_type.unique()):
    m = src & (val_df.discourse_type.values == t)
    rows.append({"discourse_type": t, "n": int(m.sum()), "L2": round(macro(y[m], pred[m]), 4),
                 "L1": round(macro(y[m], ref1[m]), 4), "delta": round(macro(y[m], pred[m]) - macro(y[m], ref1[m]), 4)})
by_type = pd.DataFrame(rows); by_type.to_csv(f"{OUT_DIR}/L2_vs_L1_by_type_source_prompts.csv", index=False)
print(by_type.to_string(index=False))
'''

# ---------------------------------------------------------------- L3
L3_INTRO = r'''
# Notebook 10 — Level 3: cả bài vào mô hình (tuần 11, hướng bổ sung / dự phòng báo cáo)

**Câu hỏi:** mục 8 của báo cáo cho rằng các lỗi Ineffective "tự tin cao" cần thông tin ở mức toàn bài
(counterclaim không được phản bác, position trơ trọi…). Cho mô hình đọc cả bài thì có tốt hơn L1 không?

**Kiến trúc:** toàn văn bài (`full_text`) được chèn token đánh dấu quanh mỗi đơn vị có nhãn, theo loại:
`[CLAIM] … [/CLAIM]`, `[EVIDENCE] … [/EVIDENCE]`, … DeBERTa-v3-base đọc cả bài (tối đa 1.536 token; bài dài hơn
được chia cửa sổ chồng 256 token), biểu diễn mỗi đơn vị = trung bình hidden state từ token mở đến token đóng,
rồi một lớp tuyến tính phân 3 nhãn. Một lượt forward cho mọi đơn vị trong bài.

**Giữ như L0/L1:** deberta-v3-base, lr 2e-5, 3 epoch, warmup 0.1, AdamW, class weight balanced (trên đơn vị),
chọn epoch theo Macro-F1 validation, cùng split. Batch hiệu dụng: 8 bài (~70 đơn vị) mỗi bước.
Chỉ validation; so với L1/L0 tuần 11 trên cùng 29.102 đơn vị, bootstrap theo bài. **Không chấm official test.**
'''

L3_BUILD = r'''
# ===== 3b. DỰNG DỮ LIỆU LEVEL 3 (cả bài + token đánh dấu) =====
from transformers import AutoModel, AutoTokenizer, get_linear_schedule_with_warmup, set_seed

CFG = dict(model_name="microsoft/deberta-v3-base", max_len=1536, overlap=256, eff_essays=8, lr=2e-5,
           weight_decay=0.01, epochs=3, warmup_ratio=0.1, seed=42, dropout=0.1)
if QUICK:
    CFG.update(epochs=1)
TYPES = sorted(units["discourse_type"].unique())
TAG = {t: t.upper().replace(" ", "_") for t in TYPES}
S_TOK = {t: f"[{TAG[t]}]" for t in TYPES}
E_TOK = {t: f"[/{TAG[t]}]" for t in TYPES}
tok = AutoTokenizer.from_pretrained(CFG["model_name"], use_fast=True)
tok.add_special_tokens({"additional_special_tokens": list(S_TOK.values()) + list(E_TOK.values())})
S_IDS = set(tok.convert_tokens_to_ids(list(S_TOK.values())))
E_IDS = set(tok.convert_tokens_to_ids(list(E_TOK.values())))
log(f"Token đánh dấu: {list(S_TOK.values())}")


def essay_items(g):
    g = g.sort_values(["start", "row_idx"], kind="mergesort")
    ft = g["full_text"].iloc[0]
    parts, pos = [], 0
    for r in g.itertuples():
        s = max(r.start, pos); e = max(r.end, s)
        parts += [ft[pos:s], f" {S_TOK[r.discourse_type]} ", ft[s:e], f" {E_TOK[r.discourse_type]} "]
        pos = e
    parts.append(ft[pos:])
    ids = tok("".join(parts), add_special_tokens=False)["input_ids"]
    starts = [i for i, x in enumerate(ids) if x in S_IDS]
    ends = [i for i, x in enumerate(ids) if x in E_IDS]
    assert len(starts) == len(ends) == len(g), (len(starts), len(ends), len(g))
    W = CFG["max_len"] - 2
    wins, a = [], 0
    while True:
        b = min(a + W, len(ids)); wins.append((a, b))
        if b >= len(ids):
            break
        a += W - CFG["overlap"]
    per_win = [[] for _ in wins]
    n_partial = 0
    for (s, e), lab, rid in zip(zip(starts, ends), g["label"].values, g["row_idx"].values):
        wi = next((i for i, (a, b) in enumerate(wins) if a <= s and e < b), None)
        if wi is None:                       # đơn vị dài hơn phần chồng: lấy cửa sổ chứa token mở, cắt ở cuối
            wi = next(i for i, (a, b) in enumerate(wins) if a <= s < b); n_partial += 1
        a, b = wins[wi]
        per_win[wi].append((s - a + 1, min(e, b - 1) - a + 1, int(lab), int(rid)))   # +1 cho [CLS]
    items = []
    for (a, b), us in zip(wins, per_win):
        if us:
            items.append({"ids": [tok.cls_token_id] + ids[a:b] + [tok.sep_token_id],
                          "spans": [(u[0], u[1]) for u in us], "labels": [u[2] for u in us],
                          "row_idx": [u[3] for u in us]})
    return items, len(ids), len(wins), n_partial


def build(d, name):
    items, lens, nwin, npart = [], [], [], 0
    for _, g in d.groupby("essay_id_comp", sort=False):
        it, L, w, p = essay_items(g)
        items += it; lens.append(L); nwin.append(w); npart += p
    lens = np.array(lens)
    log(f"[{name}] {len(lens):,} bài -> {len(items):,} cửa sổ | token/bài p50/p90/p99/max = "
        f"{np.percentile(lens, [50, 90, 99, 100]).round().tolist()} | bài > {CFG['max_len']} token: "
        f"{(lens > CFG['max_len'] - 2).mean():.2%} | đơn vị bị cắt cuối: {npart}")
    assert sum(len(x["labels"]) for x in items) == len(d)
    return items


t0 = time.time()
train_items, val_items = build(train_df, "train"), build(val_df, "val")
log(f"Dựng dữ liệu xong sau {time.time() - t0:.0f}s")
ex = val_items[0]
print(tok.decode(ex["ids"][:220]))
'''

L3_MODEL = r'''
# ===== 4. MÔ HÌNH + TRAIN LEVEL 3 =====
class EssayUnitClassifier(nn.Module):
    def __init__(self, name, vocab_size):
        super().__init__()
        self.backbone = AutoModel.from_pretrained(name)
        self.backbone.resize_token_embeddings(vocab_size)
        self.drop = nn.Dropout(CFG["dropout"])
        self.head = nn.Linear(self.backbone.config.hidden_size, 3)

    def forward(self, input_ids, attention_mask, span_b, span_s, span_e):
        h = self.backbone(input_ids=input_ids, attention_mask=attention_mask).last_hidden_state
        T = h.size(1)
        ar = torch.arange(T, device=h.device)
        w = ((ar[None, :] >= span_s[:, None]) & (ar[None, :] <= span_e[:, None])).to(h.dtype)
        w = w / w.sum(1, keepdim=True)
        pooled = torch.einsum("ut,uth->uh", w, h[span_b])          # trung bình hidden state trong đơn vị
        return self.head(self.drop(pooled)).float()


def collate(batch):
    T = max(len(x["ids"]) for x in batch)
    ids = torch.full((len(batch), T), tok.pad_token_id, dtype=torch.long)
    att = torch.zeros((len(batch), T), dtype=torch.long)
    sb, ss, se, lab, rid = [], [], [], [], []
    for i, x in enumerate(batch):
        ids[i, :len(x["ids"])] = torch.tensor(x["ids"]); att[i, :len(x["ids"])] = 1
        for (s, e), l, r in zip(x["spans"], x["labels"], x["row_idx"]):
            sb.append(i); ss.append(s); se.append(e); lab.append(l); rid.append(r)
    t = lambda v: torch.tensor(v, dtype=torch.long)
    return ids, att, t(sb), t(ss), t(se), t(lab), np.array(rid)


def make_batches(items, bs, shuffle, rng):
    idx = np.arange(len(items))
    if shuffle:
        rng.shuffle(idx)
        mega = bs * 50                                  # gom bài dài gần nhau -> bớt padding
        idx = np.concatenate([sorted(idx[i:i + mega], key=lambda j: len(items[j]["ids"]))
                              for i in range(0, len(idx), mega)])
        bl = [idx[i:i + bs] for i in range(0, len(idx), bs)]
        rng.shuffle(bl)
    else:
        idx = sorted(idx, key=lambda j: len(items[j]["ids"]))
        bl = [idx[i:i + bs] for i in range(0, len(idx), bs)]
    return bl


def seed_all(seed):
    random.seed(seed); np.random.seed(seed); os.environ["PYTHONHASHSEED"] = str(seed)
    torch.manual_seed(seed); torch.cuda.manual_seed_all(seed); set_seed(seed)


DTYPE = torch.bfloat16 if USE_BF16 else torch.float16


def pick_batch(model):
    total = torch.cuda.get_device_properties(0).total_memory
    fake = {"ids": [5] * CFG["max_len"], "spans": [(i * 40 + 1, i * 40 + 30) for i in range(20)],
            "labels": [1] * 20, "row_idx": list(range(20))}
    for bs in (8, 4, 2, 1):
        try:
            torch.cuda.empty_cache(); torch.cuda.reset_peak_memory_stats()
            ids, att, sb, ss, se, lab, _ = collate([fake] * bs)
            with torch.autocast("cuda", dtype=DTYPE):
                model(ids.cuda(), att.cuda(), sb.cuda(), ss.cuda(), se.cuda()).sum().backward()
            model.zero_grad(set_to_none=True)
            peak = torch.cuda.max_memory_allocated()
            log(f"Thử {bs} bài x {CFG['max_len']} token: đỉnh VRAM {peak / 2**30:.1f}/{total / 2**30:.1f} GB")
            if peak < 0.80 * total:
                return bs, max(1, CFG["eff_essays"] // bs)
        except torch.cuda.OutOfMemoryError:
            log(f"{bs} bài tràn VRAM")
        model.zero_grad(set_to_none=True); torch.cuda.empty_cache()
    return 1, CFG["eff_essays"]


@torch.no_grad()
def predict(model, items, bs):
    model.eval()
    out_r, out_p = [], []
    for b in make_batches(items, bs * 2, False, None):
        ids, att, sb, ss, se, lab, rid = collate([items[j] for j in b])
        with torch.autocast("cuda", dtype=DTYPE):
            logits = model(ids.cuda(), att.cuda(), sb.cuda(), ss.cuda(), se.cuda())
        out_r.append(rid); out_p.append(torch.softmax(logits, -1).cpu().numpy())
    model.train()
    r, p = np.concatenate(out_r), np.concatenate(out_p)
    pos = pd.Series(np.arange(len(r)), index=r)
    order = pos.loc[val_df["row_idx"].values].values         # về đúng thứ tự val_df
    return p[order]


seed_all(CFG["seed"])
model = EssayUnitClassifier(CFG["model_name"], len(tok)).cuda()
per_dev, accum = pick_batch(model)
weights = compute_class_weight("balanced", classes=np.array([0, 1, 2]), y=train_df["label"].values)
loss_fn = nn.CrossEntropyLoss(weight=torch.tensor(weights, dtype=torch.float).cuda())
no_decay = ["bias", "LayerNorm.weight"]
params = [{"params": [p for n, p in model.named_parameters() if not any(k in n for k in no_decay)],
           "weight_decay": CFG["weight_decay"]},
          {"params": [p for n, p in model.named_parameters() if any(k in n for k in no_decay)], "weight_decay": 0.0}]
opt = torch.optim.AdamW(params, lr=CFG["lr"])
rng = np.random.default_rng(CFG["seed"])
n_batches = math.ceil(len(train_items) / per_dev)
total_steps = math.ceil(n_batches / accum) * CFG["epochs"]
sched = get_linear_schedule_with_warmup(opt, int(CFG["warmup_ratio"] * total_steps), total_steps)
log(f"batch {per_dev} bài x grad_accum {accum} | {n_batches} batch/epoch | {total_steps} bước tối ưu | "
    f"class weights {np.round(weights, 4).tolist()}")

best, best_state, history = -1, None, []
t_all = time.time()
for ep in range(1, CFG["epochs"] + 1):
    t0, run_loss, step = time.time(), 0.0, 0
    for bi, b in enumerate(make_batches(train_items, per_dev, True, rng)):
        ids, att, sb, ss, se, lab, _ = collate([train_items[j] for j in b])
        with torch.autocast("cuda", dtype=DTYPE):
            logits = model(ids.cuda(), att.cuda(), sb.cuda(), ss.cuda(), se.cuda())
        loss = loss_fn(logits, lab.cuda()) / accum
        loss.backward()
        run_loss += loss.item() * accum
        if (bi + 1) % accum == 0 or bi + 1 == n_batches:
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            opt.step(); sched.step(); opt.zero_grad(set_to_none=True); step += 1
            if step % (10 if QUICK else 200) == 0:
                log(f"epoch {ep} bước {step} | loss {run_loss / (bi + 1):.4f} | {time.time() - t0:.0f}s")
    assert np.isfinite(run_loss), "Loss NaN"
    probs = predict(model, val_items, per_dev)
    m = metrics_dict(val_df["label"].values, probs.argmax(1))
    history.append({"epoch": ep, "train_loss": run_loss / n_batches, **{k: float(v) for k, v in m.items()},
                    "epoch_minutes": (time.time() - t0) / 60})
    log(f"epoch {ep}: train loss {run_loss / n_batches:.4f} | val Macro-F1 {m['macro_f1']:.4f} | "
        f"F1 Ineff {m['f1_ineffective']:.4f} | Acc {m['accuracy']:.4f} | {(time.time() - t0) / 60:.1f} phút")
    if m["macro_f1"] > best:
        best, best_probs = m["macro_f1"], probs
        best_state = {k: v.detach().cpu().clone() for k, v in model.state_dict().items()}
minutes = (time.time() - t_all) / 60
log(f"Train xong sau {minutes:.1f} phút | best val Macro-F1 {best:.4f}")
json.dump({"cfg": CFG, "batch_essays": per_dev, "grad_accum": accum, "history": history, "best_metric": best,
           "train_minutes": round(minutes, 1), "gpu": GPU, "transformers": TV, "class_weights": weights.tolist(),
           "quick": QUICK}, open(f"{OUT_DIR}/train_history_{KEY}.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
PROBS = best_probs
save_predictions(PROBS, KEY)
CMP = compare_with_reference(PROBS.argmax(1), KEY)
# Theo loại đơn vị (giả thuyết: Counterclaim/Rebuttal/Position cần thông tin toàn bài)
ref1 = REF.set_index("row_idx").loc[val_df["row_idx"], "pred_label"].values
y, pred = val_df["label"].values, PROBS.argmax(1)
rows = []
for t in sorted(val_df.discourse_type.unique()):
    mm = val_df.discourse_type.values == t
    rows.append({"discourse_type": t, "n": int(mm.sum()), "L3": round(macro(y[mm], pred[mm]), 4),
                 "L1": round(macro(y[mm], ref1[mm]), 4), "delta": round(macro(y[mm], pred[mm]) - macro(y[mm], ref1[mm]), 4)})
by_type = pd.DataFrame(rows); by_type.to_csv(f"{OUT_DIR}/L3_vs_L1_by_type.csv", index=False)
print(by_type.to_string(index=False))
del model, opt; gc.collect(); torch.cuda.empty_cache()
'''

# ---------------------------------------------------------------- LOPO
LOPO_INTRO = r'''
# Notebook 11 — LOPO DeBERTa-v3 Level 0, chạy lại (tuần 11, mục B16)

Lượt tuần 10 (`week10_person3_full/06_lopo_deberta_colab.ipynb`) có hai vấn đề:
1. dùng **transformers 5.20.2** (T4, fp16) — bản này làm DeBERTa-v3 train hỏng (đã kiểm chứng tuần 11);
2. đặt đề bị giấu làm `eval_dataset` với `load_best_model_at_end=True` → **chọn epoch bằng chính tập kiểm tra ngoại đề**.

Lượt này: transformers 4.57.6 + bf16; train cố định 3 epoch, lấy mô hình cuối, chấm đề bị giấu đúng một lần;
dự đoán lưu kèm `row_idx`. Giữ nguyên: đầu vào L0 `type [SEP] text`, deberta-v3-base, max_length 512, lr 2e-5,
batch hiệu dụng 32, warmup 0.1, class weight balanced theo fold, seed 42 + fold, train = toàn bộ đơn vị có nhãn của 14 đề còn lại.
'''

LOPO_CODE = r'''
# ===== LOPO: 3 đề =====
from datasets import Dataset
from transformers import (AutoModelForSequenceClassification, AutoTokenizer, DataCollatorWithPadding, Trainer,
                          TrainingArguments, set_seed)

FOLDS = {1: "A Cowboy Who Rode the Waves", 2: "Summer projects", 3: "Distance learning"}
EXPECTED = {1: 5158, 2: 9855, 3: 18526}
CFG = dict(model_name="microsoft/deberta-v3-base", max_length=512, eff_batch=32, lr=2e-5, epochs=3,
           warmup_ratio=0.1, seed=42)
if QUICK:
    CFG.update(epochs=1)
ALL = units  # LOPO dùng toàn bộ 144.289 đơn vị có nhãn
ALL["text"] = ALL["discourse_type"] + " [SEP] " + ALL["discourse_text"]


class WeightedLossTrainer(Trainer):
    def __init__(self, *args, class_weights=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.class_weights = class_weights

    def compute_loss(self, model, inputs, return_outputs=False, **kwargs):
        labels = inputs["labels"]
        outputs = model(**{k: v for k, v in inputs.items() if k != "labels"})
        logits = outputs.logits
        loss = nn.CrossEntropyLoss(weight=self.class_weights.to(logits.device, logits.dtype))(
            logits.view(-1, 3), labels.view(-1))
        return (loss, outputs) if return_outputs else loss


def seed_all(seed):
    random.seed(seed); np.random.seed(seed); os.environ["PYTHONHASHSEED"] = str(seed)
    torch.manual_seed(seed); torch.cuda.manual_seed_all(seed); set_seed(seed)


def run_fold(fold):
    prompt = FOLDS[fold]
    pred_path = f"{OUT_DIR}/predictions_fold{fold}.csv"
    if os.path.exists(pred_path):
        log(f"fold {fold}: đã có kết quả, bỏ qua"); return
    tr = ALL[ALL["prompt_name"] != prompt].reset_index(drop=True)
    te = ALL[ALL["prompt_name"] == prompt].reset_index(drop=True)
    if QUICK:
        rng = np.random.RandomState(0)
        pick = lambda d, k: d[d.essay_id_comp.isin(rng.choice(d.essay_id_comp.unique(), k, replace=False))]
        tr, te = pick(tr, 60).reset_index(drop=True), pick(te, 20).reset_index(drop=True)
    else:
        assert len(te) == EXPECTED[fold], len(te)
    assert prompt not in set(tr["prompt_name"])
    log(f"fold {fold}: giấu '{prompt}' | train {len(tr):,} đơn vị / {tr.prompt_name.nunique()} đề | "
        f"test {len(te):,} đơn vị / {te.essay_id_comp.nunique():,} bài")
    seed = CFG["seed"] + fold
    seed_all(seed)
    tok = AutoTokenizer.from_pretrained(CFG["model_name"], use_fast=True)

    def to_hf(d):
        ds = Dataset.from_pandas(d[["text", "label"]].rename(columns={"label": "labels"}), preserve_index=False)
        ds = ds.map(lambda b: tok(b["text"], truncation=True, max_length=CFG["max_length"]),
                    batched=True, batch_size=2000, remove_columns=["text"])
        return ds.map(lambda b: {"length": [len(x) for x in b["input_ids"]]}, batched=True)

    hf_tr, hf_te = to_hf(tr), to_hf(te)
    weights = compute_class_weight("balanced", classes=np.array([0, 1, 2]), y=tr["label"].values)
    model = AutoModelForSequenceClassification.from_pretrained(
        CFG["model_name"], num_labels=3, id2label=ID2LABEL, label2id=LABEL2ID).cuda()
    per_dev, accum = 16, 2          # L4 22 GB: 32 x 512 tràn, 16 x 512 đỉnh 12,4 GB (đã đo)
    args = TrainingArguments(
        output_dir=f"{WORK}/ckpt_lopo{fold}", learning_rate=CFG["lr"],
        per_device_train_batch_size=per_dev, per_device_eval_batch_size=128,
        gradient_accumulation_steps=accum, num_train_epochs=CFG["epochs"], warmup_ratio=CFG["warmup_ratio"],
        bf16=USE_BF16, fp16=not USE_BF16, tf32=True, group_by_length=True, length_column_name="length",
        dataloader_num_workers=4, eval_strategy="no", save_strategy="no",   # không chọn epoch trên đề bị giấu
        seed=seed, logging_steps=10 if QUICK else 200, report_to="none")
    trainer = WeightedLossTrainer(model=model, args=args, train_dataset=hf_tr,
                                  data_collator=DataCollatorWithPadding(tok), processing_class=tok,
                                  class_weights=torch.tensor(weights, dtype=torch.float))
    t0 = time.time()
    trainer.train()
    minutes = (time.time() - t0) / 60
    losses = [h["loss"] for h in trainer.state.log_history if "loss" in h]
    assert losses and np.isfinite(losses[-1]), losses[-5:]
    from torch.utils.data import SequentialSampler
    trainer._get_eval_sampler = lambda ds, *a, **k: SequentialSampler(ds)   # giữ đúng thứ tự (xem notebook 08)
    pred_out = trainer.predict(hf_te)
    assert (pred_out.label_ids == te["label"].values).all(), "Thứ tự dự đoán lệch"
    logits = pred_out.predictions
    logits = logits[0] if isinstance(logits, tuple) else logits
    probs = torch.softmax(torch.tensor(logits, dtype=torch.float32), -1).numpy()
    y, pred = te["label"].values, probs.argmax(1)
    m = {k: round(float(v), 4) for k, v in metrics_dict(y, pred).items()}
    out = te[["row_idx", "essay_id_comp", "discourse_type", "prompt_name"]].copy()
    out["true_label"], out["pred_label"] = y, pred
    for c in range(3):
        out[f"pred_proba_{c}"] = np.round(probs[:, c], 6)
    out.to_csv(pred_path, index=False)
    json.dump({"fold": fold, "held_out_prompt": prompt, "n_train_units": len(tr), "n_test_units": len(te),
               "n_test_essays": int(te.essay_id_comp.nunique()), **m, "train_minutes": round(minutes, 1),
               "first_loss": losses[0], "last_loss": losses[-1], "seed": seed, "cfg": CFG, "gpu": GPU,
               "transformers": TV, "quick": QUICK},
              open(f"{OUT_DIR}/metrics_fold{fold}.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    log(f"fold {fold}: train {minutes:.1f} phút | loss {losses[0]:.3f} -> {losses[-1]:.3f} | "
        f"Macro-F1 {m['macro_f1']} | Acc {m['accuracy']} | F1 Ineff {m['f1_ineffective']}")
    del trainer, model; gc.collect(); torch.cuda.empty_cache()
'''

LOPO_FINISH = r'''
rows = [json.load(open(f"{OUT_DIR}/metrics_fold{f}.json", encoding="utf-8")) for f in FOLDS]
res = pd.DataFrame(rows)[["fold", "held_out_prompt", "n_train_units", "n_test_units", "n_test_essays", "macro_f1",
                          "accuracy", "balanced_accuracy", "qwk", "f1_ineffective", "f1_adequate", "f1_effective",
                          "recall_ineffective", "train_minutes"]]
res.to_csv(f"{OUT_DIR}/lopo_deberta_rerun_results.csv", index=False)
print(res.to_string(index=False))
bundle = f"{WORK}/results_{KEY}" + ("_QUICK" if QUICK else "") + ".zip"
with zipfile.ZipFile(bundle, "w", zipfile.ZIP_DEFLATED) as zf:
    for fn in sorted(os.listdir(OUT_DIR)):
        zf.write(f"{OUT_DIR}/{fn}", f"{os.path.basename(OUT_DIR)}/{fn}")
print("Đã đóng gói:", bundle, os.path.getsize(bundle), "bytes")
'''


# ---------------------------------------------------------------- L3, số bước cập nhật ngang L1
L3B_INTRO = L3_INTRO.replace("# Notebook 10 — Level 3: cả bài vào mô hình (tuần 11, hướng bổ sung / dự phòng báo cáo)",
    "# Notebook 10b — Level 3, 7 epoch (số bước cập nhật ngang L1)") + r'''

**Vì sao có bản 7 epoch?** Ở notebook 10 (3 epoch), Macro-F1 validation còn tăng đều (0,521 → 0,551 → 0,576): mô hình chưa hội tụ.
Lý do: mỗi bước cập nhật của L3 gồm 8 bài (~74 đơn vị), nên 3 epoch chỉ có ~4.700 bước, so với ~10.800 bước của L1 (batch 32 đơn vị).
Bản này train 7 epoch (~10.900 bước, ngang L1); mọi thứ khác giữ nguyên, epoch tốt nhất vẫn chọn theo Macro-F1 validation.
'''
L3B_BUILD = L3_BUILD.replace("weight_decay=0.01, epochs=3,", "weight_decay=0.01, epochs=7,")
assert L3B_BUILD != L3_BUILD


RECOVER = r'''
# ===== CỨU DỰ ĐOÁN TỪ CHECKPOINT TỐT NHẤT (chạy trong cùng kernel sau khi ô train dừng ở assert quá chặt) =====
# Ô train trước đã train xong 3 epoch và chọn epoch tốt nhất, nhưng dừng ở assert "Macro-F1 cuối == best_metric" (dung sai 1e-6
# quá chặt vì padding khác nhau giữa lúc train và lúc dự đoán làm bf16 lệch nhẹ). Checkpoint tốt nhất vẫn còn trên đĩa.
import glob
from transformers import AutoModelForSequenceClassification, AutoTokenizer
ckpts = sorted(glob.glob(f"{WORK}/ckpt_{KEY}/checkpoint-*"), key=lambda p: int(p.rsplit("-", 1)[1]))
state = json.load(open(f"{ckpts[-1]}/trainer_state.json", encoding="utf-8"))
best_dir, best_metric = state["best_model_checkpoint"], state["best_metric"]
hist = [h for h in state["log_history"] if "eval_macro_f1" in h]
log(f"Cứu từ {best_dir} | best_metric lúc train {best_metric:.4f} | các epoch: "
    + ", ".join(f"{h['eval_macro_f1']:.4f}" for h in hist))
tok = AutoTokenizer.from_pretrained(CFG["model_name"], use_fast=True)
model = AutoModelForSequenceClassification.from_pretrained(best_dir).cuda().eval()
texts = list(val_df[TEXT_COL])
out = []
with torch.no_grad(), torch.autocast("cuda", dtype=torch.bfloat16 if USE_BF16 else torch.float16):
    for i in range(0, len(texts), 128):                      # đúng thứ tự val_df
        enc = tok(texts[i:i + 128], truncation=True, max_length=CFG["max_length"], padding=True, return_tensors="pt").to("cuda")
        out.append(torch.softmax(model(**enc).logits.float(), -1).cpu().numpy())
PROBS = np.concatenate(out)
gap = metrics_dict(val_df["label"].values, PROBS.argmax(1))["macro_f1"] - best_metric
log(f"Macro-F1 dự đoán tuần tự − best_metric lúc train = {gap:+.5f}")
assert abs(gap) < 0.005
json.dump({"name": KEY, "cfg": CFG, "epoch_evals": hist, "best_metric": best_metric, "best_checkpoint": best_dir,
           "gpu": GPU, "transformers": TV, "recovered_from_checkpoint": True, "quick": QUICK},
          open(f"{OUT_DIR}/train_history_{KEY}.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
'''


def key_cell(key):
    return f'KEY = "{key}"'


NOTEBOOKS = {
    "08_L1w2_context.ipynb": [("markdown", L1W2_INTRO), ("code", SETUP), ("code", key_cell("L1w2")), ("code", DATA),
                              ("code", EVAL), ("code", L1W2_BUILD), ("code", HF_TRAIN), ("code", L1W2_RUN),
                              ("code", FINISH)],
    "09_L2_source_text.ipynb": [("markdown", L2_INTRO), ("code", SETUP), ("code", key_cell("L2")), ("code", DATA),
                                ("code", EVAL), ("code", L2_BUILD), ("code", HF_TRAIN), ("code", L2_RUN),
                                ("code", FINISH)],
    "10_L3_whole_essay.ipynb": [("markdown", L3_INTRO), ("code", SETUP), ("code", key_cell("L3")), ("code", DATA),
                                ("code", EVAL), ("code", L3_BUILD), ("code", L3_MODEL), ("code", FINISH)],
    "10b_L3_whole_essay_7epochs.ipynb": [("markdown", L3B_INTRO), ("code", SETUP), ("code", key_cell("L3_7ep")),
                                         ("code", DATA), ("code", EVAL), ("code", L3B_BUILD), ("code", L3_MODEL),
                                         ("code", FINISH)],
    "09r_L2_recover_from_best_checkpoint.ipynb": [
        ("markdown", "# Notebook 09r — cứu dự đoán L2 từ checkpoint tốt nhất\n\nChạy trong **cùng kernel** ngay sau notebook 09 "
                     "(lượt 2) khi ô train dừng ở assert quá chặt; không train lại."),
        ("code", 'TEXT_COL = "text_L2"'), ("code", RECOVER),
        ("code", L2_RUN.replace('PROBS = train_and_predict("text_L2", KEY)\n', '')), ("code", FINISH)],
    "12_L1para_paragraph_context.ipynb": [("markdown", PARA_INTRO), ("code", SETUP), ("code", key_cell("L1para")),
                                          ("code", DATA), ("code", EVAL), ("code", PARA_BUILD), ("code", HF_TRAIN),
                                          ("code", PARA_RUN), ("code", FINISH)],
    "../week11_lopo_rerun/11_lopo_rerun_L0.ipynb": [
        ("markdown", LOPO_INTRO), ("code", SETUP), ("code", key_cell("LOPO_L0")), ("code", DATA), ("code", EVAL),
        ("code", LOPO_CODE), ("code", "run_fold(1)"), ("code", "run_fold(2)"), ("code", "run_fold(3)"),
        ("code", LOPO_FINISH)],
}

if __name__ == "__main__":
    for name, cells in NOTEBOOKS.items():
        path = os.path.normpath(os.path.join(HERE, name))
        with open(path, "w", encoding="utf-8") as f:
            json.dump(nb(cells), f, ensure_ascii=False, indent=1)
        # kiểm tra cú pháp từng ô code
        for t, s in cells:
            if t == "code":
                compile(s, path, "exec")
        print("wrote", path)
