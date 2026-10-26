#!/usr/bin/env bash
# Linux / cloud pipeline: bake -> G3 -> build -> G4 -> (render stage) -> comp -> encode -> QC
# usage: scripts/run_pipeline.sh [verify|animatic|still|key4s|preview] [start] [end]
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"; cd "$ROOT/src"
PY="${PY:-$ROOT/.venv/bin/python}"        # python3.11 venv with bpy==4.5.14 numpy pillow (scripts/setup_env.sh)
STAGE="${1:-verify}"; START="${2:-1}"; END="${3:-803}"
"$PY" kin.py
"$PY" verify_bake.py                       # G3 gate (exit 1 stops the script)
"$PY" build.py
"$PY" verify_scene.py -- --step 5          # G4 gate
"$PY" sfx_cues.py
"$PY" sync_qc.py
[ "$STAGE" = "verify" ] && { echo "VERIFY DONE"; exit 0; }
OUT="$ROOT/work/frames_$STAGE"
"$PY" render_frames.py -- --stage "$STAGE" --start "$START" --end "$END" --outdir "$OUT"
"$PY" comp_overlays.py --frames "$OUT" --out "${OUT}_comp"
"$ROOT/scripts/encode.sh" "${OUT}_comp" "$ROOT/review/R025/e5tilt_R025_${STAGE}.mp4" "$START"
"$PY" sync_qc.py --video "$ROOT/review/R025/e5tilt_R025_${STAGE}.mp4"
echo "PIPELINE DONE"
