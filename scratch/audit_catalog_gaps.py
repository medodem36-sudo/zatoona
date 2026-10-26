# -*- coding: utf-8 -*-
import os, sys, json, re

sys.stdout.reconfigure(encoding='utf-8')
REPO = r"C:\Users\Lenovo\Documents\GitHub\zatoona"

# 1. Load exercise-catalog.js
cat_file = os.path.join(REPO, "assets", "data", "exercise-catalog.js")
with open(cat_file, "r", encoding="utf-8") as f:
    cat_text = f.read()

idx1 = cat_text.find('[')
idx2 = cat_text.rfind(']') + 1
catalog = json.loads(cat_text[idx1:idx2])
print(f"Loaded catalog exercises: {len(catalog)}")

# 2. Load index.html templates and classic exercises
html_file = os.path.join(REPO, "index.html")
with open(html_file, "r", encoding="utf-8") as f:
    html_text = f.read()

# Extract EX_A_DEFAULTS and EX_B_DEFAULTS
m_a = re.search(r"const EX_A_DEFAULTS = \[(.*?)\];\s*const EX_B_DEFAULTS = \[(.*?)\];", html_text, re.DOTALL)
legacy_defaults = {}
if m_a:
    for block in [m_a.group(1), m_a.group(2)]:
        entries = re.findall(r"\{\s*key:\s*'([^']+)',\s*name:\s*'([^']+)'(?:.*?)img:\s*'([^']+)'(?:.*?)credit:\s*'([^']+)'", block, re.DOTALL)
        for k, name, img, cr in entries:
            legacy_defaults[k] = {"name": name, "img": img, "credit": cr}

print(f"Legacy classic defaults count: {len(legacy_defaults)}")
for k, v in legacy_defaults.items():
    print(f"  {k:12s} -> {v['img']}")

# Extract templates from GYM_PLAN_TEMPLATE_REGISTRY
# Extract each template and routine
m_tpl = re.search(r"const GYM_PLAN_TEMPLATE_REGISTRY = (\{.*?\n\};)", html_text, re.DOTALL)
template_exercises = []
if m_tpl:
    tpl_text = m_tpl.group(1)
    ex_matches = re.findall(r"\{\s*templateExerciseId:\s*'([^']+)',\s*name:\s*'([^']+)',\s*catalogExerciseId:\s*'([^']+)'", tpl_text)
    for tid, tname, cid in ex_matches:
        template_exercises.append({"templateExerciseId": tid, "name": tname, "catalogExerciseId": cid})

print(f"\nTotal template exercise entries: {len(template_exercises)}")
unique_template_cat_ids = sorted(list(set(e["catalogExerciseId"] for e in template_exercises)))
print(f"Unique catalog exercise IDs used in templates: {len(unique_template_cat_ids)}")
print("IDs used in templates:")
for cid in unique_template_cat_ids:
    print(f"  - {cid}")
