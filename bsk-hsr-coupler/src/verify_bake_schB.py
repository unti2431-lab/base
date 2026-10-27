#!/usr/bin/env python3
"""Independent bake verification for TEST B. Does not import kin_schB; recomputes from npz + config."""
import json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
CFG = json.load(open(os.path.join(HERE, "rig_config.json")))["test_B_scharfenberg"]
G = {k: v["value"] for k, v in CFG["geometry"].items()}
Z = np.load(os.path.join(ROOT, "evidence", "schB_bake.npz")); B = Z["bake"]; L = float(Z["link_length"])
ev = json.load(open(os.path.join(ROOT, "evidence", "schB_events.json"))); N = CFG["bake_frames"]
body = B[1:N + 1]; F, g, th, px, py, tx, ty, la, sl, mode = body.T
d = G["pivot_setback"]; core = G["plate_radius"]; LB = G["hook_lobe"]; P = np.array([0.0, -d])

def rho(a):
    if abs((a - math.radians(G["notch_angle_deg"]) + math.pi) % (2 * math.pi) - math.pi) <= math.radians(LB["notch_cut_half_width_deg"]): return G["notch_radius"]
    c, w, h = math.radians(LB["center_deg"]), math.radians(LB["half_width_deg"]), LB["height"]
    da = (a - c + math.pi) % (2 * math.pi) - math.pi
    return core + (h * 0.5 * (1 + math.cos(math.pi * da / w)) if abs(da) <= w else 0.0)

res = {}
ln = np.hypot(tx - px, ty - py); res["link_length_err_max_m"] = float(np.abs(ln - L).max())
# closed loop while locked: tipA == notchB mapped to A-local = (-nx, -ny+g)
nb = np.stack([-G["notch_radius"] * np.sin(math.radians(G["notch_angle_deg"]) + th), -d + G["notch_radius"] * np.cos(math.radians(G["notch_angle_deg"]) + th)], 1)
notchB_A = np.stack([-nb[:, 0], -nb[:, 1] + g], 1); lock = mode == 3
res["loop_closure_err_max_m"] = float(np.hypot(tx[lock] - notchB_A[lock, 0], ty[lock] - notchB_A[lock, 1]).max())
# cam never penetrated before the snap: tip radius about pivot B >= rho(plate-local angle)
qx, qy = -tx - 0.0, (-ty + g) - (-d)           # tip in B-local, relative to pivot B
r = np.hypot(qx, qy); a = np.arctan2(-qx, qy) - th
pre = mode <= 1; pen = np.array([rho(ai) for ai in a]) - r
res["cam_penetration_max_m"] = float(max(0.0, pen[pre].max()))
res["pin_radius_err_max_m"] = float(np.abs(np.hypot(px - P[0], py - P[1]) - G["link_pin_radius"]).max())
res["theta_step_max_deg"] = float(np.degrees(np.abs(np.diff(th)).max()))
res["link_ang_step_max_deg"] = float(np.degrees(np.abs(np.diff(la)).max()))
tgt = CFG["events_target"]
res["event_engage_delta_F"] = int(ev["SCH_LINK_ENGAGE"]["local_F"] - tgt["SCH_LINK_ENGAGE"]["local_F"])
res["event_locked_delta_F"] = int(ev["SCH_LOCKED"]["local_F"] - tgt["SCH_LOCKED"]["local_F"])
res["gap_monotone_until_lock"] = bool(np.all(np.diff(g[:ev["SCH_LOCKED"]["local_F"]]) <= 1e-12))
E = ev["SCH_LOCKED"]["local_F"]; res["g3_window"] = [E - 60, E + 59]; res["g3_window_fits"] = bool(E - 60 >= 1 and E + 59 <= N)
res["deflection_frames"] = int((mode == 1).sum()); res["snap_visible"] = bool(ev["derived"]["snap_visible"])
res["theta_deflect_max_abs_deg"] = float(np.degrees(np.abs(th).max()))
PASS = {"link_length": res["link_length_err_max_m"] < 1e-5, "loop_closure": res["loop_closure_err_max_m"] < 1e-5,
        "no_cam_penetration": res["cam_penetration_max_m"] < 1e-6, "pin_on_circle": res["pin_radius_err_max_m"] < 1e-9,
        "no_jumps": res["theta_step_max_deg"] < 8.0 and res["link_ang_step_max_deg"] < 8.0,
        "events_on_target": abs(res["event_engage_delta_F"]) <= 1 and abs(res["event_locked_delta_F"]) <= 1,
        "gap_monotone": res["gap_monotone_until_lock"], "g3_window_fits": res["g3_window_fits"],
        "deflection_readable": res["deflection_frames"] >= 12 and res["theta_deflect_max_abs_deg"] > 6.0, "snap_visible": res["snap_visible"]}
out = {"metrics": res, "PASS": PASS, "ALL_PASS": all(PASS.values()), "grade": "T (bake-level only; geometry is CONCEPT)"}
json.dump(out, open(os.path.join(ROOT, "evidence", "schB_bake_qc.json"), "w"), indent=2)
print(json.dumps(out, indent=2)); sys.exit(0 if out["ALL_PASS"] else 1)
