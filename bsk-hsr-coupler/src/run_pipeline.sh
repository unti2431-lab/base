#!/usr/bin/env bash
# TEST B pipeline: bake -> verify_bake (gate) -> build -> verify_scene (gate) -> optional render
# usage: src/run_pipeline.sh [PYTHON_WITH_BPY] [--render]
set -euo pipefail
cd "$(dirname "$0")/.."
PY="${1:-python3}"; shift || true
$PY src/kin_schB.py
$PY src/verify_bake_schB.py       # exits 1 on FAIL -> pipeline stops
$PY src/build_schB.py
$PY src/verify_scene_schB.py      # exits 1 on overlap -> pipeline stops
if [[ "${1:-}" == "--render" ]]; then
  $PY src/build_schB.py --render 1 180 --preset animatic --out render/schB_animatic
  src/encode_preview.sh render/schB_animatic review/schB_animatic_270p_CONCEPT.mp4 "CONCEPT_ONLY - TEST B Scharfenberg-family rig - geometry not verified"
fi
