#!/usr/bin/env python3
"""Build the link-preview card and favicons from the site's own font and colours. Run by hand; commit output.

    pip install fonttools brotli pillow playwright && playwright install chromium
    python3 tools/build-images.py

Writes  og-image.png (1200x630)   shown when the site is shared on LinkedIn, Slack, WhatsApp, X
        favicon.svg               the mark, drawn from Inter's outlines (no font needed to display it)
        favicon.ico (16/32/48), apple-touch-icon.png (180)

Rerun when the hero headline, name, role line or accent colour changes. Link previews are cached by
each platform: after deploying, refresh LinkedIn's with its Post Inspector.
"""
import base64, io, os
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.varLib.instancer import instantiateVariableFont
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
BG, INK, MUTED, ACCENT = '#0C0E0F', '#E1DDD6', '#B0A89C', '#F73D32'   # dark theme tokens in style.css


def favicon_svg():
    """'M' plus a red full stop, the same full stop that ends every heading on the site."""
    f = instantiateVariableFont(TTFont(ROOT / 'fonts/src/inter-latin.woff2'), {'wght': 500})
    gs, cmap, upm = f.getGlyphSet(), f.getBestCmap(), f['head'].unitsPerEm
    s = 40 / upm                                   # cap height ~29px in a 64px tile
    def path(ch, x):
        pen = SVGPathPen(gs)
        gs[cmap[ord(ch)]].draw(TransformPen(pen, (s, 0, 0, -s, x, 46)))
        return pen.getCommands(), gs[cmap[ord(ch)]].width * s
    m, mw = path('M', 0)
    left = (64 - mw - 9) / 2                       # centre M + dot as one group
    m, _ = path('M', left)
    dot, _ = path('.', left + mw - 2)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
            f'<rect width="64" height="64" rx="14" fill="{BG}"/>'
            f'<path fill="{INK}" d="{m}"/><path fill="{ACCENT}" d="{dot}"/></svg>\n')


OG = f"""<!doctype html><meta charset="utf-8"><style>
@font-face {{ font-family: Inter; font-weight: 100 400; src: url(fonts/inter-core.woff2); }}
* {{ margin: 0; }}
body {{ width: 1200px; height: 630px; background: {BG}; color: {INK}; font: 300 22px Inter;
       -webkit-font-smoothing: antialiased; position: relative; overflow: hidden; }}
.mark {{ position: absolute; left: 72px; top: 60px; font-weight: 400; font-size: 30px; line-height: 1; letter-spacing: -0.02em; }}
h1 {{ position: absolute; left: 72px; top: 170px; font-weight: 300; font-size: 156px; line-height: 1.0; letter-spacing: -0.035em; }}
h1 span {{ color: {ACCENT}; }}
.foot {{ position: absolute; left: 72px; right: 72px; bottom: 56px; display: flex; justify-content: space-between;
        font-size: 22px; font-weight: 400; color: {MUTED}; }}
.foot b {{ font-weight: 400; color: {INK}; }}
</style><div class="mark">Maaz<br>Husain</div>
<h1>Secure by<br><span>Design.</span></h1>
<div class="foot"><span><b>Cybersecurity Analyst</b> · DFIR · SOC tooling · Cloud security</span><span>maazhusain.com</span></div>"""


def main():
    svg = favicon_svg()
    (ROOT / 'favicon.svg').write_text(svg)
    tmp = ROOT / '.og-tmp.html'
    tmp.write_text(OG)
    try:
        with sync_playwright() as p:
            b = p.chromium.launch(executable_path=os.environ.get('CHROME'))   # CHROME=/path to use a local Chrome
            pg = b.new_page(viewport={'width': 1200, 'height': 630})
            pg.goto(tmp.as_uri()); pg.evaluate('document.fonts.ready')
            assert pg.evaluate("document.fonts.check('300 20px Inter')"), 'Inter did not load for og-image'
            pg.screenshot(path=str(ROOT / 'og-image.png'))
            pg.set_viewport_size({'width': 180, 'height': 180})
            img = f'<img src="data:image/svg+xml;base64,{base64.b64encode(svg.encode()).decode()}" width="180" height="180">'
            # iOS rounds corners itself, so the touch icon gets square corners in the tile colour.
            pg.set_content(f'<style>*{{margin:0}}body{{background:{BG}}}</style>{img}')
            Image.open(io.BytesIO(pg.screenshot())).convert('RGB').save(ROOT / 'apple-touch-icon.png', optimize=True)
            # Tabs show the .ico as-is, so it keeps transparent rounded corners.
            pg.set_content(f'<style>*{{margin:0}}</style>{img}')
            ico = Image.open(io.BytesIO(pg.screenshot(omit_background=True))).convert('RGBA')
            b.close()
    finally:
        tmp.unlink()
    ico.resize((48, 48), Image.LANCZOS).save(ROOT / 'favicon.ico', sizes=[(16, 16), (32, 32), (48, 48)])
    for n in ('og-image.png', 'favicon.svg', 'favicon.ico', 'apple-touch-icon.png'):
        print(f'{n:22} {(ROOT / n).stat().st_size:>6} B')


if __name__ == '__main__':
    main()
