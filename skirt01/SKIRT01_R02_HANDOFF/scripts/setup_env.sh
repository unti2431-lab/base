#!/usr/bin/env bash
# SKIRT01 — 클라우드 환경 bpy 설치 (LOCKS.md SPEC: Blender 4.5 LTS)
set -euo pipefail
python3.11 -m venv env
env/bin/pip install --upgrade pip
env/bin/pip install "bpy==4.5.14" numpy
echo "완료. Blender 버전 LOCK = 4.5. 편 진행 중 버전 변경 금지."
