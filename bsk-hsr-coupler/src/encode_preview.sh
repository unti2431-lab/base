#!/usr/bin/env bash
# PNG sequence -> silent H.264 preview with a post-comp watermark (allowed: overlay layer, not in the 3D scene).
# usage: encode_preview.sh FRAMES_DIR OUT.mp4 "WATERMARK TEXT"
set -euo pipefail
DIR="$1"; OUT="$2"; TXT="${3:-CONCEPT_ONLY}"; FPS=30
mkdir -p "$(dirname "$OUT")"
ffmpeg -v error -y -framerate $FPS -i "$DIR/%04d.png" \
  -vf "drawtext=text='$TXT':fontsize=14:fontcolor=white@0.85:box=1:boxcolor=black@0.5:x=8:y=h-th-8,drawtext=text='F %{frame_num}':start_number=1:fontsize=14:fontcolor=white@0.85:box=1:boxcolor=black@0.5:x=w-tw-8:y=h-th-8,scale=out_color_matrix=bt709:out_range=tv,format=yuv420p" \
  -c:v libx264 -profile:v high -crf 18 -preset medium -colorspace bt709 -color_primaries bt709 -color_trc bt709 -movflags +faststart "$OUT"
ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=width,height,r_frame_rate,nb_read_frames -of compact=p=0 "$OUT"
ffmpeg -v error -i "$OUT" -f null - && echo "decode ok"
# contact sheet: 6x6 at 2 fps + 8 key frames
ffmpeg -v error -y -i "$OUT" -vf "fps=2,scale=180:-1,tile=6x6" -frames:v 1 "${OUT%.mp4}_contact.jpg"
