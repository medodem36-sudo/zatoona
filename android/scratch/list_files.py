import subprocess

cmd = ['adb', '-s', 'R8YWA13G7WM', 'shell', 'run-as com.zatoona.app.debug ls -la "app_webview/Default/Local Storage/leveldb"']
out = subprocess.check_output(cmd).decode('utf-8', errors='ignore')
print(out)
