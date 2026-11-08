import sys, os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

sys.stdout.reconfigure(encoding='utf-8')

print("=" * 80)
print("TEST SUITE: COACH ZAITOUNA FULL-APP CONTEXT & VOICE ENGINE INTEGRATION")
print("=" * 80)

def check(name, condition):
    if condition:
        print(f"  [PASS] {name}")
    else:
        print(f"  [FAIL] {name}")
        sys.exit(1)

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--allow-file-access-from-files')
chrome_options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

driver = webdriver.Chrome(options=chrome_options)
driver.get('file:///' + os.path.abspath('index.html').replace('\\', '/'))

# 1. Check window functions exist
fns = [
    'getUnifiedZatoonaAppContext',
    'openAiVoiceSettingsModal',
    'closeAiVoiceSettingsModal',
    'testElevenLabsConnectionNow',
    'onSettingsElevenKeyInput',
    'onSettingsElevenVoiceInput',
    'executeLogExpenseAction',
    'executeCompleteActivityAction',
    'executeLogMealAction',
    'speakAiCoachMessage',
    'fallbackSpeakNativeOrWeb'
]

print("\n--- 1. Window Exports Verification ---")
for fn in fns:
    res = driver.execute_script(f"return typeof window.{fn} === 'function';")
    check(f"Function window.{fn} is exported", res)

# 2. Check getUnifiedZatoonaAppContext content
print("\n--- 2. Unified Context Aggregator Verification ---")
ctx = driver.execute_script("return window.getUnifiedZatoonaAppContext();")
print("Aggregated Context Preview:\n" + ctx)
check("Context includes Date", "التاريخ:" in ctx)
check("Context includes Worship/Prayers", "العبادات:" in ctx)
check("Context includes Schedule/Activities", "الجدول" in ctx)
check("Context includes Nutrition/Meals/Water", "الأكل والتغذية:" in ctx)
check("Context includes Budget", "الميزانية والمصاريف:" in ctx)
check("Context includes Gym/Workout", "الجيم والرياضة:" in ctx)
check("Context includes Sleep", "النوم:" in ctx)

# 3. Check App Action Executions
print("\n--- 3. App Actions Execution Verification ---")

# Log expense
exp_res = driver.execute_script("return window.executeAppAction({ type: 'log_expense', amount: 85, category: 'طعام', note: 'غداء كشري' });")
print("Expense Action Response:", exp_res)
check("Expense action returns Egyptian confirmation", "سجلتلك مصروف 85 ج.م" in exp_res)

# Complete activity
act_res = driver.execute_script("return window.executeAppAction({ type: 'complete_activity', activityName: 'استيقاظ' });")
print("Activity Action Response:", act_res)
check("Activity complete action returns Egyptian confirmation", "علمتلك على نشاط" in act_res)

# Log meal
meal_res = driver.execute_script("return window.executeAppAction({ type: 'log_meal', mealIndex: 0 });")
print("Meal Action Response:", meal_res)
check("Meal action returns Egyptian confirmation", "اتأكلت بالكامل ومطابقة لخطتك" in meal_res)

# 4. Check Local Intent Parser
print("\n--- 4. Local Intent Parser Verification ---")
intent1 = driver.execute_script("return window.parseLocalIntent('صرفت 120 جنيه مواصلات');")
check("parseLocalIntent parses expense correctly", intent1 and intent1['type'] == 'log_expense' and intent1['amount'] == 120 and intent1['category'] == 'مواصلات')

intent2 = driver.execute_script("return window.parseLocalIntent('خلصت استيقاظ في الجدول');")
check("parseLocalIntent parses activity completion correctly", intent2 and intent2['type'] == 'complete_activity')

intent3 = driver.execute_script("return window.parseLocalIntent('أكلت وجبة الغدا');")
check("parseLocalIntent parses meal logging correctly", intent3 and intent3['type'] == 'log_meal')

# 5. Check Local AI Chat Response
print("\n--- 5. Local AI Chat Responses Verification ---")
iso = driver.execute_script("return toISO(weekDates[selectedIdx]);")
reply_sched = driver.execute_script(f"return window.generateLocalAiChatResponse('إيه اللي ورايا في الجدول النهاردة', {{}}, '{iso}');")
print("Schedule reply:", reply_sched)
check("Local AI answers schedule queries accurately", "نشاط في جدول النهاردة" in reply_sched or "النشاط القادم" in reply_sched)

reply_budget = driver.execute_script(f"return window.generateLocalAiChatResponse('الميزانية والمصاريف إيه وضعها', {{}}, '{iso}');")
print("Budget reply:", reply_budget)
check("Local AI answers budget queries accurately", "مصاريف" in reply_budget or "المتبقي" in reply_budget or "صرفته" in reply_budget)

reply_gym = driver.execute_script(f"return window.generateLocalAiChatResponse('تمرين النهاردة إيه', {{}}, '{iso}');")
print("Gym reply:", reply_gym)
check("Local AI answers gym queries accurately", "تمرين" in reply_gym or "راحة" in reply_gym)

# 6. Check Voice Settings Modal UI
print("\n--- 6. Voice Settings Modal UI Verification ---")
modal_display = driver.execute_script("""
    window.openAiVoiceSettingsModal();
    const m = document.getElementById('aiVoiceSettingsModal');
    return m ? m.style.display : 'none';
""")
check("openAiVoiceSettingsModal displays modal flex", modal_display == 'flex')

close_display = driver.execute_script("""
    window.closeAiVoiceSettingsModal();
    const m = document.getElementById('aiVoiceSettingsModal');
    return m ? m.style.display : 'flex';
""")
check("closeAiVoiceSettingsModal hides modal", close_display == 'none')

# 7. Check browser console logs
logs = driver.get_log('browser')
severe_logs = [l for l in logs if l['level'] == 'SEVERE']
check("Zero SEVERE browser console errors", len(severe_logs) == 0)

driver.quit()

print("\n" + "=" * 80)
print("ALL FULL-APP CONTEXT & VOICE ENGINE CHECKS PASSED — 100% GREEN ✅")
print("=" * 80)
