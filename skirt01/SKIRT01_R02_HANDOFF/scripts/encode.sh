#!/usr/bin/env bash
# 사용: bash scripts/encode.sh <png_dir> <fps> <out.mp4> [mix.wav]
# 색 행렬 명시(BT.601 함정 방지). 홀수 해상도는 짝수로.
set -euo pipefail
D=$1; FPS=$2; OUT=$3; WAV=${4:-}
A=(); [ -n "$WAV" ] && A=(-i "$WAV" -c:a aac -b:a 320k -ar 48000 -shortest)
ffmpeg -y -framerate "$FPS" -i "$D/%04d.png" "${A[@]}" \
  -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2,scale=out_color_matrix=bt709:out_range=tv,format=yuv420p" \
  -c:v libx264 -profile:v high -crf 16 -preset slow \
  -colorspace bt709 -color_primaries bt709 -color_trc bt709 -movflags +faststart "$OUT"
ffprobe -v error -count_frames -show_entries stream=width,height,r_frame_rate,nb_read_frames -of compact "$OUT"
ffmpeg -v error -i "$OUT" -f null - && echo "decode OK"
