import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

target1 = '''<div class="theme-modal-overlay" id="themeModalOverlay" role="dialog" aria-modal="true" aria-label="تخصيص المظهر">
  <div class="theme-modal-sheet">
    <div class="tms-header">
      <div class="tms-title">🎨 تخصيص مظهر زتونة</div>
      <button type="button" class="tms-close-btn" id="btnCloseThemeModal" aria-label="إغلاق">✕</button>
    </div>'''

target2 = '''function openThemeCustomizer(){
  triggerHaptic('light');
  const overlay = document.getElementById('themeModalOverlay');
  if(overlay){
    overlay.classList.add('open');
    updateThemeModalActiveStates();
  }
}

function closeThemeCustomizer(){
  const overlay = document.getElementById('themeModalOverlay');
  if(overlay){
    overlay.classList.remove('open');
  }
}
window.openThemeCustomizer = openThemeCustomizer;
window.closeThemeCustomizer = closeThemeCustomizer;'''

print('Target 1 in html:', target1 in html)
print('Target 2 in html:', target2 in html)

with open('android/app/src/main/java/com/zatoona/app/MainActivity.kt', 'r', encoding='utf-8') as f:
    kt = f.read()

target3 = '''    private fun handleBackNavigation() {
        onBackPressedDispatcher.addCallback(this, object : OnBackPressedCallback(true) {
            override fun handleOnBackPressed() {
                if (webView.canGoBack()) {
                    webView.goBack()
                } else {
                    isEnabled = false
                    onBackPressedDispatcher.onBackPressed()
                }
            }
        })
    }'''

print('Target 3 in MainActivity.kt:', target3 in kt)
