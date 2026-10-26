import hashlib
import filecmp

files = [
    "index.html",
    "zatoona.html",
    "sw.js",
    "assets/data/exercise-catalog.js",
    "manifest.json"
]

print("--- SHA-256 Checksums ---")
for f in files:
    with open(f, 'rb') as fp:
        h = hashlib.sha256(fp.read()).hexdigest()
    print(f"{f}: {h}")

parity = filecmp.cmp("index.html", "zatoona.html", shallow=False)
print(f"\nBinary Parity (index.html == zatoona.html): {parity}")
