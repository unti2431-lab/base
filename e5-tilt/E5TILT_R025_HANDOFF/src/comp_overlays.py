"""2.5D post overlays (shapes only, never letters) projected from tilt_bake.npz. STYLE LOCK:
  cyan  = air flow (C05: fill arrow on the outer spring, vent arrow on the inner spring)
  amber = angle / height difference (C05 spring-top ticks, C06 roll arc, C04/C07 drink surface)
  white = level reference (ghost line, cup rim)
python comp_overlays.py --frames ../work/frames_animatic --out ../work/frames_comp
Writes overlay-only RGBA PNGs too (--overlay_only) for an editor comp.
"""
import os, json, argparse
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
CYAN = (60, 225, 255); AMBER = (255, 176, 46); WHITE = (245, 248, 255)

ap = argparse.ArgumentParser()
ap.add_argument('--bake', default=os.path.join(HERE, 'tilt_bake.npz'))
ap.add_argument('--frames', default=os.path.join(HERE, '..', 'work', 'frames_animatic'))
ap.add_argument('--out', default=os.path.join(HERE, '..', 'work', 'frames_comp'))
ap.add_argument('--overlay_only', action='store_true')
A = ap.parse_args()
D = dict(np.load(A.bake)); CFG = json.load(open(os.path.join(HERE, 'rig_config.json')))
CAMS = json.load(open(os.path.join(HERE, 'cameras.json')))
F = D['F']; W0, H0 = CFG['spec']['resolution']; SENS = CFG['spec']['sensor_height_mm']
TN, SP, BG, CB = CFG['train'], CFG['spring'], CFG['bogie'], CFG['cabin']
hk = TN['hero_car'] - 1


def q2m(q):
    w, x, y, z = q
    return np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                     [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                     [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])


def shot_of(f):
    for s in CAMS['shots']:
        if s['F'][0] <= f <= s['F'][1]:
            return s['id']


def projector(cid, f, W, H):
    Fr = D[f'cam_{cid}_F']; i = int(np.where(Fr == f)[0][0])
    c = D[f'cam_{cid}_loc'][i]; R = q2m(D[f'cam_{cid}_quat'][i]); lens = D[f'cam_{cid}_lens'][i]
    k = lens / SENS * H
    def P(p):
        pc = R.T @ (np.asarray(p, float) - c)
        if pc[2] >= -1e-3:
            return None
        return (W / 2 + k * pc[0] / -pc[2], H / 2 - k * pc[1] / -pc[2])
    return P


def xf(loc, quat, p):
    return q2m(quat) @ np.asarray(p, float) + loc


def arrow(dr, a, b, col, w):
    dr.line([a, b], fill=col, width=w)
    v = np.subtract(b, a); L = np.hypot(*v) + 1e-6; u = v / L; n = np.array([-u[1], u[0]])
    hl = max(3 * w, 0.35 * L)
    p1 = np.array(b) - u * hl + n * hl * 0.55; p2 = np.array(b) - u * hl - n * hl * 0.55
    dr.polygon([tuple(b), tuple(p1), tuple(p2)], fill=col)


def ext(a, b, s):
    a, b = np.array(a), np.array(b); m = (a + b) / 2
    return tuple(m + (a - m) * s), tuple(m + (b - m) * s)


def draw_frame(f, img):
    W, H = img.size
    SS = 2
    ov = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0)); dr = ImageDraw.Draw(ov)
    cid = shot_of(f); i = int(np.where(F == f)[0][0])
    P0 = projector(cid, f, W, H)
    P = lambda p: (lambda r: None if r is None else (r[0] * SS, r[1] * SS))(P0(p))
    lw = max(2, int(round(H * SS / 480 * 1.6)))
    sl = SP['s_lat'] / 2; ft = BG['frame_top_above_rail']; hb = TN['bogie_half_spacing']
    if cid == 'C05':
        bl, bq = D['bog_loc'][hk, 1, i], D['bog_quat'][hk, 1, i]
        Ld, Lq = D['body_loc'][hk, i], D['body_quat'][hk, i]
        for side, sx, dh in (('L', -1, D['dh_L'][i]), ('R', 1, D['dh_R'][i])):
            h = D[f'h_{side}'][i]
            mid = xf(bl, bq, [sx * sl, 0, ft + h * 0.5])
            top = xf(Ld, Lq, [sx * sl, -hb, -0.002])
            rate = np.clip(abs(dh) / 0.0012, 0, 1)                # m/frame normalised
            if rate > 0.08:
                a = P(mid - np.array([0, 0, 0.16 * rate]) * np.sign(dh)); b = P(mid + np.array([0, 0, 0.16 * rate]) * np.sign(dh))
                if a and b:
                    arrow(dr, a, b, CYAN + (int(255 * min(1, rate * 1.5)),), lw + 2)
            t0 = P(top - xf(np.zeros(3), Lq, [0.55, 0, 0]) + 0); t1 = P(top + xf(np.zeros(3), Lq, [0.55, 0, 0]))
            if t0 and t1:
                dr.line([t0, t1], fill=AMBER + (235,), width=lw)
    elif cid == 'C06':
        Ld, Lq = D['body_loc'][hk, i], D['body_quat'][hk, i]
        Gl, Gq = D['ghost_loc'][i], D['ghost_quat'][i]
        y = float(D['car_len'][hk]) / 2 - TN['nose_len'] + 0.3
        pa, pb = P(xf(Gl, Gq, [-1.55, y, 1.6])), P(xf(Gl, Gq, [1.55, y, 1.6]))
        qa, qb = P(xf(Ld, Lq, [-1.55, y, 1.6])), P(xf(Ld, Lq, [1.55, y, 1.6]))
        if pa and pb and qa and qb:
            pa, pb = ext(pa, pb, 3.2); qa, qb = ext(qa, qb, 3.2)
            m_ = tuple((np.array(pa) + np.array(pb)) / 2)
            dr.polygon([m_, pb, qb], fill=AMBER + (90,))
            dr.line([pa, pb], fill=WHITE + (200,), width=max(1, lw - 1))
            dr.line([qa, qb], fill=AMBER + (240,), width=lw)
            c = np.array(pa) * 0.5 + np.array(qa) * 0.5
            r = np.hypot(*(np.array(pb) - c)) * 0.92
            a0 = np.degrees(np.arctan2(pb[1] - c[1], pb[0] - c[0])); a1 = np.degrees(np.arctan2(qb[1] - c[1], qb[0] - c[0]))
            lo, hi = sorted((a0, a1))
            if hi - lo > 0.05:
                dr.arc([c[0] - r, c[1] - r, c[0] + r, c[1] + r], lo, hi, fill=AMBER + (255,), width=lw + 1)
    elif cid in ('C04', 'C07'):
        Ld, Lq = D['body_loc'][hk, i], D['body_quat'][hk, i]
        cx, cy = CB['cup_local']; fz = CB['floor_above_rail'] - TN['body_bottom_above_rail']
        tz = fz + CB['table_h'] + 0.0005
        lr = CB['cup_r'] - 0.0025; hl = CB['liquid_h']; tr = np.tan(D['resid'][i])
        rim = [xf(Ld, Lq, [cx - CB['cup_r'], cy, tz + CB['cup_h']]), xf(Ld, Lq, [cx + CB['cup_r'], cy, tz + CB['cup_h']])]
        liq = [xf(Ld, Lq, [cx - lr, cy, tz + hl - lr * tr]), xf(Ld, Lq, [cx + lr, cy, tz + hl + lr * tr])]
        a, b = P(rim[0]), P(rim[1]); c_, d_ = P(liq[0]), P(liq[1])
        if a and b and c_ and d_:
            a, b = ext(a, b, 1.6); c_, d_ = ext(c_, d_, 1.6)
            dr.line([a, b], fill=WHITE + (170,), width=max(1, lw - 1))
            dr.line([c_, d_], fill=AMBER + (235,), width=lw)
    ov = ov.resize((W, H), Image.LANCZOS)
    return ov


os.makedirs(A.out, exist_ok=True)
n = 0
for f in F:
    f = int(f)
    src = os.path.join(A.frames, f'{f:04d}.png')
    if not os.path.exists(src):
        continue
    img = Image.open(src).convert('RGBA')
    ov = draw_frame(f, img)
    if A.overlay_only:
        ov.save(os.path.join(A.out, f'{f:04d}.png'))
    else:
        Image.alpha_composite(img, ov).convert('RGB').save(os.path.join(A.out, f'{f:04d}.png'))
    n += 1
print('COMP OK', n, 'frames ->', A.out)
