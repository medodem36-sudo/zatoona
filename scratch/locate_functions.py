import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re

for fn in ['renderSimpleChecklist', 'renderScheduleChecklist']:
    m = re.search(rf'function\s+{fn}\s*\([^{{]*\{{', content)
    if m:
        start = m.start()
        # Find closing brace by counting braces
        brace_count = 0
        end = start
        for i in range(start, len(content)):
            if content[i] == '{':
                brace_count += 1
            elif content[i] == '}':
                brace_count -= 1
                if brace_count == 0:
                    end = i + 1
                    break
        print(f"=== {fn} ===")
        print(f"Start: {start}, End: {end}, Length: {end - start}")
        print(content[start:end])
        print("=" * 40)
