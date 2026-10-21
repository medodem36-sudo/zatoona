import sys, re, json

sys.stdout.reconfigure(encoding='utf-8')

# 1. Inspect exercise-catalog.js
with open('assets/data/exercise-catalog.js', 'r', encoding='utf-8') as f:
    cat_text = f.read()

# Find all exercise definitions
# Structure: { id: '...', name: '...', target: '...', ... }
ex_objs = re.findall(r'(\{\s*id:\s*["\'][^"\']+["\'][^\}]+\})', cat_text)
print(f"Total exercise objects in exercise-catalog.js: {len(ex_objs)}")

images_in_catalog = []
for ex in ex_objs:
    if 'image' in ex or 'img' in ex:
        images_in_catalog.append(ex)

print(f"Exercises in catalog with 'image' or 'img': {len(images_in_catalog)}")
if images_in_catalog:
    print("Sample with image:", images_in_catalog[0])

# Inspect fields of first exercise
if ex_objs:
    print("\nFirst exercise definition:")
    print(ex_objs[0])

# 2. Inspect WARMUP and COOLDOWN in index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html_text = f.read()

warmup_m = re.search(r'const\s+WARMUP\s*=\s*(\[[^\]]+\]);', html_text)
if warmup_m:
    print("\nWARMUP definition in index.html:")
    print(warmup_m.group(0))

cooldown_m = re.search(r'const\s+COOLDOWN\s*=\s*(\[[^\]]+\]);', html_text)
if cooldown_m:
    print("\nCOOLDOWN definition in index.html:")
    print(cooldown_m.group(0))

# 3. Check how WARMUP and COOLDOWN are rendered and used
warmup_render_m = re.search(r'function\s+renderWarmup[^\)]*\)\{[^\}]+\}', html_text)
if warmup_render_m:
    print("\nrenderWarmup:")
    print(warmup_render_m.group(0))

cooldown_render_m = re.search(r'function\s+renderCooldown[^\)]*\)\{[^\}]+\}', html_text)
if cooldown_render_m:
    print("\nrenderCooldown:")
    print(cooldown_render_m.group(0))

# 4. Check exercise image map implementation in index.html
ex_img_fns = re.findall(r'function\s+(?:loadExerciseImageMap|saveExerciseImage|getExerciseImage|openExerciseImageModal)[^{]+\{.*?\n\}', html_text, re.DOTALL)
print(f"\nFound {len(ex_img_fns)} exercise image functions:")
for fn in ex_img_fns:
    print(fn[:300] + "...\n")
