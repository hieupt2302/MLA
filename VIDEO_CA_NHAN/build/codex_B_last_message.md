Đã tạo **3 PPTX (27 slide), 3 DOCX**, cùng 4 script trong `VIDEO_CA_NHAN/build/`. Không sửa Markdown, visuals, demo hay commit Git.

| Bộ | File | Bố cục |
|---|---|---|
| Người 1 | [PPTX](C:/Users/Admin/Desktop/MLA/VIDEO_CA_NHAN/Nguoi_1_Data_Classical_Length/output/Nguoi_1_slides.pptx) · [DOCX](C:/Users/Admin/Desktop/MLA/VIDEO_CA_NHAN/Nguoi_1_Data_Classical_Length/output/Nguoi_1_script.docx) | Trace RF, biểu đồ độ dài, demo nền navy |
| Người 2 | [PPTX](C:/Users/Admin/Desktop/MLA/VIDEO_CA_NHAN/Nguoi_2_DeBERTa_Context_Threshold/output/Nguoi_2_slides.pptx) · [DOCX](C:/Users/Admin/Desktop/MLA/VIDEO_CA_NHAN/Nguoi_2_DeBERTa_Context_Threshold/output/Nguoi_2_script.docx) | So sánh L0/L1, bảng editable, biểu đồ ngưỡng |
| Người 3 | [PPTX](C:/Users/Admin/Desktop/MLA/VIDEO_CA_NHAN/Nguoi_3_TestGovernance_LOPO_Ladder/output/Nguoi_3_slides.pptx) · [DOCX](C:/Users/Admin/Desktop/MLA/VIDEO_CA_NHAN/Nguoi_3_TestGovernance_LOPO_Ladder/output/Nguoi_3_script.docx) | Governance, context ladder, hai bảng LOPO editable |

Nội dung, notes, phần DEMO nối thêm và đoạn văn DOCX đã qua kiểm tra cấu trúc. Không còn hình thiếu.

`check_numbers.py` chạy thành công, exit **0**, đối chiếu 2.117 giá trị từ 61 file:

| Người | Khớp / tổng | Chưa xác minh |
|---|---:|---|
| 1 | 96/105 | 1.050; 57.633; 47.059; 309; 23,3% — gồm các lần lặp; 8 mục xuất hiện trong output demo |
| 2 | 143/146 | 1.050 và 76,5% — giá trị cũ đang được đính chính |
| 3 | 139/141 | 1.050 và 0,464 của lần LOPO cũ |

Chi tiết có trong `output/number_check.txt` của từng người.

**Chưa hoàn tất kiểm tra render Office:** PowerPoint/Word COM báo `0x80070520`, công cụ GUI cũng không kết nối được. Đã xem đủ 27 PNG dựng gần đúng trong `output/preview_fallback/`; chưa thể bảo đảm bố cục render thực tế của Office.