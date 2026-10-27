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
