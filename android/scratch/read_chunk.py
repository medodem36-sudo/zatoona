import subprocess

cmd = ['adb', '-s', 'R8YWA13G7WM', 'exec-out', "run-as com.zatoona.app.debug cat 'app_webview/Default/Local Storage/leveldb/000003.log'"]
res = subprocess.run(cmd, stdout=subprocess.PIPE)
raw = res.stdout

# Look around offset 31140
chunk = raw[31140:32097]
# Filter printable
print("".join([chr(b) if 32 <= b <= 126 or b in (10, 13) else " " for b in chunk]))
