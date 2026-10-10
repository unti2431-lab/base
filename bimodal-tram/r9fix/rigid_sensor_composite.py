"""센서 비접촉 통과 2.5D 강체 합성 (생성 없음, 높이·틈·형상이 구성상 고정됨)

MAG 정지 이미지에서 센서 상자+브래킷 두 개를 한 덩어리 레이어로 잘라내고,
가려진 배경은 좌우 경계열 행별 보간(흐린 실험실 배경)으로 채운 클린 플레이트를 만든다.
레이어는 보(beam) 아래를 따라 수평으로만 이동한다 → y·크기·틈 변화 0.

사용: python3 -I rigid_sensor_composite.py <04_ASSETS> <출력 폴더> [진폭px] [초]
"""
import sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

A, OUT = sys.argv[1], sys.argv[2]
AMP = float(sys.argv[3]) if len(sys.argv) > 3 else 300.0
SEC = float(sys.argv[4]) if len(sys.argv) > 4 else 5.0
FPS = 24
src = Image.open(f"{A}/MAG_L_FHD_UPSCALED.jpg").convert('RGB')
w, h = src.size
a = np.asarray(src).astype(float)

# 1) 강체 레이어 마스크(상자 + 좌우 브래킷 + 힌지) — MAG 실측 좌표(FHD)
mask = Image.new('L', (w, h), 0); d = ImageDraw.Draw(mask)
d.rounded_rectangle((664, 157, 1259, 368), 14, fill=255)      # 센서 상자
d.rounded_rectangle((506, 104, 652, 302), 10, fill=255)       # 왼쪽 브래킷
d.rounded_rectangle((1276, 104, 1416, 302), 10, fill=255)     # 오른쪽 브래킷
d.rectangle((640, 210, 680, 302), fill=255); d.rectangle((1250, 210, 1290, 302), fill=255)  # 힌지
mask = mask.filter(ImageFilter.GaussianBlur(1.2))

# 2) 클린 플레이트: 영역 [L,R)×[T,B) 를 행별 선형 보간 + 약한 블러
L, R, T, B = 488, 1432, 100, 376
plate = a.copy()
left = a[T:B, L - 6:L].mean(1); right = a[T:B, R:R + 6].mean(1)
t = np.linspace(0, 1, R - L)[None, :, None]
plate[T:B, L:R] = left[:, None, :] * (1 - t) + right[:, None, :] * t
pl = Image.fromarray(plate.astype(np.uint8))
blur = pl.crop((L - 20, T - 4, R + 20, B + 4)).filter(ImageFilter.GaussianBlur(6))
pl.paste(blur.crop((20, 4, 20 + R - L, 4 + B - T)), (L, T))
beam_rows = a[0:T, :, :]                                      # 보(beam)는 원본 유지
pl = np.asarray(pl).copy(); pl[0:T] = beam_rows
plate = Image.fromarray(pl.astype(np.uint8))
plate.save(f"{OUT}/MAG_CLEAN_PLATE_test.png")

def pos(t):  # 0.5초 정지 → 좌(-AMP)에서 우(+AMP)로 사인 가감속 → 0.5초 정지
    a0, b0 = 0.5 / SEC, 1 - 0.5 / SEC
    u = 0 if t <= a0 else 1 if t >= b0 else (t - a0) / (b0 - a0)
    return -AMP + 2 * AMP * (0.5 - 0.5 * math.cos(math.pi * u))

n = int(SEC * FPS)
with open(f"{OUT}/motion_log.csv", 'w') as f:
    f.write("frame,dx_px,dy_px,scale\n")
    for i in range(n):
        dx = int(round(pos(i / (n - 1))))
        fr = plate.copy()
        layer = Image.new('RGB', (w, h)); lm = Image.new('L', (w, h), 0)
        layer.paste(src, (dx, 0)); lm.paste(mask, (dx, 0))
        fr.paste(layer, (0, 0), lm)
        fr.save(f"{OUT}/f_{i:04d}.png")
        f.write(f"{i},{dx},0,1.0\n")
print('frames', n)
