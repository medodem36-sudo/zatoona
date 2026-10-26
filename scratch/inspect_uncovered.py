import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('assets/data/exercise-catalog.js', 'r', encoding='utf-8') as f:
    catalog = json.loads(re.search(r'window\.ZATOONA_EXERCISE_CATALOG\s*=\s*(\[[\s\S]*?\]);', f.read()).group(1))

COVERED_IDS = {
    # 19 new
    'barbell_back_squat', 'conventional_deadlift', 'incline_barbell_bench_press',
    'incline_dumbbell_press', 'dumbbell_bench_press', 'seated_cable_row',
    'leg_press', 'seated_dumbbell_shoulder_press', 'hanging_leg_raise',
    'standing_dumbbell_lateral_raise', 'barbell_curl', 'hammer_curl',
    'triceps_rope_pushdown', 'skull_crushers', 'dumbbell_chest_flyes',
    'lying_leg_curl_machine', 'seated_leg_curl_machine', 'standing_calf_raise_machine',
    'seated_palms_up_wrist_curl',
    # 11 legacy
    'barbell_bench_press', 'barbell_bent_over_row', 'lat_pulldown_wide_grip',
    'standing_overhead_barbell_press', 'face_pull_cable', 'romanian_deadlift_barbell',
    'plank', 'goblet_squat', 'push_up', 'pull_up', 'walking_lunges_dumbbell'
}

uncovered = [e for e in catalog if e['id'] not in COVERED_IDS]
print(f"Total uncovered exercises: {len(uncovered)}")

uncovered_compounds = [e for e in uncovered if e.get('mechanic') == 'compound']
uncovered_isolation = [e for e in uncovered if e.get('mechanic') == 'isolation']

print(f"  - Compound uncovered: {len(uncovered_compounds)}")
print(f"  - Isolation uncovered: {len(uncovered_isolation)}")

print("\n--- Uncovered Compound Exercises (44 total) ---")
for idx, e in enumerate(uncovered_compounds, 1):
    print(f"{idx:2d}. {e['id']:32} | {e['equipment']:10} | {', '.join(e['primaryMuscles']):20} | {e.get('nameAr', e['name'])}")
