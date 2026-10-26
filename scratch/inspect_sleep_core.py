# -*- coding: utf-8 -*-
with open(r'index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines in index.html: {len(lines)}")

def find_patterns(pattern_list):
    for pat in pattern_list:
        print(f"\n--- Searching for: {pat} ---")
        matches = []
        for i, line in enumerate(lines):
            if pat.lower() in line.lower():
                matches.append((i + 1, line.strip()[:120]))
        print(f"Found {len(matches)} occurrences:")
        for line_num, text in matches[:10]:
            print(f"  L{line_num}: {text}")
        if len(matches) > 10:
            print(f"  ... and {len(matches) - 10} more")

find_patterns([
    'SLEEP_HABITS',
    'sleepq',
    'renderSleep',
    'saveSleep',
    'loadSleep',
    'napDuration',
    'sleepStartOffset',
    'exportData',
    'importData',
    'renderScheduleChecklist',
    'scheduleChecklistItems'
])
