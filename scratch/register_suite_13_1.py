import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/test_master_regression_gate.py', 'r', encoding='utf-8') as f:
    gate_content = f.read()

target = """    {
        "id": "phase12_1b",
        "name": "Phase 12.1B Curated Exercise Catalog Images",
        "category": "Images & Exercises",
        "rel_path": "scratch/test_phase12_1b_exercise_images.py",
        "timeout_sec": 120,
        "active": True,
        "description": "Verifies 19 curated exercise SVGs, 100% coverage of 26 template exercises, sw.js v24 precaching, and offline integrity."
    },"""

suite_13_1 = """    {
        "id": "phase12_1b",
        "name": "Phase 12.1B Curated Exercise Catalog Images",
        "category": "Images & Exercises",
        "rel_path": "scratch/test_phase12_1b_exercise_images.py",
        "timeout_sec": 120,
        "active": True,
        "description": "Verifies 19 curated exercise SVGs, 100% coverage of 26 template exercises, sw.js v24 precaching, and offline integrity."
    },
    {
        "id": "phase13_1",
        "name": "Phase 13.1 Checklist & Worship Labels Repair",
        "category": "UX & Checklists",
        "rel_path": "scratch/test_phase13_1_checklist_labels.py",
        "timeout_sec": 120,
        "active": True,
        "description": "Verifies renderSimpleChecklist and renderScheduleChecklist label rendering, Arabic worship labels, sleep habits labels, icons, click toggling, and layout responsiveness."
    },"""

if target in gate_content:
    gate_content = gate_content.replace(target, suite_13_1, 1)
    with open('scratch/test_master_regression_gate.py', 'w', encoding='utf-8') as f:
        f.write(gate_content)
    print("Registered Phase 13.1 suite in test_master_regression_gate.py successfully.")
else:
    print("Target not found in test_master_regression_gate.py")
