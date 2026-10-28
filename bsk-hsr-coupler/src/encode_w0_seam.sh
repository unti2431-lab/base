#!/usr/bin/env bash
# W0 seam review: plays shot13 (F1186-1260) straight into shot01-02 (F1-120), i.e. across the loop seam F1260 -> F1.
# The world frame number is burned in (post-comp overlay, not in the 3D scene).  usage: encode_w0_seam.sh FRAMES_DIR OUT.mp4
set -euo pipefail
DIR="$1"; OUT="$2"; FPS=30; FONT="${FONT:-/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf}"
mkdir -p "$(dirname "$OUT")"; TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
i=0; for f in $(seq 1186 1260) $(seq 1 120); do i=$((i+1)); ln -s "$(realpath "$DIR/$(printf %04d "$f").png")" "$TMP/$(printf %04d "$i").png"; echo "$f" >> "$TMP/map.txt"; done
# per-output-frame world F label via sendcmd-free trick: output frame n<=75 -> F=1185+n, else F=n-75
ffmpeg -v error -y -framerate $FPS -i "$TMP/%04d.png" \
  -vf "drawtext=fontfile=$FONT:text='CONCEPT_ONLY W0 PROXY':fontsize=13:fontcolor=white@0.85:box=1:boxcolor=black@0.5:x=8:y=h-th-8,drawtext=fontfile=$FONT:text='F %{eif\:if(lt(n\,75)\,1186+n\,n-74)\:d}':fontsize=13:fontcolor=white@0.85:box=1:boxcolor=black@0.5:x=w-tw-8:y=h-th-8,scale=out_color_matrix=bt709:out_range=tv,format=yuv420p" \
  -c:v libx264 -profile:v high -crf 18 -preset medium -colorspace bt709 -color_primaries bt709 -color_trc bt709 -movflags +faststart "$OUT"
ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=width,height,r_frame_rate,nb_read_frames -of compact=p=0 "$OUT"
ffmpeg -v error -i "$OUT" -f null - && echo "decode ok"
ffmpeg -v error -y -i "$OUT" -c:v libx264 -b:v 2M -maxrate 2M -bufsize 4M -an "${OUT%.mp4}_stress2M.mp4"
ffmpeg -v error -y -i "$OUT" -vf "fps=3,scale=135:-1,tile=13x5" -frames:v 1 "${OUT%.mp4}_contact.jpg"
