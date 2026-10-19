"""Stamp a version on the site's own CSS and JS links (?v=...), so browsers fetch the new files after a change
instead of using a copy they kept (GitHub Pages lets browsers keep files for 10 minutes).
Run after changing any CSS or JS:  python3 tools/bump_version.py   (uses the date and time as the version)."""
import re, sys, time, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
V = sys.argv[1] if len(sys.argv) > 1 else time.strftime('%Y%m%d%H%M')
NAMES = r'(site\.css|site\.js|parts-art\.js|player\.css|player\.js|all\.css|[a-z]+\.css)'
pat = re.compile(r'((?:\.\./|\./|/)?(?:[\w-]+/)*' + NAMES + r')(\?v=\w+)?(?=["\')])')
files = [p for p in ROOT.rglob('*') if p.suffix in ('.html', '.css', '.py', '.js') and '.git' not in p.parts and p.name != 'bump_version.py']
changed = 0
for p in files:
    s = p.read_text(encoding='utf-8')
    if p.suffix == '.css':      # only the @import lines in styles/all.css
        new = re.sub(r'@import url\("([a-z]+\.css)(\?v=\w+)?"\)', lambda m: '@import url("%s?v=%s")' % (m.group(1), V), s)
    elif p.suffix == '.js':     # player.js loads parts-art.js itself
        new = re.sub(r"'\.\./parts-art\.js(\?v=\w+)?'", "'../parts-art.js?v=%s'" % V, s)
    else:                       # <link href> and <script src> in pages, and the lesson page template in tools/build_index.py
        new = re.sub(r'((?:href|src)=")([^"]*?/)?' + NAMES + r'(\?v=\w+)?"', lambda m: '%s%s%s?v=%s"' % (m.group(1), m.group(2) or '', m.group(3), V), s)
    if new != s:
        p.write_text(new, encoding='utf-8'); changed += 1; print('stamped', p.relative_to(ROOT))
print('version', V, '-', changed, 'files')
