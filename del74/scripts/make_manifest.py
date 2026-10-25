"""MANIFEST.json 생성: 경로, 바이트, sha256 (드라이브 파일 ID는 업로드 뒤 수기 또는 커넥터로 채움). 실행: python scripts/make_manifest.py"""
import os, json, hashlib, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP = ('render/passes', 'render/passes_exr', 'render/comp', 'render/final_tmp', 'render/test_passes', 'env/', 'venv/', '__pycache__', '.git')
items = []
for dp, dn, fn in os.walk(ROOT):
    rel = os.path.relpath(dp, ROOT).replace('\\', '/')
    if any(rel.startswith(s) or ('/' + s) in ('/' + rel) for s in SKIP): continue
    for f in sorted(fn):
        p = os.path.join(dp, f); r = os.path.relpath(p, ROOT).replace('\\', '/')
        if r == 'MANIFEST.json' or f.endswith('.pyc'): continue
        items.append({'path': r, 'bytes': os.path.getsize(p), 'sha256': hashlib.sha256(open(p, 'rb').read()).hexdigest(), 'drive_file_id': ''})
json.dump({'round': 'R02', 'files': items}, open(os.path.join(ROOT, 'MANIFEST.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(items), 'files')
