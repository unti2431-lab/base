"""DEL74 베이크: rig_config.json + camera_keys.json → del74_bake.npz + ../evidence/geometry_qc.json + ../audio/SFX_CUES.csv
실행: python3 bake.py  (bpy 불필요, numpy만)"""
import json, math, os, sys, csv, hashlib
import numpy as np
import kin
from kin import V

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
cfg = kin.load_cfg(os.path.join(HERE, 'rig_config.json'))
keys = kin.load_cfg(os.path.join(HERE, cfg['camera']['keys_file']))
fps = cfg['fps']; N = cfg['total_frames']
F0, F1 = cfg['bake_frames']
frames = np.arange(F0, F1 + 1, dtype=float)       # 0 … 1417 (모션블러용 양끝 포함)
t = kin.t_of(frames, fps)
n = len(frames)
idx = lambda F: int(F - F0)                        # 프레임 → 배열 인덱스

# ---- 마스터 속도 (루프 정수 회전 역산) ----
v0, k_wheel = kin.solve_v0_for_loop(cfg)
vel, a1 = kin.master_velocity(t, cfg, v0)
loco_x = kin.integrate_position(frames, cfg, v0, sub=40)
R = V(cfg, 'wheel', 'radius')
wheel_theta = loco_x / R                           # 무미끄럼 (진행 +X, 좌측에서 보면 시계 방향)
ratio = V(cfg, 'drive', 'gear_ratio')
gear_theta = wheel_theta.copy()
pinion_theta = -ratio * gear_theta                 # 외접 맞물림: 반대 방향

# ---- 전동기 회전자: 무부하 회전(F838–894) + 피니언 동기 ----
Ffree0, Ffree1, Fl = 838, 870, V(cfg, 'master_speed', 'launch_frame')
wfree = V(cfg, 'drive', 'rotor_free_spin_omega')
w_rot = np.zeros(n)
m = (frames >= Ffree0) & (frames < Ffree1); w_rot[m] = wfree * kin.smoothstep((frames[m] - Ffree0) / (Ffree1 - Ffree0))
m = (frames >= Ffree1) & (frames < Fl);     w_rot[m] = wfree * (1 - kin.smoothstep((frames[m] - Ffree1) / (Fl - Ffree1)))
free_angle = np.cumsum(w_rot) / fps
rotor_motor = np.stack([free_angle + pinion_theta + i * 0.37 for i in range(6)], axis=1)  # 위상 오프셋은 시각 다양성

# ---- 크랭크 / 피스톤 / 발전기 회전자 ----
w_run, k_crank = kin.solve_w_run_for_loop(cfg)
crank_omega = kin.crank_omega(t, cfg, w_run)
crank_theta = kin.integrate_angle(frames, cfg, lambda ts: kin.crank_omega(ts, cfg, w_run), sub=40)
piston = kin.piston_positions(crank_theta, cfg)
rotor_gen = crank_theta.copy()                      # 1:1 직결
H = cfg['hypothetical_shaft']
amp, hz = V(cfg, 'engine', 'idle_vibration_amp'), V(cfg, 'engine', 'idle_vibration_hz')
Fst = V(H, 'stall_frame')
engine_vib = np.where((frames >= 187) & (frames < Fst), amp * np.sin(2 * np.pi * hz * t), 0.0)

# ---- 가정 구동축 ----
Fi0, Fi1 = V(H, 'insert_frames'); Fap = V(H, 'approach_frame'); Fen = V(H, 'engage_frame')
Frw0, Frw1 = V(H, 'rewind_frames'); Fre = V(H, 'reappear_frame')
off0, trav = V(H, 'insert_offset'), V(H, 'engage_travel')
ghost_x = np.zeros(n); ghost_vis = np.zeros(n)
m = (frames >= Fi0) & (frames < Fap)
ghost_x[m] = off0 * (1 - kin.ease_out((frames[m] - Fi0) / (Fi1 - Fi0))) + trav * 2   # 삽입 후 체결 전: 2단계 여유
m = (frames >= Fap) & (frames < Fen)
ghost_x[m] = trav * 2 - trav * kin.ease_out((frames[m] - Fap) / (Fen - Fap))
m = (frames >= Fen) & (frames < Frw0); ghost_x[m] = 0.0
m = (frames >= Frw0) & (frames <= Frw1); ghost_x[m] = off0 * kin.ease_in((frames[m] - Frw0) / (Frw1 - Frw0))
ghost_vis[(frames >= Fi0) & (frames <= Frw1)] = 1.0
ghost_vis[(frames >= Frw1 - 8) & (frames <= Frw1)] = np.linspace(1, 0, 9)[: int(np.sum((frames >= Frw1 - 8) & (frames <= Frw1)))]
ghost_vis[frames == Fre] = 1.0
ghost_theta = np.where((frames >= Fen) & (frames < Frw0), crank_theta, crank_theta)  # 가정 세계: 축 = 크랭크와 동회전

# ---- 장치 채널 ----
D = cfg['devices']
g0, g1 = V(D, 'skin_ghost_up'); d0, d1 = V(D, 'skin_ghost_down')
skin_ghost = np.where(frames < g0, 0.0, np.where(frames < g1, kin.ramp01(frames, g0, g1), np.where(frames < d0, 1.0, np.where(frames < d1, 1 - kin.ramp01(frames, d0, d1), 0.0))))
def cutter(spec):
    f0, f1, r = spec; return np.where(frames < f0, 0.0, kin.ramp01(frames, f0, f1) * r)
cutter_r = np.stack([cutter(V(D, 'cutter_generator'))] + [cutter(s) for s in V(D, 'cutter_axles')] + [cutter(V(D, 'cutter_motor'))], axis=1)
# 커터 링은 각 컷 체인이 끝나면 닫힘(C05 링은 C06a 시작 F552에 8F, C07 링은 C09 하드컷 F965에 즉시)
cutter_r[:, 0] *= np.where(frames < 552, 1.0, 1 - kin.ramp01(frames, 552, 560))
cutter_r[:, 1:] *= np.where(frames < 965, 1.0, 0.0)[:, None]
depth = V(D, 'iso_drop_depth')
i0, i1, _ = V(D, 'iso_drop_C04'); r0, r1 = V(D, 'iso_restore_C06'); j0, j1, j2, j3 = V(D, 'iso_drop_C08')
iso_drop = np.zeros(n)
iso_drop += np.where((frames >= i0) & (frames < r0), kin.ramp01(frames, i0, i1), 0.0) * depth
iso_drop += np.where((frames >= r0) & (frames < r1), 1 - kin.ramp01(frames, r0, r1), 0.0) * depth
iso_drop += np.where((frames >= j0) & (frames < j2), kin.ramp01(frames, j0, j1), 0.0) * depth
iso_drop += np.where((frames >= j2) & (frames <= j3), 1 - kin.ramp01(frames, j2, j3), 0.0) * depth
e0, e1 = V(D, 'electric_cable_pulse')
electric_u = np.full(n, -1.0)
m = (frames >= e0) & (frames <= e1); electric_u[m] = kin.ease_in((frames[m] - e0) / (e1 - e0))
for a, b in V(D, 'electric_fullpath_pulses'):
    m = (frames >= a) & (frames <= b); electric_u[m] = (frames[m] - a) / (b - a)
motor_pulse = np.zeros((n, 6))
for i, f in enumerate(V(D, 'electric_motor_pulses')):
    m = (frames >= f) & (frames < f + 8); motor_pulse[m, i] = 1 - (frames[m] - f) / 8.0
ghost10 = {}
for name, (a0, a1_, b0, b1) in V(D, 'ghosts_C10').items():
    ghost10[name] = np.where(frames < a0, 0, np.where(frames < a1_, kin.ramp01(frames, a0, a1_), np.where(frames < b0, 1.0, np.where(frames < b1, 1 - kin.ramp01(frames, b0, b1), 0.0))))
ll0, ll1, ev = V(D, 'light_link_C11a')
light_link = np.where((frames >= ll0) & (frames <= ll1), ev, 0.0)

# ---- 연결기 / 객차 ----
S, slack, bunch, car_off = kin.coupler_and_cars(frames, loco_x, cfg)
car_x = loco_x[:, None] + car_off[None, :] + bunch   # 뭉침(bunch)은 기관차 쪽(+X)으로
car_wheel_theta = car_x / V(cfg, 'car', 'wheel_radius')

# ---- 카메라 ----
cam = kin.camera_tracks(frames, loco_x, cfg, keys)

# ---- 사건 역산 ----
def first_frame(mask, start=1):
    w = np.where(mask & (frames >= start))[0]
    return int(frames[w[0]]) if len(w) else None
events = {
    'whistle_F': 1,
    'decel_start_F': V(cfg, 'master_speed', 'decel_frames')[0],
    'stop_F': first_frame(vel <= 1e-9, 100),
    'ghost_insert_F': [Fi0, Fi1], 'ghost_approach_F': Fap,
    'ghost_engage_F': first_frame((ghost_x <= 1e-9) & (frames >= Fap)),
    'crank_stop_F': first_frame((np.abs(crank_omega) < 1e-6) & (frames > Fen)),
    'engine_stall_F': Fst,
    'rewind_F': [Frw0, Frw1],
    'crank_ramp_F': [404, 470],
    'ignition_highlight_F': [int(f) for f in np.linspace(404, 470, 8).round()],   # 점화 8타 시각 하이라이트(0.31 s 간격)
    'ghost_reappear_F': Fre,
    'coupling_pass_F': 500,
    'cutter_generator_F': V(D, 'cutter_generator')[:2],
    'electric_start_F': e0, 'electric_cable_end_F': e1,
    'cutter_axles_F': [s[0] for s in V(D, 'cutter_axles')],
    'cutter_motor_F': V(D, 'cutter_motor')[:2],
    'motor_pulse_F': V(D, 'electric_motor_pulses'),
    'rotor_free_spin_F': [Ffree0, Fl],
    'iso_C08_F': V(D, 'iso_drop_C08'),
    'first_turn_F': first_frame(wheel_theta - wheel_theta[idx(Fl - 1)] > 1e-9, Fl - 5),
    'slack_release_F': [first_frame(car_x[:, i] - car_x[idx(Fl), i] > 1e-9, Fl) for i in range(car_x.shape[1])],
    'slack_values_m': [round(float(s), 4) for s in S],
    'fullpath_pulse_F': V(D, 'electric_fullpath_pulses'),
    'ghosts_C10_F': V(D, 'ghosts_C10'),
    'skin_close_F': [d0, d1],
    'v0_reached_F': V(cfg, 'master_speed', 'accel2_end_frame'),
    'hard_cuts_F': V(cfg, 'hard_cuts'),
}
loop = {
    'v0_m_s': round(float(v0), 6), 'wheel_revs_total': k_wheel,
    'wheel_phase_residual_rad': float(min((wheel_theta[idx(N + 1)] - wheel_theta[idx(1)]) % (2 * math.pi), 2 * math.pi - (wheel_theta[idx(N + 1)] - wheel_theta[idx(1)]) % (2 * math.pi))),
    'omega_run_rad_s': round(float(w_run), 6), 'crank_revs_total': k_crank,
    'crank_phase_residual_rad': float(min((crank_theta[idx(N + 1)] - crank_theta[idx(1)]) % (2 * math.pi), 2 * math.pi - (crank_theta[idx(N + 1)] - crank_theta[idx(1)]) % (2 * math.pi))),
    'launch_accel1_m_s2': round(float(a1), 6),
    'cam_F1417_minus_F1_local': [round(float(x), 6) for x in ((cam['cam_pos'][idx(N + 1)] - loco_x[idx(N + 1)] * np.array([1, 0, 0])) - (cam['cam_pos'][idx(1)] - loco_x[idx(1)] * np.array([1, 0, 0])))],
}

out = dict(frames=frames, t=t, loco_x=loco_x, loco_v=vel, wheel_theta=wheel_theta, gear_theta=gear_theta, pinion_theta=pinion_theta,
           rotor_motor=rotor_motor, crank_theta=crank_theta, crank_omega=crank_omega, piston=piston, rotor_gen=rotor_gen, engine_vib=engine_vib,
           ghost_x=ghost_x, ghost_vis=ghost_vis, ghost_theta=ghost_theta, skin_ghost=skin_ghost, cutter_r=cutter_r, iso_drop=iso_drop,
           electric_u=electric_u, motor_pulse=motor_pulse, light_link=light_link, car_x=car_x, car_wheel_theta=car_wheel_theta,
           coupler_slack=slack, coupler_S=S, car_offsets=car_off, **{k: v for k, v in ghost10.items()}, **cam)
out = {k: np.asarray(v, float) for k, v in out.items()}
np.savez(os.path.join(HERE, 'del74_bake.npz'), **out)
sha = hashlib.sha256(open(os.path.join(HERE, 'del74_bake.npz'), 'rb').read()).hexdigest()
os.makedirs(os.path.join(ROOT, 'evidence'), exist_ok=True)
with open(os.path.join(ROOT, 'evidence', 'geometry_qc.json'), 'w', encoding='utf-8') as f:
    json.dump({'bake_sha256': sha, 'config_sha256': hashlib.sha256(open(os.path.join(HERE, 'rig_config.json'), 'rb').read()).hexdigest(),
               'channels': {k: list(v.shape) for k, v in out.items()}, 'loop': loop, 'events': events}, f, ensure_ascii=False, indent=2)
# ---- SFX 큐시트 ----
cues = [(1, '기적', '폴리'), (events['decel_start_F'], '레일 구름 감쇠 시작', '공간음'), (187, '디젤 공회전(가정)', '폴리'),
        (events['ghost_engage_F'], '금속 체결', '폴리'), (events['ghost_engage_F'], '엔진 실속 시작', '폴리'), (events['crank_stop_F'], '엔진 정지', '폴리'),
        (Frw0, '되감기 우쉬', '전환'), (404, '디젤 가속', '폴리')] + [(f, f'점화 하이라이트 {i+1}/8', '폴리') for i, f in enumerate(events['ignition_highlight_F'])] + \
       [(e0, '전기 허밍 시작', '폴리')] + [(f, f'전동기 점등 {i+1}/6', '폴리') for i, f in enumerate(events['motor_pulse_F'])] + \
       [(events['first_turn_F'], '기어 접촉·기동', '폴리')] + [(f, f'연결기 장력 {i+1}/4', '폴리') for i, f in enumerate(events['slack_release_F'])] + \
       [(v[0], f'유령 등장 {k}', '전환') for k, v in events['ghosts_C10_F'].items()] + [(v[3], f'유령 소멸 {k}', '전환') for k, v in events['ghosts_C10_F'].items()] + \
       [(d0, '외피 닫힘', '폴리'), (V(cfg, 'master_speed', 'accel2_end_frame'), '레일 구름 v0(루프 꼬리=머리)', '공간음')]
with open(os.path.join(ROOT, 'audio', 'SFX_CUES.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f); w.writerow(['F', 't_s', 'cue', 'layer', 'source_file', 'license'])
    for F, c, l in sorted(cues, key=lambda x: x[0]): w.writerow([F, round((F - 1) / fps, 3), c, l, '', ''])
print(json.dumps({'loop': loop, 'events': events}, ensure_ascii=False, indent=1))
