# CLC02 Nhóm 6

**PERSUADE: dự báo hiệu quả đơn vị lập luận**

Đã có nhiều kết quả, nhưng cần kiểm tra lại phép so sánh trước khi thêm tối ưu. Các kết luận “superiority”, công bằng và triển khai hiện mạnh hơn bằng chứng.

## Từ bản sửa hiện tại

Nhóm báo cáo classical baselines, BERT/DeBERTa và ensemble macro-F1 0,6022, recall Ineffective 47,87%. Có confusion matrix 14.303 đơn vị validation và CI ghép cặp ensemble–DeBERTa. Phần kế hoạch tiếp theo vẫn mở rất nhiều nhánh tối ưu.

## Điểm cần sửa và lý do

**1\. Các bảng chưa chỉ rõ đang so trên tập nào.** Bộ chính thức nêu 93.677 đơn vị test nhưng bảng 4.1 dùng 46.856; cần flow lọc/lấy mẫu và lý do giữ khoảng một nửa. Bảng 4.2 có số khớp validation 14.303 nhưng tiêu đề “superiority” dễ bị đọc như so test. Mỗi số phải ghi split, cohort, số essay và số unit. Không đặt kết quả validation của encoder cạnh test của baseline để kết luận cải thiện.

**2\. Đối chứng tuyến tính đang có dấu hiệu cần sửa.** LR balanced accuracy 6,13%, macro-F1 0,0477 là bất thường, chưa đủ giải thích bằng class imbalance hoặc TF-IDF yếu. Kiểm tra nhãn/class order, convergence, ghép sparse–dense, scale và cách predict. LR threshold-optimized lại đạt macro-F1 0,5314, cao hơn SVM chọn làm baseline 0,5101. So với đối chứng mạnh nhất hợp lệ trong cùng điều kiện, không chọn bảng dễ vượt.

**3\. Ensemble chưa chứng minh lợi ích đủ để giữ độ phức tạp.** Chênh macro-F1 ensemble–DeBERTa khoảng 0,00316, CI \[-0,005156; 0,011460\] chưa cho bằng chứng rõ hơn. Không gọi là superiority. Recall 61,42% ở top 10% được tính từ 390/635 ca Ineffective trên validation, không phải “across the corpus”. ECE 0,0099 không tự chứng minh xác suất lớp hiếm được hiệu chỉnh tốt; nêu nơi fit temperature và nơi chấm, số bin và calibration theo lớp.

**4\. Lời giải thích giáo dục/công bằng còn suy diễn.** Trung bình độ dài không chứng minh bài sao chép hoặc lạc đề; cần đọc ca với prompt/context. ELL \= No không tự đồng nghĩa native speaker; không dùng demographics trong input cũng không đảm bảo không phân biệt. Kế hoạch threshold riêng theo ELL lại sử dụng thuộc tính này ở quyết định cuối và cần lý do/đánh đổi riêng, không mặc nhiên là công bằng. Tác vụ đang nhận segment/type đã có annotation; chưa là hệ thống tự đọc toàn bài và tách lập luận.

## Đọc nghiên cứu để giải thích lựa chọn

Bản báo cáo chưa có đối chiếu có hệ thống với nghiên cứu discourse effectiveness gần đây. Chọn paper nguồn PERSUADE và một công trình sát classification có context/unseen prompt; giải thích đặc trưng nào cần gold segment/type, vì sao dùng context, và họ đánh giá chuyển prompt ra sao. Danh sách kỹ thuật focal loss, LLRD, pooling không phải related work nếu không nối tới lỗi đang quan sát.

# CLC02 Nhóm 6 Hướng chuẩn bị

## Hướng triển khai khả thi

Dừng mở đồng thời full-context, nhiều pooling/loss, ordinal, LLRD, fairness thresholds và quantization. Trước hết sửa baseline/cohort/split, giữ DeBERTa đơn và đối chứng cổ điển mạnh nhất; làm một phép đánh giá unseen prompt hoặc một ablation context đã chọn bằng development. Ensemble là phụ nếu lợi ích nhỏ; latency phải đo, không chỉ suy từ số encoder.

## Bằng chứng cần mang đến buổi gặp

* Bảng nguồn → lọc → train/validation/test có essay ID; tất cả bảng ghi cùng cohort hoặc tách rõ.  
* Chẩn đoán LR 6,13%, kết quả strongest classical baseline và DeBERTa trong cùng protocol.  
* Confusion matrix/triage theo split độc lập, calibration protocol; 10 ca Ineffective đọc cùng prompt và context.

## Câu hỏi để nhóm tự kiểm tra mức hiểu

* 0,6022 được chấm trên validation hay test, và baseline cùng bảng có dùng đúng những mẫu đó không?  
* Tại sao LR chỉ đúng 6,13%, trong khi phiên bản tối ưu threshold đạt macro-F1 hơn SVM?  
* Nếu CI của phần tăng ensemble chứa 0, nhóm có lý do thực tế nào để giữ hai encoder?

## Lời nhắn cho nhóm

Thầy chưa cần thêm một danh sách kỹ thuật tối ưu. Hãy kiểm tra xem các bảng hiện tại có đang so đúng tập, đúng baseline và đúng mục tiêu hay không. Các em phải giải thích được một lỗi thực nghiệm và một lỗi dự đoán cụ thể trước khi nói mô hình đã vượt trội.