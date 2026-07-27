#!/usr/bin/env bash
# Run once: downloads the woff2 files Google Fonts serves to modern browsers
# and writes fonts.css pointing at local copies. Re-run to update.
set -euo pipefail
cd "$(dirname "$0")"

# Only the weights style.css actually uses: 400/500/600/700 mono, 400/600 sans. No italics.
URL='https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Inter:wght@400;600&display=swap'
UA='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

mkdir -p fonts
curl -sfL -A "$UA" "$URL" -o fonts/fonts.css

# ponytail: rewrite each remote URL to a local file named after its gstatic basename.
grep -o 'https://fonts\.gstatic\.com/[^)]*\.woff2' fonts/fonts.css | sort -u | while read -r u; do
  f=$(basename "$u")
  [ -f "fonts/$f" ] || curl -sfL -A "$UA" "$u" -o "fonts/$f"
  # BSD and GNU sed disagree on -i; this form works on both.
  sed "s#$u#$f#g" fonts/fonts.css > fonts/fonts.css.tmp && mv fonts/fonts.css.tmp fonts/fonts.css
done

n=$(ls -1 fonts/*.woff2 2>/dev/null | wc -l | tr -d ' ')
[ "$n" -gt 0 ] || { echo "FAIL: no woff2 downloaded"; exit 1; }
grep -q 'gstatic.com' fonts/fonts.css && { echo "FAIL: remote URLs remain in fonts.css"; exit 1; }
echo "OK: $n woff2 files in fonts/, fonts.css rewritten to local paths"
du -sh fonts
