import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/Final_Master_Plan_Reconciliation_v3.md', 'r', encoding='utf-8') as f:
    text = f.read()

print("File size:", len(text), "chars")
lines = text.splitlines()
print("Total lines:", len(lines))

# Print headings
headings = [line for line in lines if line.startswith('#')]
print("\n--- Headings in Final_Master_Plan_Reconciliation_v3.md ---")
for h in headings[:30]:
    print(h)
