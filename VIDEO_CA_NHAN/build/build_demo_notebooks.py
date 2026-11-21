"""Build and execute one demo notebook per person: VIDEO_CA_NHAN/Nguoi_N_*/demo/demo_nguoiN.ipynb.

Each notebook reuses the helpers in make_visuals.py (same numbers as demo_nguoiN.py and the slides),
shows every step as a table or figure, and is saved WITH outputs so it can be opened and shown directly.

Run from the repo root:  python VIDEO_CA_NHAN/build/build_demo_notebooks.py [--no-exec]
"""
import argparse
import sys
from pathlib import Path

import nbformat as nbf
from nbclient import NotebookClient

sys.stdout.reconfigure(encoding="utf-8")
VIDEO = Path(__file__).resolve().parents[1]

SETUP = r'''import sys, hashlib, textwrap
from pathlib import Path
import numpy as np, pandas as pd
from IPython.display import Image, display, Markdown
from sklearn.metrics import f1_score

# find the repo root from wherever the notebook is opened
HERE = Path.cwd()
ROOT = next(p for p in [HERE, *HERE.parents] if (p / "MLA_Final").is_dir())
sys.path.insert(0, str(ROOT / "VIDEO_CA_NHAN" / "build"))
sys.dont_write_bytecode = True
import make_visuals as data          # shared loaders: same numbers as the slides

pd.set_option("display.width", 140, "display.max_colwidth", 120)
LABELS = data.LABELS                  # Ineffective=0, Adequate=1, Effective=2

from IPython.display import HTML
def show(df, fmt=None, index=False):
    """Big, readable HTML table (no jinja2 needed)."""
    df = df.copy()
    for col, f in (fmt or {}).items():
        df[col] = df[col].map(lambda v, f=f: f.format(v) if isinstance(v, (int, float, np.number)) else v)
    display(HTML('<div style="font-size:18px; line-height:1.5">' + df.to_html(index=index) + "</div>"))

print("repo root:", ROOT)
'''

REPRO = r'''import subprocess
out = subprocess.run([sys.executable, "reproduce_results.py"], cwd=ROOT / "MLA_Final" / "Code",
                     capture_output=True, text=True, encoding="utf-8")
print(out.stdout[-{tail}:])'''


def md(s):
    return nbf.v4.new_markdown_cell(s.strip())


def code(s):
    return nbf.v4.new_code_cell(s.strip())


def header(title, role, steps, raw_note):
    return [
        md(f"""# Demo — {title}
**Group 06 · CLC02 · {role}**

Everything below is computed from the **saved outputs of the final project** (`MLA_Final/`): no model is re-trained and the official test labels are only read from saved prediction files.

**Run all cells top to bottom (Run All).** {raw_note}

Steps: {steps}"""),
        md("## 0 · Setup"),
        code(SETUP),
    ]


def nb_person1():
    cells = header(
        "Role 1: data, classical models and essay length", "Role 1",
        "① reproduce the paper's tables → ② trace one real test unit → ③ identifier check → ④ Ineffective recall by essay length.",
        "The raw PERSUADE test CSV is optional: if it is present the unit text is shown, otherwise the step says so (reading it takes ~20–40 s; cut that wait in the video).")
    cells += [
        md("## ① Reproduce the paper's main tables from saved predictions\nLook at the two **Random Forest (FS-B)** rows and the `[SUCCESS]` line."),
        code(REPRO.format(tail=2200)),
        md("## ② One real test unit: from the raw CSV to a prediction\nTest `row_idx` 47,059 — a Position on *Facial action coding system*."),
        code(r'''USE_RAW = data.raw_path("test").exists()      # set to False to skip the 1 GB-class CSV
raw_test = data.raw_optional("test", no_raw=not USE_RAW)
e = data.example("test", 47059, raw_test)
rf = data.probability_row("test", "rf_feature_set_b", 47059)
l1 = data.probability_row("test", "L1", 47059)
trace = pd.DataFrame([
    ("raw CSV record", f"{e['raw_record']:,}" if e["raw_record"] is not None else "(raw CSV not loaded)"),
    ("row_idx (after dropping unlabelled rows)", f"{int(e['row_idx']):,}"),
    ("prompt / type", f"{e['prompt_name']} / {e['discourse_type']}"),
    ("text", e["text"] or "(needs raw CSV)"),
    ("label string -> id", f"{LABELS[int(e['label'])]} -> {int(e['label'])}"),
    ("unit words / essay words", f"{int(e['unit_words'])} / {int(e['essay_word_count'])}"),
    ("essay-length quartile", e["length_q"]),
], columns=["step", "value"])
show(trace)
probs = pd.DataFrame({m: [f"{r['pred_proba_' + str(i)]:.3f}" for i in range(3)] + [LABELS[int(r.pred_label)]]
                      for m, r in [("Random Forest FS-B", rf), ("DeBERTa L1 (locked)", l1)]},
                     index=["P(Ineffective)", "P(Adequate)", "P(Effective)", "prediction"])
show(probs, index=True)'''),
        code(r'''display(Image(filename=str(ROOT / "VIDEO_CA_NHAN/Nguoi_1_Data_Classical_Length/visuals/v1_example_trace_rf.png"), width=1100))'''),
        md("## ③ Why every join uses `row_idx`, never `discourse_id`"),
        code(r'''raw_train = data.raw_optional("train", no_raw=not USE_RAW)
if raw_train is None:
    r = data.table("D4_identifier_integrity.csv").query("file == 'train+val annotated'").iloc[0]
    n, distinct, src = int(r.units), int(r.distinct_discourse_id), "saved table D4"
else:
    n, distinct, src = len(raw_train), raw_train.discourse_id.nunique(), "raw train CSV"
print(f"annotated units: {n:,}   distinct discourse_id values: {distinct:,}   ({src})")
print("-> Excel rounded the IDs, so joining on discourse_id would mix up units.")'''),
        md("## ④ Ineffective recall by essay-length quartile (official test, saved predictions)\nNew analysis for this video: computed here from the saved per-unit predictions."),
        code(r'''rows = data.recalls()
recall = pd.DataFrame(rows, columns=["essay-length quartile", "gold Ineffective", "RF recall", "DeBERTa L1 recall", "RF caught"])
show(recall, {"gold Ineffective": "{:,}", "RF recall": "{:.1%}", "DeBERTa L1 recall": "{:.1%}"})
q, n, *_ , caught = rows[-1]
print(f"In the longest essays the Random Forest catches {caught} of {n} gold Ineffective units.")'''),
        code(r'''display(Image(filename=str(ROOT / "VIDEO_CA_NHAN/Nguoi_1_Data_Classical_Length/visuals/v2_rf_recall_by_length.png"), width=1000))'''),
    ]
    return cells


def nb_person2():
    cells = header(
        "Role 2: DeBERTa, local context and the decision threshold", "Role 2",
        "① reproduce Table 2 (L1 − L0) → ② case 8 at Level 0 and Level 1 → ③ move the Ineffective threshold θ → ④ is case 8 flagged?",
        "The raw PERSUADE train CSV is optional: it is only needed to print the neighbouring units of case 8.")
    cells += [
        md("## ① Reproduce the paper's tables\nLook at **TABLE 2: Level 1 minus Level 0 on the same units**."),
        code(REPRO.format(tail=2200)),
        md("## ② Case 8: what DeBERTa reads at Level 0 and Level 1\nValidation `row_idx` 108,613 — a Claim on *Cell phones at school*, gold **Ineffective**."),
        code(r'''USE_RAW = data.raw_path("train").exists()
raw_train = data.raw_optional("train", no_raw=not USE_RAW)
e, l0_input, l1_input = data.inputs_case8(raw_train)
for name, text in [("Level 0 input", l0_input), ("Level 1 input", l1_input)]:
    print(name + ":")
    print(textwrap.fill(text, 110, initial_indent="   ", subsequent_indent="   "), "\n")
probs = pd.DataFrame({m: [f"{r['pred_proba_' + str(i)]:.3f}" for i in range(3)] + [LABELS[int(r.pred_label)]]
                      for m in ["L0", "L1"] for r in [data.probability_row("val", m, 108613)]},
                     index=["P(Ineffective)", "P(Adequate)", "P(Effective)", "prediction"])
show(probs, index=True)
print("gold label:", LABELS[int(e["label"])])'''),
        code(r'''display(Image(filename=str(ROOT / "VIDEO_CA_NHAN/Nguoi_2_DeBERTa_Context_Threshold/visuals/v1_case8_L0_vs_L1.png"), width=1100))'''),
        md("## ③ Flag a unit as Ineffective if P(Ineffective) ≥ θ\nLocked L1 model, **validation** only (θ is never chosen on the test). Change `THETA` and re-run this cell to show the trade-off live."),
        code(r'''THETA = 0.10

df = data.predictions("val", "L1")
p = df[[f"pred_proba_{i}" for i in range(3)]].to_numpy(); y = df.true_label.to_numpy()
rules = {"argmax": p.argmax(axis=1),
         f"θ = {THETA:.2f}": np.where(p[:, 0] >= THETA, 0, p[:, 1:].argmax(axis=1) + 1)}
rows = []
for name, pred in rules.items():
    flagged = int((pred == 0).sum()); tp = int(((pred == 0) & (y == 0)).sum())
    rows.append((name, flagged, tp / (y == 0).sum(), tp / flagged, f1_score(y, pred, average="macro"), tp, flagged - tp))
t = pd.DataFrame(rows, columns=["rule", "units flagged", "recall Ineff", "precision Ineff", "Macro-F1", "true flags", "false alarms"])
show(t, {"units flagged": "{:,}", "recall Ineff": "{:.1%}", "precision Ineff": "{:.1%}",
         "Macro-F1": "{:.3f}", "true flags": "{:,}", "false alarms": "{:,}"})
extra, false = rows[1][5] - rows[0][5], rows[1][6] - rows[0][6]
print(f"extra correct flags: {extra:,} | extra false alarms: {false:,} | false alarms per extra catch: {false/extra:.1f}")'''),
        md("## ④ Is case 8 flagged at this θ?"),
        code(r'''p8 = data.probability_row("val", "L1", 108613).pred_proba_0
print(f"case 8: P(Ineffective) = {p8:.3f} {'≥' if p8 >= THETA else '<'} θ = {THETA:.2f} -> "
      f"{'flagged' if p8 >= THETA else 'NOT flagged'}")'''),
        code(r'''display(Image(filename=str(ROOT / "VIDEO_CA_NHAN/Nguoi_2_DeBERTa_Context_Threshold/visuals/fig22_threshold_tradeoff.png"), width=900))'''),
    ]
    return cells


def nb_person3():
    cells = header(
        "Role 3: official test governance, unseen prompts and wider context", "Role 3",
        "① reproduce Tables 1 and 3 → ② check the test lock (hash) → ③ recompute test Macro-F1 → ④ case 2 through the context ladder → ⑤ LOPO gaps.",
        "The raw PERSUADE test CSV is optional: it is only needed to hash the file (no labels are read).")
    cells += [
        md("## ① Reproduce the paper's tables\nLook at the **Test** rows of TABLE 1 and at **TABLE 3 (LOPO)**."),
        code(REPRO.format(tail=3300)),
        md("## ② Has the official test file changed since it was locked?\nSHA-256 of the file vs. the hash written to `OFFICIAL_TEST_LOCK.json` before scoring. Only bytes are read, not labels."),
        code(r'''lock = data.lock()
path = data.raw_path("test")
if path.exists():
    sha = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8 * 1024 * 1024), b""):
            sha.update(chunk)
    now = sha.hexdigest()
else:
    now = None
show(pd.DataFrame([("locked at", lock["locked_at"]), ("n_test", f"{lock['n_test']:,}"),
                      ("sha256 in lock file", lock["test_sha256"][:16] + "…"),
                      ("sha256 now", (now[:16] + "…") if now else "(raw test CSV not present)"),
                      ("matches lock", now == lock["test_sha256"] if now else "n/a")],
                     columns=["item", "value"]))'''),
        md("## ③ Recompute official-test Macro-F1 from the saved per-unit predictions"),
        code(r'''r2 = data.table("R2_test_per_class.csv")
rows = []
for key, name in [("L0", "DeBERTa L0"), ("L1", "DeBERTa L1 (locked)"), ("PA", "DeBERTa Prompt-Aware")]:
    df = data.predictions("test", key)
    paper = r2[r2.system.str.contains("Prompt-Aware" if key == "PA" else key)].iloc[0].macro_f1
    rows.append((name, len(df), f1_score(df.true_label, df.pred_label, average="macro"), paper))
show(pd.DataFrame(rows, columns=["model", "units", "recomputed Macro-F1", "paper (table R2)"]),
     {"units": "{:,}", "recomputed Macro-F1": "{:.4f}", "paper (table R2)": "{:.4f}"})'''),
        md("## ④ Case 2 through the context ladder\nValidation `row_idx` 10,303 — Evidence on *Car-free cities*, gold **Ineffective**. Same DeBERTa recipe, different input at each level (saved probabilities; checkpoints are not kept)."),
        code(r'''row = data.ladder()
names = {"Ineff": "Ineffective", "Adeq": "Adequate", "Eff": "Effective"}
ladder = pd.DataFrame([(name, row[f"P_ineff_{k}"], names[row[f"pred_{k}"]]) for k, name in data.LEVELS],
                      columns=["input level", "P(Ineffective)", "prediction"])
show(ladder, {"P(Ineffective)": "{:.3f}"})'''),
        code(r'''display(Image(filename=str(ROOT / "VIDEO_CA_NHAN/Nguoi_3_TestGovernance_LOPO_Ladder/visuals/v1_case2_ladder.png"), width=1100))'''),
        md("## ⑤ Unseen prompts: LOPO vs in-domain on the same validation essays"),
        code(r'''r5 = data.table("R5_lopo_vs_indomain_per_class.csv")
rows = []
for prompt, g in r5.groupby("held_out_prompt", sort=False):
    lopo = g[g.setting.str.startswith("LOPO") & g.setting.str.contains("validation essays")].iloc[0]
    dom = g[g.setting.str.startswith("In-domain")].iloc[0]
    rows.append((prompt, lopo["units/essays"], dom.macro_f1, lopo.macro_f1, lopo.macro_f1 - dom.macro_f1))
show(pd.DataFrame(rows, columns=["held-out prompt", "units / essays", "in-domain", "LOPO", "gap"]),
     {"in-domain": "{:.4f}", "LOPO": "{:.4f}", "gap": "{:+.4f}"})
print("Paper (Table 6.7) rounds the gaps to -0.092 / -0.025 / -0.048; reproduce_results.py prints -0.091 for Cowboy (-0.0915).")'''),
        md("Full raw-row trace of case 2 (input text and token count per level): `VAN_DAP_4_TIEU_CHI/trace_mau_that/TRACE_MAU_THAT_PIPELINE.html` (local only)."),
    ]
    return cells


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-exec", action="store_true", help="write notebooks without running them")
    args = ap.parse_args()
    for n, (folder, builder) in enumerate([("Nguoi_1_Data_Classical_Length", nb_person1),
                                           ("Nguoi_2_DeBERTa_Context_Threshold", nb_person2),
                                           ("Nguoi_3_TestGovernance_LOPO_Ladder", nb_person3)], 1):
        nb = nbf.v4.new_notebook()
        nb.cells = builder()
        nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
        out = VIDEO / folder / "demo" / f"demo_nguoi{n}.ipynb"
        if not args.no_exec:
            NotebookClient(nb, timeout=600, kernel_name="python3",
                           resources={"metadata": {"path": str(out.parent)}}).execute()
        nbf.write(nb, out)
        print(out)


if __name__ == "__main__":
    main()
