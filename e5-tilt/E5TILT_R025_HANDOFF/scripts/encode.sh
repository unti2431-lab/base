#!/usr/bin/env bash
# encode a PNG sequence + VO with an explicit BT.709 matrix (ffmpeg's default RGB->YUV is BT.601)
# usage: scripts/encode.sh <frames_dir> <out.mp4> [start_number] [audio]
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
IN="$1"; OUT="$2"; START="${3:-1}"; AUD="${4:-$ROOT/audio/R024_ORIGINAL_AUDIO.m4a}"
mkdir -p "$(dirname "$OUT")"
ffmpeg -v error -y -framerate 30 -start_number "$START" -i "$IN/%04d.png" -i "$AUD" \
  -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2:out_color_matrix=bt709:out_range=tv,format=yuv420p" \
  -c:v libx264 -profile:v high -crf 18 -preset slow \
  -colorspace bt709 -color_primaries bt709 -color_trc bt709 \
  -c:a aac -b:a 320k -ar 48000 -af apad -shortest -movflags +faststart "$OUT"
ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=width,height,r_frame_rate,nb_read_frames -of compact "$OUT"
ffmpeg -v error -i "$OUT" -f null - && echo "decode OK"
sha256sum "$OUT"
