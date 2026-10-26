import xml.etree.ElementTree as ET
import os

req_filenames = [
    'ex-barbell-back-squat.svg',
    'ex-conventional-deadlift.svg',
    'ex-incline-barbell-bench-press.svg',
    'ex-incline-dumbbell-press.svg',
    'ex-dumbbell-bench-press.svg',
    'ex-seated-cable-row.svg',
    'ex-leg-press.svg',
    'ex-seated-dumbbell-shoulder-press.svg',
    'ex-hanging-leg-raise.svg',
    'ex-standing-dumbbell-lateral-raise.svg',
    'ex-barbell-curl.svg',
    'ex-hammer-curl.svg',
    'ex-triceps-rope-pushdown.svg',
    'ex-skull-crushers.svg',
    'ex-dumbbell-chest-flyes.svg',
    'ex-lying-leg-curl-machine.svg',
    'ex-seated-leg-curl-machine.svg',
    'ex-standing-calf-raise-machine.svg',
    'ex-seated-palms-up-wrist-curl.svg'
]

for fname in req_filenames:
    path = os.path.join('assets/images/exercises', fname)
    tree = ET.parse(path)
    root = tree.getroot()
    assert root.tag.endswith('svg'), f"Not an svg tag: {root.tag}"
    vb = root.attrib.get('viewBox')
    assert vb == '0 0 300 200', f"Wrong viewBox {vb} in {fname}"

print(f"All {len(req_filenames)} SVG files parsed successfully as valid SVG XML with viewBox 0 0 300 200!")
