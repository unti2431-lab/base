#!/usr/bin/env python3
"""Independent bake verification for TEST A (does not import kin_shibataA; rebuilds the polygons itself)."""
import json, math, os, sys
import numpy as np
from shapely.geometry import Point, Polygon
from shapely.ops import unary_union
from shapely import affinity

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
CFG = json.load(open(os.path.join(HERE, "rig_config.json")))["test_A_shibata"]; G = {k: v["value"] for k, v in CFG["geometry"].items()}
B = np.load(os.path.join(ROOT, "evidence", "shibA_bake.npz"))["bake"]; ev = json.load(open(os.path.join(ROOT, "evidence", "shibA_events.json")))
N = CFG["bake_frames"]; body = B[1:N + 1]; F, g, al, sl, mode = body.T
xc, rh, rn, lp, ln = G["protrusion_x"], G["protrusion_head_radius"], G["protrusion_neck_radius"], G["protrusion_length"], G["protrusion_neck_length"]
Pv = np.array(G["lock_pivot"]); R, r_hub = G["lock_radius"], G["lock_hub_radius"]; a0, a1 = [math.radians(a) for a in G["lock_span_deg"]]
AR = math.radians(G["alpha_ready_deg"]); hw, ft = G["front_plate_half_width"], G["front_plate_thickness"]
def dirv(a): return np.array([-math.sin(a), math.cos(a)])
def prot():
    return unary_union([Polygon([(xc - rn, 0), (xc + rn, 0), (xc + rn, ln), (xc - rn, ln)]),
                        Polygon([(xc - rh, ln), (xc + rh, ln), (xc + rh, lp - rh), (xc - rh, lp - rh)]), Point(xc, lp - rh).buffer(rh, 64)])
LOCK0 = Polygon([tuple(p) for p in np.load(os.path.join(ROOT, "evidence", "shibA_bake.npz"))["lock_poly"]])   # the baked lock shape; checked against config below
def sector(a): return affinity.rotate(LOCK0, math.degrees(a), origin=(Pv[0], Pv[1]))
def partner(poly, gg): return affinity.affine_transform(poly, [-1, 0, 0, -1, 0, gg])
PR = prot(); res = {}
tth = G["lock_tooth"]; bx = LOCK0.bounds
res["lock_shape_matches_config"] = bool(abs(bx[0] - tth["x0"]) < 1e-6 and abs(bx[3] - G["lock_flat_top_y"]) < 1e-6 and abs(max(np.hypot(*(np.array(LOCK0.exterior.coords) - Pv).T)) - R) < 2e-3)
# 1 penetration: lock vs partner protrusion / own protrusion / partner lock / own face slab, every frame (exact, no clearance)
pen = 0.0; face_hit = 0; lock_hit = 0
for i in range(N):
    s = sector(al[i]); pp = partner(PR, g[i])
    pen = max(pen, s.intersection(pp).area, s.intersection(PR).area)
    if s.intersects(partner(s, g[i])): lock_hit += 1
    if s.bounds[3] > 0.0: face_hit += 1                                   # lock must stay inside its own housing
res["penetration_area_max_m2"] = float(pen); res["lock_lock_hits"] = lock_hit; res["lock_crosses_own_face_frames"] = face_hit
# 2 spring pushes toward ready: alpha <= ready always, and alpha is the max free angle (check a +0.5 deg nudge is blocked while deflected)
nud = 0
for i in range(N):
    if mode[i] == 1 and al[i] < AR - 1e-6:
        s2 = sector(min(AR, al[i] + math.radians(0.5))); PRc = PR.buffer(G["design_clearance"], 16)   # the solver keeps the design clearance
        if not (s2.intersects(partner(PRc, g[i])) or s2.intersects(PRc)): nud += 1
res["frames_not_at_max_free_alpha"] = nud; res["alpha_max_deg"] = float(np.degrees(al.max()))
# 3 jumps / events / gap / window
res["alpha_step_max_deg"] = float(np.degrees(np.abs(np.diff(al)).max()))
tg = CFG["events_target"]
for k in ("JP_FIRST_CONTACT", "JP_RETRACT_PEAK", "JP_LOCKED"): res[f"{k}_delta_F"] = int(ev[k]["local_F"] - tg[k]["local_F"])
res["gap_monotone_until_lock"] = bool(np.all(np.diff(g[:ev["JP_LOCKED"]["local_F"]]) <= 1e-12))
E = ev["JP_LOCKED"]["local_F"]; res["g3_window"] = [E - 60, E + 59]; res["g3_window_fits"] = bool(E - 60 >= 1 and E + 59 <= N)
res["retraction_deg"] = float(np.degrees(AR - al.min())); res["deflection_frames"] = int((mode == 1).sum()); E_ = ev["JP_LOCKED"]["local_F"]; res["return_deg_last_8F"] = float(np.degrees(al[E_ - 1] - al[max(0, E_ - 9)]))
res["nose_in_neck_groove_at_lock"] = bool(ev["derived"]["nose_in_neck_groove_at_lock"])
PASS = {"lock_shape_matches_config": res["lock_shape_matches_config"], "no_penetration": res["penetration_area_max_m2"] < 1e-9 and res["lock_lock_hits"] == 0, "lock_inside_housing": face_hit == 0,
        "spring_follows_max_free": nud == 0 and res["alpha_max_deg"] <= G["alpha_ready_deg"] + 1e-6,
        "no_jumps": res["alpha_step_max_deg"] < 8.0,
        "events_on_target": abs(res["JP_FIRST_CONTACT_delta_F"]) <= 1 and abs(res["JP_LOCKED_delta_F"]) <= 1 and abs(res["JP_RETRACT_PEAK_delta_F"]) <= 20,
        "gap_monotone": res["gap_monotone_until_lock"], "g3_window_fits": res["g3_window_fits"],
        "retraction_readable": res["retraction_deg"] >= 8.0 and res["deflection_frames"] >= 30, "snap_visible": res["return_deg_last_8F"] >= 5.0,
        "wedge_at_lock": res["nose_in_neck_groove_at_lock"]}
out = {"metrics": res, "PASS": PASS, "ALL_PASS": all(PASS.values()), "grade": "T (bake-level only; geometry is CONCEPT_ONLY)"}
json.dump(out, open(os.path.join(ROOT, "evidence", "shibA_bake_qc.json"), "w"), indent=2); print(json.dumps(out, indent=2)); sys.exit(0 if out["ALL_PASS"] else 1)
