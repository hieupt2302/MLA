WEEK 11 - NGUOI 3: DeBERTa L0 / L1 / Prompt-Aware + Official Test (cham 1 lan, 29/10/2026)

Bang chinh: outputs/official_test_final_summary.csv (5 he thong, so that)
  SVM 0.4822 | RF 0.5098 | L0 0.5613 | L1 0.5772 | PA 0.5808 (Macro-F1, 93.677 cau test)
  (RF 0.4834 truoc day KHONG phai Feature Set B -> da cham lai dung FSB, xem Person1/README_NGUOI1.txt)
  Bang 5 he thong cap nhat: <repo>/outputs/official_test_final_summary.csv (script_official_test_evaluation.py)
Bootstrap theo bai (test): outputs/official_test_deberta_bootstrap.csv
  L1-L0 +0.0159 [0.0115, 0.0207] | PA-L1 +0.0036 [-0.0002, 0.0074] (chua phan biet duoc)
Validation cung lan chay: outputs/week11_person3/validation_L0_L1_PA.csv (+ bootstrap)
Du doan tung don vi: outputs/week11_person3/{val,test}_predictions_{L0,L1,PA}.csv
Khoa test: outputs/week11_person3/OFFICIAL_TEST_LOCK.json | Log: run_log.txt | Moi truong: run_metadata.json
Notebook da chay (co output): week11_person3_full/07_person3_prompt_aware_official_test_output.ipynb
  (07_run1_... = lan chay dau, phien Colab bi thu hoi truoc khi cham test; chi co validation)

Luu y:
- L0/L1 duoc TRAIN LAI (checkpoint cu khong con / ban L1 Colab bi NaN), cung cong thuc tuan 9-10.
- Phai dung transformers 4.x (4.57.6); transformers 5.x lam DeBERTa-v3 train hong (NaN / doan 1 lop).
- A100 + bf16, lr 2e-5, batch 8 x grad_accum 4, 3 epoch, seed 42, split outputs/split_assignments.csv.
- Checkpoint (~2.2 GB) KHONG nam trong zip; xin rieng neu can.
- Tai lap bang 5 he thong: dat cac CSV vao outputs/ roi chay  python script_official_test_evaluation.py
