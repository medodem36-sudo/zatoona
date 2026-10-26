import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('assets/data/exercise-catalog.js', 'r', encoding='utf-8') as f:
    cat = json.loads(re.search(r'(\[[\s\S]*\])', f.read()).group(1))

cat_dict = {e['id']: e for e in cat}

req_19 = [
    'barbell_back_squat',
    'conventional_deadlift',
    'incline_barbell_bench_press',
    'incline_dumbbell_press',
    'dumbbell_bench_press',
    'seated_cable_row',
    'leg_press',
    'seated_dumbbell_shoulder_press',
    'hanging_leg_raise',
    'standing_dumbbell_lateral_raise',
    'barbell_curl',
    'hammer_curl',
    'triceps_rope_pushdown',
    'skull_crushers',
    'dumbbell_chest_flyes',
    'lying_leg_curl_machine',
    'seated_leg_curl_machine',
    'standing_calf_raise_machine',
    'seated_palms_up_wrist_curl'
]

print(f"Checking {len(req_19)} requested exercises against exercise-catalog.js:")
all_found = True
for idx, eid in enumerate(req_19, 1):
    ex = cat_dict.get(eid)
    if ex:
        print(f"{idx:2d}. [FOUND] {eid:32} | {ex.get('mechanic','?'):10} | {ex.get('equipment','?'):10} | {ex.get('nameAr', ex.get('name'))}")
    else:
        print(f"{idx:2d}. [MISSING] {eid}")
        all_found = False

print(f"\nAll 19 found in catalog: {all_found}")
