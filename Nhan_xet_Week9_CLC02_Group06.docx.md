# **CLC02 Nhóm 6 · Nhận xét Tuần 9**

*PERSUADE 2.0: dự báo hiệu quả đơn vị lập luận*

Nhóm đã làm đúng mấy việc quan trọng: mọi mô hình giờ chấm trên cùng 29.102 đơn vị validation, lỗi LR 6,13% được tìm ra nguyên nhân (thứ tự nhãn của scikit-learn bị hiểu nhầm), ensemble bị bỏ vì không có lợi ích, và DeBERTa đơn hơn RF mạnh nhất với khoảng tin cậy không chứa 0\. Thầy cũng nói thẳng về cách viết: báo cáo đầy những chữ như "forensic", "definitive", "conclusively", "fully competitive", trong khi bản PDF còn lỗi KaTeX chưa sửa và số bị lặp đôi ("6.13%6.13%"). Người đọc sẽ tin một báo cáo viết vừa phải và được soát kỹ hơn một báo cáo dùng nhiều chữ mạnh.

## **Dữ liệu đang nói gì**

Mười ca Ineffective bị đoán sai với độ tự tin trên 0,94 đang nói một điều rõ ràng. Ca 2 viết "brings me back to paragraph 36", ca 5 là một claim không có trong tài liệu nguồn, ca 1 là counterclaim không có phản bác đi kèm. Người chấm đánh giá hiệu quả của một đơn vị dựa trên bài viết và đề bài; mô hình chỉ thấy loại đơn vị và một câu đơn lẻ. Phần lớn thất bại không phải do mô hình yếu, mà do thông tin người chấm dùng không có trong đầu vào. Các giải thích kiểu "từ nối học thuật kích hoạt trọng số dương" là đoán; DeBERTa không có trọng số theo từ để đọc ra như vậy.

## **Những chỗ phải sửa**

1\. Phép so ρ \= 0,857 giữa kappa người chấm và F1 mô hình chỉ có 7 điểm, không đủ để kết luận lỗi ở Claim, Counterclaim "trực tiếp do" người chấm kém đồng thuận. Kappa của mô hình so với nhãn và kappa giữa hai người chấm cũng không phải cùng một đại lượng, nên chưa nói được mô hình "ngang người". Các con số kappa theo loại đơn vị cũng cần ghi rõ trang và bảng trong Crossley và cộng sự (2024).

2\. Lỗi tăng theo độ dài bài (22% lên 30%) có thể do phân bố nhãn hoặc đề khác nhau giữa các nhóm độ dài. Xem tỷ lệ ba nhãn và đề trong từng nhóm trước khi giải thích bằng "độ phức tạp lập luận".

3\. Validation đang dùng cho chọn mô hình, chọn ngưỡng, hiệu chỉnh và kiểm định. Kết luận vượt trội cuối cùng cần một lần chấm trên Official Test đã khóa cấu hình.

4\. Báo cáo chưa có link notebook hay mã. Bổ sung, và mỗi thành viên phải tự giải thích được lỗi 6,13% bằng lời của mình.

## **Từ baseline đến đóng góp riêng**

Bộ dữ liệu này đã có một cuộc thi Kaggle với hàng nghìn đội; DeBERTa trên từng đơn vị là điểm xuất phát chung, không phải đóng góp. Đóng góp riêng của nhóm có thể đến từ chính phân tích lỗi: thông tin nào người chấm dùng mà mô hình không thấy? Thiết kế một thí nghiệm ngữ cảnh có kiểm soát: chỉ đơn vị; đơn vị cùng đơn vị đứng trước và sau; đơn vị cùng toàn bộ đoạn; đơn vị cùng đề bài. Giữ nguyên mô hình và split, chỉ đổi đầu vào, rồi xem Ineffective được cải thiện ở loại đơn vị nào. Song song, chia theo đề: hiện essay khác nhau nhưng 15 đề có mặt ở cả train và validation, nên chưa biết mô hình làm gì với một đề mới. Leave-one-prompt-out sẽ trả lời câu hỏi mà giáo viên thật sự gặp. Hai thí nghiệm này biến bài từ một benchmark thành một câu trả lời về việc đánh giá lập luận cần thông tin gì.

## **Tuần sau mang đến**

* Bảng tỷ lệ nhãn và đề trong bốn nhóm độ dài bài.  
* Kết quả đầu tiên của thí nghiệm ngữ cảnh, dù chỉ hai mức (đơn vị và đơn vị cùng câu lân cận).  
* Link notebook, và kết quả leave-one-prompt-out cho ít nhất vài đề.

## **Hai câu hỏi để các em tự trả lời**

* Trong mười ca Ineffective, ca nào sẽ được đoán đúng nếu mô hình thấy được đoạn văn xung quanh, và ca nào thì không?  
* Với một đề hoàn toàn mới, các em dự đoán macro-F1 sẽ giảm nhiều nhất ở loại đơn vị nào?

Các em đã sửa đúng những chỗ thầy hỏi. Bây giờ hãy viết bình tĩnh hơn và dùng phân tích lỗi để đặt câu hỏi nghiên cứu của riêng mình.

*Thầy Khánh*