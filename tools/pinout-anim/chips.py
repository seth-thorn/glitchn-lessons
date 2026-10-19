"""The four Glitch'n chip maps, animated the way the chips really behave.

Visual rule shared by all four: a signal that is HIGH lights up. Its pin dot turns solid cream,
an output arrow (grey) turns cream, an input arrow (orange) turns pale gold.
Pins are numbered as on the real chip: top row left to right is pin 16..9 (14..8 on the 40106),
bottom row left to right is pin 1..8 (1..7)."""
import math
import numpy as np
from lib import *

TOP, BOT = 675, 1325                                     # pin-row centres (y)


def lit_out(can, x, top, level):                          # grey output arrow above/below a pin
    box = (x - 100, 270, x + 101, 612) if top else (x - 100, 1388, x + 101, 1712)
    recolor(can, box, GREY, CREAM, level)


def lit_in(can, x, top, level):                           # orange input arrow
    box = (x - 100, 300, x + 101, 612) if top else (x - 100, 1388, x + 101, 1712)
    recolor(can, box, ORANGE, ORANGE_LIT, level)


def soft(sig_fn, t, edge=0.05):
    """0..1 level of a logic signal, with a short fade at each edge so nothing pops"""
    a = sig_fn(t - edge / 2); b = sig_fn(t + edge / 2)
    if a == b: return float(a)
    lo, hi = t - edge / 2, t + edge / 2                     # find the edge by bisection
    for _ in range(12):
        mid = (lo + hi) / 2
        if sig_fn(mid) == a: lo = mid
        else: hi = mid
    x = (t - (lo - edge / 2)) / edge
    return float(a) + (float(b) - float(a)) * ease(x)


# ---------------------------------------------------------------- 4040: ripple counter
class C4040:
    """Tempo (clock, pin 10) ticks 8 times per loop. The count goes up on each falling edge.
    ÷2 (Q1, pin 9) ÷4 (Q2, pin 7) ÷8 (Q3, pin 6). Reset (pin 11) stays low.
    The bar stacks inside are the card's own pulse pictures: 8 clock pulses, 4, 2 and 1 in the
    same span. A playhead runs down every stack together; each bar lights while its pulse is high."""
    chip, T, N = '4040', 0.5, 8
    LOOP = T * N
    X = {p: 1625 + 250 * i for i, p in enumerate([16, 15, 14, 13, 12, 11, 10, 9])}
    X.update({p: 1625 + 250 * (p - 1) for p in range(1, 9)})
    STACKS = {  # signal: list of bar boxes, top to bottom
        'clk': [(3090, 753 + 25 * k, 3160, 772 + 25 * k) for k in range(8)],
        'q1': [(3340, 753 + 50 * k, 3410, 797 + 50 * k) for k in range(4)],
        'q2': [(3090, 1053, 3160, 1147), (3090, 1153, 3160, 1247)],
        'q3': [(2840, 1053, 2910, 1247)],
    }
    DIM = 0.42

    def clk(self, t): return (t % self.T) < self.T / 2

    def count(self, t): return (math.floor((t - self.T / 2) / self.T) + 1) % 8

    def q(self, n, t): return (self.count(t) >> n) & 1

    def __init__(self): self.base = load(self.chip)

    def frame(self, t):
        can = self.base.copy(); T = self.T
        c = soft(self.clk, t)
        q = [soft(lambda u, n=n: self.q(n, u), t) for n in range(3)]
        # bars: which bar of each stack is "now", and how lit it is
        cur = {'clk': (int(t // T) % 8, c)}
        for n, name in enumerate(['q1', 'q2', 'q3']):
            per = T * 2 ** (n + 1)
            cur[name] = (int(math.floor((t - T / 2) / per)) % (8 >> (n + 1)), q[n])
        for name, bars in self.STACKS.items():
            idx, lev = cur[name]
            for i, (x0, y0, x1, y1) in enumerate(bars):
                keep = self.DIM + (1 - self.DIM) * (lev if i == idx else 0)
                box = (x0 - 3, y0 - 3, x1 + 3, y1 + 3)
                cov = coverage(can, box, TEAL, CREAM)
                s = sl(*box); can[s] = TEAL + (cov * keep)[..., None] * (CREAM - TEAL) + (can[s] - TEAL - cov[..., None] * (CREAM - TEAL))
        lit_in(can, self.X[10], True, c); pin_glow(can, self.X[10], TOP, c)
        lit_out(can, self.X[9], True, q[0]); pin_glow(can, self.X[9], TOP, q[0])
        lit_out(can, self.X[7], False, q[1]); pin_glow(can, self.X[7], BOT, q[1])
        lit_out(can, self.X[6], False, q[2]); pin_glow(can, self.X[6], BOT, q[2])
        return can


# ---------------------------------------------------------------- 40106: three oscillators
class C40106:
    """Each inverter is wired as an oscillator: its output feeds back through the knob to its
    input, where a capacitor fills and empties. The input pin brightens as the capacitor
    charges (while the output is high) and dims as it drains (output low). Every time the
    input crosses the Schmitt trigger's threshold the output flips, and the icon's two arrows
    turn half a turn. Three oscillators, three speeds."""
    chip, LOOP = '40106', 6.0
    XT = {14: 1675, 13: 1950, 12: 2225, 11: 2500, 10: 2775, 9: 3050, 8: 3325}
    XB = {p: 1675 + 275 * (p - 1) for p in range(1, 8)}
    # (input pin x, row) , (output pin x, row), icon centre, period, phase
    OSC = [((XB[1], 'b'), (XB[2], 'b'), (1812.5, 1150.0), 6.0 / 6, 0.30),
           ((XB[5], 'b'), (XB[6], 'b'), (2912.5, 1150.0), 6.0 / 4, 0.40),
           ((XT[11], 't'), (XT[10], 't'), (2637.5, 850.0), 6.0 / 8, 0.80)]

    def __init__(self): self.base = load(self.chip)

    @staticmethod
    def state(t, P, ph):
        """output level, input (capacitor) level 0..1 between the thresholds, and how many flips so far"""
        u = ((t / P + ph) % 1.0)
        out_high = u < 0.5
        k = 3.0                                            # RC curve shape
        if out_high: v = (1 - math.exp(-k * u * 2)) / (1 - math.exp(-k))
        else: v = 1 - (1 - math.exp(-k * (u - .5) * 2)) / (1 - math.exp(-k))
        return out_high, v, u

    @staticmethod
    def flips(t, P, ph, dur=0.18):
        x = 2 * (t / P + ph); n = math.floor(x)
        return n - 1 + ease((x - n) * P / 2 / dur)

    def frame(self, t):
        can = self.base.copy()
        for (xi, ri), (xo, ro), (cx, cy), P, ph in self.OSC:
            hi, v, u = self.state(t, P, ph)
            fl = lambda s, P=P, ph=ph: self.state(s, P, ph)[0]
            o = soft(fl, t, 0.04)
            # icon: its arrows point anticlockwise; it turns half a turn that way at every flip
            rotate_disc(can, cx, cy, 103, 180.0 * ((self.flips(t, P, ph) - self.flips(0, P, ph)) % 2))
            top_o = ro == 't'; top_i = ri == 't'
            lit_out(can, xo, top_o, o); pin_glow(can, xo, TOP if top_o else BOT, o)
            pin_glow(can, xi, TOP if top_i else BOT, 0.12 + 0.88 * v)
        return can


# ---------------------------------------------------------------- 4051: 8-channel switch
class C4051:
    """Switch Control A (pin 11) and B (pin 10) count in binary; C (pin 9) is tied to minus, so
    only channels 0-3 are used. 0 = pin 13, 1 = pin 14, 2 = pin 15, 3 = pin 12 (the real
    pinout, so the arm visits them in that order). The arm joins the chosen channel to the
    common pin (pin 3). Twice per loop the Master On/Off (inhibit, pin 6) goes high and the
    switch lets go of every channel."""
    chip, T, N = '4051', 0.5, 12
    LOOP = T * N
    X = {p: 1537.5 + 275 * i for i, p in enumerate([16, 15, 14, 13, 12, 11, 10, 9])}
    XB = {p: 1537.5 + 275 * (p - 1) for p in range(1, 9)}
    CH = {0: 13, 1: 14, 2: 15, 3: 12}
    BARS = {15: (1767, 280, 1858, 570), 14: (2042, 280, 2133, 570), 13: (2317, 280, 2408, 570), 12: (2592, 280, 2683, 570)}
    COM = (2042, 1430, 2133, 1720)
    HUB, HUB_R = (2087.5, 1000.0), 87.5
    INH_STEPS = (8, 9)

    def __init__(self):
        can = load(self.chip)
        # wipe the arm and the dotted lines (they are redrawn every frame); keep hub, common line and the "4051"
        box = (1770, 630, 2700, 1000); X, Y = grid(*box)
        keep = (np.hypot(X - self.HUB[0], Y - self.HUB[1]) < self.HUB_R + 1) | ((X > 2265) & (Y > 925))
        s = sl(*box); can[s] = np.where(keep[..., None], can[s], TEAL)
        self.base = can

    def count(self, k): return (2 + k) % 4

    def inh(self, k): return (k % self.N) in self.INH_STEPS

    def dots(self, can, pin):
        """the card's dotted line: dots of radius 20 at equal steps (~53 px) from the pin to the hub
        centre, leaving out the ones that would touch the hub"""
        px, py = self.X[pin], TOP; hx, hy = self.HUB
        L = math.hypot(hx - px, hy - py); n = round(L / 53.5)
        for k in range(n + 1):
            x, y = px + (hx - px) * k / n, py + (hy - py) * k / n
            if math.hypot(x - hx, y - hy) > 80: circle(can, x, y, 20, CREAM)

    def frame(self, t):
        can = self.base.copy(); T, D = self.T, 0.16
        k = int(t // T); u = t - k * T
        c_now, c_prev = self.count(k), self.count(k - 1)
        i_now, i_prev = self.inh(k), self.inh(k - 1)
        m = ease(u / D)                                       # how far the switch has moved this step
        # the arm's tip slides along the row of channel pins from the old channel to the new one
        x0, x1 = self.X[self.CH[c_prev]], self.X[self.CH[c_now]]
        tipx, tipy = x0 + (x1 - x0) * m, TOP
        ang = math.atan2(tipy - self.HUB[1], tipx - self.HUB[0]); length = math.hypot(tipx - self.HUB[0], tipy - self.HUB[1])
        reach0 = 0.0 if i_prev else 1.0; reach1 = 0.0 if i_now else 1.0
        reach = reach0 + (reach1 - reach0) * m
        for p in (15, 14, 13, 12):
            circle(can, self.X[p], TOP, 38, PIN)
        for p in (15, 14, 13, 12):
            if reach > 0.99 and abs(tipx - self.X[p]) < 0.5: continue      # the arm lies on this line
            self.dots(can, p)
        if reach > 0.001:
            r0 = self.HUB_R * 0.5; L = r0 + (length - r0) * reach
            hx, hy = self.HUB
            capsule(can, hx, hy, hx + math.cos(ang) * L, hy + math.sin(ang) * L, 40, CREAM)
        circle(can, self.HUB[0], self.HUB[1], self.HUB_R, CREAM)
        # signal path: the chosen channel and the common pin light while they are joined
        for ch, pin in self.CH.items():
            lev = 0.0
            if ch == c_prev and not i_prev: lev = max(lev, 1 - m)
            if ch == c_now and not i_now: lev = max(lev, m)
            if c_prev == c_now and ch == c_now and not i_now and not i_prev: lev = 1.0
            recolor(can, self.BARS[pin], BAR, CREAM, lev)
        recolor(can, self.COM, BAR, CREAM, reach)
        a_bit = soft(lambda s: self.count(int(s // T)) & 1, t)
        b_bit = soft(lambda s: (self.count(int(s // T)) >> 1) & 1, t)
        inh = soft(lambda s: int(self.inh(int(s // T))), t)
        lit_in(can, self.X[11], True, a_bit); pin_glow(can, self.X[11], TOP, a_bit)
        lit_in(can, self.X[10], True, b_bit); pin_glow(can, self.X[10], TOP, b_bit)
        lit_in(can, self.XB[6], False, inh); pin_glow(can, self.XB[6], BOT, inh)
        return can


# ---------------------------------------------------------------- 4021: shift register
class C4021:
    """Parallel/Serial control (pin 9) is tied to minus, so the chip works as a pure shift
    register. Every press of the button (clock, pin 10) moves all eight bits one stage along
    the conveyor (1 -> 2 -> ... -> 8) and takes a new bit in at stage 1 from the light sensor
    (serial in, pin 11, the camera): light = 1, dark = 0. A bit that is 1 shows as the
    inverted square. Stages 6, 7 and 8 come out on pins 2 (Q6), 12 (Q7) and 3 (Q8).
    The light pattern is chosen so the register is back where it started after 8 presses."""
    chip, T, N, T0 = '4021', 0.75, 8, 0.3
    LOOP = T * N
    X = {p: 1537.5 + 275 * i for i, p in enumerate([16, 15, 14, 13, 12, 11, 10, 9])}
    XB = {p: 1537.5 + 275 * (p - 1) for p in range(1, 9)}
    PITCH, BX0, BY0, BS = 137.5, 1902.5, 815.0, 95.0          # stage boxes: slot s at BX0 + s*PITCH (slot 0 = stage 8)
    INNER = (20.0, 55.0)                                       # inner square offset and size
    OUTBOX = {7: (2590.0, 165.0), 6: (1765.0, 1752.5), 8: (2040.0, 1752.5)}
    START = [0, 1, 1, 0, 1, 1, 0, 0]                           # stages 1..8 as on the card
    LIGHT = [0, 0, 1, 1, 0, 1, 1, 0]                           # the bit taken in at each press
    BELT_C = ((1912.5, 1075.0), (3050.0, 1075.0)); BELT_R = 125.0
    GAPS = 22                                                  # belt marks, about one per stage

    def __init__(self):
        can = load(self.chip)
        self.glyph = {}
        for s in range(8):
            stage = 8 - s; x0 = self.BX0 + s * self.PITCH
            self.glyph[stage] = self.grab_digit(can, x0, self.BY0, self.START[stage - 1])
        for st, (x0, y0) in self.OUTBOX.items():
            self.glyph[('out', st)] = self.grab_digit(can, x0, y0, self.START[st - 1])
        # camera interior (for the light), and the button's arrow (it moves when pressed)
        cb = (2770, 105, 3045, 305); cm = coverage(can, cb, TEAL, CREAM) > .5
        self.cam_box = cb; self.cam_in = nd.binary_fill_holes(cm) & ~nd.binary_dilation(cm, iterations=2)
        ab = (3132, 44, 3244, 160); self.arrow_box = ab; self.arrow_a = coverage(can, ab, TEAL, CREAM)
        # wipe what gets redrawn: stage boxes, output boxes, the button's cap and arrow
        can[sl(1895, 806, 2970, 919)] = TEAL
        for (x0, y0) in self.OUTBOX.values(): can[sl(x0 - 6, y0 - 6, x0 + 101, y0 + 101)] = TEAL
        can[sl(3125, 40, 3255, 200)] = TEAL
        self.base = can
        # the register's state before each press
        self.states = [list(self.START)]
        for k in range(self.N):
            st = self.states[-1]; self.states.append([self.LIGHT[k]] + st[:-1])
        assert self.states[-1] == self.START, 'pattern must loop'

    @staticmethod
    def grab_digit(can, x0, y0, inverted):
        box = (x0 + 24, y0 + 24, x0 + 71, y0 + 71)              # inside the inner square
        cov = coverage(can, box, TEAL, CREAM) if inverted else coverage(can, box, CREAM, TEAL)
        cov = np.clip((cov - 0.12) / 0.8, 0, 1)                   # drop the JPEG speckle around the digit
        return box, cov

    # ---- drawing pieces
    def boxes(self, can, t):
        k, p = self.press(t)
        st = self.states[k]                                     # state before the current/last press
        if p >= 1: st, p = self.states[k + 1], 0.0              # finished: show the new state at rest
        region = (1895, 700, 2970, 919); X, Y = grid(*region)
        boxa = np.zeros_like(X)
        for s in range(8):
            x0 = self.BX0 + s * self.PITCH
            boxa = np.maximum(boxa, rrect_alpha(X, Y, x0, self.BY0, x0 + self.BS, self.BY0 + self.BS, 10))
        inner = np.zeros_like(X); o, w = self.INNER
        for s in range(8):
            stage = 8 - s
            if st[stage - 1]:
                x0 = self.BX0 + s * self.PITCH - p * self.PITCH
                inner = np.maximum(inner, rrect_alpha(X, Y, x0 + o, self.BY0 + o, x0 + o + w, self.BY0 + o + w, 1))
        if p > 0 and self.LIGHT[k]:                             # the new bit drops into stage 1 from the serial input
            x0 = self.BX0 + 7 * self.PITCH; dy = (1 - p) * -95
            inner = np.maximum(inner, rrect_alpha(X, Y, x0 + o, self.BY0 + o + dy, x0 + o + w, self.BY0 + o + w + dy, 1))
        q = inner * boxa
        paint(can, region, boxa, CREAM); paint(can, region, q, TEAL)
        for s in range(8):
            (bx0, by0, bx1, by1), g = self.glyph[8 - s]
            qq = q[int(by0) - region[1]:int(by1) - region[1], int(bx0) - region[0]:int(bx1) - region[0]][..., None]
            paint_rgb(can, (bx0, by0, bx1, by1), g, qq * CREAM + (1 - qq) * TEAL)

    def out_box(self, can, st, x0, y0, on):
        box = (x0 - 4, y0 - 4, x0 + 100, y0 + 100); X, Y = grid(*box)
        a = rrect_alpha(X, Y, x0, y0, x0 + self.BS, y0 + self.BS, 10)
        o, w = self.INNER; c = w / 2 * on; mx, my = x0 + o + w / 2, y0 + o + w / 2
        q = (rrect_alpha(X, Y, mx - c, my - c, mx + c, my + c, 1) if on > 0.01 else np.zeros_like(X)) * a
        paint(can, box, a, CREAM); paint(can, box, q, TEAL)
        (bx0, by0, bx1, by1), g = self.glyph[('out', st)]
        qq = q[int(by0) - int(box[1]):int(by1) - int(box[1]), int(bx0) - int(box[0]):int(bx1) - int(box[0])][..., None]
        paint_rgb(can, (bx0, by0, bx1, by1), g, qq * CREAM + (1 - qq) * TEAL)

    def belt(self, can, travel):
        (lx, cy), (rx, _) = self.BELT_C; R = self.BELT_R; top, bot = cy - R, cy + R
        Ls = rx - lx; Arc = math.pi * R; P = 2 * Ls + 2 * Arc; d = P / self.GAPS
        for i in range(self.GAPS):
            s = (i * d + travel) % P
            if s < Ls: x, y, tx, ty = rx - s, top, -1, 0                                   # top run, moving left
            elif s < Ls + Arc:
                th = (s - Ls) / R; x, y = lx - R * math.sin(th), cy - R * math.cos(th); tx, ty = -math.cos(th), math.sin(th)
            elif s < 2 * Ls + Arc: x, y, tx, ty = lx + (s - Ls - Arc), bot, 1, 0
            else:
                th = (s - 2 * Ls - Arc) / R; x, y = rx + R * math.sin(th), cy + R * math.cos(th); tx, ty = math.cos(th), -math.sin(th)
            box = (x - 22, y - 22, x + 23, y + 23); X, Y = grid(*box)
            u = (X - x) * tx + (Y - y) * ty; v = -(X - x) * ty + (Y - y) * tx
            dd = np.maximum(np.abs(u) - 6, np.abs(v) - 15)
            paint(can, box, aa(dd), TEAL)

    def press(self, t):
        """index of the current/last press and how far its shift has got (0..1)"""
        k = math.floor((t - self.T0) / self.T)
        if k < 0: return 0, 0.0                                 # before the first press: at rest, state 0
        return k, ease((t - self.T0 - k * self.T) / 0.3)

    def light(self, t):
        return self.LIGHT[(math.floor((t - self.T0 - 0.35) / self.T) + 1) % self.N]

    def frame(self, t):
        can = self.base.copy(); T = self.T
        k, p = self.press(t)
        since = t - self.T0 - max(k, 0) * T if t >= self.T0 else 9
        # belt and pulley: one step of travel per press
        done = k + p if t >= self.T0 else 0.0
        self.belt(can, done * (2 * 1137.5 + 2 * math.pi * self.BELT_R) / self.GAPS)
        rotate_disc(can, 1912.5, 1075.0, 96, 90.0 * (done % 4))
        self.boxes(can, t)
        # outputs: Q8 = stage 8, Q7 = stage 7, Q6 = stage 6, switching halfway through each shift
        def q(stage, u):
            kk, pp = self.press(u)
            st = self.states[kk + 1] if (u >= self.T0 and pp >= 0.5) else self.states[kk]
            return st[stage - 1]
        for stage, (x0, y0) in self.OUTBOX.items():
            lev = soft(lambda u, s=stage: q(s, u), t, 0.08)
            self.out_box(can, stage, x0, y0, lev)
        q6, q7, q8 = (soft(lambda u, s=s: q(s, u), t, 0.08) for s in (6, 7, 8))
        lit_out(can, self.XB[2], False, q6); pin_glow(can, self.XB[2], BOT, q6)
        lit_out(can, self.XB[3], False, q8); pin_glow(can, self.XB[3], BOT, q8)
        lit_out(can, self.X[12], True, q7); pin_glow(can, self.X[12], TOP, q7)
        # button (clock): pressed for 0.25 s at each step
        down = 0.0
        if 0 <= since < 0.3: down = ease(since / 0.07) * (1 - ease((since - 0.22) / 0.08))
        dy = 26 * down
        sh = (self.arrow_box[0], self.arrow_box[1] + dy, self.arrow_box[2], self.arrow_box[3] + dy)
        paint(can, sh, self.arrow_a, CREAM) if dy == int(dy) else self.paint_shifted(can, dy)
        rrect(can, 3137.5, 162.5 + dy, 3237.5, 200.5, 3, PURPLE)
        lit_in(can, self.X[10], True, down); pin_glow(can, self.X[10], TOP, down)
        # light sensor (serial in): the camera fills with light when it sees light
        L = soft(self.light, t, 0.08)
        if L > 0:
            paint(can, self.cam_box, self.cam_in * 0.9 * L, (255, 249, 228))
        lit_in(can, self.X[11], True, L); pin_glow(can, self.X[11], TOP, L)
        return can

    def paint_shifted(self, can, dy):
        a = nd.shift(self.arrow_a, (dy - int(dy), 0), order=1, mode='constant')
        b = self.arrow_box; paint(can, (b[0], b[1] + int(dy), b[2], b[3] + int(dy)), a, CREAM)
