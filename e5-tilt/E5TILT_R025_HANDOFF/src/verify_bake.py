"""G3 gate - independent bake verification (numpy only). Does not import kin.py.

Recomputes every check from tilt_bake.npz + rig_config.json + cameras.json.
Writes ../evidence/bake_qc.json and exits 1 on any FAIL.
"""
import json, os, sys, argparse
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


def q2m(q):
    w, x, y, z = q
    return np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                     [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                     [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])


def track_frame(d, s):
    p = np.interp(s, d['path_s'], d['path_psi'])
    o = np.array([np.interp(s, d['path_s'], d['path_x']), np.interp(s, d['path_s'], d['path_y'])])
    r = np.array([np.cos(p), np.sin(p), 0.0]); f = np.array([-np.sin(p), np.cos(p), 0.0])
    return np.column_stack([r, f, [0, 0, 1.0]]), o


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--bake', default=os.path.join(HERE, 'tilt_bake.npz'))
    ap.add_argument('--config', default=os.path.join(HERE, 'rig_config.json'))
    ap.add_argument('--cameras', default=os.path.join(HERE, 'cameras.json'))
    ap.add_argument('--out', default=os.path.join(HERE, '..', 'evidence', 'bake_qc.json'))
    a_ = sys.argv
    argv = a_[a_.index('--') + 1:] if '--' in a_ else ([] if os.path.basename(a_[0]).lower().startswith('blender') else a_[1:])
    a = ap.parse_args(argv)
    d = dict(np.load(a.bake, allow_pickle=False))
    cfg = json.load(open(a.config, encoding='utf-8'))
    cams = json.load(open(a.cameras, encoding='utf-8'))
    fps = cfg['spec']['fps']; F = d['F']; n = len(F)
    R = {}; V = {}

    def chk(name, ok, value, rule):
        R[name] = 'PASS' if ok else 'FAIL'
        V[name] = {'value': value, 'rule': rule}

    # 1. wheel no-slip: d(angle) * r == -d(s)
    r = cfg['bogie']['wheel_r']
    # arc length of each bogie rebuilt from its own location track (independent of kin's s)
    bl = d['bog_loc']
    seg = np.linalg.norm(np.diff(bl, axis=2), axis=-1)            # (cars,2,n-1) chord per frame
    dang = np.abs(np.diff(d['wheel_angle'], axis=-1)) * r
    slip = np.abs(dang - seg) / np.maximum(seg, 1e-6)
    chk('wheel_no_slip', float(slip.max()) < 0.002, float(slip.max()), 'relative slip < 0.2 %')

    # 2. roll limit
    th = np.degrees(d['theta'])
    tm = cfg['tilt']['theta_max_deg']
    chk('roll_max', abs(th.max() - tm) < 0.02 and th.min() > -0.01, [float(th.min()), float(th.max())],
        f'0 <= theta <= {tm} +/- 0.02 deg')

    # 3. spring height difference equals s_lat * sin(theta) (hero car)
    s_lat = cfg['spring']['s_lat']
    dh = d['h_R'] - d['h_L']
    pred = s_lat * np.sin(d['theta'][cfg['train']['hero_car'] - 1])
    err = np.abs(dh - pred)
    chk('spring_dh_vs_roll', float(err.max()) < 0.002, float(err.max()), '|dh - s_lat sin(theta)| < 2 mm')
    chk('spring_stroke_range', bool(d['stroke_L'].min() >= 0 and d['stroke_R'].max() <= 1),
        [float(min(d['stroke_L'].min(), d['stroke_R'].min())), float(max(d['stroke_L'].max(), d['stroke_R'].max()))],
        'stroke in [0,1]')
    chk('inner_spring_vents', bool(d['h_L'].min() < cfg['spring']['h0'] - 0.02 and d['h_R'].max() > cfg['spring']['h0'] + 0.02),
        [float(d['h_L'].min()), float(d['h_R'].max())], 'left(inner) lower, right(outer) higher in a left curve')

    # 4. lean direction: body up-vector tilts to the inner (left) side, i.e. its x component < 0 in the track frame
    hk = cfg['train']['hero_car'] - 1
    i_pk = int(np.argmax(th[hk]))
    Mb = q2m(d['body_quat'][hk, i_pk])
    Mt, _ = track_frame(d, d['s_hero'][i_pk])
    upx = float((Mt.T @ Mb[:, 2])[0])
    chk('lean_to_inner', upx < 0, upx, 'body up vector x (track frame) < 0 = leans left/inner')

    # 5. jump check in the moving frame: body travel per frame / hero travel per frame within [0.8, 1.25]
    ds_h = np.abs(np.diff(d['s_hero']))
    worst = 0.0
    for k in range(d['body_loc'].shape[0]):
        st = np.linalg.norm(np.diff(d['body_loc'][k], axis=0), axis=1)
        ratio = st / np.maximum(ds_h, 1e-6)
        worst = max(worst, float(np.max(np.abs(ratio - 1))))
    chk('body_jump', worst < 0.25, worst, 'per-frame body travel / hero travel within 1 +/- 0.25')

    # 6. cameras: shot length, continuity, never static, W0
    shots = cams['shots']
    lens_s = [(s['F'][1] - s['F'][0] + 1) / fps for s in shots]
    chk('max_shot_len', max(lens_s) <= 4.0, max(lens_s), 'longest shot <= 4.0 s')
    cuts = len(shots) - 1
    dur = (cfg['spec']['frame_end'] - cfg['spec']['frame_start'] + 1) / fps
    chk('cuts_per_10s', 2.5 <= cuts / dur * 10 <= 5.0, cuts / dur * 10, '2.5..5 hard cuts / 10 s (reference: 1.9 hard cuts, 5.6 transitions / 10 s)')
    contiguous = all(shots[i + 1]['F'][0] == shots[i]['F'][1] + 1 for i in range(len(shots) - 1)) \
        and shots[0]['F'][0] == cfg['spec']['frame_start'] and shots[-1]['F'][1] == cfg['spec']['frame_end']
    chk('shots_contiguous', contiguous, contiguous, 'shots tile F1..Fend with no gap/overlap')

    jump_max, static_runs = {}, {}
    for s in shots:
        cid = s['id']
        Fr = d[f'cam_{cid}_F']; loc = d[f'cam_{cid}_loc']; q = d[f'cam_{cid}_quat']; lens = d[f'cam_{cid}_lens']
        m = (Fr >= s['F'][0]) & (Fr <= s['F'][1])
        loc, q, lens, Fr2 = loc[m], q[m], lens[m], Fr[m]
        v = np.diff(loc, axis=0)
        sp = np.linalg.norm(v, axis=1)
        acc = np.linalg.norm(np.diff(v, axis=0), axis=1)
        # spike = per-frame acceleration far above its local median (a smooth ramp is not a jump)
        spike = 0.0
        for i in range(len(acc)):
            lo, hi = max(0, i - 3), min(len(acc), i + 4)
            med = float(np.median(np.delete(acc[lo:hi], i - lo))) if hi - lo > 1 else 0.0
            spike = max(spike, (acc[i] - 4 * med) / 0.05)
        jump_max[cid] = float(spike)
        dots = np.clip(np.abs(np.sum(q[1:] * q[:-1], axis=1)), 0, 1)
        ang = np.degrees(2 * np.arccos(dots))
        still = (sp < 0.01) & (ang < 0.02) & (np.abs(np.diff(lens)) < 0.01)
        run, best = 0, 0
        for x in still:
            run = run + 1 if x else 0
            best = max(best, run)
        static_runs[cid] = int(best)
    chk('camera_continuity', max(jump_max.values()) < 1.0, jump_max, 'no per-frame acceleration spike > 4x local median + 0.05 m/F^2 inside a shot')
    chk('camera_never_static', max(static_runs.values()) < 6, static_runs, 'no run of >= 6 frames with camera fully still')

    # W0: camera pose relative to the hero track frame at F_end equals F_start
    def rel_pose(cid, frame):
        Fr = d[f'cam_{cid}_F']; i = int(np.where(Fr == frame)[0][0])
        j = int(np.where(F == frame)[0][0])
        Mt, o = track_frame(d, d['s_hero'][j])
        p = d[f'cam_{cid}_loc'][i].copy(); p[:2] -= o
        return Mt.T @ p, Mt.T @ q2m(d[f'cam_{cid}_quat'][i])
    p0, M0 = rel_pose(shots[0]['id'], shots[0]['F'][0])
    p1, M1 = rel_pose(shots[-1]['id'], shots[-1]['F'][1])
    dp = float(np.linalg.norm(p1 - p0))
    dang = float(np.degrees(np.arccos(np.clip((np.trace(M0.T @ M1) - 1) / 2, -1, 1))))
    chk('w0_pose_match', dp < 0.01 and dang < 0.05, {'dpos_m': dp, 'dang_deg': dang}, 'last frame camera = first frame camera (train-relative)')
    k_mast = (d['s_last'] - d['s_first']) / d['mast_pitch']
    chk('w0_scenery_phase', abs(k_mast - round(k_mast)) < 1e-6, float(k_mast), 'masts/slabs repeat at the W0 camera')

    # 7. events inside their beats
    def frac_inside(sig, f0, f1):
        dsig = np.abs(np.diff(sig))
        Fm = F[1:len(sig)]
        tot = dsig.sum()
        return float(dsig[(Fm >= f0) & (Fm <= f1)].sum() / tot) if tot > 0 else 0.0
    shot = {s['id']: s['F'] for s in shots}
    th_h = d['theta'][hk]
    half = int(np.argmax(F >= cfg['track']['curve_exit_F']))
    f_in = frac_inside(th_h[:half], *shot['C05'])
    f_out = frac_inside(np.concatenate([np.zeros(half), th_h[half:]]), *shot['C08'])
    chk('tilt_in_key_shot', f_in >= 0.70, f_in, '>= 70 % of the tilt-in motion happens inside C05')
    chk('tilt_out_in_C08', f_out >= 0.85, f_out, '>= 85 % of the tilt-out motion happens inside C08')
    ex = cfg['explode']
    chk('explode_inside_C03', shot['C03'][0] <= ex['rotate_start_F'] and ex['done_F'] <= shot['C03'][1] - 10,
        [ex['rotate_start_F'], ex['done_F']], 'iso rotate + explode inside C03 with >= 10F hold')

    # 8. cabin drink reads: lean grows in C04, reduced in C07
    res = np.degrees(d['resid'])
    r4 = float(res[(F >= shot['C04'][0]) & (F <= shot['C04'][1])].max())
    r7 = float(res[(F >= shot['C07'][0]) & (F <= shot['C07'][1])].mean())
    chk('drink_lean_C04', r4 >= 2.5, r4, 'max residual in C04 >= 2.5 deg')
    chk('drink_reduced_C07', r7 <= 0.6 * r4, r7, 'mean residual in C07 <= 60 % of C04 max')

    # 9. speed cap
    vmax = cfg['speed']['v_max_kmh'] / 3.6
    chk('speed_cap', float(d['speed'].max()) <= vmax + 1e-6, float(d['speed'].max()), '<= v_max')

    ok = all(v == 'PASS' for v in R.values())
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    json.dump({'gate': 'G3', 'result': 'PASS' if ok else 'FAIL', 'PASS': R, 'values': V}, open(a.out, 'w'), indent=2)
    for k_, v_ in R.items():
        print(f'{v_:5s} {k_:24s} {V[k_]["value"]}')
    print('G3', 'PASS' if ok else 'FAIL')
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
