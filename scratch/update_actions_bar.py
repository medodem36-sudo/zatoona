# Update apply_phase9c2 to keep all buttons present and clean
import os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(REPO, "index.html")
ZATOONA_PATH = os.path.join(REPO, "zatoona.html")

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# Replace the actions bar in renderInteractiveWarmupCard
old_actions_bar = """      <div class="gw-actions-bar">
        <button type="button" class="gw-btn" id="btnGwToggleExpand" title="${isCollapsed ? 'توسيع عرض الحركات' : 'طي عرض الحركات'}">
          ${isCollapsed ? 'عرض الحركات 🔽' : 'طي التفاصيل 🔼'}
        </button>
        ${!state.completed && !isAllDone ? `
          <button type="button" class="gw-btn gw-btn-good" id="btnGwCompleteAll">
            إنهاء الإحماء ✓
          </button>
        ` : ''}
        ${!state.skipped && !state.completed ? `
          <button type="button" class="gw-btn" id="btnGwSkip">
            تخطي الإحماء ⏭️
          </button>
        ` : ''}
        <button type="button" class="gw-btn gw-btn-subtle" id="btnGwReset">
          إعادة تعيين 🔄
        </button>
      </div>"""

new_actions_bar = """      <div class="gw-actions-bar">
        <button type="button" class="gw-btn" id="btnGwToggleExpand" title="${isCollapsed ? 'توسيع عرض الحركات' : 'طي عرض الحركات'}">
          ${isCollapsed ? 'عرض الحركات 🔽' : 'طي التفاصيل 🔼'}
        </button>
        <button type="button" class="gw-btn gw-btn-good" id="btnGwCompleteAll">
          ${state.completed || isAllDone ? 'إعادة تأكيد الإكمال ✓' : 'إنهاء الإحماء ✓'}
        </button>
        <button type="button" class="gw-btn" id="btnGwSkip">
          تخطي الإحماء ⏭️
        </button>
        <button type="button" class="gw-btn gw-btn-subtle" id="btnGwReset">
          إعادة تعيين 🔄
        </button>
      </div>"""

if old_actions_bar in content:
    content = content.replace(old_actions_bar, new_actions_bar, 1)
    print("Updated actions bar to always render all 4 buttons.")

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(content)
with open(ZATOONA_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("Saved index.html and zatoona.html.")
