import warnings
import os
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix, log_loss, precision_recall_curve

from . import LABELS
from .common import check_probabilities, read_json, write_json


def from_confusion(matrix):
    m = np.asarray(matrix, dtype=float)
    tp = m.diagonal()
    precision = np.divide(tp, m.sum(axis=0), out=np.zeros(3), where=m.sum(axis=0) > 0)
    recall = np.divide(tp, m.sum(axis=1), out=np.zeros(3), where=m.sum(axis=1) > 0)
    f1 = np.divide(2 * precision * recall, precision + recall, out=np.zeros(3), where=precision + recall > 0)
    n = m.sum()
    weights = ((np.arange(3)[:, None] - np.arange(3)[None, :]) / 2) ** 2
    expected = np.outer(m.sum(axis=1), m.sum(axis=0)) / n if n else np.zeros((3, 3))
    denominator = (weights * expected).sum()
    qwk = float(1 - (weights * m).sum() / denominator) if denominator else None
    return {"macro_f1": float(f1.mean()), "accuracy": float(tp.sum() / n) if n else 0.0, "qwk": qwk,
            "precision_ineffective": float(precision[0]), "recall_ineffective": float(recall[0]),
            "per_class": {name: {"precision": float(precision[i]), "recall": float(recall[i]), "f1": float(f1[i]), "support": int(m[i].sum())} for i, name in enumerate(LABELS)}}


def operating_point(y, p, minimum_precision=0.4):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        precision, recall, thresholds = precision_recall_curve(np.asarray(y) == 0, np.asarray(p)[:, 0])
    eligible = np.flatnonzero(precision[:-1] >= minimum_precision)
    if not len(eligible):
        return {"threshold": 1.000001, "precision": None, "recall": 0.0}
    best = int(eligible[np.argmax(recall[eligible])])
    return {"threshold": float(thresholds[best]), "precision": float(precision[best]), "recall": float(recall[best])}


def metrics(y, p, segment_ids=None):
    p = check_probabilities(p)
    y = np.asarray(y, dtype=int)
    m = confusion_matrix(y, p.argmax(axis=1), labels=[0, 1, 2])
    result = from_confusion(m)
    onehot = np.eye(3)[y]
    confidence, predicted = p.max(axis=1), p.argmax(axis=1)
    ece = 0.0
    for i in range(10):
        mask = (confidence >= i / 10) & (confidence < (i + 1) / 10 if i < 9 else confidence <= 1)
        if mask.any():
            ece += float(mask.mean() * abs((predicted[mask] == y[mask]).mean() - confidence[mask].mean()))
    result.update({"n": len(y), "confusion_matrix": m.tolist(), "log_loss": float(log_loss(y, p, labels=[0, 1, 2])),
                   "brier_sum_classes": float(np.square(p - onehot).sum(axis=1).mean()), "ece_10_bins": ece,
                   "recall_at_precision_0.4": operating_point(y, p)["recall"]})
    from assessment import assessment_metrics
    result.update(assessment_metrics(y,p,segment_ids))
    return result


def warning_metrics(y, flags):
    truth, flags = np.asarray(y) == 0, np.asarray(flags, dtype=bool)
    tp = int((truth & flags).sum())
    return {'flagged': int(flags.sum()), 'true_positives': tp,
            'precision': tp / int(flags.sum()) if flags.any() else None,
            'recall': tp / int(truth.sum()) if truth.any() else None}


def group_confusions(frame, p):
    groups, indexes = np.unique(frame.group_id.astype(str), return_inverse=True)
    codes = indexes * 9 + frame.label.to_numpy(dtype=int) * 3 + np.asarray(p).argmax(axis=1)
    counts = np.bincount(codes, minlength=len(groups) * 9).reshape(len(groups), 3, 3)
    return groups, counts


def bootstrap(frame, p, repeats=2000, other=None):
    groups, matrices = group_confusions(frame, p)
    if other is not None:
        other_groups, other_matrices = group_confusions(frame, other)
        if not np.array_equal(groups, other_groups):
            raise ValueError("Paired bootstrap groups differ")
    rng = np.random.default_rng(2026)
    keys = ["macro_f1", "recall_ineffective", "precision_ineffective", "qwk"]
    values = {key: [] for key in keys}
    for _ in range(repeats):
        weights = rng.multinomial(len(groups), np.full(len(groups), 1 / len(groups)))
        first = from_confusion(np.einsum("g,gij->ij", weights, matrices))
        second = from_confusion(np.einsum("g,gij->ij", weights, other_matrices)) if other is not None else None
        for key in keys:
            if first[key] is not None and (second is None or second[key] is not None):
                values[key].append(first[key] - second[key] if second else first[key])
    return {key: {"low": float(np.quantile(samples, 0.025)), "high": float(np.quantile(samples, 0.975)), "valid_resamples": len(samples)} if samples else None for key, samples in values.items()}


def write_predictions(path, frame, p, model, seed, **extra):
    p = check_probabilities(p)
    if len(frame) != len(p) or frame.segment_id.duplicated().any():
        raise ValueError("Incomplete/duplicate predictions")
    output = frame[["segment_id", "group_id", "label", "discourse_type", "prompt_name"]].copy()
    for field in ["ell_status", "grade_level", "gender"]:
        if field in frame:
            output[field] = frame[field].replace("", "Unknown")
    output["length_words"] = frame.discourse_text.str.split().str.len()
    output["pred_label"] = p.argmax(axis=1)
    for i in range(3):
        output[f"p_{i}"] = p[:, i]
    output["model"], output["seed"] = model, seed
    output["status"], output["llm_used"] = "ok", False
    for field, value in extra.items():
        output[field] = value
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=Path(path).parent,prefix='.predictions_',suffix='.csv.gz',delete=False) as temporary:
        destination=temporary.name
    output.to_csv(destination,index=False)
    os.replace(destination,path)
    return output


def evaluate_file(path, output, repeats=2000, minimum_slice=100, minimum_class=20, data_root=None):
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    frame = pd.read_csv(path, keep_default_na=False)
    p = frame[["p_0", "p_1", "p_2"]].to_numpy()
    result = metrics(frame.label, p, frame.segment_id.to_numpy())
    if Path(output).exists():
        previous = read_json(output)
        for key in ['performance', 'inference_seconds', 'examples_second', 'feature_encoder_seconds', 'end_to_end_seconds', 'truncation', 'raw_classifier_metrics', 'component_performance']:
            if key in previous: result[key] = previous[key]
    if 'flag_ineffective' in frame:
        result['fixed_calibration_warning_policy'] = warning_metrics(frame.label, frame.flag_ineffective.astype(str).str.lower().eq('true'))
    result["essay_bootstrap_95"] = bootstrap(frame, p, repeats)
    frame['length_bin'] = pd.cut(frame.length_words, [0, 50, 100, 200, 500, np.inf], include_lowest=True).astype(str)
    slices = {}
    for column in ["discourse_type", "prompt_name", "ell_status", "grade_level", "length_bin", "target_truncated", "context_truncated"]:
        if column not in frame:
            continue
        slices[column] = {}
        for name, indexes in frame.groupby(column, dropna=False).groups.items():
            rows = frame.loc[indexes]
            counts = rows.label.value_counts().reindex([0, 1, 2], fill_value=0)
            entry = {"n": len(rows), "essays": rows.group_id.nunique(), "class_counts": counts.to_dict()}
            if len(rows) >= minimum_slice and counts.min() >= minimum_class:
                entry.update(metrics(rows.label, p[indexes]))
                entry["essay_bootstrap_95"] = bootstrap(rows, p[indexes], min(500, repeats))
            else:
                entry["note"] = "insufficient sample; no subgroup performance conclusion"
            slices[column][str(name)] = entry
    if 'ell_status' in frame and 'prompt_name' in frame:
        frame['ell_normalized']=frame.ell_status.astype(str).str.strip().replace({'':'Missing','Unknown':'Missing'})
        fair={}
        for (prompt,ell),indexes in frame.groupby(['prompt_name','ell_normalized'],dropna=False).groups.items():
            rows=frame.loc[indexes]
            counts=rows.label.value_counts().reindex([0,1,2],fill_value=0)
            item={'n':len(rows),'essays':int(rows.group_id.nunique()),'class_counts':counts.to_dict()}
            if len(rows)>=minimum_slice and counts.min()>=minimum_class:
                item.update(metrics(rows.label,p[indexes]));item['essay_bootstrap_95']=bootstrap(rows,p[indexes],min(500,repeats))
            else:item['note']='insufficient sample; no subgroup performance conclusion'
            fair.setdefault(str(prompt),{})[str(ell)]=item
        result['ELL_by_prompt']=fair
    result["slices"] = slices
    incorrect=frame.loc[frame.pred_label.ne(frame.label)].copy()
    incorrect['predicted_probability']=p.max(axis=1)[incorrect.index]
    examples=[]
    for label in [0,1,2]:
        examples.append(incorrect.loc[incorrect.label.eq(label)].sort_values('predicted_probability',ascending=False).head(8))
    errors=pd.concat(examples,ignore_index=True)
    data=Path(data_root)/'segments.csv.gz' if data_root else Path(output).resolve().parents[3]/'data'/'segments.csv.gz'
    if data.exists() and len(errors):
        texts=pd.read_csv(data,usecols=['segment_id','discourse_text'],keep_default_na=False)
        errors=errors.merge(texts,on='segment_id',validate='one_to_one')
        errors['discourse_text']=errors.discourse_text.str.slice(0,1500)
    errors.to_csv(Path(output).parent/'error_examples.csv',index=False)
    if "llm_used" in frame:
        used = frame.llm_used.astype(str).str.lower().eq("true")
        result["llm_coverage"] = float(used.mean())
        result["llm_routed_rows"] = int(used.sum())
        result["llm_errors"] = int((used & frame.status.ne('ok')).sum())
        result["status_counts"] = frame.status.value_counts().to_dict()
    write_json(output, result)
    plots(frame, p, Path(output).parent)
    return result


def plots(frame, p, root):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from sklearn.calibration import calibration_curve
    matrix = confusion_matrix(frame.label, p.argmax(axis=1), labels=[0, 1, 2])
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.imshow(matrix, cmap="Blues")
    ax.set(xticks=range(3), yticks=range(3), xticklabels=LABELS, yticklabels=LABELS, xlabel="Predicted", ylabel="Actual")
    for i in range(3):
        for j in range(3):
            ax.text(j, i, str(matrix[i, j]), ha="center", va="center", color="white" if matrix[i, j] > matrix.max()/2 else "black")
    fig.tight_layout(); fig.savefig(root / "confusion.png", dpi=180); plt.close(fig)
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.plot([0, 1], [0, 1], "k--")
    for i, name in enumerate(LABELS):
        actual, predicted = calibration_curve(frame.label == i, p[:, i], n_bins=10)
        ax.plot(predicted, actual, marker="o", label=name)
    ax.set(xlabel="Mean probability", ylabel="Observed frequency", xlim=(0, 1), ylim=(0, 1))
    ax.legend(); fig.tight_layout(); fig.savefig(root / "reliability.png", dpi=180); plt.close(fig)


def performance_plot(rows, root):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.ticker import NullFormatter
    positions = np.arange(len(rows))
    fig, axes = plt.subplots(1, 2, figsize=(12, max(3.5, len(rows)*.45)), sharey=True)
    throughput = [row['examples_second'] for row in rows]
    latencies = [row[key] for row in rows for key in ['batch_latency_p50', 'batch_latency_p95']]
    axes[0].scatter(throughput, positions, color='#2563eb')
    axes[0].set(yticks=positions, yticklabels=[row['run'] for row in rows], xlabel='Segments/second (log scale)')
    axes[1].scatter([row['batch_latency_p50'] for row in rows], positions-.12, color='#818cf8', marker='o', label='p50')
    axes[1].scatter([row['batch_latency_p95'] for row in rows], positions+.12, color='#4338ca', marker='s', label='p95')
    axes[1].set_xlabel('Seconds/batch (log scale)')
    for ax, values in zip(axes, [throughput, latencies]):
        ax.set_xscale('log')
        ax.set_xlim(min(values)/2, max(values)*2)
        ax.xaxis.set_minor_formatter(NullFormatter())
        ax.grid(axis='x', alpha=.2)
        ax.set_axisbelow(True)
    axes[0].set_ylim(len(rows)-.5, -.5)
    axes[1].legend()
    fig.suptitle(f"Text-to-prediction performance — {rows[0]['split']} (warmed models)")
    fig.tight_layout()
    fig.savefig(Path(root)/'pipeline_performance.png', dpi=180)
    plt.close(fig)


def report(root):
    root = Path(root)
    records, by_split, pilots = [], {}, []
    for path in sorted(root.glob("runs/*/metrics_*.json")):
        result = read_json(path)
        metadata = read_json(path.parent / "metadata.json")
        split = path.stem.removeprefix("metrics_")
        if metadata.get('pilot'):
            if metadata.get('family') == 'neural' and split == 'validation' and 'pilot_essays' in result:
                identity=metadata['identity']
                pilots.append({'run':path.parent.name,'encoder':identity['encoder'],'seed':identity['seed'],
                    'lr':identity['lr'],'balanced':identity['balanced'],'context':identity['context'],
                    'fit_segments':metadata.get('train_segments'),'validation_essays':result['pilot_essays'],
                    'validation_segments':result['n'],'macro_f1':result['macro_f1'],
                    'precision_ineffective':result['precision_ineffective'],'recall_ineffective':result['recall_ineffective'],
                    'train_seconds':metadata.get('train_seconds'),'train_peak_vram_bytes':metadata.get('train_peak_vram_bytes'),
                    'amp_dtype':identity['amp_dtype'],'training_code_digest':metadata['environment']['code_digest']})
            continue
        row = {"run": path.parent.name, "family": metadata["family"], "comparison_group": metadata.get('comparison_group', path.parent.name), "seed": metadata.get("seed", 42), "split": split,
               **{k: result.get(k) for k in ["n", "macro_f1", "precision_ineffective", "recall_ineffective", "qwk", "log_loss", "brier_sum_classes"]}}
        policy = result.get('fixed_calibration_warning_policy', {})
        row.update(warning_precision=policy.get('precision'), warning_recall=policy.get('recall'),
                   warning_flagged=policy.get('flagged'),
                   retrospective_recall_at_precision_0_4=result.get('recall_at_precision_0.4'))
        records.append(row)
        by_split.setdefault(split, []).append(row)
    if not records:
        raise ValueError("No measured runs to report")
    pd.DataFrame(records).to_csv(root / "leaderboard.csv", index=False)
    lines = ["# Benchmark PERSUADE — kết quả thực đo", "", "Dữ liệu: CC BY-NC-SA 4.0. Xác suất theo thứ tự Ineffective, Adequate, Effective.", ""]
    coverage = root / 'input_source_coverage.json'
    if not coverage.exists():
        coverage = root / 'audit.json'
    if coverage.exists():
        inputs = read_json(coverage)
        essays = inputs.get('essays', inputs.get('unique_labeled_essays'))
        if essays is not None and 'assignment_available_essays' in inputs:
            lines += [f"Đầu vào chuẩn hóa: {essays:,} essay; {inputs['assignment_available_essays']:,} essay có văn bản assignment từ nguồn dữ liệu. Context lấy từ toàn văn quanh offset gold đã kiểm chứng. `prompt_name` và `task` không được thay vào trường assignment.", ""]
    if pilots:
        pd.DataFrame(pilots).to_csv(root/'pilot_leaderboard.csv',index=False)
        lines += ['## Pilot neural: chọn cấu hình','',
                  'Pilot dùng cùng subset essay cố định của phần fit và 200 essay validation. Điểm pilot không thay thế điểm full-fit trên toàn validation/test. Training time gồm validation/checkpoint trong job; ledger CU còn ghi chi phí điều phối và truyền artifacts.','',
                  '| Run | LR | Balanced loss | Fit segment | Validation segment | Macro-F1 | R(Ineffective) |',
                  '|---|---:|---|---:|---:|---:|---:|']
        for entry in pilots:
            lines.append(f"| {entry['run']} | {entry['lr']:g} | {entry['balanced']} | {entry['fit_segments']} | {entry['validation_segments']} | {entry['macro_f1']:.4f} | {entry['recall_ineffective']:.4f} |")
        lines.append('')
    for path in sorted(root.glob('runs/*/selection.json')):
        metadata = read_json(path.parent/'metadata.json')
        if metadata.get('family') != 'llm': continue
        choice = read_json(path)
        lines += ['## LLM: pilot validation và quyết định mở test','',
                  f"Run **{path.parent.name}**, pipeline nền **{choice['base_run']}**. "
                  + ('Đủ điều kiện mở test.' if choice['improves_validation'] else
                     'Không mở test: chưa có cấu hình vừa cải thiện validation vừa nằm trong dự toán test.'),
                  f"Cấu hình chọn: {len(choice['shots'])}-shot, route {choice['fraction']:.0%}, "
                  f"trọng số LLM {choice['weight']}. Dự toán test {choice['estimated_test_seconds']} giây; "
                  f"giới hạn còn dành cho test LLM {choice.get('test_budget_seconds')} giây.",'',
                  'Bảng dưới đây là điểm toàn pipeline trên validation, gồm các đoạn không chuyển sang LLM. '
                  'Pilot không được đưa vào leaderboard test. Dự toán là chi phí dự kiến, không phải CU hoặc thời gian test đã thực đo.','',
                  '| Shot | Route | Trọng số LLM | Macro-F1 validation | Giây test dự kiến |',
                  '|---:|---:|---:|---:|---:|']
        for entry in choice['history']:
            lines.append(f"| {len(entry['shots'])} | {entry['fraction']:.0%} | {entry['weight']} | "
                         f"{entry['metrics']['macro_f1']:.4f} | {entry['estimated_test_seconds']} |")
        lines.append('')
    for split, rows in by_split.items():
        lines += [f"## {split}", "", "| Run | Seed | Macro-F1 | P(Ineffective) | R(Ineffective) | QWK |", "|---|---:|---:|---:|---:|---:|"]
        for row in sorted([row for row in rows if row['seed']==42], key=lambda x: x["macro_f1"], reverse=True):
            lines.append(f"| {row['run']} | {row['seed']} | {row['macro_f1']:.4f} | {row['precision_ineffective']:.4f} | {row['recall_ineffective']:.4f} | {row['qwk']} |")
        lines.append("")
        policies = [row for row in rows if row['warning_flagged'] is not None]
        if policies:
            lines += [f'### {split}: chính sách cảnh báo Ineffective','',
                      'Ngưỡng được chọn và khóa từ calibration với mục tiêu precision ≥0,40. '
                      'Bảng ghi precision/recall thực tế tại ngưỡng đó; precision trên test có thể thấp hơn mục tiêu. '
                      'Không có cảnh báo thì precision không xác định (—). '
                      'Cột `retrospective_recall_at_precision_0_4` trong CSV chỉ mô tả đường precision–recall của tập đánh giá, '
                      'không phải recall của chính sách ngưỡng cố định.','',
                      '| Run | Seed | Ngưỡng calibration | Số cảnh báo | Precision cảnh báo | Recall cảnh báo |',
                      '|---|---:|---:|---:|---:|---:|']
            for row in policies:
                threshold = read_json(root/'runs'/row['run']/'operating_point.json')['threshold']
                precision = f"{row['warning_precision']:.4f}" if row['warning_precision'] is not None else '—'
                lines.append(f"| {row['run']} | {row['seed']} | {threshold:.6f} | {row['warning_flagged']} | "
                             f"{precision} | {row['warning_recall']:.4f} |")
            lines.append('')
        additional=[row for row in rows if row['seed']!=42]
        if additional:
            lines += [f'### {split}: xác nhận seed bổ sung','', '| Run | Seed | Macro-F1 | P(Ineffective) | R(Ineffective) | QWK |','|---|---:|---:|---:|---:|---:|']
            for row in additional:
                lines.append(f"| {row['run']} | {row['seed']} | {row['macro_f1']:.4f} | {row['precision_ineffective']:.4f} | {row['recall_ineffective']:.4f} | {row['qwk']} |")
            lines.append('')
    discrimination=[]
    for path in root.glob('runs/*/metrics_*.json'):
        entry=read_json(path); meta=read_json(path.parent/'metadata.json')
        if meta.get('pilot') or 'raw_classifier_metrics' not in entry: continue
        raw=entry['raw_classifier_metrics']
        discrimination.append({'run':path.parent.name,'split':path.stem.removeprefix('metrics_'),'seed':meta.get('seed',42),
            'raw_classifier_macro_f1':raw['macro_f1'],'probability_pipeline_macro_f1':entry['macro_f1'],
            'raw_precision_ineffective':raw['precision_ineffective'],'raw_recall_ineffective':raw['recall_ineffective']})
    if discrimination:
        pd.DataFrame(discrimination).to_csv(root/'calibration_ablation.csv',index=False)
        lines += ['## Tác động của calibration lên phân lớp','',
                  'SVM decision scores là score, không phải confidence. Argmax score và argmax xác suất sau sigmoid có thể cho nhãn khác nhau. Bảng này tách chất lượng classifier trước calibration khỏi pipeline xác suất dùng khi ensemble. Xác suất softmax score SVM không được diễn giải là xác suất đã hiệu chỉnh.','',
                  '| Run | Tập | Macro-F1 classifier gốc | Macro-F1 pipeline xác suất |','|---|---|---:|---:|']
        for entry in sorted(discrimination,key=lambda r:(r['split'],r['run'])):
            lines.append(f"| {entry['run']} | {entry['split']} | {entry['raw_classifier_macro_f1']:.4f} | {entry['probability_pipeline_macro_f1']:.4f} |")
        lines.append('')
    seeds = pd.DataFrame(records)
    repeated = seeds.groupby(["comparison_group", "split"]).filter(lambda x: x.seed.nunique() >= 3)
    if len(repeated):
        summary = repeated.groupby(["comparison_group", "split"]).macro_f1.agg(["mean", "std", "count"])
        summary.to_csv(root / "seed_stability.csv")
    if not (root / "selection.lock.json").exists():
        lines += ["**Test chưa được mở. Các bảng hiện có chỉ là development/validation.**", ""]
    else:
        lock=read_json(root/'selection.lock.json')
        champion=lock.get('validation_champion')
        lines += ['## Mô hình được chọn trước test','',f'Ứng viên chọn bằng validation: **{champion}**. Không chọn lại champion bằng điểm test.','']
        if champion and (root/'runs'/champion/'predictions_test.csv.gz').exists():
            first=pd.read_csv(root/'runs'/champion/'predictions_test.csv.gz',keep_default_na=False)
            reference=first[['p_0','p_1','p_2']].to_numpy()
            paired=[]
            for row in by_split.get('test',[]):
                if row['run']==champion: continue
                other=pd.read_csv(root/'runs'/row['run']/'predictions_test.csv.gz',keep_default_na=False)
                if other.segment_id.duplicated().any() or set(first.segment_id)!=set(other.segment_id): raise ValueError('Paired report prediction coverage differs')
                other=other.set_index('segment_id').loc[first.segment_id]
                if not np.array_equal(first.label.to_numpy(),other.label.to_numpy()): raise ValueError('Paired report labels differ')
                intervals=bootstrap(first,reference,2000,other=other[['p_0','p_1','p_2']].to_numpy())
                paired.append({'champion':champion,'reference':row['run'],'macro_f1_difference':metrics(first.label,reference)['macro_f1']-row['macro_f1'],'essay_bootstrap_95':intervals})
            write_json(root/'paired_comparisons.json',paired)
            lines += ['| Chênh lệch Macro-F1: champion trừ đối chứng | Delta | CI 95% theo essay |','|---|---:|---|']
            for item in paired:
                ci=item['essay_bootstrap_95']['macro_f1']
                lines.append(f"| {item['reference']} | {item['macro_f1_difference']:.4f} | [{ci['low']:.4f}, {ci['high']:.4f}] |")
            lines.append('')
    lines += ['## Các câu hỏi experiment','']
    final_rows=by_split.get('test',by_split.get('validation',[]))
    def best_family(prefix):
        candidates=[row for row in final_rows if row['family'].startswith(prefix) and row['seed']==42]
        return max(candidates,key=lambda row:row['macro_f1']) if candidates else None
    linear_candidates=[]
    for row in final_rows:
        if row['family'] not in ['lr','svm','context_lr','context_svm']: continue
        source=read_json(root/'runs'/row['run']/f"metrics_{row['split']}.json")
        raw=source.get('raw_classifier_metrics',{}).get('macro_f1',row['macro_f1'])
        linear_candidates.append(dict(row,macro_f1=max(raw,row['macro_f1']),
                                      prediction_basis='classifier gốc' if raw>row['macro_f1'] else 'pipeline xác suất'))
    linear=max(linear_candidates,key=lambda row:row['macro_f1'],default=None)
    hybrid=best_family('hybrid'); neural=best_family('neural'); ensemble=best_family('ensemble'); llm=best_family('llm')
    for title,item in [('Hybrid tốt nhất',hybrid),('Encoder fine-tune tốt nhất (seed 42)',neural),('Ensemble tốt nhất',ensemble),('Pipeline LLM tốt nhất',llm)]:
        lines.append(f"- {title}: {item['run']} — Macro-F1 {item['macro_f1']:.4f}." if item else f'- {title}: chưa có benchmark hoàn tất trong bảng này.')
    if hybrid and linear: lines.append(f"- Hybrid so với tuyến tính tốt nhất ({linear['run']}, {linear['prediction_basis']}): delta Macro-F1 {hybrid['macro_f1']-linear['macro_f1']:+.4f}.")
    lines += ['', 'Bảng validation quyết định cấu hình; bảng test và CI quyết định mức bằng chứng. Nhánh chưa chạy hoặc pilot không cải thiện không được coi là đã chứng minh hiệu quả.', '']
    measured_split='test' if 'test' in by_split else 'validation'
    indexed={row['run']:row for row in final_rows if row['seed']==42}
    comparisons=[('BERT embedding thêm vào LR có context','C3_lr','H1_lr'),
                 ('BERT embedding thêm vào SVM có context','C3_svm','H2_svm'),
                 ('Embedding task-aware thay frozen: LR','H1_lr','H3_lr'),
                 ('Embedding task-aware thay frozen: SVM','H2_svm','H3_svm'),
                 ('Thêm context cho fine-tuned BERT','N1_bert_no_context','N1_bert_42'),
                 ('Fine-tune BERT so với hybrid frozen','H1_lr','N1_bert_42')]
    for row in final_rows:
        if row['seed']!=42 or row['family'] not in ['ensemble','llm']: continue
        meta=read_json(root/'runs'/row['run']/'metadata.json')
        members=meta.get('members',[]) or ([meta['base_run']] if meta.get('base_run') else [])
        if members and all(name in indexed for name in members):
            reference=max(members,key=lambda name:indexed[name]['macro_f1'])
            comparisons.append(('Ensemble so với thành phần tốt nhất' if row['family']=='ensemble' else 'LLM so với toàn pipeline nền',reference,row['run']))
    available=[pair for pair in comparisons if pair[1] in indexed and pair[2] in indexed]
    if available:
        lines += [f'### Ablation trên {measured_split}','',
                  '| So sánh | Đối chứng | Ứng viên | Delta Macro-F1 | Thời gian train ứng viên (giờ) |',
                  '|---|---|---|---:|---:|']
        for question,base,candidate in available:
            meta=read_json(root/'runs'/candidate/'metadata.json')
            elapsed=meta.get('train_seconds')
            hours=f'{elapsed/3600:.2f}' if elapsed is not None else '—'
            lines.append(f"| {question} | {base} | {candidate} | {indexed[candidate]['macro_f1']-indexed[base]['macro_f1']:+.4f} | {hours} |")
        lines += ['', 'Delta là chênh lệch quan sát được, không tự chứng minh ý nghĩa thống kê. Thời gian train tuyến tính gồm tìm kiếm hyperparameter; thời gian neural gồm các epoch và checkpoint. Cần đọc cùng CI theo essay, chi phí và tỷ lệ lỗi từng lớp.', '']
    comparison_file=root/'H1_validation_comparisons.json'
    if comparison_file.exists():
        comparison=read_json(comparison_file)
        lines += ['### Kiểm chứng H1 trên validation','',
                  f"Paired bootstrap {comparison['repeats']:,} lần theo {comparison['essays']:,} essay, {comparison['rows']:,} segment. Kết quả này dùng validation và được tách khỏi benchmark test.",'',
                  '| H1 trừ đối chứng | Delta Macro-F1 | CI 95% theo essay |','|---|---:|---|']
        for item in [comparison]+comparison.get('additional_comparisons',[]):
            ci=item['paired_essay_bootstrap_95']['macro_f1']
            label=item['reference']+(' (argmax score gốc)' if item.get('reference_prediction')=='raw_classifier_argmax' else '')
            lines.append(f"| {label} | {item['macro_f1_difference']:+.4f} | [{ci['low']:.4f}, {ci['high']:.4f}] |")
        lines.append('')
    comparison_file=root/'H2_validation_comparisons.json'
    if comparison_file.exists():
        comparison=read_json(comparison_file)
        lines += ['### Kiểm chứng H2 trên validation','',
                  f"Paired bootstrap {comparison['repeats']:,} lần theo {comparison['essays']:,} essay, {comparison['rows']:,} segment. CI được tính từ nhãn dự đoán; score SVM gốc không được diễn giải là confidence.",'',
                  '| H2 trừ đối chứng | Biểu diễn dự đoán | Delta Macro-F1 | CI 95% theo essay |','|---|---|---:|---|']
        for item in comparison['comparisons']:
            ci=item['paired_essay_bootstrap_95']['macro_f1']
            lines.append(f"| {item['reference']} | {item['prediction_basis']} | {item['macro_f1_difference']:+.4f} | [{ci['low']:.4f}, {ci['high']:.4f}] |")
        lines.append('')
    costs=[]
    jobs=read_json(root/'remote_state.json').get('jobs',{}) if (root/'remote_state.json').exists() else {}
    for directory in root.glob('runs/*'):
        if not (directory/'metadata.json').exists(): continue
        metadata=read_json(directory/'metadata.json')
        if metadata.get('pilot'): continue
        measured=read_json(directory/'metrics_test.json') if (directory/'metrics_test.json').exists() else {}
        performance=measured.get('performance',{})
        job=jobs.get(directory.name,{})
        job_cu=job['cu_end']-job['cu_start'] if job.get('cu_end') is not None and job.get('cu_start') is not None else None
        costs.append({'run':directory.name,'train_seconds':metadata.get('train_seconds'),'train_peak_vram_bytes':metadata.get('train_peak_vram_bytes'),'feature_cache':metadata.get('feature_cache',False),'cv_jobs':metadata.get('cv_jobs',1 if metadata.get('cv_macro_f1') is not None else None),'inference_seconds':performance.get('seconds',measured.get('inference_seconds')),
                      'performance_phase':performance.get('phase'),
                      'llm_coverage':measured.get('llm_coverage'),'llm_routed_rows':measured.get('llm_routed_rows'),
                      'llm_errors':measured.get('llm_errors'),'llm_new_calls':performance.get('new_calls'),
                      'llm_cache_hits':performance.get('cache_hits'),
                      'training_job_account_cu':job_cu,
                      'examples_second':performance.get('examples_second',measured.get('examples_second')),'batch_latency_p50':performance.get('batch_latency_p50'),
                      'batch_latency_p95':performance.get('batch_latency_p95'),'feature_encoder_seconds':measured.get('feature_encoder_seconds'),
                      'gpu':performance.get('hardware',{}).get('gpu') if performance.get('hardware') else None,
                      'peak_vram_bytes':performance.get('hardware',{}).get('peak_vram_bytes') if performance.get('hardware') else None})
    pd.DataFrame(costs).to_csv(root/'performance.csv',index=False)
    uncached=[read_json(path) for path in sorted(root.glob('runs/*/uncached_performance_test.json'))]
    if uncached:
        pd.DataFrame([{key:row.get(key) for key in ['run','rows','batch_size','measured_batches','model_load_seconds','seconds','examples_second','batch_latency_p50','batch_latency_p95','llm_routed_rows','llm_errors','max_abs_probability_difference_from_saved']} for row in uncached]).to_csv(root/'uncached_pipeline_performance.csv',index=False)
        performance_plot(uncached, root)
        lines += ['## Latency từ văn bản đến dự đoán cuối','',
                  '![Throughput và latency pipeline thực đo](pipeline_performance.png)', '',
                  '| Run | Segment đo | Batch | p50 (giây/batch) | p95 (giây/batch) | Segment/giây |',
                  '|---|---:|---:|---:|---:|---:|']
        for row in uncached:
            lines.append(f"| {row['run']} | {row['rows']} | {row['batch_size']} | {row['batch_latency_p50']:.3f} | {row['batch_latency_p95']:.3f} | {row['examples_second']:.2f} |")
        lines += ['', 'Đo trực tiếp trên Colab từ văn bản, không đọc embedding/prediction cache. Model đã nạp và có warmup; thời gian nạp model ghi riêng. Mỗi batch là một population để xếp entropy cho LLM, nên tỷ lệ route được làm tròn và có thể khác benchmark chất lượng trên toàn test. p50/p95 là phân vị thời gian batch thực đo, không phải latency từng segment; số batch đo có trong CSV. Phép đo này không chọn lại cấu hình hay dùng nhãn test.', '']
    llm_costs=[entry for entry in costs if entry.get('llm_coverage') is not None]
    if llm_costs:
        lines += ['## Tỷ lệ sử dụng LLM trên toàn test','',
                  '| Run | Tỷ lệ chuyển LLM | Số dòng chuyển | Lỗi fallback |',
                  '|---|---:|---:|---:|']
        for entry in llm_costs:
            lines.append(f"| {entry['run']} | {entry['llm_coverage']:.2%} | {entry['llm_routed_rows']} | {entry['llm_errors']} |")
        lines += ['', 'Latency trong `performance_phase` chỉ áp dụng cho pha được ghi: nhánh LLM hoặc classifier dùng cache. Chi phí và latency các thành phần được lưu riêng; không cộng các quantile p50/p95 để suy ra latency toàn pipeline.', '']
    lines += ['## Hiệu năng và CU theo job','',
              '`performance.csv` ghi thời gian train, throughput, batch latency p50/p95, VRAM và `training_job_account_cu`. Cột CU là mức giảm số dư toàn tài khoản giữa hai mốc của job controller, gồm calibration/prediction/export trong job và runtime khác nếu cùng chạy. Đây không phải CU riêng đo từ GPU của model. Baseline ban đầu chạy chung một script nên không có mốc CU riêng từng model; ô trống biểu thị chưa đo, không phải 0 CU.','']
    encodings=[]
    for path in sorted(root.glob('embeddings/*/*.json')):
        record=read_json(path)
        if 'seconds' not in record or 'segment_ids' not in record: continue
        hardware=record.get('hardware',{})
        encodings.append({'cache':path.parent.name,'split':path.stem,'segments':len(record['segment_ids']),
                          'seconds':record['seconds'],'encoder':record.get('encoder'),'pooling':record.get('pooling'),
                          'source_run':record.get('source_run'),'gpu':hardware.get('gpu'),
                          'amp_dtype':hardware.get('amp_dtype'),'peak_vram_bytes':hardware.get('peak_vram_bytes')})
    if encodings:
        pd.DataFrame(encodings).to_csv(root/'encoding_performance.csv',index=False)
        lines += ['## Thời gian trích xuất embedding','',
                  'Thời gian train hybrid trong `performance.csv` đo classifier và tìm kiếm cấu hình. Đọc cùng thời gian tạo cache bên dưới; H3 còn dùng encoder đã fine-tune. Các thành phần dùng chung cache/checkpoint nên chi phí tạo chúng chỉ được tính một lần trong pipeline.','',
                  '| Cache | Tập | Segments | Giây | GPU | Pooling |','|---|---|---:|---:|---|---|']
        for entry in encodings:
            lines.append(f"| {entry['cache']} | {entry['split']} | {entry['segments']} | {entry['seconds']:.1f} | {entry['gpu']} | {entry['pooling']} |")
        lines.append('')
    if (root/'lopo.json').exists():
        lopo=read_json(root/'lopo.json')
        pd.DataFrame([{k:value for k,value in entry.items() if k not in ['per_class','confusion_matrix']} for entry in lopo]).to_csv(root/'lopo.csv',index=False)
        lines += ['## Stress test khác assignment','', 'Leave-one-prompt-out chỉ dùng development, C=1 và class-balanced. Bảng này không gộp với leaderboard test chính thức.','',
                  '| Prompt | Model | Essays | Segments | Macro-F1 |','|---|---|---:|---:|---:|']
        for entry in lopo: lines.append(f"| {entry['prompt']} | {entry['method']} | {entry['essays']} | {entry['n']} | {entry['macro_f1']:.4f} |")
        lines.append('')
    lines += ['## Phân tích lỗi','', 'Confusion matrices ghi số lỗi theo cặp nhãn. Sau khi evaluate hoàn tất, mỗi run có `error_examples.csv` với tối đa 8 ca dự đoán sai có xác suất cao nhất của từng nhãn thực tế, kèm trích đoạn khi dữ liệu chuẩn hóa có sẵn. Các ví dụ này minh họa lỗi quan sát được; không chứng minh nguyên nhân.', '']
    if (root/'budget.json').exists():
        budget=read_json(root/'budget.json')
        lines += ['## Chi phí','',f"Giảm số dư toàn tài khoản theo ledger: {budget['consumed_account_cu']:.2f}/50 CU. Đây là giới hạn bảo thủ, có thể bao gồm runtime khác của tài khoản.",'']
    if (root/'remote_state.json').exists():
        state=read_json(root/'remote_state.json')
        lines += ['## Tiến độ và nhánh dừng','',f"Trạng thái controller: {state.get('status','đang triển khai')}. Các job dừng hoặc không chạy dưới đây không có điểm test giả định.",'']
        for job in state.get('skipped',[]): lines.append(f"- {job['job']}: {job['reason']}.")
        for job in state.get('invalidated_jobs',[]): lines.append(f"- {job['job']} (kết quả chẩn đoán được lưu riêng): {job['reason']}.")
        active=[name for name,job in state.get('jobs',{}).items() if job.get('status')=='running']
        if active: lines.append('Job đang chạy tại thời điểm tạo báo cáo: '+', '.join(active)+'.')
        lines.append('')
    lines += ["## Giới hạn", "", "Kết quả chỉ áp dụng cho gold segments/types và essay-disjoint split; không chứng minh student-disjoint hoặc hiệu quả học tập. Các điểm số trong paper không nằm trong leaderboard này."]
    (root / "REPORT_VI.md").write_text("\n".join(lines), encoding="utf-8")
    return records
