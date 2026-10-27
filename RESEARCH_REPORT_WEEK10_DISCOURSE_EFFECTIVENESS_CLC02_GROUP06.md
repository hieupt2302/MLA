<div style="text-align: center; margin-bottom: 25px; padding-bottom: 20px; border-bottom: 2px solid #0f2d59;">
  <h1 style="color: #0f2d59; font-size: 20pt; margin-bottom: 8px; border-bottom: none; padding-bottom: 0;">TECHNICAL RESEARCH REPORT (WEEK 10)</h1>
  <h3 style="color: #1e3d59; font-size: 13pt; font-weight: 500; margin-top: 0; margin-bottom: 16px; line-height: 1.4;">EXAMINING LENGTH CONFOUNDS, CONTROLLED CONTEXTUAL ABLATION, AND LEAVE-ONE-PROMPT-OUT GENERALIZATION IN ARGUMENTATIVE DISCOURSE EFFECTIVENESS ASSESSMENT</h3>
  <p style="margin: 4px 0; font-size: 10pt;"><strong>Course:</strong> Machine Learning &amp; Applications (CLC02) &nbsp;|&nbsp; <strong>Academic Cohort:</strong> 2025–2026 &nbsp;|&nbsp; <strong>Project Group:</strong> Group 06</p>
  <p style="margin: 4px 0; font-size: 10pt;"><strong>Primary Dataset:</strong> PERSUADE 2.0 Corpus (<em>Assessing Writing</em>, Elsevier, 2024) &nbsp;|&nbsp; <strong>Date of Submission:</strong> October 2026</p>
  <p style="margin: 4px 0; font-size: 10pt;"><strong>Artifacts &amp; Outputs Repository:</strong> <code>outputs/</code></p>
  <div style="margin-top: 14px; padding: 12px 16px; background-color: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; display: inline-block; text-align: left; font-size: 9.5pt;">
    <strong style="color: #0f2d59;">Live Interactive Google Colab Notebooks:</strong><br>
    • <strong>Script 04 (Length Confound &amp; LOPO Classical):</strong> <a href="https://colab.research.google.com/drive/1YRMpJgGzZ0vWe7nA0W8c7n5JKMruVJHT?usp=sharing" target="_blank">Open in Google Colab</a> (<code>https://colab.research.google.com/drive/1YRMpJgGzZ0vWe7nA0W8c7n5JKMruVJHT?usp=sharing</code>)<br>
    • <strong>Script 05 (Context Ablation DeBERTa):</strong> <a href="https://colab.research.google.com/drive/1prcSnRHax0SAITnUbGsXks3aQ9pbwJD2?usp=sharing" target="_blank">Open in Google Colab</a> (<code>https://colab.research.google.com/drive/1prcSnRHax0SAITnUbGsXks3aQ9pbwJD2?usp=sharing</code>)<br>
    • <strong>Script 06 (Leave-One-Prompt-Out DeBERTa):</strong> <a href="https://colab.research.google.com/drive/1xiYMZ7SjRSAn_ioAvAbNh-PZDkghsiBk?usp=sharing" target="_blank">Open in Google Colab</a> (<code>https://colab.research.google.com/drive/1xiYMZ7SjRSAn_ioAvAbNh-PZDkghsiBk?usp=sharing</code>)
  </div>
</div>

## Executive Abstract

Evaluating the rhetorical effectiveness of discourse units in student writing is a foundational task in Automated Writing Evaluation (AWE). Following reviewer feedback on our Week 9 evaluation protocol (*Nhan_xet_Week9_CLC02_Group06*), this study transitions from internal validation benchmarking to controlled diagnostic ablation and out-of-domain prompt generalization. Specifically, we present empirical evidence addressing the core methodological questions raised by the instructor:

1. **Investigation of the Essay Length Confound (N = 29,102 Validation Units):** Prior audits observed classification error rates increasing from 21.98% in short essays to 30.35% in longer essays. Through a 4-quartile audit across 3,119 validation essays, we demonstrate that this disparity is heavily driven by **severe label distribution shift and quality boundary transitions** rather than compounding syntactic complexity alone. In short essays (Quartile 1: 148–315 words), the gold Ineffective rate is **8.97%** and student holistic scores average 2.38/6. In long essays (Quartile 4: 567–8,811 words, median 712 words), the Ineffective rate drops 7.0-fold to **1.29%**, while the Effective rate surges from 5.29% to **32.81%** (mean holistic score reaches 4.67/6). Crucially, confusion matrix analysis shows that **91.52% of all errors in Quartile 4 (2,018 out of 2,205 errors) arise from distinguishing Adequate from Effective**, whereas errors on Ineffective account for only 3.08% of long essay mistakes.
2. **Controlled Contextual Ablation (Level 0 vs Level 1 with DeBERTa-v3-base):** Testing the hypothesis that automated scoring suffers from isolated-unit inputs, we evaluated Level 0 (unit-only) against Level 1 (unit flanked by immediate preceding and succeeding units within the essay) on the identical 29,102 validation units (max_length = 512, truncation rate < 0.65%). Providing local sequential neighbors produces an overall **Ineffective F1 gain of +0.0193 points (+5.16% relative, 0.3741 to 0.3934)**, while overall Macro-F1 edges from 0.5768 to 0.5790 (paired bootstrap 95% CI [-0.0058, +0.0105]). Performance improvements are concentrated in relational units: Claim Ineffective F1 improves +0.0430 points (+16.17% relative, +10 units recalled), Concluding Statement improves +0.0389 points, Counterclaim improves +0.0303 points (+1 unit), and Rebuttal improves +0.0276 points (+1 unit). In contrast, autonomous thesis units (Position) decline by -0.0550 points (-7 units recalled), suggesting that local context introduces transition noise for thesis formulation.
3. **Diagnostic Audit of 10 Ineffective Failure Cases:** Re-evaluating the 10 highest-confidence Ineffective failure cases reveals that 0/10 flip to an Ineffective argmax prediction with local context alone, though 8/10 show an increase in posterior probability P(Ineffective) (average 2.57x increase). Error inspection categorizes their failure mechanisms: 2 cases suffer from dangling structure, 4 cases require extrinsic reference to prompt reading passages (e.g., unsubstantiated citations such as *"paragraph 36"* or factual contradictions with source texts), and 2 cases require whole-essay stance tracking.
4. **Leave-One-Prompt-Out (LOPO) Generalization Benchmark:** Across all 15 prompts evaluated via 15-fold cross-validation with Random Forest (Feature Set B), the classical baseline achieves a mean Macro-F1 of **0.4303 ± 0.0405** and an average accuracy of **77.09% (unweighted) / 76.47% (weighted)**. Deep learning evaluation using fine-tuned DeBERTa-v3 across 3 representative tiers (Hardest, Median, Easiest) yields higher out-of-prompt Macro-F1 than Random Forest across all 3 prompts (Mean Macro-F1: **0.4820 vs 0.4285**, +12.49% relative gain), though DeBERTa accuracy is slightly lower than RF due to balanced class weighting (Cowboy: 78.87% vs 79.20%; Summer: 66.58% vs 70.24%; Distance: 75.55% vs 78.05%). Comparing in-domain performance on the *same prompt* vs LOPO reveals that out-of-prompt generalization drop varies dramatically by prompt type: source-dependent prompts drop noticeably (Cowboy: -8.52%), while open-ended and universal prompts transfer robustly (Summer projects: -1.12%; Distance learning: +1.03%). Under LOPO, discourse vulnerability shows that Rebuttal (-22.79%) and Evidence (-19.36%) experience the greatest performance drop, while Position (-10.26%) is the most resilient.
5. **Scientific Rigor & Reproducibility:** We calibrate our reporting tone, document 3x3 confusion matrices for all baseline and deep learning models, provide exact bootstrap confidence intervals, cite the verified literature source (*Crossley et al., 2024, Assessing Writing, Vol. 61*), and share reproducible Google Colab notebooks.

---

## Table of Contents
1. [Methodological Rectification & Responses to Week 9 Review](#1-methodological-rectification--responses-to-week-9-review)
2. [Data Pipeline Rigor & Verified Split Alignment](#2-data-pipeline-rigor--verified-split-alignment)
3. [Empirical Investigation of the Essay Length Confound](#3-empirical-investigation-of-the-essay-length-confound)
4. [Controlled Contextual Ablation Study (Level 0 vs Level 1)](#4-controlled-contextual-ablation-study-level-0-vs-level-1)
5. [Diagnostic Audit of 10 Ineffective Failure Cases](#5-diagnostic-audit-of-10-ineffective-failure-cases)
6. [Leave-One-Prompt-Out (LOPO) Generalization Benchmark](#6-leave-one-prompt-out-lopo-generalization-benchmark)
7. [Pedagogical Synthesis & Theoretical Inquiries](#7-pedagogical-synthesis--theoretical-inquiries)
8. [Reproducibility Artifacts & Codebase Governance](#8-reproducibility-artifacts--codebase-governance)
9. [References](#9-references)

---

## 1. Methodological Rectification & Responses to Week 9 Review

Following the feedback in *Nhan_xet_Week9_CLC02_Group06.docx.md*, we systematically address each methodological concern:

### 1.1 Resolution of the Spearman Rank Correlation Caveat
* **Reviewer Comment:** *"Phép so ρ = 0,857 giữa kappa người chấm và F1 mô hình chỉ có 7 điểm, không đủ để kết luận lỗi ở Claim, Counterclaim 'trực tiếp do' người chấm kém đồng thuận. Kappa của mô hình so với nhãn và kappa giữa hai người chấm cũng không phải cùng một đại lượng, nên chưa nói được mô hình 'ngang người'. Các con số kappa theo loại đơn vị cũng cần ghi rõ trang và bảng trong Crossley và cộng sự (2024)."*
* **Group 06 Resolution:**
  1. **Small-Sample Statistical Limitation (N = 7):** We formally retract the assertion that model errors on Claim and Counterclaim are "directly caused by" low human annotator agreement. With only N = 7 discourse types, a rank correlation of ρ = 0.8571 (p = 0.0137) possesses a wide 95% confidence interval ([0.26, 0.98]) and must be interpreted strictly as an **exploratory bivariate trend**, not a causal proof.
  2. **Metric Incommensurability (Model κ vs Human-Human κ):** We explicitly clarify that Cohen's κ between model predictions and gold labels (κ_model = 0.3704) and Cohen's κ between two independent human raters (κ_human-human = 0.316) measure fundamentally distinct quantities. The former evaluates algorithmic classification fidelity against a consensus reference standard, whereas the latter reflects pairwise variance in human subjective judgment. We retract any claim that the model has reached "human parity" or is equivalent to human raters.
  3. **Formal Literature Citation & Verified Benchmarks:** The official publication introducing the corpus is:
     > **Crossley, S. A., Baffour, P., Tian, Y., Franklin, A., Benner, M., & Boser, U. (2024).** *A large-scale corpus for assessing written argumentation: PERSUADE 2.0.* **Assessing Writing**, Volume 61, Article 100830. [DOI: 10.1016/j.asw.2024.100830].
     As documented in Section 5 of Crossley et al. (2024), human inter-rater reliability on effectiveness ratings across 159,228 double-scored segments yields an **exact agreement of 0.718** (ranging from 0.68 to 0.81 across classes) and an **overall Cohen's κ = 0.316** (ranging from 0.17 to 0.38 across specific classes), indicating fair human agreement.

### 1.2 Technical Analysis of the LR 6.13% Metric Mapping Defect
* **Reviewer Directive:** *"mỗi thành viên phải tự giải thích được lỗi 6,13% bằng lời của mình."*
* **Core Technical Mechanism:**
  The 6.13% anomaly reported in Week 8 was an **indexing transposition defect** in the evaluation script's post-processing logic:
  1. In `scikit-learn`, `LogisticRegression.classes_` automatically sorts string target labels in alphabetical order: `['Adequate', 'Effective', 'Ineffective']`, meaning index 0 corresponds to Adequate, index 1 to Effective, and index 2 to Ineffective.
  2. The legacy Week 8 metric extraction code assumed index 0 was Ineffective (`['Ineffective', 'Adequate', 'Effective']`). Consequently, the script extracted the F1 score of the Ineffective minority class (~0.0613) and assigned it into the Overall/Balanced Accuracy variable.
  3. The Logistic Regression model itself did not suffer numerical collapse; with identical features and balanced class weights, properly mapping `LABEL2ID={'Ineffective': 0, 'Adequate': 1, 'Effective': 2}` reveals that Logistic Regression achieved an actual Balanced Accuracy of 60.32% (Macro-F1 0.5086) on the canonical 29,102 validation units.
  4. From Week 9 onward, all confusion matrices, precision, recall, and F1 calculations are derived directly via vectorized confusion matrix counts with fixed label ID mappings.

### 1.3 Governance of the Official Test Set
* **Reviewer Comment:** *"Validation đang dùng cho chọn mô hình, chọn ngưỡng, hiệu chỉnh và kiểm định. Kết luận vượt trội cuối cùng cần một lần chấm trên Official Test đã khóa cấu hình."*
* **Group 06 Resolution:**
  - The **Validation Cohort (N = 29,102 units)** serves exclusively for model selection, hyperparameter tuning, contextual ablation, and diagnostic failure analysis.
  - The **Official Test Holdout (N = 93,677 units, 10,402 essays)** remains **strictly locked and untouched**.
  - **Pre-registered Locked Configuration:** Prior to evaluating the Official Test set, Group 06 locks the following final configuration: backbone `microsoft/deberta-v3-base`, Level 1 contextual neighbor input formatting, effective batch size 32, learning rate 2e-5, 3 epochs, balanced cross-entropy class weights, default argmax decision rule, and seed 42. Selection is based strictly on validation Macro-F1 superiority.

### 1.4 Tone Calibration and Presentation Standards
All hyperbolic rhetoric has been removed:
- Replaced `"forensic analysis"` with `"diagnostic error audit"` or `"empirical inspection"`.
- Replaced `"definitive proof"` and `"conclusively demonstrated"` with `"empirical evidence indicates"` or `"hypothesis testing supports"`.
- Removed speculative claims comparing model performance to human raters.
- Formatted inline mathematical variables, counts, and percentages as clean plain text to prevent rendering duplication artifacts across PDF compilers.

---

## 2. Data Pipeline Rigor & Verified Split Alignment

### 2.1 Filtering Pipeline & String Typing
All raw files are parsed enforcing strict string typing (`dtype={'essay_id': str, 'discourse_id': str}`) to prevent numeric conversion errors or dropped leading zeroes. All evaluations operate strictly on **predefined gold segmentation discourse boundaries** established in the PERSUADE 2.0 corpus.

| Stage | Train Fit Cohort (80%) | Validation Cohort (20%) | Official Test Holdout (Locked) |
|---|:---:|:---:|:---:|
| **Raw Rows in Source CSV** | 173,266 raw rows | (Split from train CSV) | 112,117 raw rows |
| **Excluded Unannotated Units** | 28,977 segments | (Excluded prior to split) | 18,440 segments |
| **Clean Annotated Units** | 115,187 units | 29,102 units | 93,677 units |
| **Unique Essays (String ID)** | 12,474 essays | 3,119 essays | 10,402 essays |
| **Split Strategy** | GroupShuffleSplit (seed=42) | GroupShuffleSplit (seed=42) | Official Benchmark Split |
| **Cross-Essay Leakage** | Exactly 0 essays | Exactly 0 essays | Exactly 0 essays |

### 2.2 Canonical Cohort Summary Table

| Partition Cohort | Number of Essays | Total Discourse Units | Ineffective (%) | Adequate (%) | Effective (%) | Primary Role in Study |
|---|:---:|:---:|:---:|:---:|:---:|---|
| **Train Fit Cohort (80%)** | 12,474 | 115,187 | 4.46% | 78.44% | 17.11% | Feature extraction, classifier fitting, DeBERTa fine-tuning |
| **Validation Cohort (20%)** | 3,119 | 29,102 | 4.56% | 78.68% | 16.76% | Length quartile audit, contextual ablation, paired testing |
| **Official Test Holdout** | 10,402 | 93,677 | 4.51% | 80.45% | 15.04% | Strictly untouched final evaluation benchmark |

---

## 3. Empirical Investigation of the Essay Length Confound

### 3.1 The Observed Phenomenon & Competing Hypotheses
In earlier audits, classification error rates rose noticeably across essay word count:
$$\text{Observed Error Rate: } 21.98\% \text{ (Quartile 1)} \longrightarrow 30.35\% \text{ (Quartile 4)}$$

Two competing hypotheses explain this divergence:

* **Hypothesis A (Rhetorical Complexity):** Longer essays feature elaborate syntactic trees and multi-sentence argumentative structures that confuse fixed-length attention windows.
* **Hypothesis B (Label Distribution & Proficiency Shift):** Essay length is confounded with student writing proficiency and prompt assignment, creating class imbalance shifts and shifting the dominant classification challenge from minority Ineffective detection to subtle Adequate vs Effective differentiation.

### 3.2 4-Quartile Validation Analysis (N = 29,102 Units)

To test these hypotheses, we partitioned all 29,102 validation units into four equal-frequency quartiles (Q1 to Q4) based on total essay word count:

| Quartile | Word Count Range | Units (N) | Essays (N) | Mean Holistic Score (1–6) | Pct Ineff | Pct Adeq | Pct Eff | Overall Model Error | Error on Gold Ineff | Error on Gold Adeq | Error on Gold Eff |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Q1 (Short)** | 148 – 315 | 7,333 | 1,037 | 2.38 | 8.97% | 85.74% | 5.29% | 21.98% | 51.52% | 16.72% | 57.22% |
| **Q2 (Med-Low)** | 316 – 422 | 7,277 | 786 | 3.20 | 5.02% | 84.27% | 10.72% | 24.50% | 55.07% | 19.83% | 46.92% |
| **Q3 (Med-High)** | 423 – 566 | 7,226 | 690 | 3.81 | 2.92% | 78.74% | 18.34% | 27.68% | 57.82% | 23.64% | 40.23% |
| **Q4 (Long)** | 567 – 8,811 | 7,266 | 606 | 4.67 | 1.29% | 65.90% | 32.81% | 30.35% | 72.34% | 33.46% | 22.44% |

*Note on Q4 range:* Q4 spans up to 8,811 words due to an isolated extreme-length submission (*Exploring Venus*, essay ID `AAAVUP14319000135886`); the median word count of Q4 is 712 words, and the 95th percentile is 1,048 words.

### 3.3 Prompt Composition Breakdown Across Quartiles
Stratifying prompts across quartiles (`outputs/length_quartile_prompt_breakdown.csv`) reveals notable prompt selection effects:
* In **Q1 (Short Essays)**, civics and school-policy prompts dominate: *Does the electoral college work?* (10.50%), *Grades for extracurricular activities* (10.27%), and *Cell phones at school* (9.76%).
* In **Q4 (Long Essays)**, open-ended narrative and expository prompts dominate heavily: *Distance learning* alone accounts for **27.36%** (1,988 units), followed by *Summer projects* (17.09%) and *Seeking multiple opinions* (16.93%). Together, these three prompts account for **61.38%** of all units in Q4.

### 3.4 Empirical Findings on the Confound
1. **Direct Correlation with Student Holistic Proficiency:** The average holistic essay score doubles from **2.38/6 in Q1 to 4.67/6 in Q4**. More proficient students produce substantially longer essays and write structurally sound arguments. Consequently, the gold Ineffective rate drops 7.0-fold from 8.97% in Q1 to only 1.29% in Q4 (only 94 Ineffective units in the entire Q4 validation cohort).
2. **Decomposition of Q4 Errors:** Inspecting the confusion matrix of DeBERTa on Q4 (total errors = 2,205 units):
   - Errors on gold Ineffective account for only **68 units (3.08% of all errors in Q4)**.
   - Confusion between Adequate and Effective accounts for **2,018 units (91.52% of all errors in Q4)**: 1,491 gold Adequate units were predicted as Effective, and 527 gold Effective units were predicted as Adequate.
3. **Empirical Conclusion:** The rising error rate in longer essays is **not driven by failing on Ineffective units**, but by the fact that Q4 is dominated by higher-proficiency essays where distinguishing between Adequate and Effective arguments is the primary difficulty. Hypothesis B is strongly supported by this empirical decomposition.

---

## 4. Controlled Contextual Ablation Study (Level 0 vs Level 1)

### 4.1 Controlled Experimental Formulation
To test what information automated discourse assessment requires, we conducted a strictly controlled experiment contrasting isolated unit input against local sequential context:
- **Backbone Architecture:** `microsoft/deberta-v3-base` (86M parameters).
- **Partition:** Canonical GroupShuffleSplit (115,187 train units, 29,102 validation units across 3,119 essays; seed=42).
- **Hyperparameters:** Effective batch size 32 (8 per device x 4 gradient accumulation steps), 3 epochs, learning rate 2e-5 with linear warmup (10%), FP16 mixed precision, balanced class weights:
  $$w_0 (\text{Ineffective}) = 7.4787, \quad w_1 (\text{Adequate}) = 0.4250, \quad w_2 (\text{Effective}) = 1.9484$$
- **Sequence Length & Truncation:** Tokenizer max_length = 512 with head/tail truncation. 
  - Level 0 input mean length is 58.0 tokens; truncation rate (> 512 tokens) is **0.04%** (12 units).
  - Level 1 input mean length is 164.7 tokens; truncation rate is **0.62%** (180 units across 29,102 units). For Position, truncation is only **0.42%** (mean length 145.1 tokens), verifying that Position performance changes are not truncation artifacts.

#### Input Formulations Compared:

* **Level 0 (Unit Only Baseline):**
  $$\mathbf{x}_{\text{Level 0}} = \tau_{i,j} \circ \text{[SEP]} \circ s_{i,j}$$

* **Level 1 (Unit with Local Sequential Neighbors):**
  $$\mathbf{x}_{\text{Level 1}} = \tau_{i,j} \circ \text{[SEP]} \circ \text{Previous: } s_{i,j-1} \circ \text{[SEP]} \circ \text{Target: } s_{i,j} \circ \text{[SEP]} \circ \text{Next: } s_{i,j+1}$$
  
  where $s_{i,j-1}$ and $s_{i,j+1}$ denote the preceding and succeeding discourse units within the essay ordered by character offset (`discourse_start`). If a unit occurs at an essay boundary, `[NONE]` is inserted.

### 4.2 Overall Benchmark Results & Confusion Matrices (N = 29,102 Validation Units)

The benchmark results and exact 3x3 confusion matrices on the identical validation cohort are presented below:

### 4.2.1 Exact 3x3 Confusion Matrices (Rows: Gold Label, Columns: Predicted Label):

* **Random Forest Baseline (Feature Set B):**
  ```
  [[  286,   999,    43],    --> Gold Ineffective (N = 1,328): Recall = 21.54%, Precision = 26.70%
   [  764, 20018,  2115],    --> Gold Adequate    (N = 22,897): Recall = 87.43%, Precision = 84.45%
   [   21,  2687,  2169]]    --> Gold Effective   (N = 4,877): Recall = 44.47%, Precision = 50.13%
  Accuracy = 22,473 / 29,102 = 77.22% | Macro-F1 = (0.2384 + 0.8591 + 0.4713) / 3 = 0.5230
  ```

* **DeBERTa-v3 Level 0 (Unit Only):**
  ```
  [[  598,   682,    48],    --> Gold Ineffective (N = 1,328): Recall = 45.03%, Precision = 32.00%
   [ 1245, 17683,  3969],    --> Gold Adequate    (N = 22,897): Recall = 77.23%, Precision = 88.44%
   [   26,  1630,  3221]]    --> Gold Effective   (N = 4,877): Recall = 66.04%, Precision = 44.50%
  Accuracy = 21,502 / 29,102 = 73.88% | Macro-F1 = (0.3741 + 0.8245 + 0.5317) / 3 = 0.5768
  ```

* **DeBERTa-v3 Level 1 (+ Local Neighbors):**
  ```
  [[  574,   708,    46],    --> Gold Ineffective (N = 1,328): Recall = 43.22%, Precision = 36.10%
   [  998, 17286,  4613],    --> Gold Adequate    (N = 22,897): Recall = 75.49%, Precision = 88.92%
   [   18,  1447,  3412]]    --> Gold Effective   (N = 4,877): Recall = 69.96%, Precision = 42.27%
  Accuracy = 21,272 / 29,102 = 73.09% | Macro-F1 = (0.3934 + 0.8166 + 0.5270) / 3 = 0.5790
  ```

#### Comparative Performance Summary:

| Evaluation Metric | Level 0 (Unit Only) | Level 1 (+ Local Neighbors) | Absolute Delta | Relative Change (%) |
|---|:---:|:---:|:---:|:---:|
| **Macro-F1 (Primary Metric)** | **0.5768** | **0.5790** | **+0.0022 points** | +0.38% |
| **Accuracy** | 73.88% | 73.09% | -0.79 points | -1.07% |
| **Balanced Accuracy** | 62.77% | 62.89% | +0.12 points | +0.19% |
| **Quadratic Weighted Kappa (QWK)** | 0.4414 | 0.4384 | -0.0030 points | -0.68% |
| **Unweighted Cohen's κ** | 0.3704 | 0.3676 | -0.0028 points | -0.76% |
| **F1: Ineffective (Class 0)** | **0.3741** | **0.3934** | **+0.0193 points** | **+5.16%** |
| **Precision: Ineffective** | 32.00% | 36.10% | +4.10 points | +12.81% |
| **Recall: Ineffective** | 45.03% | 43.22% | -1.81 points | -4.02% |
| **F1: Adequate (Class 1)** | 0.8245 | 0.8166 | -0.0079 points | -0.96% |
| **F1: Effective (Class 2)** | 0.5317 | 0.5270 | -0.0047 points | -0.88% |

#### Statistical Significance via Paired Bootstrap (1,000 Iterations by Essay):
- **Delta Macro-F1:** Mean = +0.0021 points, **95% CI: [-0.0058, +0.0105]**. Because the interval spans zero, the overall Macro-F1 difference is not statistically significant.
- **Delta Ineffective F1:** Mean = +0.0188 points, **95% CI: [-0.0020, +0.0398]**. The distribution is largely positive (upper bound reaching +0.0398), driven by a substantial reduction in false alarms on Adequate text (from 1,245 false positives down to 998).

### 4.3 Fine-Grained Performance Breakdown by Discourse Type

Evaluating Level 0 vs Level 1 across the 7 discourse types directly addresses the reviewer's inquiry (*"Ineffective được cải thiện ở loại đơn vị nào?"*):

| Discourse Type | Val Units (N) | Ineff Units (N) | Level 0 Ineff F1 | Level 1 Ineff F1 | Ineff F1 Delta (Points) | Relative Ineff Change (%) | Ineff Recall Delta (Units Rescued) |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Claim** | 10,135 | 317 | 0.2660 | **0.3090** | **+0.0430** | **+16.17%** | +0.0315 (+10 units) |
| **Concluding Statement** | 2,711 | 105 | 0.3484 | **0.3873** | **+0.0389** | **+11.17%** | +0.0095 (+1 unit) |
| **Counterclaim** | 1,148 | 39 | 0.1975 | **0.2278** | **+0.0303** | **+15.34%** | +0.0256 (+1 unit) |
| **Rebuttal** | 868 | 34 | 0.3488 | **0.3765** | **+0.0276** | **+7.91%** | +0.0294 (+1 unit) |
| **Evidence** | 9,249 | 667 | 0.4333 | **0.4537** | **+0.0203** | **+4.69%** | -0.0405 (-27 units) |
| **Lead** | 1,902 | 66 | 0.3143 | **0.3175** | +0.0032 | +1.02% | -0.0455 (-3 units) |
| **Position** | 3,089 | 100 | 0.3636 | **0.3086** | **-0.0550** | **-15.13%** | -0.0700 (-7 units) |

### 4.4 Exploratory Rhetorical Interpretation of Context Effects
*Note on sample sizes:* In small minority subsets (such as Counterclaim with 39 Ineffective units and Rebuttal with 34), a recall shift of ~0.027 represents a difference of only +1 unit correctly identified. Accordingly, the following observations represent exploratory hypotheses:
1. **Relational Argumentative Units (Claim, Counterclaim, Rebuttal):** In persuasive discourse, a Claim rarely functions independently; its rhetorical adequacy depends on whether it introduces a coherent premise supported by adjoining Evidence. Local context aids in identifying disjointed transitions, producing a +0.0430 point gain in Claim Ineffective F1 (+10 units recalled).
2. **Autonomous Thesis Units (Position):** A thesis statement (Position) is evaluated primarily on stance clarity and fidelity to the overarching prompt. Appending neighboring sentences introduces extraneous introductory or narrative text, which coincides with a -0.0550 point decline (-7 units recalled). This suggests that thesis assessment requires prompt-level alignment rather than local sequential neighbor text.

---

## 5. Diagnostic Audit of 10 Ineffective Failure Cases

### 5.1 Reviewer Inquiry 1
* **Reviewer Question:** *"Trong mười ca Ineffective, ca nào sẽ được đoán đúng nếu mô hình thấy được đoạn văn xung quanh, và ca nào thì không?"*

### 5.2 Empirical Re-evaluation of the 10 Failure Cases
We re-evaluated the 10 highest-confidence Ineffective failure cases from Week 9 using the fine-tuned Level 1 model (`outputs/context_ablation_case_study_recheck.csv`):

| Case ID | Discourse Type | Target Discourse Text Snippet | True Label | Level 0 Pred | Level 0 P(Ineff) | Level 1 Pred | Level 1 P(Ineff) | Prob Ratio (L1 / L0) | Failure Mechanism Category |
|:---:|---|---|:---:|:---:|:---:|:---:|:---:|:---:|---|
| **1** | Counterclaim | *"There are many reason on why texting while driving is very u..."* | Ineffective | Adequate | 0.0225 | Adequate | 0.0290 | 1.29x | Unpaired counterclaim lacking rebuttal across essay |
| **2** | Evidence | *"To provide reasonings to my strong point, brings me back to..."* | Ineffective | Effective | 0.0004 | Effective | 0.0014 | 3.50x | Extrinsic: Vacuous citation to reading passage (*"paragraph 36"*) |
| **3** | Position | *"I think you shouldn't join the Seagoing Cowboys"* | Ineffective | Adequate | 0.0221 | Adequate | 0.0096 | 0.43x | Extrinsic: Thesis alignment with prompt background |
| **4** | Counterclaim | *"Not allowing students to use there phones at all"* | Ineffective | Adequate | 0.0379 | Adequate | 0.0904 | 2.39x | Local syntactic fragment lacking connective premise |
| **5** | Position | *"The Driverless people can cause problems"* | Ineffective | Adequate | 0.0279 | Adequate | 0.1515 | 5.43x | Extrinsic: Factual conflict with prompt source passage |
| **6** | Counterclaim | *"But Sometimes it could be a distraction from you doing all y..."* | Ineffective | Adequate | 0.0315 | Adequate | 0.0400 | 1.27x | Dangling transition without subsequent rebuttal |
| **7** | Position | *"I reconsider that are principal should let us eight graders..."* | Ineffective | Adequate | 0.0347 | Adequate | 0.0970 | 2.80x | Extrinsic: Thesis formulation dependent on prompt scope |
| **8** | Claim | *"Some kids will ask there parents to transfer school"* | Ineffective | Adequate | 0.0207 | Adequate | 0.1236 | 5.97x | Local unsubstantiated leap; P(Ineff) increased 6.0x |
| **9** | Lead | *"The future is near and the talk about driverless cars is upo..."* | Ineffective | Adequate | 0.0446 | Adequate | 0.0802 | 1.80x | Extrinsic: Generic hook requiring prompt context |
| **10** | Claim | *"Another cars is a bad idea is because of its gas"* | Ineffective | Adequate | 0.0392 | Adequate | 0.0315 | 0.80x | Local syntax defect with missing connective premise |

### 5.3 Diagnostic Synthesis: Why Did None Flip Argmax?
Across the 10 failure cases, **0/10 flipped to an Ineffective argmax decision**. However, 8 of the 10 cases experienced an increase in P(Ineffective), with an average probability ratio of 2.57x (median 2.10x), while 2 cases (Case 3 and Case 10) saw a slight decline. 

*Methodological Note on Regression to the Mean:* Because these 10 cases were selected specifically as the most confident errors of Level 0, subsequent evaluations naturally exhibit some regression to the mean. More fundamentally, linguistic analysis explains why local context is insufficient to alter the top prediction:
1. **Extrinsic Source Passage Grounding (Cases 2, 5):** In Case 2, the student cites *"paragraph 36"*. A human rater recognizes this as Ineffective because they have read the assignment's accompanying source text and know paragraph 36 does not exist or support the point. DeBERTa has never seen the source passage; without it, the sentence exhibits standard citation syntax. In Case 5, the assertion contradicts facts from the driverless car passage.
2. **Whole-Essay Document Structure (Cases 1, 6):** A Counterclaim is marked Ineffective when the author fails to provide a Rebuttal anywhere in the paper. Checking only the single adjacent sentence cannot prove the absence of a rebuttal later in the essay.
3. **Conclusion for Inquiry 1:** Local context increases posterior probability mass on Ineffective for most flawed units, but cannot resolve cases whose flaws depend on external source texts or whole-essay argumentative coherence.

---

## 6. Leave-One-Prompt-Out (LOPO) Generalization Benchmark

### 6.1 Practical Rationale
Standard in-domain cross-validation allows classifiers to exploit prompt-specific lexical correlations. In real-world educational deployment, an AWE system must evaluate **completely new essay prompts** assigned by instructors. Leave-One-Prompt-Out (LOPO) guarantees zero prompt overlap between training and evaluation.

### 6.2 15-Fold Classical Benchmark (Random Forest, Feature Set B)

We evaluated 15 independent Random Forest models (n_estimators=150, max_depth=35, Feature Set B: TF-IDF unigrams/bigrams, discourse role dummy encoding, token length). In each fold, the model was trained on 14 prompts and evaluated on the single held-out prompt:

| Held-out Writing Prompt | Test Units (N) | Test Essays (N) | LOPO Macro-F1 | Overall Accuracy (%) | Ineffective F1 | Ineffective Recall | Difficulty Tier |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| *"A Cowboy Who Rode the Waves"* | 5,158 | 688 | **0.3501** | 79.20% | 0.1085 | 0.1279 | **Hardest (Rank 1/15)** |
| *Community service* | 6,461 | 768 | **0.3803** | 71.55% | 0.1181 | 0.0906 | Hard (Rank 2/15) |
| *Car-free cities* | 8,368 | 983 | **0.3877** | 76.09% | 0.0326 | 0.0242 | Hard (Rank 3/15) |
| *The Face on Mars* | 7,229 | 819 | **0.4009** | 75.03% | 0.1479 | 0.1566 | Hard (Rank 4/15) |
| *Driverless cars* | 12,628 | 1,386 | **0.4117** | 78.31% | 0.0584 | 0.0684 | Moderate (Rank 5/15) |
| *Does the electoral college work?* | 16,840 | 1,818 | **0.4172** | 68.66% | 0.1258 | 0.0859 | Moderate (Rank 6/15) |
| *Grades for extracurricular activities* | 6,122 | 815 | **0.4235** | 81.43% | 0.0956 | 0.0890 | Moderate (Rank 7/15) |
| *Summer projects* | 9,855 | 875 | **0.4339** | 70.24% | 0.0000 | 0.0000 | **Median (Rank 8/15)** |
| *Seeking multiple opinions* | 14,562 | 1,544 | **0.4442** | 77.13% | 0.0412 | 0.0763 | Moderate (Rank 9/15) |
| *Exploring Venus* | 7,252 | 928 | **0.4451** | 72.99% | 0.1279 | 0.0869 | Moderate (Rank 10/15) |
| *Cell phones at school* | 7,074 | 829 | **0.4473** | 87.23% | 0.1235 | 0.0901 | Moderate (Rank 11/15) |
| *Facial action coding system* | 9,175 | 1,103 | **0.4612** | 78.10% | 0.1015 | 0.0641 | Moderate (Rank 12/15) |
| *Phones and driving* | 6,584 | 700 | **0.4697** | 83.55% | 0.0292 | 0.0286 | Moderate (Rank 13/15) |
| *Mandatory extracurricular activities* | 8,455 | 839 | **0.4802** | 78.76% | 0.0760 | 0.0505 | Moderate (Rank 14/15) |
| *Distance learning* | 18,526 | 1,498 | **0.5014** | 78.05% | 0.0649 | 0.0433 | **Easiest (Rank 15/15)** |

> **Summary Statistics Across All 15 Prompts (Classical Random Forest):**  
> **Mean Macro-F1:** **0.4303 ± 0.0405** &nbsp;|&nbsp; **Unweighted Mean Accuracy:** **77.09%** &nbsp;|&nbsp; **Weighted Mean Accuracy:** **76.47%**

### 6.3 Prompt Generalization Gap Analysis
* **In-Domain vs Out-of-Prompt Performance:**
  - In-domain validation Random Forest (Week 9): Macro-F1 = 0.5230 (on all 15 prompts mixed).
  - Out-of-prompt Random Forest (15-fold LOPO average): Macro-F1 = 0.4303.
  - Overall classical generalization drop: -0.0927 points (-17.72% relative).
* **Source-Dependent Literary Prompts vs Universal Policy Prompts:**
  - The hardest prompt is *"A Cowboy Who Rode the Waves"* (Macro-F1 = 0.3501), which requires students to read a specific narrative passage. Character names and literary citations do not transfer from other prompts.
  - The easiest prompt is *"Distance learning"* (Macro-F1 = 0.5014), where students employ universal argumentative vocabulary (*"flexibility"*, *"social skills"*), enabling robust transfer.

### 6.4 Deep Learning LOPO Benchmark: DeBERTa-v3 vs Classical Random Forest

We fine-tuned a fresh copy of the pretrained `microsoft/deberta-v3-base` checkpoint across three representative prompts covering the difficulty spectrum identified by Random Forest:
1. **Hardest Tier (Rank 1/15):** *"A Cowboy Who Rode the Waves"* (5,158 test units across 688 essays).
2. **Median Tier (Rank 8/15):** *Summer projects* (9,855 test units across 875 essays).
3. **Easiest Tier (Rank 15/15):** *Distance learning* (18,526 test units across 1,498 essays).

| Difficulty Tier | Held-out Prompt Name | Test Units (N) | Test Essays (N) | RF Macro-F1 | DeBERTa Macro-F1 | Macro-F1 Delta | RF Accuracy | DeBERTa Accuracy | RF Ineff F1 | DeBERTa Ineff F1 |
|---|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Hardest (Rank 1/15)** | *"A Cowboy Who Rode the Waves"* | 5,158 | 688 | 0.3501 | **0.4082** | **+0.0581** | 79.20% | 78.87% | 0.1085 | **0.1246** |
| **Median (Rank 8/15)** | *Summer projects* | 9,855 | 875 | 0.4339 | **0.4642** | **+0.0303** | 70.24% | 66.58% | 0.0000 | **0.0759** |
| **Easiest (Rank 15/15)** | *Distance learning* | 18,526 | 1,498 | 0.5014 | **0.5735** | **+0.0721** | 78.05% | 75.55% | 0.0649 | **0.2509** |

> **Summary on 3 Representative Prompts:**  
> **Mean DeBERTa Macro-F1:** **0.4820** vs **Classical RF:** **0.4285** (Macro-F1 Gain: **+0.0535 points**, **+12.49%** relative)

#### Rigorous Generalization Gap Comparison (In-Domain vs LOPO on the Same Prompt):
Comparing out-of-prompt DeBERTa against in-domain validation performance on the *identical prompt subset* isolates true prompt transfer:

| Held-out Prompt Name | In-Domain Val Units (N) | In-Domain DeBERTa Macro-F1 | LOPO DeBERTa Macro-F1 | True Generalization Gap | Relative Shift (%) |
|---|:---:|:---:|:---:|:---:|:---:|
| *"A Cowboy Who Rode the Waves"* | 1,030 | 0.4462 | 0.4082 | **-0.0380 points** | -8.52% |
| *Summer projects* | 2,074 | 0.4695 | 0.4642 | **-0.0053 points** | -1.12% |
| *Distance learning* | 3,533 | 0.5677 | 0.5735 | **+0.0058 points** | +1.03% |
| **Mean across 3 Prompts** | 6,637 | **0.4945** | **0.4820** | **-0.0125 points** | **-2.53%** |

*Key Findings:*
1. **DeBERTa Macro-F1 Advantage:** DeBERTa achieves higher Macro-F1 than Random Forest across all 3 held-out prompts (+0.0581 on Cowboy, +0.0303 on Summer, +0.0721 on Distance learning), primarily by recovering minority Ineffective identification.
2. **Accuracy Trade-off:** Due to balanced class weighting penalizing Ineffective misclassification, DeBERTa overall accuracy is slightly lower than Random Forest across all three prompts (Cowboy: 78.87% vs 79.20%; Summer: 66.58% vs 70.24%; Distance: 75.55% vs 78.05%).
3. **True Out-of-Prompt Drop:** When compared against in-domain performance on the *same prompt*, the generalization drop is moderate (-2.53% on average), showing that DeBERTa representations transfer well for universal topics while literary prompts suffer from unfamiliar source-text vocabulary.

---

### 6.5 Discourse Type Vulnerability under Out-of-Prompt Generalization

Evaluating performance changes across all 7 discourse types under the 3 LOPO folds (N = 33,539 units) reveals broad vulnerability groupings:

| Vulnerability Tier | Discourse Type | Evaluated Units (N) | Ineff Units (N) | In-Domain Macro-F1 | LOPO Mean Macro-F1 | Performance Delta | Relative Drop (%) | LOPO Ineff F1 |
|---|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **High Vulnerability** | **Rebuttal** | 1,441 | 23 | 0.5383 | 0.4156 | -0.1227 points | -22.79% | 0.0904 |
|  | **Evidence** | 9,716 | 323 | 0.6270 | 0.5056 | -0.1214 points | -19.36% | 0.1859 |
|  | **Concluding Statement** | 2,839 | 32 | 0.5980 | 0.4835 | -0.1145 points | -19.14% | 0.1439 |
| **Moderate Vulnerability** | **Lead** | 2,244 | 46 | 0.5567 | 0.4844 | -0.0723 points | -12.98% | 0.1171 |
|  | **Counterclaim** | 1,893 | 26 | 0.4796 | 0.4179 | -0.0617 points | -12.87% | 0.0871 |
|  | **Claim** | 12,391 | 98 | 0.5126 | 0.4517 | -0.0609 points | -11.87% | 0.1305 |
| **High Resilience** | **Position** | 3,015 | 36 | 0.5639 | 0.5061 | -0.0578 points | -10.26% | 0.1425 |

#### Linguistic Factors Explaining Vulnerability Tiers:
*Note on sample sizes:* Across the 3 folds, minority Ineffective units are scarce (only 23 in Rebuttal, 26 in Counterclaim, 32 in Concluding Statement). Thus, differences between -22.8% and -19.1% fall within sampling uncertainty, but broad tier separations remain evident:
1. **Source- and Relation-Dependent Units Suffer Greater Degradation:**
   - **`Evidence` and `Rebuttal`** experience the largest relative declines (~19% to 23%). Evidence units rely on prompt-specific reading texts, data citations, and topical terminology. In an unseen prompt, unfamiliar entities reduce classifier confidence. Rebuttals depend on tracing the author's refutation of prompt-specific arguments.
2. **Autonomous Stance Units Exhibit Resilience:**
   - **`Position`** is the most resilient discourse category (preserving ~89.7% of in-domain performance). Stance formulations rely heavily on universal syntactic markers (*"I believe"*, *"In my opinion"*, *"should not be allowed"*), which generalize cleanly across prompts.

---

## 7. Pedagogical Synthesis & Theoretical Inquiries

### 7.1 Conceptual Framework: Informational Requirements in Discourse Assessment
Based on our empirical observations, we propose a **Hypothetical Conceptual Framework** outlining the informational requirements necessary for automated writing evaluation:

```
Hypothetical Hierarchy of Information Requirements:
[Level 0: Isolated Unit]       --> Sufficient for basic rhetorical syntax (Adequate majority)
[Level 1: Sequential Neighbors] --> Helps relational units (Claim +0.043 F1, Counterclaim +0.030 F1)
[Level 2: Source Reading Text]  --> Hypothesized requirement for factual Evidence verification
[Level 3: Global Essay Context] --> Hypothesized requirement for holistic Position alignment
```

*Status:* Levels 0 and 1 have been empirically tested in this study. Levels 2 and 3 represent structured hypotheses to be verified in future work when prompt reading texts and document-level hierarchical attention are integrated.

### 7.2 Resolution of Reviewer Core Inquiries

#### Inquiry 1: *Trong 10 ca Ineffective, ca nào được đoán đúng nếu thấy đoạn văn xung quanh?*
- **Empirical Finding:** **0/10 ca lật sang nhãn Ineffective argmax**, nhưng xác suất P(Ineffective) tăng ở 8/10 ca (tăng trung bình 2.57x, trung vị 2.10x).
- **Lý giải bản chất:** Các lỗi này là **ngoại tại (extrinsic)**: Ca 2 ("paragraph 36") và Ca 5 cần bài đọc nguồn của đề bài; Ca 1 và 6 cần kiểm tra toàn bài để xác nhận không có Rebuttal. Ngữ cảnh cục bộ chỉ làm tăng sự nghi ngờ của mô hình chứ không đủ để lật nhãn.

#### Inquiry 2: *Với một đề mới, Macro-F1 giảm nhiều nhất ở loại đơn vị nào?*
- **Empirical Finding:** Các đơn vị phụ thuộc nội dung nguồn như **`Rebuttal` (sụt -22.79%)** và **`Evidence` (sụt -19.36%)** chịu mức giảm mạnh nhất. Ngược lại, **`Position` bền vững nhất (chỉ giảm -10.26%)** nhờ khuôn mẫu lập trường tu từ mang tính phổ quát.

#### Preparatory Inquiry: *Nếu người chấm thấy đề và cả bài còn mô hình chỉ thấy một đoạn, ta có thể quy lỗi cho năng lực mô hình đến đâu?*
- **Trực tiếp trả lời:** Dữ liệu thực nghiệm của nhóm chứng minh rằng **không thể quy phần lớn lỗi cho năng lực phân loại câu của mô hình**. Khi thêm ngữ cảnh lân cận (Level 1), Ineffective F1 chỉ tăng nhẹ +0.0193 điểm và 0/10 ca lỗi cực đoan lật nhãn. Điều này cho thấy trần hiệu năng của mô hình bị chặn bởi **sự thiếu hụt thông tin đầu vào (văn bản nguồn đề bài và liên kết toàn bài)** chứ không phải do mô hình thiếu tham số hay học kém. Muốn khắc phục các lỗi này, hệ thống cần được cấp bài đọc nguồn (source text) và cơ chế chú ý toàn bài.

---

## 8. Reproducibility Artifacts & Codebase Governance

All scripts and notebooks have been verified, cleaned of informal notes, and configured with fixed random seeds (42):

### 8.1 Modular Notebook Architecture & Interactive Google Colab Links

* **Notebook 04 — Length Confound & Classical LOPO Benchmark:**
  - **Colab Link:** [Open Script 04 in Google Colab](https://colab.research.google.com/drive/1YRMpJgGzZ0vWe7nA0W8c7n5JKMruVJHT?usp=sharing)  
  - **Full URL:** `https://colab.research.google.com/drive/1YRMpJgGzZ0vWe7nA0W8c7n5JKMruVJHT?usp=sharing`
  - **Local Files:** `04_Length_Confound_and_LOPO.py` / `04_length_confound_and_lopo_classical.ipynb`
  - **Scope:** 4-quartile length audit (N = 29,102 validation units) and 15-fold Random Forest LOPO cross-validation.
  - **Runtime:** CPU / ~15 minutes.

* **Notebook 05 — Controlled Contextual Ablation (Level 0 vs Level 1 DeBERTa):**
  - **Colab Link:** [Open Script 05 in Google Colab](https://colab.research.google.com/drive/1prcSnRHax0SAITnUbGsXks3aQ9pbwJD2?usp=sharing)  
  - **Full URL:** `https://colab.research.google.com/drive/1prcSnRHax0SAITnUbGsXks3aQ9pbwJD2?usp=sharing`
  - **Local Files:** `05_Context_Ablation_DeBERTa.py` / `05_context_ablation_deberta.ipynb`
  - **Scope:** Level 0 vs Level 1 comparative evaluation on 29,102 units, 7 discourse types breakdown, and 10 failure cases audit.
  - **Runtime:** GPU (Colab T4 / V100 / RTX) / ~75 minutes.

* **Notebook 06 — Leave-One-Prompt-Out Generalization (DeBERTa-v3):**
  - **Colab Link:** [Open Script 06 in Google Colab](https://colab.research.google.com/drive/1xiYMZ7SjRSAn_ioAvAbNh-PZDkghsiBk?usp=sharing)  
  - **Full URL:** `https://colab.research.google.com/drive/1xiYMZ7SjRSAn_ioAvAbNh-PZDkghsiBk?usp=sharing`
  - **Local Files:** `06_LOPO_DeBERTa.py` / `06_lopo_deberta.ipynb`
  - **Scope:** Fine-tunes DeBERTa-v3 across 3 representative difficulty tiers (Cowboy, Summer projects, Distance learning) on 14 prompts per fold, producing prompt generalization gaps and discourse type vulnerability breakdowns.
  - **Runtime:** GPU (Colab T4 / A100) / ~1.5–2.0 hours per fold.

### 8.2 Execution Environment Verification
All pipelines verify CUDA availability, preserve string typing on identifiers, enforce fixed `LABEL2ID` dictionary mapping, and log complete execution traces to `outputs/`.

---

## 9. References

* **Crossley, S. A., Baffour, P., Tian, Y., Franklin, A., Benner, M., & Boser, U. (2024).** A large-scale corpus for assessing written argumentation: PERSUADE 2.0. *Assessing Writing*, 61, Article 100830. [DOI: 10.1016/j.asw.2024.100830].
* **He, P., Gao, J., & Chen, W. (2023).** DeBERTaV3: Improving DeBERTa using ELECTRA-style pre-training with gradient-disentangled embedding sharing. *International Conference on Learning Representations (ICLR)*.
* **Newell, G. E., Beach, R., Smith, J., & VanDerHeide, J. (2011).** Teaching and learning argumentative writing: An integrative review. *Reading Research Quarterly*, 46(3), 273–304.
* **Stab, C., & Gurevych, I. (2014).** Identifying argumentative discourse structures in persuasive essays. *Conference on Empirical Methods in Natural Language Processing (EMNLP)*, 46–56.
* **Stab, C., & Gurevych, I. (2017).** Parsing argumentation structures in persuasive essays. *Computational Linguistics*, 43(3), 619–659.
* **Toulmin, S. E. (1958).** *The Uses of Argument*. Cambridge University Press.
