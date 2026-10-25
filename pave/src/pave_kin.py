"""PAVE 스크류(오거) 반송 기구학 — 해석적 베이크 + 독립 검증 프로토타입.

사실성이 걸린 것(감김 방향 -> 반송 방향, 날개 위상, 사건 시각)은 해석적으로 정확히 풀고,
반죽 높이는 사건 F에 맞춘 설계 포락선으로 둔다(덩어리로 밀리는 아스콘은 1D 유체 모델과 맞지 않음).

산출: bake/pave_<variant>_bake.npz(x, h, theta), bake/stones_<variant>.pc2(Mesh Cache용), bake/bake_qc.json
좌표: x = 오거 축(+는 진행방향 기준 오른쪽), y = 진행 반대방향(+는 스크리드 쪽), z = 바닥(기층) 위 높이.
시간: t = (F-1)/fps, F = 0..frames+1 (모션블러용 앞뒤 1F 포함).
"""
import json, struct, sys, pathlib
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent

def load(path=HERE / 'rig_config.json'):
    return json.loads(pathlib.Path(path).read_text(encoding='utf-8'))

def convey_dir(hand, omega_sign):
    """나사(+x축, hand=+1 오른나사)가 omega_sign 방향으로 돌 때 재료의 축방향 이동 부호.
    날개면 x = hand*p*phi/2pi 가 회전하면 고정 공간각에서 날개 위치가 -hand*sign(w)*p 만큼 진행한다."""
    return -hand * omega_sign

def velocity_field(c, x, variant):
    """구역별 반송속도. 기어박스 밑(날개 없음)은 이웃 구역 속도가 x=0에서 0으로 선형 감쇠(밀려 들어감/빠져나감)."""
    a = c['auger']; zones = {z['name']: z for z in c['zones']}
    rev = zones['FORWARD'] if c['variants'][variant]['reverse_zone'] == 'forward' else zones['REVERSE']
    v = np.zeros_like(x, dtype=float); ax = np.abs(x); gb = a['gearbox_half']
    for side, key in ((+1, 'right'), (-1, 'left')):
        on = (x >= 0) if side > 0 else (x < 0)
        sp = a['pitch'] * a[f'rps_{key}'] * a['fill_efficiency']
        zv = lambda z: convey_dir(z[f'hand_{key}'], a[f'omega_sign_{key}']) * sp
        v = np.where(on & (ax < gb), zv(rev) * ax / gb, v)
        v = np.where(on & (ax >= gb) & (ax < a['reverse_outer']), zv(rev), v)
        v = np.where(on & (ax >= a['reverse_outer']), zv(zones['FORWARD']), v)
    return v

def check_intent(c):
    out = {}
    for z in c['zones']:
        if z['intent'] == 'none':
            continue
        dr = convey_dir(z['hand_right'], c['auger']['omega_sign_right'])
        dl = convey_dir(z['hand_left'], c['auger']['omega_sign_left'])
        want_r, want_l = (1, -1) if z['intent'] == 'outward' else (-1, 1)
        out[z['name']] = bool(dr == want_r and dl == want_l)
    return out

def smoothstep(u):
    u = np.clip(u, 0, 1); return u * u * (3 - 2 * u)

def gap_depth(c, variant, F):
    e = c['events']; kind = c['variants'][variant]['envelope']
    if kind == 'steady':
        return 0.0
    if kind == 'gap_forms':
        return float(smoothstep((F - e['B_gap_start_F']) / (e['B_gap_full_F'] - e['B_gap_start_F'])))
    # gap_fills: 기어박스 구간 평균 충전율이 AB_fill_90_F 에서 정확히 0.9가 되도록 구간을 역산
    span = (e['AB_fill_90_F'] - e['AB_fill_start_F']) / _u_at_fill90(c)
    return float(1 - smoothstep((F - e['AB_fill_start_F']) / span))

def _u_at_fill90(c):
    a, hd = c['auger'], c['head']
    xs = np.linspace(-a['gearbox_half'], a['gearbox_half'], 2001)
    d90 = 0.1 / np.exp(-(xs / hd['gap_sigma']) ** 2).mean()        # 평균 충전 0.9 에 필요한 남은 틈 깊이
    lo, hi = 0.0, 1.0
    for _ in range(60):                                               # 1 - smoothstep(u) = d90 을 이분법으로 푼다
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if 1 - smoothstep(mid) > d90 else (lo, mid)
    return 0.5 * (lo + hi)

def head(c, x, F, theta_l, theta_r, variant):
    hd, a = c['head'], c['auger']
    th = np.where(x >= 0, theta_r[F], theta_l[F])
    ripple = 1 + hd['ripple'] * np.sin(th - 2 * np.pi * x / a['pitch'])   # 날개 위상에 묶인 물결
    g = 1 - gap_depth(c, variant, F) * np.exp(-(x / hd['gap_sigma']) ** 2)
    return hd['target'] * ripple * g

def particles(c, x_grid, H, variant, theta_l, theta_r):
    p, a, f = c['particles'], c['auger'], c['feed']
    rng = np.random.default_rng(p['seed']); fps = c['fps']; W = a['half_width']
    n = p['n_mix'] + p['n_coarse']; coarse = np.arange(n) >= p['n_mix']
    def spawn(k):
        s = np.sign(rng.uniform(-1, 1, k)); s[s == 0] = 1
        return s * rng.uniform(f['conveyor_inner'], f['conveyor_outer'], k)
    px = rng.uniform(-W * 0.95, W * 0.95, n); py = rng.uniform(*p['y_band'], n)
    depth = rng.uniform(0, 1, n); life = rng.uniform(*p['life_s'], n) * rng.uniform(0, 1, n)
    frames = H.shape[0]; P = np.empty((frames, n, 3), np.float32)
    zone_dx = {'REV_R': [], 'FWD_R': [], 'REV_L': [], 'FWD_L': []}
    ro, gb = a['reverse_outer'], a['gearbox_half']; hb = a['gearbox_housing']; pen = 0
    for F in range(frames):
        v = velocity_field(c, px, variant)
        streak = np.zeros(n, bool)
        if c['variants'][variant]['envelope'] == 'gap_forms' and F >= c['events']['B_gap_start_F']:
            streak = coarse & (np.abs(px) < f['conveyor_inner'])      # 굵은 골재가 빈 가운데로 굴러듦
            v = np.where(streak, -np.sign(px) * 0.08 * (np.abs(px) > 0.03), v)
        dx = v / fps; px_new = np.clip(px + dx, -W * 0.98, W * 0.98)
        for key, m in (('REV_R', (px > gb) & (px < ro)), ('FWD_R', px >= ro),
                       ('REV_L', (px < -gb) & (px > -ro)), ('FWD_L', px <= -ro)):
            zone_dx[key].extend(dx[m & ~streak].tolist())
        px = px_new
        life -= 1 / fps
        out = (life <= 0) & ~streak                                     # 스크리드 밑으로 빠짐 -> 컨베이어에서 재투입
        py = np.where(out, py + p['drift_v'] / fps, py)
        gone = py > p['despawn_y']
        k = int(gone.sum())
        if k:
            px[gone] = spawn(k); py[gone] = p['spawn_y']
            life[gone] = rng.uniform(*p['life_s'], k)
        py = np.where(~out & ~gone, np.clip(py, p['spawn_y'], p['y_band'][1]) +
                      (py < p['y_band'][0]) * p['drift_v'] / fps, py)
        hp = np.interp(px, x_grid, H[F])
        th = np.where(px >= 0, theta_r[F], theta_l[F])
        lift = p['lift'] * np.maximum(0, np.sin(th - 2 * np.pi * px / a['pitch']))
        rad = np.where(coarse, p['r_coarse'], p['r_mix'])
        z = np.where(streak & (np.abs(px) < gb + 0.05), rad, np.maximum(hp * (1 - 0.8 * depth) + lift, rad))
        under = (np.abs(px) < hb['half_x'] + rad) & (np.abs(py) < hb['half_y'] + rad)
        pen += int((under & (z + rad > hb['bottom_z'])).sum())                # 클램프 전 겹침 수(참고값)
        z = np.where(under, np.minimum(z, hb['bottom_z'] - rad - 0.001), z)   # 기어박스 하우징 밑으로만 지나감
        P[F, :, 0], P[F, :, 1], P[F, :, 2] = px, py, z
    zone_sign = {k: float(np.sign(np.mean(v))) if v else 0.0 for k, v in zone_dx.items()}
    return P, coarse, zone_sign, pen

def write_pc2(path, P, start_frame=0):
    frames, n, _ = P.shape
    with open(path, 'wb') as fh:
        fh.write(b'POINTCACHE2\0')
        fh.write(struct.pack('<iiffi', 1, n, float(start_frame), 1.0, frames))
        fh.write(P.astype('<f4').tobytes())

def main(out_dir=HERE / 'bake'):
    c = load(); out_dir = pathlib.Path(out_dir); out_dir.mkdir(exist_ok=True)
    fps, a = c['fps'], c['auger']; frames = c['frames'] + 2
    t = (np.arange(frames) - 1) / fps                                   # F0은 t<0 선형 외삽
    theta_l = 2 * np.pi * a['rps_left'] * a['omega_sign_left'] * t
    theta_r = 2 * np.pi * a['rps_right'] * a['omega_sign_right'] * t
    x = np.linspace(-a['half_width'], a['half_width'], 321)
    centre = np.abs(x) < a['gearbox_half']
    qc = {'intent': check_intent(c), 'events': c['events']}
    want = {'A_real': {'REV_R': -1, 'FWD_R': 1, 'REV_L': 1, 'FWD_L': -1},
            'B_noRev': {'REV_R': 1, 'FWD_R': 1, 'REV_L': -1, 'FWD_L': -1},
            'AB_fill': {'REV_R': -1, 'FWD_R': 1, 'REV_L': 1, 'FWD_L': -1}}
    ok = True
    for var in c['variants']:
        H = np.stack([head(c, x, F, theta_l, theta_r, var) for F in range(frames)])
        fill = H[:, centre].mean(1) / c['head']['target']
        P, coarse, zs, pen = particles(c, x, H, var, theta_l, theta_r)
        write_pc2(out_dir / f'stones_{var}.pc2', P)
        np.savez_compressed(out_dir / f'pave_{var}_bake.npz', x=x, h=H, coarse=coarse,
                            theta_l=theta_l, theta_r=theta_r)
        r = {'centre_fill_end': round(float(fill[-1]), 3), 'centre_fill_min': round(float(fill.min()), 3),
             'particle_zone_dir': zs, 'zone_dir_ok': zs == want[var],
             'z_range_m': [round(float(P[..., 2].min()), 3), round(float(P[..., 2].max()), 3)],
             'within_auger_top': bool(P[..., 2].max() <= a['axis_z'] + a['diameter'] / 2),
             'gearbox_clamp_events': pen}  # 실제 관통 판정은 G4 씬 BVH 검사가 한다(생성 코드 자기검증 금지)
        if var == 'AB_fill':
            hit = np.nonzero((np.arange(frames) > c['events']['AB_fill_start_F']) & (fill >= 0.9))[0]
            r['fill_90_F'] = int(hit[0]) if len(hit) else -1
            r['fill_90_ok'] = abs(r['fill_90_F'] - c['events']['AB_fill_90_F']) <= 1
        if var == 'B_noRev':
            r['starved_ok'] = bool(fill[c['events']['B_gap_full_F']] < 0.2)
        ok &= r['zone_dir_ok'] and r['within_auger_top'] and r.get('fill_90_ok', True) and r.get('starved_ok', True)
        qc[var] = r
    qc['ALL_PASS'] = bool(ok and all(qc['intent'].values()))
    (out_dir / 'bake_qc.json').write_text(json.dumps(qc, indent=2, ensure_ascii=False))
    print(json.dumps(qc, indent=2, ensure_ascii=False))
    return 0 if qc['ALL_PASS'] else 1

if __name__ == '__main__':
    sys.exit(main())
