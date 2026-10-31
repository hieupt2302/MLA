#!/usr/bin/env bash
# Chạy một hay nhiều notebook trên MỘT phiên Colab L4 qua colab CLI (Docker).
# Mỗi notebook: chạy thử QUICK=1 -> nếu không lỗi thì restart kernel và chạy thật QUICK=0 -> tải kết quả.
# Notebook đã chạy (kèm output) được ghi cạnh notebook gốc: <tên>_output.ipynb (bản thử: <tên>_QUICK_output.ipynb).
# Dùng: ./run_session.sh <session> <đường dẫn notebook tương đối từ repo>...
set -u
export MSYS_NO_PATHCONV=1
S=$1; shift
REPO=C:/Users/Admin/Desktop/MLA
R="docker run --rm -v mla-colab-auth:/root/.config/colab-cli -v $REPO:/workspace ati-colab-cli:0.7.4"
say() { echo "[$(date -u +%H:%M:%S)] [$S] $*"; }
retry() { for i in 1 2 3; do "$@" && return 0; sleep 20; done; return 1; }

has_error() { python -c "import json,sys; nb=json.load(open(sys.argv[1],encoding='utf-8')); sys.exit(0 if any(o.get('output_type')=='error' for c in nb['cells'] if c['cell_type']=='code' for o in c.get('outputs',[])) else 1)" "$1"; }

say "tạo phiên L4"
retry $R new -s $S --gpu L4 2>&1 | grep -E "READY|Error|rror" || { say "KHÔNG tạo được phiên"; exit 1; }
retry $R install -s $S "transformers==4.57.6" 2>&1 | tail -1
for f in week11_context_levels/upload/val_predictions_L1.csv week11_context_levels/upload/val_predictions_L0.csv \
         week11_context_levels/upload/source_texts.json; do
  retry $R upload -s $S /workspace/$f /content/$(basename $f) 2>&1 | tail -1
done

for NB in "$@"; do
  base=${NB%.ipynb}
  for MODE in 1 0; do
    $R restart-kernel -s $S 2>&1 | tail -1
    say "chạy $NB QUICK=$MODE"
    $R exec -s $S --timeout 86400 --env QUICK=$MODE -f /workspace/$NB > /dev/null 2>&1
    out=$REPO/${base}_output.ipynb
    if [ ! -f "$out" ]; then say "không thấy $out"; break 2; fi
    if [ $MODE = 1 ]; then mv "$out" "$REPO/${base}_QUICK_output.ipynb"; out=$REPO/${base}_QUICK_output.ipynb; fi
    if has_error "$out"; then say "LỖI trong $out — dừng"; break 2; fi
    say "xong $NB QUICK=$MODE"
  done
  key=$(python -c "import json,sys; nb=json.load(open(sys.argv[1],encoding='utf-8')); print([''.join(c['source']) for c in nb['cells'] if c['cell_type']=='code'][1].split('\"')[1])" "$REPO/$NB")
  mkdir -p "$REPO/$(dirname $NB)/results"
  retry $R download -s $S /content/results_$key.zip /workspace/$(dirname $NB)/results/results_$key.zip > /dev/null 2>&1 \
    && say "đã tải results_$key.zip" || say "KHÔNG tải được results_$key.zip"
done
$R stop -s $S 2>&1 | tail -1
say "HẾT"
