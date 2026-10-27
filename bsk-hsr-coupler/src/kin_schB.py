#!/usr/bin/env python3
"""TEST B — Scharfenberg-family concept rig, analytic kinematics + bake.

Pure numpy. Reads rig_config.json, writes:
  evidence/schB_bake.npz        per-frame state (local F0..F181; F0/F181 are motion-blur pads)
  evidence/schB_events.json     event frames detected from the bake (not copied from design targets)

Model (head-A local frame, +y toward partner, +Z up, +theta = CCW seen from +Z):
  pivot P = (0, -pivot_setback)
  dir(a) = (-sin a, cos a)  (angle a measured CCW from local +y)
  link pin on plate : P + r_lp * dir(phi_lp + theta)
  hook notch        : P + r_n  * dir(phi_n  + theta)
  hook-plate cam    : rho(a) = core + h*0.5*(1+cos(pi*(a-c)/w)) for |a-c|<=w, else core   (a in plate-local)
  link: rigid bar, length L, hinged at the link pin. Guided through G=(guide_x, 0) on the face before lock;
        eye sits in the partner's notch after lock (closed loop). L derived from closure at theta_lock, g=0.
  head B = head A rotated 180 deg about world Z; faces at y=+g/2 (A at -g/2). Symmetry => theta_A = theta_B.

Phases: approach (theta=0) -> deflection (partner tip rides this plate's cam, theta<0 = pushed back)
        -> free (tip passed the lobe) -> snap to lock (spring) -> locked (closed loop, micro tension pull).
All numbers CONCEPT grade. Nothing here is a measurement.
"""
import json, math, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
CFG = json.load(open(os.path.join(HERE, "rig_config.json"))); T = CFG["test_B_scharfenberg"]
G = {k: v["value"] for k, v in T["geometry"].items()}; M = {k: v["value"] if isinstance(v, dict) else v for k, v in T["motion"].items()}
N = T["bake_frames"]; F_ENGAGE = T["events_target"]["SCH_LINK_ENGAGE"]["local_F"]; F_LOCK = T["events_target"]["SCH_LOCKED"]["local_F"]
SNAP = M["snap_frames"]; F_SNAP_START = F_LOCK - SNAP
d = G["pivot_setback"]; R0 = G["plate_radius"]; LOBE = G["hook_lobe"]
r_lp = G["link_pin_radius"]; phi_lp = math.radians(G["link_pin_angle_ready_deg"])
r_n = G["notch_radius"]; phi_n = math.radians(G["notch_angle_deg"]); Gx = G["link_guide_x"]; clr = G["design_clearance"]
TH_LOCK = math.radians(G["theta_lock_deg"]); P = np.array([0.0, -d])

def dirv(a): return np.array([-math.sin(a), math.cos(a)])
def smoothstep(x): x = min(max(x, 0.0), 1.0); return x * x * (3 - 2 * x)
def wrap(a): return (a + math.pi) % (2 * math.pi) - math.pi
def in_notch(a): return abs(wrap(a - phi_n)) <= math.radians(LOBE["notch_cut_half_width_deg"])
def rho(a):
    if in_notch(a): return r_n
    c, w, h = math.radians(LOBE["center_deg"]), math.radians(LOBE["half_width_deg"]), LOBE["height"]
    da = wrap(a - c); return R0 + (h * 0.5 * (1 + math.cos(math.pi * da / w)) if abs(da) <= w else 0.0)
def linkpin_local(th): return P + r_lp * dirv(phi_lp + th)
def notch_local(th): return P + r_n * dirv(phi_n + th)
def B_to_A(p, g): return np.array([-p[0], -p[1] + g])      # B-local -> A-local (180 deg about Z, faces g apart)
A_to_B = B_to_A                                            # the map is an involution

def pin_to_notch(th, g):
    a = linkpin_local(th); b = B_to_A(notch_local(th), g); return float(np.linalg.norm(a - b)), a, b
L = pin_to_notch(TH_LOCK, 0.0)[0]

def bisect(f, lo, hi, it=60):
    flo = f(lo)
    for _ in range(it):
        m = 0.5 * (lo + hi); fm = f(m)
        if (fm < 0) == (flo < 0): lo, flo = m, fm
        else: hi = m
    return 0.5 * (lo + hi)

def theta_lock_for_gap(g):
    """closure root nearest to TH_LOCK (at g=0 that root is TH_LOCK itself by construction)."""
    f = lambda t: pin_to_notch(t, g)[0] - L
    if abs(f(TH_LOCK)) < 1e-12: return TH_LOCK
    step = math.radians(0.5); s0 = f(TH_LOCK) < 0
    for k in range(1, 121):
        for sgn in (-1, 1):
            t = TH_LOCK + sgn * k * step
            if (f(t) < 0) != s0: return bisect(f, t - sgn * step, t)
    raise RuntimeError("no closure root near theta_lock")
def guided_tip(th):
    pin = linkpin_local(th); u = np.array([Gx, 0.0]) - pin; u /= np.linalg.norm(u); return pin + L * u, pin
def tip_polar_on_B(tipA, g, thB):
    """tip of link A in plate-B polar coords: (radius, plate-local angle)"""
    q = A_to_B(tipA, g) - P; r = float(np.linalg.norm(q)); a = math.atan2(-q[0], q[1]) - thB; return r, wrap(a)
def cam_violation(th, g):
    tip, _ = guided_tip(th); r, a = tip_polar_on_B(tip, g, th); return (rho(a) + clr) - r
DEF_SIGN = M.get("deflection_sign", 1)
def theta_deflect(g, prev=0.0):
    """deflection = plate rotated by the partner's link tip, in the direction that moves the hook lobe away
    from the tip (DEF_SIGN, CONCEPT). Smallest |theta| that clears the cam.
    If the tip is already over the notch cut, the plate stays where it was until the scripted spring snap."""
    tip0, _ = guided_tip(prev); _, a0 = tip_polar_on_B(tip0, g, prev)
    if prev != 0.0 and in_notch(a0): return prev, True
    if cam_violation(0.0, g) <= 0: return 0.0, False
    th = 0.0; step = DEF_SIGN * math.radians(0.25)
    while abs(th) < math.radians(80) and cam_violation(th, g) > 0: th += step
    lo, hi = (th - step, th) if DEF_SIGN > 0 else (th, th - step)
    return bisect(lambda t: cam_violation(t, g), lo, hi), True
def tip_in_notch(th, g):
    tip, _ = guided_tip(th); _, a = tip_polar_on_B(tip, g, th); return in_notch(a)

# gap at which the partner tip first touches the cam (theta=0)
g_engage = bisect(lambda g: cam_violation(0.0, g), 0.0, M["gap_start"]) if cam_violation(0.0, 0.0) > 0 else 0.0
assert g_engage > 0, "no cam contact at all: tip never touches the hook lobe -> retune geometry"

def gap_at(F):
    g0 = M["gap_start"]
    if F <= F_ENGAGE: return g0 + (g_engage - g0) * smoothstep((F - 1) / (F_ENGAGE - 1))
    if F <= F_SNAP_START: return g_engage * (1 - smoothstep((F - F_ENGAGE) / (F_SNAP_START - F_ENGAGE)))
    p0, p1 = M["tension_pull_frames"]
    return M["post_lock_tension_pull"] * smoothstep((F - p0) / (p1 - p0)) if F >= p0 else 0.0

frames = np.arange(0, N + 2); rows = []; th_min = 0.0; th_at_snap = None; th_prev = 0.0
for F in frames:
    Fc = int(max(1, min(N, F))); g = gap_at(Fc)
    if Fc < F_SNAP_START:
        th, _ = theta_deflect(g, th_prev); tip, pin = guided_tip(th); mode = 0 if th == 0.0 else 1; th_min = th if abs(th) > abs(th_min) else th_min
        th_at_snap = th; th_prev = th
    elif Fc < F_LOCK:
        s = smoothstep((Fc - F_SNAP_START) / SNAP); th = th_at_snap + (theta_lock_for_gap(0.0) - th_at_snap) * s
        tg, pin = guided_tip(th); tn = B_to_A(notch_local(th), g)
        u = (tg * (1 - s) + tn * s) - pin; u /= np.linalg.norm(u); tip = pin + L * u; mode = 2
    else:
        th = theta_lock_for_gap(g); pin = linkpin_local(th); tip = B_to_A(notch_local(th), g); mode = 3
    la = math.atan2((tip - pin)[1], (tip - pin)[0])
    sp = P + G["spring_plate_radius"] * dirv(math.radians(G["spring_plate_angle_deg"]) + th)
    rows.append([F, g, th, pin[0], pin[1], tip[0], tip[1], la, float(np.linalg.norm(sp - np.array(G["spring_anchor"]))), mode])
B = np.array(rows)
for ch in (1, 2, 7):                                   # motion-blur pads: linear extrapolation
    B[0, ch] = 2 * B[1, ch] - B[2, ch]; B[-1, ch] = 2 * B[-2, ch] - B[-3, ch]

body = B[1:N + 1]
engage_F = int(body[np.argmax(body[:, 9] >= 1), 0]); locked_F = int(body[np.argmax(body[:, 9] == 3), 0])
events = {"SCH_LINK_ENGAGE": {"local_F": engage_F, "world_F": T["world_frame_start"] - 1 + engage_F},
          "SCH_LOCKED": {"local_F": locked_F, "world_F": T["world_frame_start"] - 1 + locked_F},
          "derived": {"link_length_m": L, "gap_engage_m": g_engage, "theta_deflect_max_abs_deg": math.degrees(th_min),
                      "theta_lock_deg": math.degrees(theta_lock_for_gap(0.0)),
                      "snap_visible": bool(abs(th_at_snap - theta_lock_for_gap(0.0)) > math.radians(3)),
                      "tip_in_notch_at_snap": bool(tip_in_notch(th_at_snap, 0.0))},
          "grade": "CONCEPT", "note": "events detected from bake mode column, not copied from targets"}
os.makedirs(os.path.join(ROOT, "evidence"), exist_ok=True)
np.savez(os.path.join(ROOT, "evidence", "schB_bake.npz"), bake=B, link_length=L,
         cols=np.array(["F", "gap", "theta", "pin_x", "pin_y", "tip_x", "tip_y", "link_ang", "spring_len", "mode"]))
json.dump(events, open(os.path.join(ROOT, "evidence", "schB_events.json"), "w"), indent=2)
print(json.dumps(events, indent=2))
