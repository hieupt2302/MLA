# TỔNG HỢP PHÂN TÍCH CHUYÊN SÂU 3 BÀI BÁO KHOA HỌC (AES / LLM / HUMAN-AI COLLABORATION)
**Dự án:** PERSUADE / MLA Scoring System  
**Ngày tổng hợp:** Tháng 10/2026  

---

## MỤC LỤC
1. [Paper R01: Yancey et al. (BEA 2023) — Rating Short L2 Essays on the CEFR Scale with GPT-4](#ma-paper-r01--rating-short-l2-essays-on-the-cefr-scale-with-gpt-4)
2. [Paper R02: Mansour et al. (LREC-COLING 2024) — Can Large Language Models Automatically Score Proficiency of Written Essays?](#ma-paper-r02--can-large-language-models-automatically-score-proficiency-of-written-essays)
3. [Paper R03: Xiao et al. (2024) — Human-AI Collaborative Essay Scoring: A Dual-Process Framework with LLMs](#ma-paper-r03--human-ai-collaborative-essay-scoring-a-dual-process-framework-with-llms)

---

# [Mã Paper: R01] — Rating Short L2 Essays on the CEFR Scale with GPT-4


## 1. METADATA & TRÍCH DẪN CHUẨN APA 7
- **Tác giả:** Kevin P. Yancey, Geoffrey T. LaFlair, Anthony R. Verardi, Jill Burstein
- **Đơn vị:** Duolingo
- **Năm xuất bản / Hội nghị:** 2023, BEA Workshop @ ACL 2023 (18th Workshop on Innovative Use of NLP for Building Educational Applications), Toronto, Canada
- **Trích dẫn APA 7 chuẩn:**
  > Yancey, K. P., LaFlair, G. T., Verardi, A. R., & Burstein, J. (2023). Rating short L2 essays on the CEFR scale with GPT-4. In *Proceedings of the 18th Workshop on Innovative Use of NLP for Building Educational Applications (BEA 2023)* (pp. 576–584). Association for Computational Linguistics. https://doi.org/10.18653/v1/2023.bea-1.49
- **Đường dẫn & Tài nguyên:**
  - ACL Anthology: https://aclanthology.org/2023.bea-1.49/
  - DOI: `10.18653/v1/2023.bea-1.49`
  - Code/Data: Paper không đề cập repository công khai. Dataset thuộc Duolingo English Test (proprietary).
- **Lưu ý phiên bản:** Đây là bản proceedings chính thức tại BEA 2023. Không có bản preprint trên arXiv.


---


## 2. BÀI TOÁN & THIẾT LẬP THỰC NGHIỆM (PROBLEM & SETUP)

- **Câu hỏi nghiên cứu chính:**
  GPT-4 (và GPT-3.5) có thể chấm điểm bài viết ngắn của người học tiếng Anh L2 trên thang CEFR tốt đến mức nào? Hiệu suất so với AWE truyền thống (XGBoost + feature engineering) và người chấm như thế nào? Có công bằng (fair) giữa các nhóm L1 và giới tính không?

- **Nhiệm vụ ML & Phạm vi:**
  - **Holistic Scoring (Chấm điểm tổng thể):** Phân loại 8 mức (6 cấp CEFR A1→C2 + 2 mức unscorable: No-Response, Nonsense/Off-Topic).
  - **Không có segmentation hay argument mining:** Toàn bộ bài viết ngắn (short essay) được chấm một lần duy nhất.
  - **Đánh giá zero-shot / few-shot qua prompt engineering**, KHÔNG fine-tune.

- **Dữ liệu thực nghiệm:**
  - **Nguồn:** Duolingo English Test — bài viết ngắn (5 phút) của người học L2.
  - **Kích thước mẫu:** ~10,000 ban đầu, lọc còn ~2,457 bài; phân tích chính trên n=1,175 bài (so sánh GPT vs Rater 1).
  - **Kiểm soát:** 7 ngôn ngữ L1 (Arabic, Mandarin, Telugu, English, Spanish, Gujarati, Bengali), cân bằng giới tính.
  - **⚠️ KHÔNG phải PERSUADE/Feedback Prize.** Đây là dataset riêng của Duolingo, không công khai.
  - **QWK giữa 2 người chấm:** 0.87 (inter-rater agreement con người cao).
  - 676 bài do assessment researchers double-rate (180 bài cả hai đồng ý → dùng làm calibration examples).

- **Thiết lập Input/Output:**
  - *Input:* Đề bài (prompt) + bài viết ngắn + rubric (tùy variant) + calibration examples (0–4 per category).
  - *Output:* 1 nhãn trong 8 mức (A1, A2, B1, B2, C1, C2, No-Response, Nonsense/Off-Topic), quy đổi 0–6 cho tính QWK.
  - *Điều kiện ranh giới:* Không áp dụng — bài viết là đơn vị nguyên vẹn, không tách discourse elements.

- **Các họ mô hình được khảo sát:**
  1. **GPT-3.5** (ChatGPT API, 4,096 token limit)
  2. **GPT-4** (8,192 token limit)
  3. **Baseline Length-Only:** Logistic Regression chỉ dùng character length
  4. **AWE Baseline (XGBoost):** 85 NLP features (cohesion, grammar complexity, lexical sophistication, accuracy, length, diversity, relevance) — hệ thống chấm điểm thực tế trên Duolingo English Test


---


## 3. KẾT QUẢ ĐỊNH LƯỢNG CỐT LÕI (KEY FINDINGS & NUMBERS)

| Mô hình / Thiết lập | Điều kiện | QWK (vs. Rater 1) | Ghi chú | Nguồn |
|---|---|---|---|---|
| **Human Rater 2 vs Rater 1** | Gold standard | **0.87** | Inter-rater agreement | Sec 2 |
| **AWE Baseline (XGBoost + 85 features)** | Trained trên ~100K+ bài | **0.84** | Strong baseline sản xuất thực tế | Sec 3.1, Fig 2 |
| **GPT-4 + 1 example/category** | Minimal rubric, 8 calibration examples | **0.81** | Gần bằng AWE, p<0.1 so với AWE | Sec 3.1, Fig 2 |
| **GPT-4 + 4 examples/category** | Minimal rubric, 32 calibration examples | ~0.82 | Cải thiện không đáng kể so với 1 example | Sec 3.1, Fig 2 |
| **GPT-4 + 0 examples** | Minimal rubric, zero-shot | ~0.55 | Kém hơn cả Length-Only baseline | Sec 3.1, Fig 2 |
| **GPT-3.5 + 2 examples/category** | Minimal rubric, max fitting (16 examples) | ~0.65 | Chỉ vừa vượt Length-Only baseline | Sec 3.1 |
| **GPT-3.5 + 0 examples** | Zero-shot | ~0.45 | Rất kém | Sec 3.1 |
| **Length-Only Baseline** | Character length only | ~0.60 | Đáng ngạc nhiên đã khá cao | Sec 3.1 |
| **GPT-4 + Detailed Rubric (0 ex.)** | With rubric, no examples | ~0.72 | Cải thiện lớn khi zero-shot | Sec 3.2, Fig 4 |
| **GPT-4 + Rationale (0 ex.)** | CoT, no examples | ~0.70 | Cải thiện lớn khi zero-shot | Sec 3.2, Fig 4 |

**Fairness by L1 (GPT-4, Fig 5 — sau importance sampling):**

| L1 | QWK (GPT-4 vs Human) |
|---|---|
| Spanish (spa) | **0.89** (cao nhất) |
| Arabic (ara) | ~0.84 |
| English (eng) | ~0.83 |
| Gujarati (guj) | ~0.80 |
| Mandarin (cmn) | ~0.76 |
| Telugu (tel) | **0.66** (thấp nhất) |
| Bengali (ben) | ~0.72 |

- **Diễn giải số liệu:**
  - GPT-4 chỉ cần **1 calibration example per category** (8 ví dụ tổng) là đạt gần tối ưu (~0.81 QWK). Thêm ví dụ không cải thiện đáng kể → **diminishing returns**.
  - Prompt engineering (detailed rubric, CoT rationale) **chỉ hữu ích khi zero-shot**; khi đã có calibration examples thì negligible.
  - GPT-3.5 kém hơn GPT-4 rất nhiều, gợi ý rằng khả năng chấm điểm phụ thuộc mạnh vào kích thước/chất lượng mô hình.
  - **Bias theo L1 tồn tại**: Telugu, Bengali, Mandarin có QWK thấp hơn đáng kể so với Spanish. Tác giả chưa xác định nguyên nhân (do GPT-4 hay do human raters thiếu nhất quán cho các L1 này).
  - **⚠️ Cảnh báo:** QWK 0.81 của GPT-4 là trên **bài viết ngắn (5 phút)**, thang 8 mức CEFR, với calibration — KHÔNG nên suy rộng trực tiếp sang bài nghị luận dài trên PERSUADE.


---


## 4. HẠN CHẾ & RANH GIỚI (LIMITATIONS & PITFALLS)

- **Hạn chế do chính tác giả thừa nhận:**
  - Dataset thuộc Duolingo (proprietary), không công khai → **không thể reproduce**.
  - Số lượng double-rated essays không đủ để phân tích reliability per L1.
  - Chưa thử fine-tuning GPT-3.5 (chỉ prompt engineering).
  - Bài viết **rất ngắn** (5 phút, ~100–200 từ) → khác biệt bản chất so với bài nghị luận dài (500–1000+ từ).

- **Ranh giới khi áp dụng vào dự án của nhóm:**
  - **Bài toán khác nhau hoàn toàn:** Paper chấm holistic trên thang CEFR (trình độ ngôn ngữ); nhóm chấm **discourse effectiveness** (chất lượng lập luận) cho từng discourse element → mức độ chi tiết (granularity) khác xa.
  - Paper dùng **bài viết ngắn L2 learners** vs nhóm dùng **bài nghị luận học sinh lớp 6–12 bản ngữ** → đối tượng khác, thang đo khác, rubric khác.
  - GPT-4 API **tốn chi phí cao** và không reproducible (model version thay đổi) → không phù hợp cho sản phẩm human-in-the-loop cần minh bạch.
  - Paper **không đo Recall per class** hay **Macro-F1** → không biết mô hình xử lý lớp thiểu số (A1, C2) tốt hay kém.
  - Paper **không cung cấp rationale/feedback sư phạm** cho giáo viên → chỉ phân loại mức, không giải thích tại sao.
  - **Rủi ro thiên lệch L1:** Nếu áp dụng cho học sinh đa dạng sắc tộc/ngôn ngữ tại Mỹ (PERSUADE), bias tương tự có thể xuất hiện.


---


## 5. ĐIỂM KẾ THỪA CHO DỰ ÁN NHÓM (ACTIONABLE TAKEAWAYS)

- **Điểm NÊN kế thừa vào MVP:**
  - ✅ **QWK là metric phù hợp** cho bài toán chấm điểm thứ bậc — nhóm cũng dùng QWK, xác nhận tính hợp lệ.
  - ✅ **Calibration examples rất quan trọng:** Chỉ cần 1 ví dụ/mức là GPT-4 cải thiện vọt → nếu nhóm thử LLM (future work), nên dùng few-shot với ví dụ chuẩn từ PERSUADE.
  - ✅ **Luôn đo fairness theo subgroup:** Khi report kết quả, nên phân tích QWK/F1 theo nhóm học sinh (nếu có metadata demographic).
  - ✅ **Feature-engineered AWE (XGBoost + 85 features)** vẫn rất mạnh (0.84 QWK) → xác nhận chiến lược bắt đầu từ Classical ML của nhóm là hợp lý.

- **Điểm KHÔNG NÊN làm theo (Bẫy cần tránh):**
  - ❌ Không nên nghĩ rằng "GPT-4 đạt 0.81 QWK" nghĩa là LLM có thể chấm discourse effectiveness tốt — bài toán của nhóm khó hơn nhiều (3 mức x 7 loại discourse element, mất cân bằng nhãn).
  - ❌ Không nên bê nguyên rubric CEFR vào prompt cho PERSUADE — thang đo hoàn toàn khác.
  - ❌ Không nên bỏ qua bias analysis chỉ vì "GPT-4 có vẻ fair" ở trung bình — paper đã chỉ ra bias rõ ràng theo L1.

- **Đề xuất thí nghiệm đối chứng:**
  - **Ablation:** So sánh TF-IDF + Logistic Regression (baseline nhóm) vs. "chỉ dùng essay length" trên PERSUADE → kiểm tra essay length có phải strong predictor cho effectiveness không (tương tự Length-Only baseline trong paper đạt ~0.60 QWK).


---


## 6. ĐÓNG GÓI CHO SLIDE THUYẾT TRÌNH & PHẢN BIỆN (DEFENSE PREP)

- **3–4 Bullet points đắt giá đưa lên Slide Related Work:**
  - *Bullet 1:* Yancey et al. (2023) đánh giá GPT-3.5 và GPT-4 chấm bài viết ngắn L2 trên thang CEFR (8 mức), sử dụng zero-shot và few-shot prompting.
  - *Bullet 2:* GPT-4 đạt QWK = 0.81 (vs. human) khi được cung cấp calibration examples, tiệm cận AWE baseline (XGBoost, 85 features, QWK = 0.84), nhưng vẫn kém human-human agreement (0.87) — trích Table/Fig 2.
  - *Bullet 3:* Tuy nhiên, GPT-4 cho thấy **bias theo L1** (QWK cho Telugu chỉ 0.66 so với Spanish 0.89 — Fig 5), đặt ra câu hỏi về fairness khi triển khai thực tế.
  - *Bullet 4:* Nhóm kế thừa: xác nhận QWK là metric phù hợp; xác nhận Classical ML + feature engineering vẫn competitive; lưu ý cần phân tích bias theo subgroup.

- **Lời thoại thuyết trình gợi ý (45–60 giây):**
  > *"Yancey và cộng sự năm 2023 tại workshop BEA đã đánh giá khả năng của GPT-4 trong việc chấm bài viết ngắn cho người học tiếng Anh trên thang CEFR. Kết quả cho thấy GPT-4 với few-shot prompting đạt QWK 0.81, khá gần với hệ thống AWE truyền thống dùng XGBoost và 85 đặc trưng ngôn ngữ ở mức 0.84. Tuy nhiên, hai điểm đáng lưu ý: thứ nhất, GPT-4 có bias rõ ràng theo ngôn ngữ mẹ đẻ — QWK cho người nói tiếng Telugu chỉ 0.66 so với 0.89 cho tiếng Tây Ban Nha. Thứ hai, bài toán của họ là chấm holistic trên bài viết ngắn 5 phút, rất khác với bài toán discourse effectiveness prediction trên PERSUADE của nhóm chúng tôi, nơi chúng tôi cần đánh giá chất lượng từng thành phần lập luận. Bài báo này xác nhận cho chúng tôi rằng QWK là metric phù hợp, và Classical ML với feature engineering vẫn là baseline mạnh cần vượt qua."*

- **Bộ câu hỏi phản biện & Gợi ý trả lời:**
  - *Câu hỏi 1:* "Paper này chấm holistic CEFR, bài toán nhóm là discourse effectiveness — liên quan gì?"
    - 👉 **Trả lời:** Paper này nằm trong Related Work về *LLM-based essay evaluation* để cho thấy landscape hiện tại: ngay cả LLM mạnh nhất (GPT-4) vẫn chưa vượt qua feature-engineered baselines trong AES. Điều này xác nhận chiến lược của nhóm bắt đầu từ Classical ML thay vì vội dùng LLM. Đồng thời, metric QWK mà paper sử dụng cũng là một trong các metric nhóm áp dụng.
  - *Câu hỏi 2:* "QWK 0.81 trông khá tốt, tại sao nhóm không dùng GPT-4 luôn?"
    - 👉 **Trả lời:** QWK 0.81 là trên bài viết ngắn (5 phút, ~150 từ) với 8 mức phân loại rõ ràng theo CEFR. Bài toán PERSUADE phức tạp hơn: phân loại 3 mức effectiveness cho từng discourse element riêng biệt, với class imbalance mạnh (Ineffective thiểu số). Hơn nữa, GPT-4 API không minh bạch, tốn chi phí, và không reproducible — không phù hợp cho sản phẩm human-in-the-loop cần giáo viên kiểm soát.
  - *Câu hỏi 3:* "Paper cho thấy bias theo L1, nhóm xử lý vấn đề fairness thế nào?"
    - 👉 **Trả lời:** Đây chính là lý do nhóm chọn triết lý Human-in-the-loop: mô hình chỉ *gợi ý* và *ưu tiên*, giáo viên giữ quyền quyết định cuối cùng. Trong PERSUADE, metadata demographic hạn chế, nhưng nhóm sẽ phân tích performance breakdown theo discourse type và prompt topic để phát hiện bias tiềm ẩn.


================================================================================

# [Mã Paper: R02] — Can Large Language Models Automatically Score Proficiency of Written Essays?


## 1. METADATA & TRÍCH DẪN CHUẨN APA 7
- **Tác giả:** Watheq Ahmad Mansour, Salam Albatarni, Sohaila Eltanbouly, Tamer Elsayed
- **Đơn vị:** The University of Queensland (Mansour); Qatar University (còn lại)
- **Năm xuất bản / Hội nghị:** 2024, LREC-COLING 2024 (Joint International Conference on Computational Linguistics, Language Resources and Evaluation), Torino, Italia
- **Trích dẫn APA 7 chuẩn:**
  > Mansour, W. A., Albatarni, S., Eltanbouly, S., & Elsayed, T. (2024). Can large language models automatically score proficiency of written essays? In *Proceedings of the 2024 Joint International Conference on Computational Linguistics, Language Resources and Evaluation (LREC-COLING 2024)* (pp. 2777–2786). ELRA and ICCL. https://aclanthology.org/2024.lrec-main.247/
- **Đường dẫn & Tài nguyên:**
  - ACL Anthology: https://aclanthology.org/2024.lrec-main.247/
  - DOI: Paper không đề cập DOI cụ thể trên ACL Anthology.
  - **GitHub (public):** https://github.com/Watheq9/AES-with-LLMs — chứa responses + feedback của LLMs.
- **Lưu ý phiên bản:** Bản proceedings chính thức tại LREC-COLING 2024.


---


## 2. BÀI TOÁN & THIẾT LẬP THỰC NGHIỆM (PROBLEM & SETUP)

- **Câu hỏi nghiên cứu chính:**
  1. (RQ1) Prompt engineering ảnh hưởng như thế nào đến hiệu suất LLM cho AES?
  2. (RQ2) LLMs có nhất quán (consistent) khi chấm cùng bài với các prompt khác nhau không?
  3. (RQ3) Hiệu suất của ChatGPT và Llama 2 so với SOTA ở mức holistic và trait-based ra sao?

- **Nhiệm vụ ML & Phạm vi:**
  - **Holistic Essay Scoring:** Dự đoán điểm tổng thể cho mỗi bài viết.
  - **Trait-based Scoring:** Chấm điểm theo từng trait riêng biệt (Content, Organization, Voice, Word Choice, Sentence Fluency, Conventions, Style) — chỉ khả dụng cho Tasks 7 & 8 trong ASAP.
  - **Zero-shot prompting** — KHÔNG fine-tune, KHÔNG training trên ASAP. Dùng incremental prompt engineering (4 prompt variants).

- **Dữ liệu thực nghiệm:**
  - **Dataset:** ASAP (Automated Student Assessment Prize) — Kaggle 2012.
  - **Kích thước:** 12,978 bài viết, 8 tasks, từ lớp 7–10 (Mỹ).
  - **3 loại task:** Persuasive, Source-Dependent Response, Narrative.
  - **Score ranges:** Khác nhau theo task (2–12, 1–6, 0–3, 0–4, 0–30, 0–60).
  - **⚠️ KHÔNG phải PERSUADE/Feedback Prize** — ASAP là holistic scoring, không có discourse element labels.
  - **Human inter-rater agreement trung bình:** QWK ~0.75 trên ASAP.

- **Thiết lập Input/Output:**
  - *Input:* Task prompt + essay + (optional) rubric + (optional) one-shot example.
  - *Output:* Holistic score (trong score range tương ứng) + commentary/feedback.
  - *Điều kiện ranh giới:* Không áp dụng — toàn bài được chấm.

- **Các họ mô hình được khảo sát:**
  1. **ChatGPT** (`gpt-3.5-turbo-0301`) — proprietary, temperature=0.
  2. **Llama 2** (`Llama-2-13b-chat-hf`) — open-source, 13B parameters, temperature=0.
  3. **SOTA Baselines (Holistic):** Xie et al. (2022) — pairwise contrastive regression; Jiang et al. (2023) — domain generalization.
  4. **SOTA Baseline (Traits):** Mathias & Bhattacharyya (2020) — neural network trait scoring (BEA 2020).


---


## 3. KẾT QUẢ ĐỊNH LƯỢNG CỐT LÕI (KEY FINDINGS & NUMBERS)

### 3a. Phase 1 — Prompt Engineering (Table 2)

| LLM | Task (Category) | Prompt A | Prompt B (+rubric) | Prompt C (+rubric+1-shot) | Prompt D (+chat format) | Best |
|---|---|---|---|---|---|---|
| ChatGPT | Task 1 (Persuasive) | 0.057 | 0.080 | **0.120** | 0.113 | C |
| ChatGPT | Task 5 (Source-Dep.) | 0.552 | **0.576** | 0.476 | 0.455 | B |
| ChatGPT | Task 7 (Narrative) | 0.060 | 0.027 | 0.055 | **0.123** | D |
| Llama 2 | Task 1 (Persuasive) | **0.331** | 0.092 | 0.154 | 0.170 | A |
| Llama 2 | Task 5 (Source-Dep.) | 0.047 | 0.346 | **0.418** | 0.180 | C |
| Llama 2 | Task 7 (Narrative) | 0.268 | **0.359** | 0.037 | 0.224 | B |

### 3b. Full ASAP — LLMs vs. SOTA (Table 4)

| Task | Xie et al. (2022) SOTA | Jiang et al. (2023) Cross-Prompt | ChatGPT (best prompt) | Llama 2 (best prompt) |
|---|---|---|---|---|
| 1 (Persuasive) | 0.856 | 0.762 | 0.120 | 0.331 |
| 2 (Persuasive) | 0.750 | 0.686 | 0.193 | **0.562** |
| 3 (Source-Dep.) | 0.756 | 0.637 | 0.198 | −0.059 |
| 4 (Source-Dep.) | 0.851 | 0.673 | 0.416 | 0.201 |
| 5 (Source-Dep.) | 0.847 | 0.778 | **0.576** | 0.418 |
| 6 (Source-Dep.) | 0.858 | 0.664 | **0.606** | 0.363 |
| 7 (Narrative) | 0.838 | 0.742 | 0.123 | 0.359 |
| 8 (Narrative) | 0.779 | 0.677 | 0.276 | 0.201 |
| **Average** | **0.817** | **0.702** | **0.313** | **0.297** |

### 3c. Trait-level Performance (Table 5, Tasks 7 & 8)

| Task | Model | Content | Organization | Voice | Word Choice | Sentence Fluency | Conventions | Style |
|---|---|---|---|---|---|---|---|---|
| 7 | BEA 2020 SOTA | 0.771 | 0.676 | — | — | — | 0.621 | 0.659 |
| 7 | ChatGPT | 0.045 | 0.068 | — | — | — | 0.097 | 0.079 |
| 7 | Llama 2 | 0.091 | 0.023 | — | — | — | 0.327 | 0.154 |
| 8 | BEA 2020 SOTA | 0.586 | 0.632 | 0.544 | 0.559 | 0.586 | 0.558 | — |
| 8 | ChatGPT | 0.185 | 0.256 | 0.155 | 0.150 | 0.203 | 0.311 | — |
| 8 | Llama 2 | 0.276 | 0.271 | 0.278 | 0.268 | 0.121 | 0.089 | — |

### 3d. Consistency Across Prompts (Table 3 — QWK giữa các cặp prompt)

| Task | LLM | Avg QWK across prompt pairs |
|---|---|---|
| 1 | ChatGPT | **0.62** |
| 1 | Llama 2 | 0.43 |
| 5 | ChatGPT | **0.58** |
| 5 | Llama 2 | 0.20 |
| 7 | ChatGPT | **0.64** |
| 7 | Llama 2 | 0.17 |

- **Diễn giải số liệu:**
  - **LLMs kém xa SOTA:** Average QWK 0.313 (ChatGPT) và 0.297 (Llama 2) vs. 0.817 (SOTA in-prompt). Khoảng cách **~0.5 QWK** — rất lớn.
  - **ChatGPT ≈ Llama 2** ở mức trung bình, nhưng ChatGPT **nhất quán hơn** (avg inter-prompt QWK 0.58–0.64 vs 0.17–0.43 cho Llama).
  - **Prompt choice matters enormously:** Best prompt khác nhau tùy task category VÀ tùy model. Không có "prompt universal" cho AES.
  - **Trait-level QWK cực thấp** (dưới 0.33 hầu hết) → LLMs gần như **không có khả năng** đánh giá traits riêng lẻ khi zero-shot.
  - **Source-dependent tasks dễ hơn** cho ChatGPT (QWK 0.4–0.6) vì task "tự chứa" — ngữ cảnh nằm trong rubric + source text.
  - **Llama 2 đạt QWK âm** (−0.059 cho Task 3) → chấm ngược chiều với human, tệ hơn random.


---


## 4. HẠN CHẾ & RANH GIỚI (LIMITATIONS & PITFALLS)

- **Hạn chế do chính tác giả thừa nhận (Section 5):**
  - Prompt bị giới hạn 4,096 tokens → không thể đưa nhiều examples hay rubric dài.
  - Chỉ dùng **one-shot** (1 ví dụ), chưa thử few-shot đầy đủ.
  - Chỉ thử 2 LLMs (ChatGPT và Llama 2); chưa thử GPT-4, Bard, hay models mới hơn.
  - Chưa fine-tune LLMs trên ASAP → chưa khai thác hết tiềm năng.
  - Chưa đánh giá chất lượng feedback sinh ra một cách hệ thống (chỉ show 2 ví dụ minh họa).

- **Ranh giới khi áp dụng vào dự án của nhóm:**
  - Paper chấm **holistic score** cho toàn bài vs nhóm chấm **discourse element effectiveness** → mức granularity khác xa.
  - ASAP dataset (lớp 7–10, Mỹ) khá gần PERSUADE về đối tượng, nhưng **thang đo hoàn toàn khác** (0–60 holistic vs 3-class effectiveness).
  - Kết quả trait-level cực kém (QWK < 0.33) là **tín hiệu cảnh báo mạnh**: nếu LLMs không thể đánh giá traits cơ bản (Content, Organization) khi zero-shot, thì càng khó đánh giá discourse effectiveness (Ineffective/Adequate/Effective) — một nhiệm vụ tinh tế hơn.
  - Paper không đo **Recall per class, Macro-F1, hay confusion matrix** → không biết LLMs xử lý extreme scores thế nào.
  - Paper dùng **gpt-3.5-turbo** (snapshot March 2023) — version cũ; kết quả có thể khác với GPT-4 hoặc phiên bản mới hơn.


---


## 5. ĐIỂM KẾ THỪA CHO DỰ ÁN NHÓM (ACTIONABLE TAKEAWAYS)

- **Điểm NÊN kế thừa vào MVP:**
  - ✅ **Xác nhận rằng LLMs zero-shot KHÔNG đủ tốt cho AES cấp production** (avg QWK ~0.3) → nhóm đúng khi bắt đầu từ Classical ML.
  - ✅ **Prompt engineering có ảnh hưởng lớn nhưng KHÔNG nhất quán** → nếu nhóm dùng LLM (future work), cần thử nhiều prompt variants và pick theo task type.
  - ✅ **ASAP inter-rater agreement ~0.75** → tương tự mức difficulty expected trong PERSUADE; dùng làm reference khi đặt target QWK cho nhóm.
  - ✅ **Feedback generation là điểm sáng duy nhất của LLMs** → nhóm có thể explore LLMs cho mục đích **sinh lời giải thích** (không phải dự đoán nhãn) trong future work.
  - ✅ **GitHub repo công khai** (https://github.com/Watheq9/AES-with-LLMs) → tham khảo prompt design cho baseline LLM.

- **Điểm KHÔNG NÊN làm theo (Bẫy cần tránh):**
  - ❌ Không nên kết luận "LLM không dùng được cho AES" — paper chỉ test zero-shot/one-shot; fine-tuning có thể cải thiện đáng kể (xem Paper R03).
  - ❌ Không nên dùng Llama-2-13B cho AES trực tiếp — quá nhạy cảm với prompt (QWK thay đổi từ −0.059 đến 0.562 chỉ do đổi prompt).
  - ❌ Không nên extrapolate kết quả ASAP sang PERSUADE — scoring scales, rubrics, và discourse types khác biệt căn bản.

- **Đề xuất thí nghiệm đối chứng:**
  - **Experiment:** Dùng GPT-3.5/4 (zero-shot, best prompt từ paper) để chấm ~100 discourse elements từ PERSUADE test set, so sánh QWK với Classical ML baseline của nhóm → **benchmark LLM zero-shot trực tiếp trên task của nhóm**, thay vì ngoại suy từ ASAP.


---


## 6. ĐÓNG GÓI CHO SLIDE THUYẾT TRÌNH & PHẢN BIỆN (DEFENSE PREP)

- **3–4 Bullet points đắt giá đưa lên Slide Related Work:**
  - *Bullet 1:* Mansour et al. (2024) đánh giá ChatGPT (GPT-3.5) và Llama 2 (13B) trên toàn bộ ASAP dataset (12,978 bài, 8 tasks) với 4 chiến lược prompt engineering tăng dần, **KHÔNG fine-tune**.
  - *Bullet 2:* Kết quả: LLMs đạt QWK trung bình chỉ **0.313 (ChatGPT)** và **0.297 (Llama 2)**, kém rất xa SOTA in-prompt (0.817) — trích Table 4. Trait-level QWK còn thấp hơn (< 0.33) — Table 5.
  - *Bullet 3:* Prompt choice ảnh hưởng lớn đến kết quả và **khác nhau tùy model + task type**; Llama 2 đặc biệt kém nhất quán (avg inter-prompt QWK chỉ 0.17–0.43 vs ChatGPT 0.58–0.64) — Table 3.
  - *Bullet 4:* Nhóm kế thừa: xác nhận LLMs zero-shot **chưa phù hợp** cho AES production; bắt đầu từ Classical ML là hợp lý. LLM có tiềm năng cho **feedback generation** — hướng future work.

- **Lời thoại thuyết trình gợi ý (45–60 giây):**
  > *"Mansour và cộng sự năm 2024 tại LREC-COLING đã kiểm tra khả năng chấm bài viết của ChatGPT và Llama 2 trên benchmark ASAP nổi tiếng với hơn 12,000 bài viết. Họ thiết kế 4 prompt tăng dần từ đơn giản đến có rubric và one-shot example. Kết quả cho thấy cả hai LLMs đều kém rất xa SOTA — QWK trung bình chỉ khoảng 0.3 so với 0.82 của mô hình supervised. Đặc biệt, Llama 2 rất nhạy cảm với cách viết prompt — có task đạt QWK âm, tức chấm ngược chiều với con người. Ở cấp trait, các LLMs gần như không phân biệt được chất lượng cụ thể. Phát hiện này củng cố quyết định của nhóm chúng tôi bắt đầu từ Classical ML thay vì LLM zero-shot, vì bài toán discourse effectiveness prediction còn tinh tế hơn holistic scoring mà LLMs đã thất bại."*

- **Bộ câu hỏi phản biện & Gợi ý trả lời:**
  - *Câu hỏi 1:* "Paper dùng GPT-3.5 và Llama 2 — đã có GPT-4 tốt hơn, sao nhóm vẫn cite?"
    - 👉 **Trả lời:** Paper R01 (Yancey et al.) đã test GPT-4 và cho kết quả tốt hơn nhưng vẫn kém AWE baseline. Paper này quan trọng vì: (a) test trên **ASAP** — benchmark chuẩn gần PERSUADE nhất về đối tượng học sinh; (b) là paper duy nhất so sánh **cả proprietary lẫn open-source LLM** trên ASAP; (c) cho thấy **trait-level scoring** (gần với task của nhóm) cực kém dù ở mức holistic, LLMs đã yếu.
  - *Câu hỏi 2:* "Tại sao nhóm không fine-tune LLM như trong Paper R03?"
    - 👉 **Trả lời:** Đó chính là lộ trình phát triển của nhóm: MVP bắt đầu từ Classical ML (interpretable, không cần GPU), sau đó khi validated concept, mở rộng sang fine-tuned LLM nhỏ (future work). Paper này (R02) cho thấy rõ rằng zero-shot LLM **không đủ** — cần fine-tuning hoặc ít nhất supervised approach.
  - *Câu hỏi 3:* "QWK ~0.3 quá thấp — có đáng để nhắc đến không?"
    - 👉 **Trả lời:** Chính vì thấp nên mới đáng nhắc — nó là **negative result cực kỳ quan trọng** giúp nhóm justify tại sao không chạy theo trend LLM zero-shot. Trong nghiên cứu khoa học, negative results (cái KHÔNG hoạt động) cũng có giá trị tương đương positive results.


================================================================================

# [Mã Paper: R03] — Human-AI Collaborative Essay Scoring: A Dual-Process Framework with LLMs


## 1. METADATA & TRÍCH DẪN CHUẨN APA 7
- **Tác giả:** Changrong Xiao, Wenxing Ma, Qingping Song, Sean Xin Xu, Kunpeng Zhang, Yufang Wang, Qi Fu
- **Đơn vị:** Tsinghua University, City University of Hong Kong, University of Maryland
- **Năm / Venue:** 2024 (preprint arXiv tháng 1/2024, v2); published tại ACM conference — DOI: `10.1145/3706468.3706507`
- **Trích dẫn APA 7 chuẩn:**
  > Xiao, C., Ma, W., Song, Q., Xu, S. X., Zhang, K., Wang, Y., & Fu, Q. (2024). Human-AI collaborative essay scoring: A dual-process framework with LLMs. *arXiv preprint arXiv:2401.06431v2*. https://doi.org/10.1145/3706468.3706507
- **Đường dẫn & Tài nguyên:**
  - arXiv: https://arxiv.org/abs/2401.06431
  - DOI (ACM): https://doi.org/10.1145/3706468.3706507
  - **GitHub (public):** https://github.com/Xiaochr/LLM-AES — code + CSEE dataset
- **Lưu ý phiên bản:** Bản v2 trên arXiv (có cập nhật so với v1); đã được chấp nhận tại hội nghị ACM. Paper toàn diện nhất trong 3 papers, bao gồm cả thực nghiệm Human-AI co-grading.


---


## 2. BÀI TOÁN & THIẾT LẬP THỰC NGHIỆM (PROBLEM & SETUP)

- **Câu hỏi nghiên cứu chính:**
  1. LLMs (GPT-3.5, GPT-4, LLaMA3-8B) có thể đạt được mức chấm điểm nào khi prompting, fine-tuning, và tích hợp kiến trúc dual-process?
  2. Hệ thống AES có thể hỗ trợ human graders (cả novice và expert) đạt complementary performance không?
  3. Prediction confidence và explanation generation đóng vai trò gì trong human-AI collaboration?

- **Nhiệm vụ ML & Phạm vi:**
  - **Holistic Essay Scoring** trên ASAP (8 subsets) và **Multi-dimensional Scoring** trên CSEE (Content, Language, Structure, Overall).
  - **Pipeline đầy đủ:** Zero-shot → Few-shot → Fine-tuning (SFT) → **Dual-Process Framework (Fast & Slow Thinking)** → Human-AI Co-Grading.
  - **Quan trọng:** Đây là paper duy nhất trong 3 papers **thực hiện fine-tuning LLM** và **thực nghiệm human-AI collaboration**.

- **Dữ liệu thực nghiệm:**
  - **ASAP:** 12,978 bài viết, 8 prompts/subsets, score ranges khác nhau. Train/test split: 80:20.
  - **CSEE (Chinese Student English Essay):** 13,372 bài viết tiếng Anh từ 29 trường THPT Trung Quốc, 2 prompts, chấm theo 3 chiều (Content, Language, Structure) + Overall (0–20). Do giáo viên kinh nghiệm chấm.
  - **⚠️ KHÔNG phải PERSUADE/Feedback Prize** — cả hai datasets đều là holistic/multi-dimensional scoring, không có discourse elements.

- **Thiết lập Input/Output:**
  - *Input:* Task prompt + essay + scoring rubric + (optional) few-shot examples.
  - *Output:* Score + (cho Slow Module) natural language explanation/feedback.
  - *Điều kiện ranh giới:* Không áp dụng.

- **Các họ mô hình được khảo sát:**
  1. **BERT Classifier** (bert-base-uncased + FC layer, fine-tuned) — traditional baseline
  2. **R2BERT** (Yang et al., 2020) — SOTA on ASAP (regression + ranking)
  3. **Tran-BERT-MS-ML-R** (Wang et al., 2022) — SOTA on ASAP (multi-scale)
  4. **GPT-4 zero-shot** (without rubrics)
  5. **GPT-4 zero-shot** (with rubrics)
  6. **GPT-4 few-shot** (with rubrics, k=3 retrieval-based examples)
  7. **Fine-tuned GPT-3.5** (gpt-3.5-turbo, SFT with explanation-augmented data)
  8. **Fine-tuned LLaMA3-8B** (LoRA, rank=16, alpha=16)
  9. **Fast & Slow Thinking Framework** (LLaMA3-8B as Slow Module + FC classifier as Fast Module, confidence-triggered switching)


---


## 3. KẾT QUẢ ĐỊNH LƯỢNG CỐT LÕI (KEY FINDINGS & NUMBERS)

### 3a. Performance on ASAP — QWK (Table 1 trong paper)

| Method | Set 1 | Set 2 | Set 3 | Set 4 | Set 5 | Set 6 | Set 7 | Set 8 | Avg |
|---|---|---|---|---|---|---|---|---|---|
| **R2BERT (SOTA)** | Paper không đề cập | — | — | — | — | — | — | — | **>0.80** (high) |
| **BERT Classifier** | — | — | — | — | — | — | — | — | ~0.72 |
| **GPT-4 zero-shot (no rubrics)** | 0.0423 | — | — | — | — | — | 0.0809 | — | Very low |
| **GPT-4 zero-shot (w/ rubrics)** | — | — | — | — | — | — | — | — | Low |
| **GPT-4 few-shot (w/ rubrics)** | — | — | — | Improved for Sets 4-6 | — | — | — | — | Still << SOTA |
| **Fine-tuned GPT-3.5** | — | — | — | — | — | — | — | — | QWK > 0.7 general |
| **Fine-tuned LLaMA3-8B (SFT)** | — | — | — | — | — | — | — | — | ≈ Fine-tuned GPT-3.5 |
| **LLaMA3 Slow Module only** | — | — | — | — | — | — | — | — | Slight drop vs SFT |
| **Fast & Slow Framework** | — | — | — | — | — | — | — | — | **Improved vs Slow only** |

> **Lưu ý quan trọng:** Paper trình bày kết quả chi tiết trong Table 1 nhưng toàn văn HTML không render đầy đủ bảng số. Các con số cụ thể trích xuất từ phần narrative:

**Key quantitative claims (trích nguyên văn từ Section 5.1):**
- GPT-4 zero-shot: Set 1 QWK = **0.0423**, Set 7 QWK = **0.0809** → "nearly as poorly as random guessing"
- GPT-4 few-shot: "improvement particularly for Sets 4-6" nhưng "significantly lagged behind SOTA"
- Fine-tuned LLMs: "QWK scores generally exceeding **0.7**" nhưng "still did not surpass traditional SOTA methods"
- Fine-tuned LLaMA3-8B: "**comparable to** that of fine-tuned proprietary models" (GPT-3.5)
- Explanation quality: vs GPT-4 generated explanations → win rate **35%**, tie **40%**, loss **25%** (qua crowdsourced comparison)

### 3b. CSEE Dataset Results (Table 2)
- Framework dự đoán reliable scores trên cả 3 chiều: Content, Language, Structure.
- Paper không đề cập con số QWK cụ thể trong phần narrative truy cập được.

### 3c. Human-AI Co-Grading Experiment (Table 3, Figure 4)
- **50 essays** từ CSEE test set, 10 novice evaluators + 5 expert evaluators.

| Condition | Average QWK |
|---|---|
| **Novice evaluators (no AI)** | **0.5256** |
| **Novice + LLM feedback** | **0.6609** (p < 0.01) |
| **Expert evaluators (no AI)** | **0.7117** |
| **Expert + LLM feedback** | **0.7734** (p = 0.13, not significant) |
| **AES system alone (on these 50 essays)** | **0.7302** |

- **⚠️ Critical finding:** LLM-assisted novice (0.6609) vs Expert alone (0.7117): **p-value = 0.27 → không có khác biệt thống kê** → novice + AI ≈ expert alone!
- Expert + AI (0.7734) > AES alone (0.7302) → **complementary performance achieved** (human-AI team > either alone).
- Experts reported: **less time needed**, **higher consensus** (lower std), appreciated **prediction confidence mechanism**.

### 3d. Prediction Confidence Analysis
- **>80% ratings unchanged** across 3 runs (temperature=0) → high consistency.
- Low-confidence threshold: < 0.2.
- For low-confidence essays: Expert QWK = 0.6809, Novice QWK = 0.5680, LLM Slow Module = 0.5478 → **humans outperform LLM on difficult cases**.
- "The model manages routine cases with high confidence and minimal human intervention, while low-confidence cases are presented to human collaborators."

### 3e. Generalizability (Table 7 — Cross-subset)
- Fine-tuned GPT-3.5 **generally outperforms** BERT classifier in cross-subset generalization.
- BERT classifier: "particularly weak generalization when trained on Sets 7 and 8, performing close to random guessing."

- **Diễn giải tổng hợp:**
  - **Zero-shot/few-shot LLMs thất bại cho AES** (consistent với Papers R01, R02), nhưng **fine-tuning cải thiện vọt** (QWK > 0.7).
  - Fine-tuned open-source LLaMA3-8B ≈ fine-tuned proprietary GPT-3.5 → **open-source viable**.
  - **Dual-process framework** (Fast + Slow) tốt hơn Slow module đơn lẻ nhờ tách biệt score prediction (numerical) và explanation generation (textual).
  - **Human-AI collaboration là breakthrough thực sự:** novice + AI = expert; expert + AI > expert alone AND > AI alone.
  - **Prediction confidence là key design element** cho human-in-the-loop systems.


---


## 4. HẠN CHẾ & RANH GIỚI (LIMITATIONS & PITFALLS)

- **Hạn chế do chính tác giả thừa nhận (Section "Limitations"):**
  - CSEE dataset chỉ gồm 2 đề thi cuối kỳ → **chưa đa dạng về chủ đề và đối tượng**.
  - Human-AI co-grading experiment là **pilot study** với mẫu nhỏ (50 essays, 15 evaluators) → "yields general results."
  - Chưa hiểu rõ cơ chế: khi nào con người nhận ra và sửa lỗi sau khi nhận feedback AI, vs khi nào AI feedback gây nhiễu (mislead).
  - Data annotation process details (số giáo viên chấm, inter-annotator agreement) **không được công bố**.

- **Ranh giới khi áp dụng vào dự án của nhóm:**
  - Paper chấm **holistic + multi-dimensional** (Content, Language, Structure) vs nhóm chấm **discourse effectiveness** (Ineffective, Adequate, Effective) cho từng discourse element → **mức granularity và taxonomy khác nhau**.
  - Fine-tuning LLaMA3-8B yêu cầu **RTX 4090 24GB GPU, ~3 tuần** → **không khả thi cho MVP của nhóm** (nhóm dùng Classical ML trước).
  - Human-AI co-grading experiment dùng **giáo viên Trung Quốc chấm bài tiếng Anh** → có thể bias văn hóa; nhóm áp dụng cho giáo viên Mỹ chấm bài học sinh Mỹ → transferability chưa rõ.
  - Paper **không đo class-level metrics** (Recall per class, Macro-F1) → không biết framework xử lý class imbalance thế nào.
  - Dual-process framework **yêu cầu LLM fine-tuned** → không áp dụng được cho Classical ML pipeline của nhóm.


---


## 5. ĐIỂM KẾ THỪA CHO DỰ ÁN NHÓM (ACTIONABLE TAKEAWAYS)

- **Điểm NÊN kế thừa vào MVP:**
  - ✅ **Triết lý Human-in-the-loop hoàn toàn trùng khớp:** Paper chứng minh empirically rằng human-AI team > human alone AND > AI alone → **xác nhận triết lý sản phẩm của nhóm**.
  - ✅ **Prediction confidence là feature thiết kế quan trọng:** Nhóm nên output confidence score cùng với prediction → cho phép giáo viên ưu tiên review bài có confidence thấp. Ngay cả Logistic Regression cũng có predict_proba().
  - ✅ **"Novice + AI = Expert" → giá trị sư phạm lớn:** Nhóm có thể argue rằng công cụ giúp giáo viên mới/chưa kinh nghiệm đạt chất lượng đánh giá gần expert.
  - ✅ **Open-source LLM ≈ proprietary:** Nếu nhóm mở rộng sang fine-tuned LLM, không nhất thiết phải dùng GPT-4 API — LLaMA3-8B đủ tốt.
  - ✅ **GroupKFold theo essay:** Paper dùng 80:20 split — nhóm nên dùng GroupKFold theo essay_id/student_id để tránh data leakage.
  - ✅ **Explanation-augmented training data:** Ý tưởng dùng GPT-4 sinh explanation, rồi train mô hình nhỏ hơn trên data augmented → nhóm có thể áp dụng cho future work.

- **Điểm KHÔNG NÊN làm theo (Bẫy cần tránh):**
  - ❌ Không nên vội fine-tune LLaMA3-8B khi nhóm chưa establish Classical ML baseline — paper cho thấy ngay cả BERT classifier (supervised) đã đạt ~0.72 QWK.
  - ❌ Không nên bê nguyên framework Fast/Slow vào MVP — yêu cầu GPU, training pipeline phức tạp, không phù hợp cho interpretable ML phase.
  - ❌ Không nên quảng bá "LLM đạt QWK > 0.7" mà không nói rõ đó là **fine-tuned** trên training data — khác xa zero-shot.
  - ❌ Không nên coi kết quả human-AI co-grading (n=50, 15 evaluators) là definitive — đó là pilot study.

- **Đề xuất thí nghiệm đối chứng:**
  - **Experiment:** Implement confidence-based flagging trong Classical ML pipeline của nhóm: (1) train TF-IDF + Logistic Regression; (2) output predict_proba → flag discourse elements có max_proba < 0.6 (hoặc entropy cao); (3) đo xem những elements bị flag có indeed bị mis-classified nhiều hơn không → **validate confidence-triggered review** trước khi cần LLM.


---


## 6. ĐÓNG GÓI CHO SLIDE THUYẾT TRÌNH & PHẢN BIỆN (DEFENSE PREP)

- **3–4 Bullet points đắt giá đưa lên Slide Related Work:**
  - *Bullet 1:* Xiao et al. (2024) đề xuất AES framework dựa trên Dual-Process Theory (Fast & Slow Thinking), sử dụng LLaMA3-8B fine-tuned: **Fast Module** (FC classifier, dự đoán nhanh + output confidence) + **Slow Module** (LLM sinh giải thích chi tiết khi confidence thấp).
  - *Bullet 2:* Fine-tuned LLaMA3-8B đạt **QWK > 0.7** trên ASAP, **comparable với** fine-tuned GPT-3.5, và cho chất lượng explanation **ngang GPT-4** (35% win, 40% tie — Section 5.1).
  - *Bullet 3:* **Human-AI co-grading experiment:** Novice evaluators + LLM feedback đạt QWK **0.6609**, không khác biệt thống kê so với expert evaluators alone (**0.7117**, p=0.27). Expert + AI đạt complementary performance (**0.7734**) — Table 3.
  - *Bullet 4:* Nhóm kế thừa: (a) xác nhận triết lý Human-in-the-loop; (b) áp dụng prediction confidence flagging; (c) open-source LLM là viable cho future work.

- **Lời thoại thuyết trình gợi ý (45–60 giây):**
  > *"Paper quan trọng nhất cho dự án của chúng tôi là Xiao và cộng sự năm 2024, người đề xuất một framework chấm bài kết hợp con người và AI dựa trên lý thuyết dual-process. Họ fine-tune LLaMA3-8B với hai module: module Fast cho dự đoán nhanh kèm confidence score, và module Slow sinh giải thích chi tiết khi confidence thấp. Kết quả đặc biệt ấn tượng ở thực nghiệm co-grading: giáo viên mới chưa có kinh nghiệm chấm bài, khi được hỗ trợ bởi AI feedback, đạt chất lượng chấm không khác biệt thống kê so với giáo viên kinh nghiệm. Đây chính là triết lý sản phẩm của nhóm chúng tôi — công cụ hỗ trợ giáo viên, không thay thế giáo viên. Chúng tôi kế thừa ý tưởng confidence flagging: trong MVP dùng Classical ML, chúng tôi sẽ output prediction probability và flag những đoạn lập luận có confidence thấp để giáo viên ưu tiên rà soát."*

- **Bộ câu hỏi phản biện & Gợi ý trả lời:**
  - *Câu hỏi 1:* "Paper dùng LLaMA3-8B fine-tuned, nhóm chỉ dùng TF-IDF + Logistic Regression — có quá đơn giản không?"
    - 👉 **Trả lời:** Chiến lược phát triển của nhóm là incremental: bắt đầu từ interpretable model (TF-IDF + LR/SVM) để hiểu rõ bài toán, features, và failure modes, rồi mới mở rộng sang deep learning. Paper R03 cho thấy ngay cả BERT classifier (supervised) đã đạt ~0.72 QWK — Classical ML có thể là strong starting point. Hơn nữa, sản phẩm human-in-the-loop cần giáo viên hiểu *tại sao* mô hình gợi ý — Logistic Regression coefficients dễ giải thích hơn LLM.
  - *Câu hỏi 2:* "Thực nghiệm co-grading chỉ có 50 bài và 15 người — có đủ tin cậy không?"
    - 👉 **Trả lời:** Chính tác giả cũng thừa nhận đây là pilot study. Nhưng kết quả vẫn có giá trị: (a) p-value < 0.01 cho novice improvement là significant; (b) direction of effect (AI giúp novice tiệm cận expert) nhất quán trên cả Overall, Content, Language, Structure. Nhóm coi đây là motivation chứ không phải proof — và design sản phẩm human-in-the-loop chính là cách giảm thiểu risk từ imperfect AI.
  - *Câu hỏi 3:* "Triết lý Human-in-the-loop nghe hay nhưng thực tế giáo viên có thời gian review từng đoạn không?"
    - 👉 **Trả lời:** Đó chính là tại sao confidence flagging quan trọng: thay vì review tất cả, giáo viên chỉ cần focus vào đoạn lập luận mà mô hình "không chắc chắn" (low confidence). Paper R03 cho thấy mô hình xử lý tốt "routine cases" (high confidence) và chỉ escalate "difficult cases" cho con người — workflow này tiết kiệm thời gian đáng kể. Hơn nữa, paper cho thấy expert evaluators report "less time to complete grading tasks" khi có LLM support.
