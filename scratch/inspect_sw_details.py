# -*- coding: utf-8 -*-
import sys, re

sys.stdout.reconfigure(encoding='utf-8')

with open('sw.js', 'r', encoding='utf-8') as f:
    sw_text = f.read()

print('sw.js length:', len(sw_text))

# Search for CACHE_VERSION
m_ver = re.search(r'const\s+CACHE_VERSION\s*=\s*[\'"]([^\'"]+)[\'"]', sw_text)
if m_ver:
    print('CACHE_VERSION:', m_ver.group(0))

# Search for SHELL_ASSETS
m_assets = re.search(r'const\s+SHELL_ASSETS\s*=\s*(\[.*?\]);', sw_text, re.DOTALL)
if m_assets:
    print('SHELL_ASSETS:\n', m_assets.group(0)[:800])

# Search for VALID_MODES
m_modes = re.search(r'VALID_MODES\s*=\s*(\[.*?\]);', sw_text, re.DOTALL)
if m_modes:
    print('VALID_MODES:\n', m_modes.group(0))
