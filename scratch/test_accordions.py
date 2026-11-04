import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# find views
views = re.findall(r'<div[^>]*id=["\']([a-zA-Z0-9]+View)["\'][^>]*>', html)
for v in views:
    m = re.search(r'(<div[^>]*id=["\']' + v + r'["\'][^>]*>.*?)(?=<div[^>]*id=["\'][a-zA-Z0-9]+View["\']|\Z)', html, re.DOTALL)
    if m:
        c = m.group(1)
        titles = re.findall(r'<div[^>]*class=["\'][^"\']*section-title[^"\']*["\'][^>]*>(.*?)</div>', c)
        if titles:
            print(f"{v}: {len(titles)} section titles")
            for t in titles[:3]:
                print(f"   - {re.sub(r'<[^>]+>', '', t).strip()}")
