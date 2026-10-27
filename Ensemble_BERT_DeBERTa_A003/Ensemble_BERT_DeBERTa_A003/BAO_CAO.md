# Báo cáo kết quả Ensemble BERT và DeBERTa

## Kết quả đã thực hiện

Nhóm kết hợp xác suất của BERT và DeBERTa để đánh giá chất lượng discourse trong bài viết học sinh theo ba lớp Ineffective, Adequate, Effective. Ensemble đạt accuracy 77,65% và Macro-F1 0,60224 trên validation gồm 14.303 segment thuộc 1.557 essay. Kết quả phục vụ hỗ trợ giáo viên xem xét; chưa phải đánh giá test độc lập hay hệ thống chấm tự động.

Đây là nội dung đóng gói để bổ sung vào báo cáo tuần theo yêu cầu. Ngày chạy thực tế là 05/10/2026, execution bắt đầu 05:57:06 UTC và artifact thu xong 06:00:12 UTC theo manifest gốc; notebook không đổi ngày hoặc output. Kỳ tuần nộp do nhóm ghi trong báo cáo tổng hợp.

## Phương pháp và thực thi

Sử dụng hai model gốc đã fine-tune: BERT N1 và DeBERTa N2. A003 là lần chạy ensemble CPU qua Docker Colab CLI, dùng lại prediction validation/calibration đã lưu; không fine-tune lại hai encoder. Notebook kernel riêng có năm cell đã thực thi, không lỗi. Dữ liệu group theo essay/content và nhãn theo thứ tự Ineffective, Adequate, Effective; prediction hai model được đối chiếu ID, group và label trước khi kết hợp.

Thử trọng số BERT 0,25; 0,50; 0,75 trên validation; trọng số DeBERTa bằng 1 trừ trọng số BERT. Chọn 0,50 và 0,50 theo Macro-F1. Xác suất hỗn hợp được calibration trên tập riêng bằng temperature 0,904014. Ngưỡng cảnh báo Ineffective là 0,653800, chọn trên calibration tại precision tối thiểu 0,40; đây là chính sách tham chiếu, không phải ngưỡng nghiệm thu bắt buộc. Config ensemble không đại diện hyperparameter training thực tế của từng model thành phần; lần này không train ba epoch encoder.

## Kết quả validation

| Chỉ số | Giá trị |
|---|---:|
| Accuracy | 77,6480% |
| Dự đoán đúng | 11.106 / 14.303 |
| Macro-F1 | 0,602243 |
| QWK | 0,478412 |
| AP Ineffective | 0,383772 |
| Log-loss | 0,511191 |
| ECE 10 bin | 0,009864 |
| Recall Ineffective tại top 10% review | 61,4173% |

Accuracy là tỷ lệ đúng tổng thể; Macro-F1 lấy trung bình F1 ba lớp, không quy đổi trực tiếp thành accuracy. Lớp Adequate chiếm 11.297/14.303 mẫu, do đó accuracy đơn lẻ chưa phản ánh tốt hiệu quả trên lớp ít mẫu.

| Lớp | Precision | Recall | F1 | Support |
|---|---:|---:|---:|---:|
| Ineffective | 0,335171 | 0,478740 | 0,394293 | 635 |
| Adequate | 0,882730 | 0,828893 | 0,854965 | 11.297 |
| Effective | 0,515782 | 0,606495 | 0,557472 | 2.371 |

Ma trận nhầm lẫn có hàng là nhãn thật và cột là nhãn dự đoán, theo thứ tự Ineffective, Adequate, Effective: [[304, 320, 11], [594, 9364, 1339], [9, 924, 1438]].

## So sánh và giới hạn

Macro-F1 BERT thành phần là 0,588547; DeBERTa là 0,599081; ensemble là 0,602243 trên cùng full validation. Ensemble tăng 0,003162 so với DeBERTa. Paired bootstrap theo essay 2.000 lần có CI 95% của chênh lệch từ −0,005156 đến 0,011460, chứa 0; chưa đủ khẳng định ensemble vượt DeBERTa chắc chắn. Weight được chọn trên chính validation, nên bootstrap này có điều kiện theo lựa chọn và không thay thế test độc lập.

Review top 10% chọn 1.431 segment theo xác suất Ineffective, tìm 390/635 mẫu Ineffective: precision 27,25%, recall 61,42%. Đây là chẩn đoán xếp hạng theo ngân sách review, khác với argmax ba lớp và khác ngưỡng cảnh báo cố định từ calibration.

A003 không đo latency từ văn bản hoặc VRAM của hai encoder. Mức giảm số dư tài khoản giữa đầu/cuối execution 0,09 CU gồm công việc khác chạy đồng thời, không được coi là CU riêng của ensemble. Không dùng kết quả này để kết luận hiệu quả chuyển đề, fairness hay chất lượng phản hồi sư phạm. A001/A002 lỗi trước đó giữ nguyên trong project; gói nộp này tập trung lần A003 hoàn tất.

## Bằng chứng và bước tiếp theo

Số liệu lấy từ results/metrics_validation.json; trọng số và calibration trong selection.json, temperature.json, operating_point.json. Notebook đã thực thi ở notebooks/kernel_output.ipynb; manifest và kiểm chứng tính lại ở evidence. Gói có code/config đúng snapshot A003, predictions validation/calibration, confusion matrix và reliability plot. Script verify_results.py tính lại số liệu và đối chiếu checksum toàn gói, không cần GPU.

Bước tiếp theo của project là khóa phương án bằng validation, đánh giá test độc lập và chi phí inference. Task model tổng thể còn các full/OOD/test run khác; gói này không tuyên bố toàn task đã hoàn thành.
