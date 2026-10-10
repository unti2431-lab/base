"""바퀴 구름 2.5D 강체 합성 (생성 없음, 무미끄럼이 구성상 보장됨)

입력: LOOP_WHEEL(버스 있음)과 LOOP_EMPTY(같은 카메라의 빈 노면 클린 플레이트)
처리: 두 장의 차이로 버스 알파를 만들고, 버스를 dx만큼 평행이동하면서
      림(휠 디스크)만 θ = dx / R 로 회전시켜 덧입힌다.
출력: 프레임 PNG 시퀀스 → ffmpeg로 MP4

사용: python3 -I rigid_roll_composite.py <04_ASSETS 경로> <출력 폴더> [이동px] [초]
"""
import sys, math
import numpy as np
from PIL import Image, ImageFilter

A, OUT = sys.argv[1], sys.argv[2]
D = float(sys.argv[3]) if len(sys.argv) > 3 else 240.0      # 총 좌측 이동량(px, FHD)
SEC = float(sys.argv[4]) if len(sys.argv) > 4 else 5.0
FPS = 24
HUB = (1146.0, 482.0)   # 허브 중심(FHD) — wheel_crop 실측
R_RIM = 150             # 림 디스크 반경(회전 레이어)
R_ROLL = 232.0          # 유효 구름 반경(허브~접지면)

W = Image.open(f"{A}/LOOP_WHEEL_L_FHD_UPSCALED.jpg").convert('RGB')
E = Image.open(f"{A}/LOOP_EMPTY_L_FHD_UPSCALED.jpg").convert('RGB')
w, h = W.size
wa, ea = np.asarray(W).astype(int), np.asarray(E).astype(int)

# 1) 버스 알파: 클린 플레이트와의 차이 → 닫힘 연산 → 가장자리 페더
m = (np.abs(wa - ea).max(2) > 40).astype(np.uint8) * 255
mi = Image.fromarray(m).filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.MinFilter(9))
# 차체 내부 구멍 채우기: 왼쪽·아래 테두리에서 이어지는 배경만 배경으로 인정(1/4 해상도 BFS)
sm = np.asarray(mi.resize((w // 4, h // 4), Image.BILINEAR)) > 127
bg = ~sm
reach = np.zeros_like(bg); reach[-1, :] = bg[-1, :]; reach[:, 0] |= bg[:, 0]
while True:
    g = reach.copy()
    g[1:, :] |= reach[:-1, :]; g[:-1, :] |= reach[1:, :]; g[:, 1:] |= reach[:, :-1]; g[:, :-1] |= reach[:, 1:]
    g &= bg
    if (g == reach).all(): break
    reach = g
holes = Image.fromarray((bg & ~reach).astype(np.uint8) * 255).resize((w, h), Image.NEAREST).filter(ImageFilter.MaxFilter(5))
mi = Image.fromarray(np.maximum(np.asarray(mi), np.asarray(holes)))
# 노면 띠는 버스 레이어에서 제외(노면 질감이 버스와 함께 흐르는 groundcrawl 방지):
# 차체 하단선 위 + 바퀴 원 + 머드플랩만 버스로 남기고, 그림자는 밝기 비율 맵으로만 옮긴다
SKIRT_Y = 640
keep = np.zeros((h, w), bool); keep[:SKIRT_Y, :] = True
yy0, xx0 = np.mgrid[0:h, 0:w]
keep |= np.hypot(xx0 - HUB[0], yy0 - HUB[1]) <= 246
keep[580:668, 1345:1440] = True
mi = Image.fromarray((np.asarray(mi) * keep).astype(np.uint8))
mi = mi.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.5))
lw, le = wa.mean(2) + 1, ea.mean(2) + 1
shade = np.ones((h, w)); band = slice(560, 820)
shade[band] = np.clip(lw[band] / le[band], 0.25, 1.0)
shade = np.asarray(Image.fromarray((shade * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(4))).astype(float) / 255
mi.resize((960, 540)).save(f"{OUT}/alpha_preview.png")

# 2) 오른쪽 가장자리 연장: 이동으로 드러나는 차체를 무늬 없는 패널 띠로 채움
EXT = int(D) + 40
strip = (1620, 0, 1920, h)
bus = Image.new('RGB', (w + EXT, h)); alpha = Image.new('L', (w + EXT, h), 0)
bus.paste(W, (0, 0)); alpha.paste(mi, (0, 0))
for x0 in range(w, w + EXT, strip[2] - strip[0]):
    bus.paste(W.crop(strip), (x0, 0)); alpha.paste(mi.crop(strip), (x0, 0))
shade_ext = np.ones((h, w + EXT)); shade_ext[:, :w] = shade
for x0 in range(w, w + EXT, strip[2] - strip[0]):
    seg = shade[:, strip[0]:strip[2]][:, :max(0, min(strip[2] - strip[0], w + EXT - x0))]
    shade_ext[:, x0:x0 + seg.shape[1]] = seg

# 3) 림 디스크 레이어
cx, cy = HUB
box = (int(cx - R_RIM), int(cy - R_RIM), int(cx + R_RIM), int(cy + R_RIM))
rim = W.crop(box)
yy, xx = np.mgrid[0:2 * R_RIM, 0:2 * R_RIM]
disc = Image.fromarray((np.clip(R_RIM - np.hypot(xx - R_RIM + .5, yy - R_RIM + .5), 0, 1.5) / 1.5 * 255).astype(np.uint8))

def ease(t):  # 0.5초 정지 → 이동(사인 가감속) → 0.5초 정지
    a, b = 0.5 / SEC, 1 - 0.5 / SEC
    if t <= a: return 0.0
    if t >= b: return 1.0
    u = (t - a) / (b - a)
    return 0.5 - 0.5 * math.cos(math.pi * u)

n = int(SEC * FPS)
log = []
for i in range(n):
    dx = -D * ease(i / (n - 1))
    theta = -dx / R_ROLL                     # rad, 왼쪽 이동 → 반시계
    ix = int(round(dx))
    sh = shade_ext[:, -ix:-ix + w] if ix <= 0 else shade_ext[:, :w]
    frame = Image.fromarray(np.clip(ea * sh[..., None], 0, 255).astype(np.uint8))
    frame.paste(bus.crop((-ix, 0, -ix + w, h)) if ix <= 0 else bus.crop((0, 0, w, h)),
                (0, 0), alpha.crop((-ix, 0, -ix + w, h)))
    r = rim.rotate(math.degrees(theta), resample=Image.BICUBIC)
    frame.paste(r, (box[0] + ix, box[1]), disc)
    frame.save(f"{OUT}/f_{i:04d}.png")
    log.append((i, round(dx, 2), round(math.degrees(theta), 3)))

with open(f"{OUT}/motion_log.csv", 'w') as f:
    f.write("frame,dx_px,rim_deg_ccw,ratio_deg_per_px\n")
    for i, dx, deg in log:
        f.write(f"{i},{dx},{deg},{(deg / -dx if dx else 0):.5f}\n")
print('frames', n, 'final dx', log[-1][1], 'final deg', log[-1][2], 'expected deg', round(math.degrees(D / R_ROLL), 3))
