"""Make downloads/glitchn-chip-labels.pdf: a US Letter sheet of chip labels like the ones in the lesson videos.

Each label is LABEL_W x LABEL_H mm: small enough to sit on top of a 14-pin DIP (body about 19 x 6.4 mm)
with the notch end left showing. Labels sit edge to edge in a grid with thin grey cut lines.
Font: TeX Gyre Adventor (free, close to the Century Gothic-style numbers on the kit labels).
Run: python3 tools/make_labels.py   (needs Playwright's Chromium; writes the PDF and a preview PNG)
"""
import asyncio, pathlib
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
FONT = ROOT / 'tools' / 'fonts' / 'texgyreadventor-regular.otf'
FONT_B = ROOT / 'tools' / 'fonts' / 'texgyreadventor-bold.otf'
LOGO = ROOT / 'downloads' / 'logos' / 'glitchn-logo.svg'
LABEL_W, LABEL_H = 13.0, 5.6          # mm
COLS, ROWS = 14, 8                    # per chip block
CHIPS = [('40106', '14'), ('4040', '16'), ('4021', '16'), ('4051', '16')]

def block(num, legs):
    cells = ''.join(f'<div class="l">{num}</div>' for _ in range(COLS * ROWS))
    return f'<section><h2>{num} <span>· {legs} legs / {legs} patas</span></h2><div class="grid">{cells}</div></section>'

HTML = f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family: Adventor; src: url("file://{FONT}"); }}
@font-face {{ font-family: Adventor; font-weight: 700; src: url("file://{FONT_B}"); }}
@page {{ size: Letter; margin: 10mm 12.7mm; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; font-family: Adventor, sans-serif; color: #161514; }}
header {{ display: flex; justify-content: space-between; align-items: flex-end; gap: 6mm; margin-bottom: 4mm; }}
h1 {{ font-size: 13pt; margin: 0 0 1.2mm; font-weight: 700; }}
.logo {{ height: 9mm; display: block; margin-bottom: 2mm; }}
.copy {{ position: fixed; bottom: 0; left: 0; right: 0; font-size: 6.5pt; color: #5E5955; }}
header p {{ margin: 0; font-size: 7.6pt; line-height: 1.35; max-width: 120mm; }}
.scale {{ font-size: 6.5pt; text-align: right; }}
.bar {{ width: 50mm; height: 2.2mm; background: #161514; margin: 0 0 1mm auto; }}
section {{ margin-top: 2.6mm; break-inside: avoid; }}
h2 {{ font-size: 8pt; margin: 0 0 1.2mm; font-weight: 700; }}
h2 span {{ font-weight: 400; color: #5E5955; }}
.grid {{ display: grid; grid-template-columns: repeat({COLS}, {LABEL_W}mm); grid-auto-rows: {LABEL_H}mm;
        border-top: 0.12mm solid #9a9a9a; border-left: 0.12mm solid #9a9a9a; width: max-content; }}
.l {{ border-right: 0.12mm solid #9a9a9a; border-bottom: 0.12mm solid #9a9a9a;
     display: flex; align-items: center; justify-content: center; font-size: 8.6pt; letter-spacing: .02em; padding-top: .15mm; }}
</style></head><body>
<header><div>
<img class="logo" src="file://{LOGO}" alt="Glitch'n">
<h1>Chip labels</h1>
<p>Print at actual size (100%, not "fit to page") on full-sheet sticker paper. Cut along the grey lines.
Stick one label on top of each chip, with the notch end showing. Each label is {LABEL_W:g} × {LABEL_H:g} mm.<br>
Imprime a tamaño real (100 %) en papel adhesivo. Corta por las líneas grises y pega una etiqueta encima de cada chip, dejando visible la muesca.</p>
</div><div class="scale"><div class="bar"></div>This bar should measure 50 mm (about 2 in).<br>Esta barra debe medir 50 mm.</div></header>
{''.join(block(n, l) for n, l in CHIPS)}
<div class="copy">© Glitch'n · glitchn.net</div>
</body></html>'''

async def main():
    out = ROOT / 'downloads'
    out.mkdir(exist_ok=True)
    html = out / '_labels.html'
    html.write_text(HTML)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page()
        await pg.goto(html.as_uri()); await pg.wait_for_timeout(300)
        await pg.pdf(path=str(out / 'glitchn-chip-labels.pdf'), format='Letter', margin={'top': '10mm', 'bottom': '10mm', 'left': '12.7mm', 'right': '12.7mm'}, prefer_css_page_size=True, print_background=True)
        await b.close()
    html.unlink()

asyncio.run(main())
