# Animated chip maps

Short silent loops of the four pinout cards, showing each chip at work. Used on the home page band
(`img/pinouts/anim/band-*.mp4|webm`) and in each lesson's chip-map fold (`img/pinouts/anim/<chip>.mp4|webm`).
The first frame of each loop is its poster (`.jpg`).

Run from this folder (needs numpy, scipy, Pillow, ffmpeg with libx264 and libvpx-vp9):

    python3 fill.py                       # <chip>-filled.png from downloads/pinouts
    for c in 4040 40106 4051 4021; do python3 render.py $c out; done
    # then copy out/card-<chip>.* to img/pinouts/anim/<chip>.* and out/band-<chip>.* to img/pinouts/anim/band-<chip>.*

`chips.py` holds the behaviour of each chip (read its class notes); `lib.py` the drawing helpers.
Visual rule: a HIGH signal lights up (pin dot solid cream, output arrow cream, input arrow pale gold).
