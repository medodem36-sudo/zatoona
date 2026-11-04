# -*- coding: utf-8 -*-
import hashlib
import shutil

INDEX_PATH = "index.html"
ZATOONA_PATH = "zatoona.html"
ANDROID_PATH = "android/app/src/main/assets/index.html"

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    lines = f.readlines()

clean_lines = [line.rstrip() + "\n" if line.endswith("\n") else line.rstrip() for line in lines]

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.writelines(clean_lines)

shutil.copyfile(INDEX_PATH, ZATOONA_PATH)
shutil.copyfile(INDEX_PATH, ANDROID_PATH)

def get_hash(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

h1 = get_hash(INDEX_PATH)
h2 = get_hash(ZATOONA_PATH)
h3 = get_hash(ANDROID_PATH)

print(f"Cleaned trailing whitespace.")
print(f"index.html SHA-256:   {h1}")
print(f"zatoona.html SHA-256: {h2}")
print(f"android asset SHA256: {h3}")
print("Parity match:", h1 == h2 == h3)
