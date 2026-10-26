# -*- coding: utf-8 -*-
import os, sys, json, re

sys.stdout.reconfigure(encoding='utf-8')
REPO = r"C:\Users\Lenovo\Documents\GitHub\zatoona"

html_file = os.path.join(REPO, "index.html")
with open(html_file, "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find("const GYM_PLAN_TEMPLATE_REGISTRY")
snippet = text[idx:idx+4000]
print("Snippet from GYM_PLAN_TEMPLATE_REGISTRY:")
print(snippet[:1500])

# Find all catalogExerciseId in the entire HTML file
all_cat_ids = re.findall(r"catalogExerciseId:\s*['\"]([^'\"]+)['\"]", text)
print(f"\nAll catalogExerciseId occurrences in index.html: {len(all_cat_ids)}")
print("Unique catalogExerciseId referenced in index.html:")
for u in sorted(set(all_cat_ids)):
    print(f"  - {u}")
