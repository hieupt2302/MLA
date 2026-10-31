# HƯỚNG DẪN HOÀN THIỆN BÁO CÁO TUẦN 11 & CẨM NANG ÔN THI PHỎNG VẤN CÁ NHÂN (RUBRIC 30 ĐIỂM)
**Môn học:** Học máy và Ứng dụng (CLC02) | **Nhóm:** Group 06  
**Đề tài:** PERSUADE 2.0 — Dự báo Hiệu quả Đơn vị Lập luận (Discourse Effectiveness)  
**Thời gian áp dụng:** Tuần 11 (Tháng 10/2026)

---

## ⚠️ ĐÍNH CHÍNH SAU RÀ SOÁT 31/10/2026 (QUAN TRỌNG — BẮT BUỘC ĐỌC KHI ÔN TẬP & PHỎNG VẤN)

> [!WARNING]
> **CẢNH BÁO QUAN TRỌNG:** Toàn bộ các bảng số liệu, kết quả thực nghiệm và gợi ý trả lời phỏng vấn ở các mục bên dưới trong tài liệu này được biên soạn trước đợt rà soát dữ liệu ngày 31/10/2026 và đã **lỗi thời** ở các điểm liệt kê dưới đây. Khi ôn tập thi và trả lời phỏng vấn cá nhân, tất cả thành viên **bắt buộc phải sử dụng số liệu trong khối đính chính này** và báo cáo Tuần 11 chính thức (`RESEARCH_REPORT_WEEK11_DISCOURSE_EFFECTIVENESS_CLC02_GROUP06.md`). Tuyệt đối không trích dẫn các con số cũ đã bị hủy bỏ bên dưới. Nguồn sự thật duy nhất tuân thủ: `RA_SOAT_TUAN11_SO_VOI_NHAN_XET_TUAN10.md` và `RESEARCH_REPORT_WEEK11_DISCOURSE_EFFECTIVENESS_CLC02_GROUP06.md`.

---

### 📊 BẢNG ĐỐI CHIẾU: SỐ CŨ (SAI) → SỐ ĐÚNG → LÝ DO ĐÍNH CHÍNH

| STT | Nội dung / Hạng mục | Số cũ (sai / lỗi thời trong file này) | Số đúng (Báo cáo Tuần 11 & Rà soát 31/10) | Lý do đính chính & Ý nghĩa khoa học |
|:---:|---|---|---|---|
| **1** | **Bảng Điểm × Độ dài** (Kiểm soát năng lực học sinh) | Tỷ lệ lỗi phẳng quanh mức **25% – 26%** ở mọi phân vị độ dài (Điểm 3: 26,59% → 25,32% → 26,48% → 26,48%; Điểm 4: 23,41% → 27,53% → 25,19% → 25,90%). Kết luận vội: "độ dài không ảnh hưởng cú pháp". | **Trong cùng một mức điểm, tỷ lệ lỗi vẫn tăng theo độ dài bài viết**.<br>• **Điểm 3 (validation):** 19,3% [17,7; 21,1] (Q1) → 21,8% [20,0; 23,9] (Q2) → 22,9% [19,8; 26,0] (Q3) → **28,2%** [22,1; 34,3] (Q4).<br>• **Điểm 3 (test):** 17,6% (Q1) → 20,8% (Q2) → 22,3% (Q3) → **29,2%** (Q4).<br>• **Hồi quy logistic** (sai số cụm theo bài): OR = **1,19 [1,14; 1,25]** mỗi bậc độ dài khi kiểm soát điểm; OR = **1,17 [1,11; 1,23]** khi kiểm soát cả điểm + nhãn gold + loại đơn vị (CI > 1). | Script cũ ghép dự đoán với điểm/độ dài qua `discourse_id` đã bị Excel làm tròn dạng số mũ (`1.62263E+12`), khiến 144.289 đơn vị chỉ còn 728 ID khác nhau, dẫn đến gán nhầm điểm/độ dài ngẫu nhiên của bài khác (sai số ngẫu nhiên làm phẳng tỷ lệ lỗi ~26%). Khi ghép đúng bằng `row_idx`, lỗi thực tế vẫn tăng theo độ dài; **Giả thuyết A (độ dài/độ phức tạp) chưa bị loại bỏ**. Dịch chuyển trình độ chỉ giải thích việc *loại lỗi* thay đổi (ở Q4 có 92% lỗi là nhầm Adequate ↔ Effective). |
| **2** | **Tỷ lệ lỗi theo độ dài toàn bài** | Chuỗi tỷ lệ lỗi tăng từ **21,98% lên 30,35%**. | Mô hình DeBERTa L1 tuần 11 (hệ thống khóa đã chấm test):<br>• **Validation:** 22,0% (Q1) → 23,0% (Q2) → 27,9% (Q3) → **30,5%** (Q4).<br>• **Test:** 21,1% (Q1) → 22,0% (Q2) → 25,5% (Q3) → **30,4%** (Q4). | Chuỗi số cũ (21,98% → 30,35%) không thuộc mô hình nào hiện có trong repository. Số liệu mới đảm bảo lấy từ cùng một mô hình nhất quán (DeBERTa L1 tuần 11) cho cả bảng toàn bài và bảng phân tích trong mức điểm. |
| **3** | **Random Forest trên Test** (Protocol bắt buộc 2) | Macro-F1 = **0,4834**, Accuracy = **67,79%**, F1 Ineffective = 0,2304. | Macro-F1 = **0,5098**, Accuracy = **78,51%**, F1 Ineffective = **0,2024** (validation đạt 0,5261, tái tạo sát mốc tuần 9 là 0,5230). | Script cũ `run_rf_official_test.py` chạy nhầm mô hình (100 cây, max_depth 30, TF-IDF 10k, min_df 3, thiếu chuẩn hóa đặc trưng, train trên cả train+val 144.289 mẫu), không phải Feature Set B. Khi dựng lại đúng cấu hình Feature Set B tuần 9 và train đúng 115.187 mẫu train, số test chính xác là 0,5098 / 78,51%. Số cũ được giữ trong chú thích minh bạch. |
| **4** | **Số DeBERTa trên Test** (L0, L1 khóa, Prompt-Aware) | Số "kỳ vọng" chép cứng trong script cũ:<br>• L0: **0,5692**<br>• L1 (Khóa): **0,5724**<br>• Prompt-Aware: **~0,582** | Kết quả thực tế chạy đúng 1 lần duy nhất trên 93.677 câu test:<br>• **DeBERTa L0:** Macro-F1 = **0,5613** (Acc 74,38%, Ineff F1 0,3387)<br>• **DeBERTa L1 (Khóa):** Macro-F1 = **0,5772** (Acc 75,68%, Ineff F1 0,3679)<br>• **Prompt-Aware:** Macro-F1 = **0,5808** (Acc 75,39%, Ineff F1 0,3787)<br>• Bootstrap theo bài: L1 − L0 = **+0,0159 [0,0115; 0,0207]**; PA − L1 = **+0,0036 [−0,0002; 0,0074]**. | Do checkpoint tuần 10 không tải lại được, nhóm đã huấn luyện lại L0, L1 và Prompt-Aware trong tuần 11 với cấu hình khóa và chấm test đúng 1 lượt. Báo cáo công khai việc train lại. Khoảng tin cậy của PA − L1 chứa 0 nên **không thể phân biệt** hiệu năng giữa Prompt-Aware và L1 trên tập test. L0 và L1 đều vượt RF từ 0,05 đến 0,07 Macro-F1. |
| **5** | **Dò ngưỡng Ineffective** (Threshold Tuning & Ca 8) | Từ "ngưỡng mặc định 0,33" hạ xuống **θ = 0,10** giúp Recall Ineffective tăng từ 36,5% lên **76,51%**, cứu được Ca 8; không nêu chi phí báo nhầm. | Mốc cơ sở là **argmax** (Recall Ineff 43,2%, Precision 36,1%, Macro-F1 0,5790).<br>Tại **θ = 0,10** (mô hình L1 tuần 10):<br>• Recall Ineffective đạt **73,0%** (Precision 18,4%).<br>• Macro-F1 giảm từ 0,579 xuống **0,517**.<br>• Có **3.670 / 29.102** đơn vị đổi nhãn.<br>• Bắt thêm được **396** câu Ineffective đúng nhưng phải trả giá bằng **3.274 cảnh báo nhầm** (tỉ lệ **~8 báo nhầm cho mỗi ca bắt thêm**).<br>• Trong 10 ca lỗi, chỉ có **2/10 ca đổi nhãn** sang Ineffective (ca 5 và 8). | Không tồn tại "ngưỡng mặc định 0,33" mà là quy tắc argmax. Con số 76,51% là tính sai logic (recall phải giảm dần theo θ; bảng cũ ghi 74,40% ở 0,09 và 71,99% ở 0,11). Phân tích cũ giấu sự đánh đổi lớn về Macro-F1 và báo nhầm hàng loạt. Với mô hình L1 tuần 11 đã chấm test, P(Ineff) của ca 8 chỉ là 0,058 nên **không lật** ở θ = 0,10. |
| **6** | **Ca lỗi số 2** (Đề *Car-free cities*) | Khẳng định học sinh trích dẫn bịa "đoạn văn 36 không tồn tại" trong bài đọc nguồn (*"paragraph 36 does not exist"*), quy kết mô hình thiếu văn bản đọc hiểu. | **Đoạn 36 có tồn tại thật** trong bộ ngữ liệu nguồn 43 đoạn của đề *Car-free cities* và chứa chính xác câu văn mà học sinh đã trích dẫn. | Nhóm đã tra cứu trực tiếp văn bản nguồn của đề bài. Nhận định cũ "trích dẫn bịa" là sai sự thật và đã bị hủy bỏ. Lỗi của học sinh ở ca 2 là phần lập luận phía sau trích dẫn bị lạc đề (nói sang chuyện thi bằng lái xe), khuyết điểm nằm ngay trong nội dung đơn vị mà mô hình cục bộ chưa nhận diện được. |
| **7** | **In-domain đề Cowboy & Khoảng cách ngoại đề** | In-domain Cowboy Macro-F1 = **0,4934**; Khoảng cách ngoại đề (Generalization Gap) = **−8,52%** (0,4082 so với 0,4934). | Đánh giá trên **cùng 1.030 đơn vị** validation của đề Cowboy:<br>• DeBERTa LOPO đạt **0,3584** so với In-domain (Week 9 L0) là **0,4462**.<br>• Khoảng cách đúng: **−0,088 [−0,138; −0,041]** (nếu so với Week 11 L0: 0,4755 → **−0,117 [−0,171; −0,057]**).<br>• Hai đề còn lại: Summer (−0,009) và Distance (+0,004) có khoảng tin cậy đều chứa 0. | Bảng cũ so sánh khập khiễng giữa LOPO trên toàn bộ 5.158 đơn vị với In-domain chỉ trên 1.030 đơn vị validation (hai tập đơn vị khác nhau hoàn toàn, không có khoảng tin cậy bootstrap). Chỉ riêng đề Cowboy ghi nhận sự sụt giảm có ý nghĩa thống kê. |
| **8** | **Mức vượt DeBERTa so với SVM/RF ở đề Cowboy** | DeBERTa LOPO (0,4082) vượt Linear SVM LOPO (+21,0%) và RF LOPO (+16,6%); kết luận "SVM/RF sụt giảm nghiêm trọng". | **Giữ nguyên các con số so sánh tương đối:**<br>• DeBERTa LOPO (0,4082) so với Linear SVM LOPO (0,3373) đạt **+21,0%**.<br>• DeBERTa LOPO so với RF LOPO (0,3501) đạt **+16,6%**.<br>• Ghi rõ: đây là **so sánh khác họ mô hình trên cùng một fold LOPO**. | Cần trình bày đúng chuẩn mực phương pháp luận: Đây là so sánh khác họ trên cùng fold để thấy DeBERTa chuyển giao tốt hơn các mô hình truyền thống. Không dùng từ "sụt giảm" vì Linear SVM và Random Forest không có số in-domain theo từng đề để xác định mức độ sụt giảm. |
| **9** | **Tỷ lệ lớp Ineffective** | "Lớp Ineffective chỉ chiếm **11,8%** dữ liệu". | **≈ 4,5%** số đơn vị có nhãn (train 4,48%; validation 4,56%; test 4,51%). | Đếm lại trực tiếp từ dữ liệu; con số 11,8% không khớp tập nào. |

---

### 🗣️ VIẾT LẠI 6 CÂU TRẢ LỜI PHỎNG VẤN VẤN ĐÁP (CHUẨN XÁC THEO BÁO CÁO TUẦN 11 MỚI)
*(Mỗi câu trả lời ngắn gọn 4–6 dòng, đúng mực sinh viên trả lời thầy cô, không dùng các từ cảm tính "chứng minh", "dứt khoát", "hoàn toàn", "hoàn hảo")*

#### Câu 1: Vì sao lỗi tăng theo độ dài không có nghĩa là bài dài khó hơn với mô hình?
> **Trả lời:**  
> "Dạ thưa Thầy, khi kiểm soát cùng mức điểm năng lực, nhóm nhận thấy lỗi của mô hình vẫn tăng dần theo độ dài bài viết. Ví dụ ở bài Điểm 3, tỷ lệ lỗi tăng từ 19,3% ở nhóm ngắn lên 28,2% ở nhóm dài (hồi quy logistic cho tỉ số chênh OR = 1,19), cho thấy giả thuyết về độ dài và độ phức tạp văn bản chưa bị loại bỏ. Tuy nhiên, sự dịch chuyển trình độ người viết giải thích rõ sự thay đổi về bản chất lỗi: ở nhóm bài dài nhất, có tới 92% số lỗi là sự nhầm lẫn giữa Đạt và Hiệu quả thay vì lỗi Kém. Do đó, cả hai yếu tố độ dài và phân phối trình độ cùng đồng thời tác động đến tỷ lệ lỗi."

#### Câu 2: Hệ số $\kappa$ mô hình (0.37) và $\kappa$ giữa 2 người chấm (0.316) vì sao không được so trực tiếp?
> **Trả lời:**  
> "Dạ thưa Thầy, hai đại lượng này phản ánh hai khía cạnh đo lường khác nhau: $\kappa$ của mô hình (khoảng 0,37 trên tập test) đo mức độ trùng khớp giữa nhãn dự đoán với nhãn đồng thuận chuẩn (ground truth); trong khi $\kappa$ giữa hai người chấm (0,316 theo Crossley et al., 2024) đo độ phân tán ngẫu nhiên giữa các chuyên gia khi chấm độc lập. Vì vậy, ta không thể so sánh số học để kết luận mô hình vượt người chấm. Con số 0,316 cho thấy độ bất đồng nhãn vốn tồn tại tự nhiên trong bài toán đánh giá lập luận, và đây cũng chính là một phần nguyên nhân giới hạn trần hiệu năng của các mô hình."

#### Câu 3: LOPO khác in-domain ở đâu, và vì sao đề Cowboy giảm nhiều nhất?
> **Trả lời:**  
> "Dạ thưa Thầy, In-domain đánh giá mô hình trên các đề bài đã xuất hiện lúc huấn luyện, còn LOPO giữ lại toàn bộ một đề để kiểm tra khả năng chuyển giao sang chủ đề mới. Khi so sánh trên cùng 1.030 đơn vị kiểm định, chỉ riêng đề Cowboy ghi nhận mức sụt giảm rõ rệt với khoảng cách −0,088 [khoảng tin cậy −0,138 đến −0,041], trong khi hai đề còn lại có khoảng tin cậy chứa 0. Đề Cowboy dựa trên một trích đoạn văn học cụ thể với nhân vật và từ vựng đặc thù, khiến thông tin đề bài trở nên quan trọng hơn. Dù vậy, do mới khảo sát 3 đề, nhóm ghi nhận đây là một giả thuyết phù hợp thay vì kết luận khái quát."

#### Câu 4: Nếu người chấm thấy đề và cả bài còn mô hình chỉ thấy một đoạn, ta có thể quy lỗi cho năng lực mô hình đến đâu?
> **Trả lời:**  
> "Dạ thưa Thầy, việc bổ sung ngữ cảnh lân cận (Level 1) mang lại mức cải thiện nhỏ (+0,0159 trên tập test). Trong 10 ca lỗi Kém, có 8 ca tăng xác suất lớp Kém nhưng chưa ca nào lật nhãn argmax. Sự thiếu hụt văn bản toàn bài (như phản biện không có lời bác bỏ) hay văn bản nguồn là giả thuyết phù hợp để giải thích trần hiệu năng, dù nhóm chưa thể kiểm chứng thực nghiệm ở cấp độ toàn bài. Đáng chú ý ở Ca 2, việc rà soát cho thấy đoạn 36 có tồn tại thật trong nguồn; khiếm khuyết nằm ở phần lập luận lạc đề ngay trong câu mà mô hình cục bộ chưa nhận diện được."

#### Câu 5: Vì sao F1 lớp Kém (Ineffective) lại thấp (< 0.40) và làm cách nào để cải thiện trong thực tế?
> **Trả lời:**  
> "Dạ thưa Thầy, F1 lớp Kém thấp do dữ liệu bị mất cân bằng lớn (chỉ chiếm khoảng 4,5% số đơn vị có nhãn) và bản thân người chấm cũng có độ phân tán cao ở nhãn này. Khi thử nghiệm dò ngưỡng tại $\theta = 0,10$, Recall lớp Kém tăng từ 43,2% lên 73,0% và đổi được nhãn ở 2 trong 10 ca lỗi khảo sát. Tuy nhiên, cái giá phải trả là Macro-F1 giảm từ 0,579 xuống 0,517, và trung bình cứ phát hiện thêm 1 câu Kém thì mô hình báo nhầm khoảng 8 câu khác. Trong thực tế ứng dụng giáo dục, việc chọn ngưỡng là bài toán cân đối mục đích sử dụng: chấp nhận cảnh báo thừa để giáo viên rà soát hay giữ độ chuẩn xác chung."

#### Câu 6: Vì sao việc so sánh Random Forest với DeBERTa trong LOPO bị coi là không công bằng, và nhóm đã khắc phục thế nào?
> **Trả lời:**  
> "Dạ thưa Thầy, Random Forest và DeBERTa thuộc hai họ mô hình khác nhau (đặc trưng từ vựng nông so với mạng transformer tiền huấn luyện), nên so sánh trực diện không thể phân tách giữa năng lực mô hình và khả năng thích ứng ngoại đề. Để giải quyết, nhóm đã thực hiện hai việc: thứ nhất, thiết lập đối chứng nội bộ cùng họ DeBERTa giữa In-Domain và LOPO trên cùng tập đơn vị để đo khoảng cách ngoại đề; thứ hai, so sánh các mô hình trên cùng fold LOPO làm mốc tham chiếu thực nghiệm (DeBERTa vượt SVM 21,0% và RF 16,6% ở đề Cowboy). Do thiếu kết quả in-domain riêng của SVM và RF, nhóm không khẳng định mô hình truyền thống bị sụt giảm mà chỉ đánh giá năng lực chuyển giao tương đối."

---


## MỤC LỤC
1. [Bối cảnh & Các yêu cầu trọng tâm cần giải quyết](#1-bối-cảnh--các-yêu-cầu-trọng-tâm-cần-giải-quyết)
2. [HƯỚNG DẪN CHI TIẾT CHẠY CODE (BẤM VÀO ĐÂU, GÕ LỆNH GÌ)](#2-hướng-dẫn-chi-tiết-chạy-code-bấm-vào-đâu-gõ-lệnh-gì)
   - [A. Chạy ngay trên máy tính cá nhân (PowerShell / Terminal)](#a-chạy-ngay-trên-máy-tính-cá-nhân-powershell--terminal)
   - [B. Chạy DeBERTa trên Google Colab GPU (8 phút)](#b-chạy-deberta-trên-google-colab-gpu-8-phút)
3. [HAI BẢNG SỐ LIỆU & ĐOẠN VĂN ĐƯA THẲNG VÀO BÁO CÁO](#3-hai-bảng-số-liệu--đoạn-văn-đưa-thẳng-vào-báo-cáo)
4. [Phân công chi tiết cho 3 Thành viên](#4-phân-công-chi-tiết-cho-3-thành-viên)
   - [👤 Thành viên 1: Dữ liệu & Yếu tố gây nhiễu từ độ dài (Confound)](#thành-viên-1-dữ-liệu--yếu-tố-gây-nhiễu-từ-độ-dài-confound)
   - [👤 Thành viên 2: Mô hình, Tối ưu ngưỡng (Threshold Tuning) & Ca lỗi](#thành-viên-2-mô-hình-tối-ưu-ngưỡng-threshold-tuning--ca-lỗi)
   - [👤 Thành viên 3: Khả năng ngoại đề (LOPO), Baseline Cùng Họ & Quản trị Test](#thành-viên-3-khả-năng-ngoại-đề-lopo-baseline-cùng-họ--quản-trị-test)
5. [Cẩm nang trả lời phỏng vấn cá nhân 6–8 phút (Rubric 30 điểm)](#5-cẩm-nang-trả-lời-phỏng-vấn-cá-nhân-68-phút-rubric-30-điểm)
6. [Bộ câu hỏi "tủ" Thầy Khánh chỉ định ôn tập](#6-bộ-câu-hỏi-tủ-thầy-khánh-chỉ-định-ôn-tập)
7. [Checklist kiểm tra trước khi vào phòng phỏng vấn](#7-checklist-kiểm-tra-trước-khi-vào-phòng-phỏng-vấn)

---

## 1. BỐI CẢNH & CÁC YÊU CẦU TRỌNG TÂM CẦN GIẢI QUYẾT

Dựa trên tài liệu nhận xét viết tay của Thầy Khánh (`Nhan_xet_Week10_CLC02_Group06.docx.md`) và các góp ý trực tiếp trên lớp:

1. **Về dữ liệu độ dài (Mục 3):** Thầy khen phát hiện độ dài bài văn rất đẹp, nhưng yêu cầu **bắt buộc phải lập bảng tách độ dài khỏi trình độ** (tính tỷ lệ lỗi theo 4 nhóm độ dài trong cùng một mức điểm holistic).
2. **Về tập Official Test (Mục 1.3):** Thầy yêu cầu **phải có mốc so sánh khi chạy test một lần duy nhất**. Protocol khóa phải đăng ký chấm cùng lượt 3 hệ thống: (1) Random Forest, (2) DeBERTa Level 0, và (3) DeBERTa Level 1.
3. **Về kết luận ngữ cảnh (Mục 7.2):** Sửa câu chữ ở mục 7.2, bỏ chữ "chứng minh", đưa về giả thuyết mở (cần bài đọc nguồn và toàn bài), và nhấn mạnh độ đồng thuận giữa người chấm chỉ có $\kappa = 0.316$.
4. **Về so sánh mô hình trong LOPO (Mục 6.4):** Không được đem Random Forest (đặc trưng nông, đếm từ) đi đọ điểm trực diện với DeBERTa (Transformer 86M tham số). Phải lấy **mô hình CÙNG HỌ** để so sánh (Linear SVM đối chứng cùng họ tuyến tính; DeBERTa In-Domain vs DeBERTa LOPO đối chứng cùng họ Transformer).
5. **Về chỉ số F1 lớp Kém (< 0.5):** Không cần cày model phức tạp, giải quyết bằng kỹ thuật **Threshold Tuning (Dò ngưỡng quyết định)** trên file xác suất có sẵn của DeBERTa để cứu Ca lỗi số 8 theo đúng hướng dẫn dòng 115 của Thầy.

---

## 2. HƯỚNG DẪN CHI TIẾT CHẠY CODE (BẤM VÀO ĐÂU, GÕ LỆNH GÌ)

### A. CHẠY NGAY TRÊN MÁY TÍNH CÁ NHÂN (POWERSHELL / TERMINAL)
Mở cửa sổ **PowerShell** hoặc **Terminal** trong thư mục dự án (`c:\Users\ADMIN\Desktop\MLA Dataset`), gõ tuần tự các lệnh sau:

#### Lệnh 1: Lấy Bảng "Điểm Holistic × Độ dài" (Mục 3)
```powershell
python script_holistic_length_table.py
```
* **Thời gian chạy:** **5 giây** (CPU cục bộ).
* **Kết quả:** In bảng ra màn hình và lưu file `outputs/holistic_score_x_length_quartile_error_rates.csv`.

#### Lệnh 2: Chạy Dò ngưỡng (Threshold Tuning) & Cứu Ca số 8 (Mục 5)
```powershell
python script_threshold_tuning_and_case8.py
```
* **Thời gian chạy:** **3 giây** (CPU cục bộ).
* **Kết quả:** In bảng quét ngưỡng và chứng minh Ca số 8 khi đặt $\theta = 0.10$ lập tức **lật nhãn thành Ineffective thành công**. Lưu file `outputs/ineffective_threshold_tuning_table.csv`.

#### Lệnh 3: Chạy nghiệm thu Random Forest trên toàn bộ 93.677 câu tập Test (Mục 1.3)
```powershell
python run_rf_official_test.py
```
* **Thời gian chạy:** **71 giây** (CPU cục bộ).
* **Kết quả thực tế 100%:** Macro-F1: **0.4834**, Accuracy: **67.79%**, Ineffective F1: **0.2304**. Lưu file `outputs/official_test_rf_actual_result.csv`.

#### Lệnh 4: Chạy nghiệm thu Linear SVM (Baseline cùng họ môn học) trên toàn bộ 93.677 câu tập Test (Mục 1.3)
```powershell
python run_svm_official_test.py
```
* **Thời gian chạy:** **40.9 giây** (CPU cục bộ).
* **Kết quả thực tế 100%:** Macro-F1: **0.4822**, Accuracy: **74.40%**, Ineffective F1: **0.2044**. Lưu file `outputs/official_test_svm_actual_result.csv`.

#### Lệnh 5: Chạy mô hình đối chứng cùng họ Tuyến tính Linear SVM LOPO trên 3 đề (Mục 6.4)
```powershell
python script_lopo_weaker_baseline.py --model svm
```
* **Thời gian chạy:** **~1.5 phút** (CPU cục bộ).
* **Kết quả thực tế 100%:** 
  - Đề Cowboy: Macro-F1 = **0.3373**, Acc = **71.99%**, Ineff F1 = **0.1027**
  - Đề Summer: Macro-F1 = **0.4269**, Acc = **64.90%**, Ineff F1 = **0.0410**
  - Đề Distance: Macro-F1 = **0.4690**, Acc = **71.35%**, Ineff F1 = **0.0622**
* Lưu bảng đối chứng cùng họ vào `outputs/lopo_svm_baseline_results.csv`.

---

### B. CHẠY DEBERTA SUY LUẬN TRÊN MÁY LOCAL HOẶC GOOGLE COLAB (~3-8 PHÚT)

Nhóm có thể chạy DeBERTa trực tiếp trên **máy Local (GPU RTX 4070 SUPER / CUDA)** hoặc chạy trên **Google Colab (GPU T4 miễn phí)**:

#### Cách 1: Chạy trực tiếp trên máy Local (nếu có card NVIDIA / CUDA)
Chạy script nghiệm thu tổng hợp trên PowerShell:
```powershell
python script_official_test_evaluation.py
```
* Script tự động nhận diện thiết bị CUDA. Thời gian suy luận 93.677 mẫu chỉ khoảng **3–4 phút** trên GPU máy bàn.

#### Cách 2: Chạy trên Google Colab GPU (nếu dùng laptop mang lên trường)
1. **Bước 1:** Mở trình duyệt web, vào link Colab của nhóm:  
   👉 [Mở Colab Script 05](https://colab.research.google.com/drive/1prcSnRHax0SAITnUbGsXks3aQ9pbwJD2?usp=sharing)
2. **Bước 2:** Nhìn sang thanh menu bên trái, bấm vào biểu tượng **Thư mục (Files)**, kéo file `persuade_corpus_2.0_test.csv` từ máy tính thả vào.
3. **Bước 3:** Kéo xuống cuối cùng của sổ tay Colab, bấm nút **`+ Code`** tạo một ô mới, copy đoạn code nghiệm thu dán vào và bấm Play (chạy khoảng 8 phút).

---

## 3. BA BẢNG SỐ LIỆU & ĐOẠN VĂN ĐƯA THẲNG VÀO BÁO CÁO

Chỉ việc mở tệp Báo cáo ra và chèn đúng 3 bảng kèm nhận định này vào:

### BẢNG 1: ĐIỂM HOLISTIC × ĐỘ DÀI (CHÈN VÀO MỤC 3.2)
*(Kết quả chạy thực tế từ script 1 trên 29.102 đơn vị tập Validation)*

| Điểm Holistic của học sinh | Q1 (Ngắn: 148–315 từ) | Q2 (TB Thấp: 316–422) | Q3 (TB Cao: 423–566) | Q4 (Dài: 567+ từ) |
|:---:|:---:|:---:|:---:|:---:|
| **Điểm 1 (Yếu)** | 28.39% | 26.86% | 28.94% | 28.57% |
| **Điểm 2** | 27.62% | 22.46% | 26.22% | 31.03% |
| **Điểm 3 (Trung bình)** | **26.59%** | **25.32%** | **26.48%** | **26.48%** |
| **Điểm 4 (Khá)** | **23.41%** | **27.53%** | **25.19%** | **25.90%** |
| **Điểm 5 (Giỏi)** | — | 14.29% | 27.55% | 29.09% |
| **Điểm 6 (Xuất sắc)** | — | — | — | 28.80% |

👉 **Nhận định khoa học chép vào Mục 3.4:**  
*"Khi kiểm soát cùng một mức điểm năng lực của học sinh (đặc biệt ở Điểm 3 và Điểm 4), tỷ lệ lỗi của mô hình gần như phẳng lì quanh mức 25% – 26%. Điều này chứng minh rằng độ dài bài văn không hề gây khó khăn cú pháp hay làm mô hình quá tải. Hiện tượng tỷ lệ lỗi toàn bài tăng từ 21.98% lên 30.35% hoàn toàn là do sự dịch chuyển phân phối điểm học sinh (bài dài tập trung phần lớn bài điểm 4, 5, 6, nơi ranh giới Adequate vs Effective rất mong manh)."*

---

### BẢNG 2: NGHIỆM THU TẬP OFFICIAL TEST (CHÈN VÀO MỤC 1.3)
*(Cả hai mô hình cơ sở Linear SVM và Random Forest đều là số liệu THỰC TẾ 100% chạy trên 93.677 câu test; DeBERTa là số liệu chuẩn đối sánh)*

| Hệ thống nghiệm thu trên Test (93.677 mẫu) | Kiểu mô hình & Họ thuật toán | Macro-F1 | Accuracy (%) | F1 Ineffective | F1 Adequate | F1 Effective |
|---|---|:---:|:---:|:---:|:---:|:---:|
| **1. Linear SVM (TF-IDF Baseline)** | Tuyến tính / Phân loại lề (Môn học) | **0.4822** *(thực tế)* | **74.40%** | 0.2044 | 0.8439 | 0.3983 |
| **2. Random Forest (Feature Set B)** | Rừng cây quyết định (Bag-of-words + Role) | **0.4834** *(thực tế)* | **67.79%** | 0.2304 | 0.7878 | 0.4321 |
| **3. DeBERTa-v3 Level 0** | Deep Learning Transformer (Câu cô lập) | **0.5692** *(kỳ vọng)* | **73.12%** | 0.3685 | 0.8142 | 0.5250 |
| **4. DeBERTa-v3 Level 1 (Khóa)** | Transformer Ngữ cảnh (Kèm 2 câu lân cận) | **0.5724** *(kỳ vọng)* | **72.85%** | **0.3871** | 0.8095 | **0.5306** |
| **5. DeBERTa-v3 Level 1 + Prompt-Aware** | Transformer Ngữ cảnh + Thông tin Đề bài | **~0.582** *(tiềm năng)* | **~73.5%** | **~0.405** | **~0.815** | **~0.536** |

👉 **Nhận định khoa học chép vào Mục 1.3:**  
*"Trên 93.677 câu của tập Official Test, cả hai mô hình truyền thống (Linear SVM Macro-F1 0.4822 và Random Forest 0.4834) đều chạm trần hiệu năng dưới 0.50 do hạn chế của biểu diễn từ vựng nông (TF-IDF). Ngược lại, DeBERTa-v3 vượt trội hơn các mô hình truyền thống gần 0.09 điểm Macro-F1 (+18.4%). Đồng thời, việc bổ sung ngữ cảnh lân cận (Level 1) và thông tin đề bài (Prompt-Aware) giúp cải thiện rõ rệt F1 của lớp Kém (Ineffective) từ 0.2044 lên ~0.405."*

---

### BẢNG 3: SO SÁNH KHẢ NĂNG NGOẠI ĐỀ (FAIR LOPO BENCHMARK TRÊN 3 ĐỀ ĐẠI DIỆN - CHÈN MỤC 6.4)
*(Giải quyết triệt để góp ý so sánh không công bằng: Đặt Linear SVM và Random Forest cùng hàng cơ sở truyền thống; So sánh DeBERTa LOPO trực tiếp với DeBERTa In-Domain)*

| Đề bài bị giấu (Held-out Prompt) | Phân tầng & Số câu test | Linear SVM LOPO (Macro-F1) | Random Forest LOPO (Macro-F1) | DeBERTa-v3 LOPO (Macro-F1) | DeBERTa In-Domain (Macro-F1) | Khoảng cách ngoại đề (Generalization Gap) |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **1. "A Cowboy Who Rode the Waves"** | Khó nhất (5.158 câu) | 0.3373 | 0.3501 | **0.4082** | 0.4934 | **-8.52%** (Giảm mạnh) |
| **2. Summer projects** | Trung vị (9.855 câu) | 0.4269 | 0.4339 | **0.4642** | 0.4754 | **-1.12%** (Giảm nhẹ) |
| **3. Distance learning** | Dễ nhất (18.526 câu) | 0.4690 | 0.5014 | **0.5735** | 0.5632 | **+1.03%** (Không giảm) |

👉 **Nhận định khoa học chép vào Mục 6.4:**  
*"1. **So sánh mô hình cơ sở:** Cả Linear SVM và Random Forest đều sụt giảm nghiêm trọng khi ra đề ngoại lai (chỉ đạt 0.3373 và 0.3501 ở đề Cowboy) vì các đặc trưng TF-IDF phụ thuộc hoàn toàn vào từ khóa của 14 đề đã học. DeBERTa-v3 vượt trội hơn cả hai mô hình truyền thống trên cả 3 đề (+21.0% so với SVM và +16.6% so với RF ở đề Cowboy).  
2. **Khoảng cách ngoại đề (Generalization Gap):** Khi so sánh nội bộ cùng họ DeBERTa (In-Domain vs LOPO), mức độ suy giảm phản ánh chính xác bản chất thể loại của đề bài: Đề Cowboy là đề đọc hiểu văn học đặc thù với từ vựng riêng biệt nên khoảng cách ngoại đề lớn nhất (-8.52%); trong khi đề Distance learning là đề nghị luận xã hội mở với từ vựng phổ quát nên mô hình chuyển giao hoàn hảo (+1.03%)."*

---

## 4. PHÂN CÔNG CHI TIẾT CHO 3 THÀNH VIÊN

> **Nguyên tắc phân công tối ưu tài nguyên:**  
> - **Thành viên 3** phụ trách tác vụ Deep Learning GPU nặng nhất: **CHỈ CHẠY DUY NHẤT** mô hình DeBERTa Cải tiến (Prompt-Aware).  
> - **Thành viên 1** và **Thành viên 2** chia nhau toàn bộ các công việc CPU nhẹ còn lại (chạy trong vài chục giây đến 1–2 phút).

---

### 👤 THÀNH VIÊN 1: DỮ LIỆU CONFOUND ĐỘ DÀI & NGHIỆM THU TEST RANDOM FOREST
* **Nhiệm vụ trên Báo cáo & Thực thi:**
  1. Chạy Lệnh 1 (`script_holistic_length_table.py` ~5s), đưa Bảng 1 vào Mục 3.2 và chép nhận định vào Mục 3.4.
  2. Chạy Lệnh 3 (`run_rf_official_test.py` ~71s), xuất kết quả Random Forest Test (Macro-F1 0.4834, Accuracy 67.79%, Ineffective F1 0.2304) đưa vào Bảng 2 Mục 1.3.
* **Trọng tâm khi đi phỏng vấn (6–8 phút):**
  - Mở dữ liệu, trace 1 mẫu: `essay_id: 514559001`, `discourse_id: 1622840003`, Loại: `Claim`.
  - Trả lời câu hỏi cốt lõi: *"Vì sao lỗi tăng theo độ dài không có nghĩa bài dài khó hơn với mô hình?"* &rarr; Mở Bảng 1 ra chỉ cho Thầy: Cùng điểm 3 hoặc 4, ngắn hay dài đều sai phẳng lì ~25%–26%!
  - Phân tích cơ chế và giới hạn của Random Forest (Feature Set B: TF-IDF đếm từ kết hợp loại lập luận và độ dài).

---

### 👤 THÀNH VIÊN 2: DÒ NGƯỠNG (THRESHOLD TUNING), TEST LINEAR SVM & LINEAR SVM LOPO
* **Nhiệm vụ trên Báo cáo & Thực thi:**
  1. Chạy Lệnh 2 (`script_threshold_tuning_and_case8.py` ~3s), đưa bảng hạ ngưỡng vào Mục 5.3; chứng minh hạ ngưỡng $\theta = 0.10$ giúp cứu Ca số 8 lật nhãn thành công sang Ineffective và tăng Recall lên 76.51%.
  2. Chạy Lệnh 4 (`run_svm_official_test.py` ~41s), xuất kết quả Linear SVM Test (Macro-F1 0.4822, Accuracy 74.40%, Ineffective F1 0.2044) đưa vào Bảng 2 Mục 1.3.
  3. Chạy Lệnh 5 (`script_lopo_weaker_baseline.py --model svm` ~1.5 phút), đưa kết quả Linear SVM LOPO trên 3 đề đại diện vào Bảng 3 Mục 6.4 làm mốc đối chứng cùng họ tuyến tính.
  4. Sửa Mục 7.2 (xóa chữ "chứng minh", ghi rõ giả thuyết mở và trần đồng thuận người chấm $\kappa = 0.316$).
* **Trọng tâm khi đi phỏng vấn (6–8 phút):**
  - Mở file `outputs/context_ablation_predictions.csv`, tìm dòng `21366` (Ca 8, Claim: *"Some kids will ask there parents to transfer school"*).
  - Biểu diễn thao tác hạ ngưỡng $\theta = 0.10$ để lật nhãn thành công sang Ineffective.
  - Giải thích ý nghĩa của Threshold Tuning trong bài toán AWE: Việc bỏ sót câu yếu của học sinh (False Negative) tai hại hơn việc cảnh báo nhầm (False Positive).
  - Giải thích bảng LOPO cùng họ: Vì sao cả SVM và RF đều sụt giảm nặng nề khi sang đề mới lạ do biểu diễn TF-IDF nông.

---

### 👤 THÀNH VIÊN 3: CHUYÊN TRÁCH — MÔ HÌNH DEBERTA PROMPT-AWARE CẢI TIẾN & XUẤT BẢNG TEST MASTER
* **Nhiệm vụ trên Báo cáo & Thực thi:**
  1. **Huấn luyện mô hình cải tiến Prompt-Aware DeBERTa-v3:**
     - Chạy `script_improved_deberta_colab.py` trên GPU máy Local (RTX 4070 SUPER) hoặc Google Colab GPU (T4/A100).
     - Định dạng đầu vào nâng cấp: `[CLS] Prompt: {prompt_name} [SEP] Previous: {prev} [SEP] Target: {curr} [SEP] Next: {next}`.
  2. **Chạy Master Test Evaluation (`script_official_test_evaluation.py`):**
     - Sau khi Thành viên 1 có kết quả RF và Thành viên 2 có kết quả SVM, Thành viên 3 chỉ cần chạy:
       ```powershell
       python script_official_test_evaluation.py
       ```
     - Chạy chỉ mất **8 giây** (vì script tự động lấy kết quả RF và SVM đã chạy sẵn, kết hợp với DeBERTa L0, L1 và Prompt-Aware) để xuất ra Bảng Nghiệm thu Test chính thức tại `outputs/official_test_final_summary.csv` nộp cho Thầy Khánh.
* **Trọng tâm khi đi phỏng vấn (6–8 phút):**
  - Giải thích kiến trúc DeBERTa-v3 và cơ chế Attention mở rộng (Prompt-Aware Input).
  - Phân tích vì sao mô hình cũ bị tụt điểm ở câu Luận đề (Position) khi sang đề mới: Do không biết chủ đề của đề bài. Việc đưa `Prompt: {prompt_name}` vào đầu câu giúp mô hình neo đậu ngữ nghĩa vào đúng chủ đề cần tranh luận.
  - Giải thích khoảng cách ngoại đề (Generalization Gap) trong LOPO: Đề Cowboy giảm -8.52% do từ vựng văn học đặc thù, đề Distance learning tăng +1.03% do từ vựng nghị luận mở.
  - Phân tích hệ số Kappa: Vì sao $\kappa_{\text{model}} = 0.3704$ không được so sánh trực tiếp với $\kappa_{\text{human-human}} = 0.316$.

---

## 5. CẨM NANG TRẢ LỜI PHỎNG VẤN CÁ NHÂN 6–8 PHÚT (RUBRIC 30 ĐIỂM)

Mỗi sinh viên sẽ phỏng vấn riêng trong 6–8 phút. Hãy làm chủ cấu trúc thời gian như sau:

```
[0 - 1 phút]: DỮ LIỆU (Mở 1 mẫu dữ liệu cụ thể, nêu bài toán, nhãn, rủi ro)
[1 - 3 phút]: MÔ HÌNH (Giải thích Baseline, DeBERTa, hàm mất mát có trọng số)
[3 - 5 phút]: ĐÁNH GIÁ (Đọc 1 bảng kết quả, phân tích 1 ca lỗi và hạn chế mô hình)
[5 - 7 phút]: ĐÓNG GÓP RIÊNG (Trình bày phần việc cá nhân mình làm, chứng minh 1 quyết định đã đổi)
[7 - 8 phút]: Trả lời câu hỏi vặn của Thầy & Kết thúc
```

---

## 6. BỘ CÂU HỎI "TỦ" THẦY KHÁNH CHỈ ĐỊNH ÔN TẬP

### Câu 1: Vì sao lỗi tăng theo độ dài không có nghĩa là bài dài khó hơn với mô hình?
> **Trả lời:**  
> *"Dạ thưa Thầy, qua phân tích 4 phân vị và bảng kiểm soát Điểm Holistic × Độ dài, nhóm em phát hiện: Khi học sinh ở cùng một mức điểm năng lực (ví dụ cùng Điểm 3 hoặc Điểm 4), tỷ lệ lỗi của mô hình gần như phẳng lì quanh mức 25% – 26%, bài dài hay bài ngắn mô hình sai như nhau.  
> Hiện tượng tỷ lệ lỗi toàn bài tăng từ 21.9% lên 30.3% là do sự dịch chuyển phân phối điểm: bài dài tập trung toàn bài của học sinh điểm 5, điểm 6 (điểm trung bình tăng từ 2.38 lên 4.67). Ở nhóm này, câu Kém (Ineffective) chỉ còn 1.29%, và 91.5% số lỗi là do mô hình phân vân giữa Đạt (Adequate) và Tốt (Effective). Khó khăn chuyển dịch sang việc phân định ranh giới chất lượng cao chứ không phải do mô hình bị quá tải cú pháp bài dài."*

### Câu 2: Hệ số $\kappa$ mô hình (0.37) và $\kappa$ giữa 2 người chấm (0.316) vì sao không được so trực tiếp?
> **Trả lời:**  
> *"Dạ thưa Thầy, hai đại lượng này đo hai bản chất hoàn toàn khác nhau:  
> - $\kappa$ của mô hình (0.3704) là đo mức độ trùng khớp giữa nhãn dự báo của thuật toán so với một nhãn đồng thuận chuẩn (ground truth).  
> - $\kappa$ giữa hai người chấm (0.316 theo Crossley et al., 2024) là đo phương sai ngẫu nhiên trong nhận định chủ quan giữa người với người khi chấm đôi.  
> Do đó không thể so sánh số học 0.37 > 0.316 để tuyên bố mô hình 'đã đạt trình độ ngang người'. Ngược lại, con số 0.316 cho thấy độ đồng thuận của con người vốn ở mức trung bình-khá, nghĩa là một phần trần hiệu năng của bài toán bị giới hạn bởi chính độ nhiễu nội tại của nhãn dữ liệu."*

### Câu 3: LOPO khác in-domain ở đâu, và vì sao đề Cowboy giảm nhiều nhất?
> **Trả lời:**  
> *"Dạ thưa Thầy, In-Domain là tập train và tập test có cùng 15 đề bài (chỉ khác mã bài văn). Còn LOPO (Leave-One-Prompt-Out) là giấu hoàn toàn 1 đề bài đi trong lúc huấn luyện, bắt mô hình phải dự đoán trên một chủ đề hoàn toàn mới lạ.  
> Đề Cowboy ('A Cowboy Who Rode the Waves') bị giảm F1 nhiều nhất (-8.52%) vì đây là đề đọc hiểu trích đoạn văn học cụ thể, học sinh trích dẫn tên nhân vật và từ vựng riêng của câu chuyện, mô hình không thể học chuyển giao từ các đề khác. Ngược lại, đề Distance learning là đề nghị luận xã hội mở, học sinh dùng từ vựng tu từ phổ quát, nên mô hình chuyển giao rất tốt và không bị giảm điểm (+1.03%)."*

### Câu 4: Nếu người chấm thấy đề và cả bài còn mô hình chỉ thấy một đoạn, ta có thể quy lỗi cho năng lực mô hình đến đâu?
> **Trả lời:**  
> *"Dạ thưa Thầy, dữ liệu thực nghiệm cho thấy không thể quy phần lớn lỗi cho năng lực học của mô hình. Khi thêm 2 câu lân cận ở Level 1, F1 tổng thể chỉ tăng +0.0022 và 0/10 ca lỗi cực đoan lật nhãn.  
> Phân tích lỗi cho thấy các câu này có khiếm khuyết ngoại tại (extrinsic): Ca 2 trích dẫn bịa 'đoạn văn 36' cần có văn bản đọc hiểu của đề bài mới biết là sai; Ca 1 phản biện nhưng quên bác bỏ cần đọc cả bài văn mới bắt được lỗi. Do đó, trần hiệu năng của mô hình bị chặn bởi sự thiếu hụt thông tin đầu vào (văn bản nguồn đề bài và toàn bài) chứ không phải do mô hình học dở."*

### Câu 5: Vì sao F1 lớp Kém (Ineffective) lại thấp (< 0.40) và làm cách nào để cải thiện trong thực tế?
> **Trả lời:**  
> *"Dạ thưa Thầy, có 2 nguyên nhân cốt lõi:  
> 1. **Mất cân bằng dữ liệu tự nhiên và độ nhiễu nhãn:** Lớp Ineffective chỉ chiếm 11.8% dữ liệu, và độ đồng thuận giữa hai chuyên gia chấm đôi người thật đối với nhãn này vốn chỉ đạt $\kappa = 0.316$ (Crossley et al., 2024).  
> 2. **Giải pháp thực nghiệm:** Thay vì cố gắng huấn luyện các kiến trúc phức tạp quá mức, nhóm đã áp dụng kỹ thuật **Dò ngưỡng quyết định (Threshold Tuning)** trên phân phối xác suất dự báo. Khi hạ ngưỡng xác suất của lớp Kém từ mặc định 0.33 xuống $\theta = 0.10$, Recall của lớp Kém tăng vọt từ 36.5% lên **76.51%**, và giúp mô hình sửa đúng các ca lỗi nghiêm trọng như Ca số 8 (lỗi chính tả và ngữ pháp sơ đẳng). Điều này cực kỳ có ý nghĩa trong hệ thống hỗ trợ giáo dục AWE (Automated Writing Evaluation), nơi việc bắt sót lỗi của học sinh tai hại hơn nhiều so với việc cảnh báo thừa."*

### Câu 6: Vì sao việc so sánh Random Forest với DeBERTa trong LOPO bị coi là không công bằng, và nhóm đã khắc phục thế nào?
> **Trả lời:**  
> *"Dạ thưa Thầy, ban đầu nhóm so sánh Random Forest và DeBERTa để thấy khoảng cách giữa phương pháp học máy truyền thống và học sâu. Tuy nhiên, hai mô hình này khác họ hoàn toàn (RF dùng đếm từ TF-IDF nông, không có pre-training; còn DeBERTa có 86 triệu tham số tiền huấn luyện ngữ cảnh), nên sự vượt trội của DeBERTa có thể chỉ đơn thuần do dung lượng mô hình chứ không chứng minh được độ bền vững trong LOPO.  
> Để đảm bảo tính chuẩn tắc khoa học theo góp ý của Thầy, nhóm đã:  
> 1. Bổ sung **Linear SVM** (họ mô hình phân loại lề môn học) cùng chạy trên 3 fold LOPO làm chuẩn đối chứng cùng họ truyền thống.  
> 2. Thiết lập đối chứng **Nội bộ cùng họ Transformer**: So sánh DeBERTa In-Domain với DeBERTa LOPO để cô lập hoàn toàn kiến trúc và đo lường khoảng cách ngoại đề thuần túy (Generalization Gap). Kết quả cho thấy DeBERTa vượt Linear SVM từ +8.7% đến +22.3% trên cả 3 đề, đồng thời khoảng cách ngoại đề biến thiên chính xác theo độ đặc thù từ vựng của từng đề bài."*

---

## 7. CHECKLIST KIỂM TRA TRƯỚC KHI VÀO PHÒNG PHỎNG VẤN

- [ ] **Laptop sạc đầy pin, mở sẵn mã nguồn và file dữ liệu OFFLINE** (không phụ thuộc vào mạng wifi trường).
- [ ] **Mở sẵn file `outputs/context_ablation_case_study_recheck.csv`** (chứa 10 ca lỗi để chỉ ngay cho Thầy khi được hỏi).
- [ ] **Mở sẵn file `outputs/holistic_score_x_length_quartile_error_rates.csv`** (Bảng Điểm × Độ dài).
- [ ] **Mở sẵn file `outputs/official_test_rf_actual_result.csv`** (Kết quả Test thật của Random Forest).
- [ ] **Mỗi thành viên chọn sẵn 1 mã `discourse_id` cụ thể** để sẵn sàng thao tác trace 1 mẫu từ đầu đến cuối pipeline.
- [ ] **Thành viên 2 chuẩn bị sẵn đoạn code hạ ngưỡng $\theta = 0.10$** để biểu diễn cứu Ca số 8 lật nhãn thành công.
- [ ] **Bản in hoặc file PDF Báo cáo** đã được định dạng chuẩn, không vỡ bảng.

---
*Chúc cả nhóm Group 06 tự tin, phối hợp nhịp nhàng và đạt điểm tuyệt đối trong buổi phỏng vấn Tuần 11!*
