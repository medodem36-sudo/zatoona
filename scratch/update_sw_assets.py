# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('sw.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Insert 34 stretch SVG paths before ];
NEW_ASSETS = """  './assets/images/stretches/str-doorway-pec-stretch.svg',
  './assets/images/stretches/str-arm-circles-dynamic.svg',
  './assets/images/stretches/str-cross-body-shoulder-stretch.svg',
  './assets/images/stretches/str-band-shoulder-dislocations.svg',
  './assets/images/stretches/str-lat-wall-stretch.svg',
  './assets/images/stretches/str-childs-pose.svg',
  './assets/images/stretches/str-band-pull-apart-activation.svg',
  './assets/images/stretches/str-upper-trap-stretch.svg',
  './assets/images/stretches/str-chin-tucks.svg',
  './assets/images/stretches/str-levator-scapulae-stretch.svg',
  './assets/images/stretches/str-kneeling-hip-flexor.svg',
  './assets/images/stretches/str-hip-opener-90-90.svg',
  './assets/images/stretches/str-butterfly-stretch.svg',
  './assets/images/stretches/str-standing-quad-stretch.svg',
  './assets/images/stretches/str-standing-hamstring-stretch.svg',
  './assets/images/stretches/str-dynamic-leg-swings.svg',
  './assets/images/stretches/str-couch-stretch.svg',
  './assets/images/stretches/str-pigeon-pose.svg',
  './assets/images/stretches/str-figure-four-stretch.svg',
  './assets/images/stretches/str-glute-bridge-activation.svg',
  './assets/images/stretches/str-wall-calf-stretch.svg',
  './assets/images/stretches/str-ankle-wall-mobilization.svg',
  './assets/images/stretches/str-soleus-bent-knee-stretch.svg',
  './assets/images/stretches/str-wrist-extensor-stretch.svg',
  './assets/images/stretches/str-wrist-flexor-prayer.svg',
  './assets/images/stretches/str-quadruped-wrist-circles.svg',
  './assets/images/stretches/str-cat-cow-mobility.svg',
  './assets/images/stretches/str-thoracic-spine-rotations.svg',
  './assets/images/stretches/str-bird-dog-activation.svg',
  './assets/images/stretches/str-cobra-lumbar-stretch.svg',
  './assets/images/stretches/str-worlds-greatest-stretch.svg',
  './assets/images/stretches/str-deep-squat-pry.svg',
  './assets/images/stretches/str-downward-dog.svg',
  './assets/images/stretches/str-inchworm-walkout.svg',
"""

old = "  './assets/images/exercises/ex-b06-lunges.svg',\n];"
new = "  './assets/images/exercises/ex-b06-lunges.svg',\n" + NEW_ASSETS + "];"

# Handle CRLF
content = content.replace(old.replace('\n', '\r\n'), new.replace('\n', '\r\n'))
# Also try LF
content = content.replace(old, new)

with open('sw.js', 'w', encoding='utf-8') as f:
    f.write(content)

# Verify
import re
m = re.search(r'const SHELL_ASSETS\s*=\s*\[(.*?)\];', content, re.DOTALL)
if m:
    count = m.group(1).count("'./")
    print(f"SHELL_ASSETS now has {count} entries")
else:
    print("ERROR: Could not find SHELL_ASSETS!")

print(f"sw.js size: {len(content)} bytes")
