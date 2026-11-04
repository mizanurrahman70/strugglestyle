# Builds the short look video for the denim page from the gallery stills.
# Needs ffmpeg with libx264 (set FFMPEG=/path/to/ffmpeg if it is not on PATH):
#   python products/denim/make_video.py
# out: products/denim/look.mp4          1080x1350, ~12 s, silent, loops inline
#      products/denim/look-poster.webp  poster frame shown before playback
import os
import shutil
import subprocess
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
FFMPEG = os.environ.get('FFMPEG') or shutil.which('ffmpeg')
if not FFMPEG:
    raise SystemExit('ffmpeg not found — install it or set FFMPEG=/path/to/ffmpeg')

# Alternate slow zoom in / zoom out so the cut between stills feels like a camera move
CLIPS = [
    ('model.webp', 'in'),
    ('half.webp', 'out'),
    ('placket.webp', 'in'),
    ('jeans.webp', 'out'),
    ('detail.webp', 'in'),
    ('hem.webp', 'out'),
]
FPS, SECONDS, FADE = 30, 2.4, .5
FRAMES = round(FPS * SECONDS)
W, H = 896, 1120
S = 2  # zoompan works on a 2x canvas so the move stays smooth

args = [FFMPEG, '-y', '-loglevel', 'error']
for name, _ in CLIPS:
    args += ['-i', str(HERE / name)]

parts, last = [], None
for i, (_, move) in enumerate(CLIPS):
    step = .12 / FRAMES
    z = f"'min(1+{step:.6f}*on,1.12)'" if move == 'in' else f"'max(1.12-{step:.6f}*on,1.0)'"
    parts.append(
        f'[{i}:v]scale={W * S}:{H * S}:force_original_aspect_ratio=increase,'
        f'crop={W * S}:{H * S},setsar=1,'
        f"zoompan=z={z}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
        f'd={FRAMES}:s={W}x{H}:fps={FPS},format=yuv420p[v{i}]'
    )
    if last is None:
        last = f'v{i}'
        continue
    offset = (SECONDS - FADE) * i
    out = f'[x{i}]' if i < len(CLIPS) - 1 else '[vout]'
    parts.append(f'[{last}][v{i}]xfade=transition=fade:duration={FADE}:offset={offset:.2f}{out}')
    last = f'x{i}'

args += [
    '-filter_complex', ';'.join(parts), '-map', '[vout]', '-an',
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '24',
    '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
    str(HERE / 'look.mp4'),
]
subprocess.run(args, check=True)

# Poster: a frame a second in, so the still is not the very first zoom frame
tmp = HERE / '.poster.png'
subprocess.run(
    [FFMPEG, '-y', '-loglevel', 'error', '-ss', '1', '-i', str(HERE / 'look.mp4'),
     '-frames:v', '1', str(tmp)],
    check=True,
)
Image.open(tmp).convert('RGB').save(HERE / 'look-poster.webp', quality=82, method=6)
tmp.unlink()
print('look.mp4 + look-poster.webp ready')
