# PROMPT & STRUCTURE TEMPLATE: TÓM TẮT & PHÂN TÍCH PAPER CHO DỰ ÁN PERSUADE / MLA

> **Hướng dẫn sử dụng:** 
> Copy toàn bộ nội dung từ phần `--- BẮT ĐẦU PROMPT ---` trở đi, dán vào AI (ChatGPT / Claude / Gemini), sau đó đính kèm file PDF hoặc copy toàn văn paper vào sau prompt.

---

```markdown
--- BẮT ĐẦU PROMPT ---

Bạn là một chuyên gia nghiên cứu học thuật về Machine Learning và NLP ứng dụng trong Giáo dục (AIED / Argument Mining). 
Nhiệm vụ của bạn là đọc toàn văn paper được cung cấp dưới đây và tạo một bản phân tích học thuật chuyên sâu (Deep-dive Academic Summary) được "đo ni đóng giày" cho dự án môn học của nhóm tôi.

### 1. BỐI CẢNH DỰ ÁN CỦA CHÚNG TÔI (ĐỂ LIÊN HỆ PHÂN TÍCH):
- **Tên đề tài:** Dự đoán hiệu quả thành phần lập luận nhằm hỗ trợ giáo viên chấm bài nghị luận học sinh (Discourse Effectiveness Prediction for Teacher Support in Student Argumentative Writing).
- **Dataset nền tảng:** PERSUADE Corpus 2.0 / Feedback Prize (Bài nghị luận của học sinh từ lớp 6–12 tại Mỹ, chia nhỏ thành các discourse elements: Claim, Evidence, Rebuttal, Counterclaim, Concluding Statement...).
- **Nhiệm vụ ML:** Phân loại 3 mức chất lượng lập luận: `Ineffective` (kém hiệu quả), `Adequate` (đạt yêu cầu), `Effective` (hiệu quả). Nhãn bị mất cân bằng mạnh (Adequate chiếm đa số, Ineffective là lớp thiểu số nhưng quan trọng nhất về mặt sư phạm).
- **Triết lý sản phẩm:** Human-in-the-loop (công cụ hỗ trợ giáo viên rà soát và ưu tiên phản hồi các đoạn lập luận yếu, giáo viên giữ quyền duyệt/sửa/bác bỏ, KHÔNG tự động chấm điểm thay giáo viên).
- **Chiến lược mô hình:** Bắt đầu từ Classical ML có thể giải thích (TF-IDF + Logistic Regression / Linear SVM) trên ranh giới thành phần đã có, trước khi mở rộng sang Deep Learning hoặc LLM nhỏ.
- **Metric ưu tiên:** Macro-F1, Recall lớp `Ineffective`, Quadratic Weighted Kappa (QWK), Confusion Matrix. Tránh nhìn vào Accuracy đơn thuần.

### 2. NGUYÊN TẮC PHÂN TÍCH BẮT BUỘC:
1. **Tuyệt đối không bịa đặt số liệu (Zero Hallucination):** Mọi con số (Accuracy, F1, QWK, % cải thiện) phải trích xuất chính xác từ Table/Section cụ thể trong paper. Nếu paper không đo hoặc không báo cáo, hãy ghi rõ "Paper không đề cập".
2. **Phân biệt điều kiện thực nghiệm:** Luôn làm rõ paper chạy trên "ranh giới chuẩn có sẵn" (Gold segmentation) hay "ranh giới do mô hình tự suy ra" (Inferred segmentation). Không lấy kết quả trên gold segmentation để quảng bá hiệu quả end-to-end.
3. **Hiểu đúng bản chất metric:** Không nhầm lẫn QWK với Accuracy (QWK đo độ đồng thuận có phạt khoảng cách thứ bậc). Không khen một mô hình chỉ vì Accuracy cao nếu Recall lớp Ineffective quá thấp.
4. **Tách bạch khách quan:** Phân biệt rõ giữa *Điều tác giả paper thực sự chứng minh* vs *Điều nhóm chúng tôi tự suy luận/kế thừa*.
5. **Định dạng:** Trình bày bằng Tiếng Việt học thuật chuẩn xác, văn phong gãy gọn, logic, nghiêm túc.

---

### CẤU TRÚC ĐẦU RA YÊU CẦU (XUẤT RA DƯỚI ĐỊNH DẠNG MARKDOWN):

# [Mã Paper: RXX] — [TÊN BÀI BÁO TIẾNG ANH GỐC]

## 1. METADATA & TRÍCH DẪN CHUẨN APA 7
- **Tác giả:** [Ghi đầy đủ họ tên các tác giả chính]
- **Năm xuất bản / Hội nghị:** [Năm, Venue: ACL, EMNLP, NAACL, BEA, CMNA, LREC...]
- **Trích dẫn APA 7 chuẩn:** [Format: Tác giả (Năm). Tên bài. Nơi xuất bản. DOI/URL]
- **Đường dẫn & Tài nguyên:** [DOI, ACL Anthology link, Github/Code nếu có]
- **Lưu ý phiên bản (nếu có):** [Ví dụ: Bản preprint khác gì bản proceedings, năm workshop vs năm công bố kỷ yếu...]

---

## 2. BÀI TOÁN & THIẾT LẬP THỰC NGHIỆM (PROBLEM & SETUP)
- **Câu hỏi nghiên cứu chính:** [Paper cố gắng giải quyết lỗ hổng (gap) nào?]
- **Nhiệm vụ ML & Phạm vi:** [Tách đoạn (Segmentation) / Phân loại vai trò (Classification) / Đánh giá chất lượng (Quality Assessment)? Pipeline tuần tự (Pipeline) hay học đa nhiệm (Multi-task)?]
- **Dữ liệu thực nghiệm:** [Dùng dataset nào? Có phải PERSUADE/Feedback Prize không? Kích thước mẫu bao nhiêu?]
- **Thiết lập Input/Output:**
  - *Input:* [Văn bản thành phần, ngữ cảnh toàn bài, đề bài (prompt), loại lập luận...]
  - *Output:* [Số lớp dự đoán, nhãn liên tục hay phân loại...]
  - *Điều kiện ranh giới:* [Gold boundaries hay Inferred boundaries?]
- **Các họ mô hình được khảo sát:** [Liệt kê Baseline, Classical ML, Transformers, hay LLMs (nhỏ/lớn)?]

---

## 3. KẾT QUẢ ĐỊNH LƯỢNG CỐT LÕI (KEY FINDINGS & NUMBERS)
*(Lập bảng trích xuất số liệu quan trọng nhất từ các Table trong bài)*

| Mô hình / Thiết lập | Điều kiện (Input / Boundary) | Metric 1 (Macro-F1 / Acc) | Metric 2 (QWK) | Metric 3 (Recall Ineffective nếu có) | Nguồn (Table/Sec) |
|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... |

- **Diễn giải số liệu đúng bản chất:**
  - [Giải thích xem sự chênh lệch điểm số thực chất đến từ đâu? Có phải do thêm ngữ cảnh? Do tăng kích thước mô hình? Hay do đổi split?]
  - [Cảnh báo hiểu sai: Tránh ngộ nhận con số này với con số khác].

---

## 4. HẠN CHẾ & RANH GIỚI (LIMITATIONS & PITFALLS)
- **Hạn chế do chính tác giả thừa nhận:**
  - [Độ dài văn bản bị cắt (truncation)? Khả năng suy rộng sang ngôn ngữ khác? Thiên lệch dữ liệu?]
  - [Lỗi suy luận (inference hallucination / repetition) nếu dùng LLM?]
- **Ranh giới khi áp dụng vào dự án của nhóm:**
  - [Tại sao nhóm không thể bê nguyên kết quả của paper vào lớp học thực tế?]
  - [Mô hình có cung cấp được lời khuyên sư phạm giải thích vì sao đoạn văn yếu không? (Thường là KHÔNG, chỉ phân loại mức độ)].
  - [Rủi ro thiên lệch (Fairness / Bias) giữa các nhóm học sinh].

---

## 5. ĐIỂM KẾ THỪA CHO DỰ ÁN NHÓM (ACTIONABLE TAKEAWAYS)
- **Điểm NÊN kế thừa vào MVP:**
  - [Ví dụ: Kỹ thuật trích xuất đặc trưng, cách đưa prompt/ngữ cảnh vào model, baseline nên chạy, chiến lược GroupKFold theo essay_id/student_id...]
- **Điểm KHÔNG NÊN làm theo (Bẫy cần tránh):**
  - [Ví dụ: Không nên vội vàng fine-tune LLM 7B/8B khi máy không đủ GPU; không nên gộp cả bài toán segmentation vào MVP đầu tiên...]
- **Đề xuất thí nghiệm đối chứng (Ablation Study) lấy cảm hứng từ bài này:**
  - [Gợi ý 1 thí nghiệm cụ thể nhóm có thể chạy trên dataset PERSUADE của nhóm].

---

## 6. ĐÓNG GÓI CHO SLIDE THUYẾT TRÌNH & PHẢN BIỆN (DEFENSE PREP)
- **3–4 Bullet points đắt giá đưa lên Slide Related Work:**
  - *Bullet 1:* [Tác giả + năm + Đóng góp chính]
  - *Bullet 2:* [Kết quả định lượng cụ thể kèm tên Table]
  - *Bullet 3:* [Giới hạn cốt lõi]
  - *Bullet 4:* [Nhóm kế thừa điều gì cho dự án]
- **Lời thoại thuyết trình gợi ý (45–60 giây):**
  - *"..." (Soạn sẵn đoạn script tự nhiên, tự tin, nêu bật trọng tâm để nói trong 1 phút)*
- **Bộ câu hỏi phản biện dễ bị Thầy/Cô chất vấn & Gợi ý trả lời (Q&A Defense):**
  - *Câu hỏi 1:* [Câu hỏi xoáy vào tính mới hoặc lý do chọn bài này]
    - 👉 **Trả lời:** [Cách bảo vệ thuyết phục, không nhận vơ công trình, nhấn mạnh vào giá trị kiểm chứng thực tế]
  - *Câu hỏi 2:* [Câu hỏi xoáy vào sự chênh lệch giữa paper và bài toán thực tế của nhóm]
    - 👉 **Trả lời:** [...]
  - *Câu hỏi 3:* [Câu hỏi về nguy cơ lỗi / rủi ro sư phạm]
    - 👉 **Trả lời:** [...]

--- BẮT ĐẦU NỘI DUNG PAPER CẦN TÓM TẮT DƯỚI ĐÂY ---
[Dán nội dung / upload file paper vào đây]
```
