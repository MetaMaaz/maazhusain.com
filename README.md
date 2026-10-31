# maazhusain.com

Personal portfolio website for Maaz Husain — Cybersecurity Analyst & Senior Quality Engineer.

🔗 **Live site:** [maazhusain.com](https://maazhusain.com)

## Stack

- HTML, CSS, JavaScript — no frameworks, no dependencies
- Hosted on GitHub Pages

## Structure

```
├── index.html             # Markup and content
├── style.css              # All styles (tokens, layout, components, light/dark)
├── script.js              # Theme toggle, full-screen menu, scroll reveal
├── fonts/
│   ├── inter-core.woff2   # Preloaded subset (generated)
│   ├── inter-ext.woff2    # Latin Extended-A, loads only when used (generated)
│   ├── fonts.css          # @font-face rules (generated)
│   └── src/               # Inter source files the subsets are cut from
├── tools/build-fonts.py   # Hand-run font subsetter; see its docstring for when to rerun
└── CNAME                  # Custom domain config for GitHub Pages
```

## Fonts

Inter is subset by hand, not in a build step. After changing font weights, adding characters outside
Latin-1 / Latin Extended-A, or turning on OpenType features, run:

```
pip install fonttools brotli
python3 tools/build-fonts.py
```

and commit the files it writes. The script refuses CSS it can't account for.

## Features

- Light / dark mode with localStorage persistence
- Scroll-triggered reveal animations (off with reduced motion)
- Responsive layout down to mobile
- Sections: Experience, Projects, Skills, Certifications, References, Education, Contact
