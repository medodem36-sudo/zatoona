import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('sw.js', 'r', encoding='utf-8') as f:
    sw_text = f.read()

# 1. Update version comment and CACHE_VERSION
old_ver_pattern = """   fully replacing external unverified/female exercise images with original male-only SVGs.
   Cache version bumped to v22 for full offline caching. */

const CACHE_VERSION = 'v23';"""

new_ver_pattern = """   fully replacing external unverified/female exercise images with original male-only SVGs.
   Cache version bumped to v22 for full offline caching.

   v24: Phase 12.1B Curated Exercise Catalog Images.
   Added 19 curated exercise SVG assets with original adult male-only SVGs to SHELL_ASSETS.
   Cache version bumped to v24 for full offline caching. */

const CACHE_VERSION = 'v24';"""

norm_sw = sw_text.replace('\r\n', '\n')
norm_old_ver = old_ver_pattern.replace('\r\n', '\n')

assert norm_old_ver in norm_sw, "old_ver_pattern not found in sw.js"

norm_sw = norm_sw.replace(norm_old_ver, new_ver_pattern.replace('\r\n', '\n'), 1)

# 2. Add 19 new SVGs to SHELL_ASSETS
# Let's locate './assets/images/exercises/ex-b06-lunges.svg'
target_asset = "'./assets/images/exercises/ex-b06-lunges.svg',"

new_assets = """'./assets/images/exercises/ex-b06-lunges.svg',
  './assets/images/exercises/ex-barbell-back-squat.svg',
  './assets/images/exercises/ex-conventional-deadlift.svg',
  './assets/images/exercises/ex-incline-barbell-bench-press.svg',
  './assets/images/exercises/ex-incline-dumbbell-press.svg',
  './assets/images/exercises/ex-dumbbell-bench-press.svg',
  './assets/images/exercises/ex-seated-cable-row.svg',
  './assets/images/exercises/ex-leg-press.svg',
  './assets/images/exercises/ex-seated-dumbbell-shoulder-press.svg',
  './assets/images/exercises/ex-hanging-leg-raise.svg',
  './assets/images/exercises/ex-standing-dumbbell-lateral-raise.svg',
  './assets/images/exercises/ex-barbell-curl.svg',
  './assets/images/exercises/ex-hammer-curl.svg',
  './assets/images/exercises/ex-triceps-rope-pushdown.svg',
  './assets/images/exercises/ex-skull-crushers.svg',
  './assets/images/exercises/ex-dumbbell-chest-flyes.svg',
  './assets/images/exercises/ex-lying-leg-curl-machine.svg',
  './assets/images/exercises/ex-seated-leg-curl-machine.svg',
  './assets/images/exercises/ex-standing-calf-raise-machine.svg',
  './assets/images/exercises/ex-seated-palms-up-wrist-curl.svg',"""

assert target_asset in norm_sw, f"{target_asset} not found in sw.js"

norm_sw = norm_sw.replace(target_asset, new_assets, 1)

# Restore CRLF
final_sw = norm_sw.replace('\n', '\r\n')

with open('sw.js', 'w', encoding='utf-8', newline='') as f:
    f.write(final_sw)

print("Updated sw.js successfully.")
