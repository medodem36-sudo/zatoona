# -*- coding: utf-8 -*-
import sys, json, os

sys.stdout.reconfigure(encoding='utf-8')

repo = r"C:\Users\Lenovo\Documents\GitHub\zatoona"
cat_path = os.path.join(repo, "assets", "data", "exercise-catalog.js")
with open(cat_path, "r", encoding="utf-8") as f:
    text = f.read()

# strip JS prefix
json_str = text[text.find('['):text.rfind(']')+1]
catalog = json.loads(json_str)

muscles = set()
sec_muscles = set()
equipment = set()
categories = set()

for ex in catalog:
    for m in ex.get('primaryMuscles', []):
        muscles.add(m)
    for m in ex.get('secondaryMuscles', []):
        sec_muscles.add(m)
    if ex.get('equipment'):
        equipment.add(ex.get('equipment'))
    if ex.get('category'):
        categories.add(ex.get('category'))

print("Primary muscles:", sorted(list(muscles)))
print("Secondary muscles:", sorted(list(sec_muscles)))
print("Equipment:", sorted(list(equipment)))
print("Categories:", sorted(list(categories)))
print("Total exercises:", len(catalog))
