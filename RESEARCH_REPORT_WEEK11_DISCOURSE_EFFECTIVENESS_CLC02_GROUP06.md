# TECHNICAL RESEARCH REPORT (WEEK 11) — OFFICIAL TEST EVALUATION AND RESPONSE TO THE WEEK 10 REVIEW
## Discourse-unit effectiveness prediction on PERSUADE 2.0: length vs. proficiency, one-pass official test, LOPO, and decision thresholds

**Course:** Machine Learning & Applications (CLC02) | **Group:** 06 | **Dataset:** PERSUADE 2.0 (Crossley et al., 2024) | **Date:** 31 October 2026
**Code and outputs:** `outputs/`, `Person1/`, `Person2Khoa/`, `Week11_Person3_DeBERTa_OfficialTest/`
**Review log for this revision:** `RA_SOAT_TUAN11_SO_VOI_NHAN_XET_TUAN10.md`

**Colab notebooks**
* Person 1 (length × proficiency, RF official test): `Person1/script_holistic_length_table.ipynb`, `Person1/run_rf_official_test.ipynb` — https://colab.research.google.com/drive/1YRMpJgGzZ0vWe7nA0W8c7n5JKMruVJHT?usp=sharing
* Person 2 (threshold analysis, Linear SVM LOPO and test): `Person2Khoa/Person2Khoa/*.ipynb` — https://colab.research.google.com/drive/1prcSnRHax0SAITnUbGsXks3aQ9pbwJD2?usp=sharing
* Person 3 (DeBERTa L0 / L1 / Prompt-Aware, official test): `Week11_Person3_DeBERTa_OfficialTest/07_person3_prompt_aware_official_test.ipynb` — https://colab.research.google.com/drive/1xiYMZ7SjRSAn_ioAvAbNh-PZDkghsiBk?usp=sharing

---

## Abstract

We classify each annotated discourse unit of a student argumentative essay as Ineffective, Adequate or Effective. This week answers the Week 10 review and runs the official test once.

1. **Length vs. proficiency (Requirement 3).** Within the same holistic score, the error rate of DeBERTa Level 1 still rises with essay length. For score-3 essays it goes from 19.3% (shortest quartile) to 28.2% (longest) on validation, and from 17.6% to 29.2% on the official test. A logistic regression with essay-clustered errors gives an odds ratio of 1.19 [1.14, 1.25] per length quartile after controlling for holistic score. It stays at 1.17 [1.11, 1.23] after also controlling for the gold label and discourse type. Proficiency shift explains why the *type* of error changes with length: in the longest quartile, 92% of errors are Adequate↔Effective confusions. It does not explain the whole *rise* in error. Hypothesis A (length/complexity) is therefore **not ruled out**, and we report both explanations. An earlier version of this table showed flat error rates; that table came from a join on corrupted IDs (Section 2.3) and is withdrawn.
2. **Official test, one pass (Requirement 2; 93,677 units, 10,402 essays).** The protocol systems scored Macro-F1: Random Forest Feature Set B **0.5098**, DeBERTa-v3 Level 0 **0.5613**, and DeBERTa-v3 Level 1, the locked system, **0.5772**. The exploratory Prompt-Aware model scored 0.5808, and a supplementary Linear SVM scored 0.4822. Level 1 beats Level 0 by +0.0159 [0.0115, 0.0207] (essay bootstrap). Prompt-Aware vs. Level 1 is +0.0036 [−0.0002, 0.0074], so they cannot be distinguished. All three DeBERTa models beat RF by 0.05–0.07 Macro-F1. The DeBERTa models scored on test were retrained this week with the locked configuration. On validation they give L1 − L0 = +0.0087 [0.0014, 0.0161], whereas the Week 10 training run gave +0.0022 (CI containing 0). The L0/L1 difference is therefore of the same order as run-to-run variation.
3. **Lowering the Ineffective threshold.** At P(Ineffective) ≥ 0.10, 3,670 of 29,102 validation predictions change, and 2 of the 10 studied failure cases (cases 5 and 8) flip to Ineffective. Recall for Ineffective rises from 43.2% to 73.0%. Precision falls from 36.1% to 18.4%, and Macro-F1 falls from 0.579 to 0.517: about 8 new false alarms per newly caught Ineffective unit.
4. **LOPO.** On the *same* validation units, DeBERTa trained without the prompt loses 0.088 Macro-F1 [−0.138, −0.041] on *A Cowboy Who Rode the Waves*. For *Summer projects* (−0.009) and *Distance learning* (+0.004), the confidence intervals include zero.

---

## 1. Response to the Week 10 review

| # | Review item | What we did | Where |
|---|---|---|---|
| 1 | **[Required]** Rewrite the conclusion in 7.2 so that it no longer says the data "prove" a ceiling caused by missing input; add a sentence on label reliability | Rewritten as a hypothesis consistent with, but not tested by, our data. We also removed "prove", "definitively" and "conclusively" from the whole report. Added the inter-rater κ = 0.316 sentence | §8 |
| 2 | **[Required]** Score RF (Feature Set B), DeBERTa L0 and L1 in the same test run; state that L0 and L1 were indistinguishable on validation | Protocol in §1.1 lists the three systems and states this. Test table has the three protocol rows plus two clearly labelled extra rows. We found the first RF test script did **not** implement Feature Set B; the corrected run is reported, and the old number is kept in a footnote | §1.1, §7 |
| 3 | **[Required]** Error rate by length quartile *within* each holistic score, plus one sentence answering whether error rises with length within a score | Table with N and essay-bootstrap CIs, clustered regression, repeated on the test set as a descriptive check. Answer: **yes, it rises**; both hypotheses are kept | §3 |
| 4 | **[Suggested]** Treat "paragraph 36" (case 2) as a hypothesis, or check the source text | Checked: the numbered *Car-free cities* source set has 43 paragraphs, and paragraph 36 contains exactly the sentence the student quotes. Our earlier "fabricated citation" reading was wrong and is withdrawn | §5.2 |
| 5 | **[Suggested]** Export the final version from Word/LaTeX | Final version exported to `.docx` from this Markdown source | `Week11_Group06_CLC02_Report.docx` |
| — | Interview walk-through, step 5: lower the Ineffective threshold on the saved probabilities and count how many cases change | Done; counts in §5.3 | §5.3 |

### 1.1 Test protocol (fixed before the test was opened)

* **Primary systems, all scored in the same pass:** (1) Random Forest, Feature Set B (Week 9 configuration); (2) DeBERTa-v3-base Level 0 (`[type] [SEP] unit`); (3) DeBERTa-v3-base Level 1 (`[type] [SEP] Previous: … [SEP] Target: … [SEP] Next: …`), the locked system.
* **Validation status at lock time:** in the Week 10 run, L0 and L1 could not be distinguished on validation: +0.0022 Macro-F1, 95% essay-bootstrap CI containing 0. L1 was locked because of its higher Ineffective F1 (+0.019), not because it was clearly better.
* **Extra systems, labelled as such:** Prompt-Aware DeBERTa (planned in Week 11: L1 input prefixed with `Prompt: <prompt name> [SEP]`) and Linear SVM on TF-IDF. Neither was part of the Week 10 protocol.
* **Fixed configuration:** `microsoft/deberta-v3-base`, max length 512, batch 8 × gradient accumulation 4, lr 2e-5, 10% warmup, 3 epochs, class-weighted cross-entropy (weights 7.48 / 0.43 / 1.95), seed 42, best epoch selected on validation Macro-F1. Essay-level paired bootstrap with 2,000 resamples.
* **Rule:** one scoring pass. No threshold, hyperparameter or model choice uses the test set. The lock file `Week11_Person3_DeBERTa_OfficialTest/outputs/week11_person3/OFFICIAL_TEST_LOCK.json` records the test file hash and model paths.

**Deviations, reported openly.**
(a) The Week 10 DeBERTa checkpoints could no longer be loaded correctly, so L0, L1 and Prompt-Aware were **retrained** in one Colab A100 run with the configuration above (transformers 4.57.6, bf16). Section 4.2 gives their own validation scores. The models scored on test are these retrained models, not the Week 10 checkpoints.
(b) The run went from training to validation to test in a single session, because an earlier session was lost when the Colab VM was reclaimed. Validation results were logged before test inference but were not reviewed by a person in between.
(c) The first RF test script trained a different model: 100 trees, depth 30, 10k TF-IDF features, min_df 3, one unscaled length feature, trained on train+validation. That run gave Macro-F1 0.4834 and is not Feature Set B. We re-implemented Feature Set B exactly as in Week 9 and trained it on the same 115,187 training units. The script refuses to score the test unless it first reproduces the Week 9 validation Macro-F1 (0.5261 vs 0.5230; scikit-learn 1.6.1, as in Week 9). It was then scored once. No setting was changed after seeing test results.

### 1.2 The Week 8 "6.13% accuracy" defect (for the interview)
`LogisticRegression.classes_` sorts labels alphabetically (`Adequate, Effective, Ineffective`), while our evaluation assumed index 0 = Ineffective. Ineffective F1 (≈0.061) was therefore written into the accuracy field. After fixing the label mapping, LR with tuned thresholds reaches Macro-F1 0.5086 and balanced accuracy 60.32% on validation.

---

## 2. Data

### 2.1 Units and split

| Stage | Train (80%) | Validation (20%) | Official test |
|---|:---:|:---:|:---:|
| Rows in source CSV | 173,266 (train + validation) | — | 112,117 |
| Unannotated segments removed | 28,977 | — | 18,440 |
| Annotated units | 115,187 | 29,102 | 93,677 |
| Essays (`essay_id_comp`) | 12,475 | 3,119 | 10,402 |
| Split | GroupShuffleSplit by essay, seed 42 | same | official holdout |
| Essays shared with another split | 0 | 0 | 0 |

### 2.2 One real unit through the pipeline (validation case 8)
* `row_idx` 108613, essay `FE3141FA4163`, prompt *Cell phones at school*, holistic score 2, essay length 169 words. Unit type **Claim**, gold label **Ineffective** (id 0).
* **Level 0 input:** `Claim [SEP] Some kids will ask there parents to transfer school`
* **Level 1 input:** `Claim [SEP] Previous: They will hide them from the teachers … You will just make all the kids mad. [SEP] Target: Some kids will ask there parents to transfer school [SEP] Next: If you chose policy one you will make the student happy.`
* **Prompt-Aware input:** `Prompt: Cell phones at school [SEP]` + Level 1 input.
* **Predicted probabilities (Ineffective / Adequate / Effective), Week 11 models:** L0 0.017 / 0.962 / 0.021; L1 0.058 / 0.937 / 0.005; PA 0.217 / 0.778 / 0.005. All three predict Adequate, so all three are wrong. The Week 10 Level 1 model gave P(Ineffective) = 0.124 for this unit.

### 2.3 Data-integrity note
The CSV files we received had been saved through a spreadsheet program, which rounded numeric IDs to scientific notation (for example `discourse_id = 1.62263E+12`). As a result, 144,289 annotated units carry only **728** distinct `discourse_id` values. `essay_id` is mostly intact (one collision merging two essays into one split group, which cannot cause leakage), and `essay_id_comp` is intact. Every analysis in this report joins units by row position (`row_idx`) or by `essay_id_comp`, and each join is checked against discourse type and gold label. The Week 11 length table first circulated in the group joined on `discourse_id` and was therefore wrong; Section 3 replaces it.

---

## 3. Essay length vs. writer proficiency (Requirement 3)

### 3.1 Question
Errors rise with essay length. **Hypothesis A:** something about longer essays makes units harder to classify. **Hypothesis B:** longer essays come from stronger writers; their units are more often Adequate or Effective, and that boundary is harder. The review asked us to compare length quartiles **within the same holistic score**.

All numbers below use one model throughout, DeBERTa Level 1 (the locked system, Week 11 run). Quartile cut points are fixed from the validation set (≤315, 316–422, 423–566, ≥567 words).

### 3.2 Without controlling for proficiency

| Length quartile | Units | Essays | Mean holistic score (per essay) | % Ineffective | % Effective | Error rate (val) | Errors that are Adequate↔Effective (val) | Error rate (test) |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Q1 (≤315) | 7,333 | 1,037 | 2.38 | 8.97 | 5.29 | 22.0% | 47.5% | 21.1% |
| Q2 (316–422) | 7,277 | 786 | 3.20 | 5.02 | 10.72 | 23.0% | 67.1% | 22.0% |
| Q3 (423–566) | 7,226 | 690 | 3.81 | 2.92 | 18.34 | 27.9% | 83.8% | 25.5% |
| Q4 (≥567) | 7,266 | 606 | 4.67 | 1.29 | 32.81 | 30.5% | 92.0% | 30.4% |

### 3.3 Within the same holistic score (validation, 29,102 units)
Error rate (%) with 95% essay-bootstrap CI; N = units / essays.

| Holistic score | Q1 (≤315) | Q2 (316–422) | Q3 (423–566) | Q4 (≥567) |
|:---:|:---:|:---:|:---:|:---:|
| 1 | 39.6 [32.6, 45.6]; 356/91 | 22.2 [12.9, 32.7]; 63/19 | 33.8 [15.8, 51.1]; 74/13 | 34.8 [16.7, 64.3]; 23/4 |
| 2 | 23.2 [21.3, 25.1]; 3,200/493 | 31.4 [27.1, 35.6]; 722/91 | 33.2 [26.3, 39.5]; 295/34 | 38.8 [27.9, 51.0]; 80/11 |
| **3** | **19.3** [17.7, 21.1]; 3,517/424 | **21.8** [20.0, 23.9]; 3,743/404 | **22.9** [19.8, 26.0]; 1,465/143 | **28.2** [22.1, 34.3]; 472/40 |
| **4** | **19.6** [13.4, 26.6]; 260/29 | **22.0** [19.9, 23.9]; 2,622/260 | **28.5** [26.5, 30.5]; 3,984/379 | **31.1** [28.2, 33.9]; 1,961/174 |
| 5 | — | 29.1 [21.3, 38.0]; 127/12 | 30.3 [26.9, 34.0]; 1,391/120 | 31.7 [29.6, 34.0]; 3,336/277 |
| 6 | — | — | — | 26.8 [24.2, 29.7]; 1,394/100 |

Same table on the official test (descriptive only; no choice depends on it), scores 3 and 4:

| Holistic score | Q1 | Q2 | Q3 | Q4 |
|:---:|:---:|:---:|:---:|:---:|
| 3 | 17.6 [16.8, 18.5]; 13,684/1,662 | 20.8 [19.7, 21.9]; 10,596/1,150 | 22.3 [20.8, 24.1]; 4,597/459 | 29.2 [26.2, 32.3]; 1,618/154 |
| 4 | 23.1 [19.4, 26.8]; 1,267/139 | 22.4 [21.3, 23.7]; 9,131/910 | 25.1 [24.0, 26.2]; 11,755/1,101 | 29.7 [27.8, 31.5]; 4,404/387 |

### 3.4 Regression (essay-clustered standard errors)
Logistic regression of unit error on length quartile (0–3). The table gives the odds ratio per quartile.

| Model specification | Validation OR [95% CI] | Test OR [95% CI] |
|---|:---:|:---:|
| Length only | 1.17 [1.14, 1.21] | 1.18 [1.16, 1.20] |
| + holistic score | 1.19 [1.14, 1.25] | 1.16 [1.13, 1.19] |
| + holistic score + gold label + discourse type | 1.17 [1.11, 1.23] | 1.13 [1.10, 1.16] |
| Score-3 essays only | 1.15 [1.06, 1.24] | 1.21 [1.16, 1.26] |
| Score-4 essays only | 1.27 [1.17, 1.37] | 1.17 [1.11, 1.23] |

The same pattern holds for DeBERTa L0 and for RF (OR 1.16 and 1.31 after controlling for score; `outputs/length_within_score_regression.csv`).

### 3.5 Answer
**Within the same holistic score, the error rate still increases with essay length.** Controlling for proficiency does not shrink the length effect. Controlling also for the gold label and the discourse type shrinks it only slightly. Hypothesis A is therefore not ruled out. What proficiency does explain is the change in error *type*: short essays contain most of the Ineffective units, while in the longest quartile 92% of errors are Adequate↔Effective confusions.

Possible reasons for the remaining length effect, none tested yet:
* The model never sees the whole essay, so "attention overload on long input" is not a plausible mechanism. More plausible: units in long essays are themselves longer, and the Level 1 input (unit plus neighbours) is more often truncated at 512 tokens.
* Raters may judge a unit relative to the rest of a long, developed essay, which a local model cannot see.
* Holistic score is coarse (six levels), so some proficiency difference may remain inside each score.

The Week 10 statement "errors rise with length because long essays are written by stronger students" is therefore only part of the explanation.

---

## 4. Context ablation (Level 0 vs. Level 1)

### 4.1 Week 10 training run (validation, 29,102 units)

| Metric | RF Feature Set B | DeBERTa L0 | DeBERTa L1 | L1 − L0 |
|---|:---:|:---:|:---:|:---:|
| Macro-F1 | 0.5230 | 0.5768 | 0.5790 | +0.0022 (CI contains 0) |
| Accuracy | 77.22% | 73.88% | 73.09% | −0.79 pts |
| F1 Ineffective | 0.2384 | 0.3741 | 0.3934 | +0.0193 |
| Precision / Recall Ineffective | 26.7% / 21.5% | 32.0% / 45.0% | 36.1% / 43.2% | +4.1 / −1.8 pts |
| F1 Adequate | 0.8591 | 0.8245 | 0.8166 | −0.0079 |
| F1 Effective | 0.4713 | 0.5317 | 0.5270 | −0.0047 |

By discourse type, Level 1 raised Ineffective F1 for Claim (+0.043), Concluding Statement (+0.039) and Counterclaim (+0.030), and lowered it for Position (−0.055).

### 4.2 Week 11 retraining run (models scored on the test)

| Metric (validation) | L0 | L1 | Prompt-Aware |
|---|:---:|:---:|:---:|
| Macro-F1 | 0.5723 | 0.5809 | 0.5855 |
| Accuracy | 72.91% | 74.17% | 74.06% |
| F1 Ineffective | 0.3755 | 0.3846 | 0.3925 |
| Recall Ineffective | 42.8% | 44.7% | 48.8% |
| Cohen κ / QWK | 0.363 / 0.433 | 0.374 / 0.445 | 0.380 / 0.455 |

Paired essay bootstrap on validation: L1 − L0 = +0.0087 [0.0014, 0.0161]; PA − L1 = +0.0045 [−0.0025, 0.0113].
Between the two training runs, the same configuration moved by −0.0045 (L0) and +0.0019 (L1). The L1 − L0 gap went from +0.0022 to +0.0087. Bootstrap intervals only capture sampling of essays, not training randomness, so a single-seed L1 − L0 difference of this size should be read with care.

---

## 5. Failure cases and decision thresholds

### 5.1 Ten high-confidence Ineffective failures, Level 0 vs. Level 1 (Week 10 models)
None of the 10 cases changes its argmax to Ineffective under Level 1. In 8 of 10, P(Ineffective) rises.

| Case | Type | Text (start) | Gold | L0 pred / P(Ineff) | L1 pred / P(Ineff) | What the unit lacks (our reading) |
|:---:|---|---|:---:|:---:|:---:|---|
| 1 | Counterclaim | "There are many reason on why texting while driving is very u…" | Ineff | Adeq / 0.022 | Adeq / 0.029 | Counterclaim never answered (needs the whole essay to see) |
| 2 | Evidence | "To provide reasonings to my strong point, brings me back to…" | Ineff | Eff / 0.0004 | Eff / 0.0014 | Correct quotation followed by off-topic reasoning (see 5.2) |
| 3 | Position | "I think you shouldn't join the Seagoing Cowboys" | Ineff | Adeq / 0.022 | Adeq / 0.010 | Bare stance with no reason |
| 4 | Counterclaim | "Not allowing students to use there phones at all" | Ineff | Adeq / 0.038 | Adeq / 0.090 | Fragment; no opposing argument stated |
| 5 | Position | "The Driverless people can cause problems" | Ineff | Adeq / 0.028 | Adeq / 0.152 | Vague, possibly at odds with the source text |
| 6 | Counterclaim | "But Sometimes it could be a distraction from you doing all y…" | Ineff | Adeq / 0.031 | Adeq / 0.040 | Counterclaim with no rebuttal |
| 7 | Position | "I reconsider that are principal should let us eight graders…" | Ineff | Adeq / 0.035 | Adeq / 0.097 | Unclear thesis scope |
| 8 | Claim | "Some kids will ask there parents to transfer school" | Ineff | Adeq / 0.021 | Adeq / 0.124 | Unsupported prediction |
| 9 | Lead | "The future is near and the talk about driverless cars is upo…" | Ineff | Adeq / 0.045 | Adeq / 0.080 | Generic hook |
| 10 | Claim | "Another cars is a bad idea is because of its gas" | Ineff | Adeq / 0.039 | Adeq / 0.032 | Claim with no support |

### 5.2 Case 2 re-examined (Requirement 4)
The unit (prompt *Car-free cities*) begins: "…brings me back to paragraph 36. It clearly states in bolded writing: 'With all these changes, people who stopped car commuting as a result of the recession may find less reason to resume the habit…'". We checked the numbered source set used for this prompt: it has 43 paragraphs, and **paragraph 36 contains exactly this sentence**. The citation is therefore accurate, and our Week 10 reading ("a reference to a paragraph that does not exist") was wrong. The unit's weakness is visible in the unit itself: after the quotation, the student writes about getting a learner's permit and a driving test, which does not support the point. The model probably rated the unit Effective because of surface features (length, an explicit quotation, connectives such as "Furthermore"). That explanation is a hypothesis we have not tested. The PERSUADE CSV only lists source titles, not their text, so a model with source access would need the passages added from outside the corpus.

### 5.3 Lowering the Ineffective threshold: how many cases change?
Rule: predict Ineffective if P(Ineffective) ≥ θ; otherwise take the larger of Adequate and Effective. The baseline is argmax; there is no "default θ". Validation only (`outputs/ineffective_threshold_tuning_table.csv`, `outputs/threshold_case_flips.csv`).

**Week 10 Level 1 model (the model behind the 10 cases):**

| Rule | Recall Ineff | Precision Ineff | F1 Ineff | Macro-F1 | Units changed | Ineffective newly caught / new false alarms | Cases flipped (of 10) |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| argmax | 43.2% | 36.1% | 0.393 | 0.579 | — | — | 0 |
| θ = 0.30 | 53.6% | 28.7% | 0.374 | 0.566 | 895 | 138 / 757 | 0 |
| θ = 0.20 | 61.8% | 24.5% | 0.350 | 0.552 | 1,762 | 246 / 1,516 | 0 |
| θ = 0.15 | 67.4% | 21.9% | 0.330 | 0.539 | 2,503 | 321 / 2,182 | 1 (case 5) |
| θ = 0.10 | 73.0% | 18.4% | 0.295 | 0.517 | 3,670 | 396 / 3,274 | 2 (cases 5, 8) |
| θ = 0.08 | 75.7% | 16.8% | 0.274 | 0.503 | 4,410 | 431 / 3,979 | 5 (cases 4, 5, 7, 8, 9) |

**Reading.** Lowering θ moves the model toward Ineffective (case 8's probability is 6× higher with context), but each extra correct catch costs about 7–8 false alarms. Macro-F1 falls monotonically, and the best Macro-F1 is at argmax. For formative feedback, a teacher might accept θ ≈ 0.15–0.20 to review twice as many flagged units. This is a product decision, and on this data it does not improve the classifier. For the Week 11 L1 model that was scored on test, the curve is similar (θ = 0.10: recall 69.6%, Macro-F1 0.535, 3/10 cases flip), but case 8 itself does **not** flip, because its P(Ineffective) is 0.058. Single-case results depend on the training run.

---

## 6. Leave-one-prompt-out (LOPO)

### 6.1 What is compared
* **Across model families, same fold:** Linear SVM (TF-IDF), RF (Feature Set B) and DeBERTa L0, each trained on 14 prompts and tested on all units of the held-out prompt.
* **Within DeBERTa:** the LOPO model vs. the in-domain model (trained with the prompt present) on **the same units**, namely the validation essays of that prompt, with a paired essay bootstrap. The Week 10 table compared LOPO on all units of the prompt with in-domain on the validation subset, i.e. two different sets of units; this section replaces it.

### 6.2 All units of the held-out prompt

| Held-out prompt | Units | Linear SVM | RF | DeBERTa L0 (LOPO) | Ineff F1: SVM / RF / DeBERTa |
|---|:---:|:---:|:---:|:---:|:---:|
| A Cowboy Who Rode the Waves | 5,158 | 0.3373 | 0.3501 | **0.4082** | 0.103 / 0.109 / 0.125 |
| Summer projects | 9,855 | 0.4269 | 0.4339 | **0.4642** | 0.041 / 0.000 / 0.076 |
| Distance learning | 18,526 | 0.4690 | 0.5014 | **0.5735** | 0.062 / 0.065 / 0.251 |

We have no in-domain per-prompt numbers for SVM and RF, so this table shows which family transfers better. It does not show how much each family drops.

### 6.3 LOPO vs. in-domain DeBERTa on the same units (`outputs/lopo_deberta_gap_same_units.csv`)

| Held-out prompt | Units / essays | LOPO | In-domain (Week 9 L0) | Gap [95% CI] | In-domain (Week 11 L0) | Gap [95% CI] |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| A Cowboy Who Rode the Waves | 1,030 / 134 | 0.3584 | 0.4462 | **−0.088 [−0.138, −0.041]** | 0.4755 | **−0.117 [−0.171, −0.057]** |
| Summer projects | 2,074 / 177 | 0.4605 | 0.4695 | −0.009 [−0.093, +0.078] | 0.5076 | −0.047 [−0.113, +0.012] |
| Distance learning | 3,533 / 283 | 0.5712 | 0.5677 | +0.004 [−0.024, +0.028] | 0.5757 | −0.005 [−0.030, +0.020] |

**Reading.** Only *A Cowboy Who Rode the Waves* shows a clear drop when the prompt is unseen. It is a source-based narrative prompt whose essays refer to characters and events of one story, which fits the idea that prompt-specific content matters. With only three prompts this remains an interpretation, not a tested cause. Caveat: the Week 10 LOPO models were trained with transformers 5.20.2. That version later broke DeBERTa-v3 training in our Week 11 runs, so the LOPO numbers may understate DeBERTa somewhat.

---

## 7. Official test (Requirement 2)

### 7.1 Results (93,677 units, 10,402 essays, one pass)

| System | Role | Macro-F1 | Accuracy | F1 Ineff | F1 Adeq | F1 Eff | Recall Ineff | QWK | Inference time |
|---|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Random Forest, Feature Set B | protocol | 0.5098 | 78.51% | 0.2024 | **0.8701** | 0.4567 | 17.2% | 0.350 | 88 s train+predict (CPU) |
| DeBERTa-v3 Level 0 | protocol | 0.5613 | 74.38% | 0.3387 | 0.8312 | 0.5141 | 37.2% | 0.422 | 57 s (A100) |
| **DeBERTa-v3 Level 1** | **protocol, locked** | **0.5772** | 75.68% | 0.3679 | 0.8410 | 0.5228 | 41.5% | 0.442 | 91 s (A100) |
| DeBERTa-v3 Prompt-Aware | exploratory | 0.5808 | 75.39% | 0.3787 | 0.8381 | 0.5258 | 44.2% | 0.446 | 94 s (A100) |
| Linear SVM (TF-IDF) ¹ | supplementary | 0.4822 | 74.40% | 0.2044 | 0.8439 | 0.3983 | — | — | 41 s (CPU) |

¹ Trained on train + validation (144,289 units); the same configuration trained on 115,187 units scores 0.4845 on validation.
Footnote on RF: the first RF test run (Section 1.1(c), not Feature Set B) gave 0.4834 / 67.79%. It is kept in `outputs/official_test_rf_misspecified_old_result.csv` for transparency and is not used in any comparison.

### 7.2 Paired essay bootstrap on the test set

| Comparison | Δ Macro-F1 | 95% CI | One-sided p (Δ ≤ 0) | Resamples |
|---|:---:|:---:|:---:|:---:|
| L1 − L0 | +0.0159 | [+0.0115, +0.0207] | < 0.0005 | 2,000 |
| PA − L1 | +0.0036 | [−0.0002, +0.0074] | 0.032 | 2,000 |
| PA − L0 | +0.0195 | [+0.0151, +0.0241] | < 0.0005 | 2,000 |
| L0 − RF | +0.0516 | [+0.0448, +0.0584] | < 0.001 | 1,000 |
| L1 − RF | +0.0675 | [+0.0605, +0.0749] | < 0.001 | 1,000 |
| PA − RF | +0.0711 | [+0.0643, +0.0780] | < 0.001 | 1,000 |

We base decisions on the two-sided 95% CI. PA − L1 has a one-sided p below 0.05, but its two-sided interval includes 0, so we report the two as **not distinguishable**.

### 7.3 What the test says
1. Validation and test agree: L1 0.5809 vs. 0.5772, L0 0.5723 vs. 0.5613, RF 0.5261 vs. 0.5098. No system collapses on unseen essays.
2. DeBERTa beats RF Feature Set B by 0.05–0.07 Macro-F1, almost entirely through the minority classes (Ineffective F1 0.34–0.38 vs. 0.20). RF keeps the highest accuracy and Adequate F1 because it predicts Adequate more often.
3. Level 1 beats Level 0 on test for this pair of trained models. Given the run-to-run variation in §4.2, we read this as "local context gives a small, consistent gain". We do not read it as a size we can state precisely.
4. Adding the prompt name gives no difference we can distinguish on test.

---

## 8. Conclusion on context and information needs (rewritten, Requirement 1)

Adding the neighbouring units (Level 1) gives a small gain. In the Week 10 run it was not distinguishable from zero on validation (+0.0022). In the Week 11 retraining it was +0.0087 on validation and +0.0159 [0.0115, 0.0207] on the official test. None of the 10 high-confidence Ineffective failures changed its argmax with context, although 8 of 10 moved toward Ineffective. Reading those cases, the missing information seems to lie mostly in the whole essay (an unanswered counterclaim, a bare position) and sometimes in the task itself. Our results are **consistent with the hypothesis** that judging such units needs the whole essay and, for source-based prompts, the source texts. We have not tested this: Level 2 (source text) and Level 3 (whole essay) were not run, and case 2 shows that our own reading of a case can be wrong.

Label reliability also limits what any model can reach here. Two trained raters agree on these effectiveness labels only at κ ≈ 0.316 (Crossley et al., 2024), so part of what looks like model error is disagreement in the labels themselves. Our model's κ against the adjudicated label (0.37 on test) and the rater–rater κ measure different things and should not be compared to claim human-level performance.

---

## 9. Limitations
* One training seed per DeBERTa configuration; differences of about 0.005–0.01 Macro-F1 are within run-to-run variation (§4.2).
* The length effect in §3 is a measured association within holistic score; we have not identified its mechanism.
* Threshold analysis (§5.3) is on validation only; we did not choose or report an operating point on test.
* LOPO covers 3 of 15 prompts and was trained with a transformers version later found to break DeBERTa-v3 training.
* Source-dependent explanations (cases 2, 5) rely on source texts that are not part of the PERSUADE CSV.

## 10. Individual contributions and AI use

| Member | Role | Work | Artifacts |
|---|---|---|---|
| Member 1 | Data and confounds | Holistic × length analysis (rerun with the corrected join), RF Feature Set B on test | `Person1/script_holistic_length_table.py`, `Person1/run_rf_official_test.py`, `Person1/output/` |
| Member 2 | Errors and thresholds | Threshold analysis and case counting, Linear SVM test and LOPO | `script_threshold_tuning_and_case8.py`, `Person2Khoa/Person2Khoa/` |
| Member 3 | DeBERTa and test governance | Retrained L0/L1/PA on Colab A100, ran the locked test pass, bootstrap; same-unit LOPO gap | `Week11_Person3_DeBERTa_OfficialTest/`, `script_official_test_evaluation.py`, `script_lopo_same_units_gap.py` |

**AI assistance.** We used Gemini/Antigravity, Claude Code and OpenAI Codex for code drafting, running Colab jobs, report formatting, and a full re-check of this report against the raw data. That re-check found the defects listed in `RA_SOAT_TUAN11_SO_VOI_NHAN_XET_TUAN10.md`. Every number in this report is produced by a script in the repository from the raw CSVs or saved predictions.

## References
* Crossley, S. A., Baffour, P., Tian, Y., Franklin, A., Benner, M., & Boser, U. (2024). A large-scale corpus for assessing written argumentation: PERSUADE 2.0. *Assessing Writing*, 61, Article 100830. https://doi.org/10.1016/j.asw.2024.100830
* He, P., Gao, J., & Chen, W. (2023). DeBERTaV3: Improving DeBERTa using ELECTRA-style pre-training with gradient-disentangled embedding sharing. *ICLR*.
* Stab, C., & Gurevych, I. (2017). Parsing argumentation structures in persuasive essays. *Computational Linguistics*, 43(3), 619–659.
* Toulmin, S. E. (1958). *The Uses of Argument*. Cambridge University Press.
