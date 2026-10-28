#!/usr/bin/env python3
"""Reproduction check: compare a fresh local bake/QC with the reference values from the cloud session (R8 track A)."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); EVD = os.path.join(os.path.dirname(HERE), "evidence")
REF = {
  "schB_events.json": {"SCH_LINK_ENGAGE.local_F": 97, "SCH_LOCKED.local_F": 120, "derived.link_length_m": (0.325852562953138, 1e-9),
                       "derived.theta_deflect_max_abs_deg": (-14.268085847667027, 0.05)},
  "shibA_events.json": {"JP_FIRST_CONTACT.local_F": 12, "JP_RETRACT_PEAK.local_F": 80, "JP_LOCKED.local_F": 140,
                        "derived.retraction_deg": (10.034962107194595, 0.05)},
  "schB_bake_qc.json": {"ALL_PASS": True}, "shibA_bake_qc.json": {"ALL_PASS": True},
  "schB_scene_qc.json": {"ALL_PASS": True, "pair_checks": 4823}, "shibA_scene_qc.json": {"ALL_PASS": True, "pair_checks": 2451},
}
def get(d, path):
    for k in path.split("."): d = d[k]
    return d
fails = []
for fn, checks in REF.items():
    d = json.load(open(os.path.join(EVD, fn)))
    for path, ref in checks.items():
        v = get(d, path)
        ok = abs(v - ref[0]) <= ref[1] if isinstance(ref, tuple) else v == ref
        print(f"{'OK  ' if ok else 'FAIL'} {fn}:{path} = {v} (ref {ref})"); fails += [] if ok else [f"{fn}:{path}"]
print("BASELINE", "PASS" if not fails else f"FAIL {fails}"); sys.exit(1 if fails else 0)
