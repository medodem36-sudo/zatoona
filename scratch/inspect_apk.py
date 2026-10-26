import zipfile
import os

apk_path = r"C:\Users\Lenovo\Documents\GitHub\zatoona\android\app\build\outputs\apk\debug\app-debug.apk"
print(f"APK Size: {os.path.getsize(apk_path)} bytes")

with zipfile.ZipFile(apk_path, 'r') as z:
    names = z.namelist()
    print(f"Total entries in APK: {len(names)}")
    
    dex_files = [n for n in names if n.endswith('.dex')]
    print(f"Dex files: {dex_files}")
    
    asset_files = [n for n in names if n.startswith('assets/')]
    print(f"Total assets in APK: {len(asset_files)}")
    print(f"Sample assets: {asset_files[:10]}")
    
    res_files = [n for n in names if 'ic_launcher' in n]
    print(f"Launcher icon files: {res_files}")
    
    has_manifest = 'AndroidManifest.xml' in names
    has_resources_arsc = 'resources.arsc' in names
    print(f"AndroidManifest.xml present: {has_manifest}")
    print(f"resources.arsc present: {has_resources_arsc}")
