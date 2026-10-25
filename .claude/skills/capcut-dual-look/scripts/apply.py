#!/usr/bin/env python3
"""CapCut Dual Look: apply measured fixed-LUT approximations via FFmpeg.

Python stdlib only. FFmpeg and FFprobe are external prerequisites.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from typing import Any

SKILL_ROOT = Path(__file__).resolve().parents[1]
LUT_DIR = SKILL_ROOT / "assets" / "luts"
LUT_4K = LUT_DIR / "CapCut_4K_Approx_33.cube"
LUT_AUTO = LUT_DIR / "CapCut_Auto_Approx_49.cube"
LUT_FUSED = LUT_DIR / "BSK_4K_then_Auto_65.cube"
EXTENSIONS = {".mp4", ".mov", ".mkv", ".m4v", ".webm"}


def executable(name: str) -> str:
    local_name = name + (".exe" if os.name == "nt" else "")
    # FFmpeg shipped alongside skill can be used without PATH changes.
    for location in (SKILL_ROOT / local_name, SKILL_ROOT / "bin" / local_name):
        if location.is_file():
            return str(location)
    path = shutil.which(name)
    if not path:
        raise RuntimeError(f"{name} 실행 파일을 찾을 수 없습니다. FFmpeg/FFprobe를 설치하고 PATH에 추가하세요.")
    return path


def probe(ffprobe: str, video: Path) -> dict[str, Any]:
    command = [ffprobe, "-v", "error", "-select_streams", "v:0", "-show_entries",
               "stream=width,height,codec_name,pix_fmt,r_frame_rate,color_space,color_transfer,color_primaries",
               "-show_entries", "format=duration", "-of", "json", str(video)]
    proc = subprocess.run(command, capture_output=True, text=True)
    if proc.returncode:
        raise RuntimeError(f"ffprobe 확인 실패: {video}\n{proc.stderr[-800:]}")
    data = json.loads(proc.stdout)
    if not data.get("streams"):
        raise RuntimeError(f"비디오 스트림이 없습니다: {video}")
    return {"video": data["streams"][0], "format": data.get("format", {})}


def check_sdr(meta: dict[str, Any], force: bool) -> None:
    stream = meta["video"]
    values = {str(stream.get(k, "")).lower() for k in
              ("color_space", "color_transfer", "color_primaries")}
    bad = {"smpte2084", "arib-std-b67", "bt2020", "bt2020nc", "bt2020c", "smpte428"}
    if values.intersection(bad) and not force:
        raise RuntimeError("HDR/BT.2020/PQ/HLG 소스가 감지됐습니다. SDR Rec.709 변환 후 적용하거나 "
                           "색 변화 위험을 이해한 경우 --force-sdr을 사용하세요.")
    if "bt709" not in values:
        print("  [주의] Rec.709 색공간 태그가 확인되지 않습니다. 결과를 육안 검수하세요.")


def collect_inputs(inputs: list[str], recursive: bool) -> list[Path]:
    paths = []
    for x in inputs:
        p = Path(x).expanduser().resolve()
        if p.is_file():
            paths.append(p)
        elif p.is_dir():
            iterator = p.rglob("*") if recursive else p.iterdir()
            paths.extend(sorted(f.resolve() for f in iterator if f.is_file() and f.suffix.lower() in EXTENSIONS
                                and "_BSK_" not in f.stem.upper()))
        else:
            print(f"  [건너뜀] 파일이나 폴더가 없습니다: {p}", file=sys.stderr)
    return list(dict.fromkeys(paths))


def filter_graph(mode: str, order: str, engine: str, sharpen: str) -> tuple[str, list[Path]]:
    if mode == "4k":
        luts = [LUT_4K]
    elif mode == "auto":
        luts = [LUT_AUTO]
    elif engine == "fused" and order == "4k-auto":
        luts = [LUT_FUSED]
    elif order == "auto-4k":
        luts = [LUT_AUTO, LUT_4K]
    else:
        luts = [LUT_4K, LUT_AUTO]

    for lut in luts:
        if not lut.exists():
            raise RuntimeError(f"LUT를 찾을 수 없습니다: {lut}")
    # Set subprocess cwd=SKILL_ROOT to avoid absolute Windows drive-colon escaping.
    filters = [f"lut3d=file=assets/luts/{p.name}:interp=tetrahedral" for p in luts]
    if sharpen == "mild":
        # Creative enhancement ONLY: 4K LUT was recovered for color, not spatial sharpening.
        filters.append("unsharp=5:5:0.25:5:5:0.0")
    filters.append("format=yuv420p")
    return ",".join(filters), luts


def suffix_for(mode: str, order: str, sharpen: str, seconds: float | None) -> str:
    label = {"4k": "4K", "auto": "AUTO"}.get(mode,
             "4K_AUTO" if order == "4k-auto" else "AUTO_4K")
    return "_BSK_" + label + ("_SHARP" if sharpen == "mild" else "") + ("_PREVIEW" if seconds else "")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def encoder_args(encoder: str, quality: int) -> list[str]:
    if encoder == "nvenc":
        return ["-c:v", "h264_nvenc", "-preset", "p5", "-rc", "vbr", "-cq", str(quality), "-b:v", "0"]
    return ["-c:v", "libx264", "-preset", "medium", "-crf", str(quality)]


def command(ffmpeg: str, src: Path, dst: Path, vf: str, encoder: str, quality: int,
            preview: float | None, overwrite: bool, transcode_audio: bool) -> list[str]:
    cmd = [ffmpeg, "-hide_banner", "-loglevel", "warning", "-stats", "-y" if overwrite else "-n", "-i", str(src)]
    cmd += ["-map", "0:v:0", "-map", "0:a?", "-map_metadata", "0", "-map_chapters", "0"]
    if preview:
        cmd += ["-t", str(preview)]
    cmd += ["-vf", vf]
    cmd += encoder_args(encoder, quality)
    cmd += ["-pix_fmt", "yuv420p", "-c:a", "aac" if transcode_audio else "copy"]
    if transcode_audio:
        cmd += ["-b:a", "192k"]
    cmd += ["-sn", "-dn", "-movflags", "+faststart", "-color_primaries", "bt709",
            "-color_trc", "bt709", "-colorspace", "bt709", str(dst)]
    return cmd


def cli():
    ap = argparse.ArgumentParser(
        description="바삭숏 4K+Auto Adjust 고정 LUT FFmpeg 일괄 적용(캡컷 불필요)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument("inputs", nargs="+", help="영상 파일 또는 폴더(복수 가능)")
    ap.add_argument("--mode", choices=["both", "4k", "auto"], default="both", help="사용할 룩")
    ap.add_argument("--order", choices=["4k-auto", "auto-4k"], default="4k-auto", help="두 룩 적용 순서")
    ap.add_argument("--engine", choices=["fused", "chain"], default="fused", help="합성 LUT 또는 원본 두 LUT 체인")
    ap.add_argument("--encoder", choices=["auto", "cpu", "nvenc"], default="auto")
    ap.add_argument("--quality", type=int, default=18, help="CPU CRF 또는 NVENC CQ(낮을수록 고품질)")
    ap.add_argument("--sharpen", choices=["none", "mild"], default="none")
    ap.add_argument("--output-dir", type=Path, help="결과 폴더(기본: 입력 원본 옆)")
    ap.add_argument("--recursive", action="store_true", help="폴더 입력 시 하위 폴더도 검색")
    ap.add_argument("--overwrite", action="store_true", help="기존 결과 파일 덮어쓰기(원본 영상은 절대 덮지 않음)")
    ap.add_argument("--preview-seconds", type=float, default=None, help="검수용 앞부분 N초만 처리")
    ap.add_argument("--force-sdr", action="store_true", help="HDR 태그 경고를 무시하고 강제 처리(추천하지 않음)")
    ap.add_argument("--dry-run", action="store_true", help="실행 계획만 출력")
    ap.add_argument("--no-report", action="store_true", help="JSON 처리 보고서 생성을 끔")
    args = ap.parse_args()
    if not 0 <= args.quality <= 51:
        ap.error("--quality 값은 0~51")
    if args.preview_seconds is not None and args.preview_seconds <= 0:
        ap.error("--preview-seconds 값은 양수")
    ffmpeg = executable("ffmpeg")
    ffprobe = executable("ffprobe")
    vf, luts = filter_graph(args.mode, args.order, args.engine, args.sharpen)
    files = collect_inputs(args.inputs, args.recursive)
    if not files:
        ap.error("처리할 비디오 파일이 없습니다.")
    if args.output_dir:
        args.output_dir = args.output_dir.expanduser().resolve()
        if not args.dry_run:
            args.output_dir.mkdir(parents=True, exist_ok=True)
    lut_hashes = {p.name: sha256(p) for p in luts}
    print(f"모드={args.mode} 순서={args.order} 방식={args.engine} 선명화={args.sharpen}; {len(files)}개 처리")
    print(f"LUT={', '.join(p.name for p in luts)}")
    failures = 0
    for i, src in enumerate(files, 1):
        suffix = suffix_for(args.mode, args.order, args.sharpen, args.preview_seconds)
        dst = (args.output_dir or src.parent) / (src.stem + suffix + ".mp4")
        dst = dst.resolve()
        if src == dst:
            print(f"[{i}] 원본 덮어쓰기 차단: {src}", file=sys.stderr)
            failures += 1
            continue
        if dst.exists() and not args.overwrite:
            print(f"[{i}] 기존 파일 유지(건너뜀): {dst}")
            continue
        try:
            info = probe(ffprobe, src)
            check_sdr(info, args.force_sdr)
        except Exception as exc:
            print(f"[{i}] ERROR: {exc}", file=sys.stderr)
            failures += 1
            continue
        candidates = [args.encoder] if args.encoder != "auto" else ["nvenc", "cpu"]
        if args.dry_run:
            print(f"[{i}] {src}\n    → {dst}\n    원본={info['video'].get('width')}x{info['video'].get('height')}, "
                  f"fps={info['video'].get('r_frame_rate')}\n    filter={vf}\n    encoder={candidates}")
            continue
        print(f"[{i}/{len(files)}] {src.name} → {dst.name}", flush=True)
        error = None
        used_encoder = None
        audio_reencode = False
        for encoder in candidates:
            for transcode_audio in (False, True):
                cmd = command(ffmpeg, src, dst, vf, encoder, args.quality, args.preview_seconds,
                              True, transcode_audio)
                outcome = subprocess.run(cmd, cwd=SKILL_ROOT, capture_output=True, text=True)
                if outcome.returncode == 0 and dst.is_file() and dst.stat().st_size > 0:
                    used_encoder = encoder
                    audio_reencode = transcode_audio
                    break
                error = (outcome.stderr or "ffmpeg 실패").strip()[-1400:]
                if dst.exists():
                    try:
                        dst.unlink()
                    except OSError:
                        pass
                # Retry transcoding audio only when FFmpeg output suggests an audio mux issue.
                errlow = error.lower()
                if not any(k in errlow for k in ("not currently supported in container", "could not find tag",
                                                  "codec not currently supported", "tag for codec", "muxer")):
                    break
            if used_encoder:
                break
            if encoder == "nvenc" and args.encoder == "auto":
                print("    NVIDIA 인코딩 불가 → CPU libx264 자동 전환")
        if not used_encoder:
            failures += 1
            print(f"    ERROR: {error}", file=sys.stderr)
            continue
        try:
            output_probe = probe(ffprobe, dst)
        except Exception as exc:
            failures += 1
            print(f"    ERROR 출력 검증 실패: {exc}", file=sys.stderr)
            continue
        if output_probe["video"].get("width") != info["video"].get("width") or output_probe["video"].get("height") != info["video"].get("height"):
            failures += 1
            print("    ERROR: 출력 해상도가 원본과 달라졌습니다.", file=sys.stderr)
            continue
        if not args.no_report:
            report = {
                "pipeline": "capcut-dual-look v1.1", "created_utc": datetime.now(timezone.utc).isoformat(),
                "source": str(src), "output": str(dst), "mode": args.mode,
                "order": args.order if args.mode == "both" else None,
                "engine": args.engine, "filter_graph": vf,
                "luts_sha256": lut_hashes, "sharpen": args.sharpen,
                "encoder": used_encoder, "quality": args.quality, "audio_reencoded": audio_reencode,
                "source_video": info["video"], "output_video": output_probe["video"],
                "fixed_look_not_dynamic_auto_adjust": True,
                "true_capcut_combined_effect_not_measured": True,
            }
            dst.with_suffix(".grade.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"    OK ({used_encoder} / {dst.stat().st_size / 1024**2:.1f} MB)")
    print(f"완료: {len(files) - failures}개 성공 또는 기존 파일 유지, {failures}개 실패")
    return 1 if failures else 0


if __name__ == "__main__":
    try:
        sys.exit(cli())
    except (RuntimeError, OSError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(2)
