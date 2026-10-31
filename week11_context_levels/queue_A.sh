#!/usr/bin/env bash
# Phiên A: chờ L1±2 (lượt 1, dự đoán bị xáo) kết thúc, lưu lại bản lỗi làm hồ sơ, rồi chạy L3 -> L2 -> L1±2 (bản đã sửa)
cd C:/Users/Admin/Desktop/MLA/week11_context_levels
until grep -q "HẾT" logs/ctxw2.log; do sleep 60; done
[ -f 08_L1w2_context_output.ipynb ] && mv 08_L1w2_context_output.ipynb 08_L1w2_context_run1_UNORDERED_PREDICTIONS_output.ipynb
[ -f results/results_L1w2.zip ] && mv results/results_L1w2.zip results/results_L1w2_run1_UNORDERED_PREDICTIONS.zip
./run_session.sh ctxl3 week11_context_levels/10_L3_whole_essay.ipynb week11_context_levels/09_L2_source_text.ipynb \
    week11_context_levels/08_L1w2_context.ipynb > logs/ctxl3.log 2>&1
