import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('assets/data/exercise-catalog.js', 'r', encoding='utf-8') as f:
    cat_text = f.read()

json_match = re.search(r'(\[[\s\S]*\])', cat_text)
catalog = json.loads(json_match.group(1))

# Template registry exercises
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

reg_match = re.search(r'const\s+GYM_PLAN_TEMPLATE_REGISTRY\s*=\s*\{([\s\S]*?)\n\};', html)
tpl_cat_ids = set()
if reg_match:
    tpl_cat_ids = set(re.findall(r'catalogExerciseId:\s*[\'\"]([^\'\"]+)[\'\"]', reg_match.group(0)))

print(f'Total catalog: {len(catalog)}')
print(f'Template unique catalog IDs: {len(tpl_cat_ids)}')

# Direct legacy matches (100% exact match between movement and SVG)
# ex-a01: dumbbell goblet squat -> goblet_squat
# ex-a02: barbell bench press -> barbell_bench_press
# ex-a03: lat pulldown wide grip -> lat_pulldown_wide_grip
# ex-a04: standing barbell overhead press -> standing_overhead_barbell_press
# ex-a05: front plank -> plank
# ex-a06: face pull cable -> face_pull_cable
# ex-b01: barbell romanian deadlift -> romanian_deadlift_barbell
# ex-b02: barbell bent-over row -> barbell_bent_over_row
# ex-b03: standard push-up -> push_up
# ex-b04: pull-up -> pull_up
# ex-b06: dumbbell lunges -> walking_lunges_dumbbell
# ex-b05: abdominal crunch -> no exact catalog entry (catalog has no floor crunch; only cable_kneeling_crunch & bicycle_crunch)

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

# Potential reuse candidates (Needs Review: category E)
# - kettlebell_goblet_squat could use ex-a01 (dumbbell vs kettlebell)
# - seated_dumbbell_shoulder_press vs standing_overhead_barbell_press (dumbbell seated vs barbell standing)
# - chin_up vs pull_up (underhand vs overhand)
# - diamond_push_up vs push_up
# - decline_push_up / incline_push_up vs push_up
POTENTIAL_REVIEW_MAP = {
    'kettlebell_goblet_squat': ('ex-a01-goblet-squat.svg', 'Kettlebell vs Dumbbell goblet squat'),
    'seated_dumbbell_shoulder_press': ('ex-a04-overhead-press.svg', 'Seated Dumbbell vs Standing Barbell Press'),
    'chin_up': ('ex-b04-pull-up.svg', 'Supinated grip vs Pronated grip pull-up'),
    'diamond_push_up': ('ex-b03-push-up.svg', 'Diamond grip vs standard push-up'),
    'decline_push_up': ('ex-b03-push-up.svg', 'Feet elevated push-up variation'),
    'incline_push_up': ('ex-b03-push-up.svg', 'Hands elevated push-up variation'),
    'lat_pulldown_close_grip': ('ex-a03-lat-pulldown.svg', 'Close grip vs wide grip lat pulldown'),
    'single_arm_cable_lat_pulldown': ('ex-a03-lat-pulldown.svg', 'Unilateral cable vs bilateral lat pulldown'),
}

classified = []
counts = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0}

for ex in catalog:
    eid = ex['id']
    is_tpl = eid in tpl_cat_ids
    mech = ex.get('mechanic', 'other')
    
    if eid in DIRECT_LEGACY_MAP:
        cat_class = 'D'
        note = f'Covered by existing local SVG: {DIRECT_LEGACY_MAP[eid]}'
    elif eid in POTENTIAL_REVIEW_MAP:
        cat_class = 'E'
        note = f'Partial visual match with {POTENTIAL_REVIEW_MAP[eid][0]} ({POTENTIAL_REVIEW_MAP[eid][1]}), needs review if reuse is acceptable'
    else:
        cat_class = 'A'
        note = 'Missing: No local SVG and empty images array in catalog'
        
    counts[cat_class] += 1
    classified.append({
        'id': eid,
        'name': ex['name'],
        'nameAr': ex['nameAr'],
        'mechanic': mech,
        'equipment': ex.get('equipment', ''),
        'primaryMuscles': ex.get('primaryMuscles', []),
        'category': cat_class,
        'in_template': is_tpl,
        'note': note
    })

print('\nClassification Totals:')
for k, v in sorted(counts.items()):
    print(f'  Category {k}: {v}')

print('\n--- Breakdown by In-Template vs Out-of-Template ---')
for cat_class in ['D', 'E', 'A']:
    tpl_count = sum(1 for c in classified if c['category'] == cat_class and c['in_template'])
    non_tpl_count = sum(1 for c in classified if c['category'] == cat_class and not c['in_template'])
    print(f'  Category {cat_class}: {tpl_count} in templates, {non_tpl_count} non-template (Total {tpl_count+non_tpl_count})')

print('\n--- Template Exercises Details (26) ---')
for c in classified:
    if c['in_template']:
        print(f"[{c['category']}] {c['id']:35} | {c['mechanic']:10} | {c['equipment']:10} | {c['nameAr']}")
