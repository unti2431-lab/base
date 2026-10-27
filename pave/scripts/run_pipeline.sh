#!/usr/bin/env bash
# PAVE 파이프라인 (Linux/macOS)
#   scripts/run_pipeline.sh              bake -> verify_bake(게이트) -> build_* -> verify_scene(게이트)
#   scripts/run_pipeline.sh --bake-only  베이크와 베이크 게이트만
#   scripts/run_pipeline.sh --check-bpy  bpy 버전 가드만 확인
# 아직 없는 단계(src/build_*.py 등)는 NOT_PERFORMED 로 기록하고 건너뛴다.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PY="${PY:-$ROOT/.venv/bin/python}"; [ -x "$PY" ] || PY=python3
EVD="$ROOT/evidence"; mkdir -p "$EVD"
STATUS="$EVD/pipeline_status.txt"; : > "$STATUS"
log() { echo "$1" | tee -a "$STATUS"; }

if [ "${1:-}" = "--check-bpy" ]; then
  "$PY" -c "import sys; sys.path.insert(0, '$ROOT/src'); import common_bpy as c; print('BPY GUARD PASS', c.bpy.app.version_string, 'LOCK', c.LOCK)"
  exit 0
fi

# 1) 베이크 + 베이크 게이트 (pave_kin.py 는 ALL_PASS 가 아니면 exit 1)
if "$PY" "$ROOT/src/pave_kin.py" > "$EVD/bake_qc_stdout.json"; then
  cp "$ROOT/src/bake/bake_qc.json" "$EVD/bake_qc.json"
  ( cd "$ROOT/src/bake" && sha256sum * ) > "$EVD/bake_sha256.txt"
  log "G3 bake: PASS"
else
  cp "$ROOT/src/bake/bake_qc.json" "$EVD/bake_qc.json" 2>/dev/null || true
  log "G3 bake: FAIL (evidence/bake_qc.json 확인)"; exit 1
fi
[ "${1:-}" = "--bake-only" ] && exit 0

# 2) 씬 빌드 단계 (T04-T08 산출물). bpy 모듈로 실행.
for st in build_auger build_internals build_head build_stones build_cameras; do
  if [ -f "$ROOT/src/$st.py" ]; then "$PY" "$ROOT/src/$st.py" && log "$st: DONE" || { log "$st: FAIL"; exit 1; }
  else log "$st: NOT_PERFORMED (src/$st.py 없음)"; fi
done
# 3) 씬 게이트 (T09)
if [ -f "$ROOT/src/verify_scene.py" ]; then "$PY" "$ROOT/src/verify_scene.py" && log "G4 scene: PASS" || { log "G4 scene: FAIL"; exit 1; }
else log "G4 scene: NOT_PERFORMED (src/verify_scene.py 없음)"; fi
