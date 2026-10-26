# -*- coding: utf-8 -*-
path = r"android/app/src/main/java/com/zatoona/app/ZatoonaBridge.kt"
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Replace any unescaped \- or similar
old_str = r'Regex("^[a-zA-Z0-9_\-:]+$")'
new_str = r'Regex("^[a-zA-Z0-9_\\-:]+$")'

if old_str in text:
    text = text.replace(old_str, new_str)
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)
    print("Cleaned regex escape.")
else:
    print("String not found or already clean.")
