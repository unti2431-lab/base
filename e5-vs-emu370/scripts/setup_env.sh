#!/usr/bin/env bash
# Blender 미설치 환경용 bpy 모듈 설치 (Blender 4.5 LTS = Python 3.11)
set -euo pipefail
cd "$(dirname "$0")/.."
PY=${PY:-python3.11}
"$PY" -m venv env
env/bin/pip install --upgrade pip
env/bin/pip install "bpy==4.5.*" numpy
env/bin/python -c "import bpy, numpy; print('bpy', bpy.app.version, 'numpy', numpy.__version__)"
