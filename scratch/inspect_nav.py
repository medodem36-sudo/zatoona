with open('android/app/build.gradle.kts', 'r', encoding='utf-8') as f:
    text = f.read()

import re
m = re.search(r'applicationId\s*=\s*["\']([^"\']+)["\']', text)
if m:
    print('applicationId:', m.group(1))
else:
    print('No applicationId match, preview:\n', text[:800])
