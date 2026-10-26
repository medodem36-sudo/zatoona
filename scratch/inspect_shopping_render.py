import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Let's search for renderShopping or renderMeal or other checklists
funcs = ['renderShopping', 'renderWarmup', 'renderCooldown']

for fn in funcs:
    m = re.search(rf'function\s+{fn}\s*\([^{{]*\{{', content)
    if m:
        start = m.start()
        print(f"\n=== {fn} ===")
        print(content[start:start+1000])
