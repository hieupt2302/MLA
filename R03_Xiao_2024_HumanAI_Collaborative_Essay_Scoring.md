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
