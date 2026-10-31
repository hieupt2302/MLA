#!/usr/bin/env bash
# Phiên A (ctxl3): sau khi L2 lượt 2 kết thúc -> cứu L2 nếu cần -> L1±2 -> L1-para. Phiên B (ctxl3b): sau L3 7 epoch -> LOPO.
cd C:/Users/Admin/Desktop/MLA/week11_context_levels
(
  until grep -q "HẾT" logs/ctxl3.log; do sleep 60; done
  if grep -q "đã tải results_L2.zip" logs/ctxl3.log; then ITEMS=""; else ITEMS="norestart:week11_context_levels/09r_L2_recover_from_best_checkpoint.ipynb"; fi
  grep -q "đã tải results_L1w2.zip" logs/ctxl3.log || ITEMS="$ITEMS week11_context_levels/08_L1w2_context.ipynb"
  ./run_session_reuse.sh ctxl3 $ITEMS week11_context_levels/12_L1para_paragraph_context.ipynb > logs/ctxA2.log 2>&1
) &
(
  until grep -q "HẾT" logs/ctxl3b.log; do sleep 60; done
  ./run_session_reuse.sh ctxl3b week11_lopo_rerun/11_lopo_rerun_L0.ipynb > logs/ctxB2.log 2>&1
) &
wait
