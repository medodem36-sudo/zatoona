# -*- coding: utf-8 -*-
import sys, re, os

sys.stdout.reconfigure(encoding='utf-8')

repo = r"C:\Users\Lenovo\Documents\GitHub\zatoona"
with open(os.path.join(repo, "index.html"), "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find('exercise-catalog.js')
print("exercise-catalog.js script tag in index.html:")
print(text[idx-50:idx+100])
