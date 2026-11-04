import sys, os, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

sys.stdout.reconfigure(encoding='utf-8')

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=chrome_options)
driver.get("file:///" + os.path.abspath("index.html").replace("\\", "/"))
time.sleep(1)

# Check console errors
logs = driver.get_log("browser")
print("Console logs on load:")
for log in logs:
    print(log)

# Check if btnOpenThemeModal is bound on initial load
is_bound = driver.execute_script("""
    var btn = document.getElementById('btnOpenThemeModal');
    return {
        exists: !!btn,
        bound: btn ? btn.dataset.bound : null,
        onclick: btn && btn.onclick ? true : false
    };
""")
print("btnOpenThemeModal status on initial load:", is_bound)

# Navigate to 'meal' view, check if btnOpenThemeModal works
driver.execute_script("navigateTo('meal');")
time.sleep(0.5)

# Try clicking btnOpenThemeModal
click_res = driver.execute_script("""
    var btn = document.getElementById('btnOpenThemeModal');
    try {
        btn.click();
        var overlay = document.getElementById('themeModalOverlay');
        return {
            clicked: true,
            overlayHasOpen: overlay ? overlay.classList.contains('open') : false,
            overlayDisplay: overlay ? window.getComputedStyle(overlay).display : null,
            overlayOpacity: overlay ? window.getComputedStyle(overlay).opacity : null,
            overlayZIndex: overlay ? window.getComputedStyle(overlay).zIndex : null
        };
    } catch(e) {
        return { error: e.toString() };
    }
""")
print("Clicking btnOpenThemeModal result on meal view:", click_res)

# Now navigate to 'home' (which runs renderDashboardCards) and test again
driver.execute_script("navigateTo('home');")
time.sleep(0.5)

is_bound_after_home = driver.execute_script("""
    var btn = document.getElementById('btnOpenThemeModal');
    return {
        exists: !!btn,
        bound: btn ? btn.dataset.bound : null,
        onclick: btn && btn.onclick ? true : false
    };
""")
print("btnOpenThemeModal status after navigating to home:", is_bound_after_home)

click_res_home = driver.execute_script("""
    var btn = document.getElementById('btnOpenThemeModal');
    try {
        btn.click();
        var overlay = document.getElementById('themeModalOverlay');
        return {
            clicked: true,
            overlayHasOpen: overlay ? overlay.classList.contains('open') : false,
            overlayDisplay: overlay ? window.getComputedStyle(overlay).display : null,
            overlayOpacity: overlay ? window.getComputedStyle(overlay).opacity : null,
            overlayZIndex: overlay ? window.getComputedStyle(overlay).zIndex : null
        };
    } catch(e) {
        return { error: e.toString() };
    }
""")
print("Clicking btnOpenThemeModal after navigating to home:", click_res_home)

driver.quit()
