#!/usr/bin/env bash
# bake → verify_bake(게이트) → build → (import) → verify_scene(게이트) → proportion(게이트) → 프리뷰
# 사용: bash scripts/run_pipeline.sh [--preview] [--asset-map assets/asset_map.json]
set -euo pipefail
cd "$(dirname "$0")/.."
PY=env/bin/python
PREVIEW=0; ASSET_MAP=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --preview) PREVIEW=1 ;;
    --asset-map) ASSET_MAP="$2"; shift ;;
    *) echo "unknown arg $1"; exit 2 ;;
  esac; shift
done
mkdir -p evidence build preview
python3 tools/check_beats.py --json evidence/beats_check.json          # G01
$PY src/bake.py                                                        # → src/motion_bake.npz
$PY src/verify_bake.py --json evidence/verify_bake.json                # G02
$PY src/build_scene.py --out build/e5_emu370.blend ${ASSET_MAP:+--asset-map "$ASSET_MAP"}
$PY src/verify_scene.py build/e5_emu370.blend --json evidence/verify_scene.json        # G03
$PY src/verify_proportion.py build/e5_emu370.blend --json evidence/proportion.json     # G05
if [[ $PREVIEW == 1 ]]; then
  $PY src/render_preview.py build/e5_emu370.blend --tier animatic --out preview/       # G04 자료
fi
md5sum src/motion_bake.npz | tee evidence/bake_md5.txt
