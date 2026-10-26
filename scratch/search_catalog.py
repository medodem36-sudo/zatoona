import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('assets/data/exercise-catalog.js', 'r', encoding='utf-8') as f:
    cat_text = f.read()

json_match = re.search(r'(\[[\s\S]*\])', cat_text)
cat_data = json.loads(json_match.group(1))

keywords = ['crunch', 'lunge', 'squat', 'push', 'pull', 'goblet']
for kw in keywords:
    print(f'=== Keyword: {kw} ===')
    for ex in cat_data:
        if kw in ex['id'] or kw in ex['name'].lower():
            print(f"  {ex['id']} | {ex['name']} | {ex['nameAr']}")
