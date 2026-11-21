# Slide spec, 5-minute version: Người 3

Role footer: `Group 06 · CLC02 · Role 3: Test governance, LOPO, context ladder`

## Slide 1 | title
title: Predicting the Effectiveness of Argumentative Units
subtitle: Individual video · Role 3: official test, unseen prompts and wider context
bullets:
- [tự điền: Full name] · [tự điền: Student ID]
- Group 06 · CLC02 · Machine Learning Applications · November 2026

## Slide 2 | bullets_image
title: The problem: which parts of an essay don't work?
bullets:
- PERSUADE 2.0: 25,996 essays, 237,966 discourse units
- Label per unit: Ineffective / Adequate / Effective
- Only 4.5% Ineffective, so we report Macro-F1
- Split by essay; official test (93,677 units) scored once
image: ../_chung/visuals/intro_label_mix.png
caption: Label mix per split (essay-level split, seed 42)
source: Final report §3.4–3.6; table E1_split_label_distribution.csv

## Slide 3 | bullets_image
title: My contribution and method
bullets:
- Trained DeBERTa L0 / L1 / Prompt-Aware; test scored once (lock: 28 Oct)
- Test Macro-F1: L0 0.561 · L1 (locked) 0.577 · PA 0.581
- Re-ran LOPO with a fixed 3 epochs; context ladder up to the whole essay
- Week 9 (one line): data pipeline and essay-level split
image: visuals/fig26_test_governance.png
caption: Test governance: every choice on validation; test hashed, locked and scored once
source: OFFICIAL_TEST_LOCK.json; Final report Table 6.5, Fig. 5.1

## Slide 4 | image
title: One real unit (case 2) through the context ladder
image: visuals/v1_case2_ladder.png
caption: Validation row_idx 10,303 · Evidence · "Car-free cities" · score 2 · gold Ineffective
source: MLA_Final/Results/predictions/context_levels_10_cases.csv; trace notebook tokens_per_level.csv; Final report Table 7.5

## Slide 5 | demo
title: Demo: saved outputs of the final project
bullets:
- python MLA_Final/Code/reproduce_results.py: TABLE 1 (test), TABLE 3 (LOPO)
- demo_nguoi3.py ①: SHA-256 of test file = lock file?
- demo_nguoi3.py ②: recompute test Macro-F1 from saved predictions
- demo_nguoi3.py ③: case 2 across the ladder

## Slide 6 | table
title: Results: unseen prompts cost Macro-F1 (same essays)
table:
| Held-out prompt | Units / essays | In-domain | LOPO | Gap [95% CI] |
|---|---|---:|---:|---|
| A Cowboy Who Rode the Waves | 1,030 / 134 | 0.476 | 0.384 | −0.092 [−0.132, −0.049] |
| Summer projects | 2,074 / 177 | 0.508 | 0.483 | −0.025 [−0.052, +0.011] |
| Distance learning | 3,533 / 283 | 0.576 | 0.528 | −0.048 [−0.078, −0.019] |
callout: Wider context: under argmax, no input beyond L1 is clearly better on validation (29,102 units)
source: Final report Table 6.7, Table 6.10; R5_lopo_vs_indomain_per_class.csv

## Slide 7 | table
title: One error: the first LOPO run leaked
table:
| Held-out prompt (all units) | Week 10 run | Re-run (31 Oct) |
|---|---:|---:|
| A Cowboy Who Rode the Waves | 0.408 | 0.402 |
| Summer projects | 0.464 | 0.438 |
| Distance learning | 0.574 | 0.538 |
| Distance: gap vs in-domain | +0.004 | −0.048 |
callout: Limitation: 3 prompts, 1 run each; the source-based link is an interpretation, not a tested cause
source: RA_SOAT_TUAN11_SO_VOI_NHAN_XET_TUAN10.md B16, B27; week11_lopo_rerun/; R5
