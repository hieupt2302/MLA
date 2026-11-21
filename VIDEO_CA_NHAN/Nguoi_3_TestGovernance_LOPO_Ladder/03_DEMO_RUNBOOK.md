# Demo runbook: Người 3 (khoảng 1 phút 55 giây sau khi cắt)

## Cách dễ nhất: notebook `demo/demo_nguoi3.ipynb` (khuyên dùng)

- Mở `Nguoi_3_TestGovernance_LOPO_Ladder/demo/demo_nguoi3.ipynb` trong VS Code hoặc Jupyter. File đã có **output lưu sẵn**, nên có thể quay ngay mà không cần chạy lại.
- Muốn chạy lại thì bấm **Run All**:
  - mất khoảng 10 giây khi không có CSV gốc;
  - mất khoảng 30–40 giây khi có CSV gốc. Cắt đoạn chờ này khi dựng video.
- Zoom VS Code (Ctrl + =) tới khi chữ bảng to rõ. Bảng hiển thị sẵn cỡ 18px.
- Thứ tự cuộn khi quay: ① TABLE 1 + 3 → ② bảng khoá test (`matches lock True`) → ③ Macro-F1 tính lại → ④ ca 2 qua thang ngữ cảnh → ⑤ bảng LOPO.
- Notebook dùng **cùng hàm và cùng số** với `demo_nguoi3.py` và slide. Cách terminal bên dưới vẫn dùng được nếu thích.
- Dựng lại notebook: `python VIDEO_CA_NHAN/build/build_demo_notebooks.py`.
- **Lưu ý làm tròn:**
  - `reproduce_results.py` in khoảng hụt của Cowboy là **−0.091**;
  - notebook in **−0.0915** (in-domain 0.4755, LOPO 0.3840);
  - báo cáo (Bảng 6.7) ghi **−0.092**.

  Ba con số là cùng một giá trị, chỉ làm tròn khác nhau. Khi nói, dùng "about minus 0.09"; nếu thầy hỏi thì giải thích như trên.

## Chuẩn bị

- Python 3.10+ có `pandas` và `scikit-learn`.
- **Nên có** `data/persuade_raw/persuade_corpus_2.0_test.csv` (382 MB) để bước ① băm file. Không có thì script bỏ qua bước ① và in rõ lý do.
- 2 tab terminal, font 18–20pt:
  - Tab A ở `MLA_Final/Code`;
  - Tab B ở thư mục gốc repo.
- Trình duyệt mở sẵn `VAN_DAP_4_TIEU_CHI/trace_mau_that/TRACE_MAU_THAT_PIPELINE.html`, zoom 150%, cuộn tới phần "Ca 2". File này chỉ có trên máy bạn, vì thư mục đó nằm trong `.gitignore`.

## Các bước quay

| # | Ở đâu | Lệnh / thao tác | Nói gì | Trỏ vào |
|---|---|---|---|---|
| 1 | Tab A | `python reproduce_results.py` | "First, the group's reproduction script." | Các dòng `Test` của TABLE 1 (L1 0.577); TABLE 3 |
| 2 | Tab B | `python VIDEO_CA_NHAN/Nguoi_3_TestGovernance_LOPO_Ladder/demo/demo_nguoi3.py` | "My demo script checks the test governance…" | Khối ①: `sha256 matches lock: True` |
| 3 | Tab B | — | "Part two recomputes…" | Khối ②: 3 dòng L0/L1/PA, cột `paper` |
| 4 | Tab B | — | "Part three prints case 2…" | Khối ③ |
| 5 | Trình duyệt | Cuộn phần Ca 2: đầu vào từng mức → bảng token → bảng xác suất | "And this is my trace notebook…" | Bảng token (cả đoạn 747 token, bị cắt ở 512) và bảng P(Ineffective) |

`[CUT]`: băm 382 MB mất vài giây, cắt đoạn chờ.

## Output mong đợi (cập nhật sau khi build)

```
① TEST LOCK   locked_at 2026-10-28T21:15:35 UTC | n_test 93,677
   sha256 (lock) 8b4cbbda471b313e…
   sha256 (now)  8b4cbbda471b313e…  -> matches lock: True   (labels not read)

② TEST MACRO-F1 RECOMPUTED FROM SAVED PREDICTIONS (93,677 units)
   model                 recomputed   paper (R2)
   DeBERTa L0               0.5613      0.5613
   DeBERTa L1 (locked)      0.5772      0.5772
   DeBERTa Prompt-Aware     0.5808      0.5808

③ CASE 2  validation row_idx 10303 | Evidence | Car-free cities | gold Ineffective
   level          P(Ineffective)   prediction
   L0                  0.001       Effective
   L1 (locked)         0.008       Effective
   Prompt-Aware        0.002       Effective
   L1 ±2               0.028       Effective
   Paragraph           0.832       Ineffective
   L2 source           0.540       Ineffective
   L3 whole, 3 ep      0.733       Ineffective
   L3 whole, 7 ep      0.924       Ineffective

④ LOPO GAP (same validation essays): Cowboy −0.092 | Summer −0.025 | Distance −0.048
```

## Nếu thầy hỏi thêm

- `Week11_Person3_DeBERTa_OfficialTest/outputs/week11_person3/run_log.txt` và `OFFICIAL_TEST_LOCK.json`.
- `outputs/lopo_deberta_rerun_gap_same_units.csv`, `outputs/context_levels_validation_summary.csv`.
- `RA_SOAT_TUAN11_SO_VOI_NHAN_XET_TUAN10.md` mục B16, B27.
