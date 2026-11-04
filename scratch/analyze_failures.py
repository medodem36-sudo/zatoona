import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/test-results/test_master_report.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for suite in data.get('suites', []):
    if suite.get('status') != 'PASS':
        name = suite.get('name', '?')
        p = suite.get('passed', 0)
        fl = suite.get('failed', 0)
        print(f"FAIL: {name} ({p}P/{fl}F)")
        for tc in suite.get('failures', []):
            msg = str(tc)[:200]
            print(f"  - {msg}")
