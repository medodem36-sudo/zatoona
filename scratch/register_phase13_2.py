# -*- coding: utf-8 -*-
with open(r'scratch/test_master_regression_gate.py', 'r', encoding='utf-8') as f:
    text = f.read()

target = '''    {
        "id": "phase13_1",
        "name": "Phase 13.1 Checklist & Worship Labels Repair",
        "category": "UX & Checklists",
        "rel_path": "scratch/test_phase13_1_checklist_labels.py",
        "timeout_sec": 120,
        "active": True,
        "description": "Verifies renderSimpleChecklist and renderScheduleChecklist label rendering, Arabic worship labels, sleep habits labels, icons, click toggling, and layout responsiveness."
    },'''

replacement = '''    {
        "id": "phase13_1",
        "name": "Phase 13.1 Checklist & Worship Labels Repair",
        "category": "UX & Checklists",
        "rel_path": "scratch/test_phase13_1_checklist_labels.py",
        "timeout_sec": 120,
        "active": True,
        "description": "Verifies renderSimpleChecklist and renderScheduleChecklist label rendering, Arabic worship labels, sleep habits labels, icons, click toggling, and layout responsiveness."
    },
    {
        "id": "phase13_2",
        "name": "Phase 13.2 Cairo Prayer Times Support",
        "category": "Prayer & Schedule",
        "rel_path": "scratch/test_phase13_2_cairo_prayer.py",
        "timeout_sec": 120,
        "active": True,
        "description": "Verifies Cairo option in #prayerCitySelect and #scPrayerCity, PRAYER_SUPPORTED_CITIES, bidirectional sync, cache isolation, historical tracking preservation, and 375px mobile responsiveness."
    },'''

# Normalize newlines for matching
normalized_text = text.replace('\r\n', '\n')
if target in normalized_text:
    new_text = normalized_text.replace(target, replacement, 1)
    # preserve original newline style if needed or write standard
    with open(r'scratch/test_master_regression_gate.py', 'w', encoding='utf-8', newline='\n') as f:
        f.write(new_text)
    print("SUCCESS: Phase 13.2 registered in master gate")
else:
    print("ERROR: Target not found")
