"""Saved-output visuals and shared readers for the three print-only demos."""
from pathlib import Path
from functools import lru_cache
import json
import shutil
import sys
import textwrap

import numpy as np
import pandas as pd

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
VIDEO = ROOT / "VIDEO_CA_NHAN"
RESULTS = ROOT / "MLA_Final/Results"
LABELS = ["Ineffective", "Adequate", "Effective"]
COLORS = ["#DC2626", "#94A3B8", "#2563EB"]
PEOPLE = ["Nguoi_1_Data_Classical_Length", "Nguoi_2_DeBERTa_Context_Threshold",
          "Nguoi_3_TestGovernance_LOPO_Ladder"]
LEVELS = [("L0", "L0"), ("L1", "L1 (locked)"), ("PA", "Prompt-Aware"),
          ("L1w2", "L1 ±2"), ("L1para", "Paragraph"), ("L2", "L2 source"),
          ("L3", "L3 whole, 3 ep"), ("L3_7ep", "L3 whole, 7 ep")]

@lru_cache
def table(name):
    return pd.read_csv(RESULTS / "tables" / name)

@lru_cache
def predictions(split, model):
    df = pd.read_csv(RESULTS / "predictions" / f"{split}_predictions_{model}.csv")
    assert df.row_idx.is_unique, "Prediction join key is not unique"
    probs = df[[f"pred_proba_{i}" for i in range(3)]].to_numpy()
    assert np.isfinite(probs).all() and np.allclose(probs.sum(axis=1), 1, atol=.002)
    return df

@lru_cache
def units():
    return pd.read_csv(ROOT / "MLA_Final/Data/samples/_units_slim.csv.gz")

def lock():
    return json.loads((ROOT / "MLA_Final/Code/configs/OFFICIAL_TEST_LOCK.json").read_text())

def raw_path(split):
    return ROOT / f"data/persuade_raw/persuade_corpus_2.0_{split}.csv"

@lru_cache
def raw_units(split, full=False):
    # Same string loading, filtering, stripping and reset-index rule as common.py.
    cols = ["discourse_id", "discourse_start", "discourse_text", "discourse_type",
            "discourse_effectiveness", "prompt_name", "essay_id_comp", "essay_word_count"]
    if full:
        cols.append("full_text")
    df = pd.read_csv(raw_path(split), usecols=cols, dtype=str, low_memory=False,
                     keep_default_na=True)
    df["raw_record"] = np.arange(len(df))
    df = df.dropna(subset=["discourse_effectiveness", "discourse_text"]).copy()
    df["discourse_text"] = df.discourse_text.str.strip()
    df["prompt_name"] = df.prompt_name.str.strip().str.strip('"')
    df = df[df.discourse_text.str.len() > 0].reset_index(drop=True)
    df["row_idx"] = np.arange(len(df))
    return df

def raw_optional(split, no_raw=False, full=False):
    if no_raw or not raw_path(split).exists():
        return None
    try:
        return raw_units(split, full)
    except (OSError, ValueError) as exc:
        print(f"Note: optional raw {split} CSV unavailable ({type(exc).__name__}); saved tables used.")
        return None

def example(split, row_idx, raw=None):
    saved = units().query("split == @split and row_idx == @row_idx").iloc[0].to_dict()
    saved["text"] = None
    saved["raw_record"] = None
    if raw is not None:
        r = raw.loc[row_idx]
        saved.update(text=r.discourse_text, raw_record=int(r.raw_record))
        if "full_text" in r:
            saved["unit_chars"] = len(r.discourse_text)
            saved["relative_start"] = float(r.discourse_start) / len(r.full_text)
    else:
        d7 = table("D7_raw_examples_traced.csv")
        match = d7[d7.row_idx == row_idx]
        if not match.empty:
            saved["text"] = match.iloc[0].text_first_60_chars
    return saved

def inputs_case8(raw=None):
    r8 = table("R8_ten_cases.csv").query("case == 8").iloc[0]
    e = example("validation", int(r8.row_idx), raw)
    base = f"{e['discourse_type']} [SEP] "
    if raw is None:
        return e, base + e["text"], base + "Target: " + e["text"] + " (neighbour text needs raw CSV)"
    essay = raw[raw.essay_id_comp == e["essay_id_comp"]].sort_values("discourse_start", key=lambda s: pd.to_numeric(s))
    pos = essay.row_idx.tolist().index(int(r8.row_idx))
    prev = essay.iloc[pos-1].discourse_text if pos else ""
    nxt = essay.iloc[pos+1].discourse_text if pos+1 < len(essay) else ""
    return e, base + e["text"], base + f"Previous: {prev} [SEP] Target: {e['text']} [SEP] Next: {nxt}"

def probability_row(split, model, row_idx):
    return predictions(split, model).set_index("row_idx").loc[row_idx]

def probability_text(row):
    return " / ".join(f"{row[f'pred_proba_{i}']:.3f}" for i in range(3))

def recalls():
    meta = units().query("split == 'test'")[["row_idx", "label", "length_q"]]
    joined = []
    for model in ["rf_feature_set_b", "L1"]:
        m = meta.merge(predictions("test", model), on="row_idx", validate="one_to_one")
        assert len(m) == len(meta) and (m.label == m.true_label).all()
        joined.append(m)
    out = []
    for q in sorted(meta.length_q.unique()):
        groups = [m[(m.length_q == q) & (m.label == 0)] for m in joined]
        n = len(groups[0])
        catches = [int((g.pred_label == 0).sum()) for g in groups]
        out.append((q, n, *[c/n for c in catches], catches[0]))
    return out

def ladder():
    return pd.read_csv(RESULTS / "predictions/context_levels_10_cases.csv").query("case == 2").iloc[0]

def tokens(case):
    p = ROOT / "VAN_DAP_4_TIEU_CHI/trace_mau_that/outputs/tokens_per_level.csv"
    if not p.exists():
        return []
    try:
        df = pd.read_csv(p)
        return df[df.Ca == f"Ca {case}"]["Token"].astype(int).tolist()
    except (OSError, ValueError, KeyError):
        print("Note: optional token table unavailable; token annotations omitted.")
        return []

def print_wrapped(s):
    print(textwrap.fill(s, width=98, subsequent_indent="   ", replace_whitespace=True))

def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch
    from PIL import Image
    plt.rcParams.update({"font.family": ["Calibri", "DejaVu Sans"], "font.sans-serif": ["Calibri", "Arial", "DejaVu Sans"],
                         "font.size": 14, "text.color": "#0F172A", "axes.labelcolor": "#0F172A",
                         "xtick.color": "#0F172A", "ytick.color": "#0F172A",
                         "figure.facecolor": "#F8FAFC", "axes.facecolor": "#F8FAFC"})
    outputs = []
    def save(fig, who, name):
        p = VIDEO / who / "visuals" / name
        p.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(p, dpi=150)
        plt.close(fig)
        outputs.append(p)
    copies = [
        ["fig18_rf_lopo_15_prompts.png", "fig09_essay_length_vs_holistic_score.png", "fig20_error_within_score_by_length.png"],
        ["fig04_context_levels.png", "fig14_L1_minus_L0_per_class.png", "fig22_threshold_tradeoff.png"],
        ["fig26_test_governance.png", "fig19_context_ladder_validation.png", "fig17_lopo_vs_indomain_same_units.png", "fig23_ten_cases_by_context_level.png"]]
    for who, names in zip(PEOPLE, copies):
        dest = VIDEO / who / "visuals"
        dest.mkdir(parents=True, exist_ok=True)
        for name in names:
            p = dest / name
            shutil.copy(ROOT / "final_report/figures" / name, p)
            outputs.append(p)

    df = table("E1_split_label_distribution.csv").set_index("split").loc[["train", "validation", "test"]]
    fig, ax = plt.subplots(figsize=(7.2, 5.4))
    y = np.arange(len(df)); left = np.zeros(len(df))
    for label, color in zip(LABELS, COLORS):
        values = df[f"% {label}"].to_numpy()
        ax.barh(y, values, left=left, color=color, height=.48, label=label)
        for j, value in enumerate(values):
            if label == LABELS[0]:
                ax.text(0, j-.32, f"{value:.2f}%", color=color, va="center", fontsize=14)
            else:
                ax.text(left[j]+value/2, j, f"{value:.2f}%", ha="center", va="center", color="white" if label == LABELS[2] else "#0F172A")
        left += values
    for j, n in enumerate(df.units):
        ax.text(103, j, f"{int(n):,}", va="center")
    ax.set(yticks=y, yticklabels=df.index, xlim=(0, 125), ylim=(2.55, -.8))
    ax.set_xticks([]); ax.spines[:].set_visible(False)
    ax.legend(loc="lower center", bbox_to_anchor=(.45, -.2), ncol=2, frameon=False)
    fig.subplots_adjust(left=.23, right=.97, bottom=.25, top=.94)
    save(fig, "_chung", "intro_label_mix.png")

    test_raw = raw_optional("test", full=True)
    e = example("test", 47059, test_raw)
    rf = probability_row("test", "rf_feature_set_b", e["row_idx"])
    l1 = probability_row("test", "L1", e["row_idx"])
    fig, ax = plt.subplots(figsize=(12.8, 7.2)); ax.set_axis_off()
    titles = ["Raw CSV record", "Clean & encode", "Feature Set B", "Random Forest"]
    raw_note = f"Record {e['raw_record']:,}" if e['raw_record'] is not None else "Raw CSV unavailable"
    text = e['text'] or "Text unavailable in slim sample"
    bodies = [f"{raw_note}\n\n{e['prompt_name']}\n{e['discourse_type']}\n\n“{text}”\n\nRaw label: {LABELS[int(e['label'])]}",
              f"Drop unlabelled / empty rows\n\nrow_idx {int(e['row_idx']):,}\n\n{LABELS[int(e['label'])]} → id {int(e['label'])}\n\nJoin key: row_idx\n(never discourse_id)",
              f"TF-IDF word 1–2-grams\n(≤15,000)\nOne-hot: {e['discourse_type']}\n\nUnit words: {int(e['unit_words']):,}\nEssay words: {int(e['essay_word_count']):,}\n{e['length_q']}\nUnit/essay: {e['unit_words']/e['essay_word_count']:.3f}",
              "200 trees\nmax depth 35"]
    if 'unit_chars' in e:
        bodies[2] += f"\nUnit chars: {e['unit_chars']:,}\nRelative start: {e['relative_start']:.3f}"
    for i, (title, body) in enumerate(zip(titles, bodies)):
        x = .012 + i*.251
        ax.add_patch(FancyBboxPatch((x,.16), .226,.77, boxstyle="round,pad=0.008", fc="white", ec="#CBD5E1"))
        ax.text(x+.012,.89,title,fontsize=22,weight="bold",va="top")
        wrapped = "\n".join(textwrap.fill(line, 20) for line in body.splitlines())
        ax.text(x+.012,.79,wrapped,fontsize=17,va="top",linespacing=1.3)
        if i < 3:
            ax.annotate("", xy=(x+.247,.53), xytext=(x+.229,.53), arrowprops={"arrowstyle":"->", "color":"#64748B", "lw":2})
    bars = ax.inset_axes([.79,.34,.16,.27])
    bars.barh(np.arange(3), [rf[f"pred_proba_{i}"] for i in range(3)], color=COLORS)
    bars.set(yticks=np.arange(3), yticklabels=["Ineff", "Adeq", "Eff"], xlim=(0, .76)); bars.tick_params(labelsize=16)
    bars.invert_yaxis(); bars.set_xticks([]); bars.spines[:].set_visible(False)
    for i in range(3):
        v = rf[f"pred_proba_{i}"]; bars.text(v+.02,i,f"{v:.3f}",va="center",fontsize=16)
    ax.text(.78,.27,f"→ {LABELS[int(rf.pred_label)]} ✓\n(gold {LABELS[int(e['label'])]})",fontsize=18,color="#16A34A")
    ax.text(.5,.06,f"Locked DeBERTa L1: P(Ineffective) = {l1.pred_proba_0:.3f}",ha="center",color="#64748B",fontsize=20)
    fig.subplots_adjust(left=.01,right=.99,bottom=.02,top=.98)
    save(fig, PEOPLE[0], "v1_example_trace_rf.png")

    rows = recalls(); fig, ax = plt.subplots(figsize=(12.8,7.2))
    x = np.arange(len(rows))
    for offset, col, label, color in [(-.19,2,"Random Forest FS-B",COLORS[1]),(.19,3,"DeBERTa L1 (locked)",COLORS[2])]:
        vals = [r[col]*100 for r in rows]
        bars = ax.bar(x+offset, vals, width=.36, label=label, color=color)
        ax.bar_label(bars, labels=[f"{v:.1f}%" for v in vals], padding=5,fontsize=16)
    ax.set(xticks=x, xticklabels=[r[0].replace(' (','\n(')+f"\nn = {r[1]:,}" for r in rows], ylim=(0,60),ylabel="Ineffective recall (%)")
    ax.spines[["top","right"]].set_visible(False); ax.legend(frameon=False,fontsize=16)
    fig.subplots_adjust(left=.1,right=.97,bottom=.23,top=.95)
    save(fig, PEOPLE[0], "v2_rf_recall_by_length.png")

    train_raw = raw_optional("train")
    e, l0input, l1input = inputs_case8(train_raw)
    fig = plt.figure(figsize=(12.8,7.2))
    for bounds, heading, content in [([.035,.66,.54,.29],"Level 0 input",l0input),([.035,.03,.54,.60],"Level 1 input",l1input)]:
        ax = fig.add_axes(bounds); ax.set_axis_off()
        ax.add_patch(FancyBboxPatch((.005,.005),.98,.98,boxstyle="round,pad=0.005",fc="white",ec="#CBD5E1"))
        ax.text(.025,.94,heading,weight="bold",fontsize=20,va="top")
        # one block per [SEP]-separated part; the target part in blue bold
        parts = content.split(" [SEP] ")
        y = .76
        line_h = 17 * 1.3 / 72 / (bounds[3] * 7.2)  # one text line in axes units
        for k, part in enumerate(parts):
            if part.startswith("Previous:") and len(part) > 170:
                part = part[:170].rsplit(" ", 1)[0] + " …"
            text = part + (" [SEP]" if k < len(parts) - 1 else "")
            is_target = part.startswith("Target:") or (len(parts) == 2 and k == 1)
            wrapped = textwrap.fill(text, 50)
            ax.text(.025, y, wrapped, fontsize=17, va="top", linespacing=1.3,
                    color="#2563EB" if is_target else "#0F172A", weight="bold" if is_target else "normal")
            y -= line_h * (wrapped.count("\n") + 1.35)
    for idx, model in enumerate(["L0","L1"]):
        ax = fig.add_axes([.69,.62-idx*.34,.26,.22])
        row = probability_row("val",model,e["row_idx"])
        vals = [row[f"pred_proba_{i}"] for i in range(3)]
        ax.barh(np.arange(3), vals, color=COLORS); ax.invert_yaxis()
        ax.set(yticks=np.arange(3),yticklabels=["Ineff","Adeq","Eff"],xlim=(0,1.17)); ax.tick_params(labelsize=16)
        ax.set_xticks([]); ax.spines[:].set_visible(False)
        count = tokens(8)
        ax.set_title(model + (f" · {count[idx]:,} tokens" if count else ""),fontsize=20,loc="left")
        for j,v in enumerate(vals): ax.text(v+.025,j,f"{v:.3f}",va="center",fontsize=16)
    fig.text(.64,.12,f"gold: {LABELS[int(e['label'])]}\nboth predict {LABELS[int(row.pred_label)]} ✗",color=COLORS[0],fontsize=19)
    save(fig,PEOPLE[1],"v1_case8_L0_vs_L1.png")

    r8 = table("R8_ten_cases.csv").query("case == 2").iloc[0]
    e = example("validation",int(r8.row_idx),train_raw)
    caption = (e['text'] or r8.text_excerpt)[:110] + "…"
    row = ladder(); counts = tokens(2); cfg = lock()['cfg']
    desc = ["unit only", "±1 unit (prev: Position; no next)", "adds prompt name", "±2 units", "whole paragraph", "adds source passage", "whole essay, 3 epochs", "whole essay, 7 epochs (overfitted)"]
    if train_raw is not None:
        essay = train_raw[train_raw.essay_id_comp == e['essay_id_comp']]
        prev = essay[essay.row_idx < e['row_idx']].iloc[-1]
        desc[1] = f"±1 unit (prev: {prev.discourse_type}; no next)"
    token_indices = [0,1,2,3,4,5,6,6]
    fig, ax = plt.subplots(figsize=(12.8,7.2))
    y = np.arange(len(LEVELS)); vals = [row[f"P_ineff_{k}"] for k,_ in LEVELS]
    ax.barh(y, vals, height=.52,color=[COLORS[0] if row[f"pred_{k}"]=='Ineff' else COLORS[1] for k,_ in LEVELS])
    ax.set(yticks=y,yticklabels=[name for _,name in LEVELS],xlim=(0,1.04),xlabel="P(Ineffective)")
    ax.invert_yaxis(); ax.axvline(.5,ls="--",color="#64748B")
    ax.text(.5,1.025,"≈ decision region",transform=ax.get_xaxis_transform(),ha="center",fontsize=16); ax.tick_params(labelsize=17); ax.xaxis.label.set_size(17)
    for j,(v,d) in enumerate(zip(vals,desc)):
        ax.text(v+.015,j,f"{v:.3f}",va="center",fontsize=17)
        if counts:
            n = counts[token_indices[j]]; d += f" · {n:,} tokens"
            if LEVELS[j][0] == 'L1para': d += f" → cut at {cfg['max_length']:,}"
        ax.text(-1.80,j,d,transform=ax.get_yaxis_transform(),fontsize=17,va="center")
    ax.spines[["top","right"]].set_visible(False)
    fig.text(.035,.95,textwrap.fill(caption,95),fontsize=19,va="top")
    fig.subplots_adjust(left=.63,right=.96,bottom=.15,top=.85)
    save(fig,PEOPLE[2],"v1_case2_ladder.png")
    for p in outputs:
        with Image.open(p) as im:
            print(f"{p.relative_to(ROOT).as_posix()}  {im.width}×{im.height}")

if __name__ == "__main__":
    main()
