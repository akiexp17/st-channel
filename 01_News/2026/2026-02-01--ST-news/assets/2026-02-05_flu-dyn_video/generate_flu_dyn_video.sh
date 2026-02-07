#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
OUT_MP4="$ROOT_DIR/flu_dyn_artistic_video_2026-02-05.mp4"
OUT_POSTER="$ROOT_DIR/flu_dyn_artistic_video_2026-02-05_poster.jpg"
FFMPEG_BIN="${FFMPEG_BIN:-/usr/local/opt/ffmpeg-full/bin/ffmpeg}"

if [ ! -x "$FFMPEG_BIN" ]; then
  echo "ffmpeg-full not found at $FFMPEG_BIN"
  echo "Set FFMPEG_BIN to your ffmpeg path and rerun."
  exit 1
fi

"$FFMPEG_BIN" -y \
  -f lavfi -i "gradients=size=1080x1920:rate=30:duration=32:c0=0x040816:c1=0x0f2d4a:c2=0x1fbad6:c3=0x3f4aa8:n=4:type=spiral:speed=0.055:seed=20260205" \
  -f lavfi -i "life=s=1080x1920:r=30:ratio=0.072:seed=52:life_color=0x74d6ff:death_color=0x00040d:mold=6:mold_color=0x3f4aa8" \
  -filter_complex "\
[0:v]tmix=frames=3:weights='1 2 1',gblur=sigma=1.2,eq=contrast=1.14:brightness=-0.05:saturation=1.25[bg]; \
[1:v]format=rgba,colorchannelmixer=aa=0.22,tmix=frames=4:weights='1 1 1 1'[life]; \
[bg][life]blend=all_mode=screen:all_opacity=0.33,drawgrid=width=90:height=90:thickness=1:color=white@0.05, \
vignette=PI/5, \
drawbox=x=70:y=74:w=940:h=278:color=black@0.22:t=fill, \
drawbox=x=70:y=74:w=940:h=278:color=white@0.14:t=2, \
drawbox=x=70:y=370:w=940:h=1160:color=black@0.20:t=fill, \
drawbox=x=70:y=370:w=940:h=1160:color=white@0.10:t=2, \
drawtext=fontfile='/System/Library/Fonts/Supplemental/Arial Bold.ttf':text='FLUID DYNAMICS RESEARCH DIGEST':fontcolor=white:fontsize=62:x='(w-text_w)/2':y=128:enable='between(t,0,32)', \
drawtext=fontfile='/System/Library/Fonts/Supplemental/Arial.ttf':text='arXiv physics.flu-dyn | RSS 2026-02-05':fontcolor=white@0.88:fontsize=32:x='(w-text_w)/2':y=214:enable='between(t,0,32)', \
drawtext=fontfile='/System/Library/Fonts/Supplemental/Arial.ttf':text='Artistic summary based on 23 papers':fontcolor=0x69d2ff@0.96:fontsize=28:x='(w-text_w)/2':y=258:enable='between(t,0,32)', \
drawtext=fontfile='/System/Library/Fonts/Supplemental/Arial Bold.ttf':text='2602.03185  Bubble-driven liquid jets':fontcolor=white:fontsize=52:x='(w-text_w)/2+28*sin(2*t)':y=500:enable='between(t,2,7)', \
drawtext=fontfile='/System/Library/Fonts/Supplemental/Arial.ttf':text='Impulse-induced jets from bubbles with arbitrary contact angles':fontcolor=0x9fe8ff:fontsize=28:x='(w-text_w)/2':y=564:enable='between(t,2,7)', \
drawtext=fontfile='/System/Library/Fonts/Supplemental/Arial Bold.ttf':text='2602.02971  Nonlinear electrohydrodynamics of drops':fontcolor=white:fontsize=50:x='(w-text_w)/2+26*sin(2*t)':y=690:enable='between(t,7,12)', \
drawtext=fontfile='/System/Library/Fonts/Supplemental/Arial.ttf':text='Surfactant-laden leaky dielectric interfaces':fontcolor=0x7cf8d9:fontsize=28:x='(w-text_w)/2':y=754:enable='between(t,7,12)', \
drawtext=fontfile='/System/Library/Fonts/Supplemental/Arial Bold.ttf':text='2602.03187  Turbulent skin-friction drag':fontcolor=white:fontsize=52:x='(w-text_w)/2+24*sin(2*t)':y=880:enable='between(t,12,17)', \
drawtext=fontfile='/System/Library/Fonts/Supplemental/Arial.ttf':text='Causal structures in wall-bounded turbulence':fontcolor=0x69d2ff:fontsize=28:x='(w-text_w)/2':y=944:enable='between(t,12,17)', \
drawtext=fontfile='/System/Library/Fonts/Supplemental/Arial Bold.ttf':text='2602.03617  Roughness transition at Mach 6':fontcolor=white:fontsize=50:x='(w-text_w)/2+22*sin(2*t)':y=1070:enable='between(t,17,22)', \
drawtext=fontfile='/System/Library/Fonts/Supplemental/Arial.ttf':text='Hypersonic blunt-body boundary-layer dynamics':fontcolor=0x7cf8d9:fontsize=28:x='(w-text_w)/2':y=1134:enable='between(t,17,22)', \
drawtext=fontfile='/System/Library/Fonts/Supplemental/Arial Bold.ttf':text='2602.02832  Koopman autoencoders for forecasting':fontcolor=white:fontsize=49:x='(w-text_w)/2+20*sin(2*t)':y=1260:enable='between(t,22,27)', \
drawtext=fontfile='/System/Library/Fonts/Supplemental/Arial.ttf':text='Continuous-time latent dynamics for fluid prediction':fontcolor=0x69d2ff:fontsize=28:x='(w-text_w)/2':y=1324:enable='between(t,22,27)', \
drawtext=fontfile='/System/Library/Fonts/Supplemental/Arial Bold.ttf':text='2602.03518  Vortex shedding in superfluids':fontcolor=white:fontsize=51:x='(w-text_w)/2+18*sin(2*t)':y=1450:enable='between(t,27,31)', \
drawtext=fontfile='/System/Library/Fonts/Supplemental/Arial.ttf':text='Dynamic similarity around a penetrable obstacle':fontcolor=0x7cf8d9:fontsize=28:x='(w-text_w)/2':y=1514:enable='between(t,27,31)', \
drawtext=fontfile='/System/Library/Fonts/Supplemental/Arial.ttf':text='Source 2026-02-05_RSS_Links.md (physics.flu-dyn)':fontcolor=white@0.72:fontsize=20:x='(w-text_w)/2':y=1836:enable='between(t,0,32)'[v]" \
  -map "[v]" \
  -t 32 \
  -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p \
  "$OUT_MP4"

"$FFMPEG_BIN" -y -i "$OUT_MP4" -ss 00:00:08 -vframes 1 -q:v 2 -update 1 "$OUT_POSTER"

echo "Generated:"
echo "  $OUT_MP4"
echo "  $OUT_POSTER"
