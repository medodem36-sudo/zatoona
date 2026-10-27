import subprocess
import re
import json

def main():
    cmd = ['adb', '-s', 'R8YWA13G7WM', 'exec-out', "run-as com.zatoona.app.debug cat 'app_webview/Default/Local Storage/leveldb/000003.log'"]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("Stdout bytes:", len(res.stdout), "Stderr:", res.stderr.decode('utf-8', errors='ignore'))
    
    # search for reminders or json
    raw = res.stdout
    matches = re.findall(rb'\{[^{}]*"title"[^{}]*\}', raw)
    print("Found JSON object matches:", len(matches))
    for m in matches:
        try:
            print("Match:", m.decode('utf-8', errors='ignore'))
        except:
            pass

    # search for any occurrences of "rem-"
    rem_matches = re.findall(rb'rem-[a-zA-Z0-9]+', raw)
    print("Found rem-* IDs:", set(rem_matches))

if __name__ == '__main__':
    main()
