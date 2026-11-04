import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

targets = {
    'target_css': "/* --- Phase 7 Styles --- */",
    'target_body': '<body>\n\n<div id="offlineIndicator"',
    'target_sched_tools': '<button type="button" class="reset-btn" id="btnCarryOverTasks" onclick="carryOverIncompleteTasks()" style="border-color:#3b82f6; color:#3b82f6; font-weight:700;">🚀 ترحيل غير المكتمل لبكرة</button>',
    'target_above_timeblocking': '<!-- PACKAGE E: FEATURE 61 - VISUAL TIME-BLOCKING -->',
    'target_js_place': "</script>\n\n<!-- 3. Zatoona Wrapped Fullscreen Festive Modal -->"
}

all_found = True
for name, t in targets.items():
    found = t in content
    print(f"Target '{name}': {found}")
    if not found:
        all_found = False

print("ALL TARGETS FOUND:", all_found)
