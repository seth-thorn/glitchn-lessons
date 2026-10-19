"""Drawing helpers for the animated chip maps. Everything works in the pinout sources' own
pixel space (5000 x 2000), on a float canvas that covers the band crop and the card crop."""
import numpy as np
from PIL import Image
from scipy import ndimage as nd

TEAL = np.array((138, 200, 195), np.float32)
CREAM = np.array((240, 230, 221), np.float32)
PIN = np.array((189, 216, 209), np.float32)
GREY = np.array((174, 168, 182), np.float32)
ORANGE = np.array((234, 169, 67), np.float32)
BAR = np.array((146, 148, 153), np.float32)
PURPLE = np.array((141, 117, 143), np.float32)
ORANGE_LIT = np.array((252, 216, 146), np.float32)

OX, OY, W, H = 965, -150, 3070, 2300          # canvas covers x 965..4035, y -150..2150


def load(chip):
    src = np.asarray(Image.open(f'{chip}-filled.png').convert('RGB')).astype(np.float32)
    can = np.empty((H, W, 3), np.float32); can[:] = TEAL
    can[-OY:-OY + 2000, :, :] = src[:, OX:OX + W]
    return can


def sl(x0, y0, x1, y1):
    return np.s_[int(y0) - OY:int(y1) - OY, int(x0) - OX:int(x1) - OX]


def grid(x0, y0, x1, y1):
    ys, xs = np.mgrid[int(y0):int(y1), int(x0):int(x1)]
    return xs + .5, ys + .5


def paint(can, box, alpha, color):
    """composite a flat colour with an alpha patch over box"""
    s = sl(*box); a = np.clip(alpha, 0, 1)[..., None]
    can[s] = can[s] * (1 - a) + np.asarray(color, np.float32) * a


def paint_rgb(can, box, alpha, rgb):
    s = sl(*box); a = np.clip(alpha, 0, 1)[..., None]
    can[s] = can[s] * (1 - a) + rgb * a


def aa(d):                                     # signed distance -> coverage
    return np.clip(.5 - d, 0, 1)


def circle(can, cx, cy, r, color, alpha=1.0):
    box = (cx - r - 2, cy - r - 2, cx + r + 3, cy + r + 3); X, Y = grid(*box)
    paint(can, box, aa(np.hypot(X - cx, Y - cy) - r) * alpha, color)


def capsule(can, x0, y0, x1, y1, w, color, alpha=1.0):
    r = w / 2; box = (min(x0, x1) - r - 2, min(y0, y1) - r - 2, max(x0, x1) + r + 3, max(y0, y1) + r + 3)
    X, Y = grid(*box); px, py = X - x0, Y - y0; dx, dy = x1 - x0, y1 - y0
    L2 = dx * dx + dy * dy or 1e-6; t = np.clip((px * dx + py * dy) / L2, 0, 1)
    paint(can, box, aa(np.hypot(px - t * dx, py - t * dy) - r) * alpha, color)


def rrect_alpha(X, Y, x0, y0, x1, y1, r):
    cx, cy, hx, hy = (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 2, (y1 - y0) / 2
    qx, qy = np.abs(X - cx) - hx + r, np.abs(Y - cy) - hy + r
    d = np.hypot(np.maximum(qx, 0), np.maximum(qy, 0)) + np.minimum(np.maximum(qx, qy), 0) - r
    return aa(d)


def rrect(can, x0, y0, x1, y1, r, color, alpha=1.0):
    box = (x0 - 2, y0 - 2, x1 + 2, y1 + 2); X, Y = grid(*box)
    paint(can, box, rrect_alpha(X, Y, x0, y0, x1, y1, r) * alpha, color)


def coverage(can, box, base, col, tol=28):
    """how much of `col` (over `base`) each pixel holds: 0..1, and 0 where the pixel is something else"""
    p = can[sl(*box)] - base; v = col - base
    t = (p @ v) / float(v @ v)
    resid = np.linalg.norm(p - t[..., None] * v, axis=-1)
    return np.where(resid < tol, np.clip(t, 0, 1), 0.0)


def recolor(can, box, frm, to, level, base=TEAL):
    """move the pixels coloured `frm` (antialiased over `base`) towards `to` by `level`"""
    if level <= 0: return
    t = coverage(can, box, base, frm)
    target = frm + (np.asarray(to, np.float32) - frm) * level
    s = sl(*box); m = t > 0.02
    can[s][m] = base + t[m][:, None] * (target - base)


def pin_glow(can, cx, cy, level):
    """a pin dot lights up (translucent -> solid cream) as its signal goes high"""
    if level <= 0: return
    box = (cx - 40, cy - 40, cx + 41, cy + 41)
    X, Y = grid(*box); inside = aa(np.hypot(X - cx, Y - cy) - 38)
    t = coverage(can, box, TEAL, PIN, tol=20)
    lift = np.where(t > 0.02, inside * level, 0)
    paint(can, box, lift, CREAM)


def rotate_disc(can, cx, cy, r, deg):
    """turn the picture inside a disc about (cx, cy) in pixel-centre coordinates;
    positive deg = anticlockwise on screen"""
    if abs(deg % 360) < 1e-3: return
    R = int(r + 4); x0, y0 = int(cx) - R, int(cy) - R; box = (x0, y0, x0 + 2 * R + 2, y0 + 2 * R + 2); s = sl(*box)
    patch = can[s].copy()
    c = np.array([cy - .5 - y0, cx - .5 - x0])                 # centre in (row, col) index space
    th = np.radians(deg); co, si = np.cos(th), np.sin(th)
    M = np.array([[co, si], [-si, co]])                         # output (row, col) -> input
    off = c - M @ c
    rot = np.stack([nd.affine_transform(patch[..., k], M, offset=off, order=3, mode='nearest') for k in range(3)], -1)
    X, Y = grid(*box); a = aa(np.hypot(X - cx, Y - cy) - r)[..., None]
    can[s] = patch * (1 - a) + np.clip(rot, 0, 255) * a


def ease(x):
    x = min(max(x, 0.0), 1.0); return x * x * (3 - 2 * x)


def ramp(t, t0, dur):                          # 0 before t0, 1 after t0+dur, eased between
    return ease((t - t0) / dur) if dur > 0 else float(t >= t0)


def to_uint8(can):
    return np.clip(can + .5, 0, 255).astype(np.uint8)
