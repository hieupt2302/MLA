# Quay và xuất video: hướng dẫn chung

## 1. Chuẩn bị máy (10 phút)

| Việc | Cách làm |
|---|---|
| Màn hình | Đặt độ phân giải **1920×1080**, scale 100%. Màn 2K/4K thì vẫn quay vùng 1920×1080 |
| Phần mềm quay | **OBS Studio**: Settings → Video: Base và Output đều 1920×1080, 30 FPS. Output: Recording format **mp4**, encoder H.264 (NVENC nếu có GPU), bitrate 8.000–12.000 Kbps. Audio 48 kHz |
| Mic | Tai nghe có mic hoặc mic USB, đặt cách miệng khoảng 15 cm. Tắt quạt và điều hoà. OBS: thêm filter **Noise Suppression (RNNoise)** cho mic |
| Terminal | Windows Terminal hoặc VS Code terminal, font **18–20pt**, nền tối, cửa sổ phóng to |
| VS Code / notebook | Zoom (Ctrl + =) tới khi chữ code cao khoảng 18–20px. File CSV mở bằng extension *Rainbow CSV* hoặc trong notebook với `pd.set_option('display.width', 120)` |
| Trình duyệt (HTML notebook) | Zoom 150% |
| PowerPoint | Slide Show toàn màn hình. Speaker notes xem trên màn hình thứ hai hoặc in bản `output/*_script.docx` |
| Dọn màn hình | Ẩn thông báo (Focus Assist), đóng tab không liên quan, **ẩn email/tên tài khoản cá nhân** trên thanh tiêu đề |

## 2. Quay

1. **Quay theo đoạn**, mỗi `[SLIDE n]` hoặc `[DEMO]` là một clip. Nói sai thì dừng 2 giây rồi nói lại câu đó, lúc dựng sẽ cắt.
2. Slide: dùng chế độ Slide Show, bật webcam nhỏ ở góc dưới phải nếu muốn (không bắt buộc). Nói thong thả, khoảng 130–150 từ/phút.
3. Demo:
   - gõ sẵn lệnh, quay lúc nhấn Enter;
   - nếu lệnh chạy quá 3 giây, đánh dấu để **cắt đoạn chờ** (`[CUT]` trong script);
   - khi nói về một con số, **trỏ chuột hoặc bôi đen** dòng đó trên màn hình.
4. Không dùng giọng AI/TTS. Không đọc script như máy; được phép diễn đạt lại, chỉ giữ đúng các số.

## 3. Dựng (Clipchamp có sẵn trên Windows, hoặc DaVinci Resolve / CapCut)

- Ghép clip theo thứ tự script, cắt khoảng lặng dài hơn 1,5 giây và các đoạn chờ.
- Nếu chữ trong demo nhỏ, dùng zoom/crop 120–150% vào vùng đang nói.
- Có thể thêm phụ đề tiếng Anh (Clipchamp: Auto-captions), không bắt buộc.
- Tổng độ dài mục tiêu **7:00–8:00**.

## 4. Xuất

- **MP4, H.264, 1920×1080 (1080p) trở lên**, 30 fps, audio AAC 48 kHz.
- Tên file: `StudentID_Name.mp4` (ví dụ `2101xxxx_NguyenVanA.mp4`). Đặt vào `Video/` trong thư mục nộp.

## 5. Checklist xem lại sau khi xuất

Xem lại **toàn bộ** file đã xuất (không phải bản trong phần mềm dựng):

- [ ] Mở được bằng trình phát mặc định trên một máy khác
- [ ] Độ phân giải 1920×1080 (chuột phải → Properties → Details)
- [ ] Có tiếng từ đầu đến cuối, không lệch tiếng, không rè
- [ ] Ở tốc độ 1×, kích thước cửa sổ bình thường: đọc được code, số trong terminal, trục biểu đồ
- [ ] Đủ 6 phần của đề (xem bảng ở `../README.md` mục 3)
- [ ] Nói rõ "My contribution …" và chỉ nhận đúng phần của mình
- [ ] Mọi con số khớp `02_SLIDE_SPEC.md`
- [ ] Không lộ thông tin cá nhân, mật khẩu, token trên màn hình
- [ ] Không còn đoạn chờ dài, đoạn nói hỏng
