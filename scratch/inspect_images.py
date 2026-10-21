# -*- coding: utf-8 -*-
import sys, re, os

sys.stdout.reconfigure(encoding='utf-8')

repo = r"C:\Users\Lenovo\Documents\GitHub\zatoona"
with open(os.path.join(repo, "index.html"), "r", encoding="utf-8") as f:
    text = f.read()

print("--- 1. Search for img tags in index.html ---")
img_tags = re.findall(r'<img[^>]+>', text)
for tag in set(img_tags):
    print("TAG:", tag)

print("\n--- 2. Search for external image URLs in index.html ---")
urls = re.findall(r'https?://[^\s"\'<>]+(?:jpg|png|gif|svg|jpeg|webp|Special:FilePath[^\s"\'<>]+)', text)
for u in sorted(set(urls)):
    print("URL:", u)

print("\n--- 3. Search in exercise-catalog.js ---")
catalog_path = os.path.join(repo, "assets", "data", "exercise-catalog.js")
if os.path.exists(catalog_path):
    with open(catalog_path, "r", encoding="utf-8") as f:
        cat_text = f.read()
    cat_urls = re.findall(r'https?://[^\s"\'<>]+(?:jpg|png|gif|svg|jpeg|webp)', cat_text)
    print("Catalog external image URLs count:", len(cat_urls))
    for u in set(cat_urls):
        print("Catalog URL:", u)

print("\n--- 4. Search in assets directory ---")
for root, dirs, files in os.walk(os.path.join(repo, "assets")):
    for file in files:
        if file.lower().endswith(('.jpg', '.png', '.gif', '.svg', '.webp')):
            print("Asset:", os.path.relpath(os.path.join(root, file), repo))
