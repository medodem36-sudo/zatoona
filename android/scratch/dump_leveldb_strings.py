import subprocess

cmd = ['adb', '-s', 'R8YWA13G7WM', 'exec-out', "run-as com.zatoona.app.debug cat 'app_webview/Default/Local Storage/leveldb/000003.log'"]
res = subprocess.run(cmd, stdout=subprocess.PIPE)
raw = res.stdout

print(f"Total bytes: {len(raw)}")

# Search for any string containing 'rem' or 'zatoona'
for i in range(len(raw) - 10):
    chunk = raw[i:i+40]
    # Check if printable ascii
    printable = "".join([chr(b) if 32 <= b <= 126 else "." for b in chunk])
    if "zatoona" in printable.lower() or "remind" in printable.lower() or "water" in printable.lower() or "sleep" in printable.lower():
        print(f"Offset {i}: {printable}")
