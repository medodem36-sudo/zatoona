# -*- coding: utf-8 -*-
import sys, re, os

sys.stdout.reconfigure(encoding='utf-8')

repo = r"C:\Users\Lenovo\Documents\GitHub\zatoona"
cat_path = os.path.join(repo, "assets", "data", "exercise-catalog.js")
with open(cat_path, "r", encoding="utf-8") as f:
    cat_text = f.read()

print("exercise-catalog.js size:", len(cat_text))
print("First 500 chars:\n", cat_text[:500])
