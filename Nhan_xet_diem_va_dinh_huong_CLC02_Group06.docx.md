# **Nhóm 06 · Discourse Effectiveness Prediction (PERSUADE 2.0)**

*Lớp 62FIT4MLA – CLC02 · Nhận xét sau buổi thuyết trình giữa kỳ*

Gửi nhóm 6,

Slide của nhóm rất chuyên nghiệp và bám sát sáu tiêu chí. Thầy thích cách nhóm đọc tài liệu: mỗi bài được chuyển thành một quyết định thiết kế cụ thể, như dùng ranh giới luận điểm có sẵn, so sánh công bằng, báo cáo theo nhóm người học. Việc đặt recall của lớp Ineffective làm metric quan trọng cho thấy nhóm hiểu giáo viên cần gì nhất.

Có một lỗi dễ sửa nhưng quan trọng: licence của PERSUADE 2.0 là CC BY-NC-SA 4.0 (thầy đã kiểm tra trên repo gốc), không phải CC BY 4.0 như slide. Số lượng train, validation, test cũng nên khớp với bản chính thức.

Logistic Regression và Linear SVM trên cùng TF-IDF thường cho kết quả rất gần nhau, nên cặp này chưa cho nhiều thông tin. Thầy coi cả hai là baseline. Mô hình đáng so là một transformer tinh chỉnh như DeBERTa-base, giống các lời giải trong Feedback Prize; nhóm cũng đã ghi nó là phần mở rộng. Chênh lệch giữa baseline và transformer trên đề chưa thấy mới là kết quả đáng báo cáo.

Trước đó, các em xem tỷ lệ Ineffective theo loại luận điểm và theo đề, và luận điểm Ineffective thường ngắn, dài hay chỉ lặp lại đề bài. Nhóm 4 cùng lớp cũng dùng PERSUADE 2.0, hai nhóm nên trao đổi để mỗi nhóm có câu hỏi riêng. Nếu tập trung vào "mô hình nhận ra luận điểm yếu trên đề chưa thấy tốt đến đâu, và có công bằng với người học ELL không", nhóm có thể làm thành đề tài NCKH.

**Tuần sau, nhóm mang đến:**

* Licence đã sửa và số mẫu từng tập theo bản chính thức.  
* Tỷ lệ Ineffective theo loại luận điểm.

Nhóm trình bày rất tốt, giờ hãy để phần phân tích dữ liệu tốt như phần trình bày.

*Thầy Khánh*

## **Điểm giữa kỳ**

| \# | Tiêu chí | Điểm | Ghi chú |
| :---- | :---- | :---- | :---- |
| 1 | Vấn đề và người dùng | 17 / 20 | Giáo viên và quyết định rõ. |
| 2 | Dữ liệu, licence, tính khả thi | 15 / 20 | PERSUADE 2.0 đúng về tồn tại, nhưng licence ghi CC BY 4.0 là sai (bản gốc CC BY-NC-SA 4.0); số train/validate/test cần khớp với bản chính thức. |
| 3 | Bài toán ML, baseline và lựa chọn mô hình | 18 / 25 | Bài toán 3 lớp rõ, có ví dụ. LR và Linear SVM trên cùng TF-IDF khá giống nhau. |
| 4 | Đánh giá, cách chia, baseline | 12 / 15 | Baseline có số liệu, QWK, recall lớp hiếm. Cách chia 60/20/20 cần khớp với test chính thức; leave-one-prompt-out mới ở mức rủi ro. |
| 5 | Rủi ro và vai trò con người | 9 / 10 | Rủi ro rõ, không dùng nhân khẩu học làm đầu vào. |
| 6 | Trình bày, thời gian, hỏi đáp | 8 / 10 | Phần trình bày tại lớp. |
|  | **Điểm trình bày** | **79 / 100** |  |

| Thành phần | Điểm |
| :---- | :---- |
| Điểm trình bày (50%) | 79 / 100 |
| Hoàn thành Lab 1–5 (50%) | 5/5 lab → 100 / 100 |
| **Điểm giữa kỳ** | **89,5 / 100, tức 9 / 10** |

*Lab của nhóm theo bảng theo dõi: Lab 1: 1, Lab 2: 1, Lab 3: 1, Lab 4: 1, Lab 5: 1 (0,5 là nộp một phần). Bạn nào có tình hình nộp lab khác với nhóm thì báo thầy để điều chỉnh riêng.*