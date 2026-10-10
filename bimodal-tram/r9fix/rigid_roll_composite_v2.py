"""바퀴 구름 2.5D 강체 합성 v2 — 바퀴 전체(타이어+림) 회전, 무미끄럼 θ = dx / R_e

v1(rim-only)의 결함: 타이어 옆면 무늬가 회전하지 않아 림과 타이어가 서로 미끄러지는
상태가 된다. v2는 허브 중심으로 바퀴 전체 텍스처를 회전시키되,
  - r <= R_IN(=200): 순수 강체 회전(림·볼트·안쪽 옆면 형상 보존)
  - R_IN < r <= 실루엣: 바깥 고무 띠만 실루엣 정규화(접지면의 평평한 바닥 유지)
로 처리한다. 접지면 바닥은 그대로 평평하고, 고무 무늬는 접지면을 통과해 돈다.

치수(LOOP_WHEEL FHD 실측): 허브 (1144.3, 481.0) · 림 147.8 · 옆면 무부하 반경 241 ·
허브→접지 231(하중 반경) · 유효 구름 반경 R_e = 241 − (241−231)/3 ≈ 238 (래디얼 타이어 근사)

사용: python3 -I rigid_roll_composite_v2.py <04_ASSETS> <출력> [이동px] [초] [R_e]
"""
import sys, math
import numpy as np
from PIL import Image, ImageFilter

A, OUT = sys.argv[1], sys.argv[2]
D = float(sys.argv[3]) if len(sys.argv) > 3 else 240.0
SEC = float(sys.argv[4]) if len(sys.argv) > 4 else 5.0
R_E = float(sys.argv[5]) if len(sys.argv) > 5 else 238.0
FPS = 24
CX, CY = 1144.3, 481.0
R_SW, CONTACT_Y, R_IN = 241.0, 712.0, 200.0

W = Image.open(f"{A}/LOOP_WHEEL_L_FHD_UPSCALED.jpg").convert('RGB')
E = Image.open(f"{A}/LOOP_EMPTY_L_FHD_UPSCALED.jpg").convert('RGB')
w, h = W.size
wa, ea = np.asarray(W).astype(float), np.asarray(E).astype(float)

# ---- 버스 알파(v1과 동일한 절차) ----
m = (np.abs(wa - ea).max(2) > 40).astype(np.uint8) * 255
mi = Image.fromarray(m).filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.MinFilter(9))
sm = np.asarray(mi.resize((w // 4, h // 4), Image.BILINEAR)) > 127
bg = ~sm; reach = np.zeros_like(bg); reach[-1, :] = bg[-1, :]; reach[:, 0] |= bg[:, 0]
while True:
    g = reach.copy()
    g[1:, :] |= reach[:-1, :]; g[:-1, :] |= reach[1:, :]; g[:, 1:] |= reach[:, :-1]; g[:, :-1] |= reach[:, 1:]
    g &= bg
    if (g == reach).all(): break
    reach = g
holes = Image.fromarray((bg & ~reach).astype(np.uint8) * 255).resize((w, h), Image.NEAREST).filter(ImageFilter.MaxFilter(5))
mi = np.maximum(np.asarray(mi), np.asarray(holes))
yy0, xx0 = np.mgrid[0:h, 0:w]
keep = np.zeros((h, w), bool); keep[:640, :] = True
keep |= (np.hypot(xx0 - CX, yy0 - CY) <= R_SW + 5) & (yy0 <= CONTACT_Y + 2)
keep[580:668, 1345:1440] = True
alpha = Image.fromarray((mi * keep).astype(np.uint8)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.5))
lw, le = wa.mean(2) + 1, ea.mean(2) + 1
shade = np.ones((h, w)); band = slice(560, 820)
shade[band] = np.clip(lw[band] / le[band], 0.25, 1.0)
shade = np.asarray(Image.fromarray((shade * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(4))).astype(float) / 255

# 오른쪽 차체 연장(이음선 없는 패널 구간 1700–1900을 반복)
EXT = int(D) + 40; strip = (1700, 1900)
bus = np.zeros((h, w + EXT, 3)); bus[:, :w] = wa
al = np.zeros((h, w + EXT)); al[:, :w] = np.asarray(alpha) / 255.0
sh = np.ones((h, w + EXT)); sh[:, :w] = shade
x0 = w
while x0 < w + EXT:
    n = min(strip[1] - strip[0], w + EXT - x0)
    bus[:, x0:x0 + n] = wa[:, strip[0]:strip[0] + n]; al[:, x0:x0 + n] = al[:, strip[0]:strip[0] + n]
    sh[:, x0:x0 + n] = sh[:, strip[0]:strip[0] + n]; x0 += n

# ---- 바퀴 텍스처 회전(실루엣 보존 극좌표 재표본) ----
B = int(R_SW + 8)
gy, gx = np.mgrid[-B:B + 1, -B:B + 1].astype(float)
def R_sil(phi):                                             # 접지선에서 잘린 원의 경계 반경
    s = np.sin(phi)
    with np.errstate(divide='ignore', invalid='ignore'):
        cut = np.where(s > 1e-6, (CONTACT_Y - CY) / s, np.inf)
    return np.minimum(R_SW, cut)
def bilinear(img, x, y):
    x = np.clip(x, 0, img.shape[1] - 1.001); y = np.clip(y, 0, img.shape[0] - 1.001)
    x0i, y0i = x.astype(int), y.astype(int); fx, fy = (x - x0i)[..., None], (y - y0i)[..., None]
    return (img[y0i, x0i] * (1 - fx) * (1 - fy) + img[y0i, x0i + 1] * fx * (1 - fy)
            + img[y0i + 1, x0i] * (1 - fx) * fy + img[y0i + 1, x0i + 1] * fx * fy)
src = wa

def ease(t):
    a, b = 0.5 / SEC, 1 - 0.5 / SEC
    if t <= a: return 0.0
    if t >= b: return 1.0
    return 0.5 - 0.5 * math.cos(math.pi * (t - a) / (b - a))

n = int(SEC * FPS)
log = open(f"{OUT}/motion_log.csv", 'w')
log.write("frame,dx_px,wheel_deg_ccw_screen,expected_deg,contact_point_velocity_px_per_frame\n")
prev = None
for i in range(n):
    dx = -D * ease(i / (n - 1))
    ix = int(round(dx))                                       # 차체·허브 모두 같은 정수 이동(서로 어긋남 0)
    theta_screen = -ix / R_E                                  # 화면상 반시계(+), 실제 적용 이동량 기준
    frame = ea * sh[:, -ix:-ix + w, None]
    a_ = al[:, -ix:-ix + w, None]
    frame = frame * (1 - a_) + bus[:, -ix:-ix + w] * a_
    hx = CX + ix; ofs = hx - math.floor(hx)                   # 허브 x의 소수부(0.3) 보정
    gxs = gx - ofs
    rr2 = np.hypot(gxs, gy); ph2 = np.arctan2(gy, gxs); Ro2 = R_sil(ph2)
    ps = ph2 + theta_screen; Rs = R_sil(ps)         # 화면 반시계 = 이미지좌표 음의 회전
    rs = np.where(rr2 <= R_IN, rr2, R_IN + (rr2 - R_IN) * (Rs - R_IN) / np.maximum(Ro2 - R_IN, 1e-6))
    patch = bilinear(src, CX + rs * np.cos(ps), CY + rs * np.sin(ps))
    em = (np.clip((Ro2 - rr2) / 1.5, 0, 1) * (rr2 <= Ro2))[..., None]
    ys, ye = int(CY) - B, int(CY) + B + 1
    xs, xe = int(math.floor(hx)) - B, int(math.floor(hx)) + B + 1
    region = frame[ys:ye, xs:xe]
    frame[ys:ye, xs:xe] = region * (1 - em) + patch * em
    Image.fromarray(np.clip(frame, 0, 255).astype(np.uint8)).save(f"{OUT}/f_{i:04d}.png")
    # 접지점 속도 = 허브 속도 + ω×r (바닥점) → v_hub - ω·R_e
    if prev is None: v = 0.0
    else: v = (ix - prev[0]) - (-(theta_screen - prev[1]) * R_E)
    log.write(f"{i},{ix},{math.degrees(theta_screen):.4f},{math.degrees(-ix / R_E):.4f},{v:.6f}\n")
    prev = (ix, theta_screen)
log.close()
print('frames', n, 'final deg', round(math.degrees(D / R_E), 3))
