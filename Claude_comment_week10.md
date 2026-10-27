# Rà soát lỗi báo cáo Tuần 10 – Nhóm 06

Oct 25, 2026 · @bvhdz

## Thống kê

Bản PDF 17 trang (Group06_CLC02_Week10_Report.pdf) có 34 lỗi, trong đó 12 lỗi nghiêm trọng cần sửa trước khi nộp. Nhóm D (kết luận vượt bằng chứng) nhiều lỗi nhất; nhóm A (trình bày PDF) là việc thầy yêu cầu sửa đầu tiên.

| Nhóm     | Nội dung                                      | Nghiêm trọng | Trung bình | Nhẹ   | Tổng   |
| -------- | --------------------------------------------- | ------------ | ---------- | ----- | ------ |
| A        | Trình bày PDF                                 | 4            | 2          | 1     | 7      |
| B        | Thiếu so với yêu cầu của thầy                 | 3            | 3          | 2     | 8      |
| C        | Số liệu sai hoặc không khớp                   | 1            | 3          | 2     | 6      |
| D        | Kết luận vượt bằng chứng, phương pháp chưa đủ | 4            | 8          | 1     | 13     |
| **Tổng** |                                               | **12**       | **16**     | **6** | **34** |

Cách xếp mức độ:

- **Nghiêm trọng:** thầy đã nêu đích danh trong nhận xét Tuần 9, hoặc làm sai một con số/kết luận chính của báo cáo.
- **Trung bình:** làm yếu lập luận hoặc gây hiểu nhầm, nhưng không làm sai kết quả chính.
- **Nhẹ:** chi tiết trình bày hoặc thuật ngữ.

12 lỗi nghiêm trọng: A1, A2, A5, A7, B1, B2, B4, C1, D1, D3, D9, D12.

## Nhóm A – Trình bày PDF (7 lỗi)

Đây là việc ưu tiên số 1 trong nhận xét Tuần 9 ("Sửa PDF"), nhưng bản Tuần 10 còn lỗi nặng hơn bản trước.

**A1 · Số và ký hiệu bị in hai lần** — gần như mọi trang · Nghiêm trọng

- Lỗi: mọi thứ viết trong \$...\$ hiện hai lần, ví dụ "22%22%", "0.37410.3741", "29, 10229, 102", "(3, 1193, 119 essays)", "κκ", "ΔΔ", "(NN)".
- Vì sao sai: đây đúng là lỗi "6.13%6.13%" thầy đã chỉ ra. Nguyên nhân là KaTeX vẽ cả bản MathML lẫn bản HTML khi file CSS katex.min.css không được nạp lúc xuất PDF. Người đọc không biết số nào là số thật.
- Sửa: bỏ \$...\$ cho số thường, chỉ giữ math cho công thức thật. Nếu vẫn dùng math thì nạp CSS của KaTeX khi xuất.

**A2 · Lỗi in đôi làm sai nghĩa cấu hình** — trang 6, 16, 17 · Nghiêm trọng

- Lỗi: "batch size 3232 (88 per device ×× 44)", "33 epochs", "seeds (4242)", "trains DeBERTa-v3 on 1414 prompts".
- Vì sao sai: người đọc lướt sẽ hiểu là 33 epoch, seed 4242, 1414 đề. Đây là thông tin tái lập thí nghiệm, đọc sai thì không chạy lại được.
- Sửa: như A1, rồi đọc soát lại từng con số cấu hình.

**A3 · Công thức hiển thị xuất hiện hai lần** — trang 5, 6, 12, 13 · Trung bình

- Lỗi: dòng Error Rate (mục 3.1), trọng số class (4.1), công thức x_Level0/x_Level1 và các dòng Summary (mục 6) đều có một bản font serif và một bản chữ thường.
- Vì sao sai: cùng nguyên nhân với A1; làm báo cáo trông chưa soát.
- Sửa: như A1.

**A4 · Sơ đồ pipeline dữ liệu bị mất** — trang 4 · Trung bình

- Lỗi: sơ đồ Mermaid ở mục 2.1 chỉ còn một ô trống.
- Vì sao sai: trình xuất PDF không hiểu khối Mermaid. Mục 2.1 nói "the filtering flow aligns with our canonical protocol" nhưng người đọc không thấy flow nào.
- Sửa: xuất sơ đồ thành ảnh PNG/SVG rồi chèn vào.

**A5 · PDF không có lớp chữ và không có link bấm được** — toàn file · Nghiêm trọng

- Lỗi: file tạo bằng Microsoft Print to PDF. Kiểm tra cho thấy không trích được chữ nào và có 0 link. Ba link Colab chỉ là ảnh.
- Vì sao sai: thầy yêu cầu link notebook, nhưng thầy phải gõ tay chuỗi ID dài mới mở được. Thầy cũng không copy hay tìm kiếm được số liệu. File nặng 4,9 MB cũng vì mỗi trang là ảnh.
- Sửa: xuất bằng "Save as PDF" của Chrome/Edge, hoặc pandoc. Xuất xong thì bôi đen thử một đoạn chữ và bấm cả ba link.

**A6 · Bảng bị vỡ bố cục** — trang 9–11 · Nhẹ

- Lỗi: bảng 10 ca lỗi kéo dài 2 trang vì cột trích đoạn quá hẹp (mỗi dòng 2–3 chữ). Trang 11 gần như trắng vì bảng LOPO bị đẩy sang trang sau.
- Vì sao sai: khó đọc, khó đối chiếu các ca với nhau.
- Sửa: nới rộng cột trích đoạn, bỏ bớt cột hoặc chia thành hai bảng.

**A7 · Câu khẳng định "đã sửa KaTeX" trái với thực tế** — trang 4 · Nghiêm trọng

- Lỗi: mục 1.4 viết _"All KaTeX mathematical formulations have been validated; duplicated text artifacts … have been eliminated"_.
- Vì sao sai: ngay trong cùng bản PDF có hàng trăm lỗi in đôi (A1–A3). Khẳng định sai về chính báo cáo làm thầy mất tin vào các khẳng định khác.
- Sửa: xóa câu này. Không cần liệt kê những gì "đã sửa", chỉ cần sửa thật.

## Nhóm B – Thiếu so với yêu cầu của thầy (8 lỗi)

Nhận xét Tuần 9 đặt điều kiện "xong" là: PDF đã sửa, macro-F1 khớp confusion matrix, nguồn kappa đúng và kết luận đã bỏ suy luận vượt bằng chứng. Hai trong ba điều kiện (confusion matrix, nguồn kappa) chưa đạt.

**B1 · Không có confusion matrix nào** — trang 7, 12 · Nghiêm trọng

- Lỗi: cả báo cáo chỉ có bảng F1 theo lớp, không có ma trận nhầm lẫn cho Level 0, Level 1, RF hay LR.
- Vì sao sai: việc ưu tiên số 1 của thầy là "tái lập macro-F1 từ confusion matrix cùng cohort". Macro-F1 bằng trung bình ba F1 lớp (đã kiểm, khớp), nhưng không có ma trận thì thầy không kiểm được F1 từng lớp có đúng không. Đây cũng là cách duy nhất để chứng minh lỗi 6,13% đã được sửa.
- Sửa: thêm ma trận cho Level 0, Level 1, RF và LR trên cùng 29.102 đơn vị, kèm một dòng tính lại macro-F1 từ ma trận.

**B2 · Trích dẫn PERSUADE 2.0 sai** — trang 3, 17 · Nghiêm trọng

- Lỗi: báo cáo ghi "Crossley, Tian & McNamara (2024), _The PERSUADE 2.0 Corpus: An English writing corpus with discourse and quality annotations_, Assessing Writing 60, Article 100830". Bài thật có tên _A large-scale corpus for assessing written argumentation: PERSUADE 2.0_ (Crossley và cộng sự, Assessing Writing tập 61).
- Vì sao sai: thầy yêu cầu "kiểm đúng nguồn kappa". Khi tên bài, tác giả và số tập đều sai thì "Table 3, p. 8" và con số κ = 0,316 cũng chưa đáng tin, vì có thể nhóm chưa mở bài gốc.
- Sửa: lấy DOI và danh sách tác giả đầy đủ từ trang nhà xuất bản, mở bài gốc, kiểm lại từng con số kappa theo loại đơn vị và số trang/bảng.

**B3 · Giải thích lỗi 6,13% viết chung cho cả nhóm** — trang 3 · Trung bình

- Lỗi: mục 1.2 có tiêu đề "Unified Verbal Explanation" và "Consensus … (Unified Across All 3 Members)".
- Vì sao sai: thầy yêu cầu "mỗi thành viên phải tự giải thích được lỗi 6,13% bằng lời của mình". Một đoạn chung cho thấy nhóm hiểu yêu cầu thành "học thuộc cùng một đoạn". Phần interview cá nhân chiếm 30% điểm cuối kỳ.
- Sửa: bỏ chữ "Unified/Consensus". Báo cáo chỉ cần nêu nguyên nhân; mỗi người tự chuẩn bị cách giải thích riêng.

**B4 · Giải thích 6,13% chứa hai cơ chế mâu thuẫn** — trang 3 · Nghiêm trọng

- Lỗi: ý 1–2 nói mô hình thật sự sụp đổ ("đoán tràn lan Ineffective, recall 98,7%", accuracy rơi xuống ~4,5%). Ý 3 nói lỗi là do lấy nhầm cột vì thứ tự nhãn của scikit-learn.
- Vì sao sai: hai cơ chế không thể cùng đúng. Nếu lỗi là lấy nhầm cột thì mô hình không hề sụp đổ: chính LR đó, vẫn class_weight='balanced', sau khi sửa ánh xạ đạt BA 60,32%. Thầy đã ghi nhận nguyên nhân là thứ tự nhãn, nên ý 1–2 vừa thừa vừa sai. Nếu một thành viên trả lời theo ý 1 trong interview sẽ bị hỏi vặn.
- Sửa: chỉ giữ cơ chế thứ tự nhãn, chứng minh bằng hai confusion matrix trước và sau khi sửa.

**B5 · Vẫn so mô hình ngang người** — trang 4 · Trung bình

- Lỗi: mục 1.4 thay "fully competitive with human agreement" bằng "approaches the numerical range of human inter-rater agreement".
- Vì sao sai: thầy nói κ mô hình–nhãn và κ người–người không cùng một đại lượng. Câu mới vẫn đặt hai con số cạnh nhau để so, chỉ đổi cách nói. Nó còn mâu thuẫn với mục 1.1, nơi nhóm đã rút lại mọi so sánh ngang người.
- Sửa: xóa câu này.

**B6 · Chưa trả lời câu hỏi chuẩn bị của thầy** — không có trong báo cáo · Trung bình

- Lỗi: thầy hỏi "Nếu người chấm thấy đề và cả bài còn mô hình chỉ thấy một đoạn, em có thể quy lỗi cho năng lực mô hình đến đâu?". Báo cáo không có đoạn nào trả lời trực tiếp.
- Vì sao sai: đây là câu thầy dặn mỗi người chuẩn bị. Thí nghiệm Level 1 chính là dữ liệu để trả lời, nhưng báo cáo không nối hai thứ lại.
- Sửa: thêm một đoạn ngắn. Ví dụ: thêm ngữ cảnh lân cận chỉ đổi Ineffective F1 thêm 0,019, nên chưa thể tách phần lỗi do mô hình với phần do thiếu thông tin cho đến khi thử thêm đề bài và toàn bài.

**B7 · Chưa ghi cấu hình sẽ khóa cho Official Test** — trang 4 · Nhẹ

- Lỗi: mục 1.3 hứa chấm Official Test một lần với cấu hình đã khóa, nhưng không nói đó là Level 0 hay Level 1, cũng không nói tiêu chí chọn.
- Vì sao sai: "khóa cấu hình" nghĩa là quyết định trước khi nhìn test. Không ghi ra thì không ai kiểm được là đã khóa.
- Sửa: ghi rõ mô hình, đầu vào, ngưỡng, seed sẽ dùng và tiêu chí chọn (ví dụ macro-F1 trên validation).

**B8 · Chưa nói rõ phạm vi phân đoạn gold** — không có trong báo cáo · Nhẹ

- Lỗi: thầy dặn "giữ phạm vi đoạn đã tách gold". Báo cáo làm đúng nhưng không nói ra.
- Vì sao sai: người đọc có thể hiểu nhầm là hệ thống tự tách đơn vị rồi mới chấm (end-to-end), khi đó kết quả thực tế sẽ thấp hơn.
- Sửa: thêm một câu ở phần dữ liệu: mọi kết quả dùng ranh giới đơn vị có sẵn trong dữ liệu.

## Nhóm C – Số liệu sai hoặc không khớp (6 lỗi)

Các số dưới đây được tính lại từ chính bảng trong báo cáo. Phần lớn số liệu khác đều khớp: macro-F1 Level 0/1, mean macro-F1 LOPO 0,4303 ± 0,0405, tổng 144.289 đơn vị của 15 đề, các % tương đối.

**C1 · Accuracy LOPO RF 70,43% không khớp bảng** — trang 2, 12 · Nghiêm trọng

- Lỗi: dòng tóm tắt ghi "Mean Macro-F1 = 0,4303 ± 0,0405 (Accuracy: 70,43%)".
- Vì sao sai: accuracy của 15 đề trong bảng nằm trong khoảng 68,66%–87,23%. Trung bình cộng là 77,09%, trung bình có trọng số theo số đơn vị là 76,47%. Không cách tính nào ra 70,43%. Con số này nằm ngay trong abstract.
- Sửa: tính lại từ file output và ghi rõ là trung bình cộng hay có trọng số.

**C2 · Số essay của cùng một đề lệch giữa hai bảng** — trang 12 và 13 · Trung bình

| Đề                          | Số đơn vị | Bảng RF (trang 12) | Mục 6.4 (trang 13) |
| --------------------------- | --------- | ------------------ | ------------------ |
| A Cowboy Who Rode the Waves | 5.158     | 664 essay          | 688 essay          |
| Summer projects             | 9.855     | 1.061 essay        | 875 essay          |
| Distance learning           | 18.526    | 2.162 essay        | 1.498 essay        |

- Vì sao sai: cùng một đề, cùng số đơn vị thì số essay phải bằng nhau. Lệch tới 664 essay cho thấy có một bảng đếm sai, hoặc hai bảng dùng hai tập dữ liệu khác nhau. Nếu là trường hợp sau thì phép so RF và DeBERTa không công bằng.
- Sửa: đếm lại essay_id duy nhất của mỗi đề trong cả hai notebook.

**C3 · Tóm tắt 10 ca lỗi sai** — trang 16 · Trung bình

- Lỗi: bảng 7.2 ghi P(Ineff) "tăng vọt gấp 1,8× đến 6,0×" và "tăng trung bình 3,2×".
- Vì sao sai: tính từ bảng 5.2, tỷ số Level 1 / Tuần 9 của 10 ca là 1,29 · 3,50 · 0,43 · 2,39 · 5,43 · 1,27 · 2,80 · 5,97 · 1,80 · 0,80. Ca 3 và ca 10 giảm; ca 1 và ca 6 chỉ tăng khoảng 1,3×. Trung bình cộng là 2,57×, trung bình nhân là 1,95×, không phải 3,2×.
- Sửa: ghi "8/10 ca tăng, 2 ca giảm, trung bình khoảng 2,6×" (hoặc dùng trung vị).

**C4 · Lẫn lộn chênh lệch tuyệt đối và tương đối** — trang 1, 2, 7, 8, 15 · Trung bình

- Lỗi: "+4,30%" cho Claim thực ra là +0,043 F1 (tuyệt đối); "+16,17%" là tương đối. Position ghi "−5,50%" trong văn bản nhưng "−15,13%" trong bảng.
- Vì sao sai: F1 0,266 → 0,309 có thể đọc thành "tăng 4,3%" hoặc "tăng 16,2%", người đọc không biết cái nào. Cùng một kết quả có hai con số khác nhau ở hai nơi.
- Sửa: chênh lệch tuyệt đối ghi bằng "điểm" (+0,043 hoặc +4,3 điểm), chỉ dùng "%" cho chênh lệch tương đối.

**C5 · Thuật ngữ "trained from scratch" sai** — trang 13 · Nhẹ

- Lỗi: "Each fold trained a fresh DeBERTa model from scratch".
- Vì sao sai: "from scratch" nghĩa là khởi tạo trọng số ngẫu nhiên. Nhóm thực ra fine-tune từ checkpoint đã pretrain microsoft/deberta-v3-base.
- Sửa: "fine-tuned a fresh copy of the pretrained checkpoint".

**C6 · Bài dài 8.811 từ chưa được kiểm** — trang 5 · Nhẹ

- Lỗi: Q4 trải từ 567 đến 8.811 từ.
- Vì sao sai: bài học sinh lớp 6–12 dài 8.811 từ là bất thường, có thể là lỗi dữ liệu (bài bị ghép, lặp). Một bài như vậy có nhiều đơn vị, đủ để làm lệch thống kê của Q4.
- Sửa: mở bài này ra xem; nếu lỗi thì ghi chú hoặc loại.

## Nhóm D – Kết luận vượt bằng chứng, phương pháp chưa đủ (13 lỗi)

Thầy kết thúc nhận xét Tuần 9 bằng yêu cầu bỏ "suy luận vượt bằng chứng". Nhóm D gom các chỗ báo cáo vẫn kết luận mạnh hơn dữ liệu cho phép.

### Độ dài bài (mục 3)

**D1 · Kết luận "resolved" khi chưa kiểm** — trang 1, 5–6 · Nghiêm trọng

- Lỗi: báo cáo kết luận lỗi tăng theo độ dài "primarily driven by" phân bố nhãn, và đặt tiêu đề là "Resolving Length Confounds".
- Vì sao sai: nhóm mới chỉ cho thấy phân bố nhãn khác nhau giữa các quartile, chưa tính lại tỷ lệ lỗi của mô hình theo quartile. Thầy bảo "xem tỷ lệ nhãn trước khi giải thích", tức là bước đầu, không phải bằng chứng cuối. Lập luận "lớp Ineffective thưa" còn mâu thuẫn số học: Ineffective ở Q4 chỉ 1,29%, nên dù đoán sai toàn bộ thì cũng chỉ góp tối đa khoảng 1,3 điểm trong mức lỗi 30%. Phần lỗi còn lại phải đến từ nhầm Adequate↔Effective (Effective chiếm 32,8% ở Q4) hoặc từ đoán thừa Ineffective.
- Sửa: tính tỷ lệ lỗi trong từng ô quartile × nhãn gold, kèm confusion matrix theo quartile. Sau đó chuẩn hóa: tính lỗi của Q4 nếu Q4 có phân bố nhãn giống Q1. Nếu khoảng cách 22%→30% biến mất thì giả thuyết B mới được ủng hộ. Đổi tiêu đề thành "Examining".

**D2 · "Competent writers write longer essays" không có số liệu** — trang 6 · Trung bình

- Lỗi: mục 3.4 ý 2 khẳng định độ dài bài gắn với năng lực học sinh.
- Vì sao sai: đây là khẳng định nhân quả không có dữ liệu đi kèm. Trong khi PERSUADE 2.0 có sẵn điểm holistic cho từng bài, nên kiểm được trực tiếp.
- Sửa: thêm điểm holistic trung bình theo quartile vào bảng 3.2.

### Thí nghiệm ngữ cảnh (mục 4)

**D3 · Không có khoảng tin cậy, chỉ một seed** — trang 7 · Nghiêm trọng

- Lỗi: macro-F1 tăng +0,0022, Ineffective F1 tăng +0,0193, nhưng chỉ chạy một seed và không có CI.
- Vì sao sai: fine-tune DeBERTa với seed khác thường làm macro-F1 dao động cỡ ±0,01, lớn hơn chính mức tăng +0,0022. Tuần 9 nhóm đã có CI cho DeBERTa so với RF (thầy khen điểm này), nên Tuần 10 thiếu là bước lùi.
- Sửa: paired bootstrap theo essay trên cùng 29.102 đơn vị (Level 0 và Level 1). Nếu có thời gian, chạy ≥3 seed và báo trung bình ± độ lệch.

**D4 · Mức "cải thiện" thực chất chỉ 1 đơn vị** — trang 7–8 · Trung bình

| Loại         | Số Ineffective | Δ recall | Tương đương |
| ------------ | -------------- | -------- | ----------- |
| Counterclaim | 39             | +0,0256  | +1 đơn vị   |
| Rebuttal     | 34             | +0,0294  | +1 đơn vị   |
| Claim        | 317            | +0,0315  | +10 đơn vị  |
| Position     | 100            | −0,0700  | −7 đơn vị   |

- Vì sao sai: mục 4.4 dựng cả lý thuyết về "đơn vị quan hệ" và "đơn vị tự trị" trên mức chênh 1 đơn vị đoán đúng thêm. Mức đó có thể chỉ là nhiễu giữa hai lần huấn luyện.
- Sửa: ghi số đơn vị bên cạnh %. Trình bày 4.4 là giả thuyết cần kiểm thêm.

**D5 · Không ghi max_length và tỷ lệ bị cắt** — trang 6 · Trung bình

- Lỗi: mục 4.1 không nói input tối đa bao nhiêu token và cắt câu thế nào.
- Vì sao sai: input Level 1 dài gần gấp 3 Level 0. Nếu max_length là 512, đơn vị đích ở Evidence hoặc Position có thể bị cắt mất một phần. Khi đó việc Position giảm có thể do bị cắt, không phải do "nhiễu ngữ cảnh" như mục 4.4 giải thích.
- Sửa: ghi max_length và chiến lược truncation; báo % đơn vị bị cắt theo từng loại ở cả hai mức.

**D6 · Chưa rõ thí nghiệm có thật sự "kiểm soát"** — trang 6 · Trung bình

- Lỗi: Level 0 được ghi là "Baseline from Week 9". Neighbor được định nghĩa là "discourse unit" liền kề.
- Vì sao sai: thầy dặn "giữ nguyên mô hình và split, chỉ đổi đầu vào". Nếu số Level 0 lấy từ Tuần 9 (khác lần chạy, có thể khác máy, khác max_length) thì chênh lệch không chỉ do đầu vào. Ngoài ra có 28.977 đoạn không có nhãn bị loại, nên "đơn vị liền kề" có thể không phải đoạn văn liền kề thật.
- Sửa: ghi rõ Level 0 có được huấn luyện lại trong cùng script, cùng seed và cấu hình không; ghi rõ neighbor lấy từ đơn vị có nhãn hay từ văn bản gốc.

### 10 ca lỗi (mục 5)

**D7 · So xác suất từ hai lần huấn luyện khác nhau** — trang 9–10 · Trung bình

- Lỗi: cột "Week 9 P(Ineff)" lấy từ mô hình Tuần 9, cột "Level 1 P(Ineff)" từ mô hình mới.
- Vì sao sai: hai mô hình khác nhau cả đầu vào lẫn lần huấn luyện. P(Ineff) thay đổi có thể chỉ do huấn luyện lại. Thêm nữa, 10 ca được chọn vì là lỗi tự tin nhất của mô hình cũ, nên chạy lại kiểu gì cũng có xu hướng bớt sai (hồi quy về trung bình).
- Sửa: đưa 10 ca qua cả Level 0 lẫn Level 1 của cùng lần chạy trong notebook 05.

**D8 · Cả 10 ca đều gắn "Extrinsic"** — trang 9–10 · Nhẹ

- Lỗi: cột Failure Mechanism ghi "Extrinsic" cho cả 10 ca (2 ca là "Local/Extrinsic").
- Vì sao sai: thầy hỏi "ca nào sẽ đoán đúng nếu thấy đoạn văn xung quanh, ca nào thì không", tức là cần phân loại. Gắn cùng một nhãn cho tất cả thì không trả lời được câu hỏi.
- Sửa: tự đọc từng ca và phân loại (đủ trong câu / cần câu lân cận / cần toàn bài / cần văn bản nguồn) trước khi xem kết quả mô hình, rồi đối chiếu.

### LOPO (mục 6)

**D9 · Khoảng cách LOPO so với sai mốc** — trang 12–14 · Nghiêm trọng

- Lỗi: "generalization gap" −0,0927 (RF) và −0,0948 (DeBERTa) được tính bằng LOPO trên từng đề trừ in-domain trên toàn bộ validation.
- Vì sao sai: hai bên khác nhau cả tập test lẫn độ khó đề. Đề Cowboy vốn khó ngay cả khi đã thấy trong train, nên một phần khoảng cách là độ khó của đề, không phải do đề mới. DeBERTa còn chỉ có 3 đề được chọn, nên −0,0948 không đại diện cho 15 đề.
- Sửa: với mỗi đề P, so in-domain trên phần validation của đề P với LOPO trên đề P.

**D10 · "Vượt trội đáng kể" chỉ với 3 đề** — trang 13–14 · Trung bình

- Lỗi: "DeBERTa-v3 significantly outperforms", "Consistent … Across All Tiers", "every single held-out prompt", "empirically bounds the cost of zero prompt transfer".
- Vì sao sai: chỉ có 3 đề, không có kiểm định thống kê, nên không dùng được chữ "significantly". Báo cáo cũng bỏ qua việc accuracy của DeBERTa thấp hơn RF ở cả 3 đề (78,87% so với 79,20%; 66,58% so với 70,24%; 75,55% so với 78,05%).
- Sửa: nói "DeBERTa có macro-F1 cao hơn RF ở cả 3 đề thử", nêu cả phần accuracy thấp hơn, bỏ "empirically bounds".

**D11 · Xếp hạng loại đơn vị trên quá ít mẫu** — trang 14, 16 · Trung bình

- Lỗi: báo cáo trả lời câu hỏi 2 của thầy bằng xếp hạng cứng: Rebuttal giảm nhiều nhất (−22,79%), rồi Evidence (−19,36%).
- Vì sao sai: 3 folds chỉ có 584 đơn vị Ineffective (1,7%, trong khi toàn bộ dữ liệu là 4,5%). Rebuttal chỉ có 23, Counterclaim 26, Concluding 32. Các mức −22,8% / −19,4% / −19,1% không phân biệt được với nhau. Mốc in-domain cũng bị lỗi như D9.
- Sửa: tính CI bằng bootstrap; trả lời theo nhóm ("Rebuttal, Evidence, Concluding Statement giảm nhiều hơn Position") thay vì xếp hạng.

### Diễn giải (mục 4.4, 5.3, 6.5, 7.1)

**D12 · Vẫn đoán cơ chế bên trong mô hình** — trang 8, 10, 14–15 · Nghiêm trọng

- Lỗi: "to DeBERTa, 'brings me back to paragraph 36' appears to be an exemplary academic citation marker"; "Local context enables DeBERTa to detect semantic repetition"; Position bền vững nhờ "generic stance-taking templates".
- Vì sao sai: thầy đã nói rõ kiểu giải thích này "là đoán; DeBERTa không có trọng số theo từ để đọc ra như vậy". Không có thí nghiệm nào trong báo cáo kiểm các câu trên. Đây là lỗi thầy đã phê, lặp lại thì bị đánh giá là không tiếp thu.
- Sửa: bỏ, hoặc ghi rõ là giả thuyết kèm cách kiểm (ví dụ: đổi "paragraph 36" thành câu trung tính rồi xem xác suất thay đổi thế nào).

**D13 · Sơ đồ 4 tầng thông tin trình bày như kết quả** — trang 15 · Trung bình

- Lỗi: mục 7.1 ghi Level 2 (văn bản nguồn) là "Essential", Level 3 (toàn bài) là "Necessary", và "Automated models cannot reach expert human reliability on Evidence units until …".
- Vì sao sai: nhóm mới thử Level 0 và Level 1. Level 2 và 3 chưa được chạy, nên đây là giả thuyết.
- Sửa: ghi là giả thuyết. Có thể kiểm Level 2 thật: 7 đề source-based trong PERSUADE 2.0 đều có văn bản nguồn. Đây cũng là mức "đơn vị cùng đề bài" thầy gợi ý.

## Thứ tự ưu tiên sửa

Sửa trình bày và các điều kiện "xong" của thầy trước, rồi đến số liệu, cuối cùng là chạy thêm phân tích. Các bước 1–3 chỉ cần sửa file, bước 4–5 cần chạy lại notebook.

1. Xuất lại PDF đúng cách: A1–A7 (bỏ \$...\$ cho số thường, chèn ảnh sơ đồ, xuất bằng trình duyệt hoặc pandoc, kiểm chữ và link).
2. Đáp ứng điều kiện "xong": B1 (confusion matrix), B2 (trích dẫn và kappa), B4 (một cơ chế 6,13%), B5.
3. Sửa số liệu trong bảng và abstract: C1–C6.
4. Chạy thêm phân tích chính: D1 (lỗi theo quartile × nhãn), D3 (bootstrap Level 0/1), D5 (max_length, tỷ lệ cắt), D9 (LOPO so cùng đề).
5. Viết lại các kết luận cho khớp bằng chứng: D12, D13, D4, D10, D11, rồi các mục còn lại (B3, B6–B8, D2, D6–D8).