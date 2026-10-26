# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Point 1: HTML sleepView
p1_start = text.find('<!-- ===== SLEEP MODE ===== -->')
p1_end = text.find('<!-- ===== PRAYER MODE ===== -->')
print(f"Point 1 (HTML sleepView): {p1_start} to {p1_end}")
print(text[p1_start:p1_end])

# Point 2: Storage functions around loadSleepHabits
p2 = text.find('function saveSleepHabits(')
print(f"\nPoint 2 (Storage): {p2}")
print(text[p2-100:p2+200])

# Point 3: KNOWN_KEY_PATTERNS in validateBackupData
p3 = text.find('const KNOWN_KEY_PATTERNS = [')
print(f"\nPoint 3 (Backup Validation): {p3}")
print(text[p3:p3+300])

# Point 4: checkAndDispatchDueReminders
p4 = text.find('return triggered;')
print(f"\nPoint 4 (Scheduler return): {p4}")
print(text[p4-200:p4+50])
