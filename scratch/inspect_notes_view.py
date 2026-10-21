# -*- coding: utf-8 -*-
import sys, re, os

sys.stdout.reconfigure(encoding='utf-8')

repo = r"C:\Users\Lenovo\Documents\GitHub\zatoona"
with open(os.path.join(repo, "index.html"), "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find('id="notesView"')
print('notesView found at:', idx)
print(text[idx-50:idx+600])

idx_enc = text.find('id="gymEncyclopediaModal"')
if idx_enc == -1:
    idx_enc = text.find('encyclopedia')
print('\nencyclopedia reference:\n', text[idx_enc-50:idx_enc+400])
