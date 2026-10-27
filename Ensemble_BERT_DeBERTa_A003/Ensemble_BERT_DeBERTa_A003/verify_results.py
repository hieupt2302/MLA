import csv,gzip,hashlib,json,math
from pathlib import Path
root=Path(__file__).resolve().parent
manifest=json.loads((root/'PACKAGE_MANIFEST.json').read_text())
for name,expected in manifest['files'].items():
    assert hashlib.sha256((root/name).read_bytes()).hexdigest()==expected,name
with gzip.open(root/'results/predictions_validation.csv.gz','rt',encoding='utf-8',newline='') as stream:
    rows=list(csv.DictReader(stream))
assert len({r['segment_id'] for r in rows})==len(rows)
cm=[[0]*3 for _ in range(3)]
for row in rows:
    probabilities=[float(row[f'p_{i}']) for i in range(3)]
    assert all(math.isfinite(p) for p in probabilities)
    label=int(row['label']);assert label in (0,1,2)
    pred=max(range(3),key=lambda i:probabilities[i])
    cm[label][pred]+=1
accuracy=sum(cm[i][i] for i in range(3))/len(rows)
macro_f1=sum(2*cm[i][i]/(sum(cm[i])+sum(cm[j][i] for j in range(3))) for i in range(3))/3
m=json.loads((root/'results/metrics_validation.json').read_text())
assert math.isclose(accuracy,m['accuracy'],abs_tol=1e-12)
assert math.isclose(macro_f1,m['macro_f1'],abs_tol=1e-12)
assert cm==m['confusion_matrix']
print('VERIFIED',len(rows),'segments',len({r['group_id'] for r in rows}),'essays','accuracy',accuracy,'Macro-F1',macro_f1)
