"""DEL74 베이크 독립 검증 (numpy만, bake.py 코드를 신뢰하지 않음). 결과 ../evidence/bake_qc.json, FAIL 있으면 exit 1."""
import json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
cfg = json.load(open(os.path.join(HERE, 'rig_config.json'), encoding='utf-8'))
def V(*k):
    n = cfg
    for key in k:
        n = key if isinstance(key, dict) else n[key]
    return n['v'] if isinstance(n, dict) and 'v' in n else n
def VH(h, key):
    n = h[key]; return n['v'] if isinstance(n, dict) and 'v' in n else n
b = np.load(os.path.join(HERE, 'del74_bake.npz'))
F = b['frames']; N = cfg['total_frames']; fps = cfg['fps']; i = lambda f: int(np.where(F == f)[0][0])
R = V('wheel', 'radius'); ratio = V('drive', 'gear_ratio'); Fl = V('master_speed', 'launch_frame')
res = {}
def check(name, ok, detail): res[name] = {'status': 'PASS' if ok else 'FAIL', 'detail': detail}

# 1 무미끄럼: Δx = R·Δθ
d = np.abs(np.diff(b['loco_x']) - R * np.diff(b['wheel_theta']))
check('no_slip', d.max() < 1e-9, {'max_abs_err_m': float(d.max())})
# 2 기어 맞물림
d = np.abs(b['pinion_theta'] + ratio * b['gear_theta']); check('gear_mesh', d.max() < 1e-9, {'max_abs_err_rad': float(d.max())})
d = np.abs(b['gear_theta'] - b['wheel_theta']); check('gear_on_axle', d.max() < 1e-12, {})
# 3 크랭크 = 발전기 회전자 1:1
d = np.abs(b['rotor_gen'] - b['crank_theta']); check('crank_rotor_1to1', d.max() < 1e-12, {})
# 4 전동기 회전자: 기동 뒤 피니언과 동기(차이 상수)
for k in range(6):
    dd = (b['rotor_motor'][:, k] - b['pinion_theta'])[i(Fl):]
    ok = np.ptp(dd) < 1e-9
    if not ok: break
check('motor_rotor_sync_after_launch', ok, {'ptp_rad': float(np.ptp(dd))})
# 5 사건 프레임이 목표와 일치
ev = json.load(open(os.path.join(ROOT, 'evidence', 'geometry_qc.json'), encoding='utf-8'))['events']
H = cfg['hypothetical_shaft']; rel = V('coupler', 'release_frames_target')
first = lambda m, s=1: int(F[np.where(m & (F >= s))[0][0]])
ft = first(b['wheel_theta'] - b['wheel_theta'][i(Fl - 1)] > 1e-9, Fl - 5)
sr = [first(b['car_x'][:, c] - b['car_x'][i(Fl - 1), c] > 1e-9, Fl) for c in range(b['car_x'].shape[1])]
eng = first((b['ghost_x'] <= 1e-9) & (F >= VH(H, 'approach_frame')))
check('event_first_turn', ft == Fl, {'got': ft, 'target': Fl})
check('event_slack_release', sr == rel, {'got': sr, 'target': rel})
check('event_engage', eng == VH(H, 'engage_frame'), {'got': eng, 'target': VH(H, 'engage_frame')})
cs = first((np.abs(b['crank_omega']) < 1e-6) & (F > VH(H, 'engage_frame')))
check('event_crank_stop', cs == VH(H, 'crank_stop_frames')[1], {'got': cs, 'target': VH(H, 'crank_stop_frames')[1]})
# 6 연결기: 객차는 기관차보다 먼저/빠르게 움직이지 않음, 유격 0 ≤ s ≤ S, 뭉침 단조
S = b['coupler_S']; s = b['coupler_slack']
check('slack_bounds', bool((s >= -1e-12).all() and (s <= S[None, :] + 1e-12).all()), {'S_m': S.tolist()})
dcar = np.diff(b['car_x'], axis=0); dloco = np.diff(b['loco_x'])[:, None]
check('cars_never_outrun_loco_on_launch', bool((dcar[i(Fl) - 1:] <= dloco[i(Fl) - 1:] + 1e-12).all()), {})
# 7 튐 검출(기관차 기준 좌표계): 객차 상대 이동량이 기관차 이동량의 1.25배를 넘지 않음
relmove = np.abs(np.diff(b['car_x'] - b['loco_x'][:, None], axis=0))
ref = np.maximum(np.abs(dloco), 1e-6)
check('no_jump_car_relative', bool((relmove <= 1.25 * ref + 1e-9).all() or relmove.max() < 0.01), {'max_rel_move_m': float(relmove.max())})
# 8 루프: F1417 ≡ F1
wr = (b['wheel_theta'][i(N + 1)] - b['wheel_theta'][i(1)]) % (2 * math.pi); wr = min(wr, 2 * math.pi - wr)
cr = (b['crank_theta'][i(N + 1)] - b['crank_theta'][i(1)]) % (2 * math.pi); cr = min(cr, 2 * math.pi - cr)
check('loop_wheel_phase', wr < 1e-6, {'residual_rad': float(wr)})
check('loop_crank_phase', cr < 1e-3, {'residual_rad': float(cr)})
check('loop_velocity', abs(b['loco_v'][i(N + 1)] - b['loco_v'][i(1)]) < 1e-9, {})
camL = b['cam_pos'] - b['loco_x'][:, None] * np.array([1, 0, 0]); tgtL = b['cam_target'] - b['loco_x'][:, None] * np.array([1, 0, 0])
dc = np.abs(camL[i(N + 1)] - camL[i(1)]).max() + np.abs(tgtL[i(N + 1)] - tgtL[i(1)]).max() + abs(b['cam_lens'][i(N + 1)] - b['cam_lens'][i(1)])
check('loop_camera_W0', dc < 1e-6, {'max_abs_diff': float(dc)})
check('loop_coupler_state', bool(np.abs(s[i(N + 1)] - s[i(1)]).max() < 1e-9), {})
# 9 피스톤: 로드 기하 성립, 행정 범위
r, l = V('engine', 'crank_radius'), V('engine', 'rod_length'); p = b['piston']
check('piston_geometry', l > r and np.isfinite(p).all() and abs((p.max() - p.min()) - 2 * r) < 1e-6, {'stroke_m': float(p.max() - p.min())})
# 10 카메라: 180° 좌측(Y>0), 정지 프레임 0(체인 내부), 하드컷에서만 점프
check('camera_left_side', bool((b['cam_pos'][:, 1] > 0).all()), {'min_y': float(b['cam_pos'][:, 1].min())})
spd = np.linalg.norm(np.diff(camL, axis=0), axis=1) * fps; dl = np.abs(np.diff(b['cam_lens'])) * fps
same = np.diff(b['cam_chain']) == 0
still = same[i(1):i(N)] & (spd[i(1):i(N)] < V('camera', 'min_move_speed')) & (dl[i(1):i(N)] < 0.5)
check('camera_never_still', int(still.sum()) == 0, {'still_frames': [int(F[i(1) + k]) for k in np.where(still)[0][:20]], 'count': int(still.sum())})
jumps = np.where(~same)[0]; jumpF = sorted(set(int(F[j + 1]) for j in jumps))
check('camera_jumps_only_at_hard_cuts', jumpF == V('hard_cuts'), {'jumps_at': jumpF})
# 11 장치 채널 범위
for k in ['skin_ghost', 'ghost_vis', 'gearbox', 'clutch', 'driveshaft']:
    check(f'range01_{k}', bool((b[k] >= -1e-9).all() and (b[k] <= 1 + 1e-9).all()), {})
check('iso_drop_nonneg', bool((b['iso_drop'] >= -1e-9).all()), {})
# 12 명사 선행 노출(VO_WORDS vs 계획 노출 F)
vo = json.load(open(os.path.join(ROOT, 'audio', 'VO_WORDS.json'), encoding='utf-8'))
nounF = {k['noun']: k['F'] for ph in vo['phrases'] for k in ph['keys']}
expose = {'기관차': 1, '엔진': 86, '바퀴': 105, '십육 기통': 394, '발전기': 488, '케이블': 552, '대차': 642, '차축': 706, '전동기': 774, '객차': 965, '변속기': 1126, '클러치': 1168, '구동축': 1196, '발전소': 1257, '전기 기관차': 1324}
lead = {k: nounF[k] - v for k, v in expose.items()}
check('noun_pre_exposure_ge6', all(v >= 6 for v in lead.values()), lead)

ok = all(v['status'] == 'PASS' for v in res.values())
out = {'ALL': 'PASS' if ok else 'FAIL', 'n_pass': sum(v['status'] == 'PASS' for v in res.values()), 'n_total': len(res), 'checks': res}
json.dump(out, open(os.path.join(ROOT, 'evidence', 'bake_qc.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print(json.dumps({k: v['status'] + ('' if v['status'] == 'PASS' else ' ' + json.dumps(v['detail'], ensure_ascii=False)) for k, v in res.items()}, ensure_ascii=False, indent=1)); print('ALL', out['ALL'])
sys.exit(0 if ok else 1)
