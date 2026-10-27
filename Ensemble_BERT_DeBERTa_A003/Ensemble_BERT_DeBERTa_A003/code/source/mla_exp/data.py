"""Data audit and essay-disjoint splits. Raw text is never normalized for offsets."""
import hashlib
import re
import time
from functools import lru_cache
from pathlib import Path

import pandas as pd
from sklearn.model_selection import StratifiedGroupKFold

from . import LABEL_MAP
from .common import digest, now, read_json, sha256, write_json

SOURCES = {
    "train": ("13phHyDzIsb0MHyJr6q-B-qIa9P2tM135", "train.csv"),
    "test": ("1K1SIJiG-2zWgMlTzxQeYOcLwOsFaVel1", "test.zip"),
}
PARTITIONS = {"train": "train", "training": "train", "test": "test", "testing": "test", "valid": "validation", "val": "validation", "validation": "validation"}
DEMOGRAPHICS = ["ell_status", "gender", "grade_level", "race_ethnicity", "economically_disadvantaged"]


def text_hash(text):
    return hashlib.sha256(re.sub(r"\s+", " ", str(text)).strip().encode("utf-8")).hexdigest()


@lru_cache(maxsize=512)
def normalized_text_map(text):
    words = list(re.finditer(r"\S+", text))
    characters, positions = [], []
    for i, word in enumerate(words):
        if i:
            characters.append(" "); positions.append(words[i - 1].end())
        characters.extend(word.group()); positions.extend(range(word.start(), word.end()))
    return "".join(characters), positions


def locate_span(text, target, start, end):
    if pd.isna(start) or pd.isna(end) or not float(start).is_integer() or not float(end).is_integer():
        return None
    start, end = int(start), int(end)
    needle = target.strip()
    if 0 <= start < end <= len(text) and text[start:end].strip() == needle:
        return start, end, "original"
    def choose(haystack, query):
        hits, position = [], 0
        while query:
            position = haystack.find(query, position)
            if position < 0: break
            hits.append(position); position += 1
        if len(hits) == 1:
            return hits[0]
        if hits:
            distances = [abs(hit - start) for hit in hits]
            nearest = min(distances)
            if distances.count(nearest) == 1 and nearest <= 256:
                return hits[distances.index(nearest)]
        return None
    position = choose(text, needle)
    if position is not None:
        return position, position + len(needle), "realigned_exact_text"
    normalized, mapping = normalized_text_map(text)
    query = " ".join(needle.split())
    position = choose(normalized, query)
    if position is not None:
        left, right = mapping[position], mapping[position + len(query) - 1] + 1
        if " ".join(text[left:right].split()) == query:
            return left, right, "realigned_whitespace"
    return None


def download_sources(root):
    import gdown
    import pyzipper
    root = Path(root)
    raw = root / "raw"
    raw.mkdir(parents=True, exist_ok=True)
    records = []
    for partition, (file_id, filename) in SOURCES.items():
        target = raw / filename
        if not target.exists():
            temp = target.with_suffix(target.suffix + ".partial")
            for attempt in range(3):
                try:
                    result = gdown.download(id=file_id, output=str(temp), quiet=False)
                    if not result or temp.stat().st_size < 1000:
                        raise RuntimeError("Dataset download returned no usable file")
                    temp.replace(target)
                    break
                except Exception:
                    if attempt == 2:
                        raise
                    time.sleep(5 * (attempt + 1))
        records.append({"partition": partition, "url": f"https://drive.google.com/file/d/{file_id}/view", "file": filename, "bytes": target.stat().st_size, "sha256": sha256(target), "verified_at": now()})
    extraction = raw / "official_test"
    if not list(extraction.rglob("*.csv")):
        extraction.mkdir(exist_ok=True)
        with pyzipper.AESZipFile(raw / "test.zip") as archive:
            archive.setpassword(b"persuade_test")
            for member in archive.infolist():
                resolved = (extraction / member.filename).resolve()
                if not resolved.is_relative_to(extraction.resolve()):
                    raise ValueError("Unsafe archive path")
            archive.extractall(extraction)
    write_json(root / "provenance.json", {"license": "CC BY-NC-SA 4.0", "source": "https://github.com/scrosseye/persuade_corpus_2.0", "files": records})


def _folds(frame, n, seed):
    if frame.group_id.nunique() < n:
        raise ValueError(f"Need at least {n} essay groups to make the specified split")
    cv = StratifiedGroupKFold(n_splits=n, shuffle=True, random_state=seed)
    return [test for _, test in cv.split(frame, frame.label, frame.group_id)]


def prepare(root, config, download=False):
    root = Path(root)
    if download:
        download_sources(root)
    raw = root / "raw"
    paths = sorted(raw.rglob("*.csv"))
    if not paths:
        raise FileNotFoundError(f"No original CSVs under {raw}; use --download or place official files there")
    parts, files = [], []
    required = ["full_text", "discourse_text", "discourse_type", "discourse_start", "discourse_end", "discourse_effectiveness"]
    for path in paths:
        source = pd.read_csv(path, dtype=str, keep_default_na=False, encoding="utf-8-sig")
        missing = set(required) - set(source.columns)
        if missing:
            raise ValueError(f"Missing columns in {path.name}: {sorted(missing)}")
        default = "test" if "test" in str(path.relative_to(raw)).lower() else "train"
        if "competition_set" in source:
            values = source.competition_set.str.strip().str.lower().replace("", default)
            unknown = set(values) - set(PARTITIONS)
            if unknown:
                raise ValueError(f"Unrecognized official partitions: {unknown}")
            source["official_partition"] = values.map(PARTITIONS)
        else:
            source["official_partition"] = default
        source["source_file"] = str(path.relative_to(raw))
        source["source_row"] = range(len(source))
        if "essay_id_comp" not in source:
            source["essay_id_comp"] = ""
        parts.append(source)
        files.append({"file": str(path.relative_to(raw)), "sha256": sha256(path), "rows": len(source)})
    df = pd.concat(parts, ignore_index=True)
    audit = {"created_at": now(), "raw_rows": len(df), "raw_files": files, "excluded": {}, "id_policy": "verified essay_id_comp plus whitespace-normalized full_text SHA256; not student-disjoint"}
    df["group_id"] = df.full_text.map(text_hash)
    ids = df.loc[df.essay_id_comp.str.strip().ne(""), ["essay_id_comp", "group_id"]].drop_duplicates()
    ambiguous = set(ids.groupby("essay_id_comp").group_id.nunique().loc[lambda x: x > 1].index)
    reason = pd.Series("", index=df.index)
    reason.loc[df.essay_id_comp.isin(ambiguous)] = "ambiguous_essay_id"
    reason.loc[df.full_text.str.strip().eq("") | df.discourse_text.str.strip().eq("")] = "empty_text"
    reason.loc[~df.discourse_effectiveness.str.strip().isin(LABEL_MAP)] = "missing_or_invalid_label"
    audit["ambiguous_essay_ids"] = len(ambiguous)
    audit["missing_essay_id_rows"] = int(df.essay_id_comp.str.strip().eq("").sum())
    df["label"] = df.discourse_effectiveness.str.strip().map(LABEL_MAP)
    for column in ["discourse_start", "discourse_end"]:
        df[column] = pd.to_numeric(df[column], errors="coerce")
    candidates = df.loc[reason.eq("")]
    df["original_discourse_start"] = df.discourse_start
    df["original_discourse_end"] = df.discourse_end
    df["span_alignment"] = "unresolved"
    resolved = candidates.apply(lambda row: locate_span(row.full_text, row.discourse_text, row.discourse_start, row.discourse_end), axis=1)
    aligned = pd.DataFrame([span if span is not None else (None, None, "unresolved") for span in resolved], index=resolved.index, columns=["start", "end", "mode"])
    reason.loc[aligned.index[aligned.start.isna()]] = "unresolvable_or_ambiguous_span"
    df.loc[aligned.index, "discourse_start"] = aligned.start.to_numpy()
    df.loc[aligned.index, "discourse_end"] = aligned.end.to_numpy()
    df.loc[aligned.index, "span_alignment"] = aligned["mode"].to_numpy()
    audit["span_alignment"] = df.loc[reason.eq(""), "span_alignment"].value_counts().to_dict()
    audit["span_policy"] = "Preserve gold text/label; re-localize exact or whitespace-equivalent segment in raw essay. Multiple occurrences need a unique nearest offset within 256 chars; ambiguity is quarantined."
    df["segment_id"] = [digest([g, str(s), str(e), t.strip()]) for g, s, e, t in zip(df.group_id, df.discourse_start, df.discourse_end, df.discourse_type)]
    candidate = df.loc[reason.eq("")]
    conflicts = set(candidate.groupby("segment_id").label.nunique().loc[lambda x: x > 1].index)
    reason.loc[df.segment_id.isin(conflicts) & reason.eq("")] = "conflicting_annotation"
    for name, count in reason.loc[reason.ne("")].value_counts().items():
        audit["excluded"][name] = int(count)
    quarantine = df.loc[reason.ne(""), ["source_file", "source_row", "essay_id_comp", "segment_id"]].copy()
    quarantine["reason"] = reason[reason.ne("")]
    df = df.loc[reason.eq("")].copy()
    # Keep the official held-out annotation; remove whole duplicate essay copies
    # from lower-priority partitions rather than splitting their segments.
    rank = {"train": 0, "validation": 1, "test": 2}
    df["priority"] = df.official_partition.map(rank)
    best = df.groupby("group_id").priority.transform("max")
    overlap = df.priority.ne(best)
    audit["excluded"]["cross_partition_duplicate_rows"] = int(overlap.sum())
    audit["cross_partition_duplicate_groups"] = int(df.loc[overlap].group_id.nunique())
    df = df.loc[~overlap].copy()
    duplicates = df.duplicated("segment_id")
    audit["excluded"]["duplicate_annotation_rows"] = int(duplicates.sum())
    df = df.loc[~duplicates].reset_index(drop=True)
    if df.empty or not df.official_partition.eq("test").any():
        raise ValueError("Need valid labeled data and an official test partition")
    df["label"] = df.label.astype(int)
    df["split"] = df.official_partition
    train = df.loc[df.official_partition.eq("train")]
    validation = df.loc[df.official_partition.eq("validation")]
    if len(validation):
        calibration = validation.iloc[_folds(validation, 2, config["seed"])[0]].index
        df.loc[train.index, "split"] = "fit"
        df.loc[calibration, "split"] = "calibration"
    else:
        folds = _folds(train, 10, config["seed"])
        df.loc[train.index, "split"] = "fit"
        df.loc[train.iloc[folds[0]].index, "split"] = "calibration"
        df.loc[train.iloc[folds[1]].index, "split"] = "validation"
    assert_disjoint(df)
    for split, rows in df.groupby("split"):
        if set(rows.label) != {0, 1, 2}:
            raise ValueError(f"Partition {split} is missing a class; audit before training")
    essay_columns = ["group_id", "essay_id_comp", "full_text", "split"] + [c for c in ["prompt_name", "assignment", "task"] + DEMOGRAPHICS if c in df]
    essays = df[essay_columns].drop_duplicates("group_id")
    segment_columns = ["segment_id", "group_id", "discourse_text", "discourse_type", "discourse_start", "discourse_end", "original_discourse_start", "original_discourse_end", "span_alignment", "label", "split", "source_file", "source_row"]
    root.mkdir(parents=True, exist_ok=True)
    essays.to_csv(root / "essays.csv.gz", index=False)
    df[segment_columns].to_csv(root / "segments.csv.gz", index=False)
    quarantine.to_csv(root / "quarantine.csv.gz", index=False)
    manifest = df[["segment_id", "group_id", "split"]].sort_values("segment_id")
    manifest.to_csv(root / "split_manifest.csv.gz", index=False)
    audit["split_digest"] = digest(manifest.to_dict("records"))
    audit["splits"] = {split: {"segments": len(rows), "essays": rows.group_id.nunique(), "class_counts": {str(k): int(v) for k, v in rows.label.value_counts().items()}, "discourse_types": {str(k): int(v) for k, v in rows.discourse_type.value_counts().items()}} for split, rows in df.groupby("split")}
    if 'prompt_name' in essays:
        audit['prompt_essay_counts']={str(split):{str(k):int(v) for k,v in rows.prompt_name.value_counts(dropna=False).items()} for split,rows in essays.groupby('split')}
    audit['unique_labeled_essays']=int(essays.group_id.nunique())
    audit["near_duplicate_limit"] = "Exact whitespace-normalized duplicates are checked; semantic near-duplicate exclusion is not claimed."
    audit['prepared_sha256']={name:sha256(root/name) for name in ['essays.csv.gz','segments.csv.gz','split_manifest.csv.gz']}
    write_json(root / "audit.json", audit)
    return audit


def refresh_audit(root):
    """Add descriptive counts without changing the prepared split or examples."""
    root=Path(root); audit=read_json(root/'audit.json')
    essays=pd.read_csv(root/'essays.csv.gz',keep_default_na=False,dtype={'essay_id_comp':str})
    audit['unique_labeled_essays']=int(essays.group_id.nunique())
    if 'prompt_name' in essays:
        audit['prompt_essay_counts']={str(split):{str(k):int(v) for k,v in rows.prompt_name.value_counts(dropna=False).items()} for split,rows in essays.groupby('split')}
    audit['assignment_available_essays']=int(essays.assignment.str.strip().ne('').sum()) if 'assignment' in essays else 0
    if 'raw_field_counts' not in audit:
        audit['raw_field_counts']={}
        for source in audit.get('raw_files',[]):
            path=root/'raw'/source['file']
            columns=pd.read_csv(path,nrows=0).columns
            fields=[name for name in ['full_text','discourse_text','essay_id_comp','discourse_id'] if name in columns]
            counts={'rows':0,**{'empty_'+name:0 for name in fields}}
            ids={name:set() for name in ['essay_id_comp','discourse_id'] if name in fields}
            for chunk in pd.read_csv(path,usecols=fields,dtype=str,keep_default_na=False,chunksize=10000):
                counts['rows']+=len(chunk)
                for name in fields:
                    values=chunk[name].str.strip(); counts['empty_'+name]+=int(values.eq('').sum())
                    if name in ids: ids[name].update(values.loc[values.ne('')])
            for name,values in ids.items():
                counts['distinct_'+name]=len(values)
                counts['repeated_nonempty_'+name+'_rows']=counts['rows']-counts['empty_'+name]-len(values)
            audit['raw_field_counts'][source['file']]=counts
        audit['raw_id_counts_policy']='Repeated supplied IDs are descriptive; essay hashes and canonical segment keys control deduplication, not scientific-notation discourse IDs.'
    segments=pd.read_csv(root/'segments.csv.gz',keep_default_na=False)
    assert_disjoint(segments)
    texts=essays.set_index('group_id',verify_integrity=True).full_text
    mismatches=0
    for row in segments.itertuples(index=False):
        text=texts.at[row.group_id]; start,end=int(row.discourse_start),int(row.discourse_end)
        if not 0<=start<end<=len(text) or ' '.join(text[start:end].split())!=' '.join(row.discourse_text.split()): mismatches+=1
    audit['prepared_span_validation']={'checked_segments':len(segments),'mismatches':mismatches,'comparison':'whitespace-normalized gold text in canonical raw essay'}
    if mismatches: raise ValueError('Prepared discourse offsets/text do not match canonical essays')
    measured={name:sha256(root/name) for name in ['essays.csv.gz','segments.csv.gz','split_manifest.csv.gz']}
    if audit.get('prepared_sha256') and audit['prepared_sha256']!=measured: raise ValueError('Prepared data changed since audit')
    audit['prepared_sha256']=measured
    write_json(root/'audit.json',audit)
    return audit


def assert_disjoint(frame):
    if frame.groupby("group_id").split.nunique().max() > 1:
        raise ValueError("Essay/text leakage between partitions")
    if frame.segment_id.duplicated().any():
        raise ValueError("Duplicate segment keys")


def load_frame(root, split, config, output=None):
    root = Path(root)
    audit=read_json(root/'audit.json')
    for name,expected in audit.get('prepared_sha256',{}).items():
        source=root/name
        if _verified_file(str(source),source.stat().st_mtime_ns,source.stat().st_size)!=expected: raise RuntimeError('Prepared dataset changed since audit')
    if split == "test":
        lock = Path(output or config["output_root"]) / "selection.lock.json"
        if not lock.exists():
            raise RuntimeError("Test is locked. Freeze selection first.")
        state = read_json(lock)
        if state["config_digest"] != digest(config) or state["split_digest"] != read_json(root / "audit.json")["split_digest"]:
            raise RuntimeError("Configuration/data changed after selection was frozen")
        if state.get('prepared_sha256',{})!=audit.get('prepared_sha256',{}): raise RuntimeError('Prepared data provenance changed after freeze')
    segments = pd.read_csv(root / "segments.csv.gz", keep_default_na=False)
    essays = pd.read_csv(root / "essays.csv.gz", keep_default_na=False, dtype={"essay_id_comp": str})
    if split != "development":
        segments = segments.loc[segments.split.eq(split)]
    else:
        segments = segments.loc[~segments.split.eq("test")]
    result = segments.merge(essays.drop(columns="split"), on="group_id", validate="many_to_one")
    result = result.sort_values("segment_id").reset_index(drop=True)
    limit = config.get("context_chars", 1800)
    result["left_context"] = [t[max(0, int(s) - limit):int(s)] for t, s in zip(result.full_text, result.discourse_start)]
    result["right_context"] = [t[int(e):int(e) + limit] for t, e in zip(result.full_text, result.discourse_end)]
    if "assignment" not in result:
        result["assignment"] = ""
    if "prompt_name" not in result:
        result["prompt_name"] = "Unknown"
    return result


@lru_cache(maxsize=32)
def _verified_file(path, modified, size):
    return sha256(path)


def small_fit(frame, seed=42):
    return frame.iloc[_folds(frame, 10, seed)[0]].reset_index(drop=True)
