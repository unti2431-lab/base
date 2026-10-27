#!/usr/bin/env python3
"""TEST A scene collision check (world-space triangle BVH, bpy 4.5). Reads evidence/TEST_A_SHIB.blend.
Pairs: partner-crossing parts only (same-head parts are rigidly assembled, cone/funnel of the same head never meet).
Every 5th frame + all frames in [E-10, E+10] around JP_LOCKED. Design contacts (<= 1 mm) are listed, not failed.
"""
import os, json, sys, math
import numpy as np
import bpy
from mathutils.bvhtree import BVHTree

LOCK = (4, 5); assert bpy.app.version[:2] == LOCK
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
bpy.ops.wm.open_mainfile(filepath=os.path.join(ROOT, "evidence", "TEST_A_SHIB.blend"))   # bpy.ops allowed: file open
sc = bpy.context.scene; dg = bpy.context.evaluated_depsgraph_get()
EV = json.load(open(os.path.join(ROOT, "evidence", "shibA_events.json"))); E = EV["JP_LOCKED"]["local_F"]
N = sc.frame_end

def world_bvh(ob, dg):
    eo = ob.evaluated_get(dg); me = eo.to_mesh(); me.calc_loop_triangles()
    v = np.empty(len(me.vertices) * 3); me.vertices.foreach_get('co', v); v = v.reshape(-1, 3)
    M = np.array(eo.matrix_world); w = v @ M[:3, :3].T + M[:3, 3]
    t = np.empty(len(me.loop_triangles) * 3, dtype=np.int32); me.loop_triangles.foreach_get('vertices', t)
    tree = BVHTree.FromPolygons(w.tolist(), t.reshape(-1, 3).tolist()); eo.to_mesh_clear(); return tree

PAIRS = [("LOCK_A", "KNUCKLE_B"), ("LOCK_B", "KNUCKLE_A"), ("LOCK_A", "LOCK_B"), ("LOCK_A", "KNUCKLE_A"), ("LOCK_B", "KNUCKLE_B"),
         ("KNUCKLE_A", "KNUCKLE_B"), ("KNUCKLE_A", "HFLOOR_B"), ("KNUCKLE_B", "HFLOOR_A"), ("LOCK_A", "MAINPIN_B"), ("KNUCKLE_A", "MAINPIN_B"), ("KNUCKLE_B", "MAINPIN_A")]
FACES = [o.name for o in bpy.data.objects if o.name.startswith("FACE")]
PAIRS += [(a, b) for a in FACES if a.endswith("_A") for b in FACES if b.endswith("_B")]
PAIRS += [(l, f) for l in ("LOCK_A", "KNUCKLE_A") for f in FACES if f.endswith("_B")] + [(l, f) for l in ("LOCK_B", "KNUCKLE_B") for f in FACES if f.endswith("_A")]
frames = sorted(set(list(range(1, N + 1, 5)) + list(range(max(1, E - 10), min(N, E + 10) + 1))))
hits = {}; checked = 0
for f in frames:
    sc.frame_set(f); dg = bpy.context.evaluated_depsgraph_get(); trees = {}
    for a, b in PAIRS:
        oa, ob_ = bpy.data.objects.get(a), bpy.data.objects.get(b)
        if oa is None or ob_ is None or oa.hide_render or ob_.hide_render: continue
        for o in (oa, ob_):
            if o.name not in trees: trees[o.name] = world_bvh(o, dg)
        ov = trees[a].overlap(trees[b]); checked += 1
        if ov: hits.setdefault(f"{a}|{b}", []).append((f, len(ov)))
# camera nearest-surface distance (skill: >= 0.15 m)
cam = sc.camera; min_cam = 1e9
for f in (1, E, N):
    sc.frame_set(f); dg = bpy.context.evaluated_depsgraph_get(); cp = cam.matrix_world.translation
    for o in sc.objects:
        if o.type != 'MESH' or o.hide_render: continue
        loc, nrm, idx, dist = world_bvh(o, dg).find_nearest(cp)
        if dist is not None: min_cam = min(min_cam, dist)
out = {"frames_checked": frames, "pair_checks": checked, "overlapping_pairs": {k: v for k, v in hits.items()},
       "camera_min_surface_distance_m": float(min_cam),
       "PASS": {"no_overlap": len(hits) == 0, "camera_clearance": min_cam >= 0.15}}
out["ALL_PASS"] = all(out["PASS"].values())
json.dump(out, open(os.path.join(ROOT, "evidence", "shibA_scene_qc.json"), "w"), indent=2)
print(json.dumps({k: out[k] for k in ("pair_checks", "overlapping_pairs", "camera_min_surface_distance_m", "PASS", "ALL_PASS")}, indent=2))
sys.exit(0 if out["ALL_PASS"] else 1)
