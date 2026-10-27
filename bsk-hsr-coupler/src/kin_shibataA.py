#!/usr/bin/env python3
"""TEST A — Shibata-family tight-lock concept rig (CONCEPT_ONLY), analytic kinematics + bake.

numpy + shapely. Reads rig_config.json["test_A_shibata"], writes evidence/shibA_bake.npz, evidence/shibA_events.json.

Head-A local frame: +y toward partner, +Z up, +alpha = CCW seen from +Z. Head B = A rotated 180 deg about Z,
faces g apart (A face at y=-g/2, B face at y=+g/2); B-local point p -> A-local (-p.x, -p.y + g).

Parts (own head, local):
  protrusion (knuckle): stadium along +y at x=+xc: neck (radius rn) for y in [0, ln], head (radius rh) for y in [ln, lp]
                        with a rounded tip. Top-view polygon, extruded in z in the build.
  chamber window:       square hole in the face at x=-xc where the partner's protrusion enters.
  lock:                 sector [a0,a1] (radius R, hub r_hub) about the vertical pivot Pv, rotated by alpha.
                        Entirely inside the housing; a1 end = nose.
Rule: the lock sector never intersects the partner's protrusion polygon (mapped to A-local at gap g), the partner's
lock, or its own protrusion. alpha(g) = largest alpha <= alpha_ready that is free (spring pushes toward ready).
The head of the incoming knuckle pushes the nose aside; when the neck groove reaches the nose, the lock is free
again -> spring snap (scripted over snap_frames, starting at the frame the solver reports the release).
Nothing here is a measurement.
"""
import json, math, os
import numpy as np
from shapely.geometry import Point, Polygon
from shapely.ops import unary_union
from shapely import affinity

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
CFG = json.load(open(os.path.join(HERE, "rig_config.json"))); T = CFG["test_A_shibata"]
G = {k: v["value"] for k, v in T["geometry"].items()}; M = {k: (v["value"] if isinstance(v, dict) else v) for k, v in T["motion"].items()}
N = T["bake_frames"]; ET = T["events_target"]
F_CONTACT, F_LOCK = ET["JP_FIRST_CONTACT"]["local_F"], ET["JP_LOCKED"]["local_F"]
SNAP = M["snap_frames"]; F_SNAP_START = F_LOCK - SNAP
xc, rh, rn, lp, ln = G["protrusion_x"], G["protrusion_head_radius"], G["protrusion_neck_radius"], G["protrusion_length"], G["protrusion_neck_length"]
Pv = np.array(G["lock_pivot"]); R, r_hub = G["lock_radius"], G["lock_hub_radius"]; a0, a1 = [math.radians(a) for a in G["lock_span_deg"]]
A_READY = math.radians(G["alpha_ready_deg"]); clr = G["design_clearance"]

def smoothstep(x): x = min(max(x, 0.0), 1.0); return x * x * (3 - 2 * x)
def dirv(a): return np.array([-math.sin(a), math.cos(a)])
def to_partner(poly, g): return affinity.affine_transform(poly, [-1, 0, 0, -1, 0, g])   # (x,y) -> (-x, -y+g)

def protrusion_poly(grow=0.0):
    """own knuckle in own local frame (+y forward), optionally grown by a clearance."""
    neck = Polygon([(xc - rn, 0), (xc + rn, 0), (xc + rn, ln), (xc - rn, ln)])
    head = Polygon([(xc - rh, ln), (xc + rh, ln), (xc + rh, lp - rh), (xc - rh, lp - rh)])
    cap = Point(xc, lp - rh).buffer(rh, 64)
    p = unary_union([neck, head, cap]); return p.buffer(grow, 16) if grow else p
PROT = protrusion_poly(clr)

def lock_poly_ready():
    """D-shaped body (sector cut flat at lock_flat_top_y) + nose tooth rectangle, A-local, alpha=0."""
    pts = [Pv + R * dirv(a0 + (a1 - a0) * i / 48) for i in range(49)] + [Pv + r_hub * dirv(a1 - (a1 - a0) * i / 12) for i in range(13)]
    body = Polygon([tuple(p) for p in pts]).intersection(Polygon([(-1, -1), (1, -1), (1, G["lock_flat_top_y"]), (-1, G["lock_flat_top_y"])]))
    t = G["lock_tooth"]; tooth = Polygon([(t["x0"], t["y0"]), (t["x1"], t["y0"]), (t["x1"], t["y1"]), (t["x0"], t["y1"])])
    u = unary_union([body, tooth]); assert u.geom_type == "Polygon", "lock body and tooth must be connected"
    return u
LOCK0 = lock_poly_ready()
def sector(alpha): return affinity.rotate(LOCK0, math.degrees(alpha), origin=(Pv[0], Pv[1]))
def blocked(alpha, g):
    s = sector(alpha)
    return s.intersects(to_partner(PROT, g)) or s.intersects(PROT) or s.intersects(to_partner(sector(alpha), g))
def alpha_for_gap(g):
    step = math.radians(0.25); a = A_READY
    while a > A_READY - math.radians(100) and blocked(a, g): a -= step
    if a <= A_READY - math.radians(100): raise RuntimeError(f"lock cannot clear at g={g:.4f}")
    if a < A_READY:
        lo, hi = a, a + step
        for _ in range(30):
            m = 0.5 * (lo + hi)
            if blocked(m, g): hi = m
            else: lo = m
        a = lo
    return a

# scan g downward: first contact gap, retraction minimum, and the gap where the spring return begins
gs = np.linspace(M["gap_start"], 0.0, 601); alphas = np.array([alpha_for_gap(g) for g in gs])
touch = np.where(alphas < A_READY - 1e-6)[0]; assert len(touch), "protrusion never touches the lock nose: retune geometry"
g_contact = float(gs[touch[0]]); imin = int(np.argmin(alphas))
ret = next((i for i in range(imin, len(gs)) if alphas[i] > alphas[imin] + math.radians(0.5)), None)
assert ret is not None, "lock never returns: nose never reaches the neck groove"
g_return = float(gs[ret - 1]); alpha_at_release = float(alphas[imin])

def gap_at(F):
    """slow readable approach to the start of the spring return, then the last millimetres at coupling speed."""
    g0 = M["gap_start"]
    if F <= F_CONTACT: return g0 + (g_contact - g0) * smoothstep((F - 1) / (F_CONTACT - 1))
    if F <= F_SNAP_START: return g_contact + (g_return - g_contact) * smoothstep((F - F_CONTACT) / (F_SNAP_START - F_CONTACT))
    if F < F_LOCK: return g_return * (1 - (F - F_SNAP_START) / SNAP)
    p0, p1 = M["tension_pull_frames"]
    return M["post_lock_tension_pull"] * smoothstep((F - p0) / (p1 - p0)) if F >= p0 else 0.0

frames = np.arange(0, N + 2); rows = []
for F in frames:
    Fc = int(max(1, min(N, F))); g = gap_at(Fc); a = alpha_for_gap(g)          # alpha always follows the geometry (no scripted pose)
    if Fc < F_SNAP_START: mode = 0 if a >= A_READY - 1e-6 else 1
    elif Fc < F_LOCK: mode = 2
    else: mode = 3
    sp = Pv + G["spring_lock_radius"] * dirv(math.radians(G["spring_lock_angle_deg"]) + a)
    rows.append([F, g, a, float(np.linalg.norm(sp - np.array(G["spring_anchor"]))), mode])
B = np.array(rows)
for ch in (1, 2): B[0, ch] = 2 * B[1, ch] - B[2, ch]; B[-1, ch] = 2 * B[-2, ch] - B[-3, ch]
body = B[1:N + 1]
contact_F = int(body[np.argmax(body[:, 4] >= 1), 0]); peak_F = int(body[np.argmin(body[:, 2]), 0]); locked_F = int(body[np.argmax(body[:, 4] == 3), 0])
s_lock = sector(A_READY); neck_box = to_partner(Polygon([(xc - rh, 0), (xc + rh, 0), (xc + rh, ln), (xc - rh, ln)]), 0.0)
wedge = s_lock.intersects(neck_box.buffer(0.004)) and not s_lock.intersects(to_partner(PROT, 0.0))
events = {"JP_FIRST_CONTACT": {"local_F": contact_F, "world_F": T["world_frame_start"] - 1 + contact_F},
          "JP_RETRACT_PEAK": {"local_F": peak_F, "world_F": T["world_frame_start"] - 1 + peak_F},
          "JP_LOCKED": {"local_F": locked_F, "world_F": T["world_frame_start"] - 1 + locked_F},
          "derived": {"gap_contact_m": g_contact, "gap_return_start_m": g_return, "alpha_min_deg": math.degrees(body[:, 2].min()),
                      "retraction_deg": G["alpha_ready_deg"] - math.degrees(body[:, 2].min()), "alpha_at_release_deg": math.degrees(alpha_at_release),
                      "nose_in_neck_groove_at_lock": bool(wedge), "lock_max_y_m": float(s_lock.bounds[3])},
          "grade": "CONCEPT_ONLY", "note": "events detected from bake; lock-to-lock engagement of the real design not modelled"}
os.makedirs(os.path.join(ROOT, "evidence"), exist_ok=True)
np.savez(os.path.join(ROOT, "evidence", "shibA_bake.npz"), bake=B, cols=np.array(["F", "gap", "alpha", "spring_len", "mode"]),
         lock_poly=np.array(LOCK0.exterior.coords), prot_poly=np.array(protrusion_poly(0.0).exterior.coords))
json.dump(events, open(os.path.join(ROOT, "evidence", "shibA_events.json"), "w"), indent=2)
print(json.dumps(events, indent=2))
