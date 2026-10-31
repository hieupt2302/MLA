#!/usr/bin/env bash
# Như run_session.sh nhưng DÙNG LẠI phiên Colab đang mở (không tạo mới, không cài lại). Tắt phiên ở cuối.
# Mục "norestart:<nb>" = chạy một lần QUICK=0 trong kernel hiện tại (không restart, không chạy thử) — dùng cho notebook cứu.
set -u
export MSYS_NO_PATHCONV=1
S=$1; shift
REPO=C:/Users/Admin/Desktop/MLA
R="docker run --rm -v mla-colab-auth:/root/.config/colab-cli -v $REPO:/workspace ati-colab-cli:0.7.4"
say() { echo "[$(date -u +%H:%M:%S)] [$S] $*"; }
retry() { for i in 1 2 3; do "$@" && return 0; sleep 20; done; return 1; }
has_error() { python -c "import json,sys; nb=json.load(open(sys.argv[1],encoding='utf-8')); sys.exit(0 if any(o.get('output_type')=='error' for c in nb['cells'] if c['cell_type']=='code' for o in c.get('outputs',[])) else 1)" "$1"; }
keyof() { python -c "import json,sys; nb=json.load(open(sys.argv[1],encoding='utf-8')); src=[''.join(c['source']) for c in nb['cells'] if c['cell_type']=='code']; k=[s for s in src if s.startswith('KEY = ')]; print(k[0].split('\"')[1] if k else sys.argv[2])" "$1" "$2"; }

for ITEM in "$@"; do
  if [[ $ITEM == norestart:* ]]; then NB=${ITEM#norestart:}; MODES="0"; RESTART=0; else NB=$ITEM; MODES="1 0"; RESTART=1; fi
  base=${NB%.ipynb}
  for MODE in $MODES; do
    [ $RESTART = 1 ] && $R restart-kernel -s $S 2>&1 | tail -1
    say "chạy $NB QUICK=$MODE"
    $R exec -s $S --timeout 86400 --env QUICK=$MODE -f /workspace/$NB > /dev/null 2>&1
    out=$REPO/${base}_output.ipynb
    if [ ! -f "$out" ]; then say "không thấy $out"; break 2; fi
    if [ $MODE = 1 ]; then mv "$out" "$REPO/${base}_QUICK_output.ipynb"; out=$REPO/${base}_QUICK_output.ipynb; fi
    if has_error "$out"; then say "LỖI trong $out — dừng"; break 2; fi
    say "xong $NB QUICK=$MODE"
  done
  key=$(keyof "$REPO/$NB" L2)
  mkdir -p "$REPO/$(dirname $NB)/results"
  retry $R download -s $S /content/results_$key.zip /workspace/$(dirname $NB)/results/results_$key.zip > /dev/null 2>&1 \
    && say "đã tải results_$key.zip" || say "KHÔNG tải được results_$key.zip"
done
$R stop -s $S 2>&1 | tail -1
say "HẾT"
