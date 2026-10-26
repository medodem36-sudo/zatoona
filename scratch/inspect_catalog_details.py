import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('assets/data/exercise-catalog.js', 'r', encoding='utf-8') as f:
    cat_text = f.read()

json_match = re.search(r'(\[[\s\S]*\])', cat_text)
cat_data = json.loads(json_match.group(1))

print(f"Total catalog exercises: {len(cat_data)}")

abs_ex = [e for e in cat_data if 'abs' in e.get('primaryMuscles', [])]
print(f"\nAbdominal exercises in catalog ({len(abs_ex)}):")
for e in abs_ex:
    print(f"  {e['id']:30} | {e['name']:35} | {e['equipment']}")

# Let's inspect all categories and primary muscles in catalog
categories = {}
muscles = {}
mechanics = {}
equipment = {}
for e in cat_data:
    cat = e.get('category', 'unknown')
    categories[cat] = categories.get(cat, 0) + 1
    mech = e.get('mechanic', 'unknown')
    mechanics[mech] = mechanics.get(mech, 0) + 1
    eq = e.get('equipment', 'unknown')
    equipment[eq] = equipment.get(eq, 0) + 1
    for m in e.get('primaryMuscles', []):
        muscles[m] = muscles.get(m, 0) + 1

print("\n--- Categories ---")
for k, v in sorted(categories.items()):
    print(f"  {k}: {v}")

print("\n--- Mechanics ---")
for k, v in sorted(mechanics.items()):
    print(f"  {k}: {v}")

print("\n--- Equipment ---")
for k, v in sorted(equipment.items()):
    print(f"  {k}: {v}")

print("\n--- Primary Muscles ---")
for k, v in sorted(muscles.items()):
    print(f"  {k}: {v}")
