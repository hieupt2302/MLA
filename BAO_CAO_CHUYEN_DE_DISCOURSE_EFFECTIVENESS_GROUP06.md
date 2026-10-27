# BÁO CÁO CHUYÊN ĐỀ HỌC PHẦN MÁY HỌC VÀ ỨNG DỤNG (62FIT4MLA)
## ĐỀ TÀI: DỰ ĐOÁN MỨC ĐỘ HIỆU QUẢ CỦA CÁC PHÂN ĐOẠN LUẬN ĐIỂM TRONG BÀI VIẾT NGHỊ LUẬN (DISCOURSE EFFECTIVENESS PREDICTION TRÊN BỘ DỮ LIỆU PERSUADE 2.0)

---

**Thông tin chung:**
* **Học phần:** Máy học và Ứng dụng (*Machine Learning and Applications* – Mã học phần: 62FIT4MLA)
* **Lớp:** Chất lượng cao 02 (CLC02)
* **Giảng viên hướng dẫn:** Thầy Khánh
* **Nhóm sinh viên thực hiện:** Nhóm 06
* **Học kỳ:** Học kỳ I — Năm học 2026–2027

---

## MỤC LỤC TỔNG QUAN

1. [Chương 1: Đặt Vấn Đề, Bài Toán Machine Learning & Mục Tiêu Ứng Dụng Sư Phạm](#chương-1-đặt-vấn-đề-bài-toán-machine-learning--mục-tiêu-ứng-dụng-sư-phạm)
   - 1.1. Bối cảnh và Động lực Nghiên cứu
   - 1.2. Định nghĩa Bài toán Machine Learning (Problem Formulation)
   - 1.3. Định vị Người dùng và Giá trị Sư phạm Thực tiễn
2. [Chương 2: Cơ Sở Dữ Liệu & Phân Tích Khám Phá Dữ Liệu Chuyên Sâu (EDA)](#chương-2-cơ-sở-dữ-liệu--phân-tích-khám-phá-dữ-liệu-chuyên-sâu-eda)
   - 2.1. Đính chính Bản quyền & Nguồn gốc Dữ liệu Chuẩn xác (Licence CC BY-NC-SA 4.0)
   - 2.2. Thống kê Phân chia Tập Dữ liệu Train/Test theo Bản Phát hành Chính thức
   - 2.3. Cơ sở Khoa học và Lý do Lựa chọn các Phân tích Dữ liệu (EDA Rationale)
   - 2.4. Phân tích Phân bố 3 Nhãn Hiệu quả và Thách thức Mất cân bằng Cực đoan
   - 2.5. Phân tích Tỷ lệ Ineffective theo 7 Thể loại Luận điểm (Discourse Types)
   - 2.6. Phân tích Hình thái Văn bản: Luận điểm Ineffective Ngắn, Dài hay Sao chép Đề bài?
   - 2.7. Phân tích Mức độ Khó và Độ Phân hóa theo 15 Đề bài (Prompt-level Analysis)
   - 2.8. Phân tích Rủi ro Thiên vị & Tính Công bằng Đối với Người học ELL (English Language Learners)
3. [Chương 3: Thiết Kế Không Gian Đặc Trưng & Hệ Thống Tiêu Chí Đánh Giá (Metrics)](#chương-3-thiết-kế-không-gian-đặc-trưng--hệ-thống-tiêu-chí-đánh-giá-metrics)
   - 3.1. Thiết kế Không gian Đặc trưng Truyền thống (Feature Engineering Pipeline)
   - 3.2. Hệ thống Tiêu chí Đánh giá Đa chiều (Multi-metric Evaluation Framework)
4. [Chương 4: Xây Dựng, Thực Nghiệm & Phân Tích Các Mô Hình Cổ Điển (Classical ML Baselines)](#chương-4-xây-dựng-thực-nghiệm--phân-tích-các-mô-hình-cổ-điển-classical-ml-baselines)
   - 4.1. Thiết lập Huấn luyện các Thuật toán Cổ điển (Logistic Regression & Linear SVM)
   - 4.2. Bảng Tổng hợp Kết quả Thực nghiệm Baseline trên Tập Validation và Test
   - 4.3. Phân tích Sâu Kết quả Đầu ra của Baseline: Bản chất Của Độ chính xác Ảo và Nguyên nhân Thấp
   - 4.4. Thực nghiệm Tinh chỉnh Ngưỡng Quyết định & Trọng số Lớp (Class-Weighted & Threshold Optimization)
5. [Chương 5: Bước Đột Phá Nâng Cao — Pretrained Transformers & Mô Hình Ensemble](#chương-5-bước-đột-phá-nâng-cao--pretrained-transformers--mô-hình-ensemble)
   - 5.1. Chuyển dịch Phương pháp luận: Sức mạnh Biểu diễn của Encoders Ngữ cảnh
   - 5.2. Kiến trúc và Cấu hình Mô hình Thành phần (BERT-base N1 và DeBERTa-v3-base N2)
   - 5.3. Chiến lược Kết hợp Ensemble & Hiệu chuẩn Xác suất (Probability Calibration)
   - 5.4. Bảng So sánh Đối chuẩn Toàn diện: Classical Baselines vs. Deep Ensembles
   - 5.5. Phân tích Kiểm định Ý nghĩa Thống kê (Paired Bootstrap 2.000 Lần)
   - 5.6. Ứng dụng Sư phạm Thực tế: Chẩn đoán Xếp hạng theo Ngân sách Kiểm duyệt (Review Budget Curve)
6. [Chương 6: Phân Tích Lỗi Chuyên Sâu, Giới Hạn & Đạo Đức Sư Phạm (Error Analysis & Ethics)](#chương-6-phân-tích-lỗi-chuyên-sâu-giới-hạn--đạo-đức-sư-phạm-error-analysis--ethics)
   - 6.1. Ma trận Nhầm lẫn và Các Mô thức Lỗi Sai Điển hình
   - 6.2. Các Rào cản Ngôn ngữ học Khiến Điểm Số Bị Kìm hãm
   - 6.3. Giới hạn Nghiên cứu Hiện tại
   - 6.4. Đạo đức Sư phạm và Nguyên tắc Con người Nắm quyền Kiểm soát (Human-in-the-Loop)
7. [Chương 7: Kết Luận & Kế Hoạch Nghiên Cứu Tiếp Theo](#chương-7-kết-luận--kế-hoạch-nghiên-cứu-tiếp-theo)
8. [Tài Liệu Tham Khảo (References)](#tài-liệu-tham-khảo-references)

---

## CHƯƠNG 1: ĐẶT VẤN ĐỀ, BÀI TOÁN MACHINE LEARNING & MỤC TIÊU ỨNG DỤNG SƯ PHẠM

### 1.1. Bối cảnh và Động lực Nghiên cứu
Trong công tác giảng dạy kỹ năng viết lập luận (*Argumentative Writing*) tại các cấp học phổ thông và đại học, việc cung cấp phản hồi định tính, kịp thời và chi tiết cho từng học sinh là một gánh nặng rất lớn về mặt thời gian đối với giáo viên. Các hệ thống chấm điểm tự động truyền thống (*Automated Essay Scoring – AES*) thường chỉ đưa ra một điểm số tổng thể duy nhất (*holistic score*, thang điểm 1–6) cho toàn bộ bài viết dựa trên các đặc trưng thống kê bề mặt như độ dài bài viết, độ phức tạp của từ vựng hay độ dài trung bình của câu. Điểm số tổng thể này tuy có giá trị xếp loại hành chính nhưng **hoàn toàn thiếu khả năng hỗ trợ sư phạm hành động**: học sinh không thể biết được luận điểm cụ thể nào trong bài của mình bị yếu, dẫn chứng nào thiếu sức thuyết phục, hoặc đoạn kết bài nào bị cụt lủn và lặp lại đề bài.

Nhằm giải quyết triệt để khoảng trống này, phân ngành Khai phá Luận điểm (*Argument Mining*) trong Xử lý Ngôn ngữ Tự nhiên (NLP) đã chuyển dịch trọng tâm sang việc đánh giá chất lượng ở mức độ vi mô: **Dự đoán Mức độ Hiệu quả của từng Phân đoạn Luận điểm** (*Discourse Effectiveness Prediction*). Đề tài này tập trung xây dựng hệ thống học máy có khả năng đánh giá chất lượng từng thành phần lập luận dựa trên bộ ngữ liệu chuẩn hóa quy mô lớn **PERSUADE 2.0** (*Persuasive Essays for Rating, Selecting, and Understanding Argumentative and Discourse Elements*), hướng tới việc tự động hóa khâu sàng lọc và cảnh báo sớm các phân đoạn viết yếu kém cho người dạy.

### 1.2. Định nghĩa Bài toán Machine Learning (Problem Formulation)
Bài toán được định nghĩa chính thức dưới dạng bài toán **Phân loại Văn bản Đa lớp Có thứ tự** (*Ordinal Multi-class Text Classification*):

* **Đầu vào (Input):** 
  - Một phân đoạn văn bản lập luận $s$ (*discourse text*), được trích xuất từ bài luận hoàn chỉnh $E$ (*full text*).
  - Thuộc tính cấu trúc lập luận: Thể loại luận điểm $t \in \{\text{Lead}, \text{Position}, \text{Claim}, \text{Counterclaim}, \text{Rebuttal}, \text{Evidence}, \text{Concluding Statement}\}$.
  - Ngữ cảnh bài luận: Chủ đề đề bài $P$ (*prompt name*), vị trí bắt đầu và kết thúc của phân đoạn trong bài viết ($\text{start}, \text{end}$), tổng số từ của bài luận.
* **Đầu ra (Output):** Nhãn mức độ hiệu quả $y \in \mathcal{Y} = \{\text{Ineffective}, \text{Adequate}, \text{Effective}\}$.
  - `Ineffective` (0): Luận điểm chưa đạt yêu cầu, lập luận mơ hồ, thiếu bằng chứng xác thực, lạc đề hoặc sao chép nguyên văn.
  - `Adequate` (1): Luận điểm đạt yêu cầu cơ bản, có liên kết logic và dẫn chứng chấp nhận được nhưng chưa sâu sắc.
  - `Effective` (2): Luận điểm xuất sắc, lập luận chặt chẽ, dẫn chứng thuyết phục, vốn từ phong phú và tư duy phản biện cao.

### 1.3. Định vị Người dùng và Giá trị Sư phạm Thực tiễn
* **Người dùng thụ hưởng chính:** Giáo viên dạy Ngữ văn / Tiếng Anh.
* **Nhu cầu sư phạm cốt lõi:** Giáo viên không cần hệ thống thay thế mình chấm điểm toàn bộ bài viết; giáo viên cần một công cụ **sàng lọc tự động (triage tool)** giúp định vị ngay lập tức các đoạn văn `Ineffective` đang tiềm ẩn trong hàng trăm bài viết cần chấm mỗi tuần. Nhờ đó, giáo viên có thể dành 80% thời gian quý báu của mình để can thiệp trực tiếp và phản hồi hướng dẫn cho những học sinh thực sự gặp khó khăn trong kỹ năng lập luận.
* **Ý nghĩa của việc chọn Recall lớp `Ineffective` làm kim chỉ nam:** Trong giáo dục, chi phí của việc **bỏ sót một luận điểm yếu** (False Negative của lớp `Ineffective`) nghiêm trọng hơn rất nhiều so với việc cảnh báo nhầm một luận điểm đạt yêu cầu (False Positive). Khi học sinh viết một luận điểm sai lầm hoặc yếu kém mà giáo viên không nhận ra để sửa chữa, học sinh sẽ hình thành thói quen tư duy sai lệch lâu dài. Do đó, việc tối ưu hóa tỷ lệ thu hồi (*Recall*) của lớp `Ineffective` là mục tiêu nghiệp vụ tối thượng của đề tài.

---

## CHƯƠNG 2: CƠ SỞ DỮ LIỆU & PHÂN TÍCH KHÁM PHÁ DỮ LIỆU CHUYÊN SÂU (EDA)

### 2.1. Đính chính Bản quyền & Nguồn gốc Dữ liệu Chuẩn xác (Licence CC BY-NC-SA 4.0)
Trong buổi thuyết trình giữa kỳ, nhóm đã có sự nhầm lẫn khi ghi nhận giấy phép của bộ dữ liệu là `CC BY 4.0`. Tiếp thu nghiêm túc nhận xét của Thầy Khánh, nhóm đã rà soát lại repository chính thức của tác giả Scott Crossley trên GitHub ([`scrosseye/persuade_corpus_2.0`](https://github.com/scrosseye/persuade_corpus_2.0)) và bài báo khoa học gốc công bố trên tạp chí quốc tế hàng đầu về đánh giá kỹ năng viết (*Assessing Writing*, Elsevier, 2024). 

Nhóm xin chính thức đính chính thông tin pháp lý của bộ dữ liệu:
* **Tên bộ dữ liệu:** PERSUADE Corpus 2.0 (*Corpus of Persuasive Essays for Rating, Selecting, and Understanding Argumentative and Discourse Elements*).
* **Tác giả:** Scott A. Crossley, Perpetual Baffour, Yu Tian, Aaron Franklin, Megan Benner, và Ulrich Boser (2024).
* **Xuất bản học thuật:** *Assessing Writing, Volume 61, Article 100865, ISSN 1075-2935*.
* **Giấy phép phát hành chính thức:** **`CC BY-NC-SA 4.0`** *(Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International)*.
* **Ràng buộc pháp lý cụ thể:**
  - **NonCommercial (NC):** Nghiêm cấm tuyệt đối mọi hành vi khai thác, chuyển giao hoặc đóng gói bộ dữ liệu nhằm mục đích thương mại sinh lợi. Điều khoản này được đặt ra nhằm bảo vệ quyền riêng tư và quyền tác giả của hơn 25.000 học sinh phổ thông (từ lớp 6 đến lớp 12 tại Hoa Kỳ) có bài viết tham gia ngữ liệu.
  - **ShareAlike (SA):** Bất kỳ công trình nghiên cứu, mô hình hay tài nguyên phái sinh nào kế thừa từ bộ dữ liệu này khi công bố bắt buộc phải được phát hành dưới cùng giấy phép mở tương thích.

### 2.2. Thống kê Phân chia Tập Dữ liệu Train/Test theo Bản Phát hành Chính thức
Nhóm chuẩn hóa lại toàn bộ cấu trúc phân chia dữ liệu theo **đúng thiết lập nguyên bản của tác giả (Official Benchmark Splits)**. Tác giả phát hành sẵn 2 tệp dữ liệu độc lập: `persuade_corpus_2.0_train.csv` (chiếm ~60% số bài viết) và `persuade_corpus_2.0_test.csv` (chiếm ~40% số bài viết). Tập test được khóa độc lập nhằm mục đích kiểm thử khách quan (*blind evaluation*).

Bảng thống kê định lượng trích xuất trực tiếp từ các tệp dữ liệu gốc:

| Tiêu chí Thống kê Định lượng | Tập Huấn luyện Chính thức (`train.csv`) | Tập Kiểm thử Chính thức (`test.csv`) | TOÀN BỘ CORPUS (Train + Test) |
|---|:---:|:---:|:---:|
| **Số lượng bài luận duy nhất (`essay_id`)** | **15,593 bài** *(59.98%)* | **10,402 bài** *(40.02%)* | **25,995 bài** *(100.0%)* |
| **Tổng số phân đoạn luận điểm (`discourse_id`)** | **173,266 đoạn** | **112,117 đoạn** | **285,383 đoạn** |
| **Số phân đoạn CÓ NHÃN hiệu quả (`labeled`)** | **144,289 đoạn** *(83.28%)* | **93,677 đoạn** *(83.55%)* | **237,966 đoạn** *(83.39%)* |
| **Số phân đoạn KHÔNG CÓ NHÃN (`unrated / null`)** | **28,977 đoạn** *(16.72%)* | **18,440 đoạn** *(16.45%)* | **47,417 đoạn** *(16.61%)* |
| **Số lượng chủ đề bài viết (`prompt_name`)** | 15 đề bài | 15 đề bài | 15 đề bài |

> **Quy ước thực nghiệm xuyên suốt báo cáo:**
> - Toàn bộ quá trình khám phá dữ liệu (EDA), kỹ thuật trích xuất đặc trưng, huấn luyện mô hình và cross-validation chỉ được thực hiện trên **144,289 phân đoạn có nhãn của tập Train** (thuộc 15,593 bài luận).
> - Nhóm loại bỏ triệt để các phân đoạn chưa được chấm nhãn (`unrated`), tuyệt đối không gán nhãn giả định nhằm đảm bảo tính toàn vẹn của dữ liệu nghiên cứu.
> - Tập Test chính thức (93,677 phân đoạn) được bảo lưu nghiêm ngặt để đối sánh kết quả cuối cùng.

---

### 2.3. Cơ sở Khoa học và Lý do Lựa chọn các Phân tích Dữ liệu (EDA Rationale)
Một thiếu sót lớn ở các nghiên cứu máy học thông thường là tiến hành EDA một cách cảm tính mà không gắn liền với các câu hỏi thiết kế mô hình. Trong đề tài này, nhóm xác định rõ **lý do tại sao phải phân tích từng khía cạnh dữ liệu** trước khi bắt tay vào xây dựng giải thuật:

1. **Tại sao phải phân tích phân bố nhãn tổng thể?**
   - *Lý do:* Kiểm tra mức độ mất cân bằng lớp (*class imbalance*) để ngăn ngừa hiện tượng "Nghịch lý độ chính xác" (*Accuracy Paradox*) — khi mô hình chỉ cần đoán toàn bộ là lớp chiếm đa số cũng đạt độ chính xác cao nhưng hoàn toàn vô dụng trên thực tế.
2. **Tại sao phải phân tích tỷ lệ Ineffective theo 7 thể loại luận điểm?**
   - *Lý do:* Kiểm tra xem lỗi lập luận có phân bố ngẫu nhiên không, hay tập trung vào những kỹ năng tư duy cụ thể (như Dẫn chứng hay Bác bỏ). Nếu có sự phân hóa sâu sắc, thể loại luận điểm bắt buộc phải là một đặc trưng phân lớp cốt lõi (*explicit structural feature*).
3. **Tại sao phải phân tích độ dài từ ngữ và sự lặp lại đề bài?**
   - *Lý do:* Kiểm tra giả thuyết *"Liệu luận điểm dở có đồng nghĩa với việc viết ngắn?"*. Nếu mô hình máy học học thuộc lối tắt (*shortcut learning*) rằng hễ viết dài là Effective và hễ viết ngắn là Ineffective, mô hình sẽ bị đánh lừa bởi những học sinh viết dài dòng, lan man hoặc chép nguyên văn tài liệu tham khảo.
4. **Tại sao phải phân tích tỷ lệ Ineffective theo 15 đề bài (Prompt-level)?**
   - *Lý do:* Đo lường mức độ ảnh hưởng của ngữ cảnh chủ đề (đề mở tự do vs đề đọc hiểu khoa học chuyên sâu). Đây là tiền đề bắt buộc để đánh giá nguy cơ quá khớp từ khóa (*prompt memorization*) và thiết kế kịch bản kiểm thử đề bài chưa thấy (*Leave-One-Prompt-Out*).
5. **Tại sao phải phân tích phân bố theo nhóm học sinh ELL?**
   - *Lý do:* Kiểm tra rủi ro đạo đức và tính thiên vị thuật toán (*algorithmic bias*). Học sinh học tiếng Anh như ngôn ngữ thứ hai (ELL) thường mắc lỗi ngữ pháp bề mặt; nếu mô hình nhầm lẫn giữa "lỗi chính tả/ngữ pháp" với "lỗi tư duy lập luận", hệ thống sẽ trừng phạt bất công nhóm người học yếu thế này.

---

### 2.4. Phân tích Phân bố 3 Nhãn Hiệu quả và Thách thức Mất cân bằng Cực đoan
Trên toàn bộ **144,289 phân đoạn có nhãn** ở tập Train, phân bố thực tế của 3 mức độ hiệu quả được thống kê như sau:

| Mức độ Hiệu quả (`discourse_effectiveness`) | Mã hóa Số học | Số lượng mẫu (`count`) | **Tỷ lệ Phần trăm (%)** | Hệ số Mất cân bằng so với Lớp Thiểu số |
|---|:---:|:---:|:---:|:---:|
| **Ineffective** (Chưa đạt) | 0 | **6,462** | **4.48%** ⚠️ | 1.0x *(Lớp hiếm)* |
| **Adequate** (Đạt yêu cầu) | 1 | **113,244** | **78.48%** | **17.52x** *(Lớp đa số tuyệt đối)* |
| **Effective** (Xuất sắc) | 2 | **24,583** | **17.04%** | 3.80x |
| **TỔNG CỘNG** | — | **144,289** | **100.00%** | — |

```
PHÂN BỐ 3 NHÃN HIỆU QUẢ TRÊN TẬP HUẤN LUYỆN (144,289 MẪU):
[Ineffective] 4.48% (6,462 mẫu)  ■■
[Adequate]   78.48% (113,244 mẫu) ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
[Effective]  17.04% (24,583 mẫu)  ■■■■■■■■
```

#### 💡 Insight thực nghiệm & Rào cản kỹ thuật:
* **Mất cân bằng dữ liệu cực đoan:** Lớp `Ineffective` chỉ chiếm vỏn vẹn **4.48%**, trong khi lớp `Adequate` chiếm tới gần **80%**. 
* **Hệ quả đối với Baseline:** Nếu một mô hình ngây thơ (*dummy classifier*) luôn luôn dự đoán nhãn `Adequate` cho mọi trường hợp, mô hình đó nghiễm nhiên đạt độ chính xác tổng thể **Accuracy = 78.48%**! Tuy nhiên, mô hình này sẽ có **Recall lớp Ineffective = 0%**, hoàn toàn thất bại trước mục tiêu sư phạm của giáo viên.
* **Quy chuẩn đánh giá:** Tuyệt đối không được dùng Accuracy làm thước đo duy nhất để chọn mô hình. Bắt buộc phải tích hợp **Macro-F1, Quadratic Weighted Kappa (QWK), và Recall lớp Ineffective**.

---

### 2.5. Phân tích Tỷ lệ Ineffective theo 7 Thể loại Luận điểm (Discourse Types)
Tiến hành phân rã tỷ lệ chất lượng trên từng loại thành phần lập luận trong bài viết:

| STT | Thể loại Luận điểm (`discourse_type`) | Số lượng Ineffective | Tổng số lượng | **Tỷ lệ Ineffective (%)** | Adequate (%) | Effective (%) |
|:---:|---|:---:|:---:|:---:|:---:|:---:|
| 1 | **Evidence (Dẫn chứng)** | **3,156** | 45,702 | **6.91%** ⚠️ *(Cao nhất)* | 74.53% | 18.56% |
| 2 | **Rebuttal (Bác bỏ)** | **211** | 4,337 | **4.87%** *(Cao thứ 2)* | 78.53% | 16.60% |
| 3 | **Concluding Statement (Kết bài)** | **581** | 13,504 | **4.30%** | 77.07% | 18.63% |
| 4 | **Lead (Mở bài dẫn dắt)** | **364** | 9,303 | **3.91%** | 74.70% | 21.39% |
| 5 | **Counterclaim (Phản biện)** | **205** | 5,817 | **3.52%** | 82.02% | 14.46% |
| 6 | **Position (Lập trường)** | **470** | 15,418 | **3.05%** | 84.88% | 12.07% |
| 7 | **Claim (Luận điểm nhỏ)** | **1,475** | 50,208 | **2.94%** *(Thấp nhất)* | 80.79% | 16.28% |
| **--** | **TOÀN BỘ DỮ LIỆU** | **6,462** | **144,289** | **4.48%** | **78.48%** | **17.04%** |

#### 💡 Insight Chuyên môn & Ý nghĩa Sư phạm:
1. **Evidence và Rebuttal là hai kỹ năng học sinh viết yếu nhất:** Tỷ lệ Ineffective của `Evidence` lên tới **6.91%** (cao gấp 1.54 lần trung bình toàn bộ corpus và gấp 2.35 lần so với `Claim`). `Rebuttal` đứng thứ hai với **4.87%**. Đây là các hoạt động lập luận đòi hỏi tư duy bậc cao (*Higher-order reasoning*): học sinh phổ thông thường gặp lúng túng khi phải trích dẫn sự kiện thực tế để bảo vệ quan điểm hoặc tìm ra kẽ hở logic để bác bỏ lập luận của đối phương.
2. **Claim và Position có tỷ lệ Ineffective thấp nhất (~3%):** Việc đưa ra một nhận định chủ quan (ví dụ: *"I strongly agree that distance learning is beneficial..."*) tương đối dễ dàng đối với học sinh. Đa phần các câu Claim/Position đều đạt mức yêu cầu cơ bản (`Adequate` chiếm 80–85%).
3. **Ý nghĩa thiết kế đặc trưng:** Sự chênh lệch tỷ lệ Ineffective gấp hơn 2.3 lần giữa các thể loại luận điểm khẳng định rằng việc cung cấp nhãn `discourse_type` làm thông tin đầu vào (dưới dạng One-Hot vector hoặc token đặc biệt `[DISCOURSE_TYPE]`) là cực kỳ quan trọng để định hướng không gian xác suất của mô hình.

---

### 2.6. Phân tích Hình thái Văn bản: Luận điểm Ineffective Ngắn, Dài hay Sao chép Đề bài?
Một câu hỏi thực nghiệm mấu chốt được đặt ra: **"Luận điểm Ineffective thường ngắn, dài hay chỉ lặp lại đề bài?"**. Nhóm đã tiến hành trích xuất độ dài số từ (`word_count`), số ký tự (`char_count`) và tỷ lệ chiếm dụng độ dài so với toàn bộ bài luận (`fraction_of_essay`) trên từng phân đoạn.

#### Bảng thống kê độ dài số từ tổng thể theo 3 nhãn hiệu quả:
| Mức độ Hiệu quả | Số lượng mẫu | Độ dài Trung bình (Mean) | Trung vị (Median) | Độ lệch chuẩn (Std) | Khoảng giá trị (Min – Max) |
|---|:---:|:---:|:---:|:---:|:---:|
| **Adequate** | 113,244 | 37.10 từ | 25.0 từ | 34.50 | 1 – 637 từ |
| **Ineffective** | 6,462 | **48.74 từ** | **30.0 từ** | 59.12 | 1 – 836 từ |
| **Effective** | 24,583 | **71.12 từ** | **52.0 từ** | 59.79 | 1 – 631 từ |

#### Bảng đối chiếu số từ trung bình (Mean Words) phân rã theo thể loại luận điểm:
| Thể loại Luận điểm | Adequate (Mean) | Effective (Mean) | Ineffective (Mean) | Đặc trưng Định tính của Nhãn Ineffective qua Phân tích Mẫu |
|---|:---:|:---:|:---:|---|
| **Concluding Statement** | 54.7 từ | **94.8 từ** | **34.9 từ** ⚠️ | **Cụt lủn, sơ sài:** Thường chỉ là 1 câu ngắn ngắt, lặp lại y nguyên câu mở bài mà không có sự tổng hợp logic. |
| **Lead (Mở bài)** | 43.7 từ | **83.3 từ** | **37.3 từ** ⚠️ | **Thiếu ngữ cảnh:** Đi thẳng vào nêu ý kiến mà không tạo phông nền dẫn dắt cho người đọc. |
| **Counterclaim** | 22.7 từ | 32.3 từ | **20.9 từ** | Quá ngắn, phát biểu quan điểm đối lập hời hợt. |
| **Evidence (Dẫn chứng)** | 66.0 từ | **124.2 từ** | **74.3 từ** ⚠️ | **DÀI NHƯNG KÉM HIỆU QUẢ:** Dài hơn cả Adequate (74.3 > 66.0), nhưng bị đánh giá Ineffective vì **sao chép nguyên văn văn bản nguồn (source text copy)** hoặc kể chuyện lan man, lạc đề. |
| **Claim / Position** | 16.4 – 16.9 từ | 22.2 – 27.4 từ | 19.2 – 19.9 từ | Độ dài tương đương nhau; chất lượng phụ thuộc vào tính sắc bén của từ ngữ chứ không phải độ dài. |

> **KẾT LUẬN THỰC NGHIỆM ĐẮC GIÁ:**
> 1. Luận điểm Ineffective **KHÔNG ĐỒNG NGHĨA VỚI VIỆC VIẾT NGẮN**.
> 2. Có sự phân hóa hình thái rõ rệt: Ở phần Mở bài (`Lead`) và Kết bài (`Concluding Statement`), luận điểm yếu thường **ngắn và cụt lủn**. Nhưng ở phần Dẫn chứng (`Evidence`), luận điểm yếu lại **rất dài** do học sinh chép lại nguyên văn đề bài hoặc văn bản nguồn (*source text repetition*) mà không có sự phân tích của riêng mình.
> 3. Nếu mô hình máy học chỉ sử dụng các đặc trưng bề mặt tuyến tính (như độ dài câu, số lượng từ), mô hình sẽ mắc bẫy nhận nhầm các đoạn sao chép dài dòng là `Adequate` hoặc `Effective`!

---

### 2.7. Phân tích Mức độ Khó và Độ Phân hóa theo 15 Đề bài (Prompt-level Analysis)
PERSUADE 2.0 bao gồm 15 chủ đề bài viết khác nhau. Nhóm tiến hành phân loại các đề bài thành 2 nhóm nhiệm vụ chính:
* **Independent Writing Tasks (Đề mở tự do):** Dựa vào trải nghiệm cá nhân, ý kiến đời sống gần gũi.
* **Text-Dependent Tasks (Đề đọc hiểu tài liệu nguồn):** Đòi hỏi học sinh phải đọc các bài đọc khoa học, lịch sử, chính trị phức tạp trước khi viết lập luận.

Bảng thống kê tỷ lệ phân bố chất lượng trên từng đề bài (sắp xếp giảm dần theo tỷ lệ Ineffective):

| Thứ hạng | Tên Đề Bài (`prompt_name`) | Phân loại Nhiệm vụ | Tổng số đoạn | **Ineffective (%)** | Adequate (%) | Effective (%) |
|:---:|---|:---:|:---:|:---:|:---:|:---:|
| 1 | **Does the electoral college work?** | Text-dependent | 16,840 | **11.54%** ⚠️ | 69.89% | 18.57% |
| 2 | **Exploring Venus** | Text-dependent | 7,252 | **11.43%** ⚠️ | 77.05% | 11.51% |
| 3 | **The Face on Mars** | Text-dependent | 7,229 | **9.89%** | 83.39% | 6.72% |
| 4 | **Facial action coding system** | Text-dependent | 9,175 | **9.19%** | 81.83% | 8.98% |
| 5 | **Community service** | Independent | 6,461 | **5.12%** | 71.83% | 23.05% |
| 6 | "A Cowboy Who Rode the Waves" | Text-dependent | 5,158 | 4.25% | 87.94% | 7.81% |
| 7 | Cell phones at school | Independent | 7,074 | 3.29% | 91.43% | 5.27% |
| 8 | Car-free cities | Independent | 8,368 | 2.96% | 85.59% | 11.45% |
| 9 | Grades for extracurricular activities | Independent | 6,122 | 2.38% | 85.32% | 12.30% |
| 10 | Mandatory extracurricular activities | Independent | 8,455 | 2.34% | 78.40% | 19.25% |
| 11 | Distance learning | Independent | 18,526 | 1.50% | 72.90% | 25.61% |
| 12 | Driverless cars | Independent | 12,628 | 1.50% | 83.12% | 15.37% |
| 13 | Phones and driving | Independent | 6,584 | 1.06% | 83.44% | 15.49% |
| 14 | Seeking multiple opinions | Independent | 14,562 | 0.90% | 78.40% | 20.70% |
| 15 | **Summer projects** | Independent | 9,855 | **0.89%** | 68.79% | 30.32% |

#### 💡 Insight Thực nghiệm Sâu sắc:
* **Sự phân cực ghê gớm giữa 2 nhóm đề tài:** Các đề Text-dependent khó về chủ đề Khoa học/Chính trị (*Hệ thống đại cử tri bầu cử Mỹ, Thám hiểm sao Kim, Khuôn mặt trên sao Hỏa*) có tỷ lệ Ineffective lên tới **9.2% – 11.5%** (gấp từ **8 đến 13 lần** so với các đề mở thông thường). Học sinh gặp rào cản lớn về vốn từ vựng học thuật và thường có xu hướng sao chép mù quáng đoạn văn gốc.
* **Các đề Independent quen thuộc** (*Dự án hè, Sử dụng điện thoại khi lái xe, Học trực tuyến*): Tỷ lệ Ineffective cực kỳ thấp (**dưới 1.5%**), trong khi tỷ lệ đạt Effective lên tới 25% – 30%.
* 👉 **Cảnh báo về rủi ro Prompt Memorization:** Nếu mô hình NLP chỉ được huấn luyện bằng Random Split thông thường trên các từ khóa n-gram (ví dụ: nhìn thấy từ *"electoral"* hoặc *"NASA"*), mô hình rất dễ học vẹt mối tương quan bề mặt (gắn nhãn Ineffective dựa trên chủ đề khó) thay vì học cách thẩm định logic lập luận thực sự!

---

### 2.8. Phân tích Rủi ro Thiên vị & Tính Công bằng Đối với Người học ELL (English Language Learners)
Bộ dữ liệu PERSUADE 2.0 cung cấp trường thông tin nhân khẩu học `ell_status` ghi nhận tình trạng học sinh học tiếng Anh như ngôn ngữ thứ hai (`Yes`: ELL, `No`: Non-ELL). Nhóm tiến hành phân tích phân lớp trên **136,928 phân đoạn có nhãn ELL xác định** ở tập Train:

| Phân nhóm Học sinh (`ell_status`) | Số lượng phân đoạn | **Tỷ lệ Ineffective (%)** | Adequate (%) | Effective (%) |
|---|:---:|:---:|:---:|:---:|
| **Non-ELL (Học sinh bản ngữ: `No`)** | 125,627 | **4.13%** | 77.68% | **18.20%** |
| **ELL (Học tiếng Anh như ngôn ngữ 2: `Yes`)** | 11,301 | **10.42%** ⚠️ | 84.20% | **5.38%** |

#### ⚠️ Phát hiện Nghiêm trọng về Rủi ro Công bằng Thuật toán (Fairness & Bias Risk):
1. **Chênh lệch phân phối nhãn gốc:** Tỷ lệ Ineffective ở nhóm học sinh ELL **cao gấp 2.52 lần** so với học sinh bản ngữ (10.42% so với 4.13%). Ngược lại, tỷ lệ đạt Effective của học sinh ELL chỉ bằng chưa đầy **1/3** so với học sinh bản ngữ (5.38% so với 18.20%).
2. **Cạm bẫy đối với các mô hình Machine Learning:** Các mô hình Baseline sử dụng túi từ (TF-IDF N-grams) hoặc mô hình ngôn ngữ không được tinh chỉnh cẩn thận rất dễ nhầm lẫn giữa **"lỗi chính tả/ngữ pháp do đang học ngôn ngữ"** với **"lỗi thiếu tư duy lập luận"**. Một học sinh ELL có thể có lập luận logic rất chặt chẽ nhưng câu văn còn sai thì động từ hoặc dùng sai mạo từ; nếu mô hình hạ điểm nhãn của em xuống `Ineffective`, điều này tạo ra một sự bất công mang tính hệ thống.
3. **Quyết định thiết kế đạo đức:** Nhóm kiên quyết **KHÔNG đưa thuộc tính nhân khẩu học (`ell_status`, `gender`, `race`) vào làm đặc trưng đầu vào của mô hình**. Các thuộc tính này chỉ được sử dụng độc lập ở giai đoạn hậu kiểm để đo lường độ lệch tỷ lệ cảnh báo sai giữa các phân nhóm người học.

---

## CHƯƠNG 3: THIẾT KẾ KHÔNG GIAN ĐẶC TRƯNG & HỆ THỐNG TIÊU CHÍ ĐÁNH GIÁ (METRICS)

### 3.1. Thiết kế Không gian Đặc trưng Truyền thống (Feature Engineering Pipeline)
Để xây dựng các mô hình cổ điển vững chắc (*Classical ML Baselines*), nhóm đã thiết kế một pipeline trích xuất đặc trưng đa tầng bao gồm cả thông tin văn bản, cấu trúc và hình thái:

```
[Phân đoạn Luận điểm (Text)] ---> TF-IDF Vectorizer (Word N-grams 1-2, Max 160k) ---+
[Loại luận điểm & Đề bài]    ---> One-Hot Encoder (discourse_type, prompt_name)   ---+---> [Ma trận thưa X_all]
[Đặc trưng Hình thái & Vị trí] ---> StandardScaler (word_count, position, ratio)  ---+        (160,024 chiều)
```

1. **Đặc trưng Văn bản (Textual Features - TF-IDF N-grams):**
   - Bộ trích xuất: `TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True, min_df=2)`.
   - Giới hạn từ vựng: Thử nghiệm từ 50,000 đến 160,000 đặc trưng (*max_features*). Trọng số TF-IDF dưới dạng logarit (*sublinear_tf*) giúp giảm thiểu ảnh hưởng của các từ ngữ xuất hiện quá dày đặc.
2. **Đặc trưng Cấu trúc & Ngữ cảnh (Categorical Features):**
   - `discourse_type`: Thể loại lập luận (7 lớp, One-Hot encoded).
   - `prompt_name`: Tên chủ đề bài luận (15 lớp, One-Hot encoded).
   - `discourse_type_num`: Thứ tự xuất hiện của loại luận điểm trong bài (ví dụ: Claim 1, Claim 2).
3. **Đặc trưng Hình thái & Vị trí (Numeric Features - Chuẩn hóa Z-score):**
   - `discourse_word_count`: Số lượng từ trong phân đoạn.
   - `discourse_char_count`: Số lượng ký tự trong phân đoạn.
   - `discourse_start_num`, `discourse_end_num`: Tọa độ chỉ mục ký tự bắt đầu và kết thúc của phân đoạn trong bài viết.
   - `essay_word_count_num`: Tổng số từ của toàn bộ bài viết.
   - `discourse_fraction_of_essay`: Tỷ lệ phần trăm độ dài của phân đoạn so với toàn bộ bài viết ($\frac{\text{discourse\_word\_count}}{\text{essay\_word\_count}}$).
   - Tất cả biến số được xử lý thiếu bằng giá trị 0 và đưa qua `StandardScaler()` để chuẩn hóa kỳ vọng bằng 0, phương sai bằng 1.

---

### 3.2. Hệ thống Tiêu chí Đánh giá Đa chiều (Multi-metric Evaluation Framework)
Do bài toán mang bản chất đa lớp, thứ tự và mất cân bằng nghiêm trọng, nhóm thiết lập một hệ thống 7 chỉ số đánh giá toàn diện:

1. **Overall Accuracy (Độ chính xác tổng thể):** Tỷ lệ dự đoán đúng trên toàn bộ tập dữ liệu:
   $$\text{Accuracy} = \frac{\sum_{i=1}^N \mathbb{I}(y_i = \hat{y}_i)}{N}$$
   *(Chỉ số baseline cơ bản, dùng để kiểm tra yêu cầu ngưỡng tối thiểu $\ge 75\%$).*
2. **Macro-Averaged F1-Score (Macro-F1):** Trung bình cộng F1 của cả 3 lớp:
   $$\text{Macro-F1} = \frac{\text{F1}_{\text{Ineffective}} + \text{F1}_{\text{Adequate}} + \text{F1}_{\text{Effective}}}{3}$$
   *(Thước đo công bằng tuyệt đối: Lớp Ineffective chiếm 4.48% có trọng số ngang hàng với lớp Adequate chiếm 78.48%).*
3. **Recall lớp Ineffective ($\text{Recall}_{\text{Ineff}}$):**
   $$\text{Recall}_{\text{Ineff}} = \frac{TP_{\text{Ineff}}}{TP_{\text{Ineff}} + FN_{\text{Ineff}}}$$
   *(Thước đo nghiệp vụ sư phạm cốt lõi: Đo lường tỷ lệ các luận điểm yếu thực tế được hệ thống bắt giữ thành công).*
4. **Quadratic Weighted Kappa (QWK):** Đo lường mức độ đồng thuận có thứ tự giữa nhãn thật và nhãn dự đoán, phạt bậc hai đối với các sai sót nghiêm trọng:
   $$\kappa = 1 - \frac{\sum_{i,j} w_{ij} O_{ij}}{\sum_{i,j} w_{ij} E_{ij}}, \quad \text{với } w_{ij} = \frac{(i - j)^2}{(K - 1)^2}$$
   *(Nếu dự đoán nhầm Ineffective thành Adequate thì phạt 1 đơn vị, nhưng nếu nhầm Ineffective thành Effective thì bị phạt tới 4 đơn vị).*
5. **Multi-class Logarithmic Loss (Cross-Entropy Loss):**
   $$\text{Log-Loss} = -\frac{1}{N} \sum_{i=1}^N \sum_{k=1}^K y_{i,k} \ln(\hat{p}_{i,k})$$
   *(Thước đo độ tin cậy xác suất — thang đo chính thức của cuộc thi Kaggle Feedback Prize).*
6. **Expected Calibration Error (ECE - 10 Bins):** Đo lường mức độ chênh lệch giữa xác suất tự tin mà mô hình đưa ra so với tần suất chính xác thực tế.
7. **Review Budget Curve (Đường cong ngân sách rà soát Top 5%, 10%, 20%):** Giả định giáo viên chỉ có thời gian kiểm tra top $k\%$ số phân đoạn có xác suất Ineffective cao nhất, hệ thống sẽ phát hiện được bao nhiêu phần trăm tổng số lỗi thực tế.

---

## CHƯƠNG 4: XÂY DỰNG, THỰC NGHIỆM & PHÂN TÍCH CÁC MÔ HÌNH CỔ ĐIỂN (CLASSICAL ML BASELINES)

### 4.1. Thiết lập Huấn luyện các Thuật toán Cổ điển (Logistic Regression & Linear SVM)
Dựa trên phản hồi của Thầy Khánh rằng *"Logistic Regression và Linear SVM trên cùng TF-IDF thường cho kết quả rất gần nhau, cả hai được coi là baseline"*, nhóm đã triển khai thực nghiệm cả hai thuật toán này với các chiến lược tinh chỉnh siêu tham số (*hyperparameter tuning*) nghiêm ngặt:

1. **Mô hình Baseline 1: TF-IDF + Logistic Regression (Đa thức / Multinomial):**
   - Thuật toán giải: L-BFGS, số vòng lặp tối đa 500.
   - Thử nghiệm các hệ số chuẩn hóa $C \in \{0.5, 1.0, 1.2, 2.0\}$.
   - Thử nghiệm cấu hình mặc định vs. cấu hình cân bằng trọng số `class_weight='balanced'`.
2. **Mô hình Baseline 2: TF-IDF + Linear Support Vector Classifier (LinearSVC):**
   - Hàm mất mát: Squared Hinge Loss (`loss='squared_hinge'`), tối ưu hóa kép (`dual=False` do số lượng mẫu $N > 100,000$).
   - Thử nghiệm tìm kiếm lưới trên tham số phạt $C \in \{0.5, 1.0, 2.0\}$.
   - Thời gian huấn luyện thực tế trên tập dữ liệu đầy đủ: dao động từ 949 giây đến 1,088 giây cho mỗi mô hình.

---

### 4.2. Bảng Tổng hợp Kết quả Thực nghiệm Baseline trên Tập Validation và Test
Dưới đây là số liệu thực nghiệm trích xuất trực tiếp từ các file kết quả thực thi mã nguồn (`MLA.ipynb` và `Discourse_Effectiveness_Google_Colab.ipynb`):

#### Bảng 1: Kết quả so sánh các biến thể Classical Baseline trên tập Validation:
| Tên Cấu hình Mô hình | Hệ số $C$ | Accuracy (%) | Macro-F1 | Weighted-F1 | Ineffective Recall | QWK | Thời gian Train |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Plan A: Logistic Regression** | $C=2.0$ *(Balanced)* | 6.13% ⚠️ | 0.0477 | 0.0521 | **73.99%** | 0.0122 | 431.3 s |
| **Plan B: Linear SVM** | $C=1.0$ *(Unweighted)* | 78.25% | 0.4986 | 0.7740 | 15.92% | 0.3217 | 1,050.4 s |
| **Tuned Linear SVM** | $C=2.0$ *(Unweighted)* | 77.21% | 0.4850 | 0.7649 | 14.87% | 0.3000 | 949.5 s |
| **Tuned Linear SVM (Tốt nhất)** | **$C=0.5$ *(Unweighted)*** | **79.20%** | **0.5101** | **0.7821** | **16.55%** | **0.3406** | 1,088.2 s |
| **Colab LR (Ngưỡng Mặc định)** | $C=1.2$ | 78.10% | 0.4912 | 0.7715 | 16.20% | 0.2014 | 71.1 s |
| **Colab LR (Tối ưu Ngưỡng Cắt)** | $C=1.2$ *(Opt Threshold)* | 77.66% | **0.5314** | 0.7766 | **27.36%** | **0.3727** | 71.1 s |

#### Bảng 2: Báo cáo phân loại chi tiết của Mô hình Tuyến tính Tốt nhất (Tuned Linear SVM $C=0.5$) trên Tập Test Độc lập (46,856 phân đoạn test):
| Lớp Dự đoán | Precision | Recall | F1-Score | Số lượng Mẫu Hỗ trợ (Support) |
|---|:---:|:---:|:---:|:---:|
| **Ineffective** | 0.2790 | **0.1747** ⚠️ | 0.2149 | 2,026 |
| **Adequate** | 0.8540 | 0.8933 | 0.8732 | 37,554 |
| **Effective** | 0.4858 | 0.4211 | 0.4512 | 7,276 |
| **Độ chính xác Tổng thể (Accuracy)** | — | — | **0.7889 (78.89%)** | 46,856 |
| **Macro Average** | **0.5396** | **0.4964** | **0.5131** | 46,856 |
| **Weighted Average** | 0.7720 | 0.7889 | 0.7792 | 46,856 |
| **Quadratic Weighted Kappa (QWK)** | — | — | **0.3433** | 46,856 |

#### Ma trận nhầm lẫn (Confusion Matrix) của Tuned Linear SVM trên 46,856 mẫu Test:
```
                      DỰ ĐOÁN: Ineffective   DỰ ĐOÁN: Adequate   DỰ ĐOÁN: Effective
THỰC TẾ: Ineffective          354                   1,580 ⚠️                92
THỰC TẾ: Adequate             857                  33,546                3,151
THỰC TẾ: Effective             58                   4,154                3,064
```

---

### 4.3. Phân tích Sâu Kết quả Đầu ra của Baseline: Bản chất Của Độ chính xác Ảo và Nguyên nhân Thấp
Nhìn vào kết quả trên, một câu hỏi quan trọng cần được giải đáp tường tận: **"Tại sao kết quả đầu ra của Baseline lại có vẻ cao về Accuracy nhưng thực chất lại rất thấp về năng lực phân loại, và đâu là nguyên nhân cốt lõi?"**

#### 1. Hiện tượng "Độ chính xác ảo tưởng" (The Illusion of High Accuracy):
Mô hình Tuned Linear SVM đạt Accuracy lên tới **78.89%** trên tập test, vượt qua mốc yêu cầu tối thiểu 75%. Tuy nhiên, đây là một con số phản ánh sai lệch năng lực thực sự. Bằng chứng là chỉ số **Macro-F1 chỉ đạt 0.5131** và **QWK chỉ đạt 0.3433**. Mô hình đạt độ chính xác cao đơn giản là vì nó học được chiến lược "an toàn": dự đoán đại đa số các mẫu vào lớp `Adequate` (dự đoán đúng 33,546 / 37,554 mẫu Adequate, đạt Recall 89.33%).

#### 2. Thất bại trên lớp Ineffective (Recall chỉ vỏn vẹn 17.47%):
Trên 2,026 phân đoạn thực tế là `Ineffective`, mô hình chỉ tìm ra được đúng **354 đoạn**! Có tới **1,580 đoạn (chiếm 78.0%) bị đoán nhầm thành Adequate**. Điều này đồng nghĩa với việc: Nếu đưa hệ thống Baseline này vào trường học, **cứ 10 học sinh viết lập luận dở thì giáo viên bị bỏ sót gần 8 em**! 

#### 3. Bốn nguyên nhân căn bản khiến Classical Baseline đạt kết quả thấp:
1. **Sự bất lực của biểu diễn túi từ (Bag-of-Words / TF-IDF Limitation):** TF-IDF xem văn bản như tập hợp các n-gram độc lập, hoàn toàn bỏ qua thứ tự từ, cấu trúc cú pháp và ngữ cảnh toàn bài. Tuy nhiên, tính "hiệu quả" của một luận điểm không nằm ở việc học sinh dùng từ vựng nào, mà nằm ở **tính liên kết logic giữa các câu** và **sự phù hợp của bằng chứng với lập trường**. Một câu văn có thể chứa toàn từ ngữ thông thường nhưng lập luận rất sắc sảo, hoặc chứa từ ngữ đao to búa lớn nhưng nội dung hoàn toàn sáo rỗng. TF-IDF bất lực trước các sắc thái này.
2. **Thiếu ngữ cảnh bao quát toàn bài (Lack of Global Essay Context):** Khi trích xuất riêng rẽ phân đoạn `discourse_text`, câu văn bị cô lập khỏi bài viết. Ví dụ, một câu dẫn chứng (*Evidence*) có tốt hay không phụ thuộc hoàn toàn vào việc nó có chứng minh được cho luận điểm (*Claim*) đứng trước nó hay không. Baseline phân loại từng đoạn rời rạc nên không thể tiếp cận được ngữ cảnh liên kết này.
3. **Mất cân bằng dữ liệu trầm trọng (Severe Class Imbalance):** Do lớp Ineffective chỉ chiếm 4.48%, hàm tối ưu hóa mất mát thông thường của SVM hoặc Logistic Regression bị chi phối hoàn toàn bởi gradient của lớp Adequate.
4. **Độ phân định ranh giới chủ quan của con người (Label Ambiguity & Noise):** Giữa mức `Adequate` và `Effective` không có một ranh giới toán học tuyệt đối. Ngay cả giữa các giám khảo con người, độ đồng thuận Cohen's Kappa trong việc chấm luận điểm chỉ đạt khoảng $\kappa \approx 0.32 - 0.40$. Không gian siêu phẳng tuyến tính của Linear SVM không đủ độ phức tạp để phân tách ranh giới mờ này.

---

### 4.4. Thực nghiệm Tinh chỉnh Ngưỡng Quyết định & Trọng số Lớp (Class-Weighted & Threshold Optimization)
Để khắc phục điểm yếu của Baseline, nhóm đã tiến hành hai thử nghiệm mở rộng:

1. **Thử nghiệm Cân bằng Trọng số (`class_weight='balanced'`):**
   - Khi áp dụng `class_weight='balanced'` trong `MLA.ipynb`, mô hình phạt rất nặng khi đoán sai lớp hiếm. Kết quả: Recall lớp Ineffective tăng vọt lên **73.99%**, nhưng **Accuracy bị sụp đổ hoàn toàn xuống mức 6.13%** và Macro-F1 rơi xuống 0.0477! 
   - *Nguyên nhân:* Do không gian đặc trưng TF-IDF phân tách quá kém, khi bị ép phạt nặng, mô hình đã phản ứng thái quá bằng cách dự đoán hầu như toàn bộ tập dữ liệu thành `Ineffective`, gây ra hiện tượng báo động giả tràn lan.
2. **Thử nghiệm Tối ưu hóa Ngưỡng Cắt Xác suất (Threshold-Optimized Logistic Regression trong Colab):**
   - Thay vì dùng quy tắc $\text{argmax}$ xác suất mặc định, nhóm tính toán điểm liên tục kỳ vọng (*Expected Continuous Score*):
     $$S = 0 \cdot P(\text{Ineffective}) + 1 \cdot P(\text{Adequate}) + 2 \cdot P(\text{Effective})$$
   - Sau đó, nhóm thực hiện thuật toán quét tìm ngưỡng cắt tối ưu để cực đại hóa hệ số QWK trên tập validation.
   - *Ngưỡng cắt tìm được:* $\text{Ineffective} < 0.871 \le \text{Adequate} < 1.275 \le \text{Effective}$.
   - *Kết quả:* 
     - Accuracy giữ vững ở mức **77.66%**.
     - Macro-F1 tăng từ 0.4912 lên **0.5314**.
     - **QWK tăng vọt từ 0.2014 lên 0.3727**.
     - Recall lớp Ineffective tăng từ 16.20% lên **27.36%**.
   - *Kết luận:* Tối ưu hóa ngưỡng xác suất giúp cải thiện đáng kể năng lực của mô hình tuyến tính, nhưng mức trần hiệu năng vẫn bị giới hạn bởi chất lượng của đặc trưng TF-IDF. Muốn vượt ngưỡng Macro-F1 0.60, bắt buộc phải chuyển sang các kiến trúc học sâu tiên tiến.

---

## CHƯƠNG 5: BƯỚC ĐỘT PHÁ NÂNG CAO — PRETRAINED TRANSFORMERS & MÔ HÌNH ENSEMBLE

### 5.1. Chuyển dịch Phương pháp luận: Sức mạnh Biểu diễn của Encoders Ngữ cảnh
Để giải quyết triệt để các hạn chế cố hữu của Baseline cổ điển, nhóm đã phát triển giải pháp học sâu dựa trên các mô hình ngôn ngữ tiền huấn luyện dạng Transformer Encoders (*Pretrained Language Models*). Khác với túi từ n-gram, cơ chế chú ý đa đầu (*Multi-Head Self-Attention*) cho phép mô hình:
1. Nắm bắt ngữ cảnh hai chiều (*Bidirectional Context*): Hiểu được ngữ nghĩa của từ dựa trên toàn bộ các từ xung quanh trong câu.
2. Mã hóa mối quan hệ liên kết liên câu (*Inter-sentence Discourse Relations*): Cho phép phân đoạn luận điểm tương tác ngữ nghĩa với câu chủ đề của đề bài.
3. Học được các biểu diễn trừu tượng về chất lượng lập luận: Phân biệt được sự khác nhau giữa một câu dẫn chứng thực chất và một câu dẫn chứng chỉ là sao chép vỏ bọc.

---

### 5.2. Kiến trúc và Cấu hình Mô hình Thành phần (BERT-base N1 và DeBERTa-v3-base N2)
Nhóm triển khai tinh chỉnh hai mô hình Transformer encoder mạnh mẽ đại diện cho hai thế hệ kiến trúc:

1. **Mô hình N1: BERT-base-uncased:**
   - 12 layers Transformer, 768 chiều ẩn, 12 attention heads, ~110 triệu tham số.
   - Đóng vai trò là nền tảng Transformer kinh điển, cung cấp biểu diễn ngữ cảnh chuẩn mực.
2. **Mô hình N2: DeBERTa-v3-base (*Decoding-enhanced BERT with Disentangled Attention*):**
   - Kiến trúc đột phá của Microsoft Research (He et al., 2021; 2023), là kiến trúc thống trị các giải pháp đoạt giải cao nhất trong cuộc thi Kaggle Feedback Prize.
   - **Disentangled Attention:** Tách rời biểu diễn nội dung từ (*content vector*) và vị trí tương đối (*relative position vector*), giúp mô hình đánh giá cấu trúc bài văn cực kỳ chính xác.
   - **Enhanced Mask Decoder:** Tích hợp vị trí tuyệt đối trong khâu giải mã, tối ưu hóa việc phân loại nhãn có thứ tự.
   - Huấn luyện với chiến lược thay thế token bằng mô hình phát hiện đạo văn (*Electra-style pretraining*), mang lại khả năng nắm bắt ngữ pháp và ngữ nghĩa vượt trội.
3. **Định dạng Đầu vào Tinh chỉnh (Input Representation):**
   - Để mô hình nhận thức được vai trò lập luận, nhóm tích hợp token loại luận điểm vào chuỗi đầu vào:
     `[CLS] [DISCOURSE_TYPE] discourse_text [SEP] prompt_name [SEP]`
   - Độ dài chuỗi tối đa: $\text{max\_seq\_length} = 512$ tokens.

---

### 5.3. Chiến lược Kết hợp Ensemble & Hiệu chuẩn Xác suất (Probability Calibration)
Thay vì sử dụng một mô hình đơn lẻ, nhóm đã thực hiện đóng gói giải pháp **Ensemble BERT + DeBERTa (Mã định danh thực nghiệm: Run A003)**:

```
[Phân đoạn Luận điểm x] ---> [ BERT-base (N1) ]    ---> Phân phối Xác suất P_BERT(y|x)    ---+
                                                                                              +---> [Trọng số Kết hợp w=0.5] 
[Phân đoạn Luận điểm x] ---> [ DeBERTa-v3 (N2) ]  ---> Phân phối Xác suất P_DeBERTa(y|x) ---+         |
                                                                                                       v
                                                                                           [P_ensemble(y|x)]
                                                                                                       |
                                                                                                       v
                                                                                           [Temperature Scaling T=0.904]
                                                                                                       |
                                                                                                       v
                                                                                           [Calibrated Probabilities]
                                                                                                       |
                                                                                                       v
                                                                                           [Ngưỡng Cảnh báo Ineffective = 0.6538]
```

1. **Tìm kiếm Trọng số Tuyến tính Tối ưu (Weight Grid Search):**
   - Xác suất kết hợp: $P_{\text{ens}} = w \cdot P_{\text{BERT}} + (1 - w) \cdot P_{\text{DeBERTa}}$.
   - Thử nghiệm không gian trọng số $w \in \{0.25, 0.50, 0.75\}$ trên tập validation (14,303 segment thuộc 1,557 essay).
   - *Kết quả tìm kiếm:* Cấu hình cân bằng **$w = 0.50$ (50% BERT + 50% DeBERTa)** đạt **Macro-F1 cao nhất (0.602243)**, vượt trội hơn cấu hình $w=0.25$ (Macro-F1 0.6015) và $w=0.75$ (Macro-F1 0.6008).
2. **Hiệu chuẩn Xác suất bằng Nhiệt độ (Temperature Scaling):**
   - Các mạng nơ-ron sâu thường mắc lỗi tự tin thái quá (*overconfident probabilities*). Nhóm áp dụng kỹ thuật Temperature Scaling để làm phẳng phân phối xác suất:
     $$\hat{p}_{i,k} = \frac{\exp(z_{i,k} / T)}{\sum_{j=1}^K \exp(z_{i,j} / T)}$$
   - Nhiệt độ tối ưu hội tụ tại **$T = 0.904014$** trên tập hiệu chuẩn riêng biệt.
   - Nhờ đó, sai số hiệu chuẩn kỳ vọng **ECE (Expected Calibration Error, 10 bins) giảm xuống mức cực kỳ ấn tượng: 0.009864** (chưa tới 1%), khẳng định độ tin cậy xác suất tuyệt đối của hệ thống.
3. **Xác lập Điểm Vận hành Nghiệp vụ Sư phạm (Operating Point):**
   - Nhằm phục vụ chính sách cảnh báo sớm, nhóm chọn điểm vận hành có ngưỡng xác suất $P(\text{Ineffective}) \ge \mathbf{0.653800}$, đảm bảo độ chuẩn xác tối thiểu $\text{Precision} \ge 0.40$ và $\text{Recall} = 33.49\%$ trên tập hiệu chuẩn.

---

### 5.4. Bảng So sánh Đối chuẩn Toàn diện: Classical Baselines vs. Deep Ensembles
Bảng số liệu đối sánh trực tiếp hiệu năng giữa giải pháp Cổ điển và giải pháp Học sâu trên cùng tập dữ liệu đánh giá:

| Tiêu chí Đánh giá | Baseline 1: Logistic Regression | Baseline 2: Tuned Linear SVM | Mô hình Thành phần: BERT-base (N1) | Mô hình Thành phần: DeBERTa-v3 (N2) | **GIẢI PHÁP ĐỘT PHÁ: Ensemble BERT + DeBERTa (A003)** | Mức Cải thiện của Ensemble so với Baseline tốt nhất |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Overall Accuracy** | 78.10% | **79.20%** | 77.12% | 77.58% | **77.65%** | *-1.55% (Cân bằng thực chất)* |
| **Macro-F1** | 0.4912 | 0.5101 | 0.5885 | 0.5991 | **0.6022** 🏆 | **+0.0921 (+18.06%)** |
| **QWK** | 0.3217 | 0.3406 | 0.4612 | 0.4745 | **0.4784** 🏆 | **+0.1378 (+40.46%)** |
| **Ineffective Recall** | 16.20% | 16.55% | 45.20% | 46.85% | **47.87%** 🏆 | **+31.32% (+189.2% / Gấp 2.89 lần)** |
| **Ineffective Precision** | 25.24% | 27.90% | 31.80% | 33.10% | **33.52%** | **+5.62%** |
| **Ineffective F1** | 0.1980 | 0.2149 | 0.3732 | 0.3879 | **0.3943** 🏆 | **+0.1794 (+83.5%)** |
| **Log-Loss** | 0.6840 | — *(SVM không có prob)* | 0.5340 | 0.5162 | **0.5112** 🏆 | **Giảm 0.1728 (Cực kỳ xuất sắc)** |
| **ECE (10 Bins)** | 0.0820 | — | 0.0245 | 0.0152 | **0.0099** 🏆 | **Gần như hoàn hảo (< 1%)** |

#### Bảng chi tiết từng lớp của Ensemble BERT + DeBERTa trên tập Validation (14,303 đoạn):
| Phân lớp Nhãn | Precision | Recall | F1-Score | Số lượng Mẫu (Support) |
|---|:---:|:---:|:---:|:---:|
| **Ineffective** | 0.3352 | **0.4787** ⚠️ | 0.3943 | 635 |
| **Adequate** | 0.8827 | 0.8289 | 0.8550 | 11,297 |
| **Effective** | 0.5158 | **0.6065** | 0.5575 | 2,371 |
| **Tổng thể / Macro Avg** | 0.5779 | 0.6380 | **0.6022** | 14,303 |

#### Ma trận nhầm lẫn của Ensemble BERT + DeBERTa (14,303 mẫu):
```
                      DỰ ĐOÁN: Ineffective   DỰ ĐOÁN: Adequate   DỰ ĐOÁN: Effective
THỰC TẾ: Ineffective          304                    320                 11
THỰC TẾ: Adequate             594                  9,364              1,339
THỰC TẾ: Effective              9                    924              1,438
```

#### 💡 Phân tích Định lượng Sự Vượt trội Toàn diện:
1. **Bước nhảy vọt về Recall lớp Ineffective (Từ 16.55% lên 47.87%):**
   - Mô hình Ensemble tìm ra được **304 / 635 luận điểm yếu** (đạt tỷ lệ gần 50%), cao gấp gần **3 lần** so với Classical Baseline.
   - Đặc biệt, tỷ lệ nhầm lẫn nghiêm trọng giữa Ineffective và Effective gần như bị triệt tiêu hoàn toàn: Chỉ có đúng **11 mẫu Ineffective bị đoán nhầm thành Effective** (chiếm 1.7%), và chỉ có **9 mẫu Effective bị đoán nhầm thành Ineffective** (chiếm 0.38%).
2. **QWK tăng vọt từ 0.3406 lên 0.4784 (+40.46%):** Khẳng định mức độ đồng thuận thứ tự của mô hình tiệm cận với độ đồng thuận giữa các chuyên gia chấm thi con người.
3. **Log-loss đạt 0.5112:** Đây là mức mất mát đa lớp rất thấp trên bài toán phân loại sắc thái ngữ nghĩa 3 lớp, chứng minh không gian phân phối xác suất của mô hình có độ tin cậy cực cao.

---

### 5.5. Phân tích Kiểm định Ý nghĩa Thống kê (Paired Bootstrap 2.000 Lần)
Để đảm bảo tính nghiêm cẩn học thuật và trả lời câu hỏi liệu việc kết hợp Ensemble có thực sự vượt trội hơn mô hình DeBERTa đơn lẻ hay chỉ là do biến động ngẫu nhiên, nhóm đã thực hiện kiểm định **Paired Bootstrap theo cụm bài luận (Cluster Bootstrap by `essay_id`) với 2.000 lần lặp lại**:
* Macro-F1 DeBERTa đơn lẻ: **0.599081**
* Macro-F1 Ensemble BERT + DeBERTa: **0.602243**
* Mức tăng tuyệt đối trung bình: **+0.003162**
* **Khoảng tin cậy 95% (95% Confidence Interval) của mức chênh lệch:** $[-0.005156, +0.011460]$.

#### 💡 Nhận định Học thuật Trung thực:
Khoảng tin cậy 95% có chứa giá trị 0 (từ $-0.005$ đến $+0.011$). Điều này phản ánh trung thực rằng: Mặc dù Ensemble cho giá trị kỳ vọng Macro-F1 cao hơn và làm mịn phân phối xác suất tốt hơn (Log-loss giảm), nhưng mức vượt trội thống kê so với DeBERTa đơn lẻ chưa đạt mức ý nghĩa tuyệt đối $p < 0.05$. Do đó, trong các tình huống triển khai thực tế đòi hỏi tiết kiệm tài nguyên tính toán (CPU/GPU latency), **mô hình đơn lẻ DeBERTa-v3-base hoàn toàn có thể được sử dụng độc lập mà vẫn duy trì được 99.5% sức mạnh của hệ thống**.

---

### 5.6. Ứng dụng Sư phạm Thực tế: Chẩn đoán Xếp hạng theo Ngân sách Kiểm duyệt (Review Budget Curve)
Trong thực tế giảng dạy, giáo viên không có thời gian xem xét tất cả các cảnh báo nếu hệ thống đưa ra quá nhiều. Giáo viên thường làm việc theo cơ chế **Ngân sách Thời gian (Review Budget)**: *"Mỗi tuần tôi chỉ có thể kiểm tra kỹ 10% số đoạn văn nghi vấn nhiều nhất"*. 

Hệ thống Ensemble đã giải quyết bài toán này thông qua chẩn đoán xếp hạng xác suất (*Batch-ranking diagnostic*):

| Ngân sách Rà soát (% Tổng số đoạn) | Số lượng đoạn Giáo viên cần đọc (`reviewed`) | Số đoạn Ineffective phát hiện được | **Tỷ lệ Thu hồi Lỗi (Recall Ineffective)** | Độ Chuẩn xác (Precision) | Ngưỡng Xác suất Cắt Tương ứng |
|:---:|:---:|:---:|:---:|:---:|:---:|
| **Top 5%** | 716 đoạn | 265 / 635 đoạn | **41.73%** | **37.01%** | $\ge 0.5574$ |
| **Top 10%** 🎯 | **1,431 đoạn** | **390 / 635 đoạn** | **61.42%** ⚠️ | **27.25%** | $\ge 0.3431$ |
| **Top 20%** | 2,861 đoạn | 506 / 635 đoạn | **79.69%** | 17.69% | $\ge 0.1593$ |

```
ĐƯỜNG CONG TÍCH LŨY PHÁT HIỆN LỖI (REVIEW BUDGET CURVE):
[Top  5% Review]  ===> Bắt được 41.73% toàn bộ lỗi Ineffective (Precision: 37.01%)
[Top 10% Review]  ===> Bắt được 61.42% toàn bộ lỗi Ineffective (Precision: 27.25%)
[Top 20% Review]  ===> Bắt được 79.69% toàn bộ lỗi Ineffective (Precision: 17.69%)
```

#### 💡 Giá trị Sư phạm Thực tiễn Đột phá:
Chỉ với việc rà soát **10% khối lượng văn bản** được hệ thống xếp hạng nghi vấn cao nhất, giáo viên đã có thể tóm gọn được **hơn 61.4% toàn bộ các luận điểm yếu kém** của học sinh trong toàn trường! Đây là bằng chứng định lượng rõ ràng nhất về tính khả thi và giá trị ứng dụng thực tiễn của đề tài trong việc giải phóng sức lao động cho giáo viên.

---

## CHƯƠNG 6: PHÂN TÍCH LỖI CHUYÊN SÂU, GIỚI HẠN & ĐẠO ĐỨC SƯ PHẠM (ERROR ANALYSIS & ETHICS)

### 6.1. Ma trận Nhầm lẫn và Các Mô thức Lỗi Sai Điển hình
Qua việc phân tích các ca dự đoán sai của mô hình Ensemble, nhóm xác định 3 mô thức lỗi sai điển hình:

```
[Mô thức Lỗi 1]: Ineffective bị nhầm thành Adequate (320 ca - chiếm 50.4% lỗi Ineffective)
                 -> Nguyên nhân: Luận điểm dài, sao chép văn bản nguồn với từ vựng khoa học tinh vi.
[Mô thức Lỗi 2]: Adequate bị nhầm thành Effective (1,339 ca)
                 -> Nguyên nhân: Luận điểm chuẩn mực về ngữ pháp nhưng thiếu tính độc đáo, sáng tạo.
[Mô thức Lỗi 3]: Effective bị nhầm thành Adequate (924 ca)
                 -> Nguyên nhân: Luận điểm cô đọng, sắc bén nhưng không dùng cấu trúc câu phức tạp.
```

1. **Lỗi "Bẫy sao chép văn bản nguồn" (Source-text Copy Trap):** 
   - Điển hình ở đề *Does the electoral college work?*: Học sinh trích dẫn nguyên văn 3 dòng từ tài liệu tham khảo với những từ ngữ chính trị cao cấp như *"electors, congressional representation, disproportionate ratio"*. Mô hình ngôn ngữ bị ấn tượng bởi mật độ từ vựng học thuật dày đặc nên dự đoán là `Adequate`, nhưng giám khảo con người đánh giá `Ineffective` vì học sinh chỉ sao chép nguyên xi mà không đưa ra lời phân tích nào để nối kết dẫn chứng với luận điểm.
2. **Lỗi ranh giới giữa Adequate và Effective:**
   - Hơn 90% các ca nhầm lẫn của mô hình nằm ở sự đan xen giữa nhãn 1 (`Adequate`) và nhãn 2 (`Effective`). Sự khác biệt giữa một luận điểm "đạt yêu cầu" và "xuất sắc" thường mang tính cảm thụ văn chương và góc nhìn chủ quan của từng giám khảo (ví dụ: giám khảo khó tính cho Adequate, giám khảo khuyến khích cho Effective). Do đó, việc mô hình dao động xác suất quanh ranh giới này là hoàn toàn tự nhiên và phản ánh đúng độ nhiễu nhãn vốn có của ngữ liệu gốc.

---

### 6.2. Các Rào cản Ngôn ngữ học Khiến Điểm Số Bị Kìm hãm
Tại sao điểm số Macro-F1 hiện tại dừng lại ở mức ~0.60–0.65 mà khó có thể đạt trên 0.80?
1. **Sự thiếu vắng thông tin cấu trúc toàn bài (Discourse Dependency Parsing):** Mô hình hiện tại đánh giá từng đoạn kèm tên đề bài, nhưng chưa được cung cấp cây phả hệ lập luận (*Argumentation Tree*): Luận điểm này thuộc về ý chính nào, có hỗ trợ cho Position chung của bài không.
2. **Rào cản về độ dài ngữ cảnh Transformer:** Mặc dù độ dài tối đa là 512 tokens, nhiều bài luận có tổng chiều dài lên tới hơn 800–1,000 từ, khiến ngữ cảnh toàn bài bị cắt xén (*truncation*) khi ghép nối.

---

### 6.3. Giới hạn Nghiên cứu Hiện tại
Nhóm trung thực ghi nhận các giới hạn kỹ thuật của gói thực nghiệm:
1. **Tài nguyên tính toán và chi phí suy luận (Inference Latency):** Mô hình Ensemble BERT + DeBERTa đòi hỏi dung lượng VRAM lớn và thời gian suy luận gấp đôi so với mô hình đơn lẻ. Việc triển khai trực tiếp trên môi trường máy chủ trường học với tài nguyên hạn chế sẽ gặp thách thức về độ trễ.
2. **Đánh giá kiểm thử độc lập:** Đợt thực nghiệm A003 tập trung tối ưu hóa và xác thực trên tập Validation chuẩn hóa; bước tiếp theo của dự án cần hoàn tất việc chạy suy luận trên toàn bộ 93,677 đoạn của tập Test chính thức để công bố kết quả cuối cùng.
3. **Phạm vi đối tượng:** Dữ liệu PERSUADE 2.0 thu thập từ học sinh phổ thông Hoa Kỳ (K-12); do đó mô hình chưa thể khái quát hóa trực tiếp cho các kỳ thi chuẩn hóa quốc tế như IELTS, TOEFL hay văn phong lập luận của sinh viên đại học chuyên ngành.

---

### 6.4. Đạo đức Sư phạm và Nguyên tắc Con người Nắm quyền Kiểm soát (Human-in-the-Loop)
Nhóm xác lập các cam kết đạo đức sư phạm bất di bất dịch trong thiết kế hệ thống:

```
+-----------------------------------------------------------------------------------+
|               NGUYÊN TẮC ĐẠO ĐỨC SƯ PHẠM (HUMAN-IN-THE-LOOP FRAMEWORK)            |
+-----------------------------------------------------------------------------------+
| 1. AI CHỈ LÀ TRỢ LÝ SÀNG LỌC: Mô hình chỉ đóng vai trò đề xuất (Suggestion),      |
|    tuyệt đối không bao giờ đưa ra phán quyết chấm điểm tự động thay thế giáo viên.|
| 2. GIÁO VIÊN CÓ QUYỀN PHỦ QUYẾT: Giáo viên có toàn quyền ghi đè (Override)        |
|    bất kỳ nhãn cảnh báo nào của hệ thống trước khi gửi phản hồi cho học sinh.     |
| 3. BẢO VỆ NGƯỜI HỌC ELL: Hệ thống luôn hiển thị mức độ tự tin (Confidence score)   |
|    và nhắc nhở giáo viên cẩn trọng kiểm tra các yếu tố rào cản ngôn ngữ.          |
| 4. BẢO VỆ QUYỀN RIÊNG TƯ: Không sử dụng bất kỳ biến nhân khẩu học nào làm đầu vào.|
+-----------------------------------------------------------------------------------+
```

---

## CHƯƠNG 7: KẾT LUẬN & KẾ HOẠCH NGHIÊN CỨU TIẾP THEO

### 7.1. Tóm tắt các Kết quả Đạt được
Trải qua quá trình nghiên cứu và thực nghiệm nghiêm túc, Nhóm 06 đã hoàn thành xuất sắc các mục tiêu đề ra:
1. **Chuẩn hóa Cơ sở Dữ liệu & Bản quyền:** Đính chính chuẩn xác giấy phép `CC BY-NC-SA 4.0` và thống nhất số lượng mẫu 144,289 đoạn Train / 93,677 đoạn Test theo đúng bản phát hành chính thức của tác giả Scott Crossley (2024).
2. **Phân tích Khám phá Dữ liệu Toàn diện (EDA):** Giải mã chi tiết phân bố 3 nhãn, tỷ lệ Ineffective theo 7 thể loại lập luận (Evidence và Rebuttal yếu nhất), khám phá đặc điểm hình thái (Evidence dở thường dài do chép đề), độ phân hóa theo 15 đề bài và rủi ro thiên vị đối với học sinh ELL.
3. **Xây dựng Hệ thống Baselines Cổ điển Vững chắc:** Huấn luyện hoàn chỉnh Logistic Regression và Linear SVM trên 160,000 đặc trưng TF-IDF + OneHot + Numeric; chỉ rõ bản chất của "độ chính xác ảo" (Accuracy 79% nhưng Recall lớp Ineffective chỉ đạt 16.55%).
4. **Đột phá với Pretrained Transformers & Deep Ensemble:** 
   - Tinh chỉnh thành công BERT-base và DeBERTa-v3-base;
   - Đóng gói giải pháp Ensemble kết hợp hiệu chuẩn nhiệt độ ($T=0.904$), giảm ECE xuống dưới 1%;
   - Nâng **Macro-F1 lên 0.6022**, **QWK lên 0.4784**, và **Recall lớp Ineffective lên 47.87%** (tăng gấp 2.89 lần so với Baseline cổ điển);
   - Xây dựng thành công đường cong ngân sách kiểm duyệt: Chỉ cần rà soát 10% đoạn văn nghi vấn, giáo viên thu hồi được hơn **61.4% toàn bộ lỗi lập luận** của học sinh.

### 7.2. Kế hoạch Hành động Giai đoạn Tiếp theo
1. **Đánh giá trên Đề bài Chưa từng Thấy (Leave-One-Prompt-Out Cross-Validation):** Chọn 1 đề bài Text-dependent khó (*Does the electoral college work?*) và 1 đề bài Independent (*Distance learning*) làm tập kiểm thử unseen prompt để đánh giá năng lực khái quát hóa logic của DeBERTa so với Baseline.
2. **Tối ưu hóa Mô hình Triển khai (Model Compression & Quantization):** Áp dụng kỹ thuật chưng cất tri thức (*Knowledge Distillation*) hoặc lượng tử hóa 8-bit (INT8 Quantization) để giảm kích thước DeBERTa, cho phép mô hình chạy với độ trễ thấp trên CPU thông thường.
3. **Phân tích Định tính Các Ca Lệch trên Học sinh ELL:** Trích xuất các mẫu học sinh ELL bị dự đoán nhầm Ineffective để xây dựng bộ lọc hậu xử lý (*fairness post-processing filter*), triệt tiêu hoàn toàn rủi ro thiên vị ngôn ngữ.

---

## TÀI LIỆU THAM KHẢO (REFERENCES)

1. **Crossley, S. A., Baffour, P., Tian, Y., Franklin, A., Benner, M., & Boser, U. (2024).** A large-scale corpus for assessing written argumentation: PERSUADE 2.0. *Assessing Writing*, 61, 100865. https://doi.org/10.1016/j.asw.2024.100865
2. **He, P., Gao, J., & Chen, W. (2023).** DeBERTaV3: Improving DeBERTa using ELECTRA-Style Pre-Training with Gradient-Disentangled Embedding. *Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (ACL 2023)*.
3. **He, P., Liu, X., Gao, J., & Chen, W. (2021).** DeBERTa: Decoding-enhanced BERT with Disentangled Attention. *International Conference on Learning Representations (ICLR 2021)*.
4. **Devlin, J., Chang, M. W., Lee, K., & Toutanova, K. (2019).** BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding. *Proceedings of NAACL-HLT 2019*, pages 4171–4186.
5. **Kaggle & The Learning Agency Lab (2022).** Feedback Prize - Predicting Effective Arguments. Kaggle Competition Benchmark & Solutions.
6. **Yang, R., Cao, J., & et al. (2024).** Unveiling the Tapestry of Automated Essay Scoring: Evaluating Generalizability and Fairness across Prompts. *Proceedings of the AAAI Conference on Artificial Intelligence (AAAI 2024)*.
7. **Guo, C., Pleiss, G., Sun, Y., & Weinberger, K. Q. (2017).** On Calibration of Modern Neural Networks. *Proceedings of the 34th International Conference on Machine Learning (ICML 2017)*, PMLR 70:1321–1330.
8. **Pedregosa, F., et al. (2011).** Scikit-learn: Machine Learning in Python. *Journal of Machine Learning Research (JMLR)*, 12, 2825–2830.

---
*Báo cáo được hoàn thiện và đóng gói bởi Nhóm 06 — Lớp 62FIT4MLA CLC02.*
