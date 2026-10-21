# -*- coding: utf-8 -*-
import os, sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

sys.stdout.reconfigure(encoding='utf-8')

repo = r"C:\Users\Lenovo\Documents\GitHub\zatoona"
preview_html = os.path.join(repo, "scratch", "svg_preview.html")

html_content = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SVG Warmup & Cooldown Preview</title>
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
    --good: #16a34a;
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
  .wc-card{background:var(--card); border:1px solid var(--line); border-radius:var(--radius); box-shadow:var(--shadow); margin-bottom:12px; overflow:hidden; display:flex; align-items:stretch;}
  .wc-photo{flex:0 0 118px; width:118px; height:118px; background:var(--bg-2); position:relative; overflow:hidden;}
  .wc-photo img{width:100%; height:100%; object-fit:contain; background:#fff;}
  .wc-body{flex:1; display:flex; align-items:center; justify-content:space-between; gap:8px; padding:10px 12px;}
  .wc-text{font-size:.85rem; line-height:1.6;}
  .wc-credit{position:absolute; bottom:2px; left:2px; background:rgba(255,255,255,.9); color:#1e293b; font-size:.55rem; padding:1px 5px; border-radius:999px; backdrop-filter:blur(4px);}
  .tbtn {
    width: 32px; height: 32px; border-radius: 8px; border: 1px solid var(--line); background: var(--bg-2);
    color: var(--accent); font-weight: bold; cursor: pointer;
  }
  h2 { font-size: 1.1rem; color: var(--accent); margin: 16px 0 8px; border-bottom: 2px solid var(--line); padding-bottom: 4px; }
</style>
</head>
<body>
<div class="container">
  <h1>معاينة صور الإحماء والتهدئة (أصلية محلية - رجال فقط)</h1>
  
  <h2>تمارين الإحماء (Warm-up)</h2>
  <div class="wc-card">
    <div class="wc-photo"><img src="../assets/images/warmup/warmup-01-cardio.svg" alt="Cardio"><span class="wc-credit">رسم أصلي محلي</span></div>
    <div class="wc-body"><div class="wc-text">5 دقايق مشي سريع / جري خفيف / دراجة أو نط حبل — عشان تعرق شوية ويزيد نبضك</div><button class="tbtn">✓</button></div>
  </div>
  <div class="wc-card">
    <div class="wc-photo"><img src="../assets/images/warmup/warmup-02-arm-circles.svg" alt="Arm Circles"><span class="wc-credit">رسم أصلي محلي</span></div>
    <div class="wc-body"><div class="wc-text">دوران الذراعين للأمام وللخلف — 15 مرة كل اتجاه</div><button class="tbtn">✓</button></div>
  </div>
  <div class="wc-card">
    <div class="wc-photo"><img src="../assets/images/warmup/warmup-03-leg-swings.svg" alt="Leg Swings"><span class="wc-credit">رسم أصلي محلي</span></div>
    <div class="wc-body"><div class="wc-text">تأرجح الرجل للأمام والخلف وجانبي — 10 لكل رجل</div><button class="tbtn">✓</button></div>
  </div>
  <div class="wc-card">
    <div class="wc-photo"><img src="../assets/images/warmup/warmup-04-hip-circles.svg" alt="Hip Circles"><span class="wc-credit">رسم أصلي محلي</span></div>
    <div class="wc-body"><div class="wc-text">دوران الحوض — 10 لكل اتجاه</div><button class="tbtn">✓</button></div>
  </div>
  <div class="wc-card">
    <div class="wc-photo"><img src="../assets/images/warmup/warmup-05-bodyweight-squat.svg" alt="Squat"><span class="wc-credit">رسم أصلي محلي</span></div>
    <div class="wc-body"><div class="wc-text">سكوات وزن الجسم بطيء ومتحكم — 10 مرات من غير وزن</div><button class="tbtn">✓</button></div>
  </div>
  <div class="wc-card">
    <div class="wc-photo"><img src="../assets/images/warmup/warmup-06-warmup-set.svg" alt="Warmup Set"><span class="wc-credit">رسم أصلي محلي</span></div>
    <div class="wc-body"><div class="wc-text">سيت تسخين خفيف (نص الوزن أو أقل) لأول تمرين في اليوم</div><button class="tbtn">✓</button></div>
  </div>

  <h2>تمارين التهدئة (Cool-down)</h2>
  <div class="wc-card">
    <div class="wc-photo"><img src="../assets/images/cooldown/cooldown-01-shoulder-stretch.svg" alt="Shoulder Stretch"><span class="wc-credit">رسم أصلي محلي</span></div>
    <div class="wc-body"><div class="wc-text">استرتش الكتف: مد دراعك أفقي قدام صدرك وامسكه بالدراع التانية — 20-30 ثانية لكل جانب</div><button class="tbtn">✓</button></div>
  </div>
  <div class="wc-card">
    <div class="wc-photo"><img src="../assets/images/cooldown/cooldown-02-chest-stretch.svg" alt="Chest Stretch"><span class="wc-credit">رسم أصلي محلي</span></div>
    <div class="wc-body"><div class="wc-text">استرتش الصدر: حط دراعك على الحيط بزاوية 90 درجة ولف جسمك بعيد عنه برفق</div><button class="tbtn">✓</button></div>
  </div>
  <div class="wc-card">
    <div class="wc-photo"><img src="../assets/images/cooldown/cooldown-03-lower-back-stretch.svg" alt="Back Stretch"><span class="wc-credit">رسم أصلي محلي</span></div>
    <div class="wc-body"><div class="wc-text">استرتش أسفل الظهر والوراك: نايم على ضهرك واسحب ركبة لصدرك — 20-30 ثانية لكل رجل</div><button class="tbtn">✓</button></div>
  </div>
  <div class="wc-card">
    <div class="wc-photo"><img src="../assets/images/cooldown/cooldown-04-hamstring-stretch.svg" alt="Hamstring Stretch"><span class="wc-credit">رسم أصلي محلي</span></div>
    <div class="wc-body"><div class="wc-text">استرتش الفخذ الخلفي: قاعد ومد رجل واحدة وحاول توصل لصوابعك برفق</div><button class="tbtn">✓</button></div>
  </div>
  <div class="wc-card">
    <div class="wc-photo"><img src="../assets/images/cooldown/cooldown-05-quad-stretch.svg" alt="Quad Stretch"><span class="wc-credit">رسم أصلي محلي</span></div>
    <div class="wc-body"><div class="wc-text">استرتش الفخذ الأمامي: واقف، امسك كاحلك واسحبه لورا لحد ما تحس بشد</div><button class="tbtn">✓</button></div>
  </div>
  <div class="wc-card">
    <div class="wc-photo"><img src="../assets/images/cooldown/cooldown-06-calm-walk.svg" alt="Calm Walk"><span class="wc-credit">رسم أصلي محلي</span></div>
    <div class="wc-body"><div class="wc-text">مشي هادي 3-5 دقايق عشان نبضك يرجع لطبيعته تدريجيًا</div><button class="tbtn">✓</button></div>
  </div>
</div>
</body>
</html>"""

with open(preview_html, "w", encoding="utf-8") as f:
    f.write(html_content)

opts = Options()
opts.add_argument('--headless=new')
opts.add_argument('--window-size=400,1800')
driver = webdriver.Chrome(options=opts)
driver.get("file:///" + preview_html.replace("\\", "/"))

# Check all images loaded
imgs = driver.find_elements("css selector", ".wc-photo img")
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

# Test 375px viewport (mobile) for overflow
driver.set_window_size(375, 800)
scroll_width = driver.execute_script("return document.documentElement.scrollWidth;")
client_width = driver.execute_script("return document.documentElement.clientWidth;")
print(f"Viewport 375px: clientWidth={client_width}, scrollWidth={scroll_width}")
assert scroll_width <= client_width, "Horizontal overflow detected at 375px!"

# Take screenshot
screenshot_path = os.path.join(repo, "scratch", "svg_preview_screenshot.png")
driver.set_window_size(450, 2000)
driver.save_screenshot(screenshot_path)
print(f"Screenshot saved at: {screenshot_path}")

driver.quit()
print("ALL SVG PREVIEW TESTS PASSED!")
