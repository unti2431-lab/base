#!/usr/bin/env bash
# bake → verify_bake(게이트) → build → (import_assets) → verify_scene(게이트) → 270p 스틸. 클라우드/리눅스(CPU).
set -euo pipefail
cd "$(dirname "$0")/.."
PY=${PY:-env/bin/python}
STEP=${STEP:-10}
$PY src/bake.py > /dev/null
$PY src/verify_bake.py || { echo "G3 FAIL"; exit 1; }
$PY src/build_scene.py -- --out render/del74_scene.blend
SCENE=render/del74_scene.blend
if [ "${ASSETS:-0}" = "1" ]; then
  $PY -c "import bpy,sys; bpy.ops.wm.open_mainfile(filepath='$SCENE'); sys.argv=['x','--','--map','assets/asset_map.json','--out','render/del74_scene_assets.blend']; exec(open('src/import_assets.py').read())"
  SCENE=render/del74_scene_assets.blend
fi
$PY -c "import bpy,sys; bpy.ops.wm.open_mainfile(filepath='$SCENE'); sys.argv=['x','--','--step','$STEP']; exec(open('src/verify_scene.py').read())" || { echo "G4 FAIL (evidence/scene_qc.json)"; exit 1; }
$PY src/render_still.py -- --blend $SCENE --frames ${FRAMES:-1,150,318,426,505,745,894,1100} --pct 25 --spp 8 --out review/R02/stills_270p
echo "PIPELINE OK"
