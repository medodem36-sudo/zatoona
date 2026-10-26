# -*- coding: utf-8 -*-
with open(r'scratch/test_master_regression_gate.py', 'r', encoding='utf-8') as f:
    text = f.read()

target = '''    {
        "id": "phase13_2",
        "name": "Phase 13.2 Cairo Prayer Times Support",
        "category": "Prayer & Schedule",
        "rel_path": "scratch/test_phase13_2_cairo_prayer.py",
        "timeout_sec": 120,
        "active": True,
        "description": "Verifies Cairo option in #prayerCitySelect and #scPrayerCity, PRAYER_SUPPORTED_CITIES, bidirectional sync, cache isolation, historical tracking preservation, and 375px mobile responsiveness."
    },'''

replacement = '''    {
        "id": "phase13_2",
        "name": "Phase 13.2 Cairo Prayer Times Support",
        "category": "Prayer & Schedule",
        "rel_path": "scratch/test_phase13_2_cairo_prayer.py",
        "timeout_sec": 120,
        "active": True,
        "description": "Verifies Cairo option in #prayerCitySelect and #scPrayerCity, PRAYER_SUPPORTED_CITIES, bidirectional sync, cache isolation, historical tracking preservation, and 375px mobile responsiveness."
    },
    {
        "id": "phase13_3",
        "name": "Phase 13.3 Healthy Sleep Habits & Bedtime Routine",
        "category": "Sleep & Recovery",
        "rel_path": "scratch/test_phase13_3_sleep_habits.py",
        "timeout_sec": 120,
        "active": True,
        "description": "Verifies target bedtime & wake settings, midnight crossing duration, circular diff, evening wind-down checklist, 5 core sleep habits preservation, actual vs target comparison, 7/28-day adherence summaries, reminder dispatching, and backup compatibility."
    },'''

normalized_text = text.replace('\r\n', '\n')
if target in normalized_text:
    new_text = normalized_text.replace(target, replacement, 1)
    with open(r'scratch/test_master_regression_gate.py', 'w', encoding='utf-8', newline='\n') as f:
        f.write(new_text)
    print("SUCCESS: Phase 13.3 registered in master gate")
else:
    print("ERROR: Target not found")
