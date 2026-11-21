# Ghi chú tiếng Việt: Người 3 (vai của bạn)

## 1. Ý chính của video trong 3 câu

1. Tập test được chấm **đúng một lần**:
   - mọi lựa chọn đều làm trên validation;
   - file test được băm SHA-256 và ghi vào file khoá ngày 28/10;
   - mọi con số đều tính lại được từ file dự đoán đã lưu.
2. Đề chưa thấy khi train làm DeBERTa giảm 0,025–0,092 Macro-F1. Lượt LOPO đầu bị **rò rỉ** vì chọn epoch trên chính đề bị giấu. Bạn phát hiện và chạy lại.
3. Ngữ cảnh rộng hơn giúp một số ca riêng lẻ (ca 2), nhưng trên toàn validation thì chưa thấy cải thiện rõ.

## 2. Giải thích từng slide

| Slide | Ý cần hiểu | Đừng nói sai |
|---|---|---|
| 3 | Tuần 9 bạn giữ vai Người 1 (pipeline, chia theo bài). Tuần 10–11 bạn là Người 3. Mô hình L0/L1/PA dùng để chấm test là do bạn train ở tuần 11 | Không nhận phần chọn 10 ca. Đó là việc "our group selected" ở tuần 9 do người giữ vai 3 khi đó làm |
| 4 | Ca 2 dài 244 từ: trích đúng đoạn 36 của nguồn, sau đó lạc sang chuyện bằng lái. Theo bảng 7.5, cái yếu **nằm ngay trong đơn vị**. Ở mức "cả đoạn" đầu vào dài 747 token nên **bị cắt ở 512**. L3 dùng cửa sổ 1.536 token | Không nói "ngữ cảnh rộng sửa được lỗi". Chỉ nói "these inputs predict Ineffective for this case" |
| 5 | Kiểm tra "dời ngưỡng": hạ ngưỡng L1 cho tới khi số đơn vị bị gắn cờ bằng mô hình rộng, vẫn 0/10 ca đổi nhãn. Vậy các ca đổi nhãn không chỉ do ngưỡng | +0,025 là **post-hoc**, chỉ trên validation, 1 lượt, chưa chấm test |
| 6 | So LOPO với in-domain trên **cùng** bài validation của đề bị giấu. Summer có CI chứa 0 | Không nói "đề dựa trên nguồn thì khó hơn" như một kết luận. Chỉ là diễn giải |
| 8 | B27: lượt tuần 10 chọn epoch tốt nhất theo điểm trên đề bị giấu, tức là dùng thông tin kiểm tra để chọn mô hình. B16: transformers 5.x làm DeBERTa-v3 train lỗi. Chạy lại: transformers 4.57.6, bf16, Colab L4, cố định 3 epoch | Không nói "số mới tốt hơn". Số mới **thấp hơn**, và đó là đúng chiều khi bỏ rò rỉ |
| 9 | Hai lượt train cùng cấu hình lệch tới khoảng 0,003–0,004, nên chênh PA − L1 (validation 0,0045; CI test [−0,0002; +0,0074]) không kết luận được | — |

## 3. Từ khó và cách đọc

| Từ | Đọc | Nghĩa |
|---|---|---|
| governance | /ˈɡʌvərnəns/ | quy trình quản lý tập test |
| hash / SHA-256 | "shah two-five-six" | dấu vân tay của file |
| leave-one-prompt-out | — | giấu một đề khi train |
| leak / leakage | — | rò rỉ thông tin kiểm tra vào việc chọn mô hình |
| post-hoc | /poʊst hɑːk/ | phân tích làm sau khi đã thấy kết quả |
| pre-registered | — | đăng ký trước cách kiểm tra |
| calibration correction | — | chỉnh lệch xác suất giữa các lớp |

## 4. Câu thầy có thể hỏi

- *Băm file có đọc nhãn test không?* Không. SHA-256 chỉ đọc byte của file để so với mã đã ghi lúc khoá.
- *Vì sao PA không được khoá thay L1?* PA là thăm dò. Cấu hình khoá đã chọn trước (L1), và chênh PA − L1 nằm trong dao động giữa các lượt.
- *Sao biết ca 2 đổi nhãn không chỉ vì mô hình rộng gắn cờ nhiều hơn?* Vì đã hạ ngưỡng L1 cho tới khi nó gắn cờ bằng số đơn vị của mô hình rộng, và vẫn 0/10 ca đổi nhãn (báo cáo §7.3).
