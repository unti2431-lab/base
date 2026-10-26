"""G4 gate - world-space triangle BVH collision check + camera clearance.

Every `--step` frames (default 5) over the full range:
  * pair overlaps from PAIRS (name globs); DESIGNED pairs are recorded, not failed
  * active camera nearest-surface distance >= --cam_min (default 0.15 m)
Writes ../evidence/scene_qc.json, exits 1 on FAIL.
python verify_scene.py -- [--blend ../work/e5tilt_R025_proxy.blend] [--step 5]
"""
import os, sys, json, fnmatch, argparse, time
import numpy as np
import bpy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import HERE, argv, world_bvh

ap = argparse.ArgumentParser()
ap.add_argument('--blend', default=os.path.join(HERE, '..', 'work', 'e5tilt_R025_proxy.blend'))
ap.add_argument('--step', type=int, default=5)
ap.add_argument('--cam_min', type=float, default=0.15)
ap.add_argument('--out', default=os.path.join(HERE, '..', 'evidence', 'scene_qc.json'))
ap.add_argument('--extra_pairs', default=None, help='json list of [globA, globB] (asset integration)')
A = ap.parse_args(argv())
if os.path.abspath(bpy.data.filepath or '') != os.path.abspath(A.blend):
    bpy.ops.wm.open_mainfile(filepath=os.path.abspath(A.blend))       # ops exception: open

HERO_PARTS = ['FRAME', 'AXLEBOX', 'COIL', 'MOTOR', 'YAWDAMP', 'SPRING_?_BASE', 'SPRING_?_BELLOWS',
              'AUXRES_?', 'LVALVE_?', 'LROD_?', 'WHEELSET_01_R_?']
PAIRS = []
for p in HERO_PARTS:
    for q in ('BODY_01', 'SKIRT_01_R_?', 'SPRING_?_TOP'):
        PAIRS.append((p, q))
for i, p in enumerate(HERO_PARTS):
    for q in HERO_PARTS[i + 1:]:
        PAIRS.append((p, q))
PAIRS += [('WHEELSET_*', 'RAIL_A_?'), ('GANGWAY_*_F', 'GANGWAY_*_R'), ('CUP', 'CABIN_TRAYS'), ('LIQUID', 'CUP'),
          ('BODY_??', 'WALL_L'), ('BODY_??', 'MAST_*'), ('SKIRT_*', 'WHEELSET_*'), ('SKIRT_*', 'RAIL_A_?'),
          ('ISO_SPRING_?_TOP', 'ISO_*'), ('ISO_AUXRES_?', 'ISO_*'), ('ISO_LVALVE_?', 'ISO_*'), ('ISO_LROD_?', 'ISO_*'),
          ('ISO_SPRING_?_BELLOWS', 'ISO_*')]
if A.extra_pairs:
    PAIRS += [tuple(x) for x in json.load(open(A.extra_pairs))]

# designed contacts (seated faces / shafts through housings) - logged, not failed
DESIGNED = [('WHEELSET_*', 'AXLEBOX'), ('WHEELSET_*', 'MOTOR'), ('SPRING_?_BELLOWS', 'SPRING_?_BASE'),
            ('ISO_SPRING_?_BELLOWS', 'ISO_SPRING_?_BASE'), ('ISO_WHEELSET_?', 'ISO_AXLEBOX'), ('ISO_WHEELSET_?', 'ISO_MOTOR'),
            ('ISO_GHOST_BODY', 'ISO_*'), ('CLOUD_DECK', '*')]
STATIC = {'RAIL_A_L', 'RAIL_A_R', 'WALL_L'} | {o.name for o in bpy.data.objects if o.name.startswith('MAST_')}

meshes = [o for o in bpy.data.objects if o.type == 'MESH' and not o.hide_render]
names = {o.name for o in meshes}


def expand(g):
    return sorted(n for n in names if fnmatch.fnmatchcase(n, g))


def side_ok(a, b):
    """same side letter for L/R families, adjacent-car rule for gangways"""
    if a == b:
        return False
    if a.startswith('GANGWAY') and b.startswith('GANGWAY'):
        return int(b.split('_')[1]) == int(a.split('_')[1]) + 1
    for x, y in ((a, b),):
        sa = [t for t in x.split('_') if t in ('L', 'R')]
        sb = [t for t in y.split('_') if t in ('L', 'R')]
    return True


def designed(a, b):
    return any((fnmatch.fnmatchcase(a, p) and fnmatch.fnmatchcase(b, q)) or (fnmatch.fnmatchcase(b, p) and fnmatch.fnmatchcase(a, q))
               for p, q in DESIGNED)


pairs = set()
for ga, gb in PAIRS:
    for a in expand(ga):
        for b in expand(gb):
            if side_ok(a, b) and a != b:
                pairs.add(tuple(sorted((a, b))))
# bodies vs masts: only cars near the mast matter; prefilter per frame by distance
pairs = sorted(pairs)
print('pairs', len(pairs))

SC = bpy.context.scene
frames = list(range(SC.frame_start, SC.frame_end + 1, A.step))
if frames[-1] != SC.frame_end:
    frames.append(SC.frame_end)
static_cache = {}
hits, contact = {}, {}
cam_min = {}
cam_check = [o for o in meshes if any(fnmatch.fnmatchcase(o.name, g) for g in
             ('BODY_0?', 'BODY_10', 'SKIRT_*', 'WALL_L', 'CABIN_*', 'CUP', 'FRAME', 'AXLEBOX', 'COIL', 'MOTOR', 'YAWDAMP',
              'SPRING_*', 'AUXRES_*', 'LVALVE_*', 'LROD_*', 'WHEELSET_01_R_?', 'ISO_*', 'GANGWAY_*'))
             and o.name not in ('ISO_GHOST_BODY',)]
t0 = time.time()
for f in frames:
    SC.frame_set(f)
    dg = bpy.context.evaluated_depsgraph_get()
    cache = {}

    def bvh(n):
        if n in STATIC:
            if n not in static_cache:
                static_cache[n] = world_bvh(bpy.data.objects[n], dg)
            return static_cache[n]
        if n not in cache:
            cache[n] = world_bvh(bpy.data.objects[n], dg)
        return cache[n]

    def near(a, b, r=40.0):
        pa = bpy.data.objects[a].matrix_world.translation; pb = bpy.data.objects[b].matrix_world.translation
        return (pa - pb).length < r or a in STATIC or b in STATIC

    for a, b in pairs:
        oa, ob = bpy.data.objects[a], bpy.data.objects[b]
        if not (a in STATIC or b in STATIC) and (oa.matrix_world.translation - ob.matrix_world.translation).length > 60:
            continue
        if (a in STATIC) ^ (b in STATIC):
            dyn = ob if a in STATIC else oa
            st = a if a in STATIC else b
            if st.startswith('MAST_') and (dyn.matrix_world.translation - bpy.data.objects[st].matrix_world.translation).length > 40:
                continue
        n = len(bvh(a).overlap(bvh(b)))
        if n:
            d = contact if designed(a, b) else hits
            d.setdefault(f'{a}|{b}', []).append([f, n])
    # camera clearance
    cam = None
    for m in sorted(SC.timeline_markers, key=lambda m: m.frame):
        if m.frame <= f and m.camera:
            cam = m.camera
    cp = cam.matrix_world.translation
    best = 1e9
    for o in cam_check:
        if (o.matrix_world.translation - cp).length > 40 and o.name not in STATIC:
            continue
        r = bvh(o.name).find_nearest(cp)
        if r[0] is not None:
            best = min(best, r[3])
    sid = cam.name.replace('CAM_', '')
    cam_min[sid] = min(cam_min.get(sid, 1e9), best)
    if f % 100 == 1:
        print(f'F{f} {time.time() - t0:.0f}s hits={sum(len(v) for v in hits.values())}', flush=True)

ok_coll = len(hits) == 0
ok_cam = all(v >= A.cam_min for v in cam_min.values())
res = {
    'gate': 'G4', 'result': 'PASS' if ok_coll and ok_cam else 'FAIL',
    'PASS': {'collisions': 'PASS' if ok_coll else 'FAIL', 'camera_clearance': 'PASS' if ok_cam else 'FAIL'},
    'frames_checked': len(frames), 'step': A.step, 'pairs_checked': len(pairs),
    'collisions': {k: {'frames': len(v), 'first': v[0], 'max_tris': max(x[1] for x in v)} for k, v in hits.items()},
    'designed_contacts': {k: {'frames': len(v), 'first': v[0]} for k, v in contact.items()},
    'camera_min_clearance_m': {k: round(v, 3) for k, v in cam_min.items()},
    'camera_min_rule_m': A.cam_min,
}
os.makedirs(os.path.dirname(A.out), exist_ok=True)
json.dump(res, open(A.out, 'w'), indent=2)
print(json.dumps({k: res[k] for k in ('result', 'PASS', 'collisions', 'camera_min_clearance_m')}, indent=1))
sys.exit(0 if res['result'] == 'PASS' else 1)
