import os
import shutil

src_root = r"C:\Users\Lenovo\Documents\GitHub\zatoona"
dest_assets = os.path.join(src_root, "android", "app", "src", "main", "assets")

os.makedirs(dest_assets, exist_ok=True)

# Copy index.html
shutil.copy2(os.path.join(src_root, "index.html"), os.path.join(dest_assets, "index.html"))
print("Copied index.html")

# Copy manifest.json
shutil.copy2(os.path.join(src_root, "manifest.json"), os.path.join(dest_assets, "manifest.json"))
print("Copied manifest.json")

# Copy sw.js
shutil.copy2(os.path.join(src_root, "sw.js"), os.path.join(dest_assets, "sw.js"))
print("Copied sw.js")

# Copy assets/ directory
dest_assets_dir = os.path.join(dest_assets, "assets")
if os.path.exists(dest_assets_dir):
    shutil.rmtree(dest_assets_dir)
shutil.copytree(os.path.join(src_root, "assets"), dest_assets_dir)
print("Copied assets/ directory")

# Copy icons/ directory
dest_icons_dir = os.path.join(dest_assets, "icons")
if os.path.exists(dest_icons_dir):
    shutil.rmtree(dest_icons_dir)
shutil.copytree(os.path.join(src_root, "icons"), dest_icons_dir)
print("Copied icons/ directory")

print("All PWA assets successfully synchronized to android/app/src/main/assets!")
