#!/usr/bin/env python3
"""Check every outbound link on the site. Changes nothing. Standard library only.

    python3 tools/check-links.py

For each unique https:// link in *.html: status, where it redirects, and response time. Flags
  BROKEN  4xx/5xx or unreachable
  SLOW    first response > 5 s, typical of a sleeping free-tier demo (Render, Streamlit) waking up;
          the script requests it twice so you can see the cold vs warm time
Run before sending applications, and after renaming a GitHub repo or moving a demo.
  CHECK   redirect loop the script can't follow (Streamlit sets a cookie first); open it in a browser
Some sites (LinkedIn, Credly) block scripts with 999/403; those are reported as BLOCKED, not broken:
open them in a browser to confirm. Behind a proxy that only allows git (some CI sandboxes), github.com
pages return 403; from a normal connection they should be 200.
"""
import re, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36'
BLOCKERS = ('linkedin.com', 'credly.com')


def fetch(url):
    t = time.monotonic()
    try:
        r = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=60)
        return r.status, r.url, time.monotonic() - t
    except urllib.error.HTTPError as e:
        return e.code, e.url, time.monotonic() - t
    except Exception as e:
        return type(e).__name__, url, time.monotonic() - t


def check(url):
    status, final, secs = fetch(url)
    warm = fetch(url)[2] if secs > 5 else None
    if isinstance(status, int) and 300 <= status < 400: flag = 'CHECK'   # redirect loop: site wants cookies (Streamlit)
    elif isinstance(status, int) and status < 400: flag = 'SLOW' if secs > 5 else 'ok'
    elif any(b in url for b in BLOCKERS) and status in (999, 403, 429): flag = 'BLOCKED'
    else: flag = 'BROKEN'
    moved = f'  -> {final}' if final.rstrip('/') != url.rstrip('/') else ''
    timing = f'{secs:5.1f}s' + (f' (warm {warm:.1f}s)' if warm else '')
    return f'{flag:7} {status!s:>4} {timing:18} {url}{moved}'


links = sorted({u for p in ROOT.glob('*.html') for u in re.findall(r'href="(https://[^"]+)"', p.read_text())}
               - {'https://maazhusain.com/'})
with ThreadPoolExecutor(8) as pool:
    for line in pool.map(check, links):
        print(line)
