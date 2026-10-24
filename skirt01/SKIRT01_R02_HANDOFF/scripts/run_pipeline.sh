#!/usr/bin/env bash
# SKIRT01 — bake → verify_bake(게이트) → build → verify_scene(게이트) → anchors → 대표 스틸
# 사용: bash scripts/run_pipeline.sh [--verify-only] [--rebake]
set -euo pipefail
cd "$(dirname "$0")/.."
PY=env/bin/python
[ -x "$PY" ] || { echo "env 없음 → bash scripts/setup_env.sh"; exit 2; }
VERIFY_ONLY=0; REBAKE=0
for a in "$@"; do case $a in --verify-only) VERIFY_ONLY=1;; --rebake) REBAKE=1;; esac; done
mkdir -p evidence overlay render review
need(){ [ -f "$1" ] || { echo "[미작성] $1 — TASKS.json $2 참조"; exit 3; }; }
if [ $VERIFY_ONLY -eq 0 ]; then
  if [ $REBAKE -eq 1 ] || [ ! -f src/step_bake.npz ]; then
    need src/bake_steps.py T-14;  $PY -I src/bake_steps.py --config src/rig_config.json --out src/
  fi
fi
need src/verify_bake.py T-15;    $PY -I src/verify_bake.py --config src/rig_config.json --bake src/step_bake.npz --out evidence/bake_qc.json
$PY -I - <<'PYEOF'
import json,sys; q=json.load(open('evidence/bake_qc.json'))
bad=[k for k,v in q.get('PASS',{}).items() if v is not True]
print('G3', 'PASS' if not bad else 'FAIL '+str(bad)); sys.exit(1 if bad else 0)
PYEOF
if [ $VERIFY_ONLY -eq 0 ]; then
  need src/build_scene.py T-16;  $PY src/build_scene.py --config src/rig_config.json --bake src/ --keys camera_keys.json --out scene.blend
fi
need src/verify_scene.py T-17;   $PY src/verify_scene.py --blend scene.blend --config src/rig_config.json --step 5 --out evidence/scene_qc.json
$PY -I - <<'PYEOF'
import json,sys; q=json.load(open('evidence/scene_qc.json'))
n=q.get('collisions_count',None); print('G4', 'PASS' if n==0 else f'FAIL collisions={n}'); sys.exit(0 if n==0 else 1)
PYEOF
need src/export_anchors.py T-17; $PY src/export_anchors.py --blend scene.blend --out overlay/overlay_anchors.json
need src/render_frames.py T-16;  $PY src/render_frames.py --blend scene.blend --res 270 --spp 8 --frames 230,505,625,721 --out render/stills_270 --probe evidence/render_probe.json
echo "파이프라인 완료. 다음: render_frames.py --res 540 --spp 24 --frames 230,505,625,721 → verify_luma.py / verify_brush.py (T-18)"
