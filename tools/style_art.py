"""Source drawings for the SVG art embedded in styles/*.css (vines, solar panel, rug, plants, radar, bird, lights…).
Each name below is a ready-to-paste CSS url("data:…") value. To change a drawing: edit it here, run
  python3 -c "import style_art as a; print(a.RUG)"   (from the tools folder)
and paste the printed value over the old one in the style file. The style files themselves are the source of truth."""
from urllib.parse import quote
def uri(svg): return 'url("data:image/svg+xml,' + quote(' '.join(svg.split()), safe=" =:/,;'()-.") + '")'
LEAF = "M0 0C5 -7 16 -8 22 0C16 8 5 7 0 0Z"
def leaves(spec, fill1='#3E9B57', fill2='#6CC07A'):
    out=''
    for i,(x,y,r,s) in enumerate(spec):
        out += f"<path d='{LEAF}' fill='{fill1 if i%2 else fill2}' transform='translate({x} {y}) rotate({r}) scale({s})'/>"
    return out
# a vine climbing up the left side of the screen and along the top
VINE = uri(f"""<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 190 130'>
<path d='M10 128C8 96 6 62 20 40S58 10 96 12S150 20 186 12' fill='none' stroke='#2E7D6B' stroke-width='3' stroke-linecap='round'/>
<path d='M60 15c-4 -8 -2 -14 6 -14' fill='none' stroke='#2E7D6B' stroke-width='2' stroke-linecap='round'/>
{leaves([(9,112,-120,1),(8,92,-60,1.05),(11,72,-130,1.1),(14,52,-50,1),(26,32,-150,1.05),(36,24,-40,1.1),(58,14,-160,1),(78,12,-30,1.05),(102,13,170,1),(124,16,-20,0.95),(150,16,160,0.9),(172,13,-25,0.8)])}
</svg>""")
# a solar panel on a stem, with two leaves
SOLAR = uri(f"""<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 160 84'>
<path d='M80 84V44' stroke='#2E7D6B' stroke-width='5' stroke-linecap='round'/>
<path d='M80 70C70 70 62 64 58 56' fill='none' stroke='#2E7D6B' stroke-width='3' stroke-linecap='round'/>
{leaves([(58,56,-150,1.1),(80,62,-20,1.15)])}
<g transform='translate(80 26) skewX(-12)'>
<rect x='-62' y='-22' width='124' height='40' rx='4' fill='#1F4E79' stroke='#173A33' stroke-width='3'/>
<g stroke='#9FC7EA' stroke-width='1.2' opacity='.9'><path d='M-31 -22V18M0 -22V18M31 -22V18M-62 -2H62'/></g>
<path d='M-56 -18L-38 -18L-52 14L-58 14Z' fill='#FFFFFF' opacity='.18'/>
</g>
<circle cx='150' cy='10' r='6' fill='#F2B41C'/>
<g stroke='#F2B41C' stroke-width='2' stroke-linecap='round'><path d='M150 0v-4M160 10h4M157 3l3-3M157 17l3 3M143 3l-3-3'/></g>
</svg>""")
# a little vine for the control bar's speaker area
WAVE = uri(f"""<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 48 24'>
<path d='M0 12C8 4 16 4 24 12S40 20 48 12' fill='none' stroke='#2E7D6B' stroke-width='2'/>
{leaves([(12,7,-140,.55),(36,17,40,.55)])}
</svg>""")
# leaves for the treehouse branch
BRANCH_LEAVES = uri(f"""<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 120 50'>
{leaves([(8,26,-150,1.3),(20,30,160,1.2),(14,22,-110,1.25),(34,24,-60,1.1),(30,30,120,1.2),(96,26,-30,1.3),(84,30,20,1.2),(104,22,-70,1.2),(88,24,-120,1.1)], '#4E8A33', '#73B04A')}
</svg>""")

# ---------- Solar Punk v2: cozy retro console ----------
# a Persian rug for the bottom of the page
def _rug():
    W,H=1000,250
    m=[]
    m.append(f"<rect x='0' y='12' width='{W}' height='{H-24}' rx='6' fill='#1F2F5C'/>")
    m.append(f"<rect x='22' y='32' width='{W-44}' height='{H-64}' fill='#B8382A'/>")
    m.append(f"<rect x='22' y='32' width='{W-44}' height='{H-64}' fill='none' stroke='#E8C98A' stroke-width='3'/>")
    m.append(f"<rect x='34' y='44' width='{W-68}' height='{H-88}' fill='none' stroke='#1F2F5C' stroke-width='4'/>")
    # border motifs
    for x in range(40, W-30, 34):
        m.append(f"<path d='M{x} 22l6-6 6 6-6 6z' fill='#E8C98A'/>"); m.append(f"<path d='M{x} {H-22}l6-6 6 6-6 6z' fill='#E8C98A'/>")
    for y in range(52, H-40, 30):
        m.append(f"<circle cx='11' cy='{y}' r='3.5' fill='#C9603B'/>"); m.append(f"<circle cx='{W-11}' cy='{y}' r='3.5' fill='#C9603B'/>")
    # central medallion
    cx,cy=W/2,H/2
    m.append(f"<path d='M{cx-170} {cy}L{cx} {cy-78}L{cx+170} {cy}L{cx} {cy+78}Z' fill='#1F2F5C'/>")
    m.append(f"<path d='M{cx-130} {cy}L{cx} {cy-58}L{cx+130} {cy}L{cx} {cy+58}Z' fill='#E8C98A'/>")
    m.append(f"<path d='M{cx-92} {cy}L{cx} {cy-40}L{cx+92} {cy}L{cx} {cy+40}Z' fill='#B8382A'/>")
    m.append(f"<circle cx='{cx}' cy='{cy}' r='16' fill='#1F2F5C'/><circle cx='{cx}' cy='{cy}' r='7' fill='#E8C98A'/>")
    for dx in (-300, 300):
        m.append(f"<path d='M{cx+dx-60} {cy}L{cx+dx} {cy-40}L{cx+dx+60} {cy}L{cx+dx} {cy+40}Z' fill='none' stroke='#E8C98A' stroke-width='4'/>")
        m.append(f"<circle cx='{cx+dx}' cy='{cy}' r='10' fill='#1F2F5C'/>")
    for (x,y) in [(60,60),(W-60,60),(60,H-60),(W-60,H-60)]:
        m.append(f"<path d='M{x-22} {y}L{x} {y-16}L{x+22} {y}L{x} {y+16}Z' fill='#1F2F5C'/>")
    # fringe
    fr=''.join(f"<path d='M{x} 12V2M{x} {H-12}V{H-2}' stroke='#E8DDC3' stroke-width='2'/>" for x in range(8, W, 9))
    return f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {W} {H}'>{fr}{''.join(m)}</svg>"
RUG = uri(_rug())

MONSTERA_LEAF = "M0 0C-14 -10 -20 -34 -6 -50C4 -60 22 -58 30 -44C38 -28 30 -8 0 0Z"
# a potted monstera (terracotta pot)
PLANT = uri(f"""<svg xmlns='http://www.w3.org/2000/svg' viewBox='-40 -50 245 240'>
<g stroke='#2F5A2A' stroke-width='3.5' fill='none' stroke-linecap='round'><path d='M75 140C68 112 50 92 26 78M75 140C76 104 78 74 86 46M75 140C84 116 106 102 132 94M75 140C64 124 48 120 22 124M75 140C90 118 110 70 130 52M75 140C70 110 58 64 44 40'/></g>
<g fill='#3F7A35' stroke='#24461F' stroke-width='2.2'>
<path d='{MONSTERA_LEAF}' transform='translate(26 78) rotate(-62) scale(1.25)'/>
<path d='{MONSTERA_LEAF}' transform='translate(86 46) rotate(8) scale(1.3)'/>
<path d='{MONSTERA_LEAF}' transform='translate(132 94) rotate(72) scale(1.15)'/>
<path d='{MONSTERA_LEAF}' transform='translate(22 124) rotate(-104) scale(1)'/>
<path d='{MONSTERA_LEAF}' transform='translate(130 52) rotate(40) scale(1.05)' fill='#4E8F3F'/>
<path d='{MONSTERA_LEAF}' transform='translate(44 40) rotate(-28) scale(1.1)' fill='#4E8F3F'/>
</g>
<path d='M44 136h62l-8 50H52z' fill='#C9603B' stroke='#3A2418' stroke-width='3' stroke-linejoin='round'/>
<rect x='38' y='128' width='74' height='14' rx='3' fill='#D8794F' stroke='#3A2418' stroke-width='3'/>
</svg>""")
# a trailing pothos hanging down
POTHOS_LEAF = "M0 0C-8 -4 -10 -14 -4 -20C2 -24 10 -22 12 -14C14 -6 8 0 0 0Z"
def _pothos():
    vines=''
    leaves=''
    import math
    for vx, length, sway in [(20,150,8),(46,110,-6),(70,170,10)]:
        pts=[(vx+sway*math.sin(i/2.2), i*10) for i in range(int(length/10)+1)]
        d='M'+' L'.join(f'{x:.1f} {y:.1f}' for x,y in pts)
        vines+=f"<path d='{d}' stroke='#2F5A2A' stroke-width='2' fill='none'/>"
        for i,(x,y) in enumerate(pts[1:]):
            side = 1 if i%2 else -1
            leaves+=f"<path d='{POTHOS_LEAF}' fill='{'#4E8F3F' if i%3 else '#7DB255'}' stroke='#24461F' stroke-width='1.2' transform='translate({x:.1f} {y+4:.1f}) rotate({side*60+180}) scale({1.1 - i*0.025:.2f})'/>"
    return f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 -6 100 186'>{vines}{leaves}</svg>"
POTHOS = uri(_pothos())
# a round radar dial
RADAR = uri("""<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 60 60'>
<circle cx='30' cy='30' r='28' fill='#C8562F' stroke='#2B2622' stroke-width='2.5'/>
<circle cx='30' cy='30' r='21' fill='#0E2A1C' stroke='#2B2622' stroke-width='2'/>
<g fill='none' stroke='#6EE59A' stroke-width='1' opacity='.75'><circle cx='30' cy='30' r='15'/><circle cx='30' cy='30' r='9'/><path d='M30 10v40M10 30h40'/></g>
<circle cx='36' cy='24' r='2' fill='#B8FFC9'/><circle cx='22' cy='36' r='1.5' fill='#B8FFC9'/>
<g fill='#F4EBD3'><circle cx='30' cy='4.5' r='1.6'/><circle cx='55.5' cy='30' r='1.6'/><circle cx='30' cy='55.5' r='1.6'/><circle cx='4.5' cy='30' r='1.6'/></g>
</svg>""")
RADAR_SWEEP = uri("""<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 60 60'><path d='M30 30L30 9A21 21 0 0 1 48 20Z' fill='#6EE59A' opacity='.45'/><path d='M30 30L30 9' stroke='#B8FFC9' stroke-width='1.5'/></svg>""")
# film grain
NOISE = uri("""<svg xmlns='http://www.w3.org/2000/svg' width='180' height='180'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 0.2  0 0 0 0 0.15  0 0 0 0 0.1  0 0 0 .3 0'/></filter><rect width='100%' height='100%' filter='url(#n)'/></svg>""")
# a screw head
SCREW = "radial-gradient(circle, #8A8170 0 1px, #D9D0BA 1.5px 3.6px, #6E6656 4px, transparent 4.6px)"

# ---------- Treehouse extras ----------
BIRD = uri("""<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 44 38'>
<path d='M8 22C8 12 16 6 25 7C33 8 37 15 36 21C35 29 27 33 19 32C12 31 8 27 8 22Z' fill='#5A7FB8' stroke='#3A2414' stroke-width='2.2'/>
<path d='M14 24C17 30 25 31 30 27C27 25 22 23 14 24Z' fill='#E9814A' stroke='#3A2414' stroke-width='1.6'/>
<path d='M10 18C4 16 1 18 2 21C5 21 7 21 10 21Z' fill='#41608F' stroke='#3A2414' stroke-width='1.8' stroke-linejoin='round'/>
<path d='M15 16C19 13 24 15 25 20C21 22 17 21 15 16Z' fill='#41608F' stroke='#3A2414' stroke-width='1.6'/>
<path d='M35 15L42 17L35 19Z' fill='#F2B33D' stroke='#3A2414' stroke-width='1.6' stroke-linejoin='round'/>
<circle cx='30' cy='14' r='2.3' fill='#3A2414'/><circle cx='30.8' cy='13.2' r='.8' fill='#FFF8E6'/>
<path d='M19 32V36M24 32V36M17 36H21M22 36H26' stroke='#3A2414' stroke-width='1.8' stroke-linecap='round'/>
</svg>""")
def _lights():
    W,H=400,40
    import math
    pts=[(x, 6+22*math.sin(math.pi*x/W)) for x in range(0,W+1,10)]
    d='M'+' L'.join(f'{x} {y:.1f}' for x,y in pts)
    bulbs=''
    for i,x in enumerate(range(20,W,36)):
        y=6+22*math.sin(math.pi*x/W)
        bulbs+=f"<path d='M{x} {y:.1f}v4' stroke='#3A2414' stroke-width='2'/><ellipse cx='{x}' cy='{y+9:.1f}' rx='4.2' ry='6' fill='{['#FFE07A','#FF9F6B','#9FE0FF','#B6F08C'][i%4]}' stroke='#3A2414' stroke-width='1.4'/>"
    return f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {W} {H}' preserveAspectRatio='none'><path d='{d}' fill='none' stroke='#3A2414' stroke-width='2'/>{bulbs}</svg>"
LIGHTS = uri(_lights())

# =====================================================================
# Quest: 1980s fantasy film at twilight
# =====================================================================
import random as _r
def _q_scene():
    _r.seed(7)
    W,H=1600,460
    o=[]
    for i in range(70):
        x,y=_r.randint(0,W),_r.randint(0,170); r=_r.choice([.8,1,1.2,1.6])
        o.append(f"<circle cx='{x}' cy='{y}' r='{r}' fill='#E9E4FF' opacity='{_r.choice([.35,.5,.7,.9])}'/>")
    o.append("<path d='M0 300L120 230L210 262L330 170L420 220L520 150L610 210L700 120L790 60L860 128L930 96L1040 190L1130 150L1230 214L1330 160L1450 236L1600 190V460H0Z' fill='#5A5C88'/>")
    o.append("<path d='M700 120L790 60L860 128L835 120L812 138L790 112L768 140L742 124Z' fill='#D9DCF2' opacity='.9'/>")
    o.append("<path d='M300 186L330 170L360 190L344 188L330 198L316 190Z' fill='#C9CCE8' opacity='.8'/>")
    o.append("<path d='M1000 260L1060 196L1200 190L1270 250Z' fill='#4A4B76'/>")
    o.append("<path d='M1110 160L1130 150L1150 162L1138 164L1130 172L1120 166Z' fill='#C9CCE8' opacity='.8'/>")
    cx=1130; base=196
    o.append("<g transform='translate(1130 196) scale(1.6) translate(-1130 -196)'>")
    def tower(x,w,h):
        return f"<rect x='{x}' y='{base-h}' width='{w}' height='{h+40}' fill='#11122A'/><path d='M{x-3} {base-h}L{x+w/2} {base-h-w*1.6}L{x+w+3} {base-h}Z' fill='#11122A'/>"
    for x,w,h in [(cx-70,16,40),(cx-46,12,62),(cx-24,22,92),(cx+6,14,70),(cx+26,18,52),(cx+50,12,34)]:
        o.append(tower(x,w,h))
    o.append(f"<path d='M{cx-80} {base+18}V{base-14}"+''.join(f'h6v-5h6v5' for _ in range(12))+f"V{base+18}Z' fill='#11122A'/>")
    o.append(f"<path d='M{cx-110} {base+40}L{cx-80} {base+14}H{cx+72}L{cx+100} {base+40}Z' fill='#2B2C4E'/>")
    for x,y in [(cx-20,base-70),(cx-14,base-50),(cx+10,base-44),(cx-42,base-36),(cx+30,base-28),(cx-62,base-18),(cx-4,base-8),(cx+44,base-10),(cx-30,base),(cx+16,base+4)]:
        o.append(f"<rect x='{x}' y='{y}' width='3.5' height='5' fill='#FFC66B'/>")
    o.append('</g>')
    o.append("<path d='M0 300C200 280 380 310 560 286S920 270 1100 292S1420 300 1600 280V340H0Z' fill='#9C9BC0' opacity='.35'/>")
    o.append("<path d='M0 360L140 300L260 330L400 280L520 320L640 290L760 336L900 300L1020 330L1160 284L1290 318L1420 290L1600 326V460H0Z' fill='#33355A'/>")
    def pine(x,h,c):
        return f"<path d='M{x} {460-h}L{x-h*.22:.0f} {460-h*.55:.0f}L{x-h*.12:.0f} {460-h*.55:.0f}L{x-h*.3:.0f} {460-h*.2:.0f}L{x-h*.16:.0f} {460-h*.2:.0f}L{x-h*.36:.0f} 460H{x+h*.36:.0f}L{x+h*.16:.0f} {460-h*.2:.0f}L{x+h*.3:.0f} {460-h*.2:.0f}L{x+h*.12:.0f} {460-h*.55:.0f}L{x+h*.22:.0f} {460-h*.55:.0f}Z' fill='{c}'/>"
    for x in range(-10,W+40,26):
        o.append(pine(x+_r.randint(-8,8), _r.randint(70,120), '#1F2A2A'))
    for x in list(range(0,260,34))+list(range(1340,W+40,34)):
        o.append(pine(x+_r.randint(-10,10), _r.randint(150,230), '#161E1F'))
    return f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {W} {H}' preserveAspectRatio='xMidYMax slice'>{''.join(o)}</svg>"
Q_SCENE = uri(_q_scene())
Q_TORCH = uri("""<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 40 120'>
<path d='M14 40L26 40L23 118L17 118Z' fill='#4A3222' stroke='#1E140C' stroke-width='2'/>
<path d='M10 34H30L27 46H13Z' fill='#6B6B78' stroke='#1E140C' stroke-width='2'/>
<path d='M12 52H28M12 60H28' stroke='#2A2B33' stroke-width='3'/>
</svg>""")
Q_FLAME = uri("""<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 40 50'>
<path d='M20 2C26 14 34 20 32 32C31 42 26 48 20 48C13 48 8 42 8 33C8 24 15 20 14 10C17 14 18 18 20 20C21 14 21 8 20 2Z' fill='#F28A2A'/>
<path d='M20 16C24 24 28 28 27 35C26 42 23 46 20 46C16 46 13 42 13 36C13 30 18 28 20 16Z' fill='#FFC94D'/>
<path d='M20 30C22 34 24 37 23 41C22 44 21 45 20 45C18 45 17 43 17 41C17 37 19 35 20 30Z' fill='#FFF3C4'/>
</svg>""")
Q_SEAL = uri("""<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'>
<path d='M50 3C58 6 62 2 69 8C76 13 82 9 86 18C90 26 97 28 95 38C93 47 99 52 94 61C90 69 94 76 86 82C79 88 77 95 67 95C58 96 54 100 46 96C38 92 31 97 24 90C17 84 9 85 7 75C5 66 0 61 4 52C8 44 2 37 8 29C13 22 12 13 21 10C30 7 35 0 50 3Z' fill='#8E1F22'/>
<circle cx='50' cy='50' r='34' fill='#A8292C'/><circle cx='50' cy='50' r='34' fill='none' stroke='#6E1416' stroke-width='3'/>
<circle cx='50' cy='50' r='27' fill='none' stroke='#C9474A' stroke-width='1.5' opacity='.7'/>
<path d='M30 30C40 22 58 22 70 32' fill='none' stroke='#E06A6C' stroke-width='3' stroke-linecap='round' opacity='.5'/>
</svg>""")
Q_LANTERN = uri("""<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 30 44'>
<path d='M15 1V6M10 6H20' stroke='#2A2015' stroke-width='2.5' stroke-linecap='round'/>
<path d='M8 10H22L24 34H6Z' fill='#FFD27A' stroke='#2A2015' stroke-width='2.5' stroke-linejoin='round'/>
<path d='M11 13V31M19 13V31' stroke='#2A2015' stroke-width='1.5' opacity='.6'/>
<path d='M5 34H25V39H5Z' fill='#5A4630' stroke='#2A2015' stroke-width='2'/>
<path d='M15 18C17 21 18 23 17 26C16 28 14 28 13 26C12 23 14 21 15 18Z' fill='#F28A2A'/>
</svg>""")
Q_COMPASS = uri("""<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'>
<g fill='none' stroke='#5B3A1E' stroke-width='1.5' opacity='.85'><circle cx='50' cy='50' r='34'/><circle cx='50' cy='50' r='29'/></g>
<path d='M50 6L56 44L94 50L56 56L50 94L44 56L6 50L44 44Z' fill='#5B3A1E' opacity='.85'/>
<path d='M50 6L56 44L50 50ZM94 50L56 56L50 50ZM50 94L44 56L50 50ZM6 50L44 44L50 50Z' fill='#C9A86A'/>
<path d='M50 24L53 47L76 50L53 53L50 76L47 53L24 50L47 47Z' fill='#8E1F22' opacity='.8' transform='rotate(45 50 50)'/>
</svg>""")
Q_ARCH = uri("""<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 80' preserveAspectRatio='none'>
<path d='M0 80V58C80 58 150 40 200 2C250 40 320 58 400 58V80Z' fill='#56586E' stroke='#1E1F2C' stroke-width='3'/>
<path d='M30 80V66C100 66 160 50 200 18C240 50 300 66 370 66V80Z' fill='#3A3B52'/>
<g stroke='#1E1F2C' stroke-width='2' opacity='.6'><path d='M200 2V18M140 40L152 52M260 40L248 52M80 56L84 66M320 56L316 66'/></g>
<path d='M188 30H212L208 50H192Z' fill='#FFC66B' opacity='.85'/><path d='M188 30H212L208 50H192Z' fill='none' stroke='#1E1F2C' stroke-width='2'/>
</svg>""")

# =====================================================================
# Skyline: a high-rise at dusk
# =====================================================================
def _s_city(seed=3, W=1600, H=320, lit=.32, far=False):
    _r.seed(seed)
    o=[]; x=-20
    while x<W:
        w=_r.randint(46,120); h=_r.randint(110,H-10) if not far else _r.randint(60,180)
        col = '#141B1C' if not far else '#22302F'
        o.append(f"<rect x='{x}' y='{H-h}' width='{w}' height='{h}' fill='{col}'/>")
        if not far and _r.random()<.3: o.append(f"<rect x='{x+w*.4:.0f}' y='{H-h-18}' width='3' height='18' fill='{col}'/>")
        for wy in range(H-h+10, H-6, 9):
            for wx in range(x+6, x+w-6, 8):
                if _r.random()<lit:
                    c=_r.choice(['#F3B562','#F7C97E','#E9A24E','#FFE0A6'])
                    o.append(f"<rect x='{wx}' y='{wy}' width='3.5' height='4.5' fill='{c}' opacity='{_r.choice([.55,.75,.95]) if not far else .45}'/>")
        x+=w+_r.randint(0,10)
    return f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {W} {H}' preserveAspectRatio='xMidYMax slice'>{''.join(o)}</svg>"
S_CITY = uri(_s_city())
S_CITY_FAR = uri(_s_city(seed=11, lit=.18, far=True))
S_PEAK = uri("""<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1600 420' preserveAspectRatio='xMidYMax slice'>
<path d='M0 420V330L180 290L330 310L460 280V420Z' fill='#3B4A4B' opacity='.8'/>
<g transform='translate(420 0)'>
<path d='M0 420V300L220 220L380 260L560 170L700 60L760 30L820 70L980 180L1140 230L1300 200L1600 280V420Z' fill='#3B4A4B'/>
<path d='M700 60L760 30L820 70L900 130L850 120L820 150L790 110L760 140L730 105L690 130L640 120Z' fill='#C9D5D5'/>
<path d='M640 120L690 130L730 105L760 140L790 110L820 150L850 120L900 130L980 180L900 170L860 190L820 168L780 196L740 166L700 188L650 162L600 170Z' fill='#A3B4B4' opacity='.8'/>
</g>
<path d='M0 300C300 270 500 300 800 280S1300 270 1600 290V420H0Z' fill='#4F6262' opacity='.45'/>
</svg>""")
def _s_windows(seed, n=46, W=420, H=420):
    _r.seed(seed)
    o=''.join(f"<rect x='{_r.randint(0,W-4)}' y='{_r.randint(0,H-5)}' width='3.5' height='4.5' fill='#F3B562' opacity='{_r.choice([.2,.3,.45])}'/>" for _ in range(n))
    return f"<svg xmlns='http://www.w3.org/2000/svg' width='{W}' height='{H}'>{o}</svg>"
S_WIN_A = uri(_s_windows(21))
S_WIN_B = uri(_s_windows(42, n=30))
S_LAMP = uri("""<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 120 260'>
<defs><radialGradient id='g' cx='.5' cy='.2' r='.8'><stop offset='0' stop-color='#FFD79A' stop-opacity='.55'/><stop offset='1' stop-color='#FFD79A' stop-opacity='0'/></radialGradient></defs>
<ellipse cx='70' cy='90' rx='60' ry='90' fill='url(#g)'/>
<path d='M30 256H60' stroke='#0C1011' stroke-width='6' stroke-linecap='round'/>
<path d='M45 254V70C45 40 60 26 80 26' fill='none' stroke='#0C1011' stroke-width='4'/>
<path d='M64 26H100L108 52H56Z' fill='#E9D3AE' stroke='#0C1011' stroke-width='2.5'/>
<path d='M60 52H104' stroke='#FFE4B0' stroke-width='3'/>
</svg>""")

# =====================================================================
# Daydream: a surreal cloud world
# =====================================================================
def _cloud(seed, W=600, H=280):
    puffs=[(W*.5,H*.62,H*.36),(W*.32,H*.7,H*.27),(W*.68,H*.68,H*.3),(W*.42,H*.42,H*.27),(W*.58,H*.36,H*.31),(W*.2,H*.8,H*.18),(W*.8,H*.8,H*.2),(W*.5,H*.22,H*.2)]
    sh=''.join(f"<circle cx='{x+6:.0f}' cy='{y+10:.0f}' r='{r:.0f}' fill='#B9CEF0'/>" for x,y,r in puffs)
    body=''.join(f"<circle cx='{x:.0f}' cy='{y:.0f}' r='{r:.0f}' fill='#FFFFFF'/>" for x,y,r in puffs)
    base=f"<rect x='{W*.16:.0f}' y='{H*.7:.0f}' width='{W*.68:.0f}' height='{H*.22:.0f}' rx='{H*.11:.0f}' fill='#DCE8FA'/>"
    return f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {W} {H}'>{sh}{base}{body}</svg>"
D_CLOUD_A = uri(_cloud(1))
D_CLOUD_B = uri(_cloud(2, 420, 200))
def _d_land(W=1600, H=300):
    _r.seed(5)
    o=[f"<rect width='{W}' height='{H}' fill='#5DA344'/>"]
    y=0
    while y<H:
        h=_r.randint(36,70); x=0
        while x<W:
            w=_r.randint(90,220); kind=_r.random()
            if kind<.45:
                o.append(f"<rect x='{x}' y='{y}' width='{w}' height='{h}' fill='#3F7F33'/>")
                for oy in range(y+7, y+h-3, 9):
                    for ox in range(x+6, x+w-3, 9):
                        o.append(f"<circle cx='{ox}' cy='{oy}' r='2.6' fill='{_r.choice(['#F07A2B','#E8682A','#F5953E'])}'/>")
            elif kind<.75:
                o.append(f"<rect x='{x}' y='{y}' width='{w}' height='{h}' fill='{_r.choice(['#7DBB4F','#98C95A','#6AAE45'])}'/>")
            else:
                o.append(f"<rect x='{x}' y='{y}' width='{w}' height='{h}' fill='#C9B36A'/>")
            o.append(f"<rect x='{x}' y='{y}' width='{w}' height='{h}' fill='none' stroke='#2F6A2A' stroke-width='2' opacity='.5'/>")
            x+=w
        y+=h
    for _ in range(7):
        cx,cy=_r.randint(60,W-60),_r.randint(40,H-30); rx=_r.randint(50,110)
        o.append(f"<ellipse cx='{cx}' cy='{cy}' rx='{rx+8}' ry='{rx*.42+8:.0f}' fill='#D9C27E'/><ellipse cx='{cx}' cy='{cy}' rx='{rx}' ry='{rx*.42:.0f}' fill='#2C6378'/><ellipse cx='{cx-rx*.2:.0f}' cy='{cy-rx*.12:.0f}' rx='{rx*.5:.0f}' ry='{rx*.12:.0f}' fill='#7FB8D6' opacity='.6'/>")
    o.append(f"<path d='M{W/2-26} 0H{W/2+26}V{H}H{W/2-26}Z' fill='#9FD3F5'/>")
    for yy in range(4, H, 14): o.append(f"<path d='M{W/2-26} {yy}H{W/2+26}' stroke='#FFFFFF' stroke-width='3' opacity='.8'/>")
    o.append(f"<path d='M{W/2-30} 0V{H}M{W/2+30} 0V{H}' stroke='#C7BCA6' stroke-width='8'/>")
    return f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {W} {H}' preserveAspectRatio='xMidYMin slice'>{''.join(o)}</svg>"
D_LAND = uri(_d_land())
def _d_arch(W=600, H=150):
    win=''.join(f"<rect x='{col+4}' y='{8+row*15}' width='8' height='10' rx='4' fill='#56627E' opacity='.5'/>" for row in range(10) for col in range(0, W, 18))
    outer=f"M0 {H}V70C0 30 {W*.22:.0f} 0 {W/2:.0f} 0S{W} 30 {W} 70V{H}Z"
    inner=f"M44 {H}V96C44 70 {W*.28:.0f} 44 {W/2:.0f} 44S{W-44} 70 {W-44} 96V{H}Z"
    return f"""<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {W} {H}' preserveAspectRatio='none'>
<defs><clipPath id='c'><path d='{outer}'/></clipPath><mask id='m'><rect width='{W}' height='{H}' fill='#fff'/><path d='{inner}' fill='#000'/></mask></defs>
<g clip-path='url(#c)' mask='url(#m)'><rect width='{W}' height='{H}' fill='#8D98AE'/>{win}<rect width='{W}' height='{H}' fill='#FFFFFF' opacity='.12'/></g>
<path d='{outer}' fill='none' stroke='#2B3550' stroke-width='3'/>
<path d='{inner}' fill='none' stroke='#2B3550' stroke-width='3'/>
<path d='M44 {H}V96C44 70 {W*.28:.0f} 44 {W/2:.0f} 44S{W-44} 70 {W-44} 96V{H}' fill='none' stroke='#E6ECF5' stroke-width='3' opacity='.7' transform='translate(0 5)'/>
</svg>"""
D_ARCH = uri(_d_arch())
D_RAFT = uri("""<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 50 40'>
<ellipse cx='25' cy='30' rx='22' ry='8' fill='#2F4F9E' stroke='#17305E' stroke-width='2.5'/>
<ellipse cx='25' cy='28' rx='15' ry='4.5' fill='#5C7FD0'/>
<path d='M25 26C21 26 20 18 25 17C30 18 29 26 25 26Z' fill='#E9EEF7' stroke='#17305E' stroke-width='2'/>
<circle cx='25' cy='13' r='4.5' fill='#3A2A20' stroke='#17305E' stroke-width='1.5'/>
<path d='M8 20L38 34' stroke='#17305E' stroke-width='2.5' stroke-linecap='round'/><path d='M4 18L12 22L10 25Z' fill='#F07A2B' stroke='#17305E' stroke-width='1.5'/>
</svg>""")

Q_STONE = uri("""<svg xmlns='http://www.w3.org/2000/svg' width='160' height='64'>
<rect width='160' height='64' fill='#24253A'/>
<g><rect x='1' y='1' width='50' height='30' rx='3' fill='#4E5068'/><rect x='53' y='1' width='54' height='30' rx='3' fill='#46485E'/><rect x='109' y='1' width='50' height='30' rx='3' fill='#525470'/>
<rect x='-26' y='33' width='52' height='30' rx='3' fill='#4A4C64'/><rect x='28' y='33' width='50' height='30' rx='3' fill='#525470'/><rect x='80' y='33' width='52' height='30' rx='3' fill='#46485E'/><rect x='134' y='33' width='52' height='30' rx='3' fill='#4E5068'/></g>
<g fill='#FFFFFF' opacity='.05'><rect x='4' y='3' width='40' height='3'/><rect x='58' y='3' width='40' height='3'/><rect x='32' y='35' width='40' height='3'/><rect x='84' y='35' width='40' height='3'/></g>
</svg>""")

# a burnt-orange sofa and a low table, for the foot of the Skyline page
S_SOFA = uri("""<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 700 190'>
<ellipse cx='350' cy='182' rx='330' ry='10' fill='#000000' opacity='.45'/>
<rect x='40' y='40' width='620' height='80' rx='22' fill='#A9501F'/>
<rect x='60' y='50' width='186' height='70' rx='16' fill='#C0612B'/><rect x='257' y='50' width='186' height='70' rx='16' fill='#C0612B'/><rect x='454' y='50' width='186' height='70' rx='16' fill='#C0612B'/>
<rect x='20' y='96' width='660' height='60' rx='18' fill='#B85A26'/>
<rect x='36' y='104' width='200' height='40' rx='12' fill='#CC6A31'/><rect x='250' y='104' width='200' height='40' rx='12' fill='#CC6A31'/><rect x='464' y='104' width='200' height='40' rx='12' fill='#CC6A31'/>
<rect x='4' y='70' width='46' height='96' rx='18' fill='#A9501F'/><rect x='650' y='70' width='46' height='96' rx='18' fill='#A9501F'/>
<rect x='560' y='58' width='60' height='46' rx='12' fill='#8F4219' transform='rotate(-10 590 80)'/>
<path d='M30 160H670' stroke='#7A3814' stroke-width='6' stroke-linecap='round'/>
<rect x='70' y='160' width='10' height='18' fill='#2A1A10'/><rect x='620' y='160' width='10' height='18' fill='#2A1A10'/>
<path d='M120 100C140 90 190 92 210 104L200 140C180 136 140 136 120 140Z' fill='#2C3334' opacity='.9'/>
</svg>""")

# the stone of the great arch: little arched windows, for tiling
D_STONEWIN = uri("""<svg xmlns='http://www.w3.org/2000/svg' width='18' height='16'><rect width='18' height='16' fill='#8D98AE'/><rect x='5' y='3' width='8' height='10' rx='4' fill='#56627E' opacity='.55'/></svg>""")
