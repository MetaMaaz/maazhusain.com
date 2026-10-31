# maazhusain.com

Personal portfolio website for Maaz Husain — Cybersecurity Analyst & Senior Quality Engineer.

🔗 **Live site:** [maazhusain.com](https://maazhusain.com)

## Stack

- HTML, CSS, JavaScript — no frameworks, no dependencies, no build step of its own
- Hosted on GitHub Pages; ready for Cloudflare Pages (see below)

## Structure

```
├── index.html               # Markup, all CSS (inline <style>), CSP, link-preview tags, JSON-LD
├── 404.html                 # Not-found page (real 404 status on both hosts; without it Cloudflare
│                            # serves the homepage with 200 for every unknown URL)
├── script.js                # Theme toggle, full-screen menu, scroll reveal
├── fonts/
│   ├── inter-core.woff2     # Preloaded subset (generated)
│   ├── inter-ext.woff2      # Latin Extended-A, loads only when used (generated)
│   └── src/                 # Inter source files the subsets are cut from
├── og-image.png             # Link-preview card (generated)
├── favicon.svg / .ico, apple-touch-icon.png   # (generated)
├── .well-known/security.txt # RFC 9116 contact; renew Expires before 2027-10-31
├── robots.txt, sitemap.xml
├── _headers                 # HTTP security headers for Cloudflare Pages (CSP line generated)
├── _config.yml              # Lets Jekyll publish .well-known and _headers, and nothing else hidden
├── .github/workflows/       # Wake Streamlit demos every 6 h; check CSP hashes on every push
├── tools/                   # Hand-run scripts, see below; tools/hooks has the pre-commit guard
└── CNAME                    # Custom domain config for GitHub Pages
```

## First time in a new clone

```
git config core.hooksPath tools/hooks
pip install fonttools brotli pillow playwright && playwright install chromium
```

The hook refuses a commit whose CSP hashes are stale.

## Hand-run tools

Generated files are committed; nothing runs on deploy. Rerun the matching script after these changes:

| Change | Run |
|---|---|
| **Any CSS edit**, or editing the inline `<script>` in `<head>` | `python3 tools/update-csp.py` (covers every *.html) — a stale hash makes browsers drop all styling or the theme script |
| New font weight, characters outside Latin-1 / Latin Extended-A, OpenType features | `python3 tools/build-fonts.py` (also refreshes the CSP) |
| Hero headline, name, role line or accent colour | `python3 tools/build-images.py`, then refresh LinkedIn's Post Inspector |
| Before sending applications | `python3 tools/check-links.py` |
| Content edits | update `<lastmod>` in `sitemap.xml` |
| Every October | bump `Expires` in `.well-known/security.txt` |

Each script's docstring has the details.

## Demos

- Streamlit demos are visited every 6 hours by `.github/workflows/wake-demos.yml` (Streamlit sleeps
  apps after 12 hours). A red run means a demo failed to start. GitHub pauses scheduled workflows after
  60 days without commits; re-enable it under Actions if so.
- The ThreatLens demo on Render sleeps after 15 minutes, too often for GitHub's scheduler, so the site
  labels the cold start. To keep it warm instead, add a free UptimeRobot HTTP monitor on
  `https://threatlens-demo.onrender.com` every 5 minutes (one always-on service fits Render's 750 free
  hours a month, but not two), then delete the note next to its link.

## Moving to Cloudflare Pages (for real security headers)

GitHub Pages can't send HTTP headers; Cloudflare Pages reads `_headers`. In the Cloudflare dashboard:
Workers & Pages → Create → Pages → connect this repo, then

- Build command: `gem install jekyll -v 4.4.1 --no-document && jekyll build`
- Build output directory: `_site`

This runs the same Jekyll build GitHub Pages does, so it publishes the same files (and `_headers`).
Then add the custom domain `maazhusain.com` there; for a root domain Cloudflare asks you to move the
domain's nameservers to Cloudflare at your registrar. Once it serves the site, turn off GitHub Pages.

## Features

- Light / dark mode with localStorage persistence
- Scroll-triggered reveal animations; content stays visible without JavaScript and with reduced motion
- Strict Content-Security-Policy: no inline code except two hashed blocks
- Responsive layout down to mobile
- Sections: Experience, Projects, Skills, Certifications, References, Education, Contact
