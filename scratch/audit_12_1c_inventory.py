import json
import os
import re
import sys
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding='utf-8')

REPO_ROOT = os.path.abspath(os.getcwd())
CATALOG_PATH = os.path.join(REPO_ROOT, 'assets', 'data', 'exercise-catalog.js')
EX_DIR = os.path.join(REPO_ROOT, 'assets', 'images', 'exercises')

# 1. Load Catalog
with open(CATALOG_PATH, 'r', encoding='utf-8') as f:
    cat_text = f.read()

m = re.search(r'window\.ZATOONA_EXERCISE_CATALOG\s*=\s*(\[[\s\S]*?\]);', cat_text)
assert m, "Catalog pattern not found!"
catalog = json.loads(m.group(1))
print(f"Catalog loaded: {len(catalog)} exercises.")

# 2. Check SVG files on disk in assets/images/exercises
disk_svgs = sorted([f for f in os.listdir(EX_DIR) if f.endswith('.svg')])
print(f"Total SVGs in assets/images/exercises: {len(disk_svgs)}")

# 3. Load Templates from index.html
with open(os.path.join(REPO_ROOT, 'index.html'), 'r', encoding='utf-8') as f:
    html = f.read()

reg_match = re.search(r'const\s+GYM_PLAN_TEMPLATE_REGISTRY\s*=\s*(\{[\s\S]*?\n\});', html)
tpl_slots = re.findall(r'\{\s*templateExerciseId:\s*[\'\"]([^\'\"]+)[\'\"]\s*,\s*catalogExerciseId:\s*[\'\"]([^\'\"]+)[\'\"]\s*,\s*name:\s*[\'\"]([^\'\"]+)[\'\"]', reg_match.group(1))
distinct_tpl_ids = sorted(list(set(ts[1] for ts in tpl_slots)))
print(f"Preset template occurrences: {len(tpl_slots)}, unique catalog IDs: {len(distinct_tpl_ids)}")

LEGACY_12 = {
    'goblet_squat': 'ex-a01-goblet-squat.svg',
    'barbell_bench_press': 'ex-a02-bench-press.svg',
    'lat_pulldown_wide_grip': 'ex-a03-lat-pulldown.svg',
    'standing_overhead_barbell_press': 'ex-a04-overhead-press.svg',
    'plank': 'ex-a05-plank.svg',
    'face_pull_cable': 'ex-a06-face-pull.svg',
    'romanian_deadlift_barbell': 'ex-b01-romanian-deadlift.svg',
    'barbell_bent_over_row': 'ex-b02-barbell-row.svg',
    'push_up': 'ex-b03-push-up.svg',
    'pull_up': 'ex-b04-pull-up.svg',
    'walking_lunges_dumbbell': 'ex-b06-lunges.svg',
}

NEW_19 = {
    'barbell_back_squat': 'ex-barbell-back-squat.svg',
    'conventional_deadlift': 'ex-conventional-deadlift.svg',
    'incline_barbell_bench_press': 'ex-incline-barbell-bench-press.svg',
    'incline_dumbbell_press': 'ex-incline-dumbbell-press.svg',
    'dumbbell_bench_press': 'ex-dumbbell-bench-press.svg',
    'seated_cable_row': 'ex-seated-cable-row.svg',
    'leg_press': 'ex-leg-press.svg',
    'seated_dumbbell_shoulder_press': 'ex-seated-dumbbell-shoulder-press.svg',
    'hanging_leg_raise': 'ex-hanging-leg-raise.svg',
    'standing_dumbbell_lateral_raise': 'ex-standing-dumbbell-lateral-raise.svg',
    'barbell_curl': 'ex-barbell-curl.svg',
    'hammer_curl': 'ex-hammer-curl.svg',
    'triceps_rope_pushdown': 'ex-triceps-rope-pushdown.svg',
    'skull_crushers': 'ex-skull-crushers.svg',
    'dumbbell_chest_flyes': 'ex-dumbbell-chest-flyes.svg',
    'lying_leg_curl_machine': 'ex-lying-leg-curl-machine.svg',
    'seated_leg_curl_machine': 'ex-seated-leg-curl-machine.svg',
    'standing_calf_raise_machine': 'ex-standing-calf-raise-machine.svg',
    'seated_palms_up_wrist_curl': 'ex-seated-palms-up-wrist-curl.svg',
}

# Audit every SVG on disk
svg_health = {}
for sf in disk_svgs:
    p = os.path.join(EX_DIR, sf)
    sz = os.path.getsize(p)
    valid_xml = False
    vb = None
    has_base64 = False
    has_js = False
    has_ext_url = False
    
    try:
        tree = ET.parse(p)
        root = tree.getroot()
        valid_xml = root.tag.endswith('svg')
        vb = root.attrib.get('viewBox')
    except Exception as e:
        valid_xml = False
        
    with open(p, 'r', encoding='utf-8') as f:
        content = f.read()
        if 'data:image' in content: has_base64 = True
        if '<script' in content: has_js = True
        c_clean = content.replace('http://www.w3.org/2000/svg', '').replace('http://www.w3.org/1999/xlink', '')
        if 'http://' in c_clean or 'https://' in c_clean: has_ext_url = True
        
    svg_health[sf] = {
        'size': sz,
        'valid_xml': valid_xml,
        'viewBox': vb,
        'has_base64': has_base64,
        'has_js': has_js,
        'has_ext_url': has_ext_url,
        'healthy': valid_xml and vb == '0 0 300 200' and not has_base64 and not has_js and not has_ext_url
    }

unhealthy_svgs = [k for k, v in svg_health.items() if not v['healthy']]
print(f"Unhealthy SVGs on disk: {len(unhealthy_svgs)}")
if unhealthy_svgs:
    print("Unhealthy:", unhealthy_svgs)

# Re-categorize all 119 exercises into A, B, C, D, E
POTENTIAL_REVIEW_NON_TPL = {
    'kettlebell_goblet_squat': ('ex-a01-goblet-squat.svg', 'كوب سكوات دمبل vs كيتل بيل'),
    'chin_up': ('ex-b04-pull-up.svg', 'عقلة قبضة سفلية vs علوية'),
    'diamond_push_up': ('ex-b03-push-up.svg', 'ضغط ماسي vs قياسي'),
    'decline_push_up': ('ex-b03-push-up.svg', 'ضغط قدمين مرتفعتين vs قياسي'),
    'incline_push_up': ('ex-b03-push-up.svg', 'ضغط يدين مرتفعتين vs قياسي'),
    'lat_pulldown_close_grip': ('ex-a03-lat-pulldown.svg', 'سحب عالي قبضة ضيقة vs واسعة'),
    'single_arm_cable_lat_pulldown': ('ex-a03-lat-pulldown.svg', 'سحب كابل فردي vs ماكينة ثنائي'),
}

classified = []
counts = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0}

for ex in catalog:
    eid = ex['id']
    is_tpl = eid in distinct_tpl_ids
    imgs = ex.get('images', [])
    
    if eid in NEW_19:
        cat_class = 'D'
        coverage_phase = 'Phase 12.1B (جديد)'
        note = f"مغطى برسم SVG جديد منفذ ومطابق ({NEW_19[eid]})"
    elif eid in LEGACY_12:
        cat_class = 'D'
        coverage_phase = 'Pre-12.1B (قديم)'
        note = f"مغطى برسم SVG سابق مطابق ({LEGACY_12[eid]})"
    elif eid in POTENTIAL_REVIEW_NON_TPL:
        cat_class = 'E'
        coverage_phase = 'Uncovered'
        note = f"تشابه جزئي مع {POTENTIAL_REVIEW_NON_TPL[eid][0]} ({POTENTIAL_REVIEW_NON_TPL[eid][1]})؛ يحتاج حسم في الدفعات القادمة"
    else:
        cat_class = 'A'
        coverage_phase = 'Uncovered'
        note = "لا توجد صورة افتراضية ملحقة"
        
    counts[cat_class] += 1
    classified.append({
        'id': eid,
        'name': ex['name'],
        'nameAr': ex.get('nameAr', ex['name']),
        'mechanic': ex.get('mechanic', ''),
        'equipment': ex.get('equipment', ''),
        'primaryMuscles': ex.get('primaryMuscles', []),
        'in_template': is_tpl,
        'category': cat_class,
        'coverage_phase': coverage_phase,
        'images': imgs,
        'note': note
    })

print("\n--- Current Coverage Summary (119 Exercises) ---")
for k, v in sorted(counts.items()):
    print(f"  Category {k}: {v}")

total_sum = sum(counts.values())
print(f"Total classified: {total_sum} (Matches catalog 119: {total_sum == 119})")

# Breakdown of D category
d_items = [c for c in classified if c['category'] == 'D']
d_tpl = [c for c in d_items if c['in_template']]
d_non_tpl = [c for c in d_items if not c['in_template']]
print(f"\nCategory D Details ({len(d_items)} total):")
print(f"  - In preset templates: {len(d_tpl)} (out of {len(distinct_tpl_ids)} template exercises -> {len(d_tpl)/len(distinct_tpl_ids)*100:.1f}%)")
print(f"  - Outside templates: {len(d_non_tpl)}")

# Check template coverage
all_tpl_covered = all(c['category'] == 'D' for c in classified if c['in_template'])
print(f"\nALL 26 PRESET TEMPLATE EXERCISES ARE CATEGORY D: {all_tpl_covered}")
