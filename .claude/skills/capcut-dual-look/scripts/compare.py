#!/usr/bin/env python3
"""CapCut Dual Look: 4분할 비교(원본 | 4K / Auto | 4K→Auto) 이미지·짧은 영상 생성.

룩을 전체 영상에 적용하기 전에 한 프레임(또는 몇 초)을 네 가지 상태로 나란히 놓고
과채도·블랙 클리핑·흰 엣지·메탈 디테일 손실을 눈으로 확인하기 위한 QC 도구다.

Python 표준 라이브러리만 사용. FFmpeg/FFprobe는 외부 필수 조건.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys

SKILL_ROOT = Path(__file__).resolve().parents[1]
LUT_REL = {
    "4k": "assets/luts/CapCut_4K_Approx_33.cube",
    "auto": "assets/luts/CapCut_Auto_Approx_49.cube",
    "both": "assets/luts/BSK_4K_then_Auto_65.cube",
}
EXTENSIONS = {".mp4", ".mov", ".mkv", ".m4v", ".webm"}
# 2x2 배치: 좌상 원본, 우상 4K, 좌하 Auto, 우하 4K→Auto
PANELS = [("ORIGINAL", None), ("4K", "4k"), ("AUTO", "auto"), ("4K+AUTO", "both")]


def executable(name: str) -> str:
    local_name = name + (".exe" if os.name == "nt" else "")
    for location in (SKILL_ROOT / local_name, SKILL_ROOT / "bin" / local_name):
        if location.is_file():
            return str(location)
    path = shutil.which(name)
    if not path:
        raise RuntimeError(f"{name} 실행 파일을 찾을 수 없습니다. FFmpeg/FFprobe를 설치하고 PATH에 추가하세요.")
    return path


def collect_inputs(inputs: list[str]) -> list[Path]:
    paths: list[Path] = []
    for x in inputs:
        p = Path(x).expanduser().resolve()
        if p.is_file():
            paths.append(p)
        elif p.is_dir():
            paths.extend(sorted(f.resolve() for f in p.iterdir()
                                if f.is_file() and f.suffix.lower() in EXTENSIONS
                                and "_BSK_" not in f.stem.upper()))
        else:
            print(f"  [건너뜀] 파일이나 폴더가 없습니다: {p}", file=sys.stderr)
    return list(dict.fromkeys(paths))


def graph(scale: float, labels: bool) -> str:
    for rel in LUT_REL.values():
        if not (SKILL_ROOT / rel).exists():
            raise RuntimeError(f"LUT를 찾을 수 없습니다: {SKILL_ROOT / rel}")
    # 각 패널을 짝수 치수로 축소한 뒤 4개로 분기
    parts = [f"[0:v]scale=trunc(iw*{scale}/2)*2:trunc(ih*{scale}/2)*2,format=rgb24,split=4[p0][p1][p2][p3]"]
    outs = []
    for i, (label, key) in enumerate(PANELS):
        chain = []
        if key:
            chain.append(f"lut3d=file={LUT_REL[key]}:interp=tetrahedral")
        if labels:
            chain.append(f"drawtext=text='{label}':x=16:y=16:fontsize=h/28:fontcolor=white:"
                         f"box=1:boxcolor=black@0.55:boxborderw=8")
        if not chain:
            chain.append("null")
        parts.append(f"[p{i}]{','.join(chain)}[q{i}]")
        outs.append(f"[q{i}]")
    parts.append(f"{''.join(outs)}xstack=inputs=4:layout=0_0|w0_0|0_h0|w0_h0,format=yuv420p[out]")
    return ";".join(parts)


def run_ffmpeg(ffmpeg: str, src: Path, dst: Path, at: float, seconds: float | None,
               scale: float, labels: bool) -> subprocess.CompletedProcess:
    cmd = [ffmpeg, "-hide_banner", "-loglevel", "error", "-y", "-ss", str(at), "-i", str(src)]
    if seconds:
        cmd += ["-t", str(seconds)]
    cmd += ["-filter_complex", graph(scale, labels), "-map", "[out]"]
    if seconds:
        cmd += ["-an", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                "-movflags", "+faststart"]
    else:
        cmd += ["-frames:v", "1", "-q:v", "2"]
    cmd.append(str(dst))
    # LUT 경로를 상대 경로로 쓰기 위해 스킬 루트에서 실행(Windows 드라이브 콜론 이스케이프 회피)
    return subprocess.run(cmd, cwd=SKILL_ROOT, capture_output=True, text=True)


def cli() -> int:
    ap = argparse.ArgumentParser(
        description="원본 | 4K / Auto | 4K→Auto 4분할 비교 이미지(기본) 또는 짧은 영상 생성",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument("inputs", nargs="+", help="영상 파일 또는 폴더(복수 가능)")
    ap.add_argument("--at", type=float, default=1.0, help="비교할 시점(초)")
    ap.add_argument("--video", type=float, default=None, help="지정하면 N초짜리 4분할 MP4도 생성")
    ap.add_argument("--scale", type=float, default=0.5, help="패널별 축소 배율(1080x1920 원본이면 0.5 권장)")
    ap.add_argument("--output-dir", type=Path, help="결과 폴더(기본: 입력 원본 옆)")
    ap.add_argument("--no-labels", action="store_true", help="패널 라벨 텍스트 생략")
    args = ap.parse_args()
    if not 0.1 <= args.scale <= 1.0:
        ap.error("--scale 값은 0.1~1.0")
    if args.at < 0:
        ap.error("--at 값은 0 이상")
    if args.video is not None and args.video <= 0:
        ap.error("--video 값은 양수")

    ffmpeg = executable("ffmpeg")
    files = collect_inputs(args.inputs)
    if not files:
        ap.error("처리할 비디오 파일이 없습니다.")
    if args.output_dir:
        args.output_dir = args.output_dir.expanduser().resolve()
        args.output_dir.mkdir(parents=True, exist_ok=True)

    failures = 0
    for i, src in enumerate(files, 1):
        out_dir = args.output_dir or src.parent
        jobs = [(out_dir / f"{src.stem}_BSK_COMPARE_{args.at:g}s.jpg", None)]
        if args.video:
            jobs.append((out_dir / f"{src.stem}_BSK_COMPARE_{args.video:g}s.mp4", args.video))
        for dst, seconds in jobs:
            labels = not args.no_labels
            result = run_ffmpeg(ffmpeg, src, dst, args.at, seconds, args.scale, labels)
            if result.returncode and labels and "drawtext" in (result.stderr or "").lower():
                # 글꼴이 없는 환경에서는 라벨 없이 재시도. 배치는 좌상 원본, 우상 4K, 좌하 Auto, 우하 4K→Auto.
                print("    [주의] drawtext 글꼴을 찾지 못해 라벨 없이 생성합니다.")
                result = run_ffmpeg(ffmpeg, src, dst, args.at, seconds, args.scale, False)
            if result.returncode or not dst.is_file() or dst.stat().st_size == 0:
                failures += 1
                print(f"[{i}] ERROR {src.name}: {(result.stderr or 'ffmpeg 실패').strip()[-1200:]}", file=sys.stderr)
                continue
            print(f"[{i}/{len(files)}] {src.name} → {dst.name}")
    print("패널 배치: 좌상 원본 | 우상 4K / 좌하 Auto | 우하 4K→Auto(기본 결합)")
    print(f"완료: {len(files) - failures}개 성공, {failures}개 실패")
    return 1 if failures else 0


if __name__ == "__main__":
    try:
        sys.exit(cli())
    except (RuntimeError, OSError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(2)
