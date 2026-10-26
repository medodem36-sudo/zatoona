import re
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

print("=== 1. LOCALSTORAGE KEYS AUDIT ===")
# Find all localStorage.getItem and localStorage.setItem, storageGet, storageSet
storage_gets = set(re.findall(r"(?:localStorage\.getItem|storageGet|storageGetJSON)\s*\(\s*['\"]([^'\"]+)['\"]", content))
storage_sets = set(re.findall(r"(?:localStorage\.setItem|storageSet)\s*\(\s*['\"]([^'\"]+)['\"]", content))

# Also dynamic prefixes
prefixes_get = set(re.findall(r"(?:localStorage\.getItem|storageGet|storageGetJSON)\s*\(\s*['\"]([^'\"]*[:_])['\"]\s*\+", content))
prefixes_set = set(re.findall(r"(?:localStorage\.setItem|storageSet)\s*\(\s*['\"]([^'\"]*[:_])['\"]\s*\+", content))

print(f"Static keys read: {len(storage_gets)}")
print(f"Static keys written: {len(storage_sets)}")
print(f"Key prefixes read: {prefixes_get}")
print(f"Key prefixes written: {prefixes_set}")

print("\nSample static keys read:")
for k in sorted(list(storage_gets))[:20]:
    print(f"  - {k} (written: {k in storage_sets})")

print("\n=== 2. BACKUP & RESTORE AUDIT ===")
# Find what keys/data backup exports and restore imports
m_export = re.search(r'function\s+(?:exportData|backupData|exportAllData|downloadBackup)\s*\([^{]*\{', content)
if not m_export:
    m_export = re.search(r'(?:export|backup)[a-zA-Z0-9_]*\s*=\s*function', content)

matches_backup = [m.start() for m in re.finditer(r'(?:backup|export|restore|import)', content, re.IGNORECASE)]
print(f"Backup/export/restore occurrences: {len(matches_backup)}")

for p in matches_backup:
    snippet = content[max(0, p-40):min(len(content), p+250)]
    if 'function ' in snippet or 'localStorage' in snippet:
        print("--- Snippet ---")
        print('\n'.join(snippet.splitlines()[:6]))

print("\n=== 3. DANGEROUS PATTERNS (eval, Function constructor) ===")
evals = list(re.finditer(r'\beval\s*\(', content))
print(f"eval() calls: {len(evals)}")
new_funcs = list(re.finditer(r'new\s+Function\s*\(', content))
print(f"new Function() calls: {len(new_funcs)}")

print("\n=== 4. ASSETS & MANIFEST INTEGRITY ===")
# Check manifest icons
with open('manifest.json', 'r', encoding='utf-8') as f:
    manifest = f.read()

import json
m_json = json.loads(manifest)
for icon in m_json.get('icons', []):
    src = icon.get('src')
    # strip leading /
    clean_src = src.lstrip('./').lstrip('/')
    exists = os.path.exists(clean_src)
    print(f"Icon {clean_src}: exists={exists}")

print("\n=== 5. SERVICE WORKER PRECACHED ASSETS ===")
with open('sw.js', 'r', encoding='utf-8') as f:
    sw = f.read()

precached = re.findall(r"['\"]([^'\"]+\.(?:html|js|css|png|svg|json|woff2?))['\"]", sw)
print(f"Precached file references in sw.js: {len(precached)}")
missing = []
for p in precached:
    clean = p.lstrip('./').lstrip('/')
    if not os.path.exists(clean):
        missing.append(clean)
print(f"Missing precache files: {len(missing)} -> {missing[:10]}")
