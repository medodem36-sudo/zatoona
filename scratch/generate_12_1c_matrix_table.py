import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('assets/data/exercise-catalog.js', 'r', encoding='utf-8') as f:
    catalog = json.loads(re.search(r'window\.ZATOONA_EXERCISE_CATALOG\s*=\s*(\[[\s\S]*?\]);', f.read()).group(1))

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

reg_match = re.search(r'const\s+GYM_PLAN_TEMPLATE_REGISTRY\s*=\s*(\{[\s\S]*?\n\});', html)
tpl_slots = re.findall(r'\{\s*templateExerciseId:\s*[\'\"]([^\'\"]+)[\'\"]\s*,\s*catalogExerciseId:\s*[\'\"]([^\'\"]+)[\'\"]\s*,\s*name:\s*[\'\"]([^\'\"]+)[\'\"]', reg_match.group(1))
distinct_tpl_ids = set(ts[1] for ts in tpl_slots)

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

POTENTIAL_REVIEW = {
    'kettlebell_goblet_squat': ('ex-a01-goblet-squat.svg', 'كوب سكوات دمبل vs كيتل بيل'),
    'chin_up': ('ex-b04-pull-up.svg', 'عقلة قبضة سفلية vs علوية'),
    'diamond_push_up': ('ex-b03-push-up.svg', 'ضغط ماسي vs قياسي'),
    'decline_push_up': ('ex-b03-push-up.svg', 'ضغط قدمين مرتفعتين vs قياسي'),
    'incline_push_up': ('ex-b03-push-up.svg', 'ضغط يدين مرتفعتين vs قياسي'),
    'lat_pulldown_close_grip': ('ex-a03-lat-pulldown.svg', 'سحب عالي قبضة ضيقة vs واسعة'),
    'single_arm_cable_lat_pulldown': ('ex-a03-lat-pulldown.svg', 'سحب كابل فردي vs ماكينة ثنائي'),
}

lines = []
lines.append("| # | معرّف التمرين (ID) | الاسم بالعربية | الاسم بالإنجليزية | العضلة | النوع | المعدات | القالب | الفئة | رسم الـ SVG / الملاحظة | مرحلة التغطية |")
lines.append("|---|---|---|---|---|---|---|:---:|:---:|---|:---:|")

for idx, ex in enumerate(catalog, 1):
    eid = ex['id']
    name_ar = ex.get('nameAr', ex.get('name', ''))
    name_en = ex.get('name', '')
    pm = ', '.join(ex.get('primaryMuscles', []))
    mech = ex.get('mechanic', '')
    eq = ex.get('equipment', '')
    is_tpl = '✓' if eid in distinct_tpl_ids else '—'
    
    if eid in NEW_19:
        cat_class = 'D'
        svg_note = f"`{NEW_19[eid]}`"
        phase_str = "Phase 12.1B (جديد)"
    elif eid in LEGACY_12:
        cat_class = 'D'
        svg_note = f"`{LEGACY_12[eid]}`"
        phase_str = "Pre-12.1B (قديم)"
    elif eid in POTENTIAL_REVIEW:
        cat_class = 'E'
        svg_note = f"تشابه جزئي مع `{POTENTIAL_REVIEW[eid][0]}` ({POTENTIAL_REVIEW[eid][1]})"
        phase_str = "—"
    else:
        cat_class = 'A'
        svg_note = "لا يوجد رسم افتراضي"
        phase_str = "—"
        
    lines.append(f"| {idx} | `{eid}` | {name_ar} | {name_en} | {pm} | {mech} | {eq} | {is_tpl} | **{cat_class}** | {svg_note} | {phase_str} |")

table_md = '\n'.join(lines)
with open('scratch/full_119_reconciled_table.md', 'w', encoding='utf-8') as f:
    f.write(table_md)

print("Generated full 119 reconciled table in scratch/full_119_reconciled_table.md")
