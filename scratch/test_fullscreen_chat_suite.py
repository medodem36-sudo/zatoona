import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def run_tests():
    print("=" * 80)
    print("TEST SUITE: FULLSCREEN DEDICATED AI CHAT MODAL & PERFORMANCE")
    print("=" * 80)

    passed = 0
    failed = 0

    def check(desc, cond):
        nonlocal passed, failed
        if cond:
            print(f"  [PASS] {desc}")
            passed += 1
        else:
            print(f"  [FAIL] {desc}")
            failed += 1

    # 1. Native Manifest & MainActivity Checks
    manifest = open('android/app/src/main/AndroidManifest.xml', 'r', encoding='utf-8').read()
    check("AndroidManifest has adjustResize softInputMode", 'android:windowSoftInputMode="adjustResize"' in manifest)

    main_activity = open('android/app/src/main/java/com/zatoona/app/MainActivity.kt', 'r', encoding='utf-8').read()
    check("MainActivity handles .ai-chat-fullscreen-overlay.open in back navigation", '.ai-chat-fullscreen-overlay.open' in main_activity)

    # 2. Selenium Headless Browser Test on index.html
    chrome_opts = Options()
    chrome_opts.add_argument("--headless=new")
    chrome_opts.add_argument("--disable-gpu")
    chrome_opts.add_argument("--window-size=412,915") # Mobile viewport (Pixel/Galaxy standard)
    chrome_opts.add_argument("--allow-file-access-from-files")
    
    driver = webdriver.Chrome(options=chrome_opts)
    try:
        file_path = os.path.abspath("index.html")
        driver.get(f"file:///{file_path}")

        # Check modal existence
        modal = driver.find_element(By.ID, "aiChatFullscreenModal")
        check("Modal #aiChatFullscreenModal exists in DOM", modal is not None)
        check("Modal initially hidden", modal.value_of_css_property("display") == "none")

        # Test openAiFullscreenChat
        driver.execute_script("window.openAiFullscreenChat();")
        modal_display = driver.execute_script("return window.getComputedStyle(document.getElementById('aiChatFullscreenModal')).display;")
        check("openAiFullscreenChat displays modal as flex", modal_display == "flex")
        check("Modal has 'open' class", "open" in modal.get_attribute("class"))

        # Check Input element & CSS
        input_el = driver.find_element(By.ID, "inpAiModalChat")
        check("Chat input #inpAiModalChat exists", input_el is not None)
        font_size = driver.execute_script("return window.getComputedStyle(document.getElementById('inpAiModalChat')).fontSize;")
        check("Chat input has font-size 16px (prevents iOS/Android auto-zoom)", font_size == "16px")

        # Test appendSingleAiMessage
        messages_container = driver.find_element(By.ID, "aiChatModalMessages")
        initial_children_count = driver.execute_script("return document.getElementById('aiChatModalMessages').children.length;")
        
        driver.execute_script("window.appendSingleAiMessage('user', 'أهلاً يا كوتش زتونة');")
        count_after_user = driver.execute_script("return document.getElementById('aiChatModalMessages').children.length;")
        check("appendSingleAiMessage adds a user bubble directly", count_after_user == initial_children_count + 1)
        
        user_bubble = driver.find_element(By.CSS_SELECTOR, ".ai-bubble-user")
        check("User bubble contains Arabic text", "أهلاً يا كوتش زتونة" in user_bubble.text)

        driver.execute_script("window.appendSingleAiMessage('assistant', 'يا مرحب بيك يا بطل! أنا جاهز أساعدك');")
        count_after_bot = driver.execute_script("return document.getElementById('aiChatModalMessages').children.length;")
        check("appendSingleAiMessage adds a bot bubble directly without wipe", count_after_bot == count_after_user + 1)

        # Test scroll behavior
        scroll_behavior = driver.execute_script("return window.getComputedStyle(document.getElementById('aiChatModalMessages')).scrollBehavior;")
        check("Scroll behavior is auto (no animated jumping from top)", scroll_behavior == "auto")

        # Test closeAiFullscreenChat
        driver.execute_script("window.closeAiFullscreenChat();")
        modal_display_closed = driver.execute_script("return window.getComputedStyle(document.getElementById('aiChatFullscreenModal')).display;")
        check("closeAiFullscreenChat hides modal (display: none)", modal_display_closed == "none")

        # Check console errors
        logs = driver.get_log('browser')
        severe_errors = [l for l in logs if l['level'] == 'SEVERE']
        check("Zero SEVERE browser console errors", len(severe_errors) == 0)
        if severe_errors:
            for e in severe_errors:
                print("   [SEVERE ERROR]", e['message'])

    finally:
        driver.quit()

    print("=" * 80)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 80)
    assert failed == 0, f"{failed} tests failed"

if __name__ == '__main__':
    run_tests()
