with open('sw.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
m = re.search(r'const\s+SHELL_ASSETS\s*=\s*(\[[\s\S]*?\]);', text)
if m:
    assets = re.findall(r'[\'\"]([^\'\"]+)[\'\"]', m.group(1))
    cat_in_sw = [a for a in assets if 'exercise-catalog' in a]
    print('exercise-catalog in sw.js:', cat_in_sw)
    stretch_in_sw = [a for a in assets if 'stretch-catalog' in a]
    print('stretch-catalog in sw.js:', stretch_in_sw)
