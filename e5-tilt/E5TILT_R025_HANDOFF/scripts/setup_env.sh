#!/usr/bin/env bash
# bpy module env for Linux / cloud (Blender LOCK 4.5 LTS -> Python 3.11 + bpy==4.5.14)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
python3.11 -m venv "$ROOT/.venv"
"$ROOT/.venv/bin/pip" install --upgrade pip
"$ROOT/.venv/bin/pip" install bpy==4.5.14 numpy==1.26.4 pillow
"$ROOT/.venv/bin/python" -c "import bpy; print('bpy', bpy.app.version_string)"
# optional, local only (cloud blocks huggingface): faster-whisper for VO_WORDS.json
# "$ROOT/.venv/bin/pip" install faster-whisper
