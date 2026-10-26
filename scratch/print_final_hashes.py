import hashlib
import os

files = ['index.html', 'zatoona.html', 'sw.js', 'manifest.json', 'assets/data/exercise-catalog.js']
for f in files:
    data = open(f, 'rb').read()
    h = hashlib.sha256(data).hexdigest().upper()
    print(f"{f}: {h} ({len(data)} bytes)")
