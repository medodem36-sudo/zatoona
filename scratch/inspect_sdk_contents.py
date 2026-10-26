# -*- coding: utf-8 -*-
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')

sdk_dir = r"C:\Users\Lenovo\AppData\Local\Android\Sdk"
print(f"Listing {sdk_dir}:")
if os.path.exists(sdk_dir):
    for item in os.listdir(sdk_dir):
        sub = os.path.join(sdk_dir, item)
        print(f"  {item}/")
        if os.path.isdir(sub):
            for sub_item in os.listdir(sub)[:10]:
                print(f"    {sub_item}")
else:
    print("Does not exist!")
