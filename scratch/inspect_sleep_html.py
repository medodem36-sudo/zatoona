# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# Find view-sleep or sleep section
m = re.search(r'(<div[^>]*id="view-sleep"[^>]*>[\s\S]*?)(<div[^>]*id="view-|\n  <!-- )', text)
if m:
    print("Found view-sleep:")
    print(m.group(1)[:2500])
else:
    # search for sleepTimeStart
    idx = text.find('sleepTimeStart')
    print("Around sleepTimeStart:")
    print(text[max(0, idx-500):idx+1500])
