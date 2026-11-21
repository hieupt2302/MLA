# Slide giới thiệu bài toán (dùng chung cho cả 3 video)

Cả 3 người dùng **cùng một slide 2** và gần như cùng một lời nói, khoảng 35 giây và khoảng 85 từ. Phần này không chấm theo cá nhân. Mục đích là để người chấm hiểu bài toán thật nhanh rồi chuyển sang phần của từng người.

## Nội dung slide (layout `bullets_image`)

- **Title:** The problem: which parts of an essay don't work?
- **Bullets:**
  - PERSUADE 2.0: 25,996 student essays, 237,966 discourse units
  - 7 unit types: Lead, Position, Claim, Counterclaim, Rebuttal, Evidence, Concluding Statement
  - Expert label per unit: Ineffective / Adequate / Effective
  - Only 4.5% Ineffective, so we report Macro-F1, not accuracy
  - Split by essay; official test (93,677 units) scored once
- **Image:** `../_chung/visuals/intro_label_mix.png`, thanh ngang 100% cho train / validation / test (% Ineffective, Adequate, Effective, lấy từ `E1_split_label_distribution.csv`).
- **Source:** Final report §3.4–3.6; table E1.

## Lời nói (tiếng Anh)

> Slide 2 xuất hiện.

Teachers who mark argumentative essays want to know *which parts* of an essay do not work, not only an overall score. Our group used the PERSUADE 2.0 corpus: almost twenty-six thousand student essays, split by expert raters into about two hundred and thirty-eight thousand discourse units, such as claims, evidence and rebuttals. Each unit is labelled Ineffective, Adequate or Effective. Only four and a half percent are Ineffective, so a model that always says "Adequate" is eighty percent accurate and useless. That is why we report Macro-F1, which weights the three classes equally.

## Số liệu và nguồn

| Số | Nguồn |
|---|---|
| 25,996 essays; 237,966 units | `E1_split_label_distribution.csv` (all annotated) |
| 4.49% Ineffective (nói "four and a half percent") | E1 |
| Majority baseline: accuracy 80.5% on test, Macro-F1 0.297 | `R2_test_per_class.csv`; Table 6.5 |
| Test 93,677 units, 10,402 essays | E1; R2 |
