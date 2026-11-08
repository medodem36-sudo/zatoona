import hashlib
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

sys.stdout.reconfigure(encoding='utf-8')

print("=" * 80)
print("TEST SUITE: AI COACH EGYPTIAN FLUENCY & EMOJI-FREE SPEECH SYNTHESIS")
print("=" * 80)

def check(name, condition):
    if condition:
        print(f"  [PASS] {name}")
    else:
        print(f"  [FAIL] {name}")
        sys.exit(1)

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Structural Checks in HTML
print("\n--- 1. Structural & Prompt Checks ---")
check("has cleanTextForSpeechSynthesis definition", "function cleanTextForSpeechSynthesis(" in html)
check("exports cleanTextForSpeechSynthesis on window", "window.cleanTextForSpeechSynthesis = cleanTextForSpeechSynthesis" in html)
check("speakAiCoachResponse uses cleanTextForSpeechSynthesis", "const clean = cleanTextForSpeechSynthesis(rawText);" in html)
check("speakAiCoachResponse sets rate to 1.0", "utterance.rate = 1.0;" in html)
check("speakAiCoachResponse sets lang to ar-EG", "utterance.lang = 'ar-EG';" in html)
check("Gemini system prompt enforces 100% Egyptian dialect", "اتكلم بلهجة مصرية عامية 100% طبيعية وسلسة" in html)
check("Gemini system prompt forbids robotic speech", "بلاش تماماً أي كلام معرب آلي أو فصحى مصطنعة" in html)
check("Gemini system prompt specifies voice reading readability", "كلامك بيتقرأ بصوت عالي للمستخدم" in html)

# 2. Action confirmation texts in Egyptian Arabic
print("\n--- 2. Egyptian Action Confirmations ---")
check("Water action returns natural Egyptian wording", "عاش يا وحش! سجلتلك" in html and "ترطيب جسمك في الجون" in html)
check("Prayer action returns brotherly Egyptian wording", "تقبل الله منك يا صاحبي!" in html)
check("Workout action returns energetic Egyptian wording", "عاش يا وحش! 🏋️‍♂️ سجلتلك **تمرين النهاردة**" in html)
check("Habit action returns natural Egyptian wording", "تسلم إيدك يا بطل! علمتلك على عادة" in html)
check("Micro-tasks action returns natural Egyptian wording", "عشان نكسر حاجز التسويف" in html)
check("Book zatoona action returns natural Egyptian wording", "جبتلك زتونة كتاب" in html)

# 3. Headless Chrome Execution Test for cleanTextForSpeechSynthesis
print("\n--- 3. Headless Chrome Runtime Execution ---")
opts = Options()
opts.add_argument('--headless=new')
opts.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=opts)
driver.get(r'file:///C:/Users/Lenovo/Documents/GitHub/zatoona/index.html')

js_test = r"""
const sampleWithEmojis = `عاش يا وحش! سجلتلك كوباية مية دلوقتي 💧 🕌 🤖 🌙 ✨ 🟢 🏋️‍♂️ 🥪 🧠 🦾 🧘‍♂️ 💡 📖 ☀️ 🌇 🚀 🎯 ✅
كدة بقوا **5 كوبايات** النهاردة.. كمل يا بطل ترطيب جسمك في الجون!
[تم التنفيذ والتحديث في التطبيق تلقائياً ✅]
<<<ACTION:{"type":"log_water","delta":1}>>>`;

const cleaned = window.cleanTextForSpeechSynthesis(sampleWithEmojis);
return {
  cleaned: cleaned,
  hasAction: cleaned.includes('<<<ACTION'),
  hasSystemTag: cleaned.includes('[تم التنفيذ'),
  hasAsterisk: cleaned.includes('*'),
  hasEmojis: /[\u{10000}-\u{10FFFF}\u{2600}-\u{27BF}\p{Extended_Pictographic}]/gu.test(cleaned)
};
"""

res = driver.execute_script(js_test)
print(f"  Cleaned text result:\n    \"{res['cleaned']}\"")
check("cleanTextForSpeechSynthesis stripped ACTION block", not res['hasAction'])
check("cleanTextForSpeechSynthesis stripped system execution tag", not res['hasSystemTag'])
check("cleanTextForSpeechSynthesis stripped markdown bold asterisks", not res['hasAsterisk'])
check("cleanTextForSpeechSynthesis stripped ALL emojis & pictographs", not res['hasEmojis'])
check("cleanTextForSpeechSynthesis preserved Egyptian words and numbers", "عاش يا وحش" in res['cleaned'] and "5 كوبايات" in res['cleaned'])
driver.quit()

# 4. 3-Way Parity Verification
print("\n--- 4. 3-Way HTML Parity Verification ---")
files = ['index.html', 'zatoona.html', 'android/app/src/main/assets/index.html']
hashes = []
for p in files:
    d = open(p, 'rb').read()
    h = hashlib.sha256(d).hexdigest()
    hashes.append(h)
    print(f"  [PARITY] {p}: {len(d)} bytes | SHA256: {h}")

check("All 3 entrypoints have 100% identical SHA-256 hash", len(set(hashes)) == 1)

print("\n" + "=" * 80)
print("ALL 16 CHECKS PASSED — 100% GREEN ✅")
print("=" * 80)
