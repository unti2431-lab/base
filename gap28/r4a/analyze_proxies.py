#!/usr/bin/env python3
"""
GAP28 R4a — 실사 프록시 자동 계측 (GAP28_R4_REVISION_PLAN.md §2.5 선별 프로토콜)

입력: R4a_proxies/ 안의 proxy_*.mp4 (270x480, bt709, 30fps)  [make_r4a_proxies.py 출력]
출력: r4a_live_metrics.json + 클립별 후보 창(window) 표 + 콘택트 시트(타임코드 포함)

측정 항목 (프레임별)
  luma_mean   중앙 70% 영역 평균 밝기 (0-255)   STYLE 명도 기준 75-135
  motion_px   연속 프레임 위상상관 전역 이동량 → 1080x1920 기준 px/F 로 환산
              (프록시 270p 이므로 ×4). 삼각대 판정: 창 평균 < 0.5 px/F
  diff        연속 프레임 평균 절대차 (measure_rhythm.py 와 같은 정의) — 피사체 움직임 지표
  dark_pct    Y < 30 화소 비율 (틈 내부 하강 창 탐지: L2 끝, B01 이음)

창 탐색: 3.0초(90F) 슬라이딩. 슬롯별 점수 = 노출 적합 + 흔들림 적합 + 슬롯 고유 조건.
  L1 전경      흔들림 작고 노출 정상, 피사체 움직임 적당(열차 정차 상태)
  L2 하강→틈   창 끝 24F 가 어두워짐(dark_pct 상승) + 창 후반 움직임(하강)
  L3 착지      창 시작 24F 가 고정에 가깝고(전환 B 이음) 중반에 피사체 움직임 피크
  L4 빈 연단   창 후반 피사체 움직임 거의 0 + 노출 정상
이 점수는 '보기 순서'를 정하는 것이지 채택 판정이 아니다. 채택은 시트·프록시 육안 판독으로 한다.

사용:  python3 -I analyze_proxies.py <R4a_proxies 디렉터리> [--out DIR]
의존:  ffmpeg/ffprobe, numpy, Pillow
"""
import argparse
import glob
import json
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw

PROXY_W, PROXY_H = 270, 480
FULL_W = 1080
SCALE = FULL_W / PROXY_W          # 4.0
WIN_F = 90                        # 3.0 s @30fps
TRIPOD_PX = 0.5                   # px/F @1080 (계획서 §2.3)
HANDHELD_OK_PX = 1.5              # 전환 컷 흔들림 상한 (계획서 §2.5)
LUMA_LO, LUMA_HI = 75, 135


def probe(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height,r_frame_rate,nb_frames:format=duration",
         "-of", "json", path], capture_output=True, text=True, check=True).stdout
    j = json.loads(out)
    st = j["streams"][0]
    num, den = st["r_frame_rate"].split("/")
    return {"width": int(st["width"]), "height": int(st["height"]),
            "fps": float(num) / float(den), "nb_frames": int(st.get("nb_frames") or 0),
            "duration_s": float(j["format"]["duration"])}


def decode_gray(path, w, h):
    """전 프레임을 8bit 회색조 numpy (n,h,w) 로. 270p 라 메모리 부담 없음(148s ≈ 575MB 아님: 4440F×130KB ≈ 577MB → 절반 해상도로 받는다)."""
    dw, dh = w // 2, h // 2          # 135x240 — measure_rhythm.py 프로브 해상도와 동일
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", path, "-vf", f"scale={dw}:{dh}:flags=area",
         "-f", "rawvideo", "-pix_fmt", "gray", "-"],
        capture_output=True, check=True).stdout
    n = len(raw) // (dw * dh)
    return np.frombuffer(raw, np.uint8)[: n * dw * dh].reshape(n, dh, dw), dw, dh


def phase_shift(a, b):
    """위상상관으로 b 가 a 대비 얼마나 이동했는지 (dx, dy) 픽셀. Hann 창, 서브픽셀은 포물선 보간."""
    h, w = a.shape
    win = np.outer(np.hanning(h), np.hanning(w))
    fa = np.fft.fft2((a - a.mean()) * win)
    fb = np.fft.fft2((b - b.mean()) * win)
    r = fa * np.conj(fb)
    r /= np.abs(r) + 1e-9
    c = np.fft.ifft2(r).real
    iy, ix = np.unravel_index(np.argmax(c), c.shape)

    def sub(cm, c0, cp):
        d = cm - 2 * c0 + cp
        return 0.0 if abs(d) < 1e-12 else 0.5 * (cm - cp) / d
    dx = ix + sub(c[iy, (ix - 1) % w], c[iy, ix], c[iy, (ix + 1) % w])
    dy = iy + sub(c[(iy - 1) % h, ix], c[iy, ix], c[(iy + 1) % h, ix])
    if dx > w / 2:
        dx -= w
    if dy > h / 2:
        dy -= h
    return float(dx), float(dy)


def per_frame_metrics(frames, dw, dh):
    n = len(frames)
    f = frames.astype(np.float32)
    cy0, cy1 = int(dh * 0.15), int(dh * 0.85)
    cx0, cx1 = int(dw * 0.15), int(dw * 0.85)
    luma = f[:, cy0:cy1, cx0:cx1].mean(axis=(1, 2))
    dark = (frames < 30).mean(axis=(1, 2)) * 100.0
    diff = np.zeros(n)
    motion = np.zeros(n)
    half_scale = SCALE * 2.0        # 135p → 1080p
    for i in range(1, n):
        diff[i] = np.abs(f[i] - f[i - 1]).mean()
        dx, dy = phase_shift(f[i - 1], f[i])
        motion[i] = float(np.hypot(dx, dy)) * half_scale
    return luma, dark, diff, motion


def window_scores(luma, dark, diff, motion, fps):
    n = len(luma)
    W = int(round(WIN_F * fps / 30.0))
    if n < W:
        return {}
    cs = lambda a: np.concatenate([[0.0], np.cumsum(a)])  # noqa: E731
    cl, cd, cf, cm = cs(luma), cs(dark), cs(diff), cs(motion)
    tail = max(1, int(24 * fps / 30.0))
    res = {k: [] for k in ("L1", "L2", "L3", "L4")}
    for s in range(0, n - W + 1, 3):
        e = s + W
        L = (cl[e] - cl[s]) / W
        M = (cm[e] - cm[s]) / W
        D = (cf[e] - cf[s]) / W
        d_tail = (cd[e] - cd[e - tail]) / tail
        d_head = (cd[s + tail] - cd[s]) / tail
        m_head = (cm[s + tail] - cm[s]) / tail
        m_tail = (cm[e] - cm[e - tail]) / tail
        f_tail = (cf[e] - cf[e - tail]) / tail
        f_mid = (cf[e - tail] - cf[s + tail]) / max(1, W - 2 * tail)
        expo = 1.0 - min(1.0, max(0.0, max(LUMA_LO - L, L - LUMA_HI)) / 40.0)
        steady = 1.0 - min(1.0, M / (2 * HANDHELD_OK_PX))
        sc = {
            "L1": expo + steady + (1.0 - min(1.0, D / 6.0)),
            "L2": expo * 0.5 + min(1.0, (d_tail - d_head) / 30.0) + min(1.0, m_tail / 6.0),
            "L3": expo + (1.0 - min(1.0, m_head / HANDHELD_OK_PX)) + min(1.0, f_mid / 4.0),
            "L4": expo + steady + (1.0 - min(1.0, f_tail / 1.0)),
        }
        row = {"f0": s + 1, "f1": e, "t0": round(s / fps, 2), "t1": round(e / fps, 2),
               "luma": round(float(L), 1), "motion_px": round(float(M), 2),
               "diff": round(float(D), 2), "dark_tail_pct": round(float(d_tail), 1),
               "tripod": bool(M < TRIPOD_PX)}
        for k in res:
            res[k].append((sc[k], row))
    out = {}
    for k, lst in res.items():
        lst.sort(key=lambda x: -x[0])
        picked, used = [], []
        for scv, row in lst:                      # 겹치지 않는 상위 3개
            if all(abs(row["f0"] - u) >= W // 2 for u in used):
                picked.append({"score": round(float(scv), 2), **row})
                used.append(row["f0"])
            if len(picked) == 3:
                break
        out[k] = picked
    return out


def contact_sheet(path, meta, luma, motion, out_jpg, cols=6, rows=5):
    """타임코드·밝기·흔들림을 셀에 찍은 콘택트 시트. 셀 = 클립을 cols*rows 등분."""
    n = meta["nb_frames"] or int(meta["duration_s"] * meta["fps"])
    cells = cols * rows
    idx = [int(i * (n - 1) / max(1, cells - 1)) for i in range(cells)]
    sel = "+".join(f"eq(n\\,{i})" for i in idx)
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", path, "-vf", f"select='{sel}',scale=135:240",
         "-vsync", "0", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
        capture_output=True, check=True).stdout
    k = len(raw) // (135 * 240 * 3)
    imgs = np.frombuffer(raw, np.uint8)[: k * 135 * 240 * 3].reshape(k, 240, 135, 3)
    sheet = Image.new("RGB", (cols * 135, rows * 240), (0, 0, 0))
    dr = ImageDraw.Draw(sheet)
    for j in range(k):
        x, y = (j % cols) * 135, (j // cols) * 240
        sheet.paste(Image.fromarray(imgs[j]), (x, y))
        fi = idx[j]
        t = fi / meta["fps"]
        lab = f"F{fi + 1} {t:5.2f}s"
        dr.rectangle([x, y, x + 134, y + 26], fill=(0, 0, 0))
        dr.text((x + 3, y + 2), lab, fill=(255, 220, 0))
        dr.text((x + 3, y + 14), f"Y{luma[min(fi, len(luma) - 1)]:.0f} m{motion[min(fi, len(motion) - 1)]:.1f}",
                fill=(180, 255, 180))
    sheet.save(out_jpg, quality=85)


def analyze(path, out_dir):
    meta = probe(path)
    frames, dw, dh = decode_gray(path, meta["width"], meta["height"])
    meta["nb_frames"] = len(frames)
    luma, dark, diff, motion = per_frame_metrics(frames, dw, dh)
    name = os.path.splitext(os.path.basename(path))[0].replace("proxy_", "")
    m = motion[1:] if len(motion) > 1 else motion
    summary = {
        "clip": name, "frames": int(len(frames)), "duration_s": round(meta["duration_s"], 3),
        "fps": meta["fps"],
        "luma_mean": round(float(luma.mean()), 1),
        "luma_in_range_pct": round(float(((luma >= LUMA_LO) & (luma <= LUMA_HI)).mean() * 100), 1),
        "motion_px_median": round(float(np.median(m)), 2),
        "motion_px_p90": round(float(np.percentile(m, 90)), 2),
        "tripod_overall": bool(np.median(m) < TRIPOD_PX),
        "diff_median": round(float(np.median(diff[1:])), 2) if len(diff) > 1 else 0.0,
        "dark_pct_max": round(float(dark.max()), 1),
        "windows": window_scores(luma, dark, diff, motion, meta["fps"]),
    }
    np.savez_compressed(os.path.join(out_dir, f"metrics_{name}.npz"),
                        luma=luma, dark=dark, diff=diff, motion=motion)
    contact_sheet(path, meta, luma, motion, os.path.join(out_dir, f"contact_{name}.jpg"))
    return summary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    out = a.out or os.path.join(a.src, "r4a_metrics")
    os.makedirs(out, exist_ok=True)
    files = sorted(glob.glob(os.path.join(a.src, "proxy_*.mp4")))
    if not files:
        print("proxy_*.mp4 없음:", a.src)
        return 1
    rows = []
    for p in files:
        print("계측:", os.path.basename(p), flush=True)
        rows.append(analyze(p, out))
    with open(os.path.join(out, "r4a_live_metrics.json"), "w", encoding="utf-8") as f:
        json.dump({"tripod_px": TRIPOD_PX, "handheld_ok_px": HANDHELD_OK_PX,
                   "luma_range": [LUMA_LO, LUMA_HI], "clips": rows}, f, ensure_ascii=False, indent=1)
    print(f"\n{'clip':<16}{'s':>7}{'F':>6}{'Y':>6}{'Y%':>6}{'mot_med':>8}{'mot_p90':>8}{'tripod':>7}{'dark%':>6}")
    for r in rows:
        print(f"{r['clip']:<16}{r['duration_s']:>7.1f}{r['frames']:>6}{r['luma_mean']:>6.0f}"
              f"{r['luma_in_range_pct']:>6.0f}{r['motion_px_median']:>8.2f}{r['motion_px_p90']:>8.2f}"
              f"{str(r['tripod_overall']):>7}{r['dark_pct_max']:>6.0f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
