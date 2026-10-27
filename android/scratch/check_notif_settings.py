import subprocess

cmd = ['adb', '-s', 'R8YWA13G7WM', 'exec-out', "run-as com.zatoona.app.debug cat 'app_webview/Default/Local Storage/leveldb/000003.log'"]
res = subprocess.run(cmd, stdout=subprocess.PIPE)
raw = res.stdout

# search for notificationSettings
for i in range(len(raw) - 20):
    if b'notification' in raw[i:i+30].lower():
        chunk = raw[i-10:i+150]
        printable = "".join([chr(b) if 32 <= b <= 126 else " " for b in chunk])
        print("At", i, ":", printable)
