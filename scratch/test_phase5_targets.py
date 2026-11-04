import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

targets = [
    ("KNOWN_KEY_PATTERNS", "/^nutrition-favorite-combos/, /^nutrition-protein-cost/, /^nutrition-carb-cycling/"),
    ("qiblaCard", '<div class="card" id="qiblaCard" style="background:var(--card-alt); border:1px solid var(--line); border-radius:12px; padding:14px; margin:14px 0 16px;"></div>'),
    ("qiyamWitr", '<div class="checklist" id="qiyamWitr"></div>'),
    ("azkar", '<div class="checklist" id="azkar"></div>'),
    ("quranWird", '<div class="checklist" id="quranWird"></div>'),
    ("fastingCard", '<div id="fastingCard" class="settings-card" style="margin-bottom:12px;"></div>'),
    ("renderPrayer", "function renderPrayer(){\n  renderPrayerTimes();\n  renderQiblaCard();\n  renderPrayerFard();\n  renderQiyam();\n  renderNawafilExtra();\n  renderAzkar();\n  renderQuranWird();\n  renderFasting();\n  renderPrayerSummary();\n  renderWorshipAdherenceSummary();\n}"),
    ("END PHASE 4", "/* ================= END PHASE 4: SMART NUTRITION, PANTRY & BUDGET ENGINE ================= */")
]

for name, t in targets:
    found = t in c
    print(f"Target '{name}': {'FOUND ✅' if found else 'NOT FOUND ❌'}")
    if not found:
        # Debug partial match
        first_few = t[:30]
        print(f"  First 30 chars in c: {first_few in c}")
