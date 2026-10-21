# -*- coding: utf-8 -*-
import os, sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

sys.stdout.reconfigure(encoding='utf-8')

repo = r"C:\Users\Lenovo\Documents\GitHub\zatoona"
preview_html = os.path.join(repo, "scratch", "ex_svg_preview.html")

html_content = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Exercise SVG Preview</title>
<style>
  :root {
    --card: #ffffff;
    --line: #e2e8f0;
    --radius: 12px;
    --shadow: 0 1px 3px rgba(0,0,0,0.05);
    --bg-2: #f8fafc;
    --text: #1e293b;
    --muted: #64748b;
    --accent: #176b4d;
  }
  body.dark {
    --card: #1e293b;
    --line: #334155;
    --bg-2: #0f172a;
    --text: #f8fafc;
    --muted: #94a3b8;
    background: #0f172a;
  }
  body {
    font-family: system-ui, sans-serif;
    background: #f1f5f9;
    color: var(--text);
    padding: 16px;
    margin: 0;
  }
  .container {
    max-width: 600px;
    margin: 0 auto;
  }
  .ex-card {
    background: var(--card);
    border: 1px solid var(--line);
    border-radius: var(--radius);
    margin-bottom: 16px;
    overflow: hidden;
  }
  .ex-photo{width:100%; height:200px; background:var(--bg-2); border-bottom:1px solid var(--line); position:relative; overflow:hidden;}
  .ex-photo img{width:100%; height:100%; object-fit:contain; object-position:center; background:#fff;}
  .ex-photo .credit{position:absolute; bottom:4px; left:6px; background:rgba(255,255,255,.9); color:var(--text); font-size:.62rem; padding:2px 7px; border-radius:999px; font-family:monospace;}
  .ex-body { padding: 12px; }
  .ex-name { font-weight: bold; font-size: 1rem; color: var(--accent); }
</style>
</head>
<body>
<div class="container">
  <h1>معاينة صور التمارين الافتراضية (A & B)</h1>
  
  <h2>Routine A</h2>
  <div class="ex-card">
    <div class="ex-photo"><img src="../assets/images/exercises/ex-a01-goblet-squat.svg" alt="Squat"><span class="credit">رسم أصلي محلي</span></div>
    <div class="ex-body"><div class="ex-name">سكوات بالدمبل (Goblet Squat)</div></div>
  </div>
  <div class="ex-card">
    <div class="ex-photo"><img src="../assets/images/exercises/ex-a02-bench-press.svg" alt="Bench"><span class="credit">رسم أصلي محلي</span></div>
    <div class="ex-body"><div class="ex-name">بنش برس بار / دمبل</div></div>
  </div>
  <div class="ex-card">
    <div class="ex-photo"><img src="../assets/images/exercises/ex-a03-lat-pulldown.svg" alt="Lat Pulldown"><span class="credit">رسم أصلي محلي</span></div>
    <div class="ex-body"><div class="ex-name">سحب لأسفل (Lat Pulldown) أو عقلة</div></div>
  </div>
  <div class="ex-card">
    <div class="ex-photo"><img src="../assets/images/exercises/ex-a04-overhead-press.svg" alt="Overhead Press"><span class="credit">رسم أصلي محلي</span></div>
    <div class="ex-body"><div class="ex-name">شولدر برس بالدمبل</div></div>
  </div>
  <div class="ex-card">
    <div class="ex-photo"><img src="../assets/images/exercises/ex-a05-plank.svg" alt="Plank"><span class="credit">رسم أصلي محلي</span></div>
    <div class="ex-body"><div class="ex-name">بلانك (Plank)</div></div>
  </div>
  <div class="ex-card">
    <div class="ex-photo"><img src="../assets/images/exercises/ex-a06-face-pull.svg" alt="Face Pull"><span class="credit">رسم أصلي محلي</span></div>
    <div class="ex-body"><div class="ex-name">فيس بول (Face Pull / Band Pull-Apart)</div></div>
  </div>

  <h2>Routine B</h2>
  <div class="ex-card">
    <div class="ex-photo"><img src="../assets/images/exercises/ex-b01-romanian-deadlift.svg" alt="RDL"><span class="credit">رسم أصلي محلي</span></div>
    <div class="ex-body"><div class="ex-name">ديدليفت روماني (Romanian Deadlift)</div></div>
  </div>
  <div class="ex-card">
    <div class="ex-photo"><img src="../assets/images/exercises/ex-b02-barbell-row.svg" alt="Row"><span class="credit">رسم أصلي محلي</span></div>
    <div class="ex-body"><div class="ex-name">رو بار (Barbell Bent-over Row)</div></div>
  </div>
  <div class="ex-card">
    <div class="ex-photo"><img src="../assets/images/exercises/ex-b03-push-up.svg" alt="Push-ups"><span class="credit">رسم أصلي محلي</span></div>
    <div class="ex-body"><div class="ex-name">ضغط (Push-ups)</div></div>
  </div>
  <div class="ex-card">
    <div class="ex-photo"><img src="../assets/images/exercises/ex-b04-pull-up.svg" alt="Pull-ups"><span class="credit">رسم أصلي محلي</span></div>
    <div class="ex-body"><div class="ex-name">عقلة (Pull-ups)</div></div>
  </div>
  <div class="ex-card">
    <div class="ex-photo"><img src="../assets/images/exercises/ex-b05-abdominal-crunch.svg" alt="Crunch"><span class="credit">رسم أصلي محلي</span></div>
    <div class="ex-body"><div class="ex-name">كرانش للبطن (Crunch)</div></div>
  </div>
  <div class="ex-card">
    <div class="ex-photo"><img src="../assets/images/exercises/ex-b06-lunges.svg" alt="Lunges"><span class="credit">رسم أصلي محلي</span></div>
    <div class="ex-body"><div class="ex-name">لنجز (Lunges)</div></div>
  </div>
</div>
</body>
</html>"""

with open(preview_html, "w", encoding="utf-8") as f:
    f.write(html_content)

opts = Options()
opts.add_argument('--headless=new')
opts.add_argument('--window-size=400,2400')
driver = webdriver.Chrome(options=opts)
driver.get("file:///" + preview_html.replace("\\", "/"))

imgs = driver.find_elements("css selector", ".ex-photo img")
print(f"Total preview images: {len(imgs)}")
broken_count = 0
for idx, img in enumerate(imgs):
    nw = driver.execute_script("return arguments[0].naturalWidth;", img)
    src = img.get_attribute("src")
    if nw == 0:
        print(f"FAILED: Image {idx} broke: {src}")
        broken_count += 1
    else:
        print(f"OK: Image {idx} loaded (naturalWidth={nw}): {os.path.basename(src)}")

assert broken_count == 0, f"{broken_count} images failed to load!"

driver.set_window_size(375, 800)
scroll_width = driver.execute_script("return document.documentElement.scrollWidth;")
client_width = driver.execute_script("return document.documentElement.clientWidth;")
print(f"Viewport 375px: clientWidth={client_width}, scrollWidth={scroll_width}")
assert scroll_width <= client_width, "Horizontal overflow at 375px!"

screenshot_path = os.path.join(repo, "scratch", "ex_svg_preview_screenshot.png")
driver.set_window_size(450, 2600)
driver.save_screenshot(screenshot_path)
print(f"Screenshot saved at: {screenshot_path}")

driver.quit()
print("ALL EXERCISE SVG PREVIEW TESTS PASSED!")
