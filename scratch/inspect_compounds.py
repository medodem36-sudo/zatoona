import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('assets/data/exercise-catalog.js', 'r', encoding='utf-8') as f:
    cat_text = f.read()

json_match = re.search(r'(\[[\s\S]*\])', cat_text)
catalog = json.loads(json_match.group(1))

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

reg_match = re.search(r'const\s+GYM_PLAN_TEMPLATE_REGISTRY\s*=\s*\{([\s\S]*?)\n\};', html)
tpl_cat_ids = set()
if reg_match:
    tpl_cat_ids = set(re.findall(r'catalogExerciseId:\s*[\'\"]([^\'\"]+)[\'\"]', reg_match.group(0)))

DIRECT_LEGACY_MAP = {
    'goblet_squat': 'assets/images/exercises/ex-a01-goblet-squat.svg',
    'barbell_bench_press': 'assets/images/exercises/ex-a02-bench-press.svg',
    'lat_pulldown_wide_grip': 'assets/images/exercises/ex-a03-lat-pulldown.svg',
    'standing_overhead_barbell_press': 'assets/images/exercises/ex-a04-overhead-press.svg',
    'plank': 'assets/images/exercises/ex-a05-plank.svg',
    'face_pull_cable': 'assets/images/exercises/ex-a06-face-pull.svg',
    'romanian_deadlift_barbell': 'assets/images/exercises/ex-b01-romanian-deadlift.svg',
    'barbell_bent_over_row': 'assets/images/exercises/ex-b02-barbell-row.svg',
    'push_up': 'assets/images/exercises/ex-b03-push-up.svg',
    'pull_up': 'assets/images/exercises/ex-b04-pull-up.svg',
    'walking_lunges_dumbbell': 'assets/images/exercises/ex-b06-lunges.svg',
}

compound_ex = [e for e in catalog if e.get('mechanic') == 'compound']
print(f'Total compound exercises in catalog: {len(compound_ex)}')

covered_compounds = [e for e in compound_ex if e['id'] in DIRECT_LEGACY_MAP]
print(f'Covered compound exercises (Category D): {len(covered_compounds)}')
for e in covered_compounds:
    print(f"  [D] {e['id']:32} | {e['equipment']:10} | {e['nameAr']}")

missing_compounds = [e for e in compound_ex if e['id'] not in DIRECT_LEGACY_MAP]
print(f'\nMissing / Uncovered compound exercises: {len(missing_compounds)}')

# Split into: in templates vs non-template
tpl_compounds = [e for e in missing_compounds if e['id'] in tpl_cat_ids]
non_tpl_compounds = [e for e in missing_compounds if e['id'] not in tpl_cat_ids]

print(f'\n--- In Preset Templates ({len(tpl_compounds)}) ---')
for e in tpl_compounds:
    print(f"  {e['id']:32} | {e['equipment']:10} | {e['nameAr']}")

print(f'\n--- Non-Template Compounds ({len(non_tpl_compounds)}) ---')
for e in non_tpl_compounds:
    print(f"  {e['id']:32} | {e['equipment']:10} | {e['nameAr']}")
