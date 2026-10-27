# 📊 Báo Cáo Phân Tích PERSUADE Corpus 2.0

---

## 1. Tổng Quan Dataset

| Thuộc tính | Giá trị |
|---|---|
| **Tên** | PERSUADE Corpus 2.0 (Persuasive Essays for Rating, Selecting, and Understanding Argumentative and Discourse Elements) |
| **Nguồn** | Kaggle — Feedback Prize Competitions (The Learning Agency Lab) |
| **Kích thước file** | ~617 MB |
| **Tổng số dòng** | 173,266 dòng (mỗi dòng = 1 discourse element) |
| **Số bài luận unique** | 15,594 bài luận |
| **Trung bình discourse/bài** | ~11 elements/essay |
| **Licence** | CC BY 4.0 (Creative Commons Attribution) — phù hợp cho nghiên cứu & giáo dục |

---

## 2. Mô Tả Các Trường Dữ Liệu (27 cột)

### 2.1 Nhóm định danh & văn bản
| Cột | Mô tả | Null |
|---|---|---|
| `essay_id` | ID bài luận (dạng số) | 0 |
| `essay_id_comp` | ID dùng cho competition | 0 |
| `competition_set` | Tập dữ liệu (train) | 0 |
| `full_text` | **Toàn bộ văn bản bài luận** | 0 |
| `discourse_text` | **Đoạn văn bản của discourse element** | 0 |
| `essay_word_count` | Số từ trong bài (min 146, max 14714, mean ~430) | 0 |

### 2.2 Nhóm annotation — Discourse
| Cột | Mô tả | Null |
|---|---|---|
| `discourse_id` | ID của discourse element | 0 |
| `discourse_start` / `discourse_end` | Vị trí ký tự bắt đầu/kết thúc | 0 |
| `discourse_type` | **Loại discourse** (7 loại + Unannotated) | 0 |
| `discourse_type_num` | Thứ tự xuất hiện của loại discourse đó trong bài | 0 |
| `discourse_effectiveness` | **Chất lượng** (Effective / Adequate / Ineffective) | 28,977 null |

### 2.3 Nhóm annotation — Hierarchical
| Cột | Mô tả | Null |
|---|---|---|
| `hierarchical_id` | ID phân cấp | 78,589 null |
| `hierarchical_text` | Văn bản phân cấp | 78,589 null |
| `hierarchical_label` | Nhãn phân cấp (Position, Claim, Counterclaim, Rebuttal, Evidence) | 78,589 null |

### 2.4 Nhóm bài tập & đề bài
| Cột | Mô tả | Null |
|---|---|---|
| `prompt_name` | **Tên đề bài** (15 đề) | 0 |
| `assignment` | Nội dung đề bài chi tiết | 0 |
| `task` | Loại bài (Independent / Text dependent) | 0 |
| `source_text` | Văn bản nguồn (cho text-dependent tasks) | 96,207 null |
| `provider` | Nguồn cung cấp (Virginia, Indiana, Florida, NCES, Georgia Virtual) | 0 |

### 2.5 Nhóm demographics học sinh
| Cột | Mô tả | Null |
|---|---|---|
| `gender` | Giới tính (F: 89,681 / M: 83,585) | 0 |
| `grade_level` | Lớp (6, 8, 9, 10, 11, 12) | 7,381 null |
| `ell_status` | English Language Learner (Yes/No) | 7,530 null |
| `race_ethnicity` | Nhóm sắc tộc (6 nhóm) | 0 |
| `economically_disadvantaged` | Tình trạng kinh tế | 38,060 null |
| `student_disability_status` | Tình trạng khuyết tật | 37,737 null |

### 2.6 Điểm holistic
| Cột | Mô tả | Null |
|---|---|---|
| `holistic_essay_score` | **Điểm tổng thể bài luận** (1–6) | 0 |

---

## 3. Phân Tích Khả Thi Về Mặt Dữ Liệu

### ✅ Điểm mạnh

| Tiêu chí | Đánh giá |
|---|---|
| **Kích thước** | 15,594 bài luận — đủ lớn cho deep learning, rất tốt cho traditional ML |
| **Multi-level labels** | 3 tầng nhãn: holistic score (essay-level), discourse type (segment-level), effectiveness (segment-level) |
| **Rich metadata** | Demographics đầy đủ (giới tính, lớp, ELL, sắc tộc) → hỗ trợ fairness analysis |
| **Đa dạng đề bài** | 15 prompt khác nhau → giảm bias theo chủ đề |
| **Licence mở** | CC BY 4.0 — tự do sử dụng |
| **Đã pre-segmented** | Discourse elements đã được annotate sẵn → tiết kiệm rất nhiều effort |

### ⚠️ Điểm cần lưu ý

| Vấn đề | Chi tiết |
|---|---|
| **Imbalanced labels** | Score phân bố lệch: Score 1 chỉ có 610 bài (~3.9%) vs Score 3–4 chiếm ~58.6% |
| **Effectiveness rất imbalanced** | Ineffective chỉ 6,462 (~4.5%) vs Adequate 113,244 (~78.5%) |
| **Missing values** | `discourse_effectiveness` thiếu 28,977 dòng; `hierarchical_*` thiếu ~78K dòng; demographics thiếu 7K–38K |
| **Subjectivity** | Holistic score 1–6 có tính chủ quan cao; chênh lệch giữa các annotator là unavoidable |
| **English only** | Chỉ có bài viết tiếng Anh, giới hạn ở học sinh Mỹ lớp 6–12 |

### 📊 Phân bố chi tiết

**Holistic Essay Score (per essay):**
```
Score 1: ████                          610  (3.9%)
Score 2: █████████████████            3,218 (20.6%)
Score 3: ██████████████████████████   4,943 (31.7%)
Score 4: ██████████████████████       4,194 (26.9%)
Score 5: ███████████                  2,082 (13.4%)
Score 6: ███                            547  (3.5%)
```

**Discourse Type Distribution:**
```
Claim:                █████████████████████████  50,208
Evidence:             ██████████████████████     45,702
Unannotated:          ██████████████             28,973
Position:             ████████                   15,419
Concluding Statement: ███████                    13,505
Lead:                 █████                       9,305
Counterclaim:         ███                         5,817
Rebuttal:             ██                          4,337
```

**Cross-tab: Score ↔ Effectiveness** (tỷ lệ hàng):
| Score | Adequate | Effective | Ineffective |
|---|---|---|---|
| 1 | 39.7% | 0.5% | **59.8%** |
| 2 | 83.4% | 3.6% | 13.0% |
| 3 | 88.8% | 7.4% | 3.9% |
| 4 | 82.9% | 16.2% | 0.9% |
| 5 | 61.2% | 38.5% | 0.3% |
| 6 | 46.1% | **53.8%** | 0.2% |

> [!IMPORTANT]
> Cross-tab cho thấy **discourse effectiveness** và **holistic score** có tương quan mạnh — bài Score 6 có 53.8% discourse elements rated "Effective", trong khi bài Score 1 có 59.8% "Ineffective". Đây là tín hiệu feature engineering rất có giá trị.

---

## 4. Các Chủ Đề Nghiên Cứu / Dự Án Có Thể Làm

| # | Chủ đề | Task ML | Đối tượng phục vụ |
|---|---|---|---|
| 1 | **Automated Essay Scoring (AES)** | Regression/Ordinal Classification (dự đoán score 1–6) | Giáo viên chấm bài |
| 2 | **Discourse Element Classification** | Multi-class Classification (7 loại discourse) | Learner nhận feedback |
| 3 | **Discourse Effectiveness Prediction** | Ordinal Classification (3 mức effectiveness) | Learner cải thiện viết |
| 4 | **Argumentation Structure Mining** | Sequence Labeling / Hierarchical Classification | Curriculum designer |
| 5 | **ELL Writing Proficiency Analysis** | Binary/Multi-class + Fairness Analysis | Giáo viên ESL |
| 6 | **Writing Quality Gap Analysis** | Statistical + ML (demographic bias detection) | Nhà quản lý giáo dục |
| 7 | **Essay Feedback Generation** | Multi-task (score + discourse type + effectiveness) | Learner tự học |

---

## 5. Ba Model Plan / Pipeline Chi Tiết

---

### 🔬 MODEL PLAN A: Automated Essay Scoring (AES)

#### 1. Problem and User

| Mục | Nội dung |
|---|---|
| **Vấn đề** | Giáo viên mất 3–5 phút chấm mỗi bài luận argumentative; với lớp 30–40 học sinh × 4–5 bài/kỳ, khối lượng rất lớn. Cần công cụ **sàng lọc sơ bộ** (first-pass screening) để giáo viên tập trung vào bài cần attention nhất. |
| **User** | **Giáo viên ELA (English Language Arts)** lớp 6–12. |
| **Decision** | Tool dự đoán score 1–6 → giáo viên ưu tiên chấm lại bài có predicted score thấp (1–2) hoặc bài mà model "không chắc" (low confidence). Giáo viên vẫn là người ra quyết định cuối cùng. |

#### 2. Data

| Mục | Chi tiết |
|---|---|
| **Data route** | Public benchmark — PERSUADE Corpus 2.0 |
| **Dataset** | [persuade_corpus_2.0_train.csv](file:///c:/Users/ADMIN/Desktop/MLA%20Dataset/persuade_corpus_2.0_train.csv) |
| **Size** | 15,594 unique essays (617 MB raw) |
| **Fields sử dụng** | `full_text` (input), `holistic_essay_score` (target 1–6), `prompt_name`, demographics cho fairness analysis |
| **Licence** | CC BY 4.0 |

#### 3. ML Task Alignment

```
Input:  full_text (toàn bộ bài luận, avg ~430 từ)
Output: holistic_essay_score ∈ {1, 2, 3, 4, 5, 6} — Ordinal Classification

Một training example:
  X: "Modern humans today are always on their phone. They are always
      on their phone more than 5 hours a day no stop..."  (378 từ)
  y: 3
```

> [!WARNING]
> **Label imbalance**: Score 1 (3.9%) và Score 6 (3.5%) rất ít so với Score 3–4 (~58%). Cần stratified sampling và weighted loss.
> **Subjectivity**: Inter-annotator agreement cho essay scoring thường chỉ κ ≈ 0.6–0.7 (moderate–substantial).

#### 4. Model Plan

| Model Family | Lý do chọn |
|---|---|
| **Model 1: Gradient Boosted Trees (LightGBM/XGBoost)** | Baseline mạnh và interpretable. Input = hand-crafted features: (1) essay_word_count, (2) sentence count, (3) vocabulary richness (type-token ratio), (4) average sentence length, (5) discourse-type distribution (% Claim, % Evidence, etc.), (6) % discourse elements rated Effective/Adequate/Ineffective, (7) number of Counterclaim + Rebuttal (argumentation complexity), (8) spelling/grammar error count. GBDT xử lý tốt tabular features và imbalanced classes. |
| **Model 2: Fine-tuned DeBERTa-v3-base** | State-of-the-art cho NLP tasks, đặc biệt essay scoring. Fine-tune trên `full_text` với ordinal regression head (MSE loss trên score chuẩn hóa). DeBERTa có disentangled attention mechanism, xử lý tốt long-range dependencies trong bài luận. Max sequence length = 512–1024 tokens. |
| **Tại sao 2 model này?** | GBDT cho interpretability (giáo viên hiểu tại sao) + DeBERTa cho accuracy tối đa. Ensemble 2 model (weighted average) thường cho kết quả tốt nhất trên AES benchmarks. |

#### 5. Evaluation Plan

| Mục | Chi tiết |
|---|---|
| **Data split** | **Stratified 5-fold CV** (stratify by `holistic_essay_score`). Holdout 10% test set. Đảm bảo tất cả discourse elements của 1 essay nằm trong cùng 1 fold (group by `essay_id_comp`). |
| **Primary metric** | **Quadratic Weighted Kappa (QWK)** — metric chuẩn cho AES, phạt nặng khi predicted score cách xa true score. |
| **Secondary metrics** | RMSE, Spearman correlation, per-class F1 (đặc biệt cho Score 1 và Score 6). |
| **Tại sao accuracy không đủ?** | Nếu model luôn đoán Score 3 → accuracy ~31.7% nhưng hoàn toàn vô dụng. QWK = 0 cho prediction constant → đúng mục đích. Accuracy cũng không phân biệt sai 1 bậc vs sai 4 bậc. |
| **Baseline** | (1) **Majority class**: luôn đoán Score 3 → QWK = 0. (2) **Linear regression** trên `essay_word_count` alone → ước tính QWK ~0.3–0.4. Model phải beat cả hai. |

#### 6. Risks and Responsible Use

| Risk | Mitigation |
|---|---|
| **Bias theo demographics** | ELL students và minority groups có thể bị penalize bất công → chạy fairness audit (QWK per subgroup, equalized odds). Nếu gap > 0.1 QWK, cần recalibrate. |
| **Over-reliance** | Giáo viên có thể lười chấm lại → thiết kế UI bắt buộc confirm/override cho mỗi bài. Score chỉ hiện dạng "suggested range" (e.g., 3–4), không phải con số tuyệt đối. |
| **Reward hacking** | Học sinh có thể học cách viết dài hơn thay vì viết hay hơn (word count correlation) → monitor feature importance, diversify features. |
| **Human control** | Giáo viên LUÔN có quyền override. Model score KHÔNG tự động vào sổ điểm. Tool chỉ là first-pass filter. |

---

### 🔬 MODEL PLAN B: Discourse Element Classification + Effectiveness Prediction (Multi-task Writing Feedback)

#### 1. Problem and User

| Mục | Nội dung |
|---|---|
| **Vấn đề** | Học sinh viết bài argumentative nhưng không biết cấu trúc lập luận của mình có hợp lý không. Họ cần feedback **cụ thể theo từng đoạn**: "Đoạn này là Claim hay Evidence?", "Claim này Effective hay Ineffective?". |
| **User** | **Học sinh lớp 6–12** đang luyện viết argumentative essay, sử dụng tool tự học (self-practice). |
| **Decision** | Tool highlight từng đoạn trong bài với nhãn discourse type + effectiveness → học sinh tự sửa. Giáo viên dùng dashboard tổng hợp để thấy pattern yếu kém chung của cả lớp. |

#### 2. Data

| Mục | Chi tiết |
|---|---|
| **Data route** | Public benchmark — PERSUADE Corpus 2.0 |
| **Dataset** | [persuade_corpus_2.0_train.csv](file:///c:/Users/ADMIN/Desktop/MLA%20Dataset/persuade_corpus_2.0_train.csv) |
| **Size** | 173,266 discourse elements từ 15,594 essays |
| **Fields sử dụng** | `discourse_text` (input), `discourse_type` (target 1 — 7 classes), `discourse_effectiveness` (target 2 — 3 classes, 28,977 null). `full_text` cho context. |
| **Licence** | CC BY 4.0 |

#### 3. ML Task Alignment

**Task 1 — Discourse Type Classification:**
```
Input:  discourse_text + context (surrounding text from full_text)
Output: discourse_type ∈ {Lead, Position, Claim, Counterclaim, Rebuttal,
        Evidence, Concluding Statement}

Ví dụ:
  X: "They are some really bad consequences when stuff happens
      when it comes to a phone."
  y: Position
```

**Task 2 — Discourse Effectiveness Prediction:**
```
Input:  discourse_text + discourse_type + context
Output: discourse_effectiveness ∈ {Ineffective, Adequate, Effective}

Ví dụ:
  X: ("They are some really bad consequences...", type=Position)
  y: Adequate
```

> [!WARNING]
> **Effectiveness cực kỳ imbalanced**: Ineffective chỉ 4.5%. Cần SMOTE, class weights, hoặc focal loss.
> **28,977 null** ở `discourse_effectiveness` (các "Unannotated" segments) → loại bỏ hoặc semi-supervised.

#### 4. Model Plan

| Model Family | Lý do chọn |
|---|---|
| **Model 1: Logistic Regression + TF-IDF** | Baseline interpretable. TF-IDF trên `discourse_text` + one-hot `discourse_type` (cho Task 2). Logistic Regression multiclass với class weights. Cho phép giáo viên hiểu "từ/cụm từ nào khiến đoạn này bị rated Ineffective" (top coefficients). |
| **Model 2: Fine-tuned BERT-base (Multi-task)** | BERT encode discourse_text với context window (256 tokens trước + sau). Hai classification heads: (1) discourse type (7 classes), (2) effectiveness (3 classes). Shared encoder giúp transfer knowledge giữa 2 tasks — biết loại discourse giúp đánh giá effectiveness tốt hơn. Multi-task training cải thiện cả hai tasks. |
| **Tại sao 2 model này?** | LR+TF-IDF là baseline nhanh, interpretable, cho thấy lower bound. BERT multi-task khai thác context và sự liên quan giữa 2 tasks → expected SOTA. So sánh 2 model cho thấy "deep context" đáng bao nhiêu accuracy. |

#### 5. Evaluation Plan

| Mục | Chi tiết |
|---|---|
| **Data split** | **Stratified GroupKFold (5 folds)**, group by `essay_id_comp`. Đảm bảo mọi discourse elements của 1 essay ở cùng fold (tránh data leakage từ cùng bài). |
| **Task 1 metrics** | **Macro F1** (vì Counterclaim/Rebuttal rất ít, macro F1 phạt nặng nếu bỏ qua minority classes). Per-class precision & recall. |
| **Task 2 metrics** | **Log-loss** (calibrated probabilities quan trọng — feedback "80% likely Ineffective" hữu ích hơn hard label) + **Macro F1**. |
| **Tại sao accuracy không đủ?** | Task 1: luôn đoán "Claim" → accuracy ~34.8% (misleading). Task 2: luôn đoán "Adequate" → accuracy ~78.5% (rất misleading!). Macro F1 = 0.33 cho constant predictor → đúng. |
| **Baseline** | Task 1: Majority class ("Claim") → Macro F1 ~0.06. Task 2: Majority class ("Adequate") → Macro F1 ~0.26. |

#### 6. Risks and Responsible Use

| Risk | Mitigation |
|---|---|
| **Sai nhãn → feedback sai** | Học sinh tin tool và không sửa đoạn thực sự yếu, hoặc sửa đoạn đã tốt → chỉ hiện feedback khi confidence > 0.7. Dưới 0.7 → "I'm not sure about this paragraph". |
| **Discouraging students** | Quá nhiều "Ineffective" labels → học sinh nản → show positive feedback trước ("3 paragraphs are well-structured"), rồi mới suggest improvements. |
| **Prompt-specific bias** | Model có thể overfit đề bài training (15 prompts) → evaluate trên unseen prompt (leave-one-prompt-out). |
| **Human control** | Giáo viên có thể override/hide feedback cho từng học sinh. Học sinh luôn thấy disclaimer "This is AI-generated feedback, discuss with your teacher". |

---

### 🔬 MODEL PLAN C: Fairness-Aware Writing Assessment — Phát Hiện Bias Trong Chấm Điểm

#### 1. Problem and User

| Mục | Nội dung |
|---|---|
| **Vấn đề** | Có bằng chứng rằng AES systems có thể biased against ELL students, minority students, và economically disadvantaged students. Cần công cụ **audit** xem scoring patterns có công bằng không, và build model AES giảm thiểu bias. |
| **User** | **Curriculum designer / Nhà quản lý giáo dục** cần đánh giá fairness của hệ thống chấm điểm hiện tại, và **giáo viên** cần một tool chấm điểm ít bias hơn. |
| **Decision** | Tool cung cấp: (1) Dashboard fairness metrics, (2) Flagged essays nơi human vs model scores differ significantly across demographic groups. |

#### 2. Data

| Mục | Chi tiết |
|---|---|
| **Data route** | Public benchmark — PERSUADE Corpus 2.0 |
| **Dataset** | [persuade_corpus_2.0_train.csv](file:///c:/Users/ADMIN/Desktop/MLA%20Dataset/persuade_corpus_2.0_train.csv) |
| **Size** | 15,594 essays với đầy đủ demographics |
| **Fields sử dụng** | `full_text`, `holistic_essay_score`, `gender`, `race_ethnicity`, `ell_status`, `grade_level`, `economically_disadvantaged`, `prompt_name` |
| **Licence** | CC BY 4.0 |
| **Lưu ý** | `economically_disadvantaged` thiếu 38K rows (~22%), `ell_status` thiếu 7.5K rows → impute hoặc analyze subset. |

#### 3. ML Task Alignment

```
PRIMARY TASK — Score Prediction (giống Plan A):
Input:  full_text
Output: holistic_essay_score ∈ {1, 2, 3, 4, 5, 6}

SECONDARY TASK — Fairness Audit:
Input:  (model predictions, true scores, demographic attributes)
Output: Fairness metrics per subgroup (QWK gap, error rate gap, 
        demographic parity difference)

Một training example:
  X: "Distance learning is a great way to learn because..."  (412 từ)
  y: 4
  metadata: {gender: F, race: Hispanic/Latino, ell: Yes, grade: 8}
  
  → Sau training, so sánh:
     QWK(model, truth | ELL=Yes) vs QWK(model, truth | ELL=No)
     Nếu gap > threshold → flag bias
```

> [!IMPORTANT]
> **Sensitive attributes KHÔNG được dùng làm features** trong model scoring. Chúng chỉ dùng trong post-hoc fairness audit.

#### 4. Model Plan

| Model Family | Lý do chọn |
|---|---|
| **Model 1: Ridge Regression trên linguistic features** | Interpretable baseline. Features: word count, sentence length, vocabulary diversity, grammatical error rate, discourse structure features (# claims, # evidence, etc.). Ridge (L2) regularization tránh overfit. Interpretability cao → dễ audit: nếu coefficient của "vocabulary diversity" quá cao, ELL students bất lợi vì vocab hạn chế → có thể điều chỉnh. |
| **Model 2: Fine-tuned DeBERTa + Adversarial Debiasing** | DeBERTa scoring model + gradient reversal layer cho demographic prediction. Ý tưởng: encoder được train để **tốt cho scoring** nhưng **không thể dự đoán demographics** từ representation. Fairness constraint built-in. So sánh QWK vs standard DeBERTa (không debiasing) để đo trade-off accuracy–fairness. |
| **Tại sao 2 model này?** | Ridge cho thấy bias ở đâu (feature-level). DeBERTa + adversarial cho thấy có thể giảm bias bao nhiêu mà không mất quá nhiều accuracy. Hai góc nhìn bổ sung: diagnostic (Ridge) + remediation (DeBERTa). |

#### 5. Evaluation Plan

| Mục | Chi tiết |
|---|---|
| **Data split** | Stratified 5-fold CV, group by `essay_id_comp`, stratify by `holistic_essay_score`. Đảm bảo distribution demographics cân bằng giữa các folds. |
| **Accuracy metrics** | QWK (primary), RMSE, per-score-class F1. |
| **Fairness metrics** | (1) **QWK gap**: max(QWK) − min(QWK) across demographic subgroups. (2) **Equal Opportunity Difference**: |TPR_group_A − TPR_group_B| cho each score threshold. (3) **Demographic Parity Difference**: |P(ŷ≥4 \| group_A) − P(ŷ≥4 \| group_B)|. |
| **Tại sao accuracy không đủ?** | Model có thể đạt QWK = 0.8 overall nhưng QWK = 0.6 cho ELL students → hại nhóm vulnerable nhất. Cần **disaggregated metrics**. |
| **Baseline** | (1) Standard DeBERTa (no debiasing) — là upper bound accuracy, lower bound fairness. (2) Random predictions — QWK ≈ 0, fairness gap ≈ 0 (trivially fair). Model phải Pareto-dominate: better accuracy than random AND better fairness than standard. |

#### 6. Risks and Responsible Use

| Risk | Mitigation |
|---|---|
| **Accuracy–fairness trade-off** | Adversarial debiasing thường giảm 2–5% QWK → cần transparent reporting: "QWK dropped from 0.82 to 0.79, but ELL gap reduced from 0.15 to 0.04". Curriculum designer quyết định trade-off chấp nhận được. |
| **Protected attributes leakage** | Dù không dùng demographics làm feature, thông tin có thể leak qua vocabulary, syntax (proxy variables) → adversarial training giúp nhưng không hoàn hảo. |
| **False sense of fairness** | "Debiased" model có thể vẫn biased theo dimensions không đo được (socioeconomic subtleties) → tool report "fairness on measured dimensions", không claim "completely fair". |
| **Misuse of demographics** | Nếu demographics bị dùng để lower scores → NGHIÊM CẤM. Demographics CHỈ dùng cho audit, không bao giờ là input. Pipeline có automated check: nếu demographic features xuất hiện trong feature vector → block training. |
| **Human control** | Curriculum designer review fairness report và quyết định deploy hay không. Không auto-deploy. Fairness thresholds do human experts đặt ra. |

---

## 6. So Sánh Tổng Hợp 3 Model Plans

| Tiêu chí | Plan A: AES | Plan B: Discourse Feedback | Plan C: Fairness Audit |
|---|---|---|---|
| **User chính** | Giáo viên | Học sinh | Curriculum designer |
| **Granularity** | Essay-level | Segment-level | Essay-level + subgroup |
| **ML Task** | Ordinal Classification | Multi-class + Multi-task | Ordinal + Adversarial |
| **Primary Metric** | QWK | Macro F1 | QWK + Fairness gaps |
| **Interpretability** | Medium (GBDT) to Low (DeBERTa) | High (LR) to Low (BERT) | High (Ridge) to Medium (Adversarial) |
| **Complexity** | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Impact giáo dục** | Tiết kiệm thời gian chấm | Cải thiện kỹ năng viết | Đảm bảo công bằng |
| **Độ khả thi** | ✅ Cao | ✅ Cao | ⚠️ Trung bình–Cao |

---

## 7. Khuyến Nghị

> [!TIP]
> **Nếu chọn 1 plan duy nhất**: Plan A (AES) là khả thi nhất, có benchmark rõ ràng (QWK), và trực tiếp giải quyết bài toán thực tế.
> 
> **Nếu muốn ambitious**: Plan B (Multi-task Feedback) tạo sản phẩm hữu ích nhất cho học sinh và showcase multi-task learning.
> 
> **Nếu muốn nổi bật về responsible AI**: Plan C (Fairness) rất relevant trong bối cảnh AI in Education hiện tại, nhưng đòi hỏi kiến thức fairness ML sâu hơn.

---

*Báo cáo được tạo dựa trên phân tích PERSUADE Corpus 2.0 — 15,594 bài luận argumentative từ học sinh lớp 6–12 tại Mỹ.*
