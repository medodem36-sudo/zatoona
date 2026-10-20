import xml.etree.ElementTree as ET

points = [
    {'iso': '2026-10-01', 'weight': 60, 'reps': 10},
    {'iso': '2026-10-05', 'weight': 62.5, 'reps': 10},
    {'iso': '2026-10-10', 'weight': 65, 'reps': 8},
    {'iso': '2026-10-15', 'weight': 67.5, 'reps': 8},
]

vals = [p['weight'] for p in points]
min_w = min(vals)
max_w = max(vals)
range_w = (max_w - min_w) or 1
w = 340
h = 120
pad_x = 28
pad_y = 18

svg_points = []
circles = []
labels = []
n = len(points)
step_x = (w - pad_x * 2) / (n - 1) if n > 1 else 0

for i, p in enumerate(points):
    x = pad_x + step_x * i
    y = pad_y + (h - pad_y * 2) * (1 - (p['weight'] - min_w) / range_w)
    svg_points.append(f'{x:.1f},{y:.1f}')
    circles.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="var(--accent)" stroke="var(--card)" stroke-width="1.5"><title>{p["iso"]}: {p["weight"]} kg</title></circle>')
    short_date = p['iso'][5:]
    labels.append(f'<text x="{x:.1f}" y="{h - 3}" font-size="9" text-anchor="middle" fill="var(--muted)">{short_date}</text>')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" style="width:100%; height:auto;">
  <polyline points="{' '.join(svg_points)}" fill="none" stroke="var(--accent)" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"/>
  {''.join(circles)}
  {''.join(labels)}
</svg>'''

root = ET.fromstring(svg)
print('SVG parsed successfully! Tag:', root.tag, 'Children:', len(root))
