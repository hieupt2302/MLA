# Slide spec, 5-minute version: Người 2

Role footer: `Group 06 · CLC02 · Role 2: DeBERTa, context, threshold`

## Slide 1 | title
title: Predicting the Effectiveness of Argumentative Units
subtitle: Individual video · Role 2: DeBERTa, local context and the decision threshold
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
- Week 9: DeBERTa-v3 vs Random Forest, same units: +0.054 [0.043, 0.065]
- Week 10: controlled test, L0 (unit) vs L1 (± 1 unit), all else fixed
- Week 11: threshold scan for the Ineffective flag; case 8
- Week 11: linear SVM on test (0.482) and on 3 held-out prompts
image: visuals/fig04_context_levels.png
caption: Context levels: L0 and L1 are the planned comparison
source: Final report §4.3, §6.1, Table 6.5, Table 6.6

## Slide 4 | image
title: One real unit (case 8): what DeBERTa reads, what it says
image: visuals/v1_case8_L0_vs_L1.png
caption: Validation row_idx 108,613 · Claim · "Cell phones at school" · gold Ineffective
source: val_predictions_L0.csv, val_predictions_L1.csv (locked week-11 models); Final report Table 7.4–7.5

## Slide 5 | demo
title: Demo: saved outputs of the final project
bullets:
- python MLA_Final/Code/reproduce_results.py: TABLE 2 (L1 − L0)
- demo_nguoi2.py ①: rebuild the L0 / L1 input of case 8
- demo_nguoi2.py ②: flag if P(Ineffective) ≥ θ, θ = 0.10
- demo_nguoi2.py ③: is case 8 flagged?

## Slide 6 | bullets_image
title: Results: L1 − L0 on the same units
bullets:
- Test: Macro-F1 +0.0159 [+0.0115, +0.0205]
- Largest gain: Ineffective F1 +0.0292
- By type: Counterclaim +0.037, Rebuttal +0.028, Claim +0.028
- First run: only +0.002 on validation, so the gain is "small"
image: visuals/fig14_L1_minus_L0_per_class.png
caption: L1 minus L0 per class, 95% essay-bootstrap CI (2,000 resamples)
source: Final report Table 6.2, Table 6.4; R4a_L1_vs_L0_same_units_deltas.csv

## Slide 7 | image
title: Limitation: a threshold moves the operating point
image: visuals/fig22_threshold_tradeoff.png
caption: Locked L1, validation: recall, precision and Macro-F1 as θ changes (dotted: argmax)
callout: θ = 0.10: recall 44.7% → 69.6%, Macro-F1 0.581 → 0.535, about 8 false alarms per extra catch. Case 8 (0.058) is not flagged
source: Final report Table 6.8, Fig. 6.8
