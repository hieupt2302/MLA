"""
Hậu kiểm trên validation (không train lại, không dùng test): hiệu chỉnh lệch lớp + ghép mô hình cho thang ngữ cảnh.

Vì sao: các mô hình train với class weight "balanced" đoán thừa lớp thiểu số; mô hình đọc rộng (L1-para, L2, L3) đoán thừa
nhiều hơn. So Macro-F1 bằng argmax vì vậy trộn hai thứ: khả năng phân biệt và độ lệch xác suất. Ở đây mọi mô hình được
áp CÙNG một quy tắc hiệu chỉnh rồi mới so.

Quy tắc: lớp = argmax(log P(Ineff) + b0, log P(Adeq), log P(Eff) + b2); b0, b2 dò trên lưới −2,0 … +1,5 (bước 0,1).
Kiểm chéo theo bài: chia 3.119 bài validation thành 2 nửa (seed 42); dò b trên nửa này, áp lên nửa kia, rồi đổi vai.
Ghép: trung bình log-xác suất. So sánh: bootstrap theo bài (2.000 lần), so với L1 đã hiệu chỉnh cùng cách.

Chạy từ thư mục gốc repo:  python week11_context_levels/posthoc_bias_and_ensemble.py
Ra: outputs/context_levels_posthoc_bias_ensemble.csv
"""
import glob
import os
import sys

import numpy as np
import pandas as pd
from sklearn.metrics import f1_score

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P3 = os.path.join(ROOT, "Week11_Person3_DeBERTa_OfficialTest/outputs/week11_person3")
RES = os.path.join(ROOT, "week11_context_levels/results")
P = ["pred_proba_0", "pred_proba_1", "pred_proba_2"]
GRID = np.round(np.arange(-2.0, 1.51, 0.1), 1)
N_BOOT = 2000
SYSTEMS = [("L0", ["L0"]), ("L1", ["L1"]), ("PA", ["PA"]), ("L1w2", ["L1w2"]), ("L1para", ["L1para"]),
           ("L2", ["L2"]), ("L3", ["L3"]), ("L3_7ep", ["L3_7ep"]),
           ("L0+L1+PA", ["L0", "L1", "PA"]), ("L1+L1w2+L3", ["L1", "L1w2", "L3"]),
           ("tất cả 8", ["L0", "L1", "PA", "L1w2", "L1para", "L2", "L3", "L3_7ep"])]


def load():
    d = {m: pd.read_csv(os.path.join(P3, f"val_predictions_{m}.csv")) for m in ["L0", "L1", "PA"]}
    for k in ["L1w2", "L1para", "L2", "L3", "L3_7ep"]:
        d[k] = pd.read_csv(glob.glob(os.path.join(RES, k, "*", f"val_predictions_{k}.csv"))[0])
    for k, v in d.items():
        assert (v["row_idx"].values == d["L1"]["row_idx"].values).all() and \
               (v["true_label"].values == d["L1"]["true_label"].values).all(), k
    return d


def best_bias(l, y):
    best, arg = -1, None
    for b0 in GRID:
        for b2 in GRID:
            s = f1_score(y, (l + [b0, 0, b2]).argmax(1), average="macro")
            if s > best:
                best, arg = s, (b0, b2)
    return arg


def main():
    d = load()
    y, ess = d["L1"]["true_label"].values, d["L1"]["essay_id_comp"].values
    ue = np.unique(ess)
    rng = np.random.default_rng(42); rng.shuffle(ue)
    half = np.isin(ess, ue[: len(ue) // 2])
    codes = pd.Series(ess).astype("category").cat.codes.values
    members = [np.flatnonzero(codes == k) for k in range(codes.max() + 1)]

    preds, rows = {}, []
    for name, ms in SYSTEMS:
        l = np.mean([np.log(d[m][P].values + 1e-9) for m in ms], 0)
        out, biases = np.empty(len(y), int), []
        for fit in (half, ~half):
            b0, b2 = best_bias(l[fit], y[fit]); biases.append((b0, b2))
            out[~fit] = (l[~fit] + [b0, 0, b2]).argmax(1)
        preds[name] = out
        rows.append({"system": name, "models": "+".join(ms),
                     "macro_f1_argmax": round(f1_score(y, l.argmax(1), average="macro"), 4),
                     "macro_f1_bias_crossfit": round(f1_score(y, out, average="macro"), 4),
                     "accuracy_bias_crossfit": round((out == y).mean(), 4),
                     "f1_ineffective_bias_crossfit": round(f1_score(y == 0, out == 0), 4),
                     "pred_ineffective_share": round((out == 0).mean(), 4),
                     "bias_half1_b0_b2": biases[0], "bias_half2_b0_b2": biases[1],
                     "bias_at_grid_edge": any(abs(b) >= 2.0 or b >= 1.5 for bb in biases for b in bb)})
        print(rows[-1], flush=True)

    rng = np.random.default_rng(0)
    base = preds["L1"]
    deltas = {n: [] for n in preds if n != "L1"}
    for _ in range(N_BOOT):
        idx = np.concatenate([members[k] for k in rng.integers(0, len(members), len(members))])
        f_base = f1_score(y[idx], base[idx], average="macro")
        for n in deltas:
            deltas[n].append(f1_score(y[idx], preds[n][idx], average="macro") - f_base)
    for r in rows:
        if r["system"] in deltas:
            dd = np.array(deltas[r["system"]])
            r["delta_vs_L1_bias"] = round(f1_score(y, preds[r["system"]], average="macro") - f1_score(y, base, average="macro"), 4)
            r["ci95_vs_L1_bias"] = f"[{np.percentile(dd, 2.5):+.4f}, {np.percentile(dd, 97.5):+.4f}]"
    tab = pd.DataFrame(rows)
    tab.to_csv(os.path.join(ROOT, "outputs/context_levels_posthoc_bias_ensemble.csv"), index=False)
    print(tab.drop(columns=["models", "bias_half1_b0_b2", "bias_half2_b0_b2"]).to_string(index=False))


if __name__ == "__main__":
    main()
