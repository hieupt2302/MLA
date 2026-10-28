# **CLC02 Nhóm 6 · Nhận xét Tuần 10**

*PERSUADE 2.0: dự báo hiệu quả đơn vị lập luận*

## **Nhận xét chung**

Nhóm đã trả lời đủ các câu hỏi của Tuần 9 và có thêm ba thí nghiệm có kiểm soát. Thứ nhất là phân rã lỗi theo độ dài bài. Thứ hai là so Level 0 với Level 1 trên cùng 29.102 đơn vị, có bootstrap theo bài. Thứ ba là leave-one-prompt-out cho RF trên 15 đề và cho DeBERTa trên 3 đề. Phần rút lại các câu nói quá (κ người–máy, “trực tiếp do”) làm đúng. Official Test vẫn khóa và cấu hình cuối đã ghi rõ.

## **Dữ liệu đang nói gì**

Phát hiện về độ dài rất đẹp. Lỗi tăng theo độ dài bài không phải vì bài dài khó hơn với mô hình. Bài dài là bài của học sinh giỏi hơn (điểm holistic từ 2,38 lên 4,67), và khó khăn chuyển từ nhận ra Ineffective sang phân biệt Adequate với Effective (91,5% lỗi ở nhóm dài nhất). Ngữ cảnh lân cận giúp rất ít trên tổng thể (+0,0022, khoảng chứa 0); có tăng ở Claim nhưng giảm ở Position. Cần nhớ thêm một điều: κ giữa hai người chấm chỉ 0,316, nên một phần trần hiệu năng đến từ chính nhãn.

## **Những chỗ phải sửa**

**1\. \[Bắt buộc\] Sửa câu kết luận ở mục 7.2**

**Ở đâu:** Mục 7.2, đoạn “Trực tiếp trả lời”.

**Vấn đề:** Câu “dữ liệu thực nghiệm chứng minh … trần hiệu năng bị chặn bởi thiếu thông tin đầu vào chứ không do mô hình học kém” mạnh hơn bằng chứng. Nhóm mới thử Level 0 và 1; Level 2 và 3 chưa thử; và nhãn người–người chỉ có κ 0,316.

**Cần làm:** Viết lại: Level 1 không cải thiện rõ; cùng với 10 ca đã đọc, kết quả này phù hợp với giả thuyết cần bài đọc nguồn và toàn bài, nhưng chưa kiểm chứng. Thêm một câu về độ tin cậy của nhãn.

**Xong khi:** Không còn chữ “chứng minh” trong mục 7.2.

**2\. \[Bắt buộc\] Chấm cả mốc trong lần chạy test duy nhất**

**Ở đâu:** Mục 1.3, cấu hình khóa.

**Vấn đề:** Level 1 được chọn với chênh \+0,0022 so với Level 0 (khoảng chứa 0); không có mốc trên test thì không đọc được số của Level 1\.

**Cần làm:** Ghi trong protocol: chấm cùng lượt RF (Feature Set B), DeBERTa Level 0 và Level 1; ghi rõ L0 và L1 không phân biệt được trên validation.

**Xong khi:** Protocol liệt kê ba hệ thống; bảng test có ba dòng.

**3\. \[Bắt buộc\] Tách độ dài khỏi trình độ**

**Ở đâu:** Mục 3\.

**Vấn đề:** Độ dài và điểm holistic đi cùng nhau, nên chưa biết riêng độ dài có ảnh hưởng không.

**Cần làm:** Tính tỷ lệ lỗi theo bốn nhóm độ dài trong cùng một mức điểm holistic (ví dụ chỉ bài điểm 3, chỉ bài điểm 4).

**Xong khi:** Bảng điểm × nhóm độ dài; một câu: trong cùng điểm, lỗi có tăng theo độ dài không.

**4\. \[Nên làm\] Ghi ca “paragraph 36” là giả thuyết**

**Ở đâu:** Mục 5.3, ca 2\.

**Vấn đề:** Nhóm chưa mở bài đọc nguồn để biết đoạn 36 có tồn tại không.

**Cần làm:** Đổi “know paragraph 36 does not exist” thành một giả thuyết, hoặc kiểm tra bài đọc nguồn nếu có.

**Xong khi:** Câu được viết đúng mức.

**5\. \[Nên làm\] Xuất bản cuối từ Word hoặc LaTeX**

**Ở đâu:** Toàn báo cáo.

**Vấn đề:** Bản PDF in từ HTML làm nhiều bảng vỡ cột, khó đọc.

**Cần làm:** Xuất bản cuối từ docx hoặc LaTeX.

**Xong khi:** Mọi bảng đọc được theo hàng và cột.

## **Hướng đi vừa sức**

Việc khoa học còn lại là một lần chấm Official Test và một bảng tách độ dài khỏi trình độ.

**Bước 1\.** Bảng điểm × độ dài trên validation.

**Bước 2\.** Khóa protocol với ba hệ thống, chạy test một lần.

**Bước 3\.** Viết lại mục 7.2.

**Nếu kết quả không như mong đợi:** Nếu trong cùng mức điểm lỗi vẫn tăng theo độ dài, giả thuyết A (độ phức tạp) không bị loại; viết cả hai khả năng.

## **Kế hoạch**

**Trước buổi review tuần 10**

* Sửa mục 7.2.  
* Bảng điểm × độ dài.

**Trước interview (từ tuần 11\)**

* Chạy test một lần.  
* Mỗi người giải thích được bảng phân rã lỗi ở nhóm dài nhất.

## **Chuẩn bị cho review và interview**

**Mỗi thành viên phải tự giải thích được, bằng lời của mình:**

* Dữ liệu: vì sao lỗi tăng theo độ dài không có nghĩa bài dài khó hơn với mô hình?  
* Đánh giá: κ mô hình 0,37 và κ giữa người chấm 0,316 vì sao không so trực tiếp?  
* Mô hình: LOPO khác in-domain ở đâu, và vì sao đề Cowboy giảm nhiều nhất?

**Mang theo:**

* Protocol khóa.  
* File outputs/context\_ablation\_case\_study\_recheck.csv.

**Đề xuất hướng đi:** Đề xuất câu kết luận chính về ngữ cảnh, viết đúng mức.

## **Một lượt đi qua để luyện interview**

1\. Chọn ca 8, đơn vị Claim “Some kids will ask there parents to transfer school”, nhãn gold Ineffective.

2\. Input Level 0 và Level 1 (thêm đơn vị trước và sau).

3\. DeBERTa cho P(Ineffective) 0,021 ở Level 0 và 0,124 ở Level 1; argmax vẫn là Adequate.

4\. Giải thích vì sao ngữ cảnh làm mô hình nghi ngờ hơn nhưng không đủ đổi nhãn.

5\. Kiểm tra trực tiếp: hạ ngưỡng quyết định cho lớp Ineffective trên file xác suất đã lưu, xem bao nhiêu ca đổi.

Các em đã đi đúng hướng thầy gợi ý và giữ được kỷ luật với tập test. Lần chấm cuối và một bảng tách độ dài với trình độ là đủ cho báo cáo.

*Thầy Khánh*