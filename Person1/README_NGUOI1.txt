WEEK 11 - NGUOI 1: Confound Do Dai x Diem Holistic & Nghiem Thu Random Forest Official Test
(cap nhat sau ra soat 31/10/2026 - xem RA_SOAT_TUAN11_SO_VOI_NHAN_XET_TUAN10.md, muc B1, B2)

!!! SO CU DA RUT LAI !!!
  Bang "phang 26%" (Diem 3: 26.59/25.32/26.48/26.48 ...) SAI: ban cu ghep du doan voi diem holistic qua
  discourse_id, ma cot nay bi Excel lam tron (144.289 don vi chi con 728 ID) -> moi don vi bi gan diem/do dai
  cua bai khac. RF 0.4834 / 67.79% cung KHONG phai RF Feature Set B.

1. Do dai x Diem holistic (Yeu cau bat buoc 3)
   - Script: script_holistic_length_table.py (+ .ipynb), ghep theo row_idx, co kiem tra.
     python Person1/script_holistic_length_table.py --train_csv <train.csv> --test_csv <test.csv>
   - Output: output/holistic_score_x_length_quartile_error_rates.csv (N, N bai, CI bootstrap theo bai),
             output/length_within_score_regression.csv, output/length_quartile_marginal_error_by_model.csv
   - Ket qua (DeBERTa L1 tuan 11, validation):
     + Diem 3: 19.3% -> 21.8% -> 22.9% -> 28.2%   (test: 17.6 -> 20.8 -> 22.3 -> 29.2)
     + Diem 4: 19.6% -> 22.0% -> 28.5% -> 31.1%
     + Hoi quy cum theo bai: OR moi bac do dai = 1.19 [1.14, 1.25] khi kiem soat diem;
       1.17 [1.11, 1.23] khi kiem soat them nhan gold + loai don vi.
     -> Trong cung muc diem, loi VAN TANG theo do dai. Gia thuyet A chua bi loai.
        Dich chuyen trinh do giai thich LOAI loi (Q4: 92% loi la nham Adequate<->Effective),
        khong giai thich het MUC loi tang.

2. Random Forest Feature Set B tren Official Test (93,677 don vi)
   - Script: run_rf_official_test.py (+ .ipynb) - dung y cau hinh tuan 9, train 115.187 don vi,
     chi cham test neu tai tao duoc Macro-F1 validation tuan 9. Dung scikit-learn==1.6.1.
   - Output: output/official_test_rf_actual_result.csv, output/test_predictions_rf_feature_set_b.csv,
             output/official_test_rf_run_metadata.json
   - Ket qua: validation 0.5261 (tuan 9: 0.5230) | TEST Macro-F1 0.5098, Accuracy 78.51%,
     F1 Ineffective 0.2024 | F1 Adequate 0.8701 | F1 Effective 0.4567
