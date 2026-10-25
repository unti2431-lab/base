#!/usr/bin/env bash
# 사용: bash Run_Dual_Look_Mac_Linux.sh video.mp4 [더 많은 입력/옵션...]
#   비교만:   bash Run_Dual_Look_Mac_Linux.sh --compare video.mp4
#   프리뷰만: bash Run_Dual_Look_Mac_Linux.sh --preview video.mp4
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ "$#" -eq 0 ]; then
  echo "Usage: bash Run_Dual_Look_Mac_Linux.sh [--compare|--preview] video.mp4 [more inputs...]" >&2
  exit 1
fi
case "$1" in
  --compare) shift; exec python3 "$ROOT/scripts/compare.py" --at 1.0 --video 2 "$@" ;;
  --preview) shift; exec python3 "$ROOT/scripts/apply.py" --mode both --encoder auto --preview-seconds 2 "$@" ;;
  *)         exec python3 "$ROOT/scripts/apply.py" --mode both --encoder auto "$@" ;;
esac
