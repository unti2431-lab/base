"""Gate self-test: every gate must FAIL on a deliberately broken input.

1. verify_bake on a bake with a camera jump        -> expect exit 1
2. verify_bake on a bake with roll 2.0 deg         -> expect exit 1
3. verify_scene on a scene with LVALVE_L sunk 5 cm -> expect exit 1
4. import_assets smoke test with fake cubes, one placed into the bogie frame -> verify_scene expect exit 1
Writes ../evidence/gate_selftest.json. Run with the bpy python (or blender -b -P selftest_gates.py).
"""
import os, sys, json, subprocess, tempfile, shutil
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable
TMP = tempfile.mkdtemp(prefix='e5tilt_selftest_')
res = {}


def run(args):
    p = subprocess.run([PY] + args, cwd=HERE, capture_output=True, text=True)
    return p.returncode, (p.stdout + p.stderr)


def failed_cleanly(rc, log):
    """a gate FAIL, not a crash"""
    return rc == 1 and 'Traceback' not in log and ('G3 FAIL' in log or '"result": "FAIL"' in log)


# 1/2 bake corruption
d = dict(np.load(os.path.join(HERE, 'tilt_bake.npz')))
bad = dict(d); loc = bad['cam_C05_loc'].copy(); loc[40:, 0] += 0.6; bad['cam_C05_loc'] = loc
p1 = os.path.join(TMP, 'bad_jump.npz'); np.savez_compressed(p1, **bad)
rc, log = run(['verify_bake.py', '--bake', p1, '--out', os.path.join(TMP, 'q1.json')])
res['bake_camera_jump'] = {'expected': 'FAIL', 'exit': rc, 'ok': failed_cleanly(rc, log)}
bad = dict(d); th = bad['theta'].copy(); th *= 2.0 / 1.5; bad['theta'] = th
p2 = os.path.join(TMP, 'bad_roll.npz'); np.savez_compressed(p2, **bad)
rc, log = run(['verify_bake.py', '--bake', p2, '--out', os.path.join(TMP, 'q2.json')])
res['bake_roll_over_limit'] = {'expected': 'FAIL', 'exit': rc, 'ok': failed_cleanly(rc, log)}

# 3 scene corruption
blend = os.path.join(HERE, '..', 'work', 'e5tilt_R025_proxy.blend')
bad_blend = os.path.join(TMP, 'bad_scene.blend')
code = (f"import bpy; bpy.ops.wm.open_mainfile(filepath=r'{blend}'); o=bpy.data.objects['LVALVE_L']; "
        f"o.location.z -= 0.05; bpy.ops.wm.save_as_mainfile(filepath=r'{bad_blend}')")
subprocess.run([PY, '-c', code], cwd=HERE, capture_output=True)
rc, log = run(['verify_scene.py', '--', '--blend', bad_blend, '--step', '100', '--out', os.path.join(TMP, 'q3.json')])
res['scene_sunk_valve'] = {'expected': 'FAIL', 'exit': rc, 'ok': failed_cleanly(rc, log),
                           'hit': [l for l in log.splitlines() if 'LVALVE' in l][:2]}

# 4 asset import smoke test (fake cubes, one deliberately inside the bogie frame)
rc4, log4 = run(['import_assets.py', '--', '--smoke', '--blend', blend, '--out', os.path.join(TMP, 'smoke.blend')])
res['import_smoke_runs'] = {'expected': 'exit 0', 'exit': rc4, 'ok': rc4 == 0, 'log': log4[-200:]}
if rc4 == 0:
    rc, log = run(['verify_scene.py', '--', '--blend', os.path.join(TMP, 'smoke.blend'), '--step', '100',
                   '--extra_pairs', os.path.join(TMP, 'smoke_pairs.json'), '--out', os.path.join(TMP, 'q4.json')])
    res['import_smoke_collision_detected'] = {'expected': 'FAIL', 'exit': rc, 'ok': failed_cleanly(rc, log),
                                              'hit': [l for l in log.splitlines() if 'FAKE_COLLIDE' in l][:2]}

allok = all(v['ok'] for v in res.values())
out = os.path.join(HERE, '..', 'evidence', 'gate_selftest.json')
json.dump({'result': 'PASS' if allok else 'FAIL', 'tests': res}, open(out, 'w'), indent=2)
print(json.dumps(res, indent=1))
print('SELFTEST', 'PASS' if allok else 'FAIL')
shutil.rmtree(TMP, ignore_errors=True)
sys.exit(0 if allok else 1)
