# -*- coding: utf-8 -*-
import sys, re, os

sys.stdout.reconfigure(encoding='utf-8')

repo = r"C:\Users\Lenovo\Documents\GitHub\zatoona"
with open(os.path.join(repo, "index.html"), "r", encoding="utf-8") as f:
    text = f.read()

for arr_name in ['EX_A_DEFAULTS', 'EX_B_DEFAULTS']:
    idx = text.find(f"const {arr_name}")
    line_no = text[:idx].count('\n') + 1
    end_idx = text.find('];', idx)
    block = text[idx:end_idx+2]
    print(f"\n=======================================================")
    print(f"=== {arr_name} (starts at line {line_no}) ===")
    print(f"=======================================================")
    
    # Split items by object delimiter
    # each item starts with { key: '...'
    items = re.split(r'\n\s*\{\s*key:\s*', block)
    for it in items[1:]:
        lines = it.split('\n')
        # extract key
        m_key = re.match(r"['\"]([^'\"]+)['\"]", it)
        key = m_key.group(1) if m_key else 'UNKNOWN'
        
        m_name = re.search(r"name:\s*['\"]([^'\"]+)['\"]", it)
        name = m_name.group(1) if m_name else 'UNKNOWN'
        
        m_img = re.search(r"img:\s*['\"]([^'\"]+)['\"]", it)
        img = m_img.group(1) if m_img else None
        
        m_credit = re.search(r"credit:\s*['\"]([^'\"]+)['\"]", it)
        credit = m_credit.group(1) if m_credit else None
        
        m_target = re.search(r"target:\s*['\"]([^'\"]+)['\"]", it)
        target = m_target.group(1) if m_target else ''

        m_opt = re.search(r"optional:\s*true", it)
        optional = bool(m_opt)
        
        print(f"\nExercise Key: '{key}' | Name: {name} | Optional: {optional}")
        print(f"  Target: {target}")
        print(f"  Image: {img}")
        print(f"  Credit: {credit}")
