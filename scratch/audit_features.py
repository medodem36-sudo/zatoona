import sys, re, os, json
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

print('=== 1. STORAGE KEYS AUDIT ===')
# Extract keys with regex
storage_sets = set(re.findall(r'storageSet(?:JSON)?\s*\(\s*["\']([^"\']+)["\']', text))
storage_gets = set(re.findall(r'storageGet(?:JSON|JSONArray)?\s*\(\s*["\']([^"\']+)["\']', text))
prefix_keys = set(re.findall(r'STORAGE_PREFIX\s*\+\s*["\']([^"\']+)["\']', text))

all_keys = sorted(storage_sets | storage_gets | prefix_keys)
print(f'Total distinct static storage keys/prefixes: {len(all_keys)}')
for k in all_keys:
    print(f'  {k}')

# Dynamic keys patterns:
dynamic_patterns = re.findall(r'STORAGE_PREFIX\s*\+\s*([a-zA-Z0-9_]+(?:\s*\+\s*[^,\)]+)?)', text)
print(f'\nDynamic storage key expressions (sample): {len(dynamic_patterns)}')
for dp in set(dynamic_patterns[:20]):
    print(f'  STORAGE_PREFIX + {dp}')

print('\n=== 2. BACKUP & EXPORT AUDIT ===')
exp_idx = text.find('function exportAllData')
if exp_idx != -1:
    print('exportAllData found at line:', text[:exp_idx].count('\n') + 1)
    print(text[exp_idx:exp_idx+1500])

val_idx = text.find('function validateBackupData')
if val_idx != -1:
    print('\nvalidateBackupData found at line:', text[:val_idx].count('\n') + 1)
    print(text[val_idx:val_idx+1500])

imp_idx = text.find('function importAllData')
if imp_idx != -1:
    print('\nimportAllData found at line:', text[:imp_idx].count('\n') + 1)
    print(text[imp_idx:imp_idx+1500])
