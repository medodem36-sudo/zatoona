import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

report_path = 'scratch/Final_Master_Plan_Reconciliation_v4.md'
summary_path = 'scratch/Final_Master_Plan_Reconciliation_v4_Summary.md'

with open('scratch/generate_v4_reports.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Add report_path and summary_path at the top of generate_v4_reports.py
fix = """# -*- coding: utf-8 -*-
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

report_path = 'scratch/Final_Master_Plan_Reconciliation_v4.md'
summary_path = 'scratch/Final_Master_Plan_Reconciliation_v4_Summary.md'
"""
code = code.replace("""# -*- coding: utf-8 -*-
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')""", fix, 1)

with open('scratch/generate_v4_reports.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated generate_v4_reports.py")
