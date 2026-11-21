from pathlib import Path
import argparse
import sys
sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "build"))
import make_visuals as data

import hashlib
from decimal import Decimal
from sklearn.metrics import f1_score

def main():
    parser = argparse.ArgumentParser(description="Check test lock and saved prediction metrics.")
    parser.add_argument("--no-raw",action="store_true")
    args = parser.parse_args()
    lock = data.lock()
    print(f"① TEST LOCK   locked_at {lock['locked_at']}")
    print(f"   n_test {lock['n_test']:,}")
    print(f"   sha256 (lock) {lock['test_sha256'][:16]}…")
    path = data.raw_path("test")
    if args.no_raw or not path.exists():
        print("   Note: optional raw test CSV unavailable/skipped; hash check not performed.")
    else:
        try:
            sha = hashlib.sha256()
            with path.open('rb') as f:
                for chunk in iter(lambda: f.read(8*1024*1024),b''):
                    sha.update(chunk)
            actual = sha.hexdigest()
            print(f"   sha256 (now)  {actual[:16]}… -> matches lock: {actual == lock['test_sha256']}")
            print("   (labels not read)")
        except OSError as exc:
            print(f"   Note: optional hash check unavailable ({type(exc).__name__}).")
    print("\n② TEST MACRO-F1 RECOMPUTED FROM SAVED PREDICTIONS")
    print("   model                       units   recomputed   paper (R2)")
    for key,name in [("L0","DeBERTa L0"),("L1","DeBERTa L1 (locked)"),("PA","DeBERTa Prompt-Aware")]:
        df = data.predictions("test",key)
        assert len(df) == lock['n_test']
        value = f1_score(df.true_label,df.pred_label,labels=[0,1,2],average='macro')
        r2 = data.table("R2_test_per_class.csv")
        paper = r2[r2.system.str.contains("Prompt-Aware" if key == 'PA' else key)].iloc[0].macro_f1
        print(f"   {name:<25} {len(df):>7,}      {value:.4f}      {paper:.4f}")
    r8 = data.table("R8_ten_cases.csv").query('case == 2').iloc[0]
    print(f"\n③ CASE {r8['case']}  validation row_idx {r8.row_idx:,} | {r8['type']}")
    print(f"   {r8.prompt} | gold {r8.gold}")
    print("   level                  P(Ineffective)   prediction")
    row = data.ladder()
    names = {'Ineff':'Ineffective','Adeq':'Adequate','Eff':'Effective'}
    for key,name in data.LEVELS:
        print(f"   {name:<24} {row[f'P_ineff_{key}']:.3f}          {names[row[f'pred_{key}']]}")
    print("\n④ LOPO GAP (same validation essays; LOPO minus in-domain Macro-F1)")
    r5 = data.table('R5_lopo_vs_indomain_per_class.csv')
    for prompt, group in r5.groupby('held_out_prompt',sort=False):
        lopo = group[group.setting.str.startswith('LOPO') & group.setting.str.contains('validation essays')].iloc[0]
        domain = group[group.setting.str.startswith('In-domain')].iloc[0]
        print(f"   {prompt}: {Decimal(str(lopo.macro_f1)) - Decimal(str(domain.macro_f1)):+.3f}")

if __name__ == "__main__":
    main()
