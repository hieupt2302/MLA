"""Additional teacher-facing diagnostics; no inherited score target is a gate."""
import json
import numpy as np
from sklearn.metrics import average_precision_score


def assessment_metrics(y, probabilities, segment_ids=None):
    y = np.asarray(y, dtype=int)
    p = np.asarray(probabilities, dtype=float)
    assert len(y) and p.shape == (len(y), 3)
    assert np.isfinite(p).all() and (p >= 0).all() and np.allclose(p.sum(1), 1)
    assert np.isin(y, [0, 1, 2]).all()
    supports = [int((y == label).sum()) for label in range(3)]
    ap = [float(average_precision_score(y == label, p[:, label])) if support else None
          for label, support in enumerate(supports)]
    if segment_ids is None:
        order = np.argsort(-p[:, 0], kind="stable")
    else:
        ids = np.asarray(segment_ids).astype(str)
        assert len(ids) == len(y) and len(np.unique(ids)) == len(ids)
        order = np.lexsort((ids, -p[:, 0]))
    curve = {}
    for fraction in [.05, .10, .20]:
        count = max(1, int(np.ceil(len(y) * fraction)))
        found = int((y[order[:count]] == 0).sum())
        curve[str(fraction)] = {"reviewed": count, "ineffective_found": found,
            "precision": found / count, "recall": found / supports[0] if supports[0] else None,
            "boundary_score": float(p[order[count - 1], 0]),
            "boundary_tie_count": int((p[:, 0] == p[order[count - 1], 0]).sum())}
    return {"average_precision_ineffective": ap[0], "average_precision_per_class": ap,
            "macro_average_precision": float(np.mean(ap)) if all(x is not None for x in ap) else None,
            "ineffective_prevalence": supports[0] / len(y), "review_budget_curve": curve,
            "review_budget_policy": "Predeclared top 5/10/20 percent by Ineffective score; batch-ranking diagnostic, not a fixed calibrated threshold",
            "review_tie_break": "segment_id" if segment_ids is not None else "prediction row order"}


if __name__ == "__main__":
    y = np.tile([0, 1, 2], 20)
    p = np.eye(3)[y] * .8 + .2 / 3
    ids = np.array([f"s{i:03}" for i in range(len(y))])
    result = assessment_metrics(y, p, ids)
    assert result["macro_average_precision"] == 1
    assert result["review_budget_curve"]["0.1"]["precision"] == 1
    assert result["review_budget_curve"]["0.1"]["recall"] == .3
    flat = np.full_like(p, 1 / 3)
    original = assessment_metrics(y, flat, ids)
    perm = np.random.default_rng(42).permutation(len(y))
    reordered = assessment_metrics(y[perm], flat[perm], ids[perm])
    assert original == reordered
    assert np.isclose(original["average_precision_ineffective"], 1 / 3)
    missing = assessment_metrics(np.ones(10, dtype=int), flat[:10])
    assert missing["average_precision_ineffective"] is None
    assert missing["review_budget_curve"]["0.1"]["recall"] is None
    json.dumps(missing, allow_nan=False)
    print("ASSESSMENT_CHECK_PASSED: perfect ranking, flat prevalence baseline, deterministic ID ties, absent-positive support")
