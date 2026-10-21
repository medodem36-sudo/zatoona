# -*- coding: utf-8 -*-
import sys, re, os

sys.stdout.reconfigure(encoding='utf-8')

repo = r"C:\Users\Lenovo\Documents\GitHub\zatoona"
with open(os.path.join(repo, "index.html"), "r", encoding="utf-8") as f:
    text = f.read()

m_nav = re.search(r'const NAV_MODES\s*=\s*\[(.*?)\];', text, re.DOTALL)
if m_nav:
    print('NAV_MODES:\n', m_nav.group(0))

views = re.findall(r'id=["\']([a-zA-Z0-9_-]+View)["\']', text)
print('Views found:\n', views)

# Check navigateTo function
idx_nav = text.find('function navigateTo(')
if idx_nav != -1:
    print('\nnavigateTo function:\n', text[idx_nav:idx_nav+600])

# Check applyMode function
idx_mode = text.find('function applyMode(')
if idx_mode != -1:
    print('\napplyMode function:\n', text[idx_mode:idx_mode+600])

# Check drawer links
m_drawer = re.search(r'id=["\']drawerNav["\'](.*?)</ul>', text, re.DOTALL)
if m_drawer:
    print('\nDrawer links:\n', m_drawer.group(0))
