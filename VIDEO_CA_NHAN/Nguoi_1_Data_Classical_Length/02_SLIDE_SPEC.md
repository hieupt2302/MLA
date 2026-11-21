# Slide spec: Người 1 (dữ liệu, mô hình cổ điển, độ dài)

Role footer: `Group 06 · CLC02 · Role 1: Data, classical models, length`

## Slide 1 | title
title: Predicting the Effectiveness of Argumentative Units
subtitle: Individual video · Role 1: data, classical models and essay length
bullets:
- [tự điền: Full name] · [tự điền: Student ID]
- Group 06 · CLC02 · Machine Learning Applications · November 2026

## Slide 2 | bullets_image
title: The problem: which parts of an essay don't work?
bullets:
- PERSUADE 2.0: 25,996 essays, 237,966 discourse units
- 7 types: Lead, Position, Claim, Counterclaim, Rebuttal, Evidence, Concluding
- Label per unit: Ineffective / Adequate / Effective
- Only 4.5% Ineffective, so we report Macro-F1
- Split by essay; official test (93,677 units) scored once
image: ../_chung/visuals/intro_label_mix.png
caption: Label mix per split (essay-level split, seed 42)
source: Final report §3.4–3.6; table E1_split_label_distribution.csv

## Slide 3 | bullets_image
title: My contribution (weeks 10–11)
bullets:
- Random Forest, Feature Set B: re-built, validation gate 0.526, then test once: 0.510
- RF leave-one-prompt-out on all 15 prompts: 0.350 to 0.501
- Length × holistic-score tables: is length confounded with proficiency?
- Builds on the group's week-9 pipeline and essay-level split (seed 42)
image: visuals/fig18_rf_lopo_15_prompts.png
caption: RF Macro-F1 when each prompt is held out of training (mean 0.430)
source: rf_run_metadata.json; Final report Fig. 6.6, Table 6.5

## Slide 4 | image
title: One real test unit: from raw CSV to a prediction
image: visuals/v1_example_trace_rf.png
caption: Test raw record 57,633 → row_idx 47,059 · Position · "Facial action coding system" · gold Ineffective
source: test CSV; MLA_Final/Results/predictions/test_predictions_rf_feature_set_b.csv, test_predictions_L1.csv

## Slide 5 | bullets_image
title: What the data shows: length goes with proficiency
bullets:
- Essay length vs holistic score: Spearman 0.76 (25,996 essays)
- Median essay: score 2 = 229 words; score 6 = 824 words
- Ineffective share: 9.0% (shortest quartile) → 1.3% (longest)
- Essay length is one of the RF's five structural features
image: visuals/fig09_essay_length_vs_holistic_score.png
caption: Essay length by holistic score (all essays)
source: Final report §3.7.4, Fig. 3.6; R7_L1_errors_by_length_quartile.csv (validation gold %)

## Slide 6 | image
title: Within the same score, errors still rise with length
image: visuals/fig20_error_within_score_by_length.png
caption: Locked DeBERTa L1 error rate by length quartile within each holistic score: (a) validation, (b) test
callout: Score 3: 19.3% → 28.2% · OR per quartile controlling for score = 1.19 [1.14, 1.25]
source: Final report Table 7.2, Table 7.3

## Slide 7 | demo
title: Demo: saved outputs of the final project
bullets:
- python reproduce_results.py: RF row of Table 1
- demo_nguoi1.py ①: trace row_idx 47,059 → RF probabilities
- demo_nguoi1.py ②: discourse_id check (728 IDs for 144,289 units)
- demo_nguoi1.py ③: Ineffective recall by essay-length quartile

## Slide 8 | image
title: Interpreting one result: the forest leans on essay length
image: visuals/v2_rf_recall_by_length.png
caption: Ineffective recall on the official test by essay-length quartile, from saved predictions
callout: RF finds 23.3% of Ineffective units in the shortest essays but 0.6% (2 of 309) in the longest
source: computed by demo_nguoi1.py from test_predictions_rf_feature_set_b.csv and test_predictions_L1.csv; RF OR 1.31: Final report §7.2

## Slide 9 | bullets
title: Summary and evidence
bullets:
- RF Feature Set B: validation gate 0.526 → official test 0.510 (one pass)
- RF LOPO, 15 prompts: 0.350–0.501; four of the five hardest are source-based
- Length ≈ proficiency (ρ 0.76), yet errors rise with length within a score (OR 1.19)
- First-version errors (ID join, RF config) fixed in the 31 Oct review
- Files: Person1/, week10_output_person1/, outputs/lopo_classical_results.csv
callout: Limitation: no re-training without the length feature yet, so length reliance is inferred, not tested
