# -*- coding: utf-8 -*-
import sys, re, os

sys.stdout.reconfigure(encoding='utf-8')

repo = r"C:\Users\Lenovo\Documents\GitHub\zatoona"
with open(os.path.join(repo, "index.html"), "r", encoding="utf-8") as f:
    text = f.read()

# search for all occurrences of EX_A and EX_B
matches = re.finditer(r'\b(EX_A|EX_B)\b', text)
for m in matches:
    idx = m.start()
    line_no = text[:idx].count('\n') + 1
    line = text.split('\n')[line_no - 1]
    print(f"Line {line_no}: {line.strip()[:100]}")
