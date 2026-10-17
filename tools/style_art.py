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
