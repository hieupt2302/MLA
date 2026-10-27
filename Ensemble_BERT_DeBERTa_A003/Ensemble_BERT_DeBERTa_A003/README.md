# Gói nộp Ensemble BERT và DeBERTa

Đọc BAO_CAO.html (mở bằng trình duyệt, có thể in) hoặc BAO_CAO.md; mở notebooks/kernel_output.ipynb để xem output thực tế. Thư mục code chứa source snapshot và config của A003. results chứa prediction, metric, calibration, plots và phân tích lỗi gốc; evidence chứa manifest và kiểm chứng.

Tính lại: `pip install numpy pandas scikit-learn` rồi `python verify_results.py` trong thư mục gói đã giải nén. Script không train hay gọi GPU.

Gói nộp giữ output/code/predictions nhưng không chép ~1,2GB model snapshots để tránh làm gói báo cáo quá lớn. Archive gốc đầy đủ trọng số vẫn ở D:/MLA_MIDTERM/task_model_run/runs/V005_N1_N2_CPU_A003/artifacts.zip. Chạy lại training/inference từ văn bản cần dữ liệu, Colab và hai model theo đường dẫn remote trong config; notebook input gốc được giữ nguyên, không cam kết chạy trên máy local bằng một click.

Ngày chạy thật 05/10/2026. Kỳ tuần nộp do nhóm điền trong báo cáo tổng hợp; không backdate notebook. Chỉ validation; không có test score trong gói.
