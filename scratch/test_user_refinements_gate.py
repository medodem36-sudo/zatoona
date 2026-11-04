import os, sys, re, json

sys.stdout.reconfigure(encoding='utf-8')

print("="*60)
print("TESTING USER REFINEMENTS & ANDROID WIDGET GATES")
print("="*60)

passed = 0
failed = 0

def check(title, condition, details=""):
    global passed, failed
    if condition:
        passed += 1
        print(f"  [PASS] {title}")
    else:
        failed += 1
        print(f"  [FAIL] {title} - {details}")

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Swipe view-pager disabled
check("Swipe view-pager is disabled by default", "let swipeNavEnabled = false;" in html)

# 2. Dynamic status capsule tap dismiss
check("Capsule has dismiss logic on click", "capsuleDismissedText = content.textContent;" in html)
check("Capsule updater checks dismissed state", "if(capsuleDismissedText === currentText)" in html)

# 3. Theme button removed from header and placed in settings
header_match = re.search(r'<header[^>]*id=["\']appHeader["\'][^>]*>(.*?)</header>', html, re.DOTALL)
check("appHeader found", header_match is not None)
if header_match:
    header_content = header_match.group(1)
    check("appHeader does NOT contain btnOpenThemeModal", "btnOpenThemeModal" not in header_content)
    check("appHeader does NOT contain themeToggleBtn", "themeToggleBtn" not in header_content)

settings_match = re.search(r'<div[^>]*id=["\']settingsView["\'][^>]*>(.*?)</div>\s*<!-- \d+\. Appearance', html, re.DOTALL)
check("settingsView contains btnOpenThemeModal", 'id="btnOpenThemeModal"' in html[html.find('id="settingsView"'):])

# 4. Home Page cleanup
# modesBar is hidden
check("modesBar has display none CSS", "#modesBar { display: none !important; }" in html)

# zatoonaWrappedCard in overviewView, not homeHero
hero_match = re.search(r'<div[^>]*id=["\']homeHero["\'][^>]*>(.*?)</div>\s*<div[^>]*id=["\']modesBar["\']', html, re.DOTALL)
if hero_match:
    hero_text = hero_match.group(1)
    check("homeHero does NOT contain zatoonaWrappedCard", "zatoonaWrappedCard" not in hero_text)
    check("homeHero DOES contain aiCoachCard", "aiCoachCard" in hero_text)

overview_match = re.search(r'<div[^>]*id=["\']overviewView["\'][^>]*>(.*?)(?=<div[^>]*id=["\'][a-zA-Z0-9]+View["\'])', html, re.DOTALL)
if overview_match:
    ov_text = overview_match.group(1)
    check("overviewView DOES contain zatoonaWrappedCard", "zatoonaWrappedCard" in ov_text)

# 5. Offline 7-Day Prayer Calculation
check("calculateOfflinePrayerTimes exists", "function calculateOfflinePrayerTimes(" in html)
check("precalculateAndCache7DaysPrayer exists", "function precalculateAndCache7DaysPrayer(" in html)
check("EGYPT_CITY_COORDINATES exists", "const EGYPT_CITY_COORDINATES = {" in html)
check("ensurePrayerTimes falls back to offline calculation", "calculateOfflinePrayerTimes(city, iso)" in html)

# 6. Accordions
check("initSectionAccordions exists", "function initSectionAccordions(" in html)
check("collapsible-section-title CSS exists", ".section-title.collapsible-section-title" in html)
check("section-accordion-body CSS exists", ".section-accordion-body.collapsed" in html)

# 7. Android Widgets
check("WaterWidgetProvider.kt exists", os.path.exists("android/app/src/main/java/com/zatoona/app/WaterWidgetProvider.kt"))
check("widget_water.xml exists", os.path.exists("android/app/src/main/res/layout/widget_water.xml"))
check("widget_water_info.xml exists", os.path.exists("android/app/src/main/res/xml/widget_water_info.xml"))

check("ScheduleWidgetProvider.kt exists", os.path.exists("android/app/src/main/java/com/zatoona/app/ScheduleWidgetProvider.kt"))
check("widget_schedule.xml exists", os.path.exists("android/app/src/main/res/layout/widget_schedule.xml"))
check("widget_schedule_info.xml exists", os.path.exists("android/app/src/main/res/xml/widget_schedule_info.xml"))

check("widget_study.xml has chronometer", "widget_study_chronometer" in open("android/app/src/main/res/layout/widget_study.xml", encoding='utf-8').read())

# 8. Widget Resizing (minWidth=40dp, maxResizeWidth=480dp, maxResizeHeight=720dp)
all_info_files = [
    "widget_all_in_one_info.xml", "widget_daily_habits_info.xml", "widget_next_prayer_info.xml",
    "widget_quick_access_info.xml", "widget_study_info.xml", "widget_water_info.xml", "widget_schedule_info.xml"
]
for inf in all_info_files:
    path = os.path.join("android/app/src/main/res/xml", inf)
    txt = open(path, encoding='utf-8').read()
    check(f"{inf} supports 1x1 to 3x6 resize", 'minResizeWidth="40dp"' in txt and 'minResizeHeight="40dp"' in txt and 'maxResizeWidth="480dp"' in txt and 'maxResizeHeight="720dp"' in txt)

# 9. 3-Way HTML Parity
with open("zatoona.html", "r", encoding="utf-8") as fz:
    z_content = fz.read()
with open("android/app/src/main/assets/index.html", "r", encoding="utf-8") as fa:
    a_content = fa.read()

check("index.html and zatoona.html identical", html == z_content)
check("index.html and android asset index.html identical", html == a_content)

print("\n" + "="*60)
print(f"SUMMARY: {passed} PASSED, {failed} FAILED")
print("="*60)

if failed > 0:
    sys.exit(1)
