# -*- coding: utf-8 -*-
with open(r'scratch/test_master_regression_gate.py', 'r', encoding='utf-8') as f:
    text = f.read()

target = '''    {
        "id": "phase13_3",
        "name": "Phase 13.3 Healthy Sleep Habits & Bedtime Routine",
        "category": "Sleep & Recovery",
        "rel_path": "scratch/test_phase13_3_sleep_habits.py",
        "timeout_sec": 120,
        "active": True,
        "description": "Verifies target bedtime & wake settings, midnight crossing duration, circular diff, evening wind-down checklist, 5 core sleep habits preservation, actual vs target comparison, 7/28-day adherence summaries, reminder dispatching, and backup compatibility."
    },'''

replacement = '''    {
        "id": "phase13_3",
        "name": "Phase 13.3 Healthy Sleep Habits & Bedtime Routine",
        "category": "Sleep & Recovery",
        "rel_path": "scratch/test_phase13_3_sleep_habits.py",
        "timeout_sec": 120,
        "active": True,
        "description": "Verifies target bedtime & wake settings, midnight crossing duration, circular diff, evening wind-down checklist, 5 core sleep habits preservation, actual vs target comparison, 7/28-day adherence summaries, reminder dispatching, and backup compatibility."
    },
    {
        "id": "phase13_4b1",
        "name": "Phase 13.4B1 Isolated Native Android Shell Foundation",
        "category": "Native Android & Bridge",
        "rel_path": "scratch/test_phase13_4b1_scaffold.py",
        "timeout_sec": 120,
        "active": True,
        "description": "Verifies toolchain preflight, SOURCE_SCAFFOLD_ONLY status, android/ scaffold integrity, security settings (cleartext disabled, file access restricted), versioned ZatoonaBridge contract (v1), WebViewAssetLoader origin, and PWA storage invariance."
    },'''

normalized_text = text.replace('\r\n', '\n')
if target in normalized_text:
    new_text = normalized_text.replace(target, replacement, 1)
    with open(r'scratch/test_master_regression_gate.py', 'w', encoding='utf-8', newline='\n') as f:
        f.write(new_text)
    print("SUCCESS: Phase 13.4B1 registered in master gate")
else:
    print("ERROR: Target not found")
