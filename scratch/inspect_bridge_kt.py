# -*- coding: utf-8 -*-
with open(r'android/app/src/main/java/com/zatoona/app/ZatoonaBridge.kt', 'r', encoding='utf-8') as f:
    text = f.read()

print(f"ZatoonaBridge.kt size: {len(text)} bytes")
print("First 40 lines:")
for line in text.split('\n')[:40]:
    print(line)
