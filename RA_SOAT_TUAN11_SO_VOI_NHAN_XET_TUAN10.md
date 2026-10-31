# RÀ SOÁT TUẦN 11 — ĐỐI CHIẾU CODE, LOGIC VÀ BÁO CÁO VỚI NHẬN XÉT TUẦN 10

**Nhóm:** CLC02 · Group 06 · **Ngày rà soát:** 31/10/2026
**Phạm vi:** `Nhan_xet_Week10_CLC02_Group06.docx.md` ↔ `RESEARCH_REPORT_WEEK11_…md` / `Week11_Group06_CLC02_Report.docx` / `.html`, toàn bộ script và file kết quả tuần 11 (`Person1/`, `Person2Khoa/`, `Week11_Person3_DeBERTa_OfficialTest/`, `outputs/`).
**Cách rà soát:** chạy lại mọi con số từ dữ liệu gốc (`persuade_corpus_2.0_train.csv`, `persuade_corpus_2.0_test.csv`) và từ các file dự đoán đã lưu; không đọc lại số trong báo cáo mà tính lại.

---

## 0. Tóm tắt nhanh

| Mức | Số mục | Ý nghĩa |
|---|:---:|---|
| 🔴 Nghiêm trọng | 8 (B1–B7, B25) | Sai số liệu hoặc sai kết luận khoa học. Nếu thầy chạy lại sẽ phát hiện ngay. |
| 🟠 Lớn | 9 (B8–B16) | Không đáp ứng đúng tiêu chí "Xong khi" của thầy, hoặc nói quá bằng chứng. |
| 🟡 Nhỏ | 9 (B17–B24, B26) | Trình bày, định dạng, nhất quán. |

**Ba phát hiện quan trọng nhất**

1. **Bảng Điểm holistic × Độ dài (yêu cầu bắt buộc 3) là sai hoàn toàn.** Bảng cũ ghép dữ liệu bằng `discourse_id`. Nhưng file CSV gốc đã bị Excel làm tròn ID (`1.62263E+12`), nên 144.289 đơn vị chỉ còn **728** giá trị `discourse_id` khác nhau. Mỗi đơn vị vì vậy bị gán điểm và độ dài của một bài khác. Con số "lỗi phẳng ~26% ở mọi ô" chính là dấu hiệu của việc gán ngẫu nhiên. Chạy lại script cũ cho ra đúng từng con số, kể cả bảng cỡ mẫu 3.2.
   Khi ghép đúng, **trong cùng một mức điểm, lỗi vẫn tăng theo độ dài**. Ví dụ điểm 3: 19,3% → 21,8% → 22,9% → 28,2% (validation) và 17,6% → 20,8% → 22,3% → 29,2% (test). Hồi quy có kiểm soát điểm, nhãn gold và loại đơn vị cho OR ≈ 1,13–1,19 mỗi bậc độ dài, khoảng tin cậy nằm hẳn trên 1. Kết luận "giả thuyết B được xác nhận trọn vẹn, độ dài không ảnh hưởng" vì vậy phải đảo lại. Đây đúng là nhánh "nếu kết quả không như mong đợi" thầy đã dặn: giả thuyết A chưa bị loại, phải viết cả hai khả năng.
2. **RF trên test không phải RF Feature Set B.** Yêu cầu bắt buộc 2 ghi rõ "RF (Feature Set B)". Script `run_rf_official_test.py` cũ lại dùng 100 cây, depth 30, TF-IDF 10k, min_df=3, chỉ một đặc trưng độ dài chưa chuẩn hóa, và huấn luyện trên cả 144.289 đơn vị (gồm cả validation). Tức là một mô hình chưa từng được validate. Đã dựng lại đúng cấu hình tuần 9 và chấm lại (xem mục B2).
3. **Số validation và số test của DeBERTa đến từ hai lượt huấn luyện khác nhau.** Tuần 11 phải train lại L0/L1/PA vì checkpoint cũ không còn dùng được. Báo cáo lại ghép số validation tuần 10 (0,5768 / 0,5790; +0,0022) với số test của mô hình train lại, rồi viết "+0,0022 trên validation → +0,0159 trên test". Lượt train lại có validation riêng: 0,5723 / 0,5809 / 0,5855 và L1−L0 = +0,0087 [0,0014; 0,0161]. Báo cáo cũng không nói việc train lại, và gọi mô hình được chấm là "Level 1 đã khóa".

---

## A. Đối chiếu từng yêu cầu của thầy (Nhan_xet_Week10)

| # | Yêu cầu của thầy | Tiêu chí "Xong khi" | Trạng thái trong báo cáo cũ | Đánh giá | Đã sửa |
|---|---|---|---|---|---|
| 1 | **[Bắt buộc]** Viết lại kết luận 7.2: L1 không cải thiện rõ; phù hợp với giả thuyết cần bài đọc nguồn và toàn bài nhưng chưa kiểm chứng; thêm một câu về độ tin cậy nhãn | Không còn chữ "chứng minh" trong mục 7.2 | Mục 8.2 đã viết lại khá đúng. Nhưng toàn báo cáo vẫn còn *"definitively resolves"*, *"conclusively verified"*, *"Hypothesis B is conclusively verified"*, *"proved Level 1 significantly beats"*, *"Disproved Hypothesis A"*, *"confirming that orienting the model to the prompt provides beneficial grounding"*. Câu κ = 0,316 lại nói quá: *"a substantial portion of the remaining ceiling stems from…"* | 🟠 Đạt một phần | ✅ Viết lại mục kết luận; bỏ mọi từ "prove/definitively/conclusively"; câu về nhãn viết đúng mức |
| 2 | **[Bắt buộc]** Protocol chấm cùng lượt RF (Feature Set B), DeBERTa L0, L1; ghi rõ L0 và L1 không phân biệt được trên validation | Protocol liệt kê ba hệ thống; bảng test có ba dòng | Mục 1.3 (protocol) chỉ mô tả cấu hình DeBERTa L1, không liệt kê ba hệ thống, không có câu "L0 và L1 không phân biệt được trên validation". Dòng RF trên test là **một mô hình khác** Feature Set B (B2). L0/L1 trên test là mô hình train lại, khác mô hình đã khóa (B3) | 🔴 Chưa đạt | ✅ Viết lại protocol (3 hệ thống chính + 2 hệ thống bổ sung được ghi rõ); chấm lại đúng RF FSB; công khai việc train lại |
| 3 | **[Bắt buộc]** Tỷ lệ lỗi theo 4 nhóm độ dài trong cùng mức điểm holistic | Bảng điểm × độ dài + một câu "trong cùng điểm, lỗi có tăng theo độ dài không" | Có bảng nhưng **số liệu sai** do ghép bằng ID bị Excel làm tròn (B1). Kết luận đi ngược dữ liệu thật | 🔴 Sai | ✅ Viết lại script (ghép theo `row_idx`), thêm N bài, CI bootstrap theo bài, hồi quy cụm theo bài, kiểm tra thêm trên test; viết lại mục 3 theo đúng nhánh "kết quả không như mong đợi" |
| 4 | **[Nên làm]** Ca "paragraph 36" ghi là giả thuyết, hoặc kiểm tra bài đọc nguồn | Câu viết đúng mức | Mục 5.2 vẫn khẳng định *"A human grader … recognizes that paragraph 36 does not exist"*. Đã kiểm tra bộ nguồn của đề *Car-free cities* (bản có đánh số đoạn, 43 đoạn): **đoạn 36 có tồn tại và chứa đúng câu học sinh trích**. Giả thuyết "trích dẫn bịa" là **sai** | 🔴 Sai sự thật | ✅ Sửa: trích dẫn đúng; điểm yếu nằm ở phần lập luận lạc đề phía sau (đọc được ngay trong đơn vị, không cần văn bản nguồn) |
| 5 | **[Nên làm]** Xuất bản cuối từ Word/LaTeX | Mọi bảng đọc được | Có docx. Nhưng builder viết LaTeX trong chuỗi Python thường, nên `\t` bị biến thành ký tự TAB: `$	heta$`, `$P(	ext{Ineffective})$` xuất hiện 10 chỗ trong md/docx/html. Builder còn **ghi đè** `RESEARCH_REPORT_WEEK10_…md` bằng nội dung tuần 11, làm mất bản nộp tuần 10 | 🟡 | ✅ Khôi phục báo cáo tuần 10 từ git; dựng lại docx/html từ md mới, không ghi đè file tuần 10 |
| — | **Luyện interview bước 5:** hạ ngưỡng Ineffective trên file xác suất đã lưu, xem **bao nhiêu ca đổi** | — | Không trả lời "bao nhiêu ca đổi". Bảng ngưỡng mâu thuẫn với chính nó (B4) | 🔴 | ✅ Script mới đếm số ca đổi (trong 10 ca và trên 29.102 đơn vị) và cái giá phải trả |
| — | **Chuẩn bị interview:** κ mô hình 0,37 với κ người 0,316 vì sao không so trực tiếp; LOPO khác in-domain ở đâu, vì sao Cowboy giảm nhiều nhất | — | Có trả lời. Nhưng phần "Cowboy giảm −8,52%" so hai tập đánh giá khác nhau (B7) | 🟠 | ✅ Tính lại trên cùng tập đơn vị, có CI |
| — | **Đề xuất câu kết luận chính về ngữ cảnh, viết đúng mức** | — | Mục 7.3 viết *"Clear superiority… conclusively outperforms"*, *"confirming … beneficial grounding"* | 🟠 | ✅ |

---

## B. Lỗi tự phát hiện (ngoài nhận xét của thầy)

### 🔴 Nghiêm trọng

| ID | Vị trí | Vấn đề | Bằng chứng (tính lại) | Xử lý |
|---|---|---|---|---|
| **B1** | `Person1/script_holistic_length_table.py`, Báo cáo §3.3–3.4, bảng 3.1–3.2, Tóm tắt, mục 9.1 | Ghép dự đoán validation với `holistic_essay_score` / `essay_word_count` qua `discourse_id` đã bị Excel làm tròn. 144.289 đơn vị → 728 ID. `drop_duplicates` rồi `merge` gán điểm/độ dài của bài khác | Chạy lại script cũ ra **y hệt** bảng 3.1 và 3.2. Dấu hiệu sai thứ hai: tổng N theo nhóm trong bảng 3.2 (8.682/5.888/6.812/7.720) không khớp bảng 3.2 tuần 10 (7.333/7.277/7.226/7.266). Dấu hiệu thứ ba: mọi ô Q1 đều ≥ 23,41% thì tỷ lệ lỗi chung của Q1 không thể là 21,98% | Script mới ghép theo vị trí/`row_idx` và tự kiểm tra (essay_id_comp, discourse_type, nhãn gold) trước khi tính. Kết quả mới: `outputs/holistic_score_x_length_quartile_error_rates.csv`, `length_within_score_regression.csv`, `length_quartile_marginal_error_by_model.csv` |
| **B2** | `run_rf_official_test.py` (gốc + `Person1/`), bảng test §7.1 | Mô hình RF trên test ≠ RF Feature Set B đã chọn trên validation (khác số cây, độ sâu, số đặc trưng TF-IDF, min_df, thiếu 4/5 đặc trưng cấu trúc, không chuẩn hóa, train trên cả train + validation). Số 0,4834 / 67,79% không thuộc mô hình nào trong protocol | So `01_Data_Pipeline_Classical_Baseline.py` dòng 690–735, 866–875 | Script mới dựng đúng FSB, train đúng 115.187 đơn vị, **chỉ chấm test nếu tái tạo được Macro-F1 validation tuần 9**. Số chấm lại ghi ở §7 báo cáo; số cũ giữ trong chú thích để minh bạch |
| **B3** | Báo cáo §1.3, §4.1, §7.1, §7.3 ý 2, Tóm tắt | Số validation của L0/L1 (0,5768/0,5790) là của mô hình tuần 10. Số test là của mô hình **train lại ở notebook 07** (checkpoint cũ không dùng được). Câu "+0,0022 trên validation → +0,0159 trên test" so hai cặp mô hình khác nhau. "Level 1 (Locked)" thực ra là mô hình train lại cùng cấu hình | `outputs/week11_person3/run_metadata.json` ("source": "train ở notebook 07"), `validation_L0_L1_PA.csv`, `validation_bootstrap_by_essay.csv` | Báo cáo mới dùng số validation của chính lượt train lại (0,5723 / 0,5809 / 0,5855; L1−L0 +0,0087 [0,0014; 0,0161]; PA−L1 +0,0045 [−0,0025; 0,0113]), công khai việc train lại, và nói rõ chênh L1−L0 dao động giữa hai lượt train (0,0022 vs 0,0087). Bootstrap trên test chỉ đo nhiễu do mẫu test, không đo nhiễu do huấn luyện |
| **B4** | Báo cáo §5.3–5.4, Tóm tắt ý 4, mục 9.1, script `script_threshold_tuning_and_case8.py` | (a) "Ngưỡng mặc định 0,33" không tồn tại; mặc định là argmax. (b) "Recall 36,5% → 76,51% tại θ = 0,10" **không thể có**: bảng của chính nhóm cho 74,40% tại 0,09 và 71,99% tại 0,11, recall giảm dần theo θ. Số đúng tại 0,10 là 73,04%. (c) Bảng ghi "0,11 (Selected)" nhưng chữ ghi 0,10. (d) Ca 8 được "tìm" bằng bộ lọc `Claim & 0,11<P<0,13`, rồi lấy dòng đầu tiên. (e) Giấu cái giá: Macro-F1 giảm 0,5790 → 0,5167; cứ 1 câu Ineffective bắt thêm được thì có ~8 cảnh báo nhầm. (f) Với mô hình L1 **đã chấm test**, P(Ineff) của ca 8 chỉ là 0,058, nên **không lật** ở θ = 0,10 | `outputs/ineffective_threshold_tuning_table.csv` (mới), `outputs/threshold_case_flips.csv` | Script mới: mốc argmax, quy tắc rõ ràng, 10 ca xác định bằng văn bản, đếm số ca đổi. Trả lời đúng câu thầy hỏi: **θ = 0,10 → 2/10 ca đổi (ca 5, 8); 3.670/29.102 đơn vị đổi nhãn; +396 Ineffective bắt đúng, +3.274 cảnh báo nhầm** |
| **B5** | Báo cáo §2.2 "Trace of a Real Sample" | Mẫu "Essay `514559001`, discourse `1622840003`, *Students should be able to use cell phones at school during lunch time.*, xác suất [0,042; 0,812; 0,146]" **không có trong dữ liệu**: tìm toàn văn trong 144.289 đơn vị không thấy. Đây là ví dụ bịa | Tìm chuỗi trong `discourse_text` | Thay bằng một mẫu thật, truy vết được: ca 8, `essay_id_comp = FE3141FA4163`, `row_idx = 108613`, xác suất thật của L0/L1/PA |
| **B6** | Báo cáo §7.1, §7.2 | Runtime "~6,5 / 7,2 / 7,8 min (A100)" không khớp log thật: suy luận test mất **57,2 / 91,0 / 93,5 giây**. Báo cáo ghi "1,000 iterations"; cấu hình thật là **n_bootstrap = 2000** | `test_runtimes.json`, `run_metadata.json` | Sửa theo log |
| **B7** | Báo cáo §6.2–6.3, bảng 6.1 | "DeBERTa Generalization Gap": LOPO chấm trên **toàn bộ** đơn vị của đề (Cowboy 5.158), in-domain chỉ chấm trên **phần validation** của đề (1.030). Hai tập khác nhau, không có CI. Kết luận nhân quả "do thể loại văn học" rút từ chỉ 3 đề | Script mới `script_lopo_same_units_gap.py` | Trên **cùng** 1.030 đơn vị: Cowboy LOPO 0,3584 vs in-domain 0,4462, chênh **−0,088 [−0,138; −0,041]** (lớn hơn số cũ −0,038); Summer −0,009 [−0,093; +0,078]; Distance +0,004 [−0,024; +0,028]. Chỉ Cowboy giảm rõ. "Thể loại" chỉ là một giả thuyết |

### 🟠 Lớn

| ID | Vị trí | Vấn đề | Xử lý |
|---|---|---|---|
| B8 | Toàn bộ file dự đoán và file CSV gốc | `essay_id`, `discourse_id` trong CSV gốc và mọi file `*_predictions.csv` đều bị Excel làm tròn. `essay_id` chỉ còn 1 cặp va chạm (gộp 2 bài vào 1 nhóm, không gây rò rỉ). `discourse_id` thì vô dụng. Báo cáo §2.1 lại nói đã "chống mất số 0 đầu" bằng `dtype=str` | Thêm đoạn "Data integrity note" trong báo cáo; mọi script mới ghép bằng `row_idx` / `essay_id_comp`. Khuyến nghị: không mở/lưu CSV bằng Excel |
| B9 | §7.1 Linear SVM | SVM trên test chưa từng có số validation (SVM của tuần 9 là *Calibrated* SVM, Macro-F1 0,3408, khác cấu hình). Nó lại được train trên 144.289 đơn vị trong khi DeBERTa/RF chỉ dùng 115.187 | Đã tính validation cho đúng cấu hình đó (train 115.187 → val): **Macro-F1 0,4845**. Ghi SVM là hệ thống bổ sung, chú thích khác biệt dữ liệu huấn luyện |
| B10 | §7.1, §7.3 | Prompt-Aware không nằm trong protocol khóa tuần 10, nhưng được trình bày như kết quả chính, kèm câu "confirming … beneficial grounding" trong khi CI của PA−L1 chứa 0 trên cả validation lẫn test | Ghi PA là hệ thống thăm dò (kế hoạch tuần 11); viết "không phân biệt được với L1" |
| B11 | §7.2 | "p < 0,001" và "p = 0,0" từ bootstrap 2.000 lần (độ phân giải p nhỏ nhất ≈ 0,0005). p = 0,0315 là p **một phía**, trong khi CI 95% là hai phía, nên đọc dễ mâu thuẫn ("p < 0,05 nhưng CI chứa 0") | Ghi "p₁ₚ < 0,0005" và nói rõ một phía; kết luận theo CI |
| B12 | §3.4, Tóm tắt, mục 9.1 | Chuỗi "21,98% → 30,35%" (lỗi theo độ dài toàn bài) không thuộc mô hình nào hiện có. Lỗi theo nhóm độ dài phải lấy từ **cùng mô hình** với bảng trong-điểm | Báo cáo mới dùng một mô hình cho cả hai bảng: L1 tuần 11, val 22,0% → 30,5%; test 21,1% → 30,4% |
| B13 | §6.3 ý 1 | "TF-IDF không chuyển giao, sụt giảm nghiêm trọng". Nhưng SVM/RF không có số in-domain theo từng đề, nên không thể nói "sụt giảm" | Chỉ so giữa các mô hình trên cùng fold; bỏ câu "sụt giảm" |
| B14 | §6.1 | Gọi Linear SVM là "same-family baseline" trong khi SVM và RF khác họ, và cả hai đều khác họ DeBERTa. Phép so sánh cùng họ thật sự là DeBERTa LOPO với DeBERTa in-domain | Đổi tên: "baseline cổ điển bổ sung" và "đối chứng trong cùng họ DeBERTa" |
| B15 | §9.2 AI disclosure | Chỉ ghi "Gemini / Antigravity". Thực tế lượt chạy Người 3 (Colab qua Docker), lượt rà soát này và việc sinh notebook có dùng Claude Code / Codex | Bổ sung trung thực. **Nhóm cần tự xác nhận danh sách công cụ cuối cùng** |
| B16 | LOPO DeBERTa tuần 10 | `lopo_run_metadata.json` ghi `transformers 5.20.2` trên T4. Tuần 11 đã thấy transformers 5.x làm DeBERTa-v3 train lỗi (NaN / không học). Kết quả LOPO vẫn học được (Macro-F1 0,41–0,57) nhưng có thể thấp hơn thực lực | Ghi thành hạn chế; không chạy lại (tốn ~6 giờ GPU, không phải yêu cầu của thầy) |

### 🟡 Nhỏ

| ID | Vấn đề | Xử lý |
|---|---|---|
| B17 | LaTeX hỏng do `\t` (10 chỗ) | ✅ Sửa |
| B18 | Builder ghi đè báo cáo tuần 10 | ✅ Khôi phục từ git, bỏ đoạn ghi đè |
| B19 | Lỗi chính tả "Chatted and registered prior to unsealing"; "Overall Accuracy … Class 0" | ✅ |
| B20 | Số bài train 12.474 (đếm `essay_id` đã hỏng) vs 12.475 (`essay_id_comp`) | ✅ Dùng 12.475 |
| B21 | Bảng 7.1 in đậm số của L1 ở cột mà PA cao hơn | ✅ |
| B22 | §3.2 cột "Mean Holistic" tính theo đơn vị hay theo bài không rõ | ✅ Ghi rõ "theo bài" |
| B23 | `WEEK11_PLAN_AND_ASSIGNMENTS.md` / `HUONG_DAN_HOAN_THIEN_TUAN_11…md` (cẩm nang interview) còn số cũ và câu nói quá ("phẳng lì 25–26%", "76,51%", in-domain Cowboy 0,4934, "chứng minh dứt khoát") | ✅ Thêm phụ lục đính chính ở đầu hai file (giao worker), để các thành viên không trả lời sai khi phỏng vấn |
| B25 | `script_official_test_evaluation.py` (thư mục gốc) chép cứng số DeBERTa giả định rồi ghi vào `outputs/official_test_final_summary.csv`; `official_test_final_3_systems_summary.csv` là rác từ lần chạy thử | ✅ Viết lại: chỉ đọc file kết quả thật + bootstrap DeBERTa so với RF. — **xếp 🔴** (số không có thật nằm trong outputs) |
| B26 | Cẩm nang interview ghi "lớp Ineffective chiếm 11,8%". Đếm lại từ dữ liệu: **4,48%** (train), 4,56% (validation), 4,51% (test) | ✅ Đính chính trong khối đầu của hai file hướng dẫn |
| B24 | `Person1/*.ipynb`, `Person2Khoa/…/script_threshold_tuning_and_case8.ipynb` không còn khớp script đã sửa | ✅ Sinh lại từ script (worker Codex) |

---

## C. Số liệu đúng sau khi tính lại (dùng cho báo cáo và interview)

**Độ dài × trình độ (DeBERTa L1 tuần 11, validation, tỷ lệ lỗi %, [CI 95% bootstrap theo bài], N đơn vị/N bài)**

| Điểm | Q1 (≤315 từ) | Q2 (316–422) | Q3 (423–566) | Q4 (≥567) |
|---|---|---|---|---|
| 2 | 23,2 [21,3; 25,1] 3.200/493 | 31,4 [27,1; 35,6] 722/91 | 33,2 [26,3; 39,5] 295/34 | 38,8 [27,9; 51,0] 80/11 |
| 3 | 19,3 [17,7; 21,1] 3.517/424 | 21,8 [20,0; 23,9] 3.743/404 | 22,9 [19,8; 26,0] 1.465/143 | 28,2 [22,1; 34,3] 472/40 |
| 4 | 19,6 [13,4; 26,6] 260/29 | 22,0 [19,9; 23,9] 2.622/260 | 28,5 [26,5; 30,5] 3.984/379 | 31,1 [28,2; 33,9] 1.961/174 |
| 5 | — | 29,1 [21,3; 38,0] 127/12 | 30,3 [26,9; 34,0] 1.391/120 | 31,7 [29,6; 34,0] 3.336/277 |

Hồi quy logistic, sai số chuẩn cụm theo bài, OR cho mỗi bậc độ dài:
- không kiểm soát: 1,17 [1,14; 1,21]
- kiểm soát điểm: 1,19 [1,14; 1,25]
- kiểm soát điểm + nhãn gold + loại đơn vị: 1,17 [1,11; 1,23]

Trên test (93.677 đơn vị), mô tả thêm, không dùng để chọn gì: 1,16 [1,13; 1,19] và 1,13 [1,10; 1,16].

**Câu trả lời cho tiêu chí của thầy:** *Trong cùng một mức điểm, lỗi vẫn tăng theo độ dài. Vì vậy giả thuyết A (độ dài/độ phức tạp) chưa bị loại. Dịch chuyển trình độ giải thích việc **loại** lỗi thay đổi (ở Q4, 92% lỗi là nhầm Adequate↔Effective), nhưng không giải thích hết **mức** lỗi tăng.*

**Ngưỡng Ineffective (L1 tuần 10, mô hình của 10 ca)**

| Quy tắc | Recall Ineff | Precision Ineff | Macro-F1 | Đơn vị đổi nhãn | Bắt thêm đúng / báo nhầm thêm | Số ca đổi /10 |
|---|---|---|---|---|---|---|
| argmax | 43,2% | 36,1% | 0,5790 | — | — | 0 |
| θ = 0,15 | 67,4% | 21,9% | 0,5393 | 2.503 | 321 / 2.182 | 1 |
| θ = 0,10 | 73,0% | 18,4% | 0,5167 | 3.670 | 396 / 3.274 | 2 (ca 5, 8) |
| θ = 0,08 | 75,7% | 16,8% | 0,5029 | 4.410 | 431 / 3.979 | 5 |

Với mô hình L1 tuần 11 (mô hình đã chấm test), θ = 0,10 cho: recall 69,6%, Macro-F1 0,5809 → 0,5348, 2.872 đơn vị đổi nhãn, 3/10 ca đổi. Ca 8 **không** đổi, vì P(Ineff) = 0,058.

**RF Feature Set B chấm lại trên test** (scikit-learn 1.6.1, train 115.187 đơn vị): validation 0,5261 (tuần 9: 0,5230); **test Macro-F1 0,5098**, accuracy 78,51%, F1 Ineffective 0,2024. DeBERTa so với RF trên test (bootstrap theo bài, 1.000 lần): L0 +0,052 [0,045; 0,058], L1 +0,068 [0,061; 0,075], PA +0,071 [0,064; 0,078].

**Phát hiện thêm khi rà soát:** `script_official_test_evaluation.py` ở thư mục gốc **chép cứng** số DeBERTa "kỳ vọng" (0,5692 / 0,5724 / 0,5820) và ghi vào `outputs/official_test_final_summary.csv`. File `official_test_final_3_systems_summary.csv` chứa số của một lần chạy thử (accuracy 90,8%, F1 Ineffective = 0). Cả hai đã được thay bằng bản tổng hợp chỉ đọc kết quả thật (B25).

**LOPO trên cùng tập đơn vị**: xem B7.

**RF Feature Set B (chấm lại)**: xem §7 báo cáo và `outputs/official_test_rf_actual_result.csv`.

---

## D. Những gì đã sửa (file)

| File | Thay đổi |
|---|---|
| `Person1/script_holistic_length_table.py` (+ bản ở thư mục gốc, + `.ipynb`) | Viết lại: ghép theo `row_idx` có kiểm tra; CI theo bài; hồi quy cụm; chạy được trên test |
| `Person1/run_rf_official_test.py` (+ bản gốc, + `.ipynb`) | Dựng đúng RF Feature Set B; train 115.187 đơn vị; cổng kiểm tra tái tạo validation trước khi chấm test; lưu dự đoán test có `row_idx` |
| `script_threshold_tuning_and_case8.py` (+ `.ipynb` của Người 2) | Viết lại: mốc argmax, 10 ca xác định bằng văn bản, đếm ca đổi, chạy cho cả hai mô hình L1 |
| `script_lopo_same_units_gap.py` (mới) | Khoảng cách ngoại đề trên cùng tập đơn vị, bootstrap theo bài |
| `outputs/*` | Thay các file kết quả sai bằng file tính lại; thêm `length_within_score_regression.csv`, `length_quartile_marginal_error_by_model.csv`, `threshold_case_flips.csv`, `lopo_deberta_gap_same_units.csv`, `test_predictions_rf_feature_set_b.csv`, `official_test_rf_run_metadata.json` |
| `RESEARCH_REPORT_WEEK11_…md`, `Week11_Group06_CLC02_Report.docx/.html` | Viết lại các mục 1, 2.2, 3, 4, 5, 6, 7, 8, 9, thêm mục hạn chế |
| `RESEARCH_REPORT_WEEK10_…md` | Khôi phục bản gốc tuần 10 (đã bị builder ghi đè) |
| `build_week11_research_report.py` | Đọc md làm nguồn duy nhất, không chép cứng nội dung; không ghi đè file tuần 10 |

## E. Việc nhóm cần tự quyết / tự làm

1. **Xác nhận việc chấm lại RF Feature Set B trên test.** Đây là sửa lỗi cài đặt, không chọn siêu tham số trên test: cấu hình được cố định từ tuần 9, và script chỉ chấm test khi tái tạo được validation. Báo cáo đã công khai cả số cũ lẫn số mới. Nếu nhóm muốn giữ nguyên tắc tuyệt đối "test chỉ mở một lần", hãy giữ số cũ, nhưng **phải** ghi rõ đó không phải Feature Set B, nghĩa là yêu cầu 2 chưa đạt.
2. **Danh sách công cụ AI trong mục 9.2**: mỗi thành viên tự xác nhận mình đã dùng gì.
3. **Người 1 và Người 2 phải nắm phần đính chính** (B1, B4) trước interview. Thầy yêu cầu "mỗi người giải thích được bảng phân rã lỗi ở nhóm dài nhất", nên con số cũ "phẳng 26%" mà nói ra là sai.
4. Không mở và lưu lại bất kỳ CSV nào bằng Excel.
