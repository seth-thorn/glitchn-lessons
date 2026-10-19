"""Render one chip's loop to two small H.264 movies (lesson card 2x, home band) plus posters."""
import sys, subprocess, numpy as np, os
from PIL import Image
from card import *
FPS = 30
OUT = sys.argv[2] if len(sys.argv) > 2 else 'out'
os.makedirs(OUT, exist_ok=True)
chip = sys.argv[1]
c = {'4040': C4040, '40106': C40106, '4051': C4051, '4021': C4021}[chip]()
n = round(c.LOOP * FPS)
targets = {'card': (card_box(chip), (1274, 1048)), 'band': ((965, 0, 4035, 2000), (922, 600))}
procs = {}
for k, (box, (w, h)) in targets.items():
    src = ['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{w}x{h}', '-r', str(FPS), '-i', '-',
           '-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv', '-an']
    procs[k + '.mp4'] = subprocess.Popen(src + ['-c:v', 'libx264', '-preset', 'veryslow', '-tune', 'animation', '-crf', '18', '-g', str(n),
        '-movflags', '+faststart', f'{OUT}/{k}-{chip}.mp4'], stdin=subprocess.PIPE)
    procs[k + '.webm'] = subprocess.Popen(src + ['-c:v', 'libvpx-vp9', '-crf', '30', '-b:v', '0', '-row-mt', '1', '-deadline', 'good', '-cpu-used', '1',
        '-g', str(n), f'{OUT}/{k}-{chip}.webm'], stdin=subprocess.PIPE)
for i in range(n):
    f = c.frame(i / FPS)
    for k, (box, size) in targets.items():
        im = Image.fromarray(crop(f, box)).resize(size, Image.LANCZOS)
        if i == 0: im.save(f'{OUT}/{k}-{chip}.jpg', quality=90, optimize=True)
        b = im.tobytes(); procs[k + '.mp4'].stdin.write(b); procs[k + '.webm'].stdin.write(b)
for p in procs.values(): p.stdin.close(); p.wait()
print(chip, n, 'frames', {k: os.path.getsize(f'{OUT}/{k.split('.')[0]}-{chip}.{k.split('.')[1]}') for k in procs})
