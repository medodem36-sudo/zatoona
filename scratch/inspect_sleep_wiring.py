# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find("document.getElementById('sleepTimeStart').addEventListener")
print(f"Wiring sleepTimeStart found at: {idx}")
print(text[idx-100:idx+350])
