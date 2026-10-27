# Project Progress Report: Discourse Effectiveness Prediction on PERSUADE 2.0
**Course:** Machine Learning and Applications (62FIT4MLA) — Class CLC02  
**Group:** Group 06  
**Instructor:** Dr. Khanh  
**Academic Term:** Fall 2026  

---

## 1. Executive Progress Summary

* **Task Formulation:** We formulate the educational problem as an **ordinal 3-class text classification task** on student argumentative writing segments: predicting whether each discourse unit is `Ineffective` (0), `Adequate` (1), or `Effective` (2).
* **Dataset Standardization:** Cleaned and verified the official **PERSUADE 2.0** benchmark split (15,593 training essays with 144,289 labeled discourse units; 10,402 test essays with 93,677 labeled units).
* **Baseline Pipeline:** Implemented classical machine learning baselines using TF-IDF n-grams (up to 160,000 features), categorical one-hot encoding (discourse types, prompts), and standardized morphological/positional features with Logistic Regression and Linear Support Vector Machines (LinearSVC).
* **Advanced Encoders & Ensemble:** Fine-tuned pretrained transformer encoders (**BERT-base** and **DeBERTa-v3-base**), developed an optimal equal-weighted probability ensemble (**Ensemble Run A003**), and applied post-hoc temperature scaling ($T = 0.904014$) to achieve calibrated probabilities (ECE $< 1\%$).
* **Practical Educational Deliverable:** Designed an actionable **Teacher-Review Budget Curve**: reviewing just the top **10%** highest-risk segments captures **61.42%** of all ineffective arguments across the corpus.

---

## 2. Alignment with Instructor Feedback

| # | Instructor Feedback & Guidance | Action Taken & Implementation Status |
|---|---|---|
| 1 | **Dataset License Correction** | Corrected from `CC BY 4.0` to the official **`CC BY-NC-SA 4.0`** (*Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International*), referencing Scott Crossley et al. (*Assessing Writing*, 2024). |
| 2 | **Official Sample Counts** | Replaced arbitrary splits with the **official corpus benchmark**: exactly 144,289 labeled training segments and 93,677 test segments across 15 prompts. |
| 3 | **Classical Algorithm Baselines** | Formally established **TF-IDF + Logistic Regression** and **TF-IDF + Linear SVM** as classical baselines; analyzed why both exhibit near-identical linear decision boundaries. |
| 4 | **Classical & Business Metrics** | Evaluated models using classical metrics (**Accuracy, Macro-F1, Weighted-F1, Log-loss, QWK**) with dedicated priority on **Ineffective Recall** for early educational triage. |
| 5 | **Analysis of Low Baseline Scores** | Investigated the **Accuracy Paradox** (Accuracy ~79% while Ineffective Recall is only 16.55%) caused by extreme class imbalance and lexical isolation of segment-only TF-IDF. |
| 6 | **Outperforming the Baseline** | Demonstrated significant gains using **DeBERTa-v3-base** and **BERT + DeBERTa Ensemble** (Macro-F1 increased from 0.5101 to **0.6022**; Ineffective Recall surged from 16.55% to **47.87%**). |
| 7 | **Deep EDA on Ineffective Segments** | Quantified Ineffective rates across **7 discourse types**, examined whether weak arguments are short vs. long vs. verbatim copies, and analyzed prompt hardness and ELL subgroup fairness. |

---

## 3. Dataset Analysis & Rationale

### 3.1. Analytical Rationale (Why analyze and select these features?)
* **Label Distribution Analysis:** Necessary to diagnose class imbalance and prevent model collapse into majority-class guessing (`Adequate`).
* **Discourse Type Breakdown:** Structural elements serve distinct argumentative functions (evidence vs. claims); analyzing their individual error rates determines whether `discourse_type` must be an explicit conditioning feature.
* **Morphological & Word Count Analysis:** Tests the hypothesis of whether weak arguments are simply short, preventing models from adopting superficial length shortcuts.
* **Prompt-Level Variance:** Compares text-dependent tasks against independent tasks to assess prompt-memorization risks and motivate unseen prompt generalization.
* **ELL Subgroup Analysis:** Evaluates demographic fairness to ensure models evaluate logical soundness rather than penalizing non-native syntactic surface errors.

### 3.2. Quantitative Findings

#### Class Distribution (144,289 Labeled Training Segments):
* `Ineffective`: **6,462 (4.48%)** — minority class (17.5x smaller than Adequate).
* `Adequate`: **113,244 (78.48%)** — overwhelming majority class.
* `Effective`: **24,583 (17.04%)** — upper tier.

#### Ineffective Rate Across 7 Discourse Types:
* **Evidence (6.91%)** and **Rebuttal (4.87%)** exhibit the highest Ineffective rates. These require higher-order reasoning, synthesis, and factual grounding, which K-12 students struggle with most.
* **Claim (2.94%)** and **Position (3.05%)** show the lowest Ineffective rates (~80–85% achieve `Adequate`), as stating subjective stances is relatively straightforward.

#### Morphological Behavior: Are Ineffective arguments short, long, or verbatim copies?
* **Concluding Statements & Leads:** Ineffective instances are **short and abrupt** (Mean: 34.9 and 37.3 words vs. 94.8 and 83.3 words for Effective), typically repeating the prompt in a single brief sentence without synthesis.
* **Evidence:** Ineffective evidence is **longer than Adequate evidence** (Mean: **74.3 words** vs. 66.0 words) but fails because students **reproduce verbatim source texts** or narrate off-topic stories without analytical commentary.
* *Takeaway:* Ineffective arguments are **not simply short**. Pure length-based features misclassify copied passages as competent arguments.

#### Prompt-Level Hardness (15 Prompts):
* **Text-Dependent Tasks** requiring complex reading comprehension (*Does the electoral college work?*: 11.54%, *Exploring Venus*: 11.43%, *Face on Mars*: 9.89%) show **10x higher Ineffective rates** than **Independent Tasks** (*Summer projects*: 0.89%, *Phones & driving*: 1.06%).
* Demonstrates that models easily overfit to prompt-specific vocabulary unless evaluated across unseen prompts.

#### Demographic Fairness (ELL vs. Non-ELL):
* English Language Learners (`ELL = Yes`) have an Ineffective label rate of **10.42%**, compared to **4.13%** for native speakers (`ELL = No`) — a **2.52x disparity**.
* *Design Constraint:* Demographic attributes (`ell_status`, `gender`, `race`) are strictly excluded from model inputs to prevent algorithmic discrimination.

---

## 4. Experimental Results & In-Depth Output Analysis

### 4.1. Classical Baseline Performance

| Model Configuration | Validation Accuracy | Validation Macro-F1 | Validation QWK | Ineffective Recall | Test Accuracy (46,856 segs) | Test Macro-F1 | Test Ineffective Recall |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Logistic Regression ($C=2.0$, Balanced)** | 6.13% ⚠️ | 0.0477 | 0.0122 | **73.99%** | — | — | — |
| **Linear SVM ($C=1.0$, Unweighted)** | 78.25% | 0.4986 | 0.3217 | 15.92% | — | — | — |
| **Linear SVM ($C=2.0$, Unweighted)** | 77.21% | 0.4850 | 0.3000 | 14.87% | — | — | — |
| **Tuned Linear SVM ($C=0.5$, Selected Baseline)** | **79.20%** | **0.5101** | **0.3406** | **16.55%** | **78.89%** | **0.5131** | **17.47%** |
| **Logistic Regression (Threshold-Optimized)** | 77.66% | **0.5314** | **0.3727** | **27.36%** | — | — | — |

#### Why are Classical Baseline scores deceptive and Ineffective Recall low?
1. **The Accuracy Paradox:** The Linear SVM achieves an apparently high test accuracy of **78.89%**, yet its **Macro-F1 is only 0.5131** and **Ineffective Recall is only 17.47%**. On 2,026 test Ineffective segments, it correctly identifies only 354, misclassifying **1,580 segments (78.0%) as Adequate**.
2. **Failure of Naive Class Weighting:** Setting `class_weight='balanced'` in Logistic Regression causes accuracy to collapse to **6.13%** because linear TF-IDF representations lack boundary precision, triggering overwhelming false alarms.
3. **Representational Bottleneck of TF-IDF:** Bag-of-words ignores syntax, discourse markers, and cross-sentence cohesion. It cannot distinguish between genuine analysis and uncritical source copying.
4. **Threshold Optimization Gain:** Shifting decision boundaries using expected continuous scores improved QWK from 0.2014 to **0.3727** and Ineffective Recall to **27.36%**, but linear features plateau around Macro-F1 ~0.53.

---

### 4.2. Superiority of Pretrained Transformers & Ensemble (Run A003)

| Metric | Tuned Linear SVM Baseline | BERT-base (N1) | DeBERTa-v3-base (N2) | **Ensemble BERT + DeBERTa (A003)** | Net Improvement vs. Baseline |
|---|:---:|:---:|:---:|:---:|:---:|
| **Accuracy** | **79.20%** | 77.12% | 77.58% | **77.65%** | *-1.55% (balanced trade-off)* |
| **Macro-F1** | 0.5101 | 0.5885 | 0.5991 | **0.6022** 🏆 | **+0.0921 (+18.06%)** |
| **Quadratic Weighted Kappa (QWK)** | 0.3406 | 0.4612 | 0.4745 | **0.4784** 🏆 | **+0.1378 (+40.46%)** |
| **Ineffective Recall** | 16.55% | 45.20% | 46.85% | **47.87%** 🏆 | **+31.32% (2.89x higher)** |
| **Ineffective Precision** | 27.90% | 31.80% | 33.10% | **33.52%** | **+5.62%** |
| **Ineffective F1** | 0.2149 | 0.3732 | 0.3879 | **0.3943** 🏆 | **+0.1794 (+83.48%)** |
| **Log-Loss** | — | 0.5340 | 0.5162 | **0.5112** 🏆 | **Substantially reduced** |
| **Expected Calibration Error (ECE)** | — | 0.0245 | 0.0152 | **0.0099** 🏆 | **Calibrated to < 1%** |

#### Confusion Matrix of Ensemble A003 (14,303 Validation Segments):
```
                      Predicted: Ineffective   Predicted: Adequate   Predicted: Effective
Actual: Ineffective            304                     320                    11
Actual: Adequate               594                   9,364                 1,339
Actual: Effective                9                     924                 1,438
```

#### Statistical Significance & Practical Triage:
* **Paired Cluster Bootstrap (2,000 iterations by essay):** 95% CI of the Macro-F1 difference between Ensemble and DeBERTa is $[-0.005156, +0.011460]$. While Ensemble provides better calibration and a modest lift (+0.00316), DeBERTa alone delivers ~99.5% of the ensemble performance at half the inference latency.
* **Review Budget Curve:**
  * Top 5% review budget $\rightarrow$ finds 265 / 635 Ineffective units (**41.73% Recall**, 37.01% Precision).
  * **Top 10% review budget** $\rightarrow$ finds 390 / 635 Ineffective units (**61.42% Recall**, 27.25% Precision).
  * Top 20% review budget $\rightarrow$ finds 506 / 635 Ineffective units (**79.69% Recall**, 17.69% Precision).

---

## 5. Next Steps & Optimization Plan

To advance our results toward publication-grade rigor, our subsequent work focuses on systematic model fine-tuning, loss function adaptation, and generalization testing:

### 5.1. Model Architecture & Representation Refinements
1. **Full-Essay Context Windowing:** Rather than encoding discourse text in isolation, prepend local discourse context and preceding claims: `[CLS] [DISCOURSE_TYPE] segment_text [SEP] preceding_claim [SEP] prompt_name [SEP]`.
2. **Contextual Pooling Schemes:** Replace standard `[CLS]` token pooling with **Multi-head Attention Pooling** or **Mean + Max Concatenation Pooling** across discourse token spans to better capture argument salience.

### 5.2. Loss Function & Objective Tuning
1. **Focal Loss Implementation:** Replace standard Cross-Entropy with multi-class Focal Loss:
   $$\mathcal{L}_{\text{Focal}} = -\alpha_t (1 - p_t)^\gamma \log(p_t), \quad \text{tuning } \gamma \in [1.5, 2.5] \text{ and class weights } \alpha$$
   This downweights easy majority Adequate examples and concentrates gradients on hard Ineffective boundaries.
2. **Ordinal Distance Penalty:** Integrate a pairwise ordinal loss penalty to strictly penalize catastrophic errors (misclassifying Ineffective directly into Effective).
3. **Label Smoothing Regularization:** Apply label smoothing ($\epsilon = 0.05$) to soften uncalibrated boundaries between adjacent Adequate and Effective human annotations.

### 5.3. Hyperparameter Tuning Protocol
1. **Layer-wise Learning Rate Decay (LLRD):** Apply decay rate $\eta = 0.90$ across DeBERTa layers, setting lower learning rates for lower lexical layers ($5e-6$) and higher rates for upper classification layers ($2e-5$).
2. **Warmup & Scheduler Optimization:** Implement Cosine Annealing with 10% linear warmup across 4–5 epochs.
3. **Gradient Accumulation & Batch Scaling:** Scale effective batch size to 32 using gradient accumulation steps to stabilize minority-class gradients.

### 5.4. Unseen Prompt Generalization & Fairness Calibration
1. **Leave-One-Prompt-Out (LOPO) Benchmark:** Validate DeBERTa vs. Baselines on unseen test prompts (*Does the electoral college work?* and *Distance learning*) to measure cross-topic argument transfer.
2. **Subgroup Threshold Post-Processing:** Calibrate decision thresholds separately across ELL vs. Non-ELL subgroups to equalize False Positive Rates (FPR parity), ensuring language learners are not penalized for surface grammatical non-fluencies.
3. **Quantization for Deployment:** Quantize the fine-tuned DeBERTa model to INT8 (ONNX Runtime) to reduce inference latency for practical classroom teacher assistance.
