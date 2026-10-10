"""출력 프레임만으로 바퀴 무미끄럼을 독립 검증한다(합성 로그는 쓰지 않음).

측정 1: 림 고리(r 60–140)와 타이어 옆면 고리(r 165–225, 접지부 하단 90° 제외)의
        회전각을 각각 회전 탐색으로 추정 → 두 값이 같아야 바퀴 전체가 한 강체로 돈다.
측정 2: 허브 이동량은 차체 패널 패치의 가로 정합으로 따로 추정 → 각 × R_e / 이동 = 1 이어야 무미끄럼.
측정 3: 노면(y>820) 첫·끝 프레임 차이 → 노면 고정.

사용: python3 -I verify_noslip.py <프레임 폴더> <R_e> [허브x 허브y] → JSON 한 줄
"""
import sys, json, glob
import numpy as np
from PIL import Image

F, R_E = sys.argv[1], float(sys.argv[2])
CX = float(sys.argv[3]) if len(sys.argv) > 3 else 1144.3
CY = float(sys.argv[4]) if len(sys.argv) > 4 else 481.0
files = sorted(glob.glob(f"{F}/f_*.png"))
L = lambda p: np.asarray(Image.open(p).convert('L')).astype(float)

def bil(img, x, y):
    x0, y0 = np.floor(x).astype(int), np.floor(y).astype(int); fx, fy = x - x0, y - y0
    return img[y0, x0]*(1-fx)*(1-fy) + img[y0, x0+1]*fx*(1-fy) + img[y0+1, x0]*(1-fx)*fy + img[y0+1, x0+1]*fx*fy

def body_shift(a, b):
    """차체 상부 패널 띠(y 60–120, x 700–1300)의 가로 이동(px, 0.1 정밀)."""
    ref = a[60:120, 700:1300]
    best = None
    for s in np.arange(-320, 20, 1.0):
        xs = np.arange(700, 1300) + s
        if xs.min() < 1 or xs.max() > 1917: continue
        v = np.abs(b[60:120][:, xs.astype(int)] - ref).mean()
        if best is None or v < best[0]: best = (v, s)
    s0 = best[1]; out = best
    for s in np.arange(s0 - 1, s0 + 1, 0.1):
        yy, xx = np.mgrid[60:120, 700:1300].astype(float)
        v = np.abs(bil(b, xx + s, yy) - ref).mean()
        if v < out[0]: out = (v, s)
    return out[1]

def ring_angle(a, b, dx, rmin, rmax, exclude_bottom, ax=0.0, grid=(-10, 90)):
    """a(첫 프레임)의 고리를 θ만큼 돌려 b(허브가 dx 이동한 프레임)와 맞춤. 화면 반시계 + (deg)."""
    yy, xx = np.mgrid[-rmax:rmax+1, -rmax:rmax+1].astype(float)
    r = np.hypot(xx, yy); m = (r >= rmin) & (r <= rmax)
    if exclude_bottom:
        ang = np.degrees(np.arctan2(yy, xx))            # 이미지 좌표: +90 = 아래
        m &= ~((ang > 45) & (ang < 135))
    px, py = xx[m], yy[m]
    tgt = bil(b, CX + dx + px, CY + py)
    def err(deg):
        t = np.radians(deg)                              # 화면 반시계 → 이미지 좌표 회전 -t
        c, s = np.cos(t), np.sin(t)
        sx, sy = c*px - s*py, s*px + c*py               # 출력점을 시계로 돌려 원본에서 표본
        return np.abs(bil(a, CX + ax + sx, CY + sy) - tgt).mean()
    grid = np.arange(grid[0], grid[1], 0.5); e = [err(d) for d in grid]; d0 = grid[int(np.argmin(e))]
    fine = np.arange(d0 - 0.5, d0 + 0.5, 0.05); ef = [err(d) for d in fine]
    return float(fine[int(np.argmin(ef))]), float(min(ef))

a = L(files[0]); res = {"frames": len(files), "R_e": R_E, "checks": []}
for k in (len(files) // 2, len(files) - 1):
    b = L(files[k]); dx = body_shift(a, b)
    rim, rim_e = ring_angle(a, b, dx, 60, 140, False)
    tyre, tyre_e = ring_angle(a, b, dx, 165, 225, True)
    exp = np.degrees(-dx / R_E)
    res["checks"].append({"frame": k, "hub_dx_px": round(dx, 2), "expected_deg": round(exp, 2),
        "rim_deg": round(rim, 2), "tyre_sidewall_deg": round(tyre, 2),
        "rim_minus_tyre_deg": round(rim - tyre, 2),
        "noslip_ratio_rim": round(rim / exp, 4) if exp else None,
        "noslip_ratio_tyre": round(tyre / exp, 4) if exp else None,
        "fit_mae": [round(rim_e, 2), round(tyre_e, 2)]})
# 0.5초(12프레임) 구간별 국소 무미끄럼 비 — R9 기준(누적비 0.9–1.1, 모든 0.5초 창 0.8–1.25)
win = []
dxs = {}
for k in range(0, len(files), 12):
    dxs[k] = body_shift(a, L(files[k])) if k else 0.0
for k in range(0, len(files) - 12, 12):
    fa, fb = L(files[k]), L(files[k + 12]); d = dxs[k + 12] - dxs[k]
    if abs(d) < 10: continue                                  # 10px 미만 이동 창은 R9와 같이 제외
    exp = np.degrees(-d / R_E)
    rim, _ = ring_angle(fa, fb, dxs[k + 12], 60, 140, False, ax=dxs[k], grid=(-3, 16))
    tyre, _ = ring_angle(fa, fb, dxs[k + 12], 165, 225, True, ax=dxs[k], grid=(-3, 16))
    win.append({"frames": [k, k + 12], "dx": round(d, 1), "expected_deg": round(exp, 2), "rim_ratio": round(rim / exp, 3), "tyre_ratio": round(tyre / exp, 3)})
res["windows_0p5s"] = win
rat = [w["rim_ratio"] for w in win] + [w["tyre_ratio"] for w in win]
res["window_ratio_minmax"] = [min(rat), max(rat)] if rat else None
b = L(files[-1]); res["road_maxdiff_y820"] = float(np.abs(a[820:] - b[820:]).max())
print(json.dumps(res, ensure_ascii=False))
