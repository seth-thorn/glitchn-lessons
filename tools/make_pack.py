"""Make downloads/glitchn-pack.zip: everything in downloads/ that people print or share, in one file.
Run after changing anything in downloads/:  python3 tools/make_pack.py"""
import pathlib, zipfile
ROOT = pathlib.Path(__file__).resolve().parent.parent
D = ROOT / 'downloads'
README = """GLITCH'N PACK  /  PAQUETE GLITCH'N
glitchn.net

logos/        Glitch'n logos (SVG, PNG)
stickers/     Stickers, 3 in and 6 in (PDF, SVG)
chip-labels/  Chip labels. Print at 100% on sticker paper.
chip-maps/    What each leg of each chip does (PDF, JPG)
colors/       Glitch'n colors

logos/        Logos de Glitch'n (SVG, PNG)
stickers/     Calcomanías, 3 y 6 pulgadas (PDF, SVG)
chip-labels/  Etiquetas para chips. Imprime al 100 % en papel adhesivo.
chip-maps/    Qué hace cada pata de cada chip (PDF, JPG)
colors/       Colores de Glitch'n

(c) Glitch'n. School of Games, Arts, Media and Engineering, Arizona State University.
"""
PLAN = [('logos', 'logos'), ('stickers', 'stickers'), ('pinouts', 'chip-maps'), ('colors', 'colors')]
out = D / 'glitchn-pack.zip'
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr('glitchn-pack/README.txt', README)
    z.write(D / 'glitchn-chip-labels.pdf', 'glitchn-pack/chip-labels/glitchn-chip-labels.pdf')
    for src, dst in PLAN:
        for f in sorted((D / src).iterdir()):
            if f.is_file() and not f.name.startswith('.'):
                z.write(f, f'glitchn-pack/{dst}/{f.name}')
print(out, round(out.stat().st_size / 1048576, 2), 'MB')
