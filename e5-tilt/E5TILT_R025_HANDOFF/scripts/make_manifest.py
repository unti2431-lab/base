"""MANIFEST.json: path, bytes, sha256 for every package file (work/ frames excluded). drive_file_id is filled after upload."""
import os, json, hashlib
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {'.venv', '__pycache__', '.git'}
SKIP_PREFIX = ('work/frames_', 'work/dbg', 'work/stills')
items = []
for d, dirs, files in os.walk(ROOT):
    dirs[:] = sorted(x for x in dirs if x not in SKIP_DIRS)
    for f in sorted(files):
        p = os.path.join(d, f); rel = os.path.relpath(p, ROOT).replace(os.sep, '/')
        if rel == 'MANIFEST.json' or rel.startswith(SKIP_PREFIX) or rel.endswith('.blend1'):
            continue
        h = hashlib.sha256(open(p, 'rb').read()).hexdigest()
        items.append({'path': rel, 'bytes': os.path.getsize(p), 'sha256': h, 'drive_file_id': ''})
json.dump({'package': 'E5TILT_R025_HANDOFF', 'files': items}, open(os.path.join(ROOT, 'MANIFEST.json'), 'w'), indent=1)
print(len(items), 'files')
