import os
import shutil

src_icon = r"C:\Users\Lenovo\Documents\GitHub\zatoona\icons\icon-192.png"
src_round = r"C:\Users\Lenovo\Documents\GitHub\zatoona\icons\icon-192.png"
res_dir = r"C:\Users\Lenovo\Documents\GitHub\zatoona\android\app\src\main\res"

densities = ["mdpi", "hdpi", "xhdpi", "xxhdpi", "xxxhdpi"]
for d in densities:
    target_dir = os.path.join(res_dir, f"mipmap-{d}")
    os.makedirs(target_dir, exist_ok=True)
    shutil.copy2(src_icon, os.path.join(target_dir, "ic_launcher.png"))
    shutil.copy2(src_round, os.path.join(target_dir, "ic_launcher_round.png"))
    print(f"Created icons for mipmap-{d}")

print("Mipmap setup complete!")
