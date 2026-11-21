# VIDEO CÁ NHÂN — GROUP 06 (CLC02)

Bộ nội dung để mỗi thành viên quay **một video riêng** (`Video/StudentID_Name.mp4`, 10% điểm).

**Ngày soạn:** 20/11/2026
**Nguồn chuẩn của phân vai:** `final_report/PHAN_CONG_VA_ON_TAP_GROUP06.md`, phần 3.
**Nguồn chuẩn của số liệu:**
- `final_report/report_src/*.md` (bản luận);
- `final_report/tables/*.csv` và `MLA_Final/Results/`.

Mỗi số trong script đều ghi rõ file nguồn trong `02_SLIDE_SPEC.md`.

---

## 1. Ai quay video nào

Chia theo **vai**, lấy công việc **tuần 10–11** làm trục. Người giữ vai ở tuần 10–11 quay video của vai đó. Phần tuần 9 chỉ nhắc một câu.

| Thư mục | Vai | Mạch chính | Ví dụ thật (không trùng nhau) |
|---|---|---|---|
| `Nguoi_1_Data_Classical_Length/` | Người 1: dữ liệu, mô hình cổ điển, độ dài | RF Feature Set B, RF LOPO 15 đề, độ dài bài so với điểm | Test `row_idx` 47059: Position, đề "Facial action coding system", gold Ineffective |
| `Nguoi_2_DeBERTa_Context_Threshold/` | Người 2: DeBERTa, ngữ cảnh, ngưỡng, SVM | L0 so với L1 trên cùng đơn vị; quét ngưỡng; ca 8 | Ca 8: validation `row_idx` 108613, Claim, đề "Cell phones at school" |
| `Nguoi_3_TestGovernance_LOPO_Ladder/` | Người 3: phân tích lỗi, LOPO, quản lý test | Chấm test một lần, file khóa; LOPO; thang ngữ cảnh | Ca 2: validation `row_idx` 10303, Evidence, đề "Car-free cities" |

Tên và MSSV điền vào chỗ `[tự điền: …]` trong `01_SCRIPT_EN.md` và slide 1 của từng thư mục.

## 1b. Hai phiên bản: 5 phút và 7–8 phút

| Phiên bản | Script / slide spec | Output | Độ dài |
|---|---|---|---|
| **5 phút** (theo khung nhóm trong `requirement video.md`) | `01_SCRIPT_EN_5MIN.md`, `02_SLIDE_SPEC_5MIN.md` (7 slide) | `output/Nguoi_N_slides_5min.pptx`, `Nguoi_N_script_5min.docx`, `preview_5min/` | 650–720 từ |
| 7–8 phút (bản đầy đủ) | `01_SCRIPT_EN.md`, `02_SLIDE_SPEC.md` (9 slide) | `output/Nguoi_N_slides.pptx`, `Nguoi_N_script.docx`, `preview/` | khoảng 1.000–1.100 từ |

Hai bản dùng cùng ví dụ, hình và script demo.

Bản 5 phút theo 5 phần của nhóm: giới thiệu, vai trò và phương pháp, ví dụ thật và demo, kết quả, lỗi/hạn chế và kết luận.

`03_DEMO_RUNBOOK.md` và `04_GHI_CHU_TIENG_VIET.md` dùng chung cho cả hai bản. Bản 5 phút chỉ quay demo khoảng 25 giây, nên chỉ trỏ vào các khối chính.

## 2. Mỗi thư mục có gì

| File | Dùng để làm gì |
|---|---|
| `01_SCRIPT_EN.md` | Lời nói tiếng Anh theo timecode. Cue `[SLIDE n]`, `[DEMO]`, `[CUT]` báo lúc chuyển cảnh |
| `02_SLIDE_SPEC.md` | Nội dung từng slide: tiêu đề, bullet, hình, chú thích, nguồn số liệu. `build/build_pptx.py` đọc file này |
| `03_DEMO_RUNBOOK.md` | Lệnh chạy, file cần mở, chỗ zoom, chỗ cắt, output mong đợi |
| `04_GHI_CHU_TIENG_VIET.md` | Giải thích từng ý bằng tiếng Việt, từ khó và cách đọc, câu dễ nói sai, câu thầy có thể hỏi |
| `demo/demo_nguoiN.py` | Script demo, chạy dưới 10 giây, chỉ đọc file đã lưu trong `MLA_Final/` |
| `demo/demo_nguoiN.ipynb` | **Notebook demo có output lưu sẵn**, mở ra là quay được ngay; cùng số với script và slide (dựng lại bằng `build/build_demo_notebooks.py`) |
| `visuals/` | Hình dùng trong slide (PNG) |
| `output/` | `Nguoi_N_slides.pptx` (script nằm trong speaker notes), `Nguoi_N_script.docx` (bản teleprompter), `preview/` (ảnh từng slide) |

Thư mục `_chung/` có:
- `STYLE.md`: quy ước slide;
- `slide_intro_problem.md`: đoạn giới thiệu bài toán, cả 3 người dùng chung;
- `QUAY_VA_XUAT_VIDEO.md`: cách quay, cách xuất, checklist xem lại.

## 3. Đối chiếu với yêu cầu của đề

Mỗi script có cùng khung khoảng 7 phút 30 giây:

| Yêu cầu của đề | Ở đâu trong video | Slide/cảnh |
|---|---|---|
| Present in English, in your own voice | Cả video, tự đọc, không dùng TTS | — |
| Briefly introduce the problem | 0:10–0:45 | Slide 2 (chung) |
| Identify your contribution | 0:45–1:15 và tóm tắt cuối | Slide 3, Slide 9 |
| Real example, from data to prediction | 1:15–2:45 | Slide 4 |
| Chart, table or annotated example: what the data shows | 2:45–4:15 | Slide 5–6 |
| Demonstrate with notebook/saved outputs | 4:15–6:15 | Slide 7 rồi quay màn hình (DEMO) |
| Interpret one result, error or limitation | 6:15–7:10 | Slide 8 |
| MP4 ≥1080p, clear audio, readable, trimmed, reviewed | — | `_chung/QUAY_VA_XUAT_VIDEO.md` |

## 4. Quy trình cho mỗi người

1. Đọc `04_GHI_CHU_TIENG_VIET.md` để hiểu rõ từng ý.
2. Chạy thử `03_DEMO_RUNBOOK.md` trên máy mình. Script demo chỉ cần thư mục `MLA_Final/`; CSV gốc không bắt buộc.
3. Mở `output/Nguoi_N_slides.pptx` và sửa tên/MSSV ở slide 1.
4. Đọc to script 2–3 lần, bấm giờ. Nói tự nhiên và được phép diễn đạt lại; **chỉ giữ nguyên các con số**.
5. Quay theo `_chung/QUAY_VA_XUAT_VIDEO.md`, xuất `StudentID_Name.mp4` và chép vào `Video/` của thư mục nộp.

## 5. Dựng lại pptx/docx sau khi sửa md

Chạy từ thư mục gốc repo, Python 3.10+ có `python-pptx`, `python-docx`, `matplotlib`, `pandas`:

```
python VIDEO_CA_NHAN/build/make_visuals.py
python VIDEO_CA_NHAN/build/build_pptx.py            # cả hai bản; --variant 5min hoặc full để chọn một bản
python VIDEO_CA_NHAN/build/build_script_docx.py      # tương tự
powershell -ExecutionPolicy Bypass -File VIDEO_CA_NHAN/build/render_preview.ps1
python VIDEO_CA_NHAN/build/check_numbers.py
```

## 6. Lưu ý trước khi nộp

- `MLA_Final/README.md` mục 1 đang mô tả vai **khác** với PHAN_CONG:
  - ghi thang ngữ cảnh rộng là của Role 2 (hồ sơ ghi là của Người 3);
  - ghi RF LOPO 15 đề là của Role 3 (hồ sơ ghi là của Người 1);
  - ghi validation gate RF là 0,523 (bản tái tạo là 0,5261).

  Đề yêu cầu README, báo cáo và video là cùng một phiên bản, nên cần sửa README cho khớp với video.
- Không ai được nói một việc của vai khác là "I did". Phần của người khác thì nói "my teammate …" hoặc "the group …".
