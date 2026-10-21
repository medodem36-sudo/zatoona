import os, sys, hashlib, datetime

sys.stdout.reconfigure(encoding='utf-8')

repo_dir = r"C:\Users\Lenovo\Documents\GitHub\zatoona"
report_file = os.path.join(repo_dir, "scratch", "Master_Plan_Reconciliation_Audit_v2.md")

print(f"Target report file: {report_file}")
