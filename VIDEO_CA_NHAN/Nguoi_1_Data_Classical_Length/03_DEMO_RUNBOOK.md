# Demo runbook: Người 1 (khoảng 1 phút 55 giây sau khi cắt)

## Cách dễ nhất: notebook `demo/demo_nguoi1.ipynb` (khuyên dùng)

- Mở `Nguoi_1_Data_Classical_Length/demo/demo_nguoi1.ipynb` trong VS Code hoặc Jupyter. File đã có **output lưu sẵn**, nên có thể quay ngay mà không cần chạy lại.
- Muốn chạy lại thì bấm **Run All**:
  - mất khoảng 10 giây khi không có CSV gốc;
  - mất khoảng 30–40 giây khi có CSV gốc. Cắt đoạn chờ này khi dựng video.
- Zoom VS Code (Ctrl + =) tới khi chữ bảng to rõ. Bảng hiển thị sẵn cỡ 18px.
- Thứ tự cuộn khi quay: ① RF row của TABLE 1 → ② bảng trace + hình → ③ dòng 728 ID → ④ bảng recall theo quartile + hình.
- Notebook dùng **cùng hàm và cùng số** với `demo_nguoi1.py` và slide. Cách terminal bên dưới vẫn dùng được nếu thích.
- Dựng lại notebook: `python VIDEO_CA_NHAN/build/build_demo_notebooks.py`.

## Chuẩn bị (trước khi bấm quay)

- Python 3.10+ có `pandas`, `scikit-learn` (đã có nếu cài `MLA_Final/Code/requirements.txt`).
- **Tuỳ chọn:** đặt CSV gốc tại `data/persuade_raw/persuade_corpus_2.0_test.csv` và `..._train.csv`.
  - Có CSV thì demo in nguyên văn đơn vị và đếm `discourse_id` trực tiếp.
  - Không có CSV thì script tự lấy từ bảng đã lưu (`D7_raw_examples_traced.csv`, `D4_identifier_integrity.csv`) và **in rõ là đang dùng bảng đã lưu**.
- Mở 2 tab terminal, font 18–20pt:
  - Tab A ở `MLA_Final/Code`;
  - Tab B ở thư mục gốc repo.
- Gõ sẵn lệnh, chưa nhấn Enter.

## Các bước quay

| # | Ở đâu | Lệnh / thao tác | Nói gì (script) | Trỏ vào |
|---|---|---|---|---|
| 1 | Tab A | `python reproduce_results.py` | "First, our reproduction script…" | Hai dòng `Random Forest (FS-B)` của TABLE 1; dòng `[SUCCESS]` cuối |
| 2 | Tab B | `python VIDEO_CA_NHAN/Nguoi_1_Data_Classical_Length/demo/demo_nguoi1.py` | "Now my own demo script…" | Khối ① TRACE |
| 3 | Tab B | (cuộn lên nếu cần) | "Part two is the identifier check…" | Khối ② dòng `distinct discourse_id` |
| 4 | Tab B | — | "Part three is new to this video…" | Khối ③ bảng recall theo quartile |

`[CUT]`: cắt mọi đoạn chờ trên 1 giây. Nếu có CSV gốc, script mất khoảng 20–40 giây để đọc file 1 GB; **cắt đoạn đó**, hoặc chạy với `--no-raw` cho nhanh.

## Output mong đợi (đã chạy thử, sẽ cập nhật sau khi build)

```
① TRACE  test row_idx 47059  (raw record 57633)
   prompt: Facial action coding system | type: Position | essay words: 225 -> Q1 (<=315)
   text  : "That is all everything you need to know about Mona Lisa and her smile."
   label : "Ineffective" -> id 0   (Ineffective=0, Adequate=1, Effective=2)
   RF FS-B  P(Ineff/Adeq/Eff) = 0.544 / 0.342 / 0.114 -> predicts Ineffective (correct)
   DeBERTa L1 (locked) P(Ineff) = 0.978 -> predicts Ineffective

② ID CHECK  train+val annotated units 144,289 | distinct discourse_id 728  -> join on row_idx

③ INEFFECTIVE RECALL BY ESSAY-LENGTH QUARTILE (official test, saved predictions)
   quartile        gold Ineff   RF recall   DeBERTa L1 recall
   Q1 (<=315)          2,384      23.3%          45.1%
   Q2 (316-422)          934      13.7%          38.4%
   Q3 (423-566)          598       6.9%          35.6%
   Q4 (>=567)            309       0.6%          35.0%
```

## Nếu thầy hỏi thêm (không quay, chỉ để biết)

- File gốc của bảng điểm × độ dài: `Person1/output/holistic_score_x_length_quartile_error_rates.csv`.
- Kết quả RF LOPO 15 đề: `outputs/lopo_classical_results.csv`, lọc các dòng `overall`.
- Lý do sửa bảng và sửa RF: `RA_SOAT_TUAN11_SO_VOI_NHAN_XET_TUAN10.md` mục B1, B2.
