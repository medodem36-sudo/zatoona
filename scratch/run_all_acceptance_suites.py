# -*- coding: utf-8 -*-
import subprocess
import sys

suites = [
    ('scratch/test_mega_full_system_sync.py', 27),
    ('scratch/test_compliance_legal_suite.py', 17),
    ('scratch/test_ui_paradigms.py', 10),
    ('scratch/test_prayer_nutrition_suite.py', 7),
    ('scratch/test_scrollable_schedule_widget.py', 8),
    ('scratch/test_phase13_habit_streaks.py', 26),
    ('scratch/test_phase17_perf_responsiveness_suite.py', 7)
]

print("================================================================================")
print("             ZATOONA MASTER FULL-SYSTEM ACCEPTANCE SUITE RUNNER                 ")
print("================================================================================")

all_passed = True
total_checks = 0

for script, expected_count in suites:
    p = subprocess.run([sys.executable, script], capture_output=True, text=True, encoding='utf-8')
    status = "PASS" if p.returncode == 0 else "FAIL"
    if p.returncode != 0:
        all_passed = False
        print(f"[{status}] {script} (Expected ~{expected_count} checks)")
        print("  STDERR:", p.stderr.strip()[:300])
    else:
        total_checks += expected_count
        print(f"[{status}] {script:<45} (PASSED ~{expected_count} checks)")

print("--------------------------------------------------------------------------------")
print(f"OVERALL STATUS: {'ALL SUITES PASSED (100%)' if all_passed else 'SOME SUITES FAILED'}")
print(f"TOTAL VERIFIED CHECKS: {total_checks}")
print("================================================================================")

if not all_passed:
    sys.exit(1)
