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
