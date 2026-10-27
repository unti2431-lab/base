#!/usr/bin/env bash
# 저장소의 pave/ 에서 PAVE_R01_HANDOFF.zip 을 만든다.
#   scripts/make_handoff.sh <출력 폴더>
# 1) 깨끗한 사본 구성 2) 베이크 기준값(EXPECTED) 생성 3) MANIFEST.json 4) zip 5) 별도 폴더에 풀어 재현 검사
set -euo pipefail
PAVE="$(cd "$(dirname "$0")/.." && pwd)"; REPO="$(cd "$PAVE/.." && pwd)"
OUT="$(mkdir -p "${1:?출력 폴더}" && cd "$1" && pwd)"; NAME=PAVE_R01_HANDOFF
STAGE="$OUT/stage"; rm -rf "$STAGE"; mkdir -p "$STAGE/$NAME"
PKG="$STAGE/$NAME"
( cd "$PAVE" && git ls-files --cached --others --exclude-standard ) | while read -r f; do
  mkdir -p "$PKG/$(dirname "$f")"; cp "$PAVE/$f" "$PKG/$f"; done
cp "$REPO/heavy-mech-series/RANKING_v2.md" "$PKG/reference/RANKING_v2.md"
mkdir -p "$PKG/evidence"
python3 "$PKG/src/pave_kin.py" > /dev/null
cp "$PKG/src/bake/bake_qc.json" "$PKG/evidence/EXPECTED_bake_qc.json"
rm -rf "$PKG/src/bake" "$PKG/src/__pycache__"
python3 - "$PKG" <<'PY'
import hashlib, json, pathlib, sys
root = pathlib.Path(sys.argv[1]); files = []
for p in sorted(root.rglob('*')):
    if p.is_file() and p.name != 'MANIFEST.json':
        files.append({'path': p.relative_to(root).as_posix(), 'bytes': p.stat().st_size,
                      'sha256': hashlib.sha256(p.read_bytes()).hexdigest()})
(root / 'MANIFEST.json').write_text(json.dumps({'package': root.name, 'files': files}, indent=2, ensure_ascii=False))
print('manifest files:', len(files))
PY
rm -f "$OUT/$NAME.zip"; ( cd "$STAGE" && zip -qr -X "$OUT/$NAME.zip" "$NAME" )
# 재현 검사: 새 폴더에 풀어 베이크 게이트를 다시 돌리고 기준값과 수치 비교
CHK="$OUT/verify"; rm -rf "$CHK"; mkdir -p "$CHK"; ( cd "$CHK" && unzip -q "$OUT/$NAME.zip" )
bash "$CHK/$NAME/scripts/run_pipeline.sh" --bake-only
python3 - "$CHK/$NAME" <<'PY'
import json, pathlib, sys
r = pathlib.Path(sys.argv[1])
a = json.loads((r / 'evidence/bake_qc.json').read_text()); b = json.loads((r / 'evidence/EXPECTED_bake_qc.json').read_text())
assert a == b, 'bake_qc 가 기준값과 다름'
print('REPRO PASS: bake_qc == EXPECTED, ALL_PASS =', a['ALL_PASS'])
PY
rm -rf "$STAGE"
echo "ZIP -> $OUT/$NAME.zip"
