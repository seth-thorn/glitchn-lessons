#!/bin/bash
# Make web-sized copies of a lesson's clips for the player (needs ffmpeg).
#
#   bash tools/encode_clips.sh lessons/<slug>/video  clip1.mov  clip2.mov  ...
#
# Clips are numbered in the order given: part-1.mp4, part-2.mp4, ...
# These names match what the step editor writes into lesson.json.
# Output: 960x540 H.264, about 600-900 kbps, AAC audio, ready for streaming.
set -e
out="$1"; shift
if [ -z "$out" ] || [ "$#" -eq 0 ]; then
  echo "usage: bash tools/encode_clips.sh <output folder> <clip> [clip ...]"; exit 1
fi
mkdir -p "$out"
n=0
for f in "$@"; do
  n=$((n+1))
  ffmpeg -v error -y -i "$f" -map 0:v:0 -map 0:a:0? -vf "scale=960:540" \
    -c:v libx264 -preset veryfast -crf 24 -maxrate 900k -bufsize 1800k -pix_fmt yuv420p \
    -c:a aac -b:a 64k -ac 2 -movflags +faststart "$out/part-$n.mp4" 2>&1 | grep -v "out of range" || true
  echo "part-$n.mp4  <-  $(basename "$f")"
done
echo "Done: $n clips in $out"
