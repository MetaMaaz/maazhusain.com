#!/usr/bin/env python3
"""Keep the Content-Security-Policy <meta> in every page in sync with its inline scripts.

    python3 tools/update-csp.py

Rerun after editing any inline <script> in a page (today: the theme script in <head>), then commit.
The policy allows no inline code except scripts whose sha256 hash it lists, so an edited script
silently stops running until this is rerun. Pages: *.html in the repo root.

GitHub Pages can't send headers, so the policy lives in <meta>. Browsers ignore frame-ancestors,
report-uri and sandbox there, so they're left out rather than shipped as dead weight.
"""
import base64, hashlib, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POLICY = ("default-src 'none'; script-src 'self' {hashes}; style-src 'self'; font-src 'self'; "
          "img-src 'self'; base-uri 'none'; form-action 'none'; upgrade-insecure-requests")
META = re.compile(r'<meta http-equiv="Content-Security-Policy" content="[^"]*" />')
# Inline scripts that execute; JSON-LD and other data blocks don't, so CSP doesn't apply to them.
SCRIPT = re.compile(r'<script(?![^>]*\bsrc=)(?![^>]*type="application/ld\+json")[^>]*>(.*?)</script>', re.S)

for page in sorted(ROOT.glob('*.html')):
    html = page.read_text(encoding='utf-8')
    if not META.search(html):
        sys.exit(f'{page.name}: no CSP <meta> to update; add one right after <meta charset>.')
    if re.search(r'\sstyle="|<style[\s>]|\son\w+="', html):
        sys.exit(f"{page.name}: inline style or event handler found; style-src/script-src 'self' would block it.")
    hashes = ' '.join("'sha256-" + base64.b64encode(hashlib.sha256(s.encode()).digest()).decode() + "'"
                      for s in SCRIPT.findall(html))
    new = META.sub(f'<meta http-equiv="Content-Security-Policy" content="{POLICY.format(hashes=hashes)}" />', html)
    if new != html:
        page.write_text(new, encoding='utf-8')
    print(f'{page.name}: {hashes or "no inline scripts"}')
