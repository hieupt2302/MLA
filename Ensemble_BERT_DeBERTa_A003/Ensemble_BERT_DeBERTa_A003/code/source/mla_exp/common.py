import hashlib
import json
import os
import platform
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import numpy as np


def now():
    return datetime.now(timezone.utc).isoformat()


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, default=str).encode()).hexdigest()


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2, allow_nan=False, default=str)
        temp = stream.name
    os.replace(temp, path)


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def environment():
    import importlib.metadata
    names = ["numpy", "scipy", "pandas", "scikit-learn", "joblib", "torch", "transformers", "bitsandbytes"]
    versions = {}
    for name in names:
        try:
            versions[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            pass
    sources={path.name:sha256(path) for path in Path(__file__).parent.glob('*.py')}
    return {"python": platform.python_version(), "platform": platform.platform(), "packages": versions, "time": now(),'code_digest':digest(sources)}


def softmax(scores):
    scores = np.asarray(scores, dtype=np.float64)
    exp = np.exp(scores - scores.max(axis=1, keepdims=True))
    return exp / exp.sum(axis=1, keepdims=True)


def check_probabilities(probabilities):
    p = np.asarray(probabilities, dtype=np.float64)
    if p.ndim != 2 or p.shape[1] != 3 or not np.isfinite(p).all():
        raise ValueError("Expected finite N x 3 probabilities in label order 0,1,2")
    if (p < 0).any() or not np.allclose(p.sum(axis=1), 1, atol=1e-5):
        raise ValueError("Invalid probabilities")
    return p / p.sum(axis=1, keepdims=True)
