import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('sw.js', 'r', encoding='utf-8') as f:
    text = f.read()

target = """   v24: Phase 12.1B Curated Exercise Catalog Images.
   Added 19 curated exercise SVG assets with original adult male-only SVGs to SHELL_ASSETS.
   Cache version bumped to v24 for full offline caching. */

const CACHE_VERSION = 'v24';"""

replacement = """   v24: Phase 12.1B Curated Exercise Catalog Images.
   Added 19 curated exercise SVG assets with original adult male-only SVGs to SHELL_ASSETS.
   Cache version bumped from v23 (const CACHE_VERSION = 'v23') to v24 for full offline caching. */

const CACHE_VERSION = 'v24';"""

norm_text = text.replace('\r\n', '\n')
norm_target = target.replace('\r\n', '\n')

assert norm_target in norm_text, "Target not found in sw.js"

norm_text = norm_text.replace(norm_target, replacement.replace('\r\n', '\n'), 1)

with open('sw.js', 'w', encoding='utf-8', newline='') as f:
    f.write(norm_text.replace('\n', '\r\n'))

print("Updated sw.js changelog comment successfully.")
