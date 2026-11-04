import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

targets = {
    'target_css': "/* --- Phase 7 Styles --- */",
    'target_sleep': '''  <div style="display:flex; align-items:center; gap:10px;">
    <span class="screen-free-streak-badge" id="screenFreeStreakBadge">🔥 0 يوم متتالي</span>
    <button type="button" class="tbtn" id="btnToggleScreenFree" onclick="toggleScreenFreeBedtime()">✓</button>
  </div>
</div>
  </div>

  <!-- ===== PRAYER MODE ===== -->''',
    'target_study_btn': '''          <button type="button" class="study-btn-main" id="btnStudyTimerToggle">▶️ ابدأ الجلسة</button>
          <button type="button" class="study-btn-sec" id="btnStudyTimerSkip">⏭️ تخطي المرحلة</button>
          <button type="button" class="study-btn-sec" id="btnStudyTimerReset">🔄 إعادة تعيين</button>
        </div>''',
    'target_study_modal_place': '''        <button type="button" class="study-btn-sec" id="btnCancelExamModal">إلغاء</button>
        <button type="button" class="study-btn-main" id="btnSaveExamModal">حفظ الامتحان</button>
      </div>
    </div>
  </div>''',
    'target_pomo_complete': '''      completedPomosToday++;
      const dur = timerMode === 'flow' ? timerElapsedFlow : timerTotalPhaseSeconds;
      logStudySession(dur);''',
    'target_sched_btn': '''      <button class="reset-btn" id="scheduleCopyBtn" style="border-color:var(--teal); color:var(--teal); font-weight:700;">📋 نسخ الجدول لأيام تانية</button>
      <button class="reset-btn" id="scheduleAddActBtn" style="border-color:var(--good); color:var(--good); font-weight:700;">➕ إضافة نشاط</button>''',
    'target_sched_cards': '''    <div class="settings-card hidden" id="scheduleCopyCard"></div>
    <div class="settings-card hidden" id="scheduleActEditCard"></div>
    <!-- PHASE 6: SCHEDULE VIEW CARDS (To be inserted into #scheduleView) -->''',
    'target_js_engine': '''  // Auto-init on load
  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', initPhase6Engine);
  } else {
    initPhase6Engine();
  }

})();

</script>'''
}

all_found = True
for name, t in targets.items():
    found = t in content
    print(f"Target '{name}': {found}")
    if not found:
        all_found = False

print("ALL TARGETS FOUND:", all_found)
