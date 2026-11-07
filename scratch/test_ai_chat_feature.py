# -*- coding: utf-8 -*-
import sys, time
sys.stdout.reconfigure(encoding='utf-8')
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

opts = Options()
opts.add_argument('--headless=new')
opts.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
driver = webdriver.Chrome(options=opts)

passed = 0
failed = 0

def test(name, condition, details=""):
    global passed, failed
    if condition:
        passed += 1
        print(f"  [PASS] {name} {details}")
    else:
        failed += 1
        print(f"  [FAIL] {name} - {details}")

try:
    print(">>> Starting AI Assistant Chat Interactive Test Suite <<<")
    driver.get('file:///C:/Users/Lenovo/Documents/GitHub/zatoona/index.html')
    time.sleep(2)

    # 1. Check card exists
    card = driver.find_element(By.ID, 'aiCoachCard')
    test("aiCoachCard exists on Home page", card is not None)

    # 2. Check enable / opt-in
    btn_enable = driver.find_elements(By.ID, 'btnEnableAiCoach')
    if btn_enable:
        btn_enable[0].click()
        time.sleep(0.5)
        test("Click enable AI coach", True)
    else:
        test("AI coach already enabled", True)

    # 3. Check tabs exist
    tab_chat = driver.find_elements(By.ID, 'btnTabAiChat')
    tab_analysis = driver.find_elements(By.ID, 'btnTabAiAnalysis')
    test("Tab Chat button exists", len(tab_chat) > 0)
    test("Tab Analysis button exists", len(tab_analysis) > 0)

    # 4. Check chat messages container and welcome message
    chat_box = driver.find_element(By.ID, 'aiCoachChatBox')
    test("Chat box container exists", chat_box is not None)
    
    messages = driver.find_elements(By.CSS_SELECTOR, '.ai-chat-msg-row')
    test("Welcome message displayed", len(messages) >= 1, f"Found {len(messages)} messages")

    # 5. Check quick prompt buttons
    prompts = driver.find_elements(By.CSS_SELECTOR, '.ai-quick-prompt')
    test("Quick prompt chips exist", len(prompts) >= 5, f"Found {len(prompts)} chips")

    # 6. Click a quick prompt button (e.g. water prompt)
    initial_count = len(driver.find_elements(By.CSS_SELECTOR, '.ai-chat-msg-row'))
    prompts[0].click()
    time.sleep(0.8)
    new_count = len(driver.find_elements(By.CSS_SELECTOR, '.ai-chat-msg-row'))
    test("Quick prompt click added user & assistant messages", new_count >= initial_count + 2, f"{initial_count} -> {new_count}")

    # 7. Type question and click send
    chat_input = driver.find_element(By.ID, 'aiCoachChatInput')
    btn_send = driver.find_element(By.ID, 'btnSendAiChat')
    
    driver.execute_script("arguments[0].value = 'ازاي اوفق بين الصلاة والجيم؟';", chat_input)
    btn_send.click()
    time.sleep(0.8)

    messages_after_send = driver.find_elements(By.CSS_SELECTOR, '.ai-chat-msg-row')
    last_bot_msg = messages_after_send[-1].find_element(By.CSS_SELECTOR, '.ai-chat-bubble').text
    test("Custom chat question answered", "🕌" in last_bot_msg or "صلاة" in last_bot_msg, f"Response preview: {last_bot_msg[:60]}")

    # 8. Test local responder directly for all core intents
    intents = [
        ("water", "قصرت في شرب المياه النهاردة", "💧"),
        ("prayer", "عايز نصيحة لصلاة الفجر", "🌅"),
        ("gym", "عندي ألم في العضلات بعد التمرين", "🏋️"),
        ("sleep", "مش عارف أنام كويس وعندي أرق", "🌙"),
        ("nutrition", "إيه أفضل بروتين صحي ورخيص", "🥗"),
        ("study", "طريقة المذاكرة بالبومودورو", "📚"),
        ("summary", "لخصلي وقيم لي أدائي اليوم", "📊"),
        ("motivation", "حاسس بإحباط وتعب شديد", "💪")
    ]

    for label, query, expected_emoji in intents:
        resp = driver.execute_script(f"""
            const iso = toISO(weekDates[selectedIdx]);
            const stats = analyzeDailyWellnessStats(iso);
            return generateLocalAiChatResponse({repr(query)}, stats, iso);
        """)
        test(f"Intent {label}: '{query}'", expected_emoji in resp, f"Received {expected_emoji}")

    # 9. Test clear chat
    # Overwrite confirm to true
    driver.execute_script("window.confirm = function() { return true; };")
    btn_clear = driver.find_element(By.ID, 'btnClearAiChat')
    btn_clear.click()
    time.sleep(0.5)

    cleared_messages = driver.find_elements(By.CSS_SELECTOR, '.ai-chat-msg-row')
    test("Clear chat resets messages to 1 welcome message", len(cleared_messages) == 1, f"Count={len(cleared_messages)}")

    # 10. Test Tab switching to Analysis and back to Chat
    btn_tab_analysis = driver.find_element(By.ID, 'btnTabAiAnalysis')
    driver.execute_script("arguments[0].click();", btn_tab_analysis)
    time.sleep(0.5)
    test("Switch to Analysis tab", driver.find_element(By.ID, 'aiCoachAnalysisBox').is_displayed())
    
    # Switch back to Chat
    btn_tab_chat = driver.find_element(By.ID, 'btnTabAiChat')
    driver.execute_script("arguments[0].click();", btn_tab_chat)
    time.sleep(0.5)
    test("Switch back to Chat tab", driver.find_element(By.ID, 'aiCoachChatBox').is_displayed())

    # 11. Check console logs for errors
    logs = driver.get_log('browser')
    errors = [l for l in logs if l['level'] == 'SEVERE' and 'favicon' not in l['message'].lower() and 'manifest' not in l['message'].lower()]
    test("Zero browser console errors", len(errors) == 0, f"Errors: {errors}")

    print(f"\nAI Chat Test Suite Results: {passed} PASSED, {failed} FAILED")

except Exception as err:
    import traceback
    print(f"Exception during test: {err}")
    traceback.print_exc()

finally:
    driver.quit()
    sys.exit(0 if failed == 0 else 1)
