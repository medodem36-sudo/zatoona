# -*- coding: utf-8 -*-
import os, sys, json, re

sys.stdout.reconfigure(encoding='utf-8')
REPO = r"C:\Users\Lenovo\Documents\GitHub\zatoona"

# Load exercise catalog
cat_file = os.path.join(REPO, "assets", "data", "exercise-catalog.js")
with open(cat_file, "r", encoding="utf-8") as f:
    cat_text = f.read()

idx1 = cat_text.find('[')
idx2 = cat_text.rfind(']') + 1
catalog = json.loads(cat_text[idx1:idx2])

# Load index.html
html_file = os.path.join(REPO, "index.html")
with open(html_file, "r", encoding="utf-8") as f:
    html_text = f.read()

# Catalog IDs used in templates
template_cat_ids = set(re.findall(r"catalogExerciseId:\s*['\"]([^'\"]+)['\"]", html_text))

# Existing SVGs on disk in assets/images/exercises/
ex_svg_dir = os.path.join(REPO, "assets", "images", "exercises")
existing_svgs = os.listdir(ex_svg_dir) if os.path.exists(ex_svg_dir) else []
print(f"Existing exercise SVGs on disk ({len(existing_svgs)}): {existing_svgs}")

# Check exact mapping to 12 legacy defaults
# Legacy defaults in EX_A_DEFAULTS and EX_B_DEFAULTS:
# squat, bench, pulldown, press, plank, facepull, rdl, row, pushup, pullup, crunch, lunge
legacy_keys = {
    'squat': 'assets/images/exercises/ex-a01-goblet-squat.svg',
    'bench': 'assets/images/exercises/ex-a02-bench-press.svg',
    'pulldown': 'assets/images/exercises/ex-a03-lat-pulldown.svg',
    'press': 'assets/images/exercises/ex-a04-overhead-press.svg',
    'plank': 'assets/images/exercises/ex-a05-plank.svg',
    'facepull': 'assets/images/exercises/ex-a06-face-pull.svg',
    'rdl': 'assets/images/exercises/ex-b01-romanian-deadlift.svg',
    'row': 'assets/images/exercises/ex-b02-barbell-row.svg',
    'pushup': 'assets/images/exercises/ex-b03-push-up.svg',
    'pullup': 'assets/images/exercises/ex-b04-pull-up.svg',
    'crunch': 'assets/images/exercises/ex-b05-abdominal-crunch.svg',
    'lunge': 'assets/images/exercises/ex-b06-lunges.svg'
}

# In catalog, does any exercise currently have images: [] populated?
cat_with_img = [e for e in catalog if e.get('images') and len(e['images']) > 0]
print(f"Catalog items with non-empty 'images' array: {len(cat_with_img)}")

# Analyze all 119 exercises
compounds = [e for e in catalog if e.get('mechanic') == 'compound']
isolations = [e for e in catalog if e.get('mechanic') == 'isolation']
print(f"Catalog mechanics: {len(compounds)} compound, {len(isolations)} isolation, total: {len(catalog)}")

# Find which template exercises are compound vs isolation
tpl_compounds = [e for e in catalog if e['id'] in template_cat_ids and e.get('mechanic') == 'compound']
tpl_isolations = [e for e in catalog if e['id'] in template_cat_ids and e.get('mechanic') == 'isolation']
print(f"Template exercises: {len(tpl_compounds)} compound, {len(tpl_isolations)} isolation (total {len(template_cat_ids)})")

# Map of potential direct matches with 12 existing SVGs:
# e.g.:
# 'barbell_bench_press' -> ex-a02-bench-press.svg
# 'plank' -> ex-a05-plank.svg
# 'pull_up' -> ex-b04-pull-up.svg
# 'push_up' -> ex-b03-push-up.svg
# 'crunch' -> ex-b05-abdominal-crunch.svg
# 'lat_pulldown_wide_grip' -> ex-a03-lat-pulldown.svg
# 'barbell_bent_over_row' -> ex-b02-barbell-row.svg
# 'face_pull_cable' -> ex-a06-face-pull.svg
# 'romanian_deadlift_barbell' -> ex-b01-romanian-deadlift.svg
# 'dumbbell_goblet_squat' -> ex-a01-goblet-squat.svg
# 'standing_overhead_barbell_press' -> ex-a04-overhead-press.svg (or dumbbell press)
# 'walking_lunge' / 'dumbbell_lunge' -> ex-b06-lunges.svg

print("\n--- Catalog IDs in Templates (26) ---")
for e in catalog:
    if e['id'] in template_cat_ids:
        print(f"ID: {e['id']:32s} | Mech: {e.get('mechanic',''):9s} | Equip: {e.get('equipment',''):10s} | {e['nameAr']} ({e['name']})")
