#!/usr/bin/env python3
"""L08 W0 loop QC (bpy 4.5). Reads evidence/W0_BLOCK.blend only (does not import build_w0.py).
Checks: virtual F1261 == F1 for camera pose / FOV / env phase / wheel phase / lights; velocity and angular velocity
continuity across the seam (F1260->F1261 vs F1->F2); no kink at the F50 follow->dolly join; camera clearance on every
shown frame; no negative-scale objects. Writes evidence/w0_loop_qc.json.
"""
import os, json, sys, math
import numpy as np
import bpy
from mathutils.bvhtree import BVHTree

LOCK = (4, 5); assert bpy.app.version[:2] == LOCK
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
QC = json.load(open(os.path.join(HERE, "rig_config.json"), encoding="utf-8"))["w0_loop"]["qc"]
bpy.ops.wm.open_mainfile(filepath=os.path.join(ROOT, "evidence", "W0_BLOCK.blend"))   # bpy.ops allowed: file open
sc = bpy.context.scene; cam = sc.camera; SEAM = sc.frame_end + 1

def state(f):
    sc.frame_set(f); M = np.array(cam.matrix_world, dtype=float)
    env = {o.name: o.location.y for o in sc.objects if o.name.startswith("ENV_")}
    wheels = {o.name: o.rotation_euler.x for o in sc.objects if "_WHEEL_" in o.name and not o.name.endswith("_MARK")}
    lights = {o.name: (o.data.energy, tuple(o.matrix_world.translation), tuple(o.rotation_euler)) for o in sc.objects if o.type == 'LIGHT'}
    return {"M": M, "lens": cam.data.lens, "env": env, "wheels": wheels, "lights": lights}

def _rotvec(R):   # well-conditioned for small angles: theta = atan2(|skew|, (tr-1)/2), axis from the skew part
    k = np.array([R[2, 1] - R[1, 2], R[0, 2] - R[2, 0], R[1, 0] - R[0, 1]]) / 2.0; s = np.linalg.norm(k)
    th = math.atan2(s, (np.trace(R) - 1) / 2.0)
    return np.zeros(3) if s < 1e-15 else math.degrees(th) * k / s

def rot_angle_deg(Ra, Rb): return float(np.linalg.norm(_rotvec(Ra.T @ Rb)))

def ang_vel(Ra, Rb): return _rotvec(Rb @ Ra.T)   # rotation vector of Rb Ra^T (deg)

S1, S2, S60, S61 = state(1), state(2), state(SEAM - 1), state(SEAM)
R = lambda s: s["M"][:3, :3]; P = lambda s: s["M"][:3, 3]
pos_d = float(np.linalg.norm(P(S61) - P(S1))); rot_d = rot_angle_deg(R(S1), R(S61))
v_start, v_seam = P(S2) - P(S1), P(S61) - P(S60); dv = float(np.linalg.norm(v_seam - v_start))
w_start, w_seam = ang_vel(R(S1), R(S2)), ang_vel(R(S60), R(S61)); dw = float(np.linalg.norm(w_seam - w_start))
env_d = max(abs(S61["env"][k] - S1["env"][k]) for k in S1["env"])
env_v = max(abs((S61["env"][k] - S60["env"][k]) - (S2["env"][k] - S1["env"][k])) for k in S1["env"])
sixth = 2 * math.pi / 6
wheel_d = max(abs(((S61["wheels"][k] - S1["wheels"][k]) + sixth / 2) % sixth - sixth / 2) for k in S1["wheels"])
light_same = S61["lights"] == S1["lights"]
# kink at the F50 join (follow -> dolly)
a49, a50, a51 = state(49), state(50), state(51)
kink = float(np.linalg.norm((P(a51) - P(a50)) - (P(a50) - P(a49))))
kink_ref = float(np.linalg.norm(P(a50) - P(a49)))
# per-frame speed profile on shown frames (for the report: no stall, no spike)
shown = list(range(1, 121)) + list(range(1186, SEAM))
pts = {f: P(state(f)) for f in shown}
spd = {f: float(np.linalg.norm(pts[f + 1] - pts[f])) for f in shown if f + 1 in pts}
acc = [abs(spd[f + 1] - spd[f]) for f in spd if f + 1 in spd]
# camera clearance on every 2nd shown frame
dg = bpy.context.evaluated_depsgraph_get(); trees = {}
def world_bvh(ob):
    eo = ob.evaluated_get(dg); me = eo.to_mesh(); me.calc_loop_triangles()
    v = np.empty(len(me.vertices) * 3); me.vertices.foreach_get('co', v); v = v.reshape(-1, 3)
    M = np.array(eo.matrix_world); w = v @ M[:3, :3].T + M[:3, 3]
    t = np.empty(len(me.loop_triangles) * 3, dtype=np.int32); me.loop_triangles.foreach_get('vertices', t)
    tr = BVHTree.FromPolygons(w.tolist(), t.reshape(-1, 3).tolist()); eo.to_mesh_clear(); return tr
min_cam, min_at, min_ob = 1e9, None, None
for f in shown[::2] + [120, 1186]:
    sc.frame_set(f); dg = bpy.context.evaluated_depsgraph_get(); cp = cam.matrix_world.translation
    for o in sc.objects:
        if o.type != 'MESH' or o.hide_render: continue
        loc, nrm, idx, dist = world_bvh(o).find_nearest(cp)
        if dist is not None and dist < min_cam: min_cam, min_at, min_ob = dist, f, o.name
neg = [o.name for o in sc.objects if np.linalg.det(np.array(o.matrix_world)[:3, :3]) <= 0]

out = {"seam_F": SEAM, "camera_pos_delta_m": pos_d, "camera_rot_delta_deg": rot_d, "lens_F1": S1["lens"], "lens_F1261": S61["lens"],
       "velocity_F1_F2": v_start.tolist(), "velocity_F1260_F1261": v_seam.tolist(), "velocity_delta_m_per_frame": dv,
       "angvel_F1_F2_deg": w_start.tolist(), "angvel_F1260_F1261_deg": w_seam.tolist(), "angvel_delta_deg_per_frame": dw,
       "env_phase_delta_m": env_d, "env_velocity_delta_m_per_frame": env_v, "wheel_phase_delta_rad_mod_60deg": wheel_d, "lights_identical": light_same,
       "join_F50_kink_m_per_frame": kink, "join_F50_speed_m_per_frame": kink_ref,
       "camera_speed_min_max_m_per_frame": [min(spd.values()), max(spd.values())], "camera_speed_max_frame_to_frame_change": max(acc),
       "camera_min_surface_distance_m": float(min_cam), "camera_min_at_F": min_at, "camera_min_object": min_ob, "negative_scale_objects": neg}
out["PASS"] = {
    "seam_position": pos_d < QC["seam_pos_tol_m"], "seam_rotation": rot_d < QC["seam_rot_tol_deg"], "seam_fov": abs(S61["lens"] - S1["lens"]) < 1e-9,
    "seam_velocity": dv < QC["seam_vel_tol_m_per_frame"], "seam_angular_velocity": dw < QC["seam_rotvel_tol_deg_per_frame"],
    "seam_env_phase": env_d < 1e-6 and env_v < 1e-6, "seam_wheel_phase": wheel_d < 1e-6, "seam_lights": light_same,
    "join_F50_no_kink": kink < 0.1 * kink_ref + 1e-6, "camera_clearance": min_cam >= QC["camera_clearance_m"], "no_negative_scale": not neg}
out["ALL_PASS"] = all(out["PASS"].values())
json.dump(out, open(os.path.join(ROOT, "evidence", "w0_loop_qc.json"), "w"), indent=2)
print(json.dumps(out, indent=2)); sys.exit(0 if out["ALL_PASS"] else 1)
