# -*- coding: utf-8 -*-
import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

REPO = r"C:\Users\Lenovo\Documents\GitHub\zatoona"

with open(os.path.join(REPO, "sw.js"), "r", encoding="utf-8") as f:
    text = f.read()

m = re.search(r"const SHELL_ASSETS = \[(.*?)\];", text, re.DOTALL)
if not m:
    print("SHELL_ASSETS not found!")
    sys.exit(1)

paths = re.findall(r"'([^']+)'", m.group(1))
print(f"SHELL_ASSETS count: {len(paths)}")

missing = []
for p in paths:
    disk = os.path.join(REPO, p.replace("./", ""))
    if not os.path.exists(disk):
        missing.append(p)
        print(f"  MISSING: {p}")
print(f"Missing files: {len(missing)} of {len(paths)}")

warmup = [p for p in paths if "warmup" in p]
cooldown = [p for p in paths if "cooldown" in p]
exercises = [p for p in paths if "exercises" in p]
stretches = [p for p in paths if "stretches" in p]
fonts = [p for p in paths if "fonts" in p]
icons = [p for p in paths if "icons" in p or "favicon" in p]
data = [p for p in paths if "data" in p]
print(f"Warmup SVGs: {len(warmup)}")
print(f"Cooldown SVGs: {len(cooldown)}")
print(f"Exercise SVGs: {len(exercises)}")
print(f"Stretch SVGs: {len(stretches)}")
print(f"Font files: {len(fonts)}")
print(f"Icon files: {len(icons)}")
print(f"Data files: {len(data)}")
print(f"Other: {len(paths) - len(warmup) - len(cooldown) - len(exercises) - len(stretches) - len(fonts) - len(icons) - len(data)}")

# Check duplicates
dups = [p for p in paths if paths.count(p) > 1]
if dups:
    print(f"DUPLICATES: {set(dups)}")
else:
    print("No duplicates in SHELL_ASSETS.")
