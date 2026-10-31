#!/usr/bin/env python3
"""Keep the Content-Security-Policy in sync with each page's inline <script> and <style> (all *.html in root).

    python3 tools/update-csp.py           rewrite the policy in index.html and _headers
    python3 tools/update-csp.py --check   exit 1 if the policy is stale (used by tools/hooks/pre-commit)

The policy allows no inline code except blocks whose sha256 hash it lists. Editing the inline theme
script or ANY CSS in the <style> block changes its hash, and a stale hash makes the browser ignore the
block: the site loses its JavaScript set-up or all of its styling. So rerun this after every such edit.
Install the guard once per clone:  git config core.hooksPath tools/hooks

Where the policy lives:
  index.html <meta>  works on any host. Browsers ignore frame-ancestors there, so it's left out.
  _headers           real HTTP headers on Cloudflare Pages (ignored by GitHub Pages), with frame-ancestors.
Both are enforced together when both are present, so they must match; this script writes both.
"""
import base64, hashlib, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES, HEADERS = sorted(ROOT.glob('*.html')), ROOT / '_headers'
# connect-src 'self': nothing on the site fetches, but Lighthouse reads robots.txt via an in-page fetch and
# reports it missing under 'none'. Same-origin only, on a static host, so it opens nothing exploitable.
POLICY = ("default-src 'none'; script-src 'self' {scripts}; style-src {styles}; font-src 'self'; "
          "img-src 'self'; connect-src 'self'; base-uri 'none'; form-action 'none'; upgrade-insecure-requests")
META = re.compile(r'<meta http-equiv="Content-Security-Policy" content="[^"]*" />')
HEADER = re.compile(r'^(  Content-Security-Policy: ).*$', re.M)
# Inline scripts that execute; JSON-LD and other data blocks don't, so CSP doesn't apply to them.
SCRIPT = re.compile(r'<script(?![^>]*\bsrc=)(?![^>]*type="application/ld\+json")[^>]*>(.*?)</script>', re.S)
STYLE = re.compile(r'<style[^>]*>(.*?)</style>', re.S)

sha = lambda s: "'sha256-" + base64.b64encode(hashlib.sha256(s.encode()).digest()).decode() + "'"

def hashes(html):
    code = re.sub(r'<!--.*?-->', '', html, flags=re.S)    # a comment mentioning "<style>" must not count as one
    return [sha(s) for s in SCRIPT.findall(code)], [sha(s) for s in STYLE.findall(code)]


def policy(scripts, styles):
    uniq = lambda xs: ' '.join(dict.fromkeys(xs))
    return POLICY.format(scripts=uniq(scripts), styles=uniq(styles) or "'self'")


writes, all_scripts, all_styles = [], [], []
for page in PAGES:
    html = page.read_text(encoding='utf-8')
    if not META.search(html):
        sys.exit(f'{page.name}: no CSP <meta> to update; add one right after <meta charset>.')
    if re.search(r'\sstyle="|\son\w+="', html):
        sys.exit(f'{page.name}: inline style="" or on*="" handler found; the policy blocks those. '
                 'Move it into the <style> block or script.js.')
    sc, st = hashes(html); all_scripts += sc; all_styles += st
    meta = f'<meta http-equiv="Content-Security-Policy" content="{policy(sc, st)}" />'   # each page: only its own blocks
    writes.append((page, html, META.sub(lambda _: meta, html)))
# One header policy covers every path, so it lists every page's hashes.
headers = HEADERS.read_text(encoding='utf-8')
writes.append((HEADERS, headers, HEADER.sub(lambda m: m[1] + policy(all_scripts, all_styles) + "; frame-ancestors 'none'", headers)))

stale = [p.name for p, old, new in writes if old != new]
if '--check' in sys.argv:
    if stale: sys.exit(f'CSP is stale in {", ".join(stale)}: run python3 tools/update-csp.py')
    print('CSP up to date'); sys.exit(0)
for p, old, new in writes:
    if old != new: p.write_text(new, encoding='utf-8')
print(('updated: ' + ', '.join(stale)) if stale else 'already up to date')
