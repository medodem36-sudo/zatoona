import re

with open('assets/data/stretch-catalog.js', 'r', encoding='utf-8') as f:
    text = f.read()

imgs = re.findall(r'[\'\"](\.?/?assets/images/[^\'\"]+)[\'\"]', text)
print('Stretch catalog image samples:', imgs[:5])
