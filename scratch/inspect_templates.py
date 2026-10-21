import re, sys
sys.stdout.reconfigure(encoding="utf-8")
with open("index.html", "r", encoding="utf-8") as f:
    text = f.read()

# Find templates
for m in re.finditer(r"(\w+):\s*\{\s*id:\s*['\"](\w+)['\"]\s*,\s*name:\s*['\"]([^'\"]+)['\"]", text):
    if m.group(1) == m.group(2):
        print(f"Template: {m.group(1)} - {m.group(3)}")

for m in re.finditer(r"id:\s*['\"]([a-zA-Z0-9_]+)['\"]\s*,\s*name:\s*['\"]([^'\"]+)['\"]\s*,\s*desc:\s*['\"]([^'\"]+)['\"]", text):
    rid = m.group(1)
    if any(k in rid for k in ["fb_", "ppl_", "ul_", "bro_"]):
        print(f"   Routine: {rid:15s} | {m.group(2):20s} | {m.group(3)}")
