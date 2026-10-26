#!/usr/bin/env bash
# review packet for a round: contact sheet (one frame per shot, labelled), 2 Mbps stress encode, first/last SSIM
# usage: scripts/make_review.sh <comp_frames_dir> <round e.g. R025> <animatic.mp4>
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
IN="$1"; RD="$ROOT/review/$2"; MP4="$3"; mkdir -p "$RD"
FRAMES=$(python3 -c "
import json; c=json.load(open('$ROOT/src/cameras.json'))
print(' '.join(str((s['F'][0]+s['F'][1])//2) for s in c['shots']))")
IDS=$(python3 -c "
import json; c=json.load(open('$ROOT/src/cameras.json')); print(' '.join(s['id'] for s in c['shots']))")
TMP=$(mktemp -d); i=0; set -- $IDS
for f in 1 $FRAMES 803; do
  lab="F$f"; [ $i -ge 1 ] && [ $i -le $# ] && lab="$(eval echo \${$i}) F$f"
  ffmpeg -v error -y -i "$IN/$(printf %04d $f).png" -vf "scale=270:480,drawbox=x=0:y=0:w=270:h=22:color=black@0.55:t=fill,drawtext=text='$lab':x=6:y=4:fontsize=14:fontcolor=white" "$TMP/$(printf %02d $i).png"
  i=$((i+1))
done
ffmpeg -v error -y -pattern_type glob -i "$TMP/*.png" -vf "tile=11x1:padding=4:color=white" -frames:v 1 "$RD/contact_270p.jpg"
rm -rf "$TMP"
ffmpeg -v error -y -i "$MP4" -c:v libx264 -b:v 2M -maxrate 2M -bufsize 4M -an "$RD/stress_2M.mp4"
ffmpeg -v error -y -i "$IN/0001.png" -frames:v 1 "$RD/_first.png"; ffmpeg -v error -y -i "$IN/0803.png" -frames:v 1 "$RD/_last.png"
SSIM=$(ffmpeg -i "$RD/_first.png" -i "$RD/_last.png" -lavfi ssim -f null - 2>&1 | grep -o "All:[0-9.]*" | cut -d: -f2)
rm -f "$RD/_first.png" "$RD/_last.png"
echo "{\"loop_ssim_first_last\": $SSIM}" > "$RD/loop_ssim.json"
echo "review packet -> $RD (loop SSIM $SSIM)"
