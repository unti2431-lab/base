#!/usr/bin/env bash
# PAVE 환경 셋업 (Linux/macOS, 클라우드 포함)
#   scripts/setup_env.sh --blender 4.5   -> python3.11 venv + bpy==4.5.14 + numpy
#   scripts/setup_env.sh --blender 5.2   -> python3.13 venv + bpy==5.2.2  + numpy
#   scripts/setup_env.sh --bake-only     -> numpy 만 (T02 베이크 재현용, bpy 불필요)
# --blender 값은 사용자 결정(G-PAVE-04)이다. 정하지 않았으면 --bake-only 로 시작한다.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MODE="${1:-}"; VER="${2:-}"
case "$MODE" in
  --blender)
    case "$VER" in
      4.5) PYBIN=python3.11; BPY=bpy==4.5.14 ;;
      5.2) PYBIN=python3.13; BPY=bpy==5.2.2 ;;
      *) echo "사용법: $0 --blender 4.5|5.2" >&2; exit 2 ;;
    esac ;;
  --bake-only) PYBIN=python3; BPY="" ;;
  *) echo "사용법: $0 --blender 4.5|5.2  또는  $0 --bake-only" >&2; exit 2 ;;
esac
command -v "$PYBIN" >/dev/null || { echo "$PYBIN 이 없습니다. 설치 후 다시 실행하세요." >&2; exit 3; }
"$PYBIN" -m venv "$ROOT/.venv"
"$ROOT/.venv/bin/python" -m pip install -q --upgrade pip
"$ROOT/.venv/bin/python" -m pip install -q "numpy>=1.26"
if [ -n "$BPY" ]; then
  "$ROOT/.venv/bin/python" -m pip install -q "$BPY"
  "$ROOT/.venv/bin/python" - "$ROOT/src/spec_lock.json" "$VER" <<'PY'
import json, sys, pathlib
p = pathlib.Path(sys.argv[1]); s = json.loads(p.read_text(encoding='utf-8'))
s['blender'] = sys.argv[2]; s['blender_status'] = 'LOCKED by setup_env.sh (사용자 결정 G-PAVE-04)'
p.write_text(json.dumps(s, indent=2, ensure_ascii=False), encoding='utf-8')
PY
fi
"$ROOT/.venv/bin/python" -c "import numpy; print('numpy', numpy.__version__)"
[ -n "$BPY" ] && "$ROOT/.venv/bin/python" -c "import bpy; print('bpy', bpy.app.version_string)" || true
echo "SETUP OK -> $ROOT/.venv"
