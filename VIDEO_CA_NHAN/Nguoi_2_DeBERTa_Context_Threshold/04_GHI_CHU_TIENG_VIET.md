# Ghi chú tiếng Việt: Người 2

## 1. Ý chính của video trong 3 câu

1. Bạn thiết kế thí nghiệm **có kiểm soát**: L0 (chỉ đơn vị) so với L1 (thêm đơn vị trước và sau). Mọi thứ khác giữ nguyên: cùng dữ liệu train, cùng cấu hình, cùng seed, chấm trên cùng đơn vị.
2. Kết quả: L1 tốt hơn **một chút và nhất quán** (test +0,016 Macro-F1, Ineffective F1 +0,029). Mức tăng này ngang dao động giữa hai lượt train, vì lượt đầu chỉ được +0,002.
3. Hạ ngưỡng θ thì recall Ineffective tăng, nhưng độ chính xác giảm mạnh, khoảng 8 báo nhầm cho mỗi ca bắt thêm. Ngưỡng là **lựa chọn của người dùng**, không làm mô hình tốt hơn.

## 2. Giải thích từng slide

| Slide | Ý cần hiểu | Đừng nói sai |
|---|---|---|
| 3 | +0,054 [0,043; 0,065] là DeBERTa L0 so với RF trên **cùng validation**, ở lượt chạy tuần 9 | Không nói đó là số test |
| 4 | Chuỗi L1 có dạng `type [SEP] Previous: … [SEP] Target: … [SEP] Next: …`, ở đầu/cuối bài thì dùng `[NONE]`. Tokenizer SentencePiece của DeBERTa-v3, tối đa 512 token. Vector `[CLS]` → lớp tuyến tính → softmax 3 lớp | Xác suất ca 8 trong video là của **mô hình đã khoá tuần 11** (L0 0,017; L1 0,058). Bảng 7.4 trong báo cáo có số khác (0,021 / 0,124) vì đó là lượt chạy tuần 9–10. Nếu thầy hỏi thì giải thích như vậy |
| 5 | Mô hình chấm test do đồng đội (Người 3) train lại ở tuần 11, theo đúng công thức của bạn. Bạn nói "trained by my teammate with the same recipe" | Không nói "I trained the locked model" |
| 6 | 15,2% dự đoán đổi nhãn; số đúng thêm chỉ nhỉnh hơn số sai thêm. Gain tập trung ở Counterclaim, Rebuttal, Claim, là các loại được chấm **so với đơn vị bên cạnh** | — |
| 8 | Quy tắc: nếu P(Ineff) ≥ θ thì gắn Ineffective, ngược lại chọn lớp lớn hơn giữa Adequate và Effective. θ chỉ được xem trên **validation** | Không nói "θ = 0,10 tốt hơn". Không nói ca 8 được cứu |
| 9 | Đính chính phần của bạn: bản đầu ghi 76,51%, số đúng 73,04% (lượt L1 đầu). Script ngưỡng được viết lại trong đợt rà soát 31/10 | Nói thật, ngắn gọn |

## 3. Từ khó và cách đọc

| Từ | Đọc | Nghĩa |
|---|---|---|
| DeBERTa | "deh-BER-tah" | mô hình transformer encoder |
| tokenizer / sub-word | — | tách từ thành mảnh nhỏ |
| softmax | — | biến điểm thành xác suất cộng lại bằng 1 |
| operating point | — | điểm vận hành (cặp recall/precision) |
| bootstrap by essay | — | lấy mẫu lại theo **bài**, vì các đơn vị trong cùng bài không độc lập |
| theta (θ) | "THAY-tah" | ngưỡng |

## 4. Câu thầy có thể hỏi

- *Vì sao khoá L1 mà không phải L0?* Vì Ineffective F1 trên validation cao hơn (+0,019 ở lượt đầu), không phải vì Macro-F1 rõ ràng cao hơn.
- *Vì sao 10 ca không đổi nhãn ở L1?* Đa số cần thông tin xa hơn hai câu lân cận (cả bài, đề, nguồn), hoặc yếu ngay trong câu.
- *SVM có QWK không?* Không có. SVM test 0,482 được train trên train + validation. Cùng cấu hình train trên 115.187 đơn vị cho validation 0,485.
