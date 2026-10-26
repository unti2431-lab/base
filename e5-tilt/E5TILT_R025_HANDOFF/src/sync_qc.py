"""G5 sync + structure QC.
1. every cut lies inside (or within 6F of) a VO silence gap  -> cuts never chop a phrase
2. noun-first: object first-exposure F <= noun first-utterance F - 6, using BEATS_R025.csv
   (noun F columns are PROVISIONAL until VO_WORDS.json exists -> status NOT_DECIDABLE, never PASS)
3. optional --video: per-second motion (YAVG of frame difference at 180 px wide, 10 fps), static seconds, scene cuts
Writes ../evidence/sync_qc.json
"""
import os, sys, json, csv, argparse, subprocess, re
HERE = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument('--video', default=None)
A = ap.parse_args()
cfg = json.load(open(os.path.join(HERE, 'rig_config.json')))
cams = json.load(open(os.path.join(HERE, 'cameras.json')))
vp = json.load(open(os.path.join(HERE, '..', 'audio', 'VO_PHRASES.json')))
fps = cfg['spec']['fps']
gapsF = [[int(round(a * fps)) + 1, int(round(b * fps)) + 1] for a, b in vp['silence_gaps_s']]
res = {'PASS': {}, 'values': {}}

cuts = [s['F'][0] for s in cams['shots'][1:]]
cut_rep = []
for c in cuts:
    d = min((0 if g[0] <= c <= g[1] else min(abs(c - g[0]), abs(c - g[1]))) for g in gapsF)
    cut_rep.append({'cut_F': c, 'frames_from_gap': d})
ok = all(x['frames_from_gap'] <= 6 for x in cut_rep)
res['PASS']['cuts_on_vo_gaps'] = 'PASS' if ok else 'FAIL'
res['values']['cuts_on_vo_gaps'] = cut_rep

words = os.path.join(HERE, '..', 'audio', 'VO_WORDS.json')
beats = os.path.join(HERE, '..', 'BEATS_R025.csv')
if os.path.exists(words):
    res['PASS']['noun_first'] = 'NOT_PERFORMED'      # implement once VO_WORDS.json exists: fill noun F in BEATS and compare
else:
    res['PASS']['noun_first'] = 'NOT_DECIDABLE'
    res['values']['noun_first'] = 'VO_WORDS.json missing (whisper model download blocked in cloud). Run scripts/vo_words.py locally.'

if A.video:
    cmd = ['ffmpeg', '-i', A.video, '-vf', 'scale=180:-1,fps=10,tblend=all_mode=difference,signalstats,metadata=print:key=lavfi.signalstats.YAVG', '-f', 'null', '-']
    out = subprocess.run(cmd, capture_output=True, text=True).stderr
    y = [float(v) for v in re.findall(r'YAVG=([0-9.]+)', out)]
    per_s = [round(sum(y[i:i + 10]) / len(y[i:i + 10]), 2) for i in range(0, len(y), 10) if y[i:i + 10]]
    cmd2 = ['ffmpeg', '-i', A.video, '-vf', "select='gt(scene,0.2)',showinfo", '-f', 'null', '-']
    cut_t = [float(v) for v in re.findall(r'pts_time:([0-9.]+)', subprocess.run(cmd2, capture_output=True, text=True).stderr)]
    mean = sum(per_s) / len(per_s)
    res['values']['motion_per_s'] = per_s
    res['values']['motion_mean'] = round(mean, 2)
    res['values']['motion_min'] = min(per_s)
    res['values']['hard_cuts_detected_s'] = cut_t
    res['PASS']['motion_mean_ge_9'] = 'PASS' if mean >= 9 else 'FAIL'
    res['PASS']['no_static_second'] = 'PASS' if min(per_s) >= 3 else 'FAIL'
    res['PASS']['hard_cuts_6_to_16'] = 'PASS' if 6 <= len(cut_t) <= 16 else 'FAIL'
res['result'] = 'FAIL' if 'FAIL' in res['PASS'].values() else ('PASS' if all(v == 'PASS' for v in res['PASS'].values()) else 'INCOMPLETE')
json.dump(res, open(os.path.join(HERE, '..', 'evidence', 'sync_qc.json'), 'w'), indent=2)
print(json.dumps(res['PASS'], indent=1), res['result'])
