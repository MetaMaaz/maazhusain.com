#!/usr/bin/env python3
"""Visit every Streamlit demo linked from the site, waking any that have gone to sleep.

    pip install playwright && playwright install chromium
    python3 tools/wake-demos.py

Run every 6 hours by .github/workflows/wake-demos.yml. Streamlit Community Cloud puts apps to sleep
after 12 hours without traffic, and only a real browser visit counts (a plain HTTP request doesn't open
the app's websocket). Exits non-zero if a demo doesn't come up, so GitHub emails you about a broken demo.

Not covered: the ThreatLens demo on Render sleeps after 15 minutes idle, too often for GitHub's
best-effort scheduler; the site labels its cold start instead. See README for the UptimeRobot option.
"""
import os, re, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
URLS = sorted(set(re.findall(r'href="(https://[\w-]+\.streamlit\.app/?)"', (ROOT / 'index.html').read_text())))
WAKE = 'Yes, get this app back up'


def app_ready(page):
    """The app renders inside an iframe; it's up once any frame has Streamlit's root element."""
    return any(f.query_selector('[data-testid="stApp"]') for f in page.frames)


def main():
    failed = []
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=os.environ.get('CHROME'))
        for url in URLS:
            page = browser.new_page()
            page.goto(url, wait_until='domcontentloaded', timeout=90_000)
            state = 'awake'
            for _ in range(90):                       # up to ~3 minutes for a cold boot
                if app_ready(page): break
                button = page.get_by_role('button', name=WAKE)
                if button.count():
                    button.first.click(); state = 'was asleep, woken'
                page.wait_for_timeout(2000)
            else:
                state = 'DID NOT COME UP'; failed.append(url)
            print(f'{state:18} {url}')
            page.close()
        browser.close()
    if failed: sys.exit(f'{len(failed)} demo(s) failed to start: {failed}')


if __name__ == '__main__':
    main()
