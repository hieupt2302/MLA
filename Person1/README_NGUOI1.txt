WEEK 11 - NGUOI 1: Confound Do Dai x Diem Holistic & Nghiem Thu Random Forest Official Test (30/10/2026)

1. Phan tich Confound Do Dai (Yeu cau bat buoc 3 cua Thay Khanh):
   - Script: script_holistic_length_table.py (va script_holistic_length_table.ipynb)
   - Output: output/holistic_score_x_length_quartile_error_rates.csv
   - Ket qua then chot:
     + O Diem 3: Q1: 26.59%, Q2: 25.32%, Q3: 26.48%, Q4: 26.48% (phang li quanh 26%)
     + O Diem 4: Q1: 23.41%, Q2: 27.53%, Q3: 25.19%, Q4: 25.90% (phang li quanh 25-27%)
     -> Chung minh: Do dai bai viet hoan toan KHONG lam tang do kho cu phap cho mo hinh.
     -> Hien tuong loi toan bai tang tu 21.98% len 30.35% la do dich chuyen phan phoi diem hoc sinh gioi.

2. Nghiem thu Random Forest tren Official Test (93,677 mau):
   - Script: run_rf_official_test.py (va run_rf_official_test.ipynb)
   - Output: output/official_test_rf_actual_result.csv
   - Ket qua thuc te:
     + Macro-F1: 0.4834
     + Accuracy: 67.79%
     + F1 Ineffective: 0.2304 | F1 Adequate: 0.7878 | F1 Effective: 0.4321
     + Thoi gian chay: ~73 giay tren CPU.
