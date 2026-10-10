"""센서 합성의 강체성 독립 검증: 출력 프레임 − 클린 플레이트 차이로 센서 영역을 잡아
프레임별 위끝·아래끝·폭·중심x와 시편 윗면까지의 틈을 측정한다(합성 로그 미사용).
사용: python3 -I verify_sensor.py <프레임 폴더(f_*.png, MAG_CLEAN_PLATE_test.png 포함)>"""
import sys, glob, json
import numpy as np
from PIL import Image
F = sys.argv[1]
plate = np.asarray(Image.open(f"{F}/MAG_CLEAN_PLATE_test.png").convert('L')).astype(float)
SPEC_TOP = None
rows = []
for p in sorted(glob.glob(f"{F}/f_*.png")):
    a = np.asarray(Image.open(p).convert('L')).astype(float)
    d = np.abs(a - plate)[100:420] > 25
    ys, xs = np.nonzero(d)
    if not len(ys): continue
    cols = np.nonzero(d.sum(0) > 20)[0]           # 센서가 차지한 열(잡음 제거)
    rws = np.nonzero(d.sum(1) > 40)[0]
    rows.append(dict(top=int(rws.min()) + 100, bottom=int(rws.max()) + 100,
                     width=int(cols.max() - cols.min() + 1), cx=float((cols.max() + cols.min()) / 2)))
# 시편 윗면: 첫 프레임 원본에서 센서 아래 첫 밝기 급변(열 960 기준)
a0 = np.asarray(Image.open(sorted(glob.glob(f"{F}/f_*.png"))[0]).convert('L')).astype(float)
col = a0[380:560, 900:1020].mean(1); spec_top = int(np.argmax(np.abs(np.diff(col)))) + 380
T = np.array([r['top'] for r in rows]); Bm = np.array([r['bottom'] for r in rows]); Wd = np.array([r['width'] for r in rows])
out = dict(frames=len(rows), top_minmax=[int(T.min()), int(T.max())], bottom_minmax=[int(Bm.min()), int(Bm.max())],
           width_minmax=[int(Wd.min()), int(Wd.max())], cx_range=[round(rows[0]['cx'], 1), round(rows[-1]['cx'], 1)],
           specimen_top_y=spec_top, gap_px_minmax=[int(spec_top - Bm.max()), int(spec_top - Bm.min())],
           monotonic_x=bool(np.all(np.diff([r['cx'] for r in rows]) >= -0.5)))
print(json.dumps(out, ensure_ascii=False))
