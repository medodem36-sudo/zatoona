import sys, os
sys.stdout.reconfigure(encoding='utf-8')

brain_scratch = r'C:\Users\Lenovo\.gemini\antigravity\brain\220cd884-91e5-4cf7-90a3-e5ff4b3e8db0\scratch'
repo_scratch = 'scratch'

test_files = []
for folder in [repo_scratch, brain_scratch]:
    if os.path.exists(folder):
        for f in os.listdir(folder):
            if f.startswith('test_') and f.endswith('.py'):
                p = os.path.join(folder, f)
                test_files.append((f, p, os.path.getsize(p)))

# Deduplicate by filename
unique_tests = {}
for fn, path, sz in test_files:
    if fn not in unique_tests:
        unique_tests[fn] = (path, sz)

print(f'Total unique test scripts found: {len(unique_tests)}')
for fn in sorted(unique_tests.keys()):
    path, sz = unique_tests[fn]
    with open(path, 'r', encoding='utf-8') as tf:
        code = tf.read()
    uses_selenium = 'selenium' in code
    test_count = code.count('test(') + code.count('def test_') + code.count('assert ')
    print(f'  {fn:40} ({sz:6,} B) | Selenium: {str(uses_selenium):5} | ~{test_count:2} test assertions')
