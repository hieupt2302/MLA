"""Report displayed numbers absent from the approved saved evidence (never a gate)."""
import csv
import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VIDEO = ROOT / 'VIDEO_CA_NHAN'
NUMBER = re.compile(r'(?<![\w.])([+−-]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?)(%?)(?!\w|\.\d|,\d)')


def scrub(line):
    line = re.sub(r'\b\d{4}-\d{2}-\d{2}(?:T[\d:]+(?:Z)?)?', '', line)
    line = re.sub(r'\b\d{1,2}/\d{1,2}/\d{4}\b|\b\d{1,2}:\d{2}\b', '', line)
    line = re.sub(r'\b(?:Slide|SLIDE)\s+\d+\b|\b2026\b', '', line)
    line = re.sub(r'\b\d{1,2}\s+(?:Oct(?:ober)?|Nov(?:ember)?)\b', '', line)
    return line


def tokens(line):
    for m in NUMBER.finditer(scrub(line)):
        token = m[1].replace(',', '').replace('−', '-')
        precision = len(token.split('.')[1]) if '.' in token else 0
        percent = bool(m[2]) or bool(re.match(r'\s*(?:percent\b|–\d+(?:\.\d+)?%)', scrub(line)[m.end():]))
        yield m[0], float(token), precision, percent


def known_values():
    values = set()
    paths = sorted((ROOT / 'MLA_Final/Results/tables').glob('*.csv'))
    paths += [ROOT / 'MLA_Final/Results/predictions/context_levels_10_cases.csv']
    paths += sorted((ROOT / 'VAN_DAP_4_TIEU_CHI/trace_mau_that/outputs').glob('*.csv'))
    def add(value):
        if isinstance(value, bool) or value is None:
            return
        if isinstance(value, (int, float)):
            if math.isfinite(value):
                values.add(float(value))
        elif isinstance(value, dict):
            for child in value.values():
                add(child)
        elif isinstance(value, list):
            for child in value:
                add(child)
        elif isinstance(value, str):
            try:
                numeric = float(value.replace(',', '').replace('−', '-'))
            except ValueError:
                pass
            else:
                if math.isfinite(numeric):
                    values.add(numeric)
                return
            for _, number, _, percent in tokens(value):
                values.add(number / 100 if percent else number)
    for path in paths:
        if path.is_file():
            with path.open(encoding='utf-8-sig', newline='') as stream:
                for row in csv.reader(stream):
                    for cell in row:
                        add(cell)
    configs = sorted((ROOT / 'MLA_Final/Code/configs').glob('*.json'))
    reports = sorted((ROOT / 'final_report/report_src').glob('*.md'))
    for path in configs:
        add(json.loads(path.read_text(encoding='utf-8-sig')))
    for path in reports:
        add(path.read_text(encoding='utf-8-sig'))
    assert paths and configs and reports and values, 'Evidence inputs are missing'
    return values, len(paths) + len(configs) + len(reports)


def rounded_values(values, precision):
    return {round(v * scale, precision) for v in values for scale in (1, 100, .01)}


def run():
    values, count = known_values()
    cache = {}
    def verified(value, precision, percent):
        key = precision, percent
        if key not in cache:
            # Percentage/fraction equivalence is symmetric, including explicit % evidence.
            cache[key] = rounded_values(values, precision)
        return round(value, precision) in cache[key]
    assert .577 in rounded_values({.5772}, 3)
    assert .578 not in rounded_values({.5772}, 3)
    assert 19.3 in rounded_values({.1932}, 1)
    assert -.092 in rounded_values({-.0918}, 3)
    assert list(tokens('1:15–2:45 Slide 4 2026 −0.092 144,289')) == [('−0.092', -.092, 3, False), ('144,289', 144289., 0, False)]
    print(f'Known evidence: {len(values):,} distinct numeric values from {count} files.')
    for folder in sorted(VIDEO.glob('Nguoi_*')):
        runbook = (folder / '03_DEMO_RUNBOOK.md').read_text(encoding='utf-8-sig')
        expected = re.search(r'## Output[^\n]*\n(.*?)(?=\n## |\Z)', runbook, re.S)
        demo = list(tokens(expected[1] if expected else ''))
        general, demo_only, total = [], [], 0
        for filename in [f for f in ('01_SCRIPT_EN.md', '02_SLIDE_SPEC.md', '01_SCRIPT_EN_5MIN.md', '02_SLIDE_SPEC_5MIN.md') if (folder / f).is_file()]:
            for line_no, line in enumerate((folder / filename).read_text(encoding='utf-8-sig').splitlines(), 1):
                for display, value, precision, percent in tokens(line):
                    total += 1
                    if not verified(value, precision, percent):
                        row = f'{filename}:{line_no} | {display} | {line.strip()}'
                        target = demo_only if any(round(v, precision) == round(value, precision) for _, v, _, _ in demo) else general
                        target.append(row)
        lines = [f'{folder.name}: {total} tokens; {total-len(general)-len(demo_only)} verified; '
                 f'{len(general)+len(demo_only)} unverified occurrences.',
                 '', 'UNVERIFIED — absent from approved evidence', 'File:line | Number | Context', *general,
                 '', 'UNVERIFIED — also present in runbook expected output (demo-derived candidates)',
                 'File:line | Number | Context', *demo_only]
        if not general:
            lines.insert(4, '(none)')
        if not demo_only:
            lines.append('(none)')
        report = '\n'.join(lines) + '\n'
        out = folder / 'output'
        out.mkdir(exist_ok=True)
        (out / 'number_check.txt').write_text(report, encoding='utf-8')
        print('\n' + report)


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    run()
