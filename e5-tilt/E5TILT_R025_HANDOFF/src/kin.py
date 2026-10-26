"""E5 TILT R025 - kinematics solver and bake (numpy only, no bpy).

Reads rig_config.json + cameras.json, writes:
  tilt_bake.npz            the only motion input of build.py
  ../evidence/geometry_qc.json  events (frame numbers) used by beats, cameras and SFX

Time convention: t = (F - 1) / fps. Bake covers F0 .. F(end+1); t<0 uses constant speed (linear extrapolation).
Run:  python kin.py [--config rig_config.json] [--cameras cameras.json] [--out tilt_bake.npz]
"""
import json, os, sys, argparse
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


def args_after_dashdash():
    """args after '--'; inside the Blender app without '--' there are no script args."""
    a = sys.argv
    if '--' in a:
        return a[a.index('--') + 1:]
    if os.path.basename(a[0]).lower().startswith('blender'):
        return []
    return a[1:]


# ---------------------------------------------------------------- math helpers
def smoothstep(x):
    x = np.clip(x, 0.0, 1.0)
    return x * x * (3 - 2 * x)


def keyed_smooth(t, keys):
    """piecewise smoothstep through (t, v) keys, held flat outside."""
    t = np.asarray(t, float)
    k = np.asarray(keys, float)
    out = np.full_like(t, k[0, 1])
    for (t0, v0), (t1, v1) in zip(k[:-1], k[1:]):
        m = (t >= t0) & (t <= t1)
        out[m] = v0 + (v1 - v0) * smoothstep((t[m] - t0) / max(t1 - t0, 1e-9))
    out[t > k[-1, 0]] = k[-1, 1]
    return out


def keyed_linear(F, keys):
    k = np.asarray(keys, float)
    return np.interp(F, k[:, 0], k[:, 1])


def mat_to_quat(M):
    """3x3 rotation -> (w,x,y,z)"""
    m = M
    tr = m[0, 0] + m[1, 1] + m[2, 2]
    if tr > 0:
        s = np.sqrt(tr + 1.0) * 2
        w = 0.25 * s; x = (m[2, 1] - m[1, 2]) / s; y = (m[0, 2] - m[2, 0]) / s; z = (m[1, 0] - m[0, 1]) / s
    elif m[0, 0] > m[1, 1] and m[0, 0] > m[2, 2]:
        s = np.sqrt(1.0 + m[0, 0] - m[1, 1] - m[2, 2]) * 2
        w = (m[2, 1] - m[1, 2]) / s; x = 0.25 * s; y = (m[0, 1] + m[1, 0]) / s; z = (m[0, 2] + m[2, 0]) / s
    elif m[1, 1] > m[2, 2]:
        s = np.sqrt(1.0 + m[1, 1] - m[0, 0] - m[2, 2]) * 2
        w = (m[0, 2] - m[2, 0]) / s; x = (m[0, 1] + m[1, 0]) / s; y = 0.25 * s; z = (m[1, 2] + m[2, 1]) / s
    else:
        s = np.sqrt(1.0 + m[2, 2] - m[0, 0] - m[1, 1]) * 2
        w = (m[1, 0] - m[0, 1]) / s; x = (m[0, 2] + m[2, 0]) / s; y = (m[1, 2] + m[2, 1]) / s; z = 0.25 * s
    q = np.array([w, x, y, z])
    return q / np.linalg.norm(q)


def quat_track(Ms):
    """list of 3x3 -> (n,4) quats with sign continuity"""
    q = np.array([mat_to_quat(M) for M in Ms])
    for i in range(1, len(q)):
        if np.dot(q[i], q[i - 1]) < 0:
            q[i] = -q[i]
    return q


def rot_y(b):
    c, s = np.cos(b), np.sin(b)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])


def rot_z(a):
    c, s = np.cos(a), np.sin(a)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


def catmull_rom(tk, pk, t):
    """non-uniform Catmull-Rom (Hermite), end tangents 0. pk: (m,d). t: (n,) -> (n,d)"""
    tk = np.asarray(tk, float); pk = np.asarray(pk, float)
    m = len(tk)
    if m == 1:
        return np.repeat(pk[:1], len(t), 0)
    tan = np.zeros_like(pk)
    for i in range(1, m - 1):
        tan[i] = (pk[i + 1] - pk[i - 1]) / (tk[i + 1] - tk[i - 1])
    out = np.empty((len(t), pk.shape[1]))
    for j, tt in enumerate(t):
        if tt <= tk[0]:
            out[j] = pk[0]; continue
        if tt >= tk[-1]:
            out[j] = pk[-1]; continue
        i = np.searchsorted(tk, tt) - 1
        h = tk[i + 1] - tk[i]; u = (tt - tk[i]) / h
        h00 = 2 * u**3 - 3 * u**2 + 1; h10 = u**3 - 2 * u**2 + u
        h01 = -2 * u**3 + 3 * u**2; h11 = u**3 - u**2
        out[j] = h00 * pk[i] + h10 * h * tan[i] + h01 * pk[i + 1] + h11 * h * tan[i + 1]
    return out


def look_at(cam, tgt, up):
    f = tgt - cam; f /= np.linalg.norm(f)
    x = np.cross(f, up); x /= np.linalg.norm(x)
    y = np.cross(x, f)
    return np.column_stack([x, y, -f])


# ---------------------------------------------------------------- path
class TrackPath:
    def __init__(self, cfg, s_entry, s_exit):
        tr = cfg['track']
        self.R = tr['R_visual']; self.L = tr['spiral_len']
        self.sign = 1.0 if tr['curve_dir'] == 'left' else -1.0
        self.s_e, self.s_x = s_entry, s_exit
        self.z = tr['rail_top_z']
        s = np.arange(tr['s_min'], tr['s_max'] + tr['ds'] / 2, tr['ds'])
        c = self.curv01(s)
        kappa = self.sign * c / self.R
        psi = np.concatenate([[0.0], np.cumsum(0.5 * (kappa[1:] + kappa[:-1]) * np.diff(s))])
        psi -= np.interp(0.0, s, psi)              # heading 0 (+Y) at s = 0
        tx, ty = -np.sin(psi), np.cos(psi)
        x = np.concatenate([[0.0], np.cumsum(0.5 * (tx[1:] + tx[:-1]) * np.diff(s))])
        y = np.concatenate([[0.0], np.cumsum(0.5 * (ty[1:] + ty[:-1]) * np.diff(s))])
        x -= np.interp(0.0, s, x); y -= np.interp(0.0, s, y)
        self.s, self.psi, self.x, self.y = s, psi, x, y

    def curv01(self, s):
        s = np.asarray(s, float)
        a = np.clip((s - self.s_e) / self.L, 0, 1)
        b = np.clip((s - self.s_x) / self.L, 0, 1)
        return a - b

    def P(self, s):
        s = np.asarray(s, float)
        return np.stack([np.interp(s, self.s, self.x), np.interp(s, self.s, self.y),
                         np.full_like(s, self.z)], -1)

    def heading(self, s):
        return np.interp(s, self.s, self.psi)

    def frame(self, s):
        p = self.heading(s)
        r = np.array([np.cos(p), np.sin(p), 0.0]); f = np.array([-np.sin(p), np.cos(p), 0.0])
        return np.column_stack([r, f, [0, 0, 1.0]])


# ---------------------------------------------------------------- solver
def solve(cfg, cams):
    sp = cfg['spec']; fps = sp['fps']
    F = np.arange(sp['frame_start'] - sp['bake_pad'], sp['frame_end'] + sp['bake_pad'] + 1).astype(float)
    tF = (F - 1) / fps
    n = len(F)

    # ---- master speed curve -> s_hero(t) on a fine grid (t<0: constant v)
    v = cfg['speed']['v_max_kmh'] / 3.6
    dt = cfg['speed']['dt_fine']
    t_lo = tF[0] - 4.0
    tf = np.arange(t_lo, tF[-1] + 0.5, dt)
    fac = np.where(tf < 0, cfg['speed']['keys'][0][1], keyed_smooth(tf, cfg['speed']['keys']))
    vf = v * fac
    sf = np.concatenate([[0.0], np.cumsum(0.5 * (vf[1:] + vf[:-1]) * dt)])
    sf -= np.interp(0.0, tf, sf)                  # s_hero(0) = 0
    s_hero_t = lambda t: np.interp(t, tf, sf)
    v_t = lambda t: np.interp(t, tf, vf)

    # ---- curve placement by event inversion (hero car centre)
    tr = cfg['track']
    t_entry = (tr['curve_entry_F'] - 1) / fps
    t_exit = (tr['curve_exit_F'] - 1) / fps
    s_entry, s_exit = float(s_hero_t(t_entry)), float(s_hero_t(t_exit))
    path = TrackPath(cfg, s_entry, s_exit)

    # ---- consist
    trn = cfg['train']; nc = trn['n_cars']
    lens_ = [trn['end_car_len'] if k in (0, nc - 1) else trn['mid_car_len'] for k in range(nc)]
    off = [0.0]
    for k in range(1, nc):
        off.append(off[-1] + (lens_[k - 1] + lens_[k]) / 2 + trn['car_gap'])
    off = np.array(off)
    hb = trn['bogie_half_spacing']
    zb = trn['body_bottom_above_rail']

    # ---- tilt per car: command = theta_max * c(s_car(t - delay)), first-order lag on the fine grid
    tl = cfg['tilt']; thmax = np.radians(tl['theta_max_deg'])
    alpha = 1 - np.exp(-dt / tl['tau_s'])
    theta_cars = np.zeros((nc, n))
    c_cars = np.zeros((nc, n))
    for k in range(nc):
        sc_delay = np.interp(tf - tl['delay_s'], tf, sf) - off[k]
        cmd = thmax * path.curv01(sc_delay)
        th = np.zeros_like(cmd)
        for i in range(1, len(cmd)):
            th[i] = th[i - 1] + alpha * (cmd[i] - th[i - 1])
        theta_cars[k] = np.interp(tF, tf, th)
        c_cars[k] = path.curv01(s_hero_t(tF) - off[k])

    # ---- bodies, ghost, bogies
    body_loc = np.zeros((nc, n, 3)); body_M = np.zeros((nc, n, 3, 3)); yaw_M = np.zeros((nc, n, 3, 3))
    bog_loc = np.zeros((nc, 2, n, 3)); bog_M = np.zeros((nc, 2, n, 3, 3)); bog_s = np.zeros((nc, 2, n))
    sh = s_hero_t(tF)
    up = np.array([0, 0, 1.0])
    for k in range(nc):
        sc = sh - off[k]
        Pf = path.P(sc + hb); Pr = path.P(sc - hb)
        for i in range(n):
            fb = Pf[i] - Pr[i]; fb /= np.linalg.norm(fb)
            rb = np.cross(fb, up); rb /= np.linalg.norm(rb)
            Ry = np.column_stack([rb, fb, up])
            yaw_M[k, i] = Ry
            body_M[k, i] = Ry @ rot_y(-theta_cars[k, i])        # +theta = right side up = lean to the left (inner)
            body_loc[k, i] = 0.5 * (Pf[i] + Pr[i]) + up * zb
            for j, sgn in enumerate((+1, -1)):                    # j=0 front bogie, j=1 rear bogie
                sb = sc[i] + sgn * hb
                bog_s[k, j, i] = sb
                bog_loc[k, j, i] = path.P(sb)
                bog_M[k, j, i] = path.frame(sb)

    wheel_r = cfg['bogie']['wheel_r']
    wheel_angle = -bog_s / wheel_r                                # rotation about bogie local +X

    # ---- hero air springs (rear bogie of hero car)
    hk = trn['hero_car'] - 1
    sl = cfg['spring']['s_lat'] / 2
    ftop = cfg['bogie']['frame_top_above_rail']
    h = {}
    for side, x in (('L', -sl), ('R', +sl)):
        top = np.einsum('nij,j->ni', body_M[hk], np.array([x, -hb, 0.0])) + body_loc[hk]
        base = np.einsum('nij,j->ni', bog_M[hk, 1], np.array([x, 0.0, ftop])) + bog_loc[hk, 1]
        h[side] = top[:, 2] - base[:, 2]
    spr = cfg['spring']
    stroke = {k_: (h[k_] - spr['h_min']) / (spr['h_max'] - spr['h_min']) for k_ in h}

    # ---- ISO set: yaw + explode (F-keyed)
    ex = cfg['explode']
    iso_yaw = np.radians(ex['rotate_yaw_deg']) * smoothstep((F - ex['rotate_start_F']) / (ex['rotate_done_F'] - ex['rotate_start_F']))
    explode = smoothstep((F - ex['start_F']) / (ex['done_F'] - ex['start_F']))
    iso_M = np.array([rot_z(a) for a in iso_yaw])

    # ---- xray / ghost
    xr = cfg['xray']
    skirt_xray = keyed_linear(F, xr['skirt_keys_F'])
    ghost_vis = keyed_linear(F, xr['ghost_keys_F'])

    # ---- cabin drink: residual lean in the body frame (+ = right/outer side higher)
    cb = cfg['cabin']
    resid = np.radians(cb['residual_before_deg']) * c_cars[hk] - theta_cars[hk]
    liquid_key = np.tan(resid) / np.tan(np.radians(cb['tilt_key_max_deg']))

    # ---- anchors and cameras
    def anchor_frame(a, t_arr, shot_F):
        typ = a['type']; dy = a.get('dy', 0.0)
        Ms, Os = [], []
        if typ == 'hero':
            ss = s_hero_t(t_arr) + dy
            for s_ in ss:
                Ms.append(path.frame(s_)); Os.append(path.P(s_))
        elif typ == 'hero_body':
            for tt in t_arr:
                i = np.clip(np.searchsorted(tF, tt), 0, n - 1)
                Ms.append(body_M[hk, i]); Os.append(body_loc[hk, i])
        elif typ == 'world':
            s0 = float(s_hero_t((a['ref_F'] - 1) / fps)) + dy
            Ms = [path.frame(s0)] * len(t_arr); Os = [path.P(s0)] * len(t_arr)
        elif typ == 'ramp':
            t0, t1 = a['t0'], a['t1']
            w = lambda tt: smoothstep((tt - t0) / (t1 - t0))
            ss = []
            for tt in t_arr:
                if tt >= t1:
                    D = 0.0
                else:
                    g = np.linspace(tt, t1, 400)
                    D = np.trapz((1 - w(g)) * v_t(g), g)
                ss.append(float(s_hero_t(tt)) + dy + D)
            for s_ in ss:
                Ms.append(path.frame(s_)); Os.append(path.P(s_))
        elif typ == 'iso':
            o = np.array(cfg['iso']['origin'], float)
            Ms = [np.eye(3)] * len(t_arr); Os = [o] * len(t_arr)
        elif typ == 'w0':
            ds = anchor_s_offset[a['match']]
            t_end = (shot_F[1] - 1) / fps
            s0 = float(s_hero_t(t_end)) + ds
            Ms = [path.frame(s0)] * len(t_arr); Os = [path.P(s0)] * len(t_arr)
        else:
            raise ValueError(typ)
        return np.array(Ms), np.array(Os)

    # anchor offset of every shot's first frame relative to s_hero (used by w0)
    anchor_s_offset = {}
    for c in cams['shots']:
        a = c['cam_anchor']
        if a['type'] == 'ramp':
            t0 = (c['F'][0] - 1) / fps
            g = np.linspace(t0, a['t1'], 2000)
            w = smoothstep((g - a['t0']) / (a['t1'] - a['t0']))
            anchor_s_offset[c['id']] = a.get('dy', 0.0) + float(np.trapz((1 - w) * v_t(g), g))
        elif a['type'] == 'hero':
            anchor_s_offset[c['id']] = a.get('dy', 0.0)

    cam_out = {}
    for c in cams['shots']:
        f0, f1 = c['F']
        Fr = np.arange(max(f0 - 2, F[0]), min(f1 + 2, F[-1]) + 1)
        tt = (Fr - 1) / fps
        keys = c['keys']
        tk = np.array([(k_['F'] - 1) / fps for k_ in keys])
        cl = catmull_rom(tk, [k_['cam'] for k_ in keys], tt)
        tl_ = catmull_rom(tk, [k_['tgt'] for k_ in keys], tt)
        lens = catmull_rom(tk, [[k_['lens']] for k_ in keys], tt)[:, 0]
        fst = catmull_rom(tk, [[k_['fstop']] for k_ in keys], tt)[:, 0]
        Mc, Oc = anchor_frame(c['cam_anchor'], tt, c['F'])
        Mt, Ot = anchor_frame(c['tgt_anchor'], tt, c['F'])
        cw = np.einsum('nij,nj->ni', Mc, cl) + Oc
        tw = np.einsum('nij,nj->ni', Mt, tl_) + Ot
        Ms = []
        for i in range(len(tt)):
            upv = Mc[i][:, 2] if c['cam_anchor']['type'] == 'hero_body' else up
            Ms.append(look_at(cw[i], tw[i], upv))
        cam_out[c['id']] = dict(F=Fr, loc=cw, quat=quat_track(Ms), lens=lens, fstop=fst,
                                focus=np.linalg.norm(tw - cw, axis=1), tgt=tw)

    # ---- slab / mast phase so the W0 frame repeats the F1 background
    first, last = cams['shots'][0], cams['shots'][-1]
    s_first = float(s_hero_t((first['F'][0] - 1) / fps)) + anchor_s_offset[first['id']]
    s_last = float(s_hero_t((last['F'][1] - 1) / fps)) + anchor_s_offset[first['id']]
    total = s_last - s_first
    n_slab = int(10 * round(total / (10 * (tr['slab_len'] + tr['slab_gap']))))
    slab_pitch = total / n_slab
    mast_pitch = 10 * slab_pitch
    phase0 = s_first + 21.0                                       # a mast 21 m ahead of the W0 camera

    # ---- events (hero car)
    th = np.degrees(theta_cars[hk])
    def first_F(mask):
        idx = np.where(mask)[0]
        return int(F[idx[0]]) if len(idx) else None
    i_exit = np.searchsorted(F, tr['curve_exit_F'])
    ev = {
        'curve_entry_F': tr['curve_entry_F'],
        'curve_full_F': first_F(c_cars[hk] >= 0.999),
        'tilt_start_F': first_F(th > tl['start_threshold_deg']),
        'tilt_reach_F': first_F(th >= tl['reach_threshold_deg']),
        'curve_exit_F': tr['curve_exit_F'],
        'tilt_return_F': (lambda m: int(F[i_exit + m[0]]) if len(m) else None)(np.where(th[i_exit:] < tl['start_threshold_deg'])[0]),
        'theta_max_deg_baked': float(th.max()),
        'spring_dh_max_m': float(np.max(np.abs(h['R'] - h['L']))),
        'iso_rotate_F': [ex['rotate_start_F'], ex['rotate_done_F']],
        'explode_F': [ex['start_F'], ex['done_F']],
        'speed_ramp_down_t': cfg['speed']['keys'][1][0:1] + cfg['speed']['keys'][2][0:1],
        'speed_ramp_up_t': cfg['speed']['keys'][3][0:1] + cfg['speed']['keys'][4][0:1],
        'cuts_F': [c['F'][0] for c in cams['shots'][1:]],
        'shots': {c['id']: c['F'] for c in cams['shots']},
        'skirt_xray_on_F': [k_[0] for k_ in cfg['xray']['skirt_keys_F']],
        'resid_max_deg': float(np.degrees(resid.max())),
        'resid_C07_deg': float(np.degrees(resid[np.searchsorted(F, 550)])),
    }
    # air flow sign for overlays: +1 filling, -1 venting
    dhL = np.gradient(h['L']); dhR = np.gradient(h['R'])

    out = dict(
        F=F, t=tF, s_hero=sh, speed=v_t(tF), car_off=off, car_len=np.array(lens_),
        theta=theta_cars, curv=c_cars,
        body_loc=body_loc, body_quat=np.array([quat_track(body_M[k]) for k in range(nc)]),
        ghost_quat=quat_track(yaw_M[hk]), ghost_loc=body_loc[hk],
        bog_loc=bog_loc, bog_quat=np.array([[quat_track(bog_M[k, j]) for j in range(2)] for k in range(nc)]),
        wheel_angle=wheel_angle,
        h_L=h['L'], h_R=h['R'], stroke_L=stroke['L'], stroke_R=stroke['R'], dh_L=dhL, dh_R=dhR,
        iso_quat=quat_track(iso_M), explode=explode,
        skirt_xray=skirt_xray, ghost_vis=ghost_vis,
        resid=resid, liquid_key=liquid_key,
        path_s=path.s[::10], path_x=path.x[::10], path_y=path.y[::10], path_psi=path.psi[::10],
        s_entry=s_entry, s_exit=s_exit, slab_pitch=slab_pitch, mast_pitch=mast_pitch, phase0=phase0,
        s_first=s_first, s_last=s_last,
        body_M_hero=body_M[hk], yaw_M_hero=yaw_M[hk],
    )
    for cid, d in cam_out.items():
        for kk, vv in d.items():
            out[f'cam_{cid}_{kk}'] = vv
    out['cam_ids'] = np.array([c['id'] for c in cams['shots']])
    return out, ev


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--config', default=os.path.join(HERE, 'rig_config.json'))
    ap.add_argument('--cameras', default=os.path.join(HERE, 'cameras.json'))
    ap.add_argument('--out', default=os.path.join(HERE, 'tilt_bake.npz'))
    ap.add_argument('--evidence', default=os.path.join(HERE, '..', 'evidence'))
    a = ap.parse_args(args_after_dashdash())
    cfg = json.load(open(a.config, encoding='utf-8'))
    cams = json.load(open(a.cameras, encoding='utf-8'))
    out, ev = solve(cfg, cams)
    np.savez_compressed(a.out, **out)
    os.makedirs(a.evidence, exist_ok=True)
    json.dump({'events': ev}, open(os.path.join(a.evidence, 'geometry_qc.json'), 'w'), indent=2)
    print('BAKE OK', a.out)
    print(json.dumps(ev, indent=1))


if __name__ == '__main__':
    main()
