# HƯỚNG DẪN & DÀN KHUNG CHUNG VIDEO BÁO CÁO (5 PHÚT)
## Course: Machine Learning Applications — Final Project Video Specification
**Đề tài:** Predicting the Effectiveness of Argumentative Discourse Units in Student Essays  
**Lớp / Nhóm:** CLC02 · Group 06  
**Thời lượng:** Khoảng **5 phút** (khuyến nghị 4:30 – 5:15, tương đương 650 – 720 từ tiếng Anh nói)  
**Định dạng nộp:** `Video/StudentID_Name.mp4` (1080p, âm thanh rõ, trình bày bằng tiếng Anh)  

---

## 1. YÊU CẦU CỐT LÕI TỪ GIẢNG VIÊN (`Requirements.md`)

Mỗi sinh viên nộp 1 video cá nhân riêng biệt. Đề yêu cầu **nội dung** gồm:
- Nói tiếng Anh, bằng giọng của chính mình. Giới thiệu ngắn bài toán và **nêu rõ phần đóng góp của bản thân**.
- Lấy một **ví dụ thật** từ dự án cuối và giải thích nó đi từ dữ liệu đến dự đoán/kết quả thế nào.
- Dùng biểu đồ, bảng hoặc ví dụ có chú thích để giải thích dữ liệu cho thấy điều gì.
- Demo bằng giao diện, notebook hoặc output đã lưu, và diễn giải **một** kết quả, lỗi hoặc giới hạn.

Điểm video được chấm theo **4 tiêu chí** (đúng nguyên văn đề):
1. **Technical explanation:** giải thích kỹ thuật đúng và rõ.
2. **Evidence and demonstration:** có ví dụ thật, số liệu thật, demo thật trên màn hình.
3. **Personal contribution:** thấy rõ phần **của bạn**, không phải phần của cả nhóm.
4. **Production quality:**
   - MP4 từ 1080p trở lên, âm thanh rõ;
   - code, biểu đồ, terminal đọc được ở tốc độ phát bình thường;
   - đã cắt các đoạn chờ lâu và xem lại file sau khi xuất.

---

## 2. DÀN KHUNG THUYẾT TRÌNH CHUNG (5 PHÚT)
*(Dàn khung dùng chung cho tất cả thành viên. Mỗi người chỉ cần đưa phần việc cụ thể của mình vào các vị trí đánh dấu `[...]`)*

```
[00:00 - 00:45] PHẦN 1: Giới thiệu bản thân & Bài toán nghiên cứu (45 giây)
[00:45 - 01:30] PHẦN 2: Phần việc cá nhân đảm nhiệm & Phương pháp tiếp cận (45 giây)
[01:30 - 02:45] PHẦN 3: Thao tác thực tế (Demo) & Lần vết 1 ví dụ cụ thể (75 giây)
[02:45 - 04:00] PHẦN 4: Phân tích kết quả thực nghiệm & Biểu đồ chính (75 giây)
[04:00 - 05:00] PHẦN 5: Phân tích trường hợp lỗi, Hạn chế & Kết luận (60 giây)
```

---

### CHI TIẾT TỪNG PHẦN:

### PHẦN 1: Giới thiệu bản thân & Bài toán (0:00 – 0:45)
- **Hình ảnh trình chiếu:** Slide tiêu đề (Họ tên, MSSV, Nhóm 06, Lớp CLC02, Tên đề tài) + Sơ đồ bài toán tổng thể (`fig01_user_decision_workflow.png`).
- **Nội dung nói:**
  - Giới thiệu bản thân: Tên, MSSV, nhóm.
  - Bối cảnh bài toán: Giáo viên dạy viết văn nghị luận tiếng Anh cần biết đoạn văn/luận điểm nào của học sinh bị yếu để sửa, thay vì chỉ nhận một con điểm tổng thể.
  - Dữ liệu nghiên cứu: Tập PERSUADE 2.0 (hơn 237.000 đơn vị luận điểm, 26.000 bài luận học sinh lớp 6–12 tại Mỹ, 15 đề viết).
  - Thách thức lớn nhất: Nhãn phân loại bị lệch rất nặng. Trên toàn bộ 237.966 đơn vị: `Ineffective` chỉ chiếm 4.5%, `Adequate` 79.3%, `Effective` 16.3%. Trên tập test: 4.5% / 80.5% / 15.0%. Nguồn: bảng `E1_split_label_distribution.csv`.

---

### PHẦN 2: Phần việc cá nhân & Phương pháp (0:45 – 1:30)
- **Hình ảnh trình chiếu:** Slide tóm tắt phân công cá nhân + Sơ đồ kiến trúc/pipeline tổng thể (`fig02_data_pipeline_split.png` hoặc `fig03_ml_pipeline.png`).
- **Nội dung nói:**
  - Nêu rõ phần việc cá nhân: `[Điền vai trò/nội dung cá nhân thực hiện: ví dụ xử lý dữ liệu & mô hình cổ điển / fine-tuning Transformer & ngữ cảnh / phân tích lỗi & kiểm soát đánh giá tập test]`.
  - Nguyên tắc dữ liệu của dự án:
    - File train được chia 80/20 **theo bài luận** thành train và validation (115.187 / 29.102 đơn vị; `GroupShuffleSplit`, seed 42), để các đoạn của cùng một bài không nằm ở hai tập.
    - Tập **test** là file test chính thức riêng (93.677 đơn vị, 10.402 bài), không cắt từ 20% kia. Test được chấm **đúng một lần** với cấu hình đã khoá.
  - Mục tiêu tối ưu: Đánh giá bằng Macro-F1 và F1 từng lớp để đảm bảo nhận diện tốt lớp thiểu số `Ineffective`.

---

### PHẦN 3: Thao tác thực tế & Lần vết ví dụ cụ thể (1:30 – 2:45)
- **Hình ảnh trình chiếu:** Quay màn hình thao tác thực tế (Mở VS Code / Jupyter Notebook hoặc chạy terminal lệnh tái lập).
- **Thao tác demo:**
  - *Cách 1 (Nhanh & trực quan):* Mở terminal, chạy lệnh `python MLA_Final/Code/reproduce_results.py` để hiển thị quá trình tính toán và kiểm chứng các bảng kết quả.
  - *Cách 2 (Chi tiết mô hình):* Mở một notebook đã chạy sẵn trong `MLA_Final/Code/notebooks/` để chỉ ra cấu hình mô hình và các cell xuất kết quả.
- **Lần vết 1 ví dụ dữ liệu:**
  - Chọn 1 đơn vị luận điểm thực tế **thuộc phần việc của mình**. Mỗi người một ví dụ khác nhau, để 3 video không trùng nhau. Gợi ý theo `VIDEO_CA_NHAN/README.md`:
    - Người 1: test `row_idx` 47059 ("That is all everything you need to know about Mona Lisa and her smile.", RF Feature Set B);
    - Người 2: ca 8, validation `row_idx` 108613 (*Claim: "Some kids will ask there parents to transfer school"*, L0 so với L1);
    - Người 3: ca 2, validation `row_idx` 10303 (Evidence trích đoạn 36 của nguồn, đi qua thang ngữ cảnh).
  - Giải thích cách dữ liệu đi từ văn bản gốc $\to$ đưa qua mô hình $\to$ cho ra nhãn dự đoán và xác suất xác thực.

---

### PHẦN 4: Kết quả thực nghiệm & Phân tích biểu đồ (2:45 – 4:00)
- **Hình ảnh trình chiếu:** Chiếu 1–2 biểu đồ chất lượng cao trong thư mục hình ảnh (`Results/figures/`) kết hợp với bảng số liệu tương ứng.
- **Nội dung nói:**
  - Trình bày kết quả cốt lõi liên quan đến phần việc của mình:
    - *Nếu nói về so sánh mô hình:* DeBERTa-v3 Level 1 đạt Macro-F1 **0.577** trên test, vượt trội so với Random Forest (**0.510**) và Majority (**0.297**).
    - *Nếu nói về vai trò ngữ cảnh:* Thêm **2 đơn vị lân cận** (đơn vị ngay trước và ngay sau, Level 1) giúp tăng **+0.016 Macro-F1** trên test.
      - Một đơn vị có thể dài nhiều câu.
      - Tăng mạnh nhất ở các loại được chấm so với đơn vị bên cạnh (`Counterclaim`, `Rebuttal`, `Claim`).
      - Mức tăng này ngang dao động giữa hai lượt train (lượt đầu chỉ +0.002 trên validation), nên chỉ nói là "small".
    - *Nếu nói về đề bài mới:* Đánh giá trên đề chưa từng thấy (LOPO) bị hụt từ **0.025 đến 0.092 Macro-F1** so với in-domain trên cùng bài.
      - Hụt nhiều nhất ở "A Cowboy Who Rode the Waves", là đề dựa trên bài đọc nguồn.
      - Mới có 3 đề, mỗi đề 1 lượt chạy, và khoảng tin cậy của Summer projects chứa 0. Vì vậy liên hệ "đề đọc nguồn thì hụt nhiều hơn" chỉ là **diễn giải, chưa được kiểm chứng**.
    - *Nếu nói về độ dài bài:* Độ dài bài tương quan mạnh với điểm (0.76). Trong cùng một mức điểm, bài càng dài thì tỷ lệ lỗi vẫn tăng (odds ratio 1.19).
  - Chỉ rõ số liệu trên biểu đồ và giải thích ý nghĩa thực tế.

---

### PHẦN 5: Phân tích lỗi, Hạn chế & Kết luận (4:00 – 5:00)
- **Hình ảnh trình chiếu:** Biểu đồ phân tích lỗi (`fig23`, `fig20` hoặc `fig24_rater_rater_vs_model_rater_agreement.png`).
- **Nội dung nói:**
  - Chỉ ra 1 điểm hạn chế hoặc 1 trường hợp mô hình đoán sai:
    - Ví dụ về tính chủ quan của người chấm: Độ đồng thuận giữa 2 người chấm độc lập chỉ đạt $\kappa = 0.316$. Nghĩa là bản thân nhãn đã có độ nhiễu, và một phần "lỗi mô hình" thực chất là bất đồng trong chính nhãn.
      - **Không so trực tiếp** với $\kappa$ mô hình–nhãn = 0.372. Hai số khác nhau về đối tượng so sánh, nhãn (trước/sau phân xử), đơn vị và cách tính.
      - Vì vậy 0.372 > 0.316 **không** có nghĩa là mô hình giỏi hơn người chấm.
    - Hoặc ví dụ về việc hạ ngưỡng phát hiện: Hạ ngưỡng $\theta = 0.10$ (mô hình L1 đã khoá, validation) giúp tìm được 70% nhãn Ineffective, so với 45% khi dùng argmax.
      - Đổi lại, cứ mỗi ca bắt thêm thì có khoảng 8 cảnh báo nhầm, và Macro-F1 giảm từ 0.581 xuống 0.535.
      - Ngưỡng là lựa chọn của người dùng, không làm mô hình tốt hơn.
  - Tuyên bố phạm vi ứng dụng: Công cụ này dùng để hỗ trợ giáo viên sắp xếp thứ tự đọc bài nhanh hơn, **tuyệt đối không dùng để chấm điểm tự động học sinh**.
  - Lời cảm ơn và kết thúc bài thuyết trình.

---

## 3. KHO TÀI NGUYÊN HÌNH ẢNH & SỐ LIỆU CHUNG (ASSET POOL)
*(Người làm video có thể tự do chọn các hình ảnh và bảng số liệu dưới đây để đưa vào bài nói)*

### A. Danh mục hình ảnh có sẵn (Độ phân giải 300 DPI tại `MLA_Final/Results/figures/`):
1. **Tổng quan & Luồng bài toán:**
   - `fig01_user_decision_workflow.png`: Luồng hỗ trợ giáo viên ra quyết định đọc và chữa bài.
   - `fig02_data_pipeline_split.png`: Luồng tiền xử lý, lọc dòng thiếu và phân chia tập 80/20 theo bài.
   - `fig03_ml_pipeline.png`: Pipeline mô hình hoá của **mọi** hệ thống (Majority, LR/RF trên Feature Set B, DeBERTa). Bộ biến đổi đặc trưng chỉ fit trên train; mọi hệ thống chấm trên cùng đơn vị, cùng thước đo.
   - `fig26_test_governance.png`: Quy trình quản trị tập test độc lập (chấm 1 lần duy nhất với file khoá).
2. **Khảo sát dữ liệu & Biến nhiễu độ dài:**
   - `fig05_label_distribution_by_split.png`: Phân bố mất cân bằng nhãn trên các tập train/val/test.
   - `fig08_unit_length_by_label.png`: Phân bố số lượng từ của từng loại nhãn.
   - `fig09_essay_length_vs_holistic_score.png`: Tương quan chặt chẽ giữa độ dài bài và điểm tổng thể (Spearman 0.76).
   - `fig20_error_within_score_by_length.png`: Tỷ lệ lỗi trong cùng mức điểm phân theo 4 nhóm độ dài.
3. **Hiệu năng mô hình & Cắt bỏ ngữ cảnh:**
   - `fig12_per_class_results_val_test.png`: F1 từng lớp và Macro-F1 giữa các họ mô hình.
   - `fig13_confusion_matrices_test.png`: Ma trận nhầm lẫn 3x3 trên tập test chính thức.
   - `fig04_context_levels.png`: Thang biểu diễn các cấp độ ngữ cảnh (L0, L1, paragraph, source, full essay).
   - `fig14_L1_minus_L0_per_class.png`: Mức cải thiện của L1 so với L0 **theo từng lớp nhãn** (Macro-F1, F1 Ineffective/Adequate/Effective) trên validation và test, kèm khoảng tin cậy 95%. Số theo **loại luận điểm** (Counterclaim +0.037…) nằm ở Bảng 6.4 / `R4a_L1_vs_L0_same_units_deltas.csv`, không có trong hình này.
   - `fig22_threshold_tradeoff.png`: Đánh đổi giữa độ bao phủ (Recall) và cảnh báo nhầm khi đổi ngưỡng $\theta$.
4. **Khái quát hóa trên đề mới & Phân tích lỗi:**
   - `fig16_prompt_coverage_indomain_vs_lopo.png`: Mức độ phủ 15 đề giữa in-domain và LOPO.
   - `fig17_lopo_vs_indomain_same_units.png`: So sánh hiệu năng LOPO và in-domain trên cùng các bài validation.
   - `fig23_ten_cases_by_context_level.png`: Kết quả dự đoán của các cấp ngữ cảnh trên 10 ca lỗi Ineffective.
   - `fig24_rater_rater_vs_model_rater_agreement.png`: Đặt cạnh nhau hai đại lượng **khác nhau**: $\kappa$ người–người (0.316, độ tin cậy của nhãn) và $\kappa$ mô hình–nhãn đã phân xử (0.372). Không so trực tiếp, không kết luận mô hình giỏi hơn người.

### B. Các bảng số liệu cốt lõi (Xem file CSV tại `MLA_Final/Results/tables/`):
- **Bảng 1 (So sánh mô hình trên tập Test):**
  - Majority Baseline: Macro-F1 = 0.297 | Accuracy = 80.5% | Ineffective F1 = 0.000
  - Random Forest (Feature Set B): Macro-F1 = 0.510 | Accuracy = 78.5% | Ineffective F1 = 0.202 (Recall 17.2%)
  - DeBERTa-v3 L0 (chỉ câu): Macro-F1 = 0.561 | Accuracy = 74.4% | Ineffective F1 = 0.339
  - DeBERTa-v3 L1 (kèm câu trước sau): Macro-F1 = **0.577** | Accuracy = 75.7% | Ineffective F1 = **0.368** (Recall 41.5%)
- **Bảng 2 (Độ chênh Level 1 − Level 0 trên cùng đơn vị):**
  - Test Macro-F1 delta: **+0.0159** [95% CI: +0.0115, +0.0205]
  - Test Ineffective F1 delta: **+0.0292**
  - Loại tăng mạnh nhất: Counterclaim (+0.037), Rebuttal (+0.028), Claim (+0.028)
- **Bảng 3 (Độ hụt khi sang đề mới - LOPO):**
  - A Cowboy Who Rode the Waves: sụt **−0.092** Macro-F1 (từ 0.476 xuống 0.384)
  - Distance learning: sụt **−0.048** Macro-F1 (từ 0.576 xuống 0.528)
  - Summer projects: sụt **−0.025** Macro-F1 (từ 0.508 xuống 0.483)

---

## 4. HƯỚNG DẪN THỰC HIỆN PHẦN DEMO THỰC TẾ TRONG VIDEO

Trong phần 3 (từ 1:30 đến 2:45), người thuyết trình cần quay trực tiếp màn hình máy tính. Có 2 cách thực hiện rất dễ:

### Cách 1: Chạy script kiểm chứng 1-lệnh trong Terminal (Khuyến nghị, nhanh nhất)
1. Mở Terminal (PowerShell / Command Prompt / VS Code Terminal).
2. Di chuyển vào thư mục: `cd MLA_Final/Code`
3. Chạy lệnh: `python reproduce_results.py`
4. Màn hình sẽ chạy và in ra toàn bộ Bảng 1, Bảng 2, Bảng 3 trong khoảng 5 giây. Người nói dùng chuột trỏ vào các hàng số liệu để diễn giải.

### Cách 2: Mở một Notebook đã chạy sẵn kết quả
- Mở một trong các Jupyter Notebook có sẵn trong `MLA_Final/Code/notebooks/`:
  - `01_deberta_prompt_aware_official_test.ipynb` (quá trình chấm test chính thức của DeBERTa).
  - `02_lopo_rerun_deberta_L0.ipynb` (đánh giá trên đề mới).
  - `03_random_forest_official_test.ipynb` (huấn luyện và đánh giá Random Forest).
- Cuộn đến đoạn code nạp dữ liệu và bảng ma trận nhầm lẫn / kết quả đánh giá để thuyết minh.

---

## 5. MẪU PROMPT CHUNG ĐỂ GIAO CHO AI KHÁC SINH SCRIPT CHI TIẾT

Khi bạn hoặc người khác muốn đưa tài liệu này vào một mô hình AI khác để tự động viết kịch bản chi tiết (lời thoại tiếng Anh từng câu + mô tả slide), hãy sử dụng mẫu prompt sau.

> **Bắt buộc:**
> - Nếu dùng AI để viết script, mỗi người ghi vào `AI_Log/AI_Use_Log.md`: dùng ở đâu, công cụ nào, và **bạn đã tự kiểm tra hoặc sửa gì**, đặc biệt là đối chiếu mọi con số với `MLA_Final/Results/tables/`.
> - Lời nói trong video vẫn phải là giọng của chính bạn, không dùng TTS.

```text
PROMPT:
You are an expert academic presentation coach. Write a complete, timed 5-minute English spoken presentation script for an individual student presentation in an advanced Machine Learning course.

Student Name: [Điền tên sinh viên]
Student ID: [Điền mã sinh viên]
Group: Group 06, Class CLC02
Paper Title: Predicting the Effectiveness of Argumentative Discourse Units in Student Essays
My specific role/contribution: [Mô tả ngắn gọn vai trò hoặc phần việc của bạn]

Requirements:
1. Follow the exact 5-part timeline specified in "requirement video.md":
   - Part 1: Self-Introduction & Problem Context (0:00 - 0:45)
   - Part 2: Personal Ownership & Methodology (0:45 - 1:30)
   - Part 3: Live Demo & Example Walkthrough (1:30 - 2:45)
   - Part 4: Key Results & Visualizations (2:45 - 4:00)
   - Part 5: Error Analysis, Limitations & Conclusion (4:00 - 5:00)
2. Total word count: around 650 - 700 spoken English words.
3. For each part, include:
   - [Slide / Visual Cue]: specify which figure from the Asset Pool in "requirement video.md" to display.
   - [On-screen Action]: describe what to show on screen (slides or live terminal/notebook demo).
   - [Spoken Script]: the exact words to speak in natural, professional academic English.
4. Use the exact numbers from the Asset Pool (Macro-F1 0.577, L1 delta +0.016, class imbalance 4.5%, rater kappa 0.316).
5. Use cautious wording: "suggests" / "is consistent with", never "proves". Do not compare the rater-rater kappa (0.316) directly with the model-label kappa (0.372). Do not present the source-based-prompt explanation of the LOPO drop as a tested cause.
6. Claim only my own work with "I"; describe teammates' work as "my teammate" or "the group".
```
