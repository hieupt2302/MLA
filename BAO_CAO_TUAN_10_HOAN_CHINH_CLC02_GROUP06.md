<div style="text-align: center; margin-bottom: 25px; padding-bottom: 20px; border-bottom: 2px solid #0f2d59;">
  <h1 style="color: #0f2d59; font-size: 20pt; margin-bottom: 8px; border-bottom: none; padding-bottom: 0;">BÁO CÁO NGHIÊN CỨU KỸ THUẬT (TUẦN 10)</h1>
  <h3 style="color: #1e3d59; font-size: 13pt; font-weight: 500; margin-top: 0; margin-bottom: 16px; line-height: 1.4;">KHẢO SÁT YẾU TỐ GÂY NHIỄU TỪ ĐỘ DÀI, THÍ NGHIỆM TRIỆT TIÊU NGỮ CẢNH CÓ KIỂM SOÁT VÀ ĐÁNH GIÁ KHẢ NĂNG TỔNG QUÁT HÓA TRÊN ĐỀ BÀI MỚI (LOPO) TRONG DỰ BÁO HIỆU QUẢ ĐƠN VỊ LẬP LUẬN</h3>
  <p style="margin: 4px 0; font-size: 10pt;"><strong>Môn học:</strong> Học máy và Ứng dụng (CLC02) &nbsp;|&nbsp; <strong>Niên khóa:</strong> 2025–2026 &nbsp;|&nbsp; <strong>Nhóm thực hiện:</strong> Nhóm 06 (Group 06)</p>
  <p style="margin: 4px 0; font-size: 10pt;"><strong>Tập dữ liệu chính:</strong> Ngữ liệu PERSUADE 2.0 (<em>Assessing Writing</em>, Elsevier, 2024) &nbsp;|&nbsp; <strong>Thời gian:</strong> Tháng 10 năm 2026</p>
  <p style="margin: 4px 0; font-size: 10pt;"><strong>Thư mục lưu trữ kết quả thực nghiệm:</strong> <code>outputs/</code></p>
  <div style="margin-top: 14px; padding: 12px 16px; background-color: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; display: inline-block; text-align: left; font-size: 9.5pt;">
    <strong style="color: #0f2d59;">Liên kết Google Colab tương tác trực tiếp:</strong><br>
    • <strong>Script 04 (Length Confound &amp; LOPO Cổ điển):</strong> <a href="https://colab.research.google.com/drive/1YRMpJgGzZ0vWe7nA0W8c7n5JKMruVJHT?usp=sharing" target="_blank">Mở trên Google Colab</a> (<code>https://colab.research.google.com/drive/1YRMpJgGzZ0vWe7nA0W8c7n5JKMruVJHT?usp=sharing</code>)<br>
    • <strong>Script 05 (Triệt tiêu ngữ cảnh DeBERTa):</strong> <a href="https://colab.research.google.com/drive/1prcSnRHax0SAITnUbGsXks3aQ9pbwJD2?usp=sharing" target="_blank">Mở trên Google Colab</a> (<code>https://colab.research.google.com/drive/1prcSnRHax0SAITnUbGsXks3aQ9pbwJD2?usp=sharing</code>)<br>
    • <strong>Script 06 (Leave-One-Prompt-Out DeBERTa):</strong> <a href="https://colab.research.google.com/drive/1xiYMZ7SjRSAn_ioAvAbNh-PZDkghsiBk?usp=sharing" target="_blank">Mở trên Google Colab</a> (<code>https://colab.research.google.com/drive/1xiYMZ7SjRSAn_ioAvAbNh-PZDkghsiBk?usp=sharing</code>)
  </div>
</div>

## Tóm tắt điều hành (Executive Abstract)

Đánh giá hiệu quả tu từ của các đơn vị lập luận trong bài viết học sinh là một bài toán nền tảng của hệ thống Đánh giá Viết tự động (Automated Writing Evaluation - AWE). Tiếp thu nhận xét phản biện đối với quy trình đánh giá Tuần 9 (*Nhan_xet_Week9_CLC02_Group06*), nghiên cứu này chuyển trọng tâm từ việc đo đạc điểm chuẩn nội bộ sang thí nghiệm chẩn đoán triệt tiêu ngữ cảnh có kiểm soát và kiểm tra khả năng tổng quát hóa trên đề bài mới ngoài phân phối (out-of-domain prompt generalization). Cụ thể, báo cáo cung cấp bằng chứng thực nghiệm giải quyết trọn vẹn các vấn đề phương pháp luận do giảng viên đặt ra:

1. **Khảo sát thực nghiệm yếu tố gây nhiễu từ độ dài bài văn (N = 29.102 đơn vị tập Validation):** Trong các đợt kiểm tra trước, tỷ lệ lỗi phân loại tăng rõ rệt từ 21.98% ở bài ngắn lên 30.35% ở bài dài. Thông qua phân tích 4 phân vị (quartiles) trên 3.119 bài văn tập validation, nhóm chứng minh rằng sự chênh lệch này chủ yếu xuất phát từ **sự dịch chuyển phân phối nhãn và sự dịch chuyển ranh giới chất lượng bài viết**, thay vì chỉ do độ phức tạp cú pháp tích lũy. Ở nhóm bài ngắn (Phân vị Q1: 148–315 từ), tỷ lệ nhãn Kém (Ineffective) chuẩn là **8.97%** và điểm tổng thể bài viết trung bình đạt 2.38/6. Ở nhóm bài dài (Phân vị Q4: 567–8.811 từ, trung vị 712 từ), tỷ lệ Ineffective giảm mạnh gấp 7.0 lần xuống chỉ còn **1.29%**, trong khi tỷ lệ nhãn Hiệu quả cao (Effective) tăng vọt từ 5.29% lên **32.81%** (điểm tổng thể bài viết đạt 4.67/6). Đáng chú ý, phân tích ma trận nhầm lẫn cho thấy **91.52% tổng số lỗi ở Phân vị Q4 (2.018 trên 2.205 ca lỗi) bắt nguồn từ sự phân vân giữa Đạt yêu cầu (Adequate) và Hiệu quả cao (Effective)**, trong khi lỗi trên nhãn Ineffective chỉ chiếm 3.08% tổng số sai sót ở bài văn dài.
2. **Thí nghiệm triệt tiêu ngữ cảnh có kiểm soát (Level 0 so với Level 1 trên DeBERTa-v3-base):** Nhằm kiểm chứng giả thuyết cho rằng việc chấm điểm tự động gặp khó khăn do chỉ nhận đầu vào là các đơn vị cô lập, nhóm thiết lập thử nghiệm so sánh Level 0 (chỉ nhận đơn vị mục tiêu) với Level 1 (đơn vị mục tiêu kèm đơn vị liền trước và liền sau trong bài viết) trên cùng 29.102 đơn vị tập validation (max_length = 512, tỷ lệ cắt cụt token < 0.65%). Khi được bổ sung ngữ cảnh lân cận, **điểm F1 của lớp Ineffective tăng +0.0193 điểm (+5.16% tương đối, từ 0.3741 lên 0.3934)**, trong khi Macro-F1 tổng thể tăng nhẹ từ 0.5768 lên 0.5790 (khoảng tin cậy 95% Bootstrap cặp [-0.0058, +0.0105]). Mức độ cải thiện tập trung rõ rệt ở các đơn vị mang tính quan hệ: Claim (Luận điểm) tăng +0.0430 điểm F1 Ineffective (+16.17% tương đối, bắt thêm được +10 đơn vị), Concluding Statement (Kết luận) tăng +0.0389 điểm, Counterclaim (Phản biện) tăng +0.0303 điểm (+1 đơn vị), và Rebuttal (Bác bỏ) tăng +0.0276 điểm (+1 đơn vị). Ngược lại, các đơn vị luận đề mang tính tự lập (Position) bị sụt giảm -0.0550 điểm (-7 đơn vị bắt trúng), cho thấy ngữ cảnh lân cận tạo ra nhiễu chuyển đoạn đối với việc nhận định lập trường luận đề.
3. **Kiểm định chẩn đoán 10 ca lỗi dự báo nhãn Kém (Ineffective):** Đánh giá lại 10 ca lỗi Ineffective có độ tự tin cao nhất chỉ ra rằng 0/10 ca lật sang nhãn dự báo Ineffective (argmax) khi chỉ bổ sung ngữ cảnh lân cận cục bộ, dù 8/10 ca ghi nhận sự gia tăng xác suất hậu nghiệm P(Ineffective) (trung bình tăng gấp 2.57 lần). Phân loại cơ chế lỗi cho thấy: 2 ca bị lỗi cấu trúc treo (dangling), 4 ca phụ thuộc vào văn bản nguồn bên ngoài của đề bài (ví dụ dẫn chứng sai lệch như trích dẫn *"đoạn văn 36"* không hề tồn tại hoặc mâu thuẫn trực tiếp với ngữ liệu đọc hiểu), và 2 ca đòi hỏi theo dõi lập trường xuyên suốt toàn bộ bài văn.
4. **Đánh giá khả năng tổng quát hóa trên đề bài mới (Leave-One-Prompt-Out - LOPO):** Trên toàn bộ 15 đề bài thông qua kiểm định chéo 15-fold với Random Forest (Bộ đặc trưng B), mô hình cổ điển đạt Macro-F1 trung bình là **0.4303 ± 0.0405** và độ chính xác (accuracy) trung bình đạt **77.09% (không trọng số) / 76.47% (có trọng số)**. Đánh giá mô hình học sâu DeBERTa-v3 tinh chỉnh trên 3 tầng đề bài đại diện (Khó nhất, Trung vị, Dễ nhất) cho thấy DeBERTa vượt trội hơn Random Forest về Macro-F1 trên cả 3 đề (Macro-F1 trung bình: **0.4820 so với 0.4285**, mức tăng tương đối +12.49%), mặc dù độ chính xác tổng thể của DeBERTa thấp hơn một chút do mô hình sử dụng trọng số phạt mạnh để cứu vớt lớp thiểu số (Cowboy: 78.87% so với 79.20%; Summer: 66.58% so với 70.24%; Distance: 75.55% so với 78.05%). So sánh hiệu năng nội miền trên *cùng một đề* so với LOPO cho thấy khoảng cách suy giảm hiệu năng phụ thuộc rất lớn vào bản chất đề bài: các đề dựa trên văn bản đọc hiểu giảm rõ rệt (Cowboy: -8.52%), trong khi các đề nghị luận xã hội mở chuyển giao rất vững chắc (Summer projects: -1.12%; Distance learning: +1.03%). Dưới góc độ các loại lập luận, Rebuttal (-22.79%) và Evidence (-19.36%) chịu sự sụt giảm nặng nề nhất khi sang đề mới, trong khi Position (-10.26%) thể hiện tính bền vững cao nhất.
5. **Tính chặt chẽ khoa học và Khả năng tái lập:** Nhóm điều chỉnh văn phong trung lập, minh bạch hóa đầy đủ ma trận nhầm lẫn 3x3 cho toàn bộ mô hình cơ sở và học sâu, cung cấp khoảng tin cậy Bootstrap chính xác, trích dẫn tài liệu gốc chuẩn mực (*Crossley et al., 2024, Assessing Writing, Tập 61*), và đính kèm đầy đủ sổ tay thực nghiệm Google Colab có thể chạy lại trực tiếp.

---

## Mục lục
1. [Khắc phục phương pháp luận & Phản hồi nhận xét Tuần 9](#1-khac-phuc-phuong-phap-luan--phan-hoi-nhan-xet-tuan-9)
2. [Quy chuẩn đường ống dữ liệu & Cố định phân chia tập mẫu](#2-quy-chuan-duong-ong-du-lieu--co-dinh-phan-chia-tap-mau)
3. [Khảo sát thực nghiệm yếu tố gây nhiễu từ độ dài bài văn](#3-khao-sat-thuc-nghiem-yeu-to-gay-nhieu-tu-do-dai-bai-van)
4. [Thí nghiệm triệt tiêu ngữ cảnh có kiểm soát (Level 0 so với Level 1)](#4-thi-nghiem-triet-tieu-ngu-canh-co-kiem-soat-level-0-so-voi-level-1)
5. [Kiểm định chẩn đoán 10 ca lỗi dự báo nhãn Kém (Ineffective)](#5-kiem-dinh-chan-doan-10-ca-loi-du-bao-nhan-kem-ineffective)
6. [Đánh giá khả năng tổng quát hóa trên đề bài mới (Leave-One-Prompt-Out - LOPO)](#6-danh-gia-kha-nang-tong-quat-hoa-tren-de-bai-moi-leave-one-prompt-out---lopo)
7. [Tổng hợp sư phạm & Giải đáp các câu hỏi lý thuyết](#7-tong-hop-su-pham--giai-dap-cac-cau-hoi-ly-thuyet)
8. [Hiện vật tái lập thực nghiệm & Quản trị mã nguồn](#8-hien-vat-tai-lap-thuc-nghiem--quan-tri-ma-nguon)
9. [Danh mục tài liệu tham khảo](#9-danh-muc-tai-lieu-tham-khao)

---

## 1. Khắc phục phương pháp luận & Phản hồi nhận xét Tuần 9

Tiếp thu các góp ý trong tài liệu *Nhan_xet_Week9_CLC02_Group06.docx.md*, nhóm tiến hành chấn chỉnh toàn diện các vấn đề phương pháp luận:

### 1.1 Khắc phục hạn chế về tương quan hạng Spearman
* **Nhận xét của Giảng viên:** *"Phép so ρ = 0,857 giữa kappa người chấm và F1 mô hình chỉ có 7 điểm, không đủ để kết luận lỗi ở Claim, Counterclaim 'trực tiếp do' người chấm kém đồng thuận. Kappa của mô hình so với nhãn và kappa giữa hai người chấm cũng không phải cùng một đại lượng, nên chưa nói được mô hình 'ngang người'. Các con số kappa theo loại đơn vị cũng cần ghi rõ trang và bảng trong Crossley và cộng sự (2024)."*
* **Biện pháp khắc phục của Nhóm 06:**
  1. **Hạn chế thống kê cỡ mẫu nhỏ (N = 7):** Nhóm chính thức rút lại khẳng định cho rằng sai sót của mô hình trên Claim và Counterclaim là "nguyên nhân trực tiếp" từ độ bất đồng thuận của người chấm. Với cỡ mẫu chỉ có N = 7 loại đơn vị lập luận, hệ số tương quan hạng ρ = 0.8571 (p = 0.0137) có khoảng tin cậy 95% rất rộng ([0.26, 0.98]). Do đó, con số này chỉ được hiểu như một **xu hướng song biến mang tính khám phá (exploratory trend)** chứ không phải bằng chứng xác thực quan hệ nhân quả.
  2. **Tính bất tương đồng giữa hai đại lượng đo (Model κ so với Human-Human κ):** Nhóm làm rõ rằng hệ số Cohen's κ giữa dự báo của mô hình với nhãn chuẩn (κ_model = 0.3704) và hệ số Cohen's κ giữa hai giám khảo độc lập (κ_human-human = 0.316) phản ánh hai bản chất đo lường hoàn toàn khác nhau. Đại lượng thứ nhất đo lường độ khớp của thuật toán phân loại so với một chuẩn tham chiếu đồng thuận, trong khi đại lượng thứ hai đo lường phương sai ngẫu nhiên trong nhận định chủ quan giữa con người với con người. Nhóm hủy bỏ mọi tuyên bố cho rằng mô hình đã "ngang trình độ người chấm".
  3. **Trích dẫn chuẩn xác tài liệu gốc:** Bài báo chính thức công bố bộ ngữ liệu PERSUADE 2.0 là:
     > **Crossley, S. A., Baffour, P., Tian, Y., Franklin, A., Benner, M., & Boser, U. (2024).** *A large-scale corpus for assessing written argumentation: PERSUADE 2.0.* **Assessing Writing**, Tập 61, Mã bài báo 100830. [DOI: 10.1016/j.asw.2024.100830].
     Theo Mục 5 của bài báo, độ tin cậy chấm chéo giữa hai người chấm trên 159.228 đoạn văn được chấm đôi đạt **tỷ lệ đồng thuận tuyệt đối là 0.718** (dao động từ 0.68 đến 0.81 tùy lớp nhãn) và **Cohen's κ tổng thể = 0.316** (dao động từ 0.17 đến 0.38 giữa các lớp nhãn), thể hiện mức độ đồng thuận ở mức trung bình - khá (fair agreement).

### 1.2 Phân tích kỹ thuật về lỗi hiển thị chỉ số LR 6.13%
* **Yêu cầu của Giảng viên:** *"mỗi thành viên phải tự giải thích được lỗi 6,13% bằng lời của mình."*
* **Bản chất kỹ thuật của lỗi:**
  Hiện tượng con số 6.13% xuất hiện ở Tuần 8 là một **lỗi hoán vị chỉ mục (indexing transposition defect)** trong hàm trích xuất chỉ số sau đánh giá:
  1. Trong thư viện `scikit-learn`, thuộc tính `LogisticRegression.classes_` tự động sắp xếp nhãn dạng chuỗi theo thứ tự bảng chữ cái: `['Adequate', 'Effective', 'Ineffective']`, nghĩa là chỉ mục 0 tương ứng với Adequate, chỉ mục 1 là Effective, và chỉ mục 2 mới là Ineffective.
  2. Đoạn mã đánh giá cũ ở Tuần 8 mặc định chỉ mục 0 là Ineffective (`['Ineffective', 'Adequate', 'Effective']`). Do đó, mã nguồn đã lấy nhầm điểm F1 của lớp thiểu số Ineffective (~0.0613) gán vào biến Overall / Balanced Accuracy.
  3. Bản thân mô hình Hồi quy Logistic không bị suy sụp thuật toán; với cùng tập đặc trưng và trọng số lớp cân bằng, khi ánh xạ đúng từ điển `LABEL2ID={'Ineffective': 0, 'Adequate': 1, 'Effective': 2}`, mô hình Logistic Regression đạt Balanced Accuracy thực tế là 60.32% (Macro-F1 0.5086) trên 29.102 đơn vị tập validation.
  4. Kể từ Tuần 9 trở đi, toàn bộ các chỉ số ma trận nhầm lẫn, Precision, Recall và F1 đều được tính toán trực tiếp thông qua ma trận nhầm lẫn dạng vector với bảng ánh xạ nhãn cố định tuyệt đối.

### 1.3 Quy chế quản trị tập kiểm tra chính thức (Official Test Set)
* **Nhận xét của Giảng viên:** *"Validation đang dùng cho chọn mô hình, chọn ngưỡng, hiệu chỉnh và kiểm định. Kết luận vượt trội cuối cùng cần một lần chấm trên Official Test đã khóa cấu hình."*
* **Quy tắc thực thi của Nhóm 06:**
  - **Tập mẫu Validation (N = 29.102 đơn vị)** chỉ được dùng duy nhất cho mục đích lựa chọn mô hình, tinh chỉnh siêu tham số, thực hiện thí nghiệm triệt tiêu ngữ cảnh và phân tích lỗi chẩn đoán.
  - **Tập kiểm tra chính thức khóa kín (Official Test Holdout, N = 93.677 đơn vị, 10.402 bài văn)** được **bảo vệ nguyên vẹn và tuyệt đối không chạm tới**.
  - **Đăng ký trước cấu hình khóa:** Nhóm ấn định cấu hình mô hình cuối cùng trước khi chạy nghiệm thu trên Official Test như sau: kiến trúc nền tảng `microsoft/deberta-v3-base`, định dạng đầu vào Level 1 (kèm hai đơn vị lân cận), kích thước batch hiệu dụng 32, tốc độ học 2e-5, huấn luyện 3 epochs, hàm mất mát cross-entropy với trọng số lớp cân bằng, luật quyết định argmax mặc định, cố định seed 42. Việc lựa chọn cấu hình này dựa hoàn toàn trên sự vượt trội về Macro-F1 trên tập validation.

### 1.4 Hiệu chỉnh văn phong khoa học và Chuẩn mực trình bày
Nhóm đã rà soát và loại bỏ toàn bộ các từ ngữ mang tính phóng đại:
- Thay thế cụm từ *"phân tích pháp y"* (forensic analysis) bằng *"kiểm định chẩn đoán lỗi"* hoặc *"khảo sát thực nghiệm"*.
- Thay thế *"chứng minh dứt khoát"* bằng *"bằng chứng thực nghiệm chỉ ra rằng"* hoặc *"kết quả kiểm định hỗ trợ giả thuyết"*.
- Loại bỏ các suy diễn chủ quan so sánh hiệu năng máy tính với giám khảo con người.
- Định dạng các đại lượng, số đếm và tỷ lệ phần trăm dưới dạng văn bản thuần để loại bỏ triệt để hiện tượng lỗi hiển thị hoặc lặp ký tự trên các trình biên dịch PDF/HTML.

---

## 2. Quy chuẩn đường ống dữ liệu & Cố định phân chia tập mẫu

### 2.1 Đường ống lọc và Ép kiểu chuỗi định danh
Tất cả các tệp dữ liệu thô đều được xử lý với quy tắc ép kiểu chuỗi nghiêm ngặt (`dtype={'essay_id': str, 'discourse_id': str}`) nhằm ngăn chặn lỗi ép kiểu số làm mất các chữ số 0 ở đầu mã định danh. Mọi đánh giá đều thực hiện trên **ranh giới phân đoạn chuẩn có sẵn (gold segmentation discourse boundaries)** của ngữ liệu PERSUADE 2.0.

| Giai đoạn đường ống | Tập Huấn luyện (Train Fit - 80%) | Tập Thẩm định (Validation - 20%) | Tập Kiểm tra Khóa kín (Official Test) |
|---|:---:|:---:|:---:|
| **Số dòng thô trong file CSV gốc** | 173.266 dòng thô | (Tách ra từ file train CSV) | 112.117 dòng thô |
| **Số đơn vị chưa gán nhãn loại bỏ** | 28.977 đoạn | (Loại bỏ trước khi tách tập) | 18.440 đoạn |
| **Số đơn vị hợp lệ đã làm sạch** | 115.187 đơn vị | 29.102 đơn vị | 93.677 đơn vị |
| **Số bài văn duy nhất (String ID)** | 12.474 bài văn | 3.119 bài văn | 10.402 bài văn |
| **Chiến lược phân chia** | GroupShuffleSplit (seed=42) | GroupShuffleSplit (seed=42) | Phân chia chuẩn của Cuộc thi |
| **Rò rỉ bài văn giữa các tập** | Tuyệt đối 0 bài rò rỉ | Tuyệt đối 0 bài rò rỉ | Tuyệt đối 0 bài rò rỉ |

### 2.2 Bảng tổng hợp các tập phân vùng chuẩn hóa

| Tập phân vùng dữ liệu | Số lượng bài văn | Tổng số đơn vị lập luận | Tỷ lệ Kém (%) | Tỷ lệ Đạt (%) | Tỷ lệ Tốt (%) | Vai trò chính trong nghiên cứu |
|---|:---:|:---:|:---:|:---:|:---:|---|
| **Tập Huấn luyện (Train Fit - 80%)** | 12.474 | 115.187 | 4.46% | 78.44% | 17.11% | Trích xuất đặc trưng, huấn luyện mô hình cơ sở và tinh chỉnh DeBERTa |
| **Tập Thẩm định (Validation - 20%)** | 3.119 | 29.102 | 4.56% | 78.68% | 16.76% | Phân tích 4 phân vị độ dài, triệt tiêu ngữ cảnh, kiểm định Bootstrap |
| **Tập Kiểm tra Khóa kín (Official Test)** | 10.402 | 93.677 | 4.51% | 80.45% | 15.04% | Chuẩn đánh giá cuối cùng, được giữ nguyên vẹn tuyệt đối |

---

## 3. Khảo sát thực nghiệm yếu tố gây nhiễu từ độ dài bài văn

### 3.1 Hiện tượng quan sát và Các giả thuyết đối lập
Trong các phân tích sơ bộ trước đây, tỷ lệ lỗi phân loại tăng dần theo số lượng từ của bài viết:
$$\text{Tỷ lệ lỗi quan sát: } 21.98\% \text{ (Phân vị 1 - Bài ngắn)} \longrightarrow 30.35\% \text{ (Phân vị 4 - Bài dài)}$$

Có hai giả thuyết đối lập giải thích hiện tượng này:

* **Giả thuyết A (Độ phức tạp tu từ):** Các bài văn dài sở hữu cây cú pháp phức tạp, cấu trúc lập luận nhiều câu móc nối vượt quá khả năng tiếp nhận của cửa sổ chú ý cố định của mô hình.
* **Giả thuyết B (Dịch chuyển phân phối nhãn và Trình độ viết):** Độ dài bài văn là một biến gây nhiễu bị gắn chặt với trình độ viết của học sinh và đặc tính của đề bài. Điều này làm dịch chuyển phân phối lớp, chuyển thách thức phân loại từ việc nhận diện lớp thiểu số Kém (Ineffective) sang việc phân định ranh giới tinh tế giữa Đạt yêu cầu (Adequate) và Hiệu quả cao (Effective).

### 3.2 Phân tích 4 phân vị trên tập Validation (N = 29.102 đơn vị)

Để kiểm chứng các giả thuyết, toàn bộ 29.102 đơn vị tập validation được chia thành 4 phân vị bằng nhau (Q1 đến Q4) dựa trên tổng số từ của bài viết:

| Phân vị độ dài | Khoảng số từ | Số đơn vị (N) | Số bài văn (N) | Điểm tổng thể TB (1–6) | Tỷ lệ Kém | Tỷ lệ Đạt | Tỷ lệ Tốt | Tỷ lệ lỗi chung | Lỗi trên nhãn Kém | Lỗi trên nhãn Đạt | Lỗi trên nhãn Tốt |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Q1 (Ngắn)** | 148 – 315 | 7.333 | 1.037 | 2.38 | 8.97% | 85.74% | 5.29% | 21.98% | 51.52% | 16.72% | 57.22% |
| **Q2 (TB Thấp)** | 316 – 422 | 7.277 | 786 | 3.20 | 5.02% | 84.27% | 10.72% | 24.50% | 55.07% | 19.83% | 46.92% |
| **Q3 (TB Cao)** | 423 – 566 | 7.226 | 690 | 3.81 | 2.92% | 78.74% | 18.34% | 27.68% | 57.82% | 23.64% | 40.23% |
| **Q4 (Dài)** | 567 – 8.811 | 7.266 | 606 | 4.67 | 1.29% | 65.90% | 32.81% | 30.35% | 72.34% | 33.46% | 22.44% |

*Ghi chú về phân vị Q4:* Khoảng đếm từ của Q4 kéo dài đến 8.811 từ do có một bài viết cá biệt mang độ dài ngoại lai (*Exploring Venus*, mã bài `AAAVUP14319000135886`); giá trị trung vị thực tế của Q4 là 712 từ và phân vị thứ 95 đạt 1.048 từ.

### 3.3 Phân rã cấu trúc đề bài theo từng phân vị độ dài
Khi thống kê phân phối đề bài trên từng phân vị (`outputs/length_quartile_prompt_breakdown.csv`), hiệu ứng phân hóa đề bài thể hiện rất rõ nét:
* Ở **Phân vị Q1 (Bài ngắn)**, các đề bài thuộc chủ đề nội quy học đường và giáo dục công dân chiếm ưu thế: *Does the electoral college work?* (10.50%), *Grades for extracurricular activities* (10.27%), và *Cell phones at school* (9.76%).
* Ở **Phân vị Q4 (Bài dài)**, các đề bài nghị luận mở hoặc kể chuyện chiếm tỷ trọng áp đảo: Đề *Distance learning* chiếm tới **27.36%** (1.988 đơn vị), tiếp theo là *Summer projects* (17.09%) và *Seeking multiple opinions* (16.93%). Tổng cộng ba đề bài này chiếm đến **61.38%** toàn bộ các đơn vị lập luận trong nhóm Q4.

### 3.4 Kết luận thực nghiệm về yếu tố gây nhiễu
1. **Mối tương quan thuận trực tiếp với năng lực viết của học sinh:** Điểm số bài văn tổng thể (holistic score) tăng gần gấp đôi từ **2.38/6 ở Q1 lên 4.67/6 ở Q4**. Những học sinh có năng lực viết tốt hơn sẽ viết bài dài hơn đáng kể và tổ chức lập luận vững chắc hơn. Do đó, tỷ lệ nhãn Kém (Ineffective) thực tế giảm mạnh gấp 7.0 lần, từ 8.97% ở Q1 xuống chỉ còn 1.29% ở Q4 (chỉ có duy nhất 94 đơn vị Ineffective trong toàn bộ tập Q4).
2. **Phân rã bản chất các ca lỗi trong Q4:** Bóc tách ma trận nhầm lẫn của DeBERTa trên tập Q4 (tổng số lỗi = 2.205 đơn vị):
   - Số lỗi rơi vào nhãn Kém chuẩn chỉ chiếm **68 đơn vị (3.08% tổng số lỗi của Q4)**.
   - Nhầm lẫn giữa Đạt yêu cầu và Hiệu quả cao chiếm tới **2.018 đơn vị (91.52% tổng số lỗi của Q4)**: trong đó 1.491 đơn vị Adequate bị đoán nhầm thành Effective, và 527 đơn vị Effective bị đoán nhầm thành Adequate.
3. **Kết luận khoa học:** Tỷ lệ lỗi gia tăng ở các bài văn dài **không phải do mô hình bị quá tải khi bắt lỗi câu văn Kém**, mà do nhóm Q4 tập trung phần lớn các bài văn chất lượng cao, nơi bài toán chính là phân định ranh giới giữa Đạt yêu cầu và Xuất sắc. Bằng chứng phân rã thực nghiệm ủng hộ mạnh mẽ **Giả thuyết B**.

---

## 4. Thí nghiệm triệt tiêu ngữ cảnh có kiểm soát (Level 0 so với Level 1)

### 4.1 Thiết lập thực nghiệm có kiểm soát
Để kiểm tra lượng thông tin mà mô hình chấm điểm tự động thực sự đòi hỏi, nhóm thiết lập thử nghiệm so sánh có kiểm soát tuyệt đối giữa đầu vào đơn vị cô lập và đầu vào có bổ sung ngữ cảnh kế cận:
- **Kiến trúc mạng:** `microsoft/deberta-v3-base` (86 triệu tham số).
- **Phân chia tập mẫu:** Giữ nguyên GroupShuffleSplit chuẩn (115.187 đơn vị train, 29.102 đơn vị validation trên 3.119 bài văn; seed=42).
- **Siêu tham số:** Kích thước batch hiệu dụng 32 (8 mẫu/GPU x 4 bước tích lũy gradient), 3 epochs, tốc độ học 2e-5 với bước làm ấm tuyến tính (warmup 10%), độ chính xác hỗn hợp FP16, trọng số lớp cân bằng:
  $$w_0 (\text{Ineffective}) = 7.4787, \quad w_1 (\text{Adequate}) = 0.4250, \quad w_2 (\text{Effective}) = 1.9484$$
- **Độ dài chuỗi và Tỷ lệ cắt cụt:** Giới hạn max_length = 512 với chiến lược cắt cụt hai đầu.
  - Đầu vào Level 0 có độ dài trung bình 58.0 token; tỷ lệ vượt quá 512 token chỉ là **0.04%** (12 đơn vị).
  - Đầu vào Level 1 có độ dài trung bình 164.7 token; tỷ lệ cắt cụt chỉ là **0.62%** (180 trên 29.102 đơn vị). Đối với riêng Position, tỷ lệ cắt cụt chỉ là **0.42%** (độ dài trung bình 145.1 token), xác nhận rằng việc giảm điểm ở Position không bắt nguồn từ lỗi mất từ do cắt cụt chuỗi.

#### Định dạng đầu vào so sánh:

* **Level 0 (Mô hình cơ sở chỉ nhận đơn vị mục tiêu):**
  $$\mathbf{x}_{\text{Level 0}} = \tau_{i,j} \circ \text{[SEP]} \circ s_{i,j}$$

* **Level 1 (Đơn vị mục tiêu kèm hai đơn vị lân cận):**
  $$\mathbf{x}_{\text{Level 1}} = \tau_{i,j} \circ \text{[SEP]} \circ \text{Previous: } s_{i,j-1} \circ \text{[SEP]} \circ \text{Target: } s_{i,j} \circ \text{[SEP]} \circ \text{Next: } s_{i,j+1}$$
  
  trong đó $s_{i,j-1}$ và $s_{i,j+1}$ là đơn vị đứng ngay trước và ngay sau trong bài văn theo chỉ mục ký tự (`discourse_start`). Nếu đơn vị nằm ở đầu hoặc cuối bài văn, token `[NONE]` sẽ được chèn vào.

### 4.2 Kết quả chuẩn đối sánh & Ma trận nhầm lẫn (N = 29.102 đơn vị Validation)

Dưới đây là ma trận nhầm lẫn 3x3 chi tiết và bảng so sánh hiệu năng trên cùng một tập thẩm định:

### 4.2.1 Ma trận nhầm lẫn 3x3 chính xác (Hàng: Nhãn chuẩn, Cột: Nhãn dự báo):

* **Mô hình cổ điển Random Forest (Bộ đặc trưng B):**
  ```
  [[  286,   999,    43],    --> Nhãn chuẩn Ineffective (N = 1.328): Recall = 21.54%, Precision = 26.70%
   [  764, 20018,  2115],    --> Nhãn chuẩn Adequate    (N = 22.897): Recall = 87.43%, Precision = 84.45%
   [   21,  2687,  2169]]    --> Nhãn chuẩn Effective   (N = 4.877): Recall = 44.47%, Precision = 50.13%
  Độ chính xác (Accuracy) = 22.473 / 29.102 = 77.22% | Macro-F1 = (0.2384 + 0.8591 + 0.4713) / 3 = 0.5230
  ```

* **DeBERTa-v3 Level 0 (Chỉ nhận đơn vị mục tiêu):**
  ```
  [[  598,   682,    48],    --> Nhãn chuẩn Ineffective (N = 1.328): Recall = 45.03%, Precision = 32.00%
   [ 1245, 17683,  3969],    --> Nhãn chuẩn Adequate    (N = 22.897): Recall = 77.23%, Precision = 88.44%
   [   26,  1630,  3221]]    --> Nhãn chuẩn Effective   (N = 4.877): Recall = 66.04%, Precision = 44.50%
  Độ chính xác (Accuracy) = 21.502 / 29.102 = 73.88% | Macro-F1 = (0.3741 + 0.8245 + 0.5317) / 3 = 0.5768
  ```

* **DeBERTa-v3 Level 1 (Kèm đơn vị lân cận):**
  ```
  [[  574,   708,    46],    --> Nhãn chuẩn Ineffective (N = 1.328): Recall = 43.22%, Precision = 36.10%
   [  998, 17286,  4613],    --> Nhãn chuẩn Adequate    (N = 22.897): Recall = 75.49%, Precision = 88.92%
   [   18,  1447,  3412]]    --> Nhãn chuẩn Effective   (N = 4.877): Recall = 69.96%, Precision = 42.27%
  Độ chính xác (Accuracy) = 21.272 / 29.102 = 73.09% | Macro-F1 = (0.3934 + 0.8166 + 0.5270) / 3 = 0.5790
  ```

#### Bảng tổng hợp hiệu năng so sánh:

| Chỉ số đánh giá | Level 0 (Đơn vị cô lập) | Level 1 (+ Ngữ cảnh lân cận) | Độ lệch tuyệt đối | Mức thay đổi tương đối (%) |
|---|:---:|:---:|:---:|:---:|
| **Macro-F1 (Chỉ số chính)** | **0.5768** | **0.5790** | **+0.0022 điểm** | +0.38% |
| **Độ chính xác (Accuracy)** | 73.88% | 73.09% | -0.79 điểm | -1.07% |
| **Độ chính xác cân bằng (Balanced Acc)** | 62.77% | 62.89% | +0.12 điểm | +0.19% |
| **Quadratic Weighted Kappa (QWK)** | 0.4414 | 0.4384 | -0.0030 điểm | -0.68% |
| **Cohen's κ không trọng số** | 0.3704 | 0.3676 | -0.0028 điểm | -0.76% |
| **F1: Lớp Kém (Ineffective - Lớp 0)** | **0.3741** | **0.3934** | **+0.0193 điểm** | **+5.16%** |
| **Precision: Lớp Kém** | 32.00% | 36.10% | +4.10 điểm | +12.81% |
| **Recall: Lớp Kém** | 45.03% | 43.22% | -1.81 điểm | -4.02% |
| **F1: Lớp Đạt (Adequate - Lớp 1)** | 0.8245 | 0.8166 | -0.0079 điểm | -0.96% |
| **F1: Lớp Tốt (Effective - Lớp 2)** | 0.5317 | 0.5270 | -0.0047 điểm | -0.88% |

#### Kiểm định ý nghĩa thống kê bằng Paired Bootstrap (1.000 lượt theo bài viết):
- **Độ chênh lệch Macro-F1:** Giá trị trung bình = +0.0021 điểm, **Khoảng tin cậy 95% CI: [-0.0058, +0.0105]**. Do khoảng tin cậy chứa giá trị 0, mức tăng Macro-F1 tổng thể chưa đạt ý nghĩa thống kê ở mức α = 0.05.
- **Độ chênh lệch F1 lớp Kém (Ineffective):** Giá trị trung bình = +0.0188 điểm, **Khoảng tin cậy 95% CI: [-0.0020, +0.0398]**. Phân phối tập trung phần lớn ở phía dương (cận trên đạt tới +0.0398), được thúc đẩy nhờ việc giảm mạnh báo động giả trên các câu đạt chuẩn (giảm từ 1.245 ca đoán nhầm xuống 998 ca).

### 4.3 Phân rã hiệu năng chi tiết theo 7 loại đơn vị lập luận

Kết quả so sánh giữa Level 0 và Level 1 trên 7 loại lập luận giải đáp trực tiếp câu hỏi của giảng viên (*"Ineffective được cải thiện ở loại đơn vị nào?"*):

| Loại đơn vị lập luận | Số đơn vị Val (N) | Số đơn vị Kém (N) | F1 Kém Level 0 | F1 Kém Level 1 | Chênh lệch điểm F1 | Mức tăng tương đối (%) | Thay đổi Recall (Số ca cứu vãn) |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Claim (Luận điểm)** | 10.135 | 317 | 0.2660 | **0.3090** | **+0.0430** | **+16.17%** | +0.0315 (+10 đơn vị) |
| **Concluding Statement (Kết luận)** | 2.711 | 105 | 0.3484 | **0.3873** | **+0.0389** | **+11.17%** | +0.0095 (+1 đơn vị) |
| **Counterclaim (Phản biện)** | 1.148 | 39 | 0.1975 | **0.2278** | **+0.0303** | **+15.34%** | +0.0256 (+1 đơn vị) |
| **Rebuttal (Bác bỏ)** | 868 | 34 | 0.3488 | **0.3765** | **+0.0276** | **+7.91%** | +0.0294 (+1 đơn vị) |
| **Evidence (Dẫn chứng)** | 9.249 | 667 | 0.4333 | **0.4537** | **+0.0203** | **+4.69%** | -0.0405 (-27 đơn vị) |
| **Lead (Mở đầu / Dẫn dắt)** | 1.902 | 66 | 0.3143 | **0.3175** | +0.0032 | +1.02% | -0.0455 (-3 đơn vị) |
| **Position (Lập trường / Luận đề)** | 3.089 | 100 | 0.3636 | **0.3086** | **-0.0550** | **-15.13%** | -0.0700 (-7 đơn vị) |

### 4.4 Phân tích tu từ mang tính khám phá về tác động của ngữ cảnh
*Lưu ý về quy mô mẫu:* Đối với các nhóm nhãn thiểu số (như Counterclaim chỉ có 39 đơn vị Kém và Rebuttal chỉ có 34 đơn vị Kém), mức dịch chuyển độ nhạy ~0.027 trên thực tế chỉ đại diện cho sự thay đổi đúng/sai của đúng +1 câu văn. Do đó, các kết luận dưới đây được trình bày dưới dạng giả thuyết khám phá:
1. **Các đơn vị lập luận mang tính quan hệ (Claim, Counterclaim, Rebuttal):** Trong văn nghị luận, một Luận điểm (Claim) hiếm khi đứng độc lập; giá trị tu từ của nó phụ thuộc vào việc nó có mở ra một tiền đề mạch lạc được hỗ trợ bởi Dẫn chứng (Evidence) liền sau hay không. Ngữ cảnh lân cận giúp nhận diện các mối nối rời rạc, đem lại mức tăng +0.0430 điểm F1 Kém ở Claim (bắt thêm được +10 đơn vị).
2. **Đơn vị luận đề mang tính tự lập (Position):** Một câu nêu Lập trường / Luận đề của toàn bài được đánh giá chủ yếu dựa trên sự dứt khoát của lập trường và độ bám sát vào câu hỏi của đề bài. Việc đưa thêm câu văn dẫn dắt phía trước hoặc câu luận điểm chi tiết phía sau vô tình tạo ra nhiễu chuyển đoạn, khiến F1 lớp Kém giảm -0.0550 điểm (-7 đơn vị nhận diện). Điều này cho thấy việc chấm câu Luận đề cần sự đối chiếu với đề bài thay vì ngữ cảnh câu lân cận.

---

## 5. Kiểm định chẩn đoán 10 ca lỗi dự báo nhãn Kém (Ineffective)

### 5.1 Câu hỏi định hướng của Giảng viên
* **Câu hỏi:** *"Trong mười ca Ineffective, ca nào sẽ được đoán đúng nếu mô hình thấy được đoạn văn xung quanh, và ca nào thì không?"*

### 5.2 Đánh giá lại thực nghiệm trên 10 ca lỗi
Nhóm đã cho mô hình Level 1 đánh giá lại đúng 10 ca lỗi Ineffective có độ tự tin cao nhất từng được báo cáo ở Tuần 9 (`outputs/context_ablation_case_study_recheck.csv`):

| Mã ca lỗi | Loại đơn vị | Đoạn trích văn bản mục tiêu | Nhãn chuẩn | Dự báo Level 0 | P(Ineff) Level 0 | Dự báo Level 1 | P(Ineff) Level 1 | Tỷ lệ tăng P (L1 / L0) | Phân loại cơ chế lỗi |
|:---:|---|---|:---:|:---:|:---:|:---:|:---:|:---:|---|
| **1** | Counterclaim | *"There are many reason on why texting while driving is very u..."* | Ineffective | Adequate | 0.0225 | Adequate | 0.0290 | 1.29x | Phản biện đơn độc, thiếu câu Bác bỏ trong toàn bài |
| **2** | Evidence | *"To provide reasonings to my strong point, brings me back to..."* | Ineffective | Effective | 0.0004 | Effective | 0.0014 | 3.50x | Ngoại tại: Trích dẫn rỗng vào bài đọc (*"đoạn văn 36"*) |
| **3** | Position | *"I think you shouldn't join the Seagoing Cowboys"* | Ineffective | Adequate | 0.0221 | Adequate | 0.0096 | 0.43x | Ngoại tại: Khớp nối lập trường với bối cảnh đề bài |
| **4** | Counterclaim | *"Not allowing students to use there phones at all"* | Ineffective | Adequate | 0.0379 | Adequate | 0.0904 | 2.39x | Đoạn cụt cú pháp tại chỗ, thiếu mệnh đề liên kết |
| **5** | Position | *"The Driverless people can cause problems"* | Ineffective | Adequate | 0.0279 | Adequate | 0.1515 | 5.43x | Ngoại tại: Mâu thuẫn thông tin thực tế với bài đọc nguồn |
| **6** | Counterclaim | *"But Sometimes it could be a distraction from you doing all y..."* | Ineffective | Adequate | 0.0315 | Adequate | 0.0400 | 1.27x | Chuyển đoạn treo, không có luận điểm bác bỏ theo sau |
| **7** | Position | *"I reconsider that are principal should let us eight graders..."* | Ineffective | Adequate | 0.0347 | Adequate | 0.0970 | 2.80x | Ngoại tại: Xây dựng luận đề phụ thuộc vào phạm vi đề bài |
| **8** | Claim | *"Some kids will ask there parents to transfer school"* | Ineffective | Adequate | 0.0207 | Adequate | 0.1236 | 5.97x | Suy diễn thiếu căn cứ cục bộ; P(Ineff) tăng gấp 6.0 lần |
| **9** | Lead | *"The future is near and the talk about driverless cars is upo..."* | Ineffective | Adequate | 0.0446 | Adequate | 0.0802 | 1.80x | Ngoại tại: Mở bài chung chung cần đối chiếu với đề |
| **10** | Claim | *"Another cars is a bad idea is because of its gas"* | Ineffective | Adequate | 0.0392 | Adequate | 0.0315 | 0.80x | Lỗi cú pháp cục bộ nhưng thiếu tiền đề liên kết |

### 5.3 Tổng hợp chẩn đoán: Vì sao không có ca nào lật nhãn argmax?
Trên cả 10 ca lỗi, **0/10 ca lật sang nhãn dự báo Ineffective theo luật quyết định argmax**. Tuy nhiên, 8/10 ca ghi nhận sự gia tăng về khối lượng xác suất P(Ineffective), với tỷ lệ tăng xác suất trung bình đạt 2.57 lần (trung vị đạt 2.10 lần), trong khi 2 ca (Ca 3 và Ca 10) bị giảm nhẹ.

*Ghi chú phương pháp luận về hiện tượng hồi quy về giá trị trung bình (Regression to the Mean):* Vì 10 ca này được chọn ra từ những ca lỗi nặng nề nhất (tự tin sai nhất) của Level 0, việc đánh giá lại tất yếu chịu tác động của hiện tượng hồi quy thống kê. Tuy nhiên, dưới góc độ ngôn ngữ học, nguyên nhân sâu xa khiến ngữ cảnh cục bộ không thể giúp mô hình lật nhãn gồm có:
1. **Sự phụ thuộc vào văn bản nguồn của đề bài (Các ca 2, 5):** Ở Ca 2, học sinh viết *"để chứng minh cho quan điểm của em, hãy xem đoạn văn 36"*. Người chấm đánh giá là Ineffective vì họ đã đọc văn bản đề bài và biết bài đọc không hề có đoạn 36 hoặc đoạn đó không liên quan. Mô hình DeBERTa hoàn toàn không được cung cấp bài đọc nguồn; do đó câu văn có cấu trúc trích dẫn dẫn chứng rất chuẩn mực và bị đoán nhầm là Effective. Ở Ca 5, câu văn mâu thuẫn trực tiếp với thông tin trong bài đọc về xe tự lái.
2. **Cấu trúc nghị luận toàn bài (Các ca 1, 6):** Một câu Phản biện (Counterclaim) bị chấm Kém khi người viết bỏ quên không đưa ra câu Bác bỏ (Rebuttal) ở bất kỳ đâu trong bài. Việc chỉ mở rộng thêm đúng một câu đứng trước và một câu đứng sau không thể giúp mô hình kiểm tra xem đoạn cuối bài học sinh có bác bỏ luận điểm đó hay không.
3. **Kết luận cho Câu hỏi 1:** Ngữ cảnh cục bộ lân cận giúp mô hình tăng mức độ nghi ngờ (tăng xác suất P(Ineffective) ở 8/10 ca), nhưng **không thể lật nhãn dự báo cuối cùng** đối với những câu văn có khiếm khuyết phụ thuộc vào kiến thức ngoại tại của đề bài hoặc tính liên kết xuyên suốt toàn bài.

---

## 6. Đánh giá khả năng tổng quát hóa trên đề bài mới (Leave-One-Prompt-Out - LOPO)

### 6.1 Cơ sở thực tiễn
Quy trình kiểm định chéo nội miền thông thường cho phép mô hình tận dụng các tương quan từ vựng đặc thù của đề bài. Trong môi trường triển khai giáo dục thực tế, hệ thống AWE bắt buộc phải đánh giá **các đề bài hoàn toàn mới** do giáo viên giao. Thí nghiệm Leave-One-Prompt-Out (LOPO) đảm bảo nguyên tắc không có bất kỳ sự trùng lặp nào về đề bài giữa tập huấn luyện và tập đánh giá.

### 6.2 Đánh giá mô hình cổ điển trên 15 đề bài (Random Forest, Bộ đặc trưng B)

Nhóm đã huấn luyện và đánh giá 15 mô hình Random Forest độc lập (n_estimators=150, max_depth=35, Bộ đặc trưng B: TF-IDF unigram/bigram, one-hot vai trò lập luận, độ dài token). Trong mỗi fold, mô hình học trên 14 đề và đánh giá trên đề bài duy nhất bị giữ lại:

| Tên đề bài giữ lại đánh giá | Số đơn vị test (N) | Số bài văn test (N) | LOPO Macro-F1 | Độ chính xác tổng thể (%) | F1 lớp Kém | Recall lớp Kém | Tầng độ khó |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| *"A Cowboy Who Rode the Waves"* | 5.158 | 688 | **0.3501** | 79.20% | 0.1085 | 0.1279 | **Khó nhất (Hạng 1/15)** |
| *Community service* | 6.461 | 768 | **0.3803** | 71.55% | 0.1181 | 0.0906 | Khó (Hạng 2/15) |
| *Car-free cities* | 8.368 | 983 | **0.3877** | 76.09% | 0.0326 | 0.0242 | Khó (Hạng 3/15) |
| *The Face on Mars* | 7.229 | 819 | **0.4009** | 75.03% | 0.1479 | 0.1566 | Khó (Hạng 4/15) |
| *Driverless cars* | 12.628 | 1.386 | **0.4117** | 78.31% | 0.0584 | 0.0684 | Trung bình (Hạng 5/15) |
| *Does the electoral college work?* | 16.840 | 1.818 | **0.4172** | 68.66% | 0.1258 | 0.0859 | Trung bình (Hạng 6/15) |
| *Grades for extracurricular activities* | 6.122 | 815 | **0.4235** | 81.43% | 0.0956 | 0.0890 | Trung bình (Hạng 7/15) |
| *Summer projects* | 9.855 | 875 | **0.4339** | 70.24% | 0.0000 | 0.0000 | **Trung vị (Hạng 8/15)** |
| *Seeking multiple opinions* | 14.562 | 1.544 | **0.4442** | 77.13% | 0.0412 | 0.0763 | Trung bình (Hạng 9/15) |
| *Exploring Venus* | 7.252 | 928 | **0.4451** | 72.99% | 0.1279 | 0.0869 | Trung bình (Hạng 10/15) |
| *Cell phones at school* | 7.074 | 829 | **0.4473** | 87.23% | 0.1235 | 0.0901 | Trung bình (Hạng 11/15) |
| *Facial action coding system* | 9.175 | 1.103 | **0.4612** | 78.10% | 0.1015 | 0.0641 | Trung bình (Hạng 12/15) |
| *Phones and driving* | 6.584 | 700 | **0.4697** | 83.55% | 0.0292 | 0.0286 | Trung bình (Hạng 13/15) |
| *Mandatory extracurricular activities* | 8.455 | 839 | **0.4802** | 78.76% | 0.0760 | 0.0505 | Trung bình (Hạng 14/15) |
| *Distance learning* | 18.526 | 1.498 | **0.5014** | 78.05% | 0.0649 | 0.0433 | **Dễ nhất (Hạng 15/15)** |

> **Thống kê tổng hợp trên toàn bộ 15 đề bài (Mô hình Random Forest cổ điển):**  
> **Macro-F1 trung bình:** **0.4303 ± 0.0405** &nbsp;|&nbsp; **Độ chính xác trung bình không trọng số:** **77.09%** &nbsp;|&nbsp; **Độ chính xác trung bình có trọng số:** **76.47%**

### 6.3 Phân tích khoảng cách tổng quát hóa đề bài
* **Hiệu năng nội miền so với ngoại đề:**
  - Mô hình Random Forest thẩm định nội miền (Tuần 9): Macro-F1 = 0.5230 (khi trộn lẫn 15 đề).
  - Mô hình Random Forest ngoại đề (trung bình 15-fold LOPO): Macro-F1 = 0.4303.
  - Khoảng cách sụt giảm hiệu năng tổng quát hóa cổ điển: -0.0927 điểm (-17.72% tương đối).
* **Đề bài đọc hiểu văn học phụ thuộc ngữ liệu so với Đề bài nghị luận xã hội:**
  - Đề bài khó nhất là *"A Cowboy Who Rode the Waves"* (Macro-F1 = 0.3501), một đề bài yêu cầu học sinh đọc một đoạn trích văn học cụ thể. Tên nhân vật và các chi tiết trích dẫn không thể học chuyển giao từ các đề bài khác.
  - Đề bài dễ nhất là *"Distance learning"* (Macro-F1 = 0.5014), nơi học sinh sử dụng vốn từ vựng nghị luận mang tính phổ quát (*"tính linh hoạt"*, *"kỹ năng xã hội"*), giúp mô hình chuyển giao rất thuận lợi.

---

### 6.4 Đánh giá LOPO với Mô hình Học sâu: DeBERTa-v3 so với Random Forest Cổ điển

Nhóm đã tinh chỉnh mới hoàn toàn mô hình `microsoft/deberta-v3-base` trên 3 đề bài đại diện bao trùm toàn bộ dải độ khó được phân loại bởi Random Forest:
1. **Tầng Khó nhất (Hạng 1/15):** *"A Cowboy Who Rode the Waves"* (5.158 đơn vị test trên 688 bài văn).
2. **Tầng Trung vị (Hạng 8/15):** *Summer projects* (9.855 đơn vị test trên 875 bài văn).
3. **Tầng Dễ nhất (Hạng 15/15):** *Distance learning* (18.526 đơn vị test trên 1.498 bài văn).

| Tầng độ khó | Tên đề bài giữ lại kiểm tra | Số đơn vị test (N) | Số bài văn test (N) | Macro-F1 RF | Macro-F1 DeBERTa | Chênh lệch Macro-F1 | Độ chính xác RF | Độ chính xác DeBERTa | F1 Kém RF | F1 Kém DeBERTa |
|---|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Khó nhất (Hạng 1/15)** | *"A Cowboy Who Rode the Waves"* | 5.158 | 688 | 0.3501 | **0.4082** | **+0.0581** | 79.20% | 78.87% | 0.1085 | **0.1246** |
| **Trung vị (Hạng 8/15)** | *Summer projects* | 9.855 | 875 | 0.4339 | **0.4642** | **+0.0303** | 70.24% | 66.58% | 0.0000 | **0.0759** |
| **Dễ nhất (Hạng 15/15)** | *Distance learning* | 18.526 | 1.498 | 0.5014 | **0.5735** | **+0.0721** | 78.05% | 75.55% | 0.0649 | **0.2509** |

> **Tổng hợp trên 3 đề bài đại diện:**  
> **Macro-F1 trung bình của DeBERTa:** **0.4820** so với **Random Forest cổ điển:** **0.4285** (Mức tăng Macro-F1: **+0.0535 điểm**, **+12.49%** tương đối)

#### Đo lường chuẩn xác khoảng cách tổng quát hóa (Nội miền so với LOPO trên cùng một đề bài):
Bằng cách so sánh DeBERTa chạy LOPO với hiệu năng của DeBERTa nội miền được đo trên *đúng tập con của đề bài đó*, nhóm cô lập được khoảng cách suy giảm thực tế khi chuyển sang đề mới:

| Tên đề bài giữ lại kiểm tra | Số đơn vị Val nội miền (N) | Macro-F1 DeBERTa Nội miền | Macro-F1 DeBERTa LOPO | Khoảng cách tổng quát hóa thực | Mức dịch chuyển tương đối (%) |
|---|:---:|:---:|:---:|:---:|:---:|
| *"A Cowboy Who Rode the Waves"* | 1.030 | 0.4462 | 0.4082 | **-0.0380 điểm** | -8.52% |
| *Summer projects* | 2.074 | 0.4695 | 0.4642 | **-0.0053 điểm** | -1.12% |
| *Distance learning* | 3.533 | 0.5677 | 0.5735 | **+0.0058 điểm** | +1.03% |
| **Trung bình trên 3 đề bài** | 6.637 | **0.4945** | **0.4820** | **-0.0125 điểm** | **-2.53%** |

*Các phát hiện trọng tâm:*
1. **Ưu thế Macro-F1 của DeBERTa:** DeBERTa đạt điểm Macro-F1 vượt trội hơn Random Forest trên cả 3 đề kiểm tra (+0.0581 ở Cowboy, +0.0303 ở Summer, +0.0721 ở Distance learning), chủ yếu nhờ khả năng nhận diện lớp thiểu số Ineffective tốt hơn hẳn.
2. **Sự đánh đổi về độ chính xác (Accuracy):** Do sử dụng trọng số phạt mất cân bằng nhằm cứu vớt các ca Ineffective, độ chính xác tổng thể của DeBERTa thấp hơn một chút so với Random Forest trên cả 3 đề (Cowboy: 78.87% so với 79.20%; Summer: 66.58% so với 70.24%; Distance: 75.55% so với 78.05%).
3. **Mức độ sụt giảm ngoại đề thực tế:** Khi so sánh trực tiếp trên cùng một đề bài, mức sụt giảm hiệu năng thực tế của DeBERTa khi chuyển sang đề mới chỉ ở mức khiêm tốn (-2.53% trung bình). Điều này chứng minh biểu diễn ngữ nghĩa của DeBERTa có tính chuyển giao rất tốt đối với các chủ đề mở, trong khi các đề bài văn học chịu thiệt thòi do từ vựng văn bản nguồn chưa từng xuất hiện trong tập huấn luyện.

---

### 6.5 Mức độ nhạy cảm của các loại đơn vị lập luận khi gặp đề bài mới

Đánh giá sự biến thiên hiệu năng trên toàn bộ 7 loại đơn vị lập luận qua 3 fold LOPO (N = 33.539 đơn vị) chỉ ra các nhóm mức độ nhạy cảm rõ rệt:

| Phân tầng nhạy cảm | Loại đơn vị lập luận | Số đơn vị đánh giá (N) | Số đơn vị Kém (N) | Macro-F1 Nội miền | Macro-F1 TB LOPO | Độ lệch hiệu năng | Tỷ lệ sụt giảm tương đối (%) | F1 Kém LOPO |
|---|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Nhạy cảm cao (Giảm mạnh)** | **Rebuttal (Bác bỏ)** | 1.441 | 23 | 0.5383 | 0.4156 | -0.1227 điểm | -22.79% | 0.0904 |
|  | **Evidence (Dẫn chứng)** | 9.716 | 323 | 0.6270 | 0.5056 | -0.1214 điểm | -19.36% | 0.1859 |
|  | **Concluding Statement (Kết luận)** | 2.839 | 32 | 0.5980 | 0.4835 | -0.1145 điểm | -19.14% | 0.1439 |
| **Nhạy cảm trung bình** | **Lead (Mở đầu / Dẫn dắt)** | 2.244 | 46 | 0.5567 | 0.4844 | -0.0723 điểm | -12.98% | 0.1171 |
|  | **Counterclaim (Phản biện)** | 1.893 | 26 | 0.4796 | 0.4179 | -0.0617 điểm | -12.87% | 0.0871 |
|  | **Claim (Luận điểm)** | 12.391 | 98 | 0.5126 | 0.4517 | -0.0609 điểm | -11.87% | 0.1305 |
| **Tính bền vững cao (Ít suy giảm)** | **Position (Lập trường / Luận đề)** | 3.015 | 36 | 0.5639 | 0.5061 | -0.0578 điểm | -10.26% | 0.1425 |

#### Các yếu tố ngôn ngữ học giải thích sự phân tầng nhạy cảm:
*Lưu ý về quy mô mẫu:* Trên 3 fold, số lượng đơn vị Ineffective rất khan hiếm (chỉ có 23 đơn vị Rebuttal, 26 đơn vị Counterclaim, 32 đơn vị Concluding Statement). Do đó, sự khác biệt giữa mức -22.8% và -19.1% có thể nằm trong biên độ dao động ngẫu nhiên, nhưng bức tranh phân tầng lớn là hoàn toàn rõ rệt:
1. **Các đơn vị phụ thuộc văn bản nguồn và quan hệ lập luận bị suy giảm nặng nề nhất:**
   - **`Evidence` (Dẫn chứng) và `Rebuttal` (Bác bỏ)** chịu mức giảm tương đối lớn nhất (~19% đến 23%). Các đơn vị Dẫn chứng phụ thuộc trực tiếp vào bài đọc đi kèm của đề, các số liệu trích dẫn và thuật ngữ chuyên biệt của chủ đề. Khi sang một đề mới, các thực thể lạ khiến mô hình mất tự tin phân loại. Đơn vị Bác bỏ đòi hỏi phải bám sát vào việc phản hồi lại các lập luận riêng của đề bài đó.
2. **Các đơn vị nêu lập trường mang tính tự lập thể hiện tính bền vững cao:**
   - **`Position` (Lập trường / Luận đề)** là loại đơn vị lập luận kiên cường nhất trước đề bài mới (bảo toàn được ~89.7% hiệu năng nội miền). Việc phát biểu lập trường thường dựa vào các cấu trúc tu từ mang tính phổ quát (*"tôi tin rằng"*, *"theo quan điểm của tôi"*, *"không nên được cho phép"*), những cấu trúc này chuyển giao hoàn hảo sang bất kỳ chủ đề nghị luận nào.

---

## 7. Tổng hợp sư phạm & Giải đáp các câu hỏi lý thuyết

### 7.1 Khung giả thuyết: Thứ bậc thông tin cần thiết trong chấm điểm lập luận
Từ các quan sát thực nghiệm, nhóm đề xuất một **Khung giả thuyết thứ bậc thông tin (Hypothetical Information Hierarchy)** mô tả các tầng dữ liệu cần thiết cho việc đánh giá tự động:

```
Thứ bậc thông tin giả định trong đánh giá viết tự động:
[Level 0: Đơn vị cô lập]           --> Đủ nhận diện cấu trúc tu từ cơ bản (Đa số lớp Đạt yêu cầu)
[Level 1: Đơn vị lân cận kế tiếp]   --> Hỗ trợ các đơn vị quan hệ (Claim tăng +0.043 F1, Counterclaim +0.030 F1)
[Level 2: Văn bản đọc nguồn của đề] --> Tầng thông tin giả thuyết cần để xác minh tính chuẩn xác của Evidence
[Level 3: Ngữ cảnh toàn bài viết]   --> Tầng thông tin giả thuyết cần để kiểm tra tính nhất quán của Position & Counterclaim
```

*Trạng thái kiểm chứng:* Tầng Level 0 và Level 1 đã được kiểm chứng thực nghiệm đầy đủ trong nghiên cứu này. Tầng Level 2 và Level 3 là các giả thuyết khoa học có cấu trúc, chờ được kiểm chứng trong các nghiên cứu tương lai khi tích hợp văn bản đọc nguồn và cơ chế chú ý toàn bài dạng phân cấp (hierarchical document attention).

### 7.2 Trực tiếp giải đáp các câu hỏi cốt lõi của Giảng viên

#### Câu hỏi 1: *Trong 10 ca Ineffective, ca nào được đoán đúng nếu thấy đoạn văn xung quanh?*
- **Kết quả thực nghiệm:** **0/10 ca lật sang nhãn Ineffective argmax**, nhưng xác suất P(Ineffective) tăng ở 8/10 ca (tăng trung bình gấp 2.57 lần, trung vị 2.10 lần).
- **Lý giải bản chất:** Các lỗi này mang tính **ngoại tại (extrinsic)**: Ca 2 ("đoạn văn 36") và Ca 5 cần bài đọc nguồn của đề bài để kiểm tra tính xác thực; Ca 1 và Ca 6 cần duyệt toàn bộ bài văn để xác nhận tác giả có viết đoạn Bác bỏ hay không. Ngữ cảnh cục bộ chỉ làm tăng mức độ nghi ngờ của mô hình chứ không đủ cơ sở thông tin để lật nhãn.

#### Câu hỏi 2: *Với một đề mới, Macro-F1 giảm nhiều nhất ở loại đơn vị nào?*
- **Kết quả thực nghiệm:** Các đơn vị phụ thuộc chặt chẽ vào nội dung đọc hiểu như **`Rebuttal` (sụt giảm -22.79%)** và **`Evidence` (sụt giảm -19.36%)** chịu mức giảm mạnh nhất. Ngược lại, **`Position` bền vững nhất (chỉ giảm -10.26%)** nhờ khuôn mẫu tu từ mang tính phổ quát giữa các đề tài.

#### Câu hỏi chuẩn bị phỏng vấn: *Nếu người chấm thấy đề và cả bài còn mô hình chỉ thấy một đoạn, ta có thể quy lỗi cho năng lực mô hình đến đâu?*
- **Trực tiếp trả lời:** Dữ liệu thực nghiệm của nhóm chứng minh rằng **không thể quy phần lớn lỗi cho năng lực phân loại câu của mô hình**. Khi được bổ sung ngữ cảnh lân cận (Level 1), điểm F1 lớp Kém chỉ tăng nhẹ +0.0193 điểm và không có ca nào trong 10 ca lỗi cực đoan lật được nhãn. Điều này chứng minh trần hiệu năng của mô hình hiện bị giới hạn bởi **sự thiếu hụt thông tin đầu vào (văn bản nguồn đề bài và liên kết toàn bài)** chứ không phải do mô hình thiếu tham số hay học kém. Muốn khắc phục các lỗi này, hệ thống bắt buộc phải được cung cấp bài đọc nguồn (source reading passage) và kiến trúc mô hình hóa toàn bài.

---

## 8. Hiện vật tái lập thực nghiệm & Quản trị mã nguồn

Toàn bộ các tệp mã nguồn và sổ tay Jupyter đã được chuẩn hóa, dọn dẹp các ghi chú không chính thức và thiết lập hạt giống ngẫu nhiên cố định (seed 42):

### 8.1 Cấu trúc mã nguồn module & Liên kết Google Colab tương tác

* **Notebook 04 — Khảo sát Confound Độ dài & Benchmark LOPO Cổ điển:**
  - **Liên kết Colab:** [Mở Script 04 trên Google Colab](https://colab.research.google.com/drive/1YRMpJgGzZ0vWe7nA0W8c7n5JKMruVJHT?usp=sharing)  
  - **URL đầy đủ:** `https://colab.research.google.com/drive/1YRMpJgGzZ0vWe7nA0W8c7n5JKMruVJHT?usp=sharing`
  - **Tệp cục bộ:** `04_Length_Confound_and_LOPO.py` / `04_length_confound_and_lopo_classical.ipynb`
  - **Nhiệm vụ:** Phân tích 4 phân vị độ dài (N = 29.102 đơn vị validation) và kiểm định chéo 15-fold Random Forest LOPO.
  - **Thời gian chạy:** CPU / khoảng 15 phút.

* **Notebook 05 — Thí nghiệm Triệt tiêu Ngữ cảnh có kiểm soát (Level 0 so với Level 1 DeBERTa):**
  - **Liên kết Colab:** [Mở Script 05 trên Google Colab](https://colab.research.google.com/drive/1prcSnRHax0SAITnUbGsXks3aQ9pbwJD2?usp=sharing)  
  - **URL đầy đủ:** `https://colab.research.google.com/drive/1prcSnRHax0SAITnUbGsXks3aQ9pbwJD2?usp=sharing`
  - **Tệp cục bộ:** `05_Context_Ablation_DeBERTa.py` / `05_context_ablation_deberta.ipynb`
  - **Nhiệm vụ:** Đánh giá so sánh Level 0 và Level 1 trên 29.102 đơn vị, phân rã 7 loại lập luận và rà soát 10 ca lỗi.
  - **Thời gian chạy:** GPU (Colab T4 / V100 / RTX) / khoảng 75 phút.

* **Notebook 06 — Đánh giá Khả năng Tổng quát hóa Ngoại đề LOPO (DeBERTa-v3):**
  - **Liên kết Colab:** [Mở Script 06 trên Google Colab](https://colab.research.google.com/drive/1xiYMZ7SjRSAn_ioAvAbNh-PZDkghsiBk?usp=sharing)  
  - **URL đầy đủ:** `https://colab.research.google.com/drive/1xiYMZ7SjRSAn_ioAvAbNh-PZDkghsiBk?usp=sharing`
  - **Tệp cục bộ:** `06_LOPO_DeBERTa.py` / `06_lopo_deberta.ipynb`
  - **Nhiệm vụ:** Tinh chỉnh DeBERTa-v3 trên 3 tầng đề bài đại diện (Cowboy, Summer projects, Distance learning) với 14 đề/fold, đo lường khoảng cách tổng quát hóa và phân tích mức độ nhạy cảm của 7 loại đơn vị lập luận.
  - **Thời gian chạy:** GPU (Colab T4 / A100) / khoảng 1.5 – 2.0 giờ mỗi fold.

### 8.2 Quy chuẩn kiểm tra môi trường thực thi
Toàn bộ các đường ống đều tự động kiểm tra tính sẵn sàng của CUDA, bảo toàn kiểu chuỗi cho các mã định danh, cố định bảng ánh xạ từ điển `LABEL2ID` và ghi nhật ký thực thi đầy đủ vào thư mục `outputs/`.

---

## 9. Danh mục tài liệu tham khảo

* **Crossley, S. A., Baffour, P., Tian, Y., Franklin, A., Benner, M., & Boser, U. (2024).** A large-scale corpus for assessing written argumentation: PERSUADE 2.0. *Assessing Writing*, 61, Article 100830. [DOI: 10.1016/j.asw.2024.100830].
* **He, P., Gao, J., & Chen, W. (2023).** DeBERTaV3: Improving DeBERTa using ELECTRA-style pre-training with gradient-disentangled embedding sharing. *International Conference on Learning Representations (ICLR)*.
* **Newell, G. E., Beach, R., Smith, J., & VanDerHeide, J. (2011).** Teaching and learning argumentative writing: An integrative review. *Reading Research Quarterly*, 46(3), 273–304.
* **Stab, C., & Gurevych, I. (2014).** Identifying argumentative discourse structures in persuasive essays. *Conference on Empirical Methods in Natural Language Processing (EMNLP)*, 46–56.
* **Stab, C., & Gurevych, I. (2017).** Parsing argumentation structures in persuasive essays. *Computational Linguistics*, 43(3), 619–659.
* **Toulmin, S. E. (1958).** *The Uses of Argument*. Cambridge University Press.
