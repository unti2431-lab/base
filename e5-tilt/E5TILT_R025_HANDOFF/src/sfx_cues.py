"""SFX cue sheet from geometry_qc.json events (cue F == event F, so |cue - event| = 0 <= 1F by construction).
Writes ../audio/SFX_CUES.csv. Source files / licences are blank until the sound pass fills them (assets/LICENSES.csv).
"""
import os, json, csv
HERE = os.path.dirname(os.path.abspath(__file__))
ev = json.load(open(os.path.join(HERE, '..', 'evidence', 'geometry_qc.json')))['events']
cfg = json.load(open(os.path.join(HERE, 'rig_config.json')))
sh = ev['shots']; fps = cfg['spec']['fps']
xr = cfg['xray']['skirt_keys_F']
rows = [
    (1, 'train pass-by roar + rail joint clacks', 'foley', 'C01 hook, starts at full level (loop seam)'),
    (sh['C01'][1] - 6, 'whoosh into C02', 'transition', ''),
    (xr[1][0], 'X-ray reveal: low shimmer swell', 'transition', 'skirt goes transparent'),
    (ev['iso_rotate_F'][0], 'whoosh into isolated bogie', 'transition', ''),
    (ev['explode_F'][0], 'metal clicks x4 (parts release)', 'foley', 'spread 0/6/12/18F'),
    (ev['explode_F'][1], 'settle click', 'foley', ''),
    (ev['curve_entry_F'], 'flange squeal (soft) + cabin creak', 'foley', 'curve entry'),
    (ev['tilt_start_F'], 'air FILL hiss (bright) on outer spring + VENT hiss (dull) on inner', 'foley', 'tilt starts'),
    (ev['tilt_reach_F'], 'valve close tick', 'foley', 'tilt reaches 1.45 deg'),
    (sh['C06'][0], 'wind rush, axial', 'ambience', ''),
    (sh['C07'][0], 'cabin room tone', 'ambience', ''),
    (ev['curve_exit_F'], 'flange release', 'foley', 'curve exit'),
    (ev['curve_exit_F'] + int(cfg['tilt']['delay_s'] * fps), 'air exchange hiss (springs equalise)', 'foley', 'tilt-out start'),
    (ev['tilt_return_F'], 'valve close tick', 'foley', 'tilt back to 0'),
    (sh['C09'][0], 'distant pass on viaduct, crane-down whoosh', 'foley', ''),
    (sh['C09'][1] - 40, 'approach roar build -> cross-fade into F1 roar', 'foley', 'loop tail'),
]
out = os.path.join(HERE, '..', 'audio', 'SFX_CUES.csv')
with open(out, 'w', newline='', encoding='utf-8') as fh:
    w = csv.writer(fh)
    w.writerow(['F', 't_s', 'kind', 'layer', 'note', 'source_file', 'license'])
    for f, k, layer, note in sorted(rows):
        w.writerow([f, round((f - 1) / fps, 3), k, layer, note, '', ''])
print('SFX CUES', len(rows), '->', out)
