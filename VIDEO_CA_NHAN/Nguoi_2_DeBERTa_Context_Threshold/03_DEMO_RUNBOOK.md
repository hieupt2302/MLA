# Demo runbook: Người 2 (khoảng 1 phút 55 giây sau khi cắt)

## Cách dễ nhất: notebook `demo/demo_nguoi2.ipynb` (khuyên dùng)

- Mở `Nguoi_2_DeBERTa_Context_Threshold/demo/demo_nguoi2.ipynb` trong VS Code hoặc Jupyter. File đã có **output lưu sẵn**, nên có thể quay ngay mà không cần chạy lại.
- Muốn chạy lại thì bấm **Run All**:
  - mất khoảng 10 giây khi không có CSV gốc;
  - mất khoảng 30–40 giây khi có CSV gốc. Cắt đoạn chờ này khi dựng video.
- Zoom VS Code (Ctrl + =) tới khi chữ bảng to rõ. Bảng hiển thị sẵn cỡ 18px.
- Thứ tự cuộn khi quay: ① TABLE 2 → ② chuỗi L0/L1 + bảng xác suất → ③ bảng θ (sửa `THETA = 0.20` rồi chạy lại cell nếu muốn demo trực tiếp) → ④ ca 8.
- Notebook dùng **cùng hàm và cùng số** với `demo_nguoi2.py` và slide. Cách terminal bên dưới vẫn dùng được nếu thích.
- Dựng lại notebook: `python VIDEO_CA_NHAN/build/build_demo_notebooks.py`.

## Chuẩn bị

- Python 3.10+ có `pandas` và `scikit-learn`.
- **Tuỳ chọn:** CSV gốc `data/persuade_raw/persuade_corpus_2.0_train.csv`.
  - Có CSV thì demo in nguyên văn đơn vị trước, đích và sau.
  - Không có CSV thì script in câu đích lấy từ bảng `D7_raw_examples_traced.csv`, báo rõ là thiếu văn bản lân cận, rồi vẫn chạy phần ②③ bình thường.
- 2 tab terminal, font 18–20pt:
  - Tab A ở `MLA_Final/Code`;
  - Tab B ở thư mục gốc repo.

## Các bước quay

| # | Ở đâu | Lệnh / thao tác | Nói gì | Trỏ vào |
|---|---|---|---|---|
| 1 | Tab A | `python reproduce_results.py` | "First, the group's reproduction script…" | TABLE 2, dòng Macro-F1 delta |
| 2 | Tab B | `python VIDEO_CA_NHAN/Nguoi_2_DeBERTa_Context_Threshold/demo/demo_nguoi2.py --theta 0.10` | "Now my demo script…" | Khối ① (chuỗi L0, chuỗi L1, xác suất) |
| 3 | Tab B | — | "Part two asks a practical question…" | Khối ②: argmax so với θ |
| 4 | Tab B | — | "And case 8…" | Khối ③ |
| (tuỳ chọn) | Tab B | chạy lại với `--theta 0.20` | "With 0.20 the trade-off is milder…" | Recall 60,0%, Macro-F1 0,558 |

`[CUT]`: đọc CSV gốc mất 20–40 giây, cắt đoạn đó; hoặc thêm `--no-raw`.

## Output mong đợi (cập nhật sau khi build)

```
① CASE 8  validation row_idx 108613 | Claim | Cell phones at school | gold Ineffective
   L0 input: Claim [SEP] Some kids will ask there parents to transfer school
   L1 input: Claim [SEP] Previous: They will hide them from the teachers ... [SEP] Target: Some kids will ask there parents to transfer school [SEP] Next: If you chose policy one you will make the student happy.
   L0 (locked)  P(Ineff/Adeq/Eff) = 0.017 / 0.962 / 0.021 -> Adequate
   L1 (locked)  P(Ineff/Adeq/Eff) = 0.058 / 0.937 / 0.005 -> Adequate

② FLAG IF P(Ineffective) >= θ   (locked L1, validation, 29,102 units, 1,328 gold Ineffective)
   rule      flagged   recall   precision   Macro-F1
   argmax      1,761    44.7%      33.7%      0.581
   θ=0.10      4,633    69.6%      19.9%      0.535
   extra correct flags: 330 | extra false alarms: 2,542  (≈ 7.7 per catch)

③ case 8: P(Ineffective) = 0.058 < θ = 0.10 -> not flagged
```

## Mở thêm nếu cần

- `MLA_Final/Code/notebooks/05_threshold_tuning_and_case8.ipynb`: notebook gốc, đã có output.
- `MLA_Final/Results/tables/R4a_L1_vs_L0_same_units_deltas.csv`.
