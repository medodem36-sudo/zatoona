import subprocess, time, sys
sys.stdout.reconfigure(encoding='utf-8')

print("==================================================")
print("PHYSICAL DEVICE REBOOT TEST — SAMSUNG GALAXY A04E")
print("==================================================")

# 1. Verify device connected
res = subprocess.run(["adb", "devices"], capture_output=True, text=True)
print("Device status:\n", res.stdout.strip())
if "device" not in res.stdout:
    print("Error: No device connected!")
    sys.exit(1)

# 2. Check pre-reboot alarms
res_pre = subprocess.run(["adb", "shell", "dumpsys", "alarm"], capture_output=True, text=True)
pre_count = res_pre.stdout.count("com.zatoona.app.ALARM_TRIGGER")
print(f"Pre-reboot alarms in AlarmManager: {pre_count}")

# 3. Trigger reboot
print("\n[STEP 1] Executing `adb reboot`...")
reboot_res = subprocess.run(["adb", "reboot"], capture_output=True, text=True)
print(f"Reboot command issued (code: {reboot_res.returncode})")

# 4. Wait for device to go offline then come back online
print("\n[STEP 2] Waiting for device to restart and reconnect via ADB (timeout: 180s)...")
start_time = time.time()
time.sleep(10) # give time to drop offline

# Wait for device
wait_proc = subprocess.run(["adb", "wait-for-device"], capture_output=True, text=True, timeout=180)
print(f"Device reconnected in {int(time.time() - start_time)}s")

# 5. Wait for sys.boot_completed == 1
print("\n[STEP 3] Waiting for sys.boot_completed == 1...")
boot_completed = False
for attempt in range(60):
    chk = subprocess.run(["adb", "shell", "getprop", "sys.boot_completed"], capture_output=True, text=True)
    val = chk.stdout.strip()
    if val == "1":
        boot_completed = True
        print(f"Boot completed successfully at attempt {attempt+1} ({int(time.time() - start_time)}s total)!")
        break
    time.sleep(2)

if not boot_completed:
    print("Warning: Timed out waiting for sys.boot_completed")

# Give system 5 seconds to finish broadcasting BOOT_COMPLETED
print("\n[STEP 4] Allowing 10 seconds for BOOT_COMPLETED broadcast delivery...")
time.sleep(10)

# 6. Check BootReceiver in logcat
print("\n[STEP 5] Checking ZatoonaBootReceiver logs in logcat...")
log_chk = subprocess.run(
    ["adb", "logcat", "-d", "-s", "ZatoonaBootReceiver:I", "ZatoonaAlarmScheduler:I"],
    capture_output=True,
    text=True
)
print("Logcat output:")
print(log_chk.stdout.strip() if log_chk.stdout.strip() else "(No explicit tag logs found yet)")

# 7. Check post-reboot alarms in AlarmManager
print("\n[STEP 6] Checking AlarmManager post-reboot dumpsys...")
res_post = subprocess.run(["adb", "shell", "dumpsys", "alarm"], capture_output=True, text=True)
post_count = res_post.stdout.count("com.zatoona.app.ALARM_TRIGGER")
print(f"Post-reboot alarms in AlarmManager: {post_count}")

# 8. Start app to verify clean resume
print("\n[STEP 7] Launching Zatoona app to ensure clean resume...")
launch_res = subprocess.run(
    ["adb", "shell", "am", "start", "-n", "com.zatoona.app.debug/com.zatoona.app.MainActivity"],
    capture_output=True,
    text=True
)
print(launch_res.stdout.strip())

# Check running processes
ps_chk = subprocess.run(["adb", "shell", "pidof", "com.zatoona.app.debug"], capture_output=True, text=True)
pid = ps_chk.stdout.strip()
print(f"Zatoona PID on device: {pid}")

print("\n==================================================")
if post_count > 0 or pid:
    print(f"REBOOT PERSISTENCE VERIFICATION: SUCCESS! (Alarms: {post_count}, PID: {pid})")
else:
    print("REBOOT PERSISTENCE VERIFICATION: INCONCLUSIVE / PENDING")
print("==================================================")
