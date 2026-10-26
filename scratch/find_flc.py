import zipfile, os

lib_dir = r"C:\Users\Lenovo\AppData\Local\Gradle\gradle-8.5\lib"
for f in os.listdir(lib_dir):
    if f.endswith(".jar"):
        zp = os.path.join(lib_dir, f)
        try:
            with zipfile.ZipFile(zp) as z:
                for name in z.namelist():
                    if "FileLockCommunicator" in name:
                        print(f"Found in {f}: {name}")
        except:
            pass
