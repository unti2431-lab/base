#!/usr/bin/env bash
# DEL74 환경: Python 3.11 venv + bpy 4.5.14(LOCK) + numpy + pillow. Blender 본체가 없는 클라우드/리눅스용.
set -euo pipefail
cd "$(dirname "$0")/.."
python3.11 -m venv env
env/bin/pip install -q --upgrade pip
env/bin/pip install -q "bpy==4.5.14" numpy pillow
env/bin/python -c "import bpy; v=bpy.app.version; assert v[:2]==(4,5), v; print('bpy', bpy.app.version_string, 'OK')"
