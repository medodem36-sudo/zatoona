import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('assets/data/exercise-catalog.js', 'r', encoding='utf-8') as f:
    cat = json.loads(re.search(r'window\.ZATOONA_EXERCISE_CATALOG\s*=\s*(\[[\s\S]*?\]);', f.read()).group(1))

cat_dict = {e['id']: e for e in cat}

batch_2 = [
    ('barbell_front_squat', 'سكوات أمامي بالبار (فرونت سكوات)'),
    ('chest_dips', 'متوازي للصدر (Dips)'),
    ('one_arm_dumbbell_row', 'تجديف دمبل فردي (منشار دمبل)'),
    ('t_bar_row', 'تجديف تي بار (T-Bar Row)'),
    ('barbell_hip_thrust', 'هيب ثرست بالبار (Hip Thrust)'),
    ('bulgarian_split_squat', 'بلغاريان سبليت سكوات بالدمبل (سكوات بلغاري)'),
    ('sumo_deadlift', 'سومو ديدليفت بالبار (وقفة واسعة)'),
    ('hack_squat_machine', 'هاك سكوات بالماكينة'),
    ('pendlay_row', 'بيندلاي رو بالبار (تجديف من الأرض)'),
    ('close_grip_bench_press', 'بنش برس قبضة ضيقة بالبار (تركيز ترايسبس)'),
    ('arnold_press', 'أرنولد برس بالدمبل جالس'),
    ('kettlebell_swing', 'سوينج كيتل بيل (مرجحة الكيتل بيل)'),
    ('ab_wheel_rollout', 'دحرجة عجلة البطن (آب رول آوت)'),
    ('farmers_walk', 'مشي المزارع بالدمبل (فارمرز ووك)'),
    ('chin_up', 'تمرين العقلة قبضة سفلية معكوسة'),
    ('decline_barbell_bench_press', 'بنش هابط بالبار'),
    ('cable_crossover_high_to_low', 'تجميع كابل من أعلى لأسفل'),
    ('preacher_curl', 'كيرل بايسبس على بنش بريتشر (لاري سكوت)'),
    ('cable_kneeling_crunch', 'كرانش البطن بالكابل راكعاً (سجود بالكابل)'),
    ('dumbbell_shrugs', 'رفع الكتفين بالدمبل (ترابيس بالدمبل)')
]

print("Checking Batch 2 (20 exercises):")
all_found = True
for idx, (eid, ar) in enumerate(batch_2, 1):
    ex = cat_dict.get(eid)
    if ex:
        print(f"{idx:2d}. [FOUND] {eid:30} | {ex.get('mechanic','?'):10} | {ex.get('equipment','?'):10} | {ex.get('nameAr', ex.get('name'))}")
    else:
        print(f"{idx:2d}. [NOT FOUND] {eid}")
        all_found = False

print(f"\nAll 20 verified in catalog: {all_found}")
