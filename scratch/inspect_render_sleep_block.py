# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'index.html', 'r', encoding='utf-8') as f:
    text = f.read()

p5_start = text.find('function renderSleepSummary(){')
p5_end = text.find('/* ================= RENDER: PRAYER VIEW ================= */')
print(f"Point 5 (Sleep Render Functions): {p5_start} to {p5_end}")
print(text[p5_start:p5_end])
