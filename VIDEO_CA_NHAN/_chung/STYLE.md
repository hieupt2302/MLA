# Quy ước slide và định dạng file nguồn

## 1. Thiết kế slide

- Kích thước 16:9 (13,333 × 7,5 inch). Xuất ảnh/video ở 1920×1080.
- Bảng màu giống `build_editable_pptx.py` (đã dùng cho slide giữa kỳ):

  | Vai trò | Màu |
  |---|---|
  | Nền | `#F8FAFC` |
  | Chữ chính / thanh tiêu đề | navy `#0F172A` |
  | Nhấn mạnh | blue `#2563EB` |
  | Chữ phụ | gray `#64748B` |
  | Đúng / tốt | green `#16A34A` |
  | Cảnh báo / giới hạn | orange `#D97706` |
  | Sai / Ineffective | red `#DC2626` |

  Màu nhãn **cố định** trong mọi hình: Ineffective = `#DC2626`, Adequate = `#94A3B8`, Effective = `#2563EB`.
- Font: tiêu đề Trebuchet MS 34–36pt đậm; thân Calibri **≥ 20pt**; chú thích hình ≥ 14pt; dòng nguồn 12pt màu xám.
- Mỗi slide tối đa 5 bullet, mỗi bullet tối đa khoảng 14 từ. Phần còn lại để lời nói.
- Góc dưới phải mỗi slide có số slide và "Group 06 · CLC02 · <Role>".
- Hình chiếm ít nhất 55% chiều rộng khi slide có hình. Không kéo giãn méo hình, giữ tỉ lệ.

## 2. Định dạng `02_SLIDE_SPEC.md` (để `build/build_pptx.py` đọc)

Mỗi slide bắt đầu bằng một dòng `## Slide <n> | <layout>`. Sau đó là các khóa:

```
## Slide 4 | bullets_image
title: Một dòng tiêu đề
subtitle: (tuỳ chọn) dòng phụ dưới tiêu đề
bullets:
- bullet 1
- bullet 2
image: visuals/v1_example_trace.png
caption: Chú thích dưới hình
callout: (tuỳ chọn) một câu nhấn mạnh, in trong hộp màu
source: (tuỳ chọn) nguồn số liệu, in nhỏ cuối slide
```

**Các layout:**

| Layout | Bố cục |
|---|---|
| `title` | Tiêu đề lớn, `subtitle`, và các dòng `bullets` làm thông tin người nói |
| `bullets` | Tiêu đề + bullets + `callout` |
| `bullets_image` | Bullets bên trái (khoảng 38%), hình bên phải |
| `image` | Một hình lớn chiếm gần hết slide, `caption` ở dưới |
| `table` | Tiêu đề + bảng markdown nằm dưới khóa `table:` + `callout` |
| `demo` | Slide chuyển cảnh "Live demo": `bullets` là các bước sẽ làm |

**Quy tắc:**
- Bảng markdown đặt ngay sau dòng `table:`, viết theo cú pháp `| a | b |` bình thường.
- `image:` là đường dẫn tương đối tính từ thư mục của người đó. Hình chung thì dùng `../_chung/visuals/...`.

## 3. Định dạng `01_SCRIPT_EN.md`

- Mỗi đoạn bắt đầu bằng `## [SLIDE n] m:ss–m:ss — tiêu đề` hoặc `## [DEMO] m:ss–m:ss — tiêu đề`.
- Lời nói là các đoạn văn thường.
- Dòng bắt đầu bằng `>` là **chỉ dẫn sân khấu**, không đọc: bấm chuột, zoom, cắt…
- `build_pptx.py` đưa lời nói của `[SLIDE n]` vào speaker notes của slide n. Lời của `[DEMO]` đưa vào notes của slide `demo`.
- `build_script_docx.py` in toàn bộ thành bản teleprompter:
  - lời nói cỡ 16pt;
  - chỉ dẫn in nghiêng màu xám;
  - timecode in đậm.
