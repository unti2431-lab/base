#!/usr/bin/env bash
# bpy module install (version LOCK 4.5). On a cut-off download pip reports a hash mismatch: re-run, it is a transfer error.
set -euo pipefail
ENV="${1:-$HOME/bpyenv}"
python3.11 -m venv "$ENV"
"$ENV/bin/pip" install --no-cache-dir "bpy==4.5.14" numpy shapely
"$ENV/bin/python" -c "import bpy, shapely; print('bpy', bpy.app.version_string, 'shapely', shapely.__version__)"
