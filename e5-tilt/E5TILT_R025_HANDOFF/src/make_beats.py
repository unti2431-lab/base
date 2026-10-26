"""Regenerate ../BEATS_R025.csv from cameras.json + evidence/geometry_qc.json + audio/VO_PHRASES.json.
Narration column = R025 proposal (re-record option, blocker G-1). noun_first_F stays blank until VO_WORDS.json exists.
"""
import os, json, csv
HERE = os.path.dirname(os.path.abspath(__file__))
cams = json.load(open(os.path.join(HERE, 'cameras.json')))
ev = json.load(open(os.path.join(HERE, '..', 'evidence', 'geometry_qc.json')))['events']
vp = json.load(open(os.path.join(HERE, '..', 'audio', 'VO_PHRASES.json')))
NARR = {
    'C01': ('E5', '시속 320킬로미터, E5입니다.', 1),
    'C02': ('공기스프링', '차체는 공기스프링 두 개 위에 떠 있습니다.', 92),
    'C03': ('벨로우즈 / 보조 공기실 / 높이조절밸브', '고무 벨로우즈와 보조 공기실, 그리고 높이조절밸브입니다.', 118),
    'C04': ('곡선 / 승객', '곡선에 들어서면 승객은 바깥쪽으로 쏠립니다.', 225),
    'C05': ('공기', '바깥쪽 스프링에 공기를 넣고 안쪽은 빼서 차체를 안쪽으로 기울입니다.', 319),
    'C06': ('1.5도', '기울기는 최대 1.5도입니다.', 415),
    'C07': ('쏠림', '승객이 느끼는 쏠림은 그만큼 줄어듭니다.', 497),
    'C08': ('높이', '곡선을 빠져나오면 양쪽 높이가 다시 같아집니다.', 602),
    'C09': ('320킬로미터', '이 작은 기울임으로 E5는 곡선에서도 320킬로미터를 냅니다.', 713),
}
EVENT = {
    'C01': 'F1 nose already passing; camera whips on board by F31',
    'C02': f'skirt X-ray F{70}-F{92}',
    'C03': f'iso yaw F{ev["iso_rotate_F"][0]}-F{ev["iso_rotate_F"][1]}, explode F{ev["explode_F"][0]}-F{ev["explode_F"][1]}',
    'C04': f'curve entry F{ev["curve_entry_F"]}, drink lean max {ev["resid_max_deg"]:.1f} deg',
    'C05': f'tilt F{ev["tilt_start_F"]}-F{ev["tilt_reach_F"]} (0 -> 1.45 deg), spring dh {ev["spring_dh_max_m"] * 100:.1f} cm',
    'C06': 'roll held 1.5 deg; ghost twin on',
    'C07': f'drink lean {ev["resid_C07_deg"]:.1f} deg (reduced)',
    'C08': f'curve exit F{ev["curve_exit_F"]}, tilt back to 0 by F{ev["tilt_return_F"]}; skirt closes F668-F700',
    'C09': 'crane down to W0; last frame = F1 (train-relative pose)',
}
SFX = {'C01': 'pass-by roar', 'C02': 'shimmer swell', 'C03': 'whoosh, clicks x4', 'C04': 'flange squeal, creak',
       'C05': 'FILL hiss + VENT hiss, valve tick', 'C06': 'axial wind', 'C07': 'room tone', 'C08': 'flange release, equalise hiss, tick',
       'C09': 'distant pass -> approach roar -> crossfade to F1'}
LOOP = {'C01': 'W0 (loop seam start)', 'C09': 'W0 return (loop seam end)'}
phr = vp['phrases']
out = os.path.join(HERE, '..', 'BEATS_R025.csv')
with open(out, 'w', newline='', encoding='utf-8') as fh:
    w = csv.writer(fh)
    w.writerow(['shot', 'F_start', 'F_end', 't_start', 't_end', 'cam_anchor', 'lens_mm', 'new_info', 'event_F (bake)',
                'VO_phrases (silence-gap timing)', 'narration_proposal', 'noun', 'object_first_exposure_F', 'noun_first_F', 'SFX', 'loop'])
    for s in cams['shots']:
        f0, f1 = s['F']
        ps = [p for p in phr if p['F'][0] <= f1 and p['F'][1] >= f0]
        lens = sorted({k['lens'] for k in s['keys']})
        noun, line, expo = NARR[s['id']]
        w.writerow([s['id'], f0, f1, round((f0 - 1) / 30, 2), round(f1 / 30, 2), s['cam_anchor']['type'], f'{lens[0]}-{lens[-1]}',
                    s['info'], EVENT[s['id']], ' '.join(f"P{p['i']}[F{p['F'][0]}-{p['F'][1]}]" for p in ps), line, noun, expo, '',
                    SFX[s['id']], LOOP.get(s['id'], '')])
print('BEATS ->', out)
