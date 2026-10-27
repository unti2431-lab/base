#!/usr/bin/env bash
# Pipeline per test: bake -> verify_bake (gate) -> build -> verify_scene (gate) -> optional render + encode
# usage: src/run_pipeline.sh PYTHON_WITH_BPY {A|B|all} [--render]
set -euo pipefail
cd "$(dirname "$0")/.."
PY="$1"; WHICH="${2:-all}"; RENDER="${3:-}"
run_test () {   # $1 = tag (schB|shibA), $2 = kin, $3 = verify_bake, $4 = build, $5 = verify_scene, $6 = frames, $7 = label
  $PY "src/$2"; $PY "src/$3"; $PY "src/$4"; $PY "src/$5"
  if [[ "$RENDER" == "--render" ]]; then
    $PY "src/$4" --render 1 "$6" --preset animatic --out "render/$1_animatic"
    src/encode_preview.sh "render/$1_animatic" "review/$1_animatic_270p_CONCEPT.mp4" "$7"
  fi
}
[[ "$WHICH" == "B" || "$WHICH" == "all" ]] && run_test schB  kin_schB.py     verify_bake_schB.py     build_schB.py     verify_scene_schB.py     180 "CONCEPT_ONLY TEST B"
[[ "$WHICH" == "A" || "$WHICH" == "all" ]] && run_test shibA kin_shibataA.py verify_bake_shibataA.py build_shibataA.py verify_scene_shibataA.py 200 "CONCEPT_ONLY TEST A"
echo "pipeline done: $WHICH"
