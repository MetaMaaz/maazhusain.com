# maazhusain.com

Personal portfolio website for Maaz Husain — Cybersecurity Analyst & Senior Quality Engineer.

🔗 **Live site:** [maazhusain.com](https://maazhusain.com)

## Stack

- HTML, CSS, JavaScript — no frameworks, no dependencies, no build step
- Hosted on GitHub Pages

## Structure

```
├── index.html               # Markup and content (CSP, link-preview tags, JSON-LD in <head>)
├── style.css                # All styles; the @font-face block at the top is generated
├── script.js                # Theme toggle, full-screen menu, scroll reveal
├── fonts/
│   ├── inter-core.woff2     # Preloaded subset (generated)
│   ├── inter-ext.woff2      # Latin Extended-A, loads only when used (generated)
│   └── src/                 # Inter source files the subsets are cut from
├── og-image.png             # Link-preview card (generated)
├── favicon.svg / .ico, apple-touch-icon.png   # (generated)
├── .well-known/security.txt # RFC 9116 contact; renew Expires before 2027-10-31
├── robots.txt, sitemap.xml
├── _config.yml              # Lets Jekyll publish .well-known (and nothing else hidden)
├── tools/                   # Hand-run scripts, see below
└── CNAME                    # Custom domain config for GitHub Pages
```

## Hand-run tools

Generated files are committed; nothing runs on deploy. Rerun the matching script after these changes:

| Change | Run |
|---|---|
| Edit the inline `<script>` in `<head>` (or add inline code anywhere) | `python3 tools/update-csp.py` — otherwise the browser blocks it |
| New font weight, characters outside Latin-1 / Latin Extended-A, OpenType features | `python3 tools/build-fonts.py` |
| Hero headline, name, role line or accent colour | `python3 tools/build-images.py`, then refresh LinkedIn's Post Inspector |
| Content edits | update `<lastmod>` in `sitemap.xml` |
| Every October | bump `Expires` in `.well-known/security.txt` |

Setup: `pip install fonttools brotli pillow playwright && playwright install chromium`.
Each script's docstring has the details.

## Features

- Light / dark mode with localStorage persistence
- Scroll-triggered reveal animations; content stays visible without JavaScript and with reduced motion
- Strict Content-Security-Policy (no inline code except one hashed script)
- Responsive layout down to mobile
- Sections: Experience, Projects, Skills, Certifications, References, Education, Contact
