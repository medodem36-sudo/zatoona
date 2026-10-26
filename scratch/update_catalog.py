import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

CATALOG_PATH = 'assets/data/exercise-catalog.js'

with open(CATALOG_PATH, 'r', encoding='utf-8') as f:
    original_text = f.read()

# Extract header before the array
header_match = re.search(r'([\s\S]*?window\.ZATOONA_EXERCISE_CATALOG\s*=\s*)(\[[\s\S]*?\]);?\s*$', original_text)
if not header_match:
    raise ValueError("Could not find window.ZATOONA_EXERCISE_CATALOG in file")

header = header_match.group(1)
catalog_json_str = header_match.group(2)
catalog = json.loads(catalog_json_str)

print(f"Loaded {len(catalog)} exercises.")

# Map of images to assign
EXERCISE_IMAGES_MAP = {
    # 19 New SVGs created in Phase 12.1B
    'barbell_back_squat': './assets/images/exercises/ex-barbell-back-squat.svg',
    'conventional_deadlift': './assets/images/exercises/ex-conventional-deadlift.svg',
    'incline_barbell_bench_press': './assets/images/exercises/ex-incline-barbell-bench-press.svg',
    'incline_dumbbell_press': './assets/images/exercises/ex-incline-dumbbell-press.svg',
    'dumbbell_bench_press': './assets/images/exercises/ex-dumbbell-bench-press.svg',
    'seated_cable_row': './assets/images/exercises/ex-seated-cable-row.svg',
    'leg_press': './assets/images/exercises/ex-leg-press.svg',
    'seated_dumbbell_shoulder_press': './assets/images/exercises/ex-seated-dumbbell-shoulder-press.svg',
    'hanging_leg_raise': './assets/images/exercises/ex-hanging-leg-raise.svg',
    'standing_dumbbell_lateral_raise': './assets/images/exercises/ex-standing-dumbbell-lateral-raise.svg',
    'barbell_curl': './assets/images/exercises/ex-barbell-curl.svg',
    'hammer_curl': './assets/images/exercises/ex-hammer-curl.svg',
    'triceps_rope_pushdown': './assets/images/exercises/ex-triceps-rope-pushdown.svg',
    'skull_crushers': './assets/images/exercises/ex-skull-crushers.svg',
    'dumbbell_chest_flyes': './assets/images/exercises/ex-dumbbell-chest-flyes.svg',
    'lying_leg_curl_machine': './assets/images/exercises/ex-lying-leg-curl-machine.svg',
    'seated_leg_curl_machine': './assets/images/exercises/ex-seated-leg-curl-machine.svg',
    'standing_calf_raise_machine': './assets/images/exercises/ex-standing-calf-raise-machine.svg',
    'seated_palms_up_wrist_curl': './assets/images/exercises/ex-seated-palms-up-wrist-curl.svg',
    
    # 11 Legacy SVGs directly matching catalog exercises
    'barbell_bench_press': './assets/images/exercises/ex-a02-bench-press.svg',
    'barbell_bent_over_row': './assets/images/exercises/ex-b02-barbell-row.svg',
    'lat_pulldown_wide_grip': './assets/images/exercises/ex-a03-lat-pulldown.svg',
    'standing_overhead_barbell_press': './assets/images/exercises/ex-a04-overhead-press.svg',
    'face_pull_cable': './assets/images/exercises/ex-a06-face-pull.svg',
    'romanian_deadlift_barbell': './assets/images/exercises/ex-b01-romanian-deadlift.svg',
    'plank': './assets/images/exercises/ex-a05-plank.svg',
    'goblet_squat': './assets/images/exercises/ex-a01-goblet-squat.svg',
    'push_up': './assets/images/exercises/ex-b03-push-up.svg',
    'pull_up': './assets/images/exercises/ex-b04-pull-up.svg',
    'walking_lunges_dumbbell': './assets/images/exercises/ex-b06-lunges.svg',
}

updated_count = 0
for ex in catalog:
    eid = ex.get('id')
    if eid in EXERCISE_IMAGES_MAP:
        ex['images'] = [EXERCISE_IMAGES_MAP[eid]]
        updated_count += 1

print(f"Updated images for {updated_count} exercises out of {len(catalog)}.")
assert updated_count == len(EXERCISE_IMAGES_MAP), f"Expected {len(EXERCISE_IMAGES_MAP)} updates, got {updated_count}"

# Update header comment
new_header = """/**
 * Zatoona Local Exercise Catalog
 * Source: free-exercise-db / Everkinetic (Public Domain - The Unlicense)
 * Curated offline-first original SVG illustrations added in Phase 12.1B adhering to strict Males-Only policy.
 * Standalone offline asset, compatible with file:/// and PWA caching.
 */
window.ZATOONA_EXERCISE_CATALOG = """

new_content = new_header + json.dumps(catalog, ensure_ascii=False, indent=2) + ";\n"

with open(CATALOG_PATH, 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"Successfully wrote updated catalog to {CATALOG_PATH} ({len(new_content)} bytes).")
