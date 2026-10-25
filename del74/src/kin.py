"""DEL74 해석적 운동 풀이. 수치는 rig_config.json에서만 읽는다(하드코딩 금지).
모든 함수는 numpy 벡터 입력(프레임 배열)을 받고 같은 길이 배열을 돌려준다.
시간 규약: t = (F - 1) / fps. 프레임 범위 양끝 포함."""
import json, math
import numpy as np

def load_cfg(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)

def V(cfg, *keys):
    """cfg['a']['b']['v'] 접근. 값 노드는 {'v':..,'s':..} 형태."""
    node = cfg
    for k in keys:
        node = node[k]
    return node['v'] if isinstance(node, dict) and 'v' in node else node

def t_of(F, fps):
    return (np.asarray(F, float) - 1.0) / fps

def smoothstep(x):
    x = np.clip(x, 0.0, 1.0)
    return x * x * (3.0 - 2.0 * x)

def ease_out(x):
    x = np.clip(x, 0.0, 1.0)
    return 1.0 - (1.0 - x) ** 2

def ease_in(x):
    x = np.clip(x, 0.0, 1.0)
    return x * x

# ---------------- 마스터 속도 곡선 ----------------
def master_velocity(t, cfg, v0):
    """F1 v0 → decel(F100–187) → 0 → launch(F894) 등가속 a1 → F1046 이후 smoothstep으로 v0(F1324) → 유지."""
    fps = cfg['fps']
    dF0, dF1 = V(cfg, 'master_speed', 'decel_frames')
    Fl = V(cfg, 'master_speed', 'launch_frame')
    F2 = V(cfg, 'master_speed', 'accel2_end_frame')
    rel = V(cfg, 'coupler', 'release_frames_target')
    S1 = V(cfg, 'coupler', 'slack_1_target')
    t_d0, t_d1 = t_of(dF0, fps), t_of(dF1, fps)
    # 첫 운동 프레임이 정확히 Fl·rel[n]이 되도록 가속 시작과 해소 목표를 1F 앞당긴다(F-1에서 변위 0, F에서 양수)
    t_l, t_r1, t_r4, t_2 = t_of(Fl - 1, fps), t_of(rel[0] - 1, fps), t_of(rel[-1] - 1, fps), t_of(F2, fps)
    a1 = 2.0 * S1 / (t_r1 - t_l) ** 2                 # 첫 유격 해소 프레임 역산
    v1 = a1 * (t_r4 - t_l)                              # 마지막 유격 해소 시점 속도
    t = np.asarray(t, float)
    v = np.empty_like(t)
    m = t < t_d0;                 v[m] = v0
    m = (t >= t_d0) & (t < t_d1); v[m] = v0 * (1.0 - smoothstep((t[m] - t_d0) / (t_d1 - t_d0)))
    m = (t >= t_d1) & (t < t_l);  v[m] = 0.0
    m = (t >= t_l) & (t < t_r4);  v[m] = a1 * (t[m] - t_l)
    m = (t >= t_r4) & (t < t_2);  v[m] = v1 + (v0 - v1) * smoothstep((t[m] - t_r4) / (t_2 - t_r4))
    m = t >= t_2;                 v[m] = v0
    return v, a1

def integrate_position(frames, cfg, v0, sub=20):
    """loco_x(F): F1에서 0. 서브스텝 사다리꼴 적분(해석 구간은 정확)."""
    fps = cfg['fps']
    frames = np.asarray(frames, float)
    x = np.zeros_like(frames)
    for i, F in enumerate(frames):
        if F == 1.0:
            x[i] = 0.0; continue
        ts = np.linspace(t_of(1, fps), t_of(F, fps), int(abs(F - 1) * sub) + 2)
        v, _ = master_velocity(ts, cfg, v0)
        x[i] = np.trapezoid(v, ts) if hasattr(np, 'trapezoid') else np.trapz(v, ts)
    return x

def solve_v0_for_loop(cfg):
    """F1417 차륜 위상 ≡ F1 (mod 2π) 가 되도록 v0 역산. 이동 거리 D(v0) = k·2πR."""
    R = V(cfg, 'wheel', 'radius'); target = V(cfg, 'master_speed', 'v0_target')
    N = cfg['total_frames']
    def D(v0): return integrate_position([N + 1], cfg, v0, sub=40)[0]
    k = max(1, round(D(target) / (2 * math.pi * R)))
    goal = k * 2 * math.pi * R
    lo, hi = target * 0.5, target * 1.5
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if D(mid) < goal: lo = mid
        else: hi = mid
    return 0.5 * (lo + hi), k

# ---------------- 크랭크 ----------------
def crank_omega(t, cfg, w_run):
    """구간별 각속도. F1–186 w_run(실세계 주행) / C03 가정: idle→체결 정지→되감기 역회전 / F394 idle→w_run 램프 → 유지."""
    fps = cfg['fps']; H = cfg['hypothetical_shaft']
    w_idle = V(cfg, 'engine', 'omega_idle')
    hc = V(cfg, 'hard_cuts')
    t_h0 = t_of(hc[0], fps)                                   # 187 가정 세계 시작
    t_e0, t_e1 = [t_of(f, fps) for f in V(H, 'crank_stop_frames')]
    t_rw0, t_rw1 = [t_of(f, fps) for f in V(H, 'rewind_frames')]
    t_c4 = t_of(hc[1], fps)                                   # 394 실세계 복귀
    t_r0, t_r1 = t_of(404, fps), t_of(470, fps)               # 램프(계획 P4 C04)
    t = np.asarray(t, float); w = np.empty_like(t)
    m = t < t_h0;                  w[m] = w_run
    m = (t >= t_h0) & (t < t_e0);  w[m] = w_idle
    m = (t >= t_e0) & (t < t_e1);  w[m] = w_idle * (1.0 - smoothstep((t[m] - t_e0) / (t_e1 - t_e0)))
    m = (t >= t_e1) & (t < t_rw0); w[m] = 0.0
    m = (t >= t_rw0) & (t < t_rw1)
    # 되감기: 종 모양 역회전(총 -1.5 회전 정도), 양끝 0
    u = (t[m] - t_rw0) / (t_rw1 - t_rw0); w[m] = -w_idle * 3.0 * np.sin(np.pi * u)
    m = (t >= t_rw1) & (t < t_c4); w[m] = 0.0
    m = (t >= t_c4) & (t < t_r0);  w[m] = w_idle
    m = (t >= t_r0) & (t < t_r1);  w[m] = w_idle + (w_run - w_idle) * smoothstep((t[m] - t_r0) / (t_r1 - t_r0))
    m = t >= t_r1;                 w[m] = w_run
    return w

def integrate_angle(frames, cfg, omega_fn, sub=20):
    fps = cfg['fps']; frames = np.asarray(frames, float); th = np.zeros_like(frames)
    for i, F in enumerate(frames):
        if F == 1.0: continue
        ts = np.linspace(t_of(1, fps), t_of(F, fps), int(abs(F - 1) * sub) + 2)
        w = omega_fn(ts)
        th[i] = np.trapezoid(w, ts) if hasattr(np, 'trapezoid') else np.trapz(w, ts)
    return th

def solve_w_run_for_loop(cfg):
    target = V(cfg, 'engine', 'omega_run_target'); N = cfg['total_frames']
    def TH(w): return integrate_angle([N + 1], cfg, lambda ts: crank_omega(ts, cfg, w), sub=40)[0]
    k = round(TH(target) / (2 * math.pi)); goal = k * 2 * math.pi
    lo, hi = target * 0.7, target * 1.3
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if TH(mid) < goal: lo = mid
        else: hi = mid
    return 0.5 * (lo + hi), k

def piston_positions(crank_theta, cfg):
    """(n, 16) 피스톤 핀 위치(뱅크 축 방향, 크랭크 중심 기준). 실린더 i: 스로 i//2, 뱅크 i%2 (0=좌 +22.5°, 1=우 −22.5°)."""
    r = V(cfg, 'engine', 'crank_radius'); l = V(cfg, 'engine', 'rod_length')
    ph = np.deg2rad(V(cfg, 'engine', 'throw_phase_deg')); half = np.deg2rad(V(cfg, 'engine', 'bank_angle_deg')) / 2
    th = np.asarray(crank_theta, float)[:, None]
    n = V(cfg, 'engine', 'cylinders'); out = np.empty((len(th), n))
    for i in range(n):
        bank = +half if i % 2 == 0 else -half
        a = th[:, 0] + ph[i // 2] - bank
        out[:, i] = r * np.cos(a) + np.sqrt(l * l - (r * np.sin(a)) ** 2)
    return out

# ---------------- 연결기 ----------------
def coupler_and_cars(frames, loco_x, cfg):
    """유격 S_n은 목표 해소 프레임에서 역산. 반환: slack_values, bunch(n_frames, n_cars), car_x_offsets(static)."""
    fps = cfg['fps']; rel = V(cfg, 'coupler', 'release_frames_target'); n = V(cfg, 'car', 'count')
    Fl = V(cfg, 'master_speed', 'launch_frame')
    frames = np.asarray(frames, float)
    xi = lambda F: np.interp(F, frames, loco_x)
    Fl = Fl - 1                                   # master_velocity와 같은 규약
    dx = [xi(f - 1) - xi(Fl) for f in rel]
    S = [dx[0]] + [dx[i] - dx[i - 1] for i in range(1, n)]
    dF0, dF1 = V(cfg, 'master_speed', 'decel_frames')
    # 유격 상태 s_n ∈ [0, S_n] (S=펴짐). F1 펴짐 → 감속 중 뭉침 → 정지 유지 → 기동 시 순차 펴짐
    s = np.zeros((len(frames), n))
    ext = np.maximum(loco_x - xi(Fl), 0.0)          # 기동 뒤 기관차 이동량
    for i in range(n):
        base = sum(S[:i])
        s[:, i] = np.clip(ext - base, 0.0, S[i])
        pre = frames < Fl
        f = frames[pre]
        s[pre, i] = np.where(f < dF0, S[i], np.where(f < dF1, S[i] * (1 - smoothstep((f - dF0) / (dF1 - dF0))), 0.0))
    bunch = np.cumsum(np.array(S)[None, :] - s, axis=1)
    L_loco = V(cfg, 'loco', 'length_over_couplers'); L_car = V(cfg, 'car', 'length_over_couplers')
    off = np.array([-(L_loco / 2 + L_car / 2 + i * L_car) for i in range(n)])
    return np.array(S), s, bunch, off

# ---------------- 카메라 ----------------
def catmull_rom(keys_F, keys_val, F):
    """Catmull-Rom, 끝점 접선 0(양끝 키 복제). keys_val (k, d)."""
    kF = np.asarray(keys_F, float); kv = np.asarray(keys_val, float)
    if kv.ndim == 1: kv = kv[:, None]
    P = np.vstack([kv[:1], kv, kv[-1:]]); T = np.concatenate([[kF[0]], kF, [kF[-1]]])
    F = np.asarray(F, float); out = np.empty((len(F), kv.shape[1]))
    for j, f in enumerate(F):
        i = int(np.clip(np.searchsorted(kF, f, side='right') - 1, 0, len(kF) - 2))
        f0, f1 = kF[i], kF[i + 1]; u = 0.0 if f1 == f0 else (f - f0) / (f1 - f0)
        p0, p1, p2, p3 = P[i], P[i + 1], P[i + 2], P[i + 3]
        out[j] = 0.5 * ((2 * p1) + (-p0 + p2) * u + (2 * p0 - 5 * p1 + 4 * p2 - p3) * u ** 2 + (-p0 + 3 * p1 - 3 * p2 + p3) * u ** 3)
    return out

def camera_tracks(frames, loco_x, cfg, keys):
    """체인별 보간 → 월드 좌표. 반환 dict of arrays (n,3)/(n,)"""
    frames = np.asarray(frames, float); n = len(frames)
    pos = np.zeros((n, 3)); tgt = np.zeros((n, 3)); lens = np.zeros(n); fst = np.zeros(n); chain_id = np.full(n, -1)
    xi = lambda F: np.interp(F, frames, loco_x)
    chains = keys['chains']
    for ci, ch in enumerate(chains):
        kF = [k['F'] for k in ch['keys']]
        lo, hi = kF[0], kF[-1]
        nxt = chains[ci + 1]['keys'][0]['F'] if ci + 1 < len(chains) else 10 ** 9
        m = (frames >= (lo if ci else -1e9)) & (frames < nxt)   # 체인 소속 = 다음 체인 시작 전까지(양끝 외삽은 clamp)
        if ci == len(chains) - 1: m = frames >= lo
        Fm = frames[m]
        P = catmull_rom(kF, [k['p'] for k in ch['keys']], Fm)
        Tt = catmull_rom(kF, [k['t'] for k in ch['keys']], Fm)
        L = catmull_rom(kF, [k['lens'] for k in ch['keys']], Fm)[:, 0]
        S = catmull_rom(kF, [k['fstop'] for k in ch['keys']], Fm)[:, 0]
        if ch['anchor'] == 'follow': shift = xi(Fm)
        else: shift = np.full(len(Fm), xi(ch['anchor_frame']))
        P[:, 0] += shift; Tt[:, 0] += shift
        pos[m] = P; tgt[m] = Tt; lens[m] = L; fst[m] = S; chain_id[m] = ci
    return dict(cam_pos=pos, cam_target=tgt, cam_lens=lens, cam_fstop=fst, cam_chain=chain_id)

def ramp01(frames, f0, f1, fn=smoothstep):
    frames = np.asarray(frames, float)
    return fn((frames - f0) / max(f1 - f0, 1e-9))
