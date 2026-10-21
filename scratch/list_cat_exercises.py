# -*- coding: utf-8 -*-
import json, re, sys

sys.stdout.reconfigure(encoding='utf-8')

with open('assets/data/exercise-catalog.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Match the array
m = re.search(r'window\.ZATOONA_EXERCISE_CATALOG\s*=\s*(\[.*?\]);', text, re.DOTALL)
if m:
    catalog = json.loads(m.group(1))
    print(f"Total exercises in catalog: {len(catalog)}")
    for ex in catalog:
        print(f"id: {ex['id']} | name: {ex['name']} | muscles: {ex.get('primaryMuscles', [])}")
