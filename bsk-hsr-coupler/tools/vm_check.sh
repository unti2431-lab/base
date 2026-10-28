#!/usr/bin/env bash
# Cowork Linux VM self-check (no Blender, no GPU): re-bake both rigs and run the independent bake verifiers.
# Proves the numbers in rig_config.json still solve before asking the user / computer-use to run Windows Blender.
set -euo pipefail
cd "$(dirname "$0")/.."
VENV="${VENV:-$HOME/.bsk_venv}"
[[ -x "$VENV/bin/python" ]] || { python3 -m venv "$VENV"; "$VENV/bin/pip" install -q numpy shapely; }
PY="$VENV/bin/python"
OUT="logs/vm_check_$(date +%Y%m%d_%H%M%S).log"; mkdir -p logs
{
  $PY src/kin_schB.py >/dev/null && $PY src/verify_bake_schB.py | grep -E '"ALL_PASS"'
  $PY src/kin_shibataA.py >/dev/null && $PY src/verify_bake_shibataA.py | grep -E '"ALL_PASS"'
} 2>&1 | tee "$OUT"
grep -q false "$OUT" && { echo "VM_CHECK: FAIL (see $OUT)"; exit 1; } || echo "VM_CHECK: PASS (bake level; scene QC and render need Windows Blender)"
