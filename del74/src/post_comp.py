"""후합성 (2.5D 레이어, 3D 씬 밖). 입력: render/passes_exr/*.exr(depth,index,ghost_index,electric,normal) + render/passes/combined 16bit PNG + src/del74_bake.npz
출력: render/comp/####.png (최종 프레임). 발광·색은 전부 여기서만. 실행: python post_comp.py --frames 1-1416 [--root ../render]
의존: numpy, OpenEXR 또는 imageio[freeimage]; 없으면 PNG 16bit 패스만으로 동작(깊이 엣지는 normal 기준)."""
import os, sys, json, argparse
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
ap = argparse.ArgumentParser(); ap.add_argument('--frames', default='1-1416'); ap.add_argument('--root', default=os.path.join(ROOT, 'render')); ap.add_argument('--preview', action='store_true')
a = ap.parse_args()
lo, hi = [int(x) for x in a.frames.split('-')] if '-' in a.frames else (int(a.frames), int(a.frames))
B = np.load(os.path.join(HERE, 'del74_bake.npz')); FR = B['frames']; ix = lambda f: int(np.where(FR == f)[0][0])
STYLE = {'cyan': np.array([0.20, 0.95, 0.90]), 'edge': np.array([0.82, 0.84, 0.86]), 'rim': np.array([1.0, 1.0, 1.0]), 'ghost_dash': np.array([0.80, 0.80, 0.80])}
IDX = {'body': 1, 'engine_block': 2, 'gen_case': 3, 'cable': 4, 'bogie_frame': 5, 'ghost_shaft': 11, 'gearbox': 12, 'clutch': 13, 'driveshaft': 14, 'motor': [20, 21, 22], 'rims': list(range(30, 35))}

def read_png16(path):
    from PIL import Image
    im = np.asarray(Image.open(path)).astype(np.float32)
    return im / 65535.0 if im.max() > 255 else im / 255.0
def read_exr(path):
    """멀티채널 EXR → (H,W) 또는 (H,W,3). Normal은 X/Y/Z, 나머지는 R/G/B(동일값) 또는 단일 채널."""
    try:
        import OpenEXR, Imath
        f = OpenEXR.InputFile(path); h = f.header(); dw = h['dataWindow']; W, H = dw.max.x - dw.min.x + 1, dw.max.y - dw.min.y + 1
        chs = set(h['channels'].keys())
        names = ['X', 'Y', 'Z'] if {'X', 'Y', 'Z'} <= chs else (['R', 'G', 'B'] if {'R', 'G', 'B'} <= chs else [sorted(chs)[0]])
        arrs = [np.frombuffer(f.channel(c, Imath.PixelType(Imath.PixelType.FLOAT)), dtype=np.float32).reshape(H, W) for c in names]
        return np.stack(arrs, -1) if len(arrs) > 1 else arrs[0]
    except ImportError:
        import imageio.v3 as iio
        return iio.imread(path).astype(np.float32)
def sobel(img):
    gx = np.zeros_like(img); gy = np.zeros_like(img)
    gx[:, 1:-1] = img[:, 2:] - img[:, :-2]; gy[1:-1, :] = img[2:, :] - img[:-2, :]
    return np.sqrt(gx ** 2 + gy ** 2)
def mask_edge(mask):
    m = mask.astype(np.float32); return np.clip(sobel(m), 0, 1)
def dash(mask_edge_img, period=14, duty=0.55):
    H, W = mask_edge_img.shape; yy, xx = np.mgrid[0:H, 0:W]
    pat = ((xx + yy) % period) < period * duty
    return mask_edge_img * pat
def srgb(x): return np.where(x <= 0.0031308, 12.92 * x, 1.055 * np.power(np.clip(x, 0, 1), 1 / 2.4) - 0.055)

os.makedirs(os.path.join(a.root, 'comp'), exist_ok=True)
for F in range(lo, hi + 1):
    tag = f'{F:04d}'
    comb = read_png16(os.path.join(a.root, 'passes', f'combined{tag}.png'))[..., :3]   # File Output PNG = AgX 적용된 디스플레이 참조. 오버레이는 이 공간에서 더한다.
    try:
        idx = np.rint(read_exr(os.path.join(a.root, 'passes_exr', f'index{tag}.exr'))).astype(int)
        gidx = np.rint(read_exr(os.path.join(a.root, 'passes_exr', f'ghost_index{tag}.exr'))).astype(int)
        elec = read_exr(os.path.join(a.root, 'passes_exr', f'electric{tag}.exr'))
        nrm = read_exr(os.path.join(a.root, 'passes_exr', f'normal{tag}.exr'))
        dep = read_exr(os.path.join(a.root, 'passes_exr', f'depth{tag}.exr'))
    except FileNotFoundError:
        print('passes missing for', F); continue
    if idx.ndim == 3: idx = idx[..., 0]
    if gidx.ndim == 3: gidx = gidx[..., 0]
    if elec.ndim == 3: elec = elec[..., 0]
    if dep.ndim == 3: dep = dep[..., 0]
    out = comb.copy(); i = ix(F)
    # D1 엣지 라인: 외피 고스트 강도 × (법선·깊이 불연속) × 내부 부품 영역(외피 자체 제외)
    sg = float(B['skin_ghost'][i])
    if sg > 0:
        e = np.clip(sobel(nrm[..., 0]) + sobel(nrm[..., 1]) + sobel(nrm[..., 2]), 0, 1) * 0.6 + np.clip(sobel(np.log1p(np.nan_to_num(dep, posinf=0))) * 4, 0, 1) * 0.4
        inside = (idx != IDX['body']) & (idx > 0)
        line = np.clip(e * inside, 0, 1) * sg * 0.55
        out = out * (1 - line[..., None]) + STYLE['edge'] * line[..., None]
    # D2 커터 림: GHOST 레이어 IndexOB 30–34 (가림 반영)
    rimm = np.isin(gidx, IDX['rims']).astype(np.float32)
    if rimm.any(): out = out * (1 - rimm[..., None] * 0.9) + STYLE['rim'] * rimm[..., None] * 0.9
    # D5 청록 펄스: 케이블 u 대비 가우시안 꼬리(앞 짧고 뒤 길게)
    u_t = float(B['electric_u'][i])
    if u_t >= 0:
        cab = idx == IDX['cable']; d = u_t - elec
        pulse = np.where(d >= 0, np.exp(-(d / 0.12) ** 2), np.exp(-(d / 0.03) ** 2)) * cab
        out = out + STYLE['cyan'] * (pulse * 1.4)[..., None]
    for k, m_idx in enumerate(IDX['motor']):          # 전동기 점등(테두리 펄스)
        s = float(B['motor_pulse'][i, k]) if k < B['motor_pulse'].shape[1] else 0.0
        if s > 0:
            me_ = mask_edge(idx == m_idx); out = out + STYLE['cyan'] * (me_ * s * 1.2)[..., None]
    # D6 유령 점선 윤곽: GHOST 레이어 IndexOB 11–14 × 베이크 강도
    for key, gi in (('ghost_vis', 11), ('gearbox', 12), ('clutch', 13), ('driveshaft', 14)):
        s = float(B[key][i])
        if s > 0:
            dl = dash(mask_edge(gidx == gi)) * s
            out = out * (1 - dl[..., None]) + STYLE['ghost_dash'] * dl[..., None]
    from PIL import Image
    Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8)).save(os.path.join(a.root, 'comp', f'{tag}.png'))   # 이미 디스플레이 참조이므로 재인코딩 없음
    print('comp', F, flush=True)
