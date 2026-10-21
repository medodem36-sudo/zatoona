import re, sys, os, json

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html_text = f.read()

with open('assets/data/exercise-catalog.js', 'r', encoding='utf-8') as f:
    catalog_text = f.read()

with open('sw.js', 'r', encoding='utf-8') as f:
    sw_text = f.read()

print("="*80)
print("1. EXERCISE CATALOG & IMAGES AUDIT")
print("="*80)

# Check exercise-catalog.js structure
print("Catalog text length:", len(catalog_text))
has_images_in_catalog = 'image' in catalog_text.lower() or 'img' in catalog_text.lower() or 'photo' in catalog_text.lower()
print("Does exercise-catalog.js contain image/img/photo properties?", has_images_in_catalog)

# Sample entries from catalog
m_cat = re.search(r'const\s+ZATOONA_EXERCISE_CATALOG\s*=\s*\[(.*?)\];', catalog_text, re.DOTALL)
if m_cat:
    # count items
    items = re.findall(r'\{\s*id:\s*["\']([^"\']+)["\']', m_cat.group(1))
    print(f"Total exercises in ZATOONA_EXERCISE_CATALOG: {len(items)}")
    # check first 3 items
    first_items = re.findall(r'(\{[^}]+\})', m_cat.group(1))
    for it in first_items[:3]:
        print("  Sample item:", it.strip())

# Check exercise-image-map in index.html
print("\n--- Exercise Image Map Engine in index.html ---")
ex_img_refs = re.findall(r'exercise-image-map-v1', html_text)
print("Occurrences of 'exercise-image-map-v1':", len(ex_img_refs))

# Find functions related to exercise images
for fn in ['loadExerciseImageMap', 'saveExerciseImage', 'getExerciseImage', 'renderExerciseImage', 'openExerciseImageModal']:
    found = fn in html_text
    print(f"  {fn}: {found}")

# Search for male-only references in index.html
male_refs = re.findall(r'.{0,40}(?:maleOnly|رجال|ذكور).{0,40}', html_text)
print(f"\nMale-only policy references ({len(male_refs)}):")
for mr in male_refs[:5]:
    print("  ", mr.strip())

print("\n" + "="*80)
print("2. STRETCHES & MOBILITY AUDIT")
print("="*80)
stretch_terms = ['stretch', 'mobility', 'استطالة', 'تمدد', 'إطالة', 'مرونة', 'موبيلتي']
for st in stretch_terms:
    matches = re.findall(rf'.{{0,30}}{st}.{{0,30}}', html_text, re.IGNORECASE)
    cat_matches = re.findall(rf'.{{0,30}}{st}.{{0,30}}', catalog_text, re.IGNORECASE)
    print(f"Term '{st}': {len(matches)} in index.html, {len(cat_matches)} in catalog")
    if matches:
        print(f"   Sample from index: {matches[0].strip()}")
    if cat_matches:
        print(f"   Sample from catalog: {cat_matches[0].strip()}")

print("\n" + "="*80)
print("3. WARM-UP & COOL-DOWN AUDIT")
print("="*80)
warmup_terms = ['warmup', 'warm-up', 'تسخين', 'إحماء', 'cooldown', 'cool-down', 'تهدئة']
for wt in warmup_terms:
    matches = re.findall(rf'.{{0,40}}{wt}.{{0,40}}', html_text, re.IGNORECASE)
    print(f"Term '{wt}': {len(matches)} in index.html")
    for m in matches[:3]:
        print(f"   Sample: {m.strip()}")

print("\n" + "="*80)
print("4. HOME INVENTORY (المخزون المنزلي) AUDIT")
print("="*80)
pantry_terms = ['pantry', 'inventory', 'مخزون', 'ثلاجة', 'منزل']
for pt in pantry_terms:
    matches = re.findall(rf'.{{0,40}}{pt}.{{0,40}}', html_text, re.IGNORECASE)
    print(f"Term '{pt}': {len(matches)} in index.html")
    for m in matches[:3]:
        print(f"   Sample: {m.strip()}")

print("\n" + "="*80)
print("5. WEB PUSH & BACKGROUND NOTIFICATIONS AUDIT")
print("="*80)
print("In sw.js:")
print("  has 'push' listener:", "addEventListener('push'" in sw_text or 'addEventListener("push"' in sw_text)
print("  has 'periodicsync':", "periodicsync" in sw_text)
print("  has 'notificationclick':", "addEventListener('notificationclick'" in sw_text)
print("In index.html:")
print("  has PushManager:", "PushManager" in html_text)
print("  has pushManager.subscribe:", "pushManager.subscribe" in html_text)
print("  has VAPID references:", "vapid" in html_text.lower())

print("\n" + "="*80)
print("6. CONVERSATIONAL AI / ASSISTANT AUDIT")
print("="*80)
ai_terms = ['chatbot', 'assistant', 'مساعد ذكي', 'openai', 'gemini', 'anthropic', 'bot']
for at in ai_terms:
    matches = re.findall(rf'.{{0,40}}{at}.{{0,40}}', html_text, re.IGNORECASE)
    print(f"Term '{at}': {len(matches)} in index.html")
    for m in matches[:2]:
        print(f"   Sample: {m.strip()}")
