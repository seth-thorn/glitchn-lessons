"""Step 1: make <chip>-filled.png from downloads/pinouts/<chip>-pinout.jpg (white corners painted teal)."""
from PIL import Image, ImageDraw
import os
SRC = os.path.join(os.path.dirname(__file__), '../../downloads/pinouts/')
for c in ['40106', '4040', '4021', '4051']:
    im = Image.open(SRC + c + '-pinout.jpg').convert('RGB')
    for xy in [(0, 0), (im.width - 1, 0), (0, im.height - 1), (im.width - 1, im.height - 1)]:
        ImageDraw.floodfill(im, xy, (138, 200, 195), thresh=40)
    im.save(c + '-filled.png')
