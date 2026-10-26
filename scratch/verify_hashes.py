import hashlib

files = {
    'index.html': '10C7B5ACB7DFF16997F90421AD44A3AF3F98425FC65565F794635AD437A2A957',
    'zatoona.html': '10C7B5ACB7DFF16997F90421AD44A3AF3F98425FC65565F794635AD437A2A957',
    'sw.js': '7AB40099A5529823119CD5FB1A85AF88FAB26546FE2B8885D974B792063130C3',
    'assets/data/exercise-catalog.js': 'BC6320D1CA83A748F3F15722010388CDA2333FC7AEE3C267840AB6C42EDAAC26',
    'manifest.json': 'C872752E51F5B339BD3965370B5DF54B47CBAAAD398785F85D6453FD93C743E5'
}

all_match = True
for fpath, expected in files.items():
    with open(fpath, 'rb') as f:
        actual = hashlib.sha256(f.read()).hexdigest().upper()
    match = (actual == expected)
    if not match:
        all_match = False
    print(f"{'PASS' if match else 'FAIL'}: {fpath} -> {actual}")

print(f"\nALL MATCH: {all_match}")
