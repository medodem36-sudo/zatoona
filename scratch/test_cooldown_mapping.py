import json, os, sys

sys.stdout.reconfigure(encoding="utf-8")

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG_PATH = os.path.join(REPO, "assets", "data", "stretch-catalog.js")

with open(CATALOG_PATH, "r", encoding="utf-8") as f:
    text = f.read()

catalog = json.loads(text.split("window.ZATOONA_STRETCH_CATALOG =")[1].strip().rstrip(";"))
cooldown_stretches = {s['id']: s for s in catalog if 'cooldown' in s.get('suitableFor', [])}

print("Loaded cooldown stretches:", len(cooldown_stretches))

# Test target muscles mapping
mapping = {
    'chest': 'str-doorway-pec-stretch',
    'shoulders': 'str-cross-body-shoulder-stretch',
    'lats': 'str-lat-wall-stretch',
    'lower_back': 'str-childs-pose',
    'neck': 'str-upper-trap-stretch',
    'hip_flexors': 'str-kneeling-hip-flexor',
    'adductors': 'str-butterfly-stretch',
    'quads': 'str-standing-quad-stretch',
    'hamstrings': 'str-standing-hamstring-stretch',
    'glutes': 'str-pigeon-pose',
    'calves': 'str-wall-calf-stretch',
    'forearms': 'str-wrist-extensor-stretch',
    'abs': 'str-cobra-lumbar-stretch',
    'spine': 'str-cat-cow-mobility'
}

for m, sid in mapping.items():
    assert sid in cooldown_stretches, f"Missing {sid} for muscle {m}"
    s = cooldown_stretches[sid]
    print(f"Muscle: {m:12s} -> {sid:30s} | {s['nameAr']} ({s['durationSeconds']}s)")

print("\nAll cooldown muscle mappings valid!")
