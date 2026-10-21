import os, sys, hashlib, datetime, re

sys.stdout.reconfigure(encoding='utf-8')

# Ensure we're in repo
repo_dir = r"C:\Users\Lenovo\Documents\GitHub\zatoona"
os.chdir(repo_dir)

report_path = os.path.join(repo_dir, "scratch", "Master_Plan_Reconciliation_Audit_v2.md")

# Gather all data dynamically
# File metadata
files = ['index.html', 'zatoona.html', 'sw.js', 'manifest.json']
meta = {}
for f in files:
    size = os.path.getsize(f)
    mtime = datetime.datetime.fromtimestamp(os.path.getmtime(f)).strftime('%Y-%m-%d %H:%M:%S')
    with open(f, 'rb') as fp:
        h = hashlib.sha256(fp.read()).hexdigest()
    with open(f, 'r', encoding='utf-8') as fp:
        lines = len(fp.readlines())
    meta[f] = {'size': size, 'mtime': mtime, 'hash': h, 'lines': lines}

print("File metadata collected.")
