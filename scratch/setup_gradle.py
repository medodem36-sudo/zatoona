# -*- coding: utf-8 -*-
import urllib.request
import os
import zipfile
import sys
import time

DEST_DIR = r"C:\Users\Lenovo\AppData\Local\Gradle"
ZIP_PATH = os.path.join(DEST_DIR, "gradle-8.5-bin.zip")
EXTRACT_DIR = os.path.join(DEST_DIR, "gradle-8.5")

os.makedirs(DEST_DIR, exist_ok=True)

if os.path.exists(os.path.join(EXTRACT_DIR, "bin", "gradle.bat")):
    print("Gradle 8.5 already extracted and ready!")
    sys.exit(0)

url = "https://services.gradle.org/distributions/gradle-8.5-bin.zip"
print(f"Downloading {url} to {ZIP_PATH}...")

t0 = time.time()
def reporthook(count, block_size, total_size):
    if count % 1000 == 0:
        percent = int(count * block_size * 100 / total_size)
        mb = (count * block_size) / (1024 * 1024)
        total_mb = total_size / (1024 * 1024)
        print(f"  Downloaded {mb:.1f} / {total_mb:.1f} MB ({percent}%)")

urllib.request.urlretrieve(url, ZIP_PATH, reporthook)
print(f"Download completed in {time.time() - t0:.1f}s")

print("Extracting Gradle zip...")
with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
    zip_ref.extractall(DEST_DIR)

print("Extraction completed!")
if os.path.exists(ZIP_PATH):
    os.remove(ZIP_PATH)
    print("Removed temporary zip.")

gradle_bat = os.path.join(EXTRACT_DIR, "bin", "gradle.bat")
print(f"Gradle bat exists: {os.path.exists(gradle_bat)}")
