import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('assets/data/exercise-catalog.js', 'r', encoding='utf-8') as f:
    cat_text = f.read()

json_match = re.search(r'(\[[\s\S]*\])', cat_text)
catalog = json.loads(json_match.group(1))

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

reg_match = re.search(r'const\s+GYM_PLAN_TEMPLATE_REGISTRY\s*=\s*\{([\s\S]*?)\n\};', html)
tpl_cat_ids = set()
if reg_match:
    tpl_cat_ids = set(re.findall(r'catalogExerciseId:\s*[\'\"]([^\'\"]+)[\'\"]', reg_match.group(0)))

DIRECT_LEGACY_MAP = {
    'goblet_squat': 'assets/images/exercises/ex-a01-goblet-squat.svg',
    'barbell_bench_press': 'assets/images/exercises/ex-a02-bench-press.svg',
    'lat_pulldown_wide_grip': 'assets/images/exercises/ex-a03-lat-pulldown.svg',
    'standing_overhead_barbell_press': 'assets/images/exercises/ex-a04-overhead-press.svg',
    'plank': 'assets/images/exercises/ex-a05-plank.svg',
    'face_pull_cable': 'assets/images/exercises/ex-a06-face-pull.svg',
    'romanian_deadlift_barbell': 'assets/images/exercises/ex-b01-romanian-deadlift.svg',
    'barbell_bent_over_row': 'assets/images/exercises/ex-b02-barbell-row.svg',
    'push_up': 'assets/images/exercises/ex-b03-push-up.svg',
    'pull_up': 'assets/images/exercises/ex-b04-pull-up.svg',
    'walking_lunges_dumbbell': 'assets/images/exercises/ex-b06-lunges.svg',
}

POTENTIAL_REVIEW_MAP = {
    'kettlebell_goblet_squat': ('ex-a01-goblet-squat.svg', 'كيتل بيل مقابل دمبل في جوبلت سكوات'),
    'seated_dumbbell_shoulder_press': ('ex-a04-overhead-press.svg', 'دمبل جالس مقابل بار واقف في شولدر برس'),
    'chin_up': ('ex-b04-pull-up.svg', 'قبضة مقلوبة سفلية مقابل قبضة علوية في العقلة'),
    'diamond_push_up': ('ex-b03-push-up.svg', 'قبضة ماسية ضيقة مقابل ضغط قياسي'),
    'decline_push_up': ('ex-b03-push-up.svg', 'قدمان مرتفعتان مقابل ضغط قياسي'),
    'incline_push_up': ('ex-b03-push-up.svg', 'يدان مرتفعتان مقابل ضغط قياسي'),
    'lat_pulldown_close_grip': ('ex-a03-lat-pulldown.svg', 'قبضة ضيقة V-bar مقابل قبضة واسعة'),
    'single_arm_cable_lat_pulldown': ('ex-a03-lat-pulldown.svg', 'سحب فردي بالكابل مقابل سحب بالماكينة'),
}

lines = []
lines.append("| # | معرّف التمرين (ID) | الاسم بالعربية | الاسم بالإنجليزية | العضلة الأساسية | النوع | المعدات | القالب | الفئة | حالة الصورة / الملاحظة |")
lines.append("|---|---|---|---|---|---|---|:---:|:---:|---|")

for idx, ex in enumerate(catalog, 1):
    eid = ex['id']
    name_ar = ex.get('nameAr', ex.get('name', ''))
    name_en = ex.get('name', '')
    pm = ', '.join(ex.get('primaryMuscles', []))
    mech = ex.get('mechanic', '')
    eq = ex.get('equipment', '')
    is_tpl = '✓' if eid in tpl_cat_ids else '—'
    
    if eid in DIRECT_LEGACY_MAP:
        cat_class = 'D'
        note = f"مغطى برسم محلي مطابق (`{DIRECT_LEGACY_MAP[eid]}`)"
    elif eid in POTENTIAL_REVIEW_MAP:
        cat_class = 'E'
        note = f"تشابه جزئي مع `{POTENTIAL_REVIEW_MAP[eid][0]}` ({POTENTIAL_REVIEW_MAP[eid][1]})؛ يحتاج حسم"
    else:
        cat_class = 'A'
        note = "مفقود — لا يوجد رسم SVG محلي وقائمة images فارغة"
        
    lines.append(f"| {idx} | `{eid}` | {name_ar} | {name_en} | {pm} | {mech} | {eq} | {is_tpl} | **{cat_class}** | {note} |")

output_table = '\n'.join(lines)
with open('scratch/full_119_matrix_table.md', 'w', encoding='utf-8') as f:
    f.write(output_table)

print(f"Generated table with {len(catalog)} rows. Saved to scratch/full_119_matrix_table.md")
