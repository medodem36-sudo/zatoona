import sys, re

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'const\s+EX_A_DEFAULTS\s*=\s*\[(.*?)\];', text, re.DOTALL)
if m:
    keys = re.findall(r'key:\s*["\']([^"\']+)["\']', m.group(1))
    print('EX_A_DEFAULTS keys:', len(keys), keys)

m2 = re.search(r'const\s+EX_B_DEFAULTS\s*=\s*\[(.*?)\];', text, re.DOTALL)
if m2:
    keys2 = re.findall(r'key:\s*["\']([^"\']+)["\']', m2.group(1))
    print('EX_B_DEFAULTS keys:', len(keys2), keys2)

# Check templates
tpl_m = re.search(r'const\s+GYM_PLAN_TEMPLATE_REGISTRY\s*=\s*(\{.*?\n\};)', text, re.DOTALL)
if tpl_m:
    tpl_keys = re.findall(r'id:\s*["\']([^"\']+)["\']', tpl_m.group(1))
    print('Template registry templates:', len(tpl_keys), tpl_keys)
