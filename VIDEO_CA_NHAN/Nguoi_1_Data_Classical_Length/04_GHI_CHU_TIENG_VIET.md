# Ghi chú tiếng Việt: Người 1

## 1. Ý chính của video trong 3 câu

1. Bạn làm phần **mô hình cổ điển và dữ liệu**:
   - RF Feature Set B chấm test **sau khi tái tạo validation**;
   - RF LOPO 15 đề;
   - bảng độ dài × điểm.
2. Độ dài bài **gắn với trình độ** (ρ = 0,76), nhưng trong cùng một mức điểm lỗi vẫn tăng theo độ dài (OR 1,19).
3. Phát hiện riêng trong video:
   - RF bắt Ineffective gần như chỉ ở bài ngắn: recall 23,3% ở Q1, chỉ 0,6% ở Q4;
   - DeBERTa giảm ít hơn nhiều: 45,1% → 35,0%;
   - nghĩa là RF dựa nhiều vào **độ dài bài** (một trong 5 đặc trưng cấu trúc), mà độ dài lại là dấu hiệu gián tiếp của trình độ.

## 2. Giải thích từng slide

| Slide | Ý cần hiểu | Đừng nói sai |
|---|---|---|
| 3 | "Validation gate": trước khi chấm test, chạy lại đúng cấu hình RF trên validation và phải ra khoảng 0,52 (tái tạo được 0,5261). Đạt rồi mới chấm test, và chỉ chấm **một lần** | Không nói "RF đạt 0,523 trên test". Test là **0,510** |
| 4 | `raw record` = số thứ tự dòng trong file CSV gốc. `row_idx` = số thứ tự sau khi bỏ dòng không có nhãn. Mọi file dự đoán đều khoá theo `row_idx` | Không nói ghép theo `discourse_id`. ID đó đã bị Excel làm tròn (728 giá trị / 144.289 đơn vị) |
| 4 | Feature Set B = TF-IDF từ đơn + cặp từ (tối đa 15.000) + one-hot loại (7 cột) + 5 đặc trưng cấu trúc: độ dài đơn vị (ký tự, từ), **độ dài bài**, vị trí bắt đầu tương đối, tỉ lệ độ dài đơn vị/bài | — |
| 4 | RF: 200 cây, sâu tối đa 35, `class_weight="balanced"`, seed 42. Xác suất là trung bình phiếu của các cây | — |
| 5 | Spearman 0,76 là tương quan **thứ hạng** giữa số từ của bài và điểm holistic (1–6) | Không nói "bài dài thì tốt hơn". Chỉ nói "đi cùng nhau" |
| 6 | Hình 20 là lỗi của **DeBERTa L1 đã khoá**, không phải của RF. OR 1,19: mỗi bậc tứ phân vị độ dài làm odds lỗi tăng 19%, đã kiểm soát điểm | Không nói "chứng minh". Nói "suggests / is consistent with" |
| 8 | Recall theo quartile được **tính trong demo** từ file dự đoán đã lưu. Báo cáo không có bảng này, nên phải nói rõ "new to this video, computed from saved predictions" | Không nói nguyên nhân chắc chắn là đặc trưng độ dài. Chưa train lại bỏ đặc trưng đó, nên chỉ là **suy luận** |
| 9 | Hai lỗi bản đầu (ghép theo ID, RF test chưa đúng FS-B) được phát hiện trong đợt rà soát 31/10 rồi chạy lại | Nói thật. Rubric đánh giá cao việc nêu và sửa sai |

## 3. Từ khó và cách đọc

| Từ | Đọc | Nghĩa |
|---|---|---|
| discourse unit | /dɪˈskɔːrs ˈjuːnɪt/ | đơn vị luận điểm |
| holistic score | /hoʊˈlɪstɪk/ | điểm tổng thể của bài (1–6) |
| quartile | /ˈkwɔːrtaɪl/ | nhóm tứ phân vị |
| odds ratio | /ɑːdz ˈreɪʃioʊ/ | tỉ số odds |
| confounded | /kənˈfaʊndɪd/ | bị lẫn yếu tố gây nhiễu |
| leave-one-prompt-out | — | giấu một đề khi train, rồi chấm trên đề đó |
| TF-IDF | "tee-eff-eye-dee-eff" | trọng số từ |

## 4. Đọc số bằng tiếng Anh

- 0.526: "zero point five two six"
- 144,289: "one hundred forty-four thousand, two hundred eighty-nine"
- 57,633: "fifty-seven thousand, six hundred thirty-three"
- 19.3 percent: "nineteen point three percent"
- 1.19: "one point one nine"

## 5. Câu thầy có thể hỏi sau khi xem video

- *Vì sao không bỏ đặc trưng độ dài bài?* Đó là đặc trưng có sẵn lúc dự đoán, nên hợp lệ. Nhưng nó khiến RF khai thác trình độ một cách gián tiếp. Bước tiếp theo là ablation bỏ đặc trưng này và so trên cùng validation.
- *RF LOPO thấp nhất ở đề nào?* "A Cowboy Who Rode the Waves", 0,350. 4 trong 5 đề khó nhất là đề dựa trên bài đọc nguồn.
- *Vì sao recall RF thấp mà accuracy cao (78,5%)?* RF bám lớp Adequate, lớp chiếm 80%.
