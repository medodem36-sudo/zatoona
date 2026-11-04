import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Target 1: btnOpenThemeModal in HTML
t1 = '<button class="theme-toggle-btn" id="btnOpenThemeModal" type="button" aria-label="تخصيص المظهر والألوان"'
print("t1 (btnOpenThemeModal) found:", t1 in c)

# Target 2: initTheme function
t2 = """function initTheme(){
  const theme = getSavedTheme();
  applyTheme(theme, false);
  applyThemeAccent(loadThemeAccent());
  applyThemeFontScale(loadThemeFontScale());
  const btn = document.getElementById('themeToggleBtn');
  if(btn && !btn.dataset.bound){
    btn.dataset.bound = 'true';
    btn.addEventListener('click', toggleTheme);
  }
}"""
print("t2 (initTheme) found:", t2 in c)

# Target 3: openThemeCustomizer
t3 = """function openThemeCustomizer(){
  triggerHaptic('light');
  const overlay = document.getElementById('themeModalOverlay');
  if(overlay){
    overlay.classList.add('open');
    updateThemeModalActiveStates();
  }
}"""
print("t3 (openThemeCustomizer) found:", t3 in c)

# Target 4: theme-modal-overlay CSS
t4 = """.theme-modal-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.65);
    backdrop-filter: blur(4px);
    z-index: 9999;
    display: flex;
    align-items: flex-end;
    justify-content: center;
    opacity: 0;
    pointer-events: none;
    transition: opacity .2s ease;
  }
  .theme-modal-overlay.open {
    opacity: 1;
    pointer-events: auto;
  }"""
print("t4 (theme-modal-overlay CSS) found:", t4 in c)
