# -*- coding: utf-8 -*-
import winreg
import sys
sys.stdout.reconfigure(encoding='utf-8')

print("=== SEARCHING WINDOWS REGISTRY FOR ANDROID / GOOGLE INSTALLATIONS ===")

def search_uninstall(hive, hive_name, subkey):
    try:
        with winreg.OpenKey(hive, subkey) as key:
            num_subkeys = winreg.QueryInfoKey(key)[0]
            for i in range(num_subkeys):
                try:
                    kname = winreg.EnumKey(key, i)
                    with winreg.OpenKey(key, kname) as subk:
                        # read DisplayName, InstallLocation, DisplayVersion, UninstallString
                        try:
                            dname = winreg.QueryValueEx(subk, "DisplayName")[0]
                        except:
                            dname = ""
                        if any(term in dname.lower() for term in ['android', 'studio', 'sdk', 'gradle', 'google']):
                            try: loc = winreg.QueryValueEx(subk, "InstallLocation")[0]
                            except: loc = ""
                            try: ver = winreg.QueryValueEx(subk, "DisplayVersion")[0]
                            except: ver = ""
                            try: uninst = winreg.QueryValueEx(subk, "UninstallString")[0]
                            except: uninst = ""
                            print(f"[{hive_name}] {dname} (v{ver})")
                            print(f"   Location: {loc}")
                            print(f"   Uninstall: {uninst}")
                except Exception:
                    pass
    except Exception as e:
        print(f"Error opening {hive_name}\\{subkey}: {e}")

search_uninstall(winreg.HKEY_LOCAL_MACHINE, "HKLM_64", r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")
search_uninstall(winreg.HKEY_LOCAL_MACHINE, "HKLM_32", r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall")
search_uninstall(winreg.HKEY_CURRENT_USER, "HKCU", r"Software\Microsoft\Windows\CurrentVersion\Uninstall")

# Also check Android specific registry keys
for hive, hname in [(winreg.HKEY_LOCAL_MACHINE, "HKLM"), (winreg.HKEY_CURRENT_USER, "HKCU")]:
    for path in [r"SOFTWARE\Android Studio", r"SOFTWARE\Android SDK Tools", r"SOFTWARE\Google\Android Studio"]:
        try:
            with winreg.OpenKey(hive, path) as k:
                print(f"[FOUND REG KEY]: {hname}\\{path}")
                num_vals = winreg.QueryInfoKey(k)[1]
                for i in range(num_vals):
                    print("  ", winreg.EnumValue(k, i))
        except:
            pass
