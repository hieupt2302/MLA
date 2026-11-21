Created 4 Python scripts and all 15 PNGs. Build succeeded; all six demo runs passed. `--no-raw` runtimes: **2.11s / 4.24s / 4.86s**. All expected results match; test SHA-256 matches the lock.

Files written under `VIDEO_CA_NHAN/`:

- `build/make_visuals.py`
- `Nguoi_1_Data_Classical_Length/demo/demo_nguoi1.py`
- `Nguoi_2_DeBERTa_Context_Threshold/demo/demo_nguoi2.py`
- `Nguoi_3_TestGovernance_LOPO_Ladder/demo/demo_nguoi3.py`
- `_chung/visuals/intro_label_mix.png`
- Person 1 `visuals/`: `fig18_rf_lopo_15_prompts.png`, `fig09_essay_length_vs_holistic_score.png`, `fig20_error_within_score_by_length.png`, `v1_example_trace_rf.png`, `v2_rf_recall_by_length.png`
- Person 2 `visuals/`: `fig04_context_levels.png`, `fig14_L1_minus_L0_per_class.png`, `fig22_threshold_tradeoff.png`, `v1_case8_L0_vs_L1.png`
- Person 3 `visuals/`: `fig26_test_governance.png`, `fig19_context_ladder_validation.png`, `fig17_lopo_vs_indomain_same_units.png`, `fig23_ten_cases_by_context_level.png`, `v1_case2_ladder.png`

The four new person-specific visuals are **1920×1080**; the shared label mix is **1080×810**. Copied figures retain their source dimensions.

Full stdout with raw CSVs, Person 1:

```text
① TRACE  test row_idx 47,059 (raw record 57,633)
   prompt: Facial action coding system | type: Position
   essay words: 225 -> Q1 (<=315)
   text: "That is all everything you need to know about Mona Lisa and her smile."
   label: "Ineffective" -> id 0
   (Ineffective=0, Adequate=1, Effective=2)
   RF FS-B P(Ineff/Adeq/Eff) = 0.544 / 0.342 / 0.114 -> predicts Ineffective (correct)
   DeBERTa L1 (locked) P(Ineff) = 0.978 -> predicts Ineffective

② ID CHECK  train+val annotated units 144,289 | distinct discourse_id 728
   -> join on row_idx

③ INEFFECTIVE RECALL BY ESSAY-LENGTH QUARTILE (official test, saved predictions)
   quartile          gold Ineff   RF recall   DeBERTa L1 recall
   Q1 (<=315)              2,384     23.3%            45.1%
   Q2 (316-422)              934     13.7%            38.4%
   Q3 (423-566)              598      6.9%            35.6%
   Q4 (>=567)                309      0.6%            35.0%
   RF catches 2 of 309 gold Ineffective units in the longest essays
```

Person 2 (`--theta 0.10`):

```text
① CASE 8  validation row_idx 108,613 | Claim
   Cell phones at school | gold Ineffective
   L0 input: Claim [SEP] Some kids will ask there parents to transfer school
   L0 (locked) P(Ineff/Adeq/Eff) = 0.017 / 0.962 / 0.021 -> Adequate
   L1 input: Claim [SEP] Previous: They will hide them from the teachers .Teachers can't go threw
   the students stuff any way . Just make the kids put them in there locker during class.  If you
   do a lot of the students will dich school any way, to be on there phones. You will just make
   all the kids mad. [SEP] Target: Some kids will ask there parents to transfer school [SEP] Next:
   If you chose policy one you will make the student happy.
   L1 (locked) P(Ineff/Adeq/Eff) = 0.058 / 0.937 / 0.005 -> Adequate

② FLAG IF P(Ineffective) >= θ   (locked L1, validation)
   29,102 units, 1,328 gold Ineffective
   rule          flagged   recall   precision   Macro-F1
   argmax         1,761    44.7%       33.7%      0.581
   θ=0.10         4,633    69.6%       19.9%      0.535
   extra correct flags: 330 | extra false alarms: 2,542
   false alarms per extra catch: 7.7

③ case 8: P(Ineffective) = 0.058 < θ = 0.10 -> not flagged
```

Person 3:

```text
① TEST LOCK   locked_at 2026-10-28T21:15:35.952813+00:00
   n_test 93,677
   sha256 (lock) 8b4cbbda471b313e…
   sha256 (now)  8b4cbbda471b313e… -> matches lock: True
   (labels not read)

② TEST MACRO-F1 RECOMPUTED FROM SAVED PREDICTIONS
   model                       units   recomputed   paper (R2)
   DeBERTa L0                 93,677      0.5613      0.5613
   DeBERTa L1 (locked)        93,677      0.5772      0.5772
   DeBERTa Prompt-Aware       93,677      0.5808      0.5808

③ CASE 2  validation row_idx 10,303 | Evidence
   Car-free cities | gold Ineffective
   level                  P(Ineffective)   prediction
   L0                       0.001          Effective
   L1 (locked)              0.008          Effective
   Prompt-Aware             0.002          Effective
   L1 ±2                    0.028          Effective
   Paragraph                0.832          Ineffective
   L2 source                0.540          Ineffective
   L3 whole, 3 ep           0.733          Ineffective
   L3 whole, 7 ep           0.924          Ineffective

④ LOPO GAP (same validation essays; LOPO minus in-domain Macro-F1)
   A Cowboy Who Rode the Waves: -0.092
   Summer projects: -0.025
   Distance learning: -0.048
```

No discrepancies. No models were retrained or videos rendered; verification used saved predictions and local raw CSVs. No git commit was made.