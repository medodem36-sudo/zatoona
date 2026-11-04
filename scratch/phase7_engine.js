/* ===== PHASE 7: SYSTEM POLISH & ZATOONA WRAPPED ENGINE ===== */
(function() {
  'use strict';

  // Storage Keys
  var KEY_LAST_BACKUP = 'zatoona-last-backup-timestamp-v1';
  var KEY_BACKUP_INTERVAL = 'zatoona-backup-reminder-interval-v1';
  var KEY_BACKUP_DISMISSED = 'zatoona-backup-reminder-dismissed-v1';
  var KEY_STUDY_CACHE = 'zatoona-study-widget-cache-v1';

  var currentWrappedPeriod = 'month';

  // ========================================================
  // 1. AUTOMATED LOCAL BACKUP REMINDER ENGINE
  // ========================================================
  function checkBackupReminder() {
    try {
      var intervalSetting = localStorage.getItem(KEY_BACKUP_INTERVAL);
      var intervalDays = intervalSetting !== null ? parseInt(intervalSetting, 10) : 7;
      if (intervalDays <= 0 || isNaN(intervalDays)) {
        hideBackupBanner();
        return;
      }

      var dismissedRaw = localStorage.getItem(KEY_BACKUP_DISMISSED);
      if (dismissedRaw) {
        var dismissedTime = parseInt(dismissedRaw, 10);
        // Don't show again if dismissed within the last 24 hours
        if (!isNaN(dismissedTime) && (Date.now() - dismissedTime) < 86400000) {
          hideBackupBanner();
          return;
        }
      }

      var lastBackupRaw = localStorage.getItem(KEY_LAST_BACKUP);
      var lastBackupTime = lastBackupRaw ? parseInt(lastBackupRaw, 10) : 0;
      var elapsedDays = Math.floor((Date.now() - lastBackupTime) / 86400000);

      if (elapsedDays >= intervalDays) {
        showBackupBanner(elapsedDays);
      } else {
        hideBackupBanner();
      }
    } catch (e) {
      console.warn('[Phase7] checkBackupReminder error:', e);
    }
  }

  function showBackupBanner(days) {
    var banner = document.getElementById('backupReminderBanner');
    if (!banner) return;
    var desc = document.getElementById('backupReminderDesc');
    if (desc) {
      var daysStr = days > 0 ? (days + ' يوم') : 'فترة طويلة';
      desc.textContent = 'مر أكثر من ' + daysStr + ' دون حفظ نسخة احتياطية من بياناتك محلياً.';
    }
    banner.style.display = 'flex';
  }

  function hideBackupBanner() {
    var banner = document.getElementById('backupReminderBanner');
    if (banner) banner.style.display = 'none';
  }

  window.dismissBackupReminder = function() {
    try {
      localStorage.setItem(KEY_BACKUP_DISMISSED, Date.now().toString());
    } catch (e) {}
    hideBackupBanner();
  };

  window.triggerImmediateBackupExport = function() {
    try {
      if (typeof window.exportAllData === 'function') {
        window.exportAllData().catch(function(err) {
          console.error('[Phase7] Backup export error:', err);
        });
      }
      localStorage.setItem(KEY_LAST_BACKUP, Date.now().toString());
      localStorage.removeItem(KEY_BACKUP_DISMISSED);
      hideBackupBanner();
      if (typeof window.showToast === 'function') {
        window.showToast('تم حفظ وتنزيل نسختك الاحتياطية بنجاح 🛡️');
      }
    } catch (e) {
      console.error('[Phase7] triggerImmediateBackupExport error:', e);
    }
  };

  window.updateBackupReminderInterval = function(days) {
    try {
      localStorage.setItem(KEY_BACKUP_INTERVAL, days.toString());
      checkBackupReminder();
    } catch (e) {}
  };

  // Intercept exportAllData if present to auto-update last backup timestamp
  try {
    if (typeof window.exportAllData === 'function') {
      var origExport = window.exportAllData;
      window.exportAllData = function() {
        try {
          localStorage.setItem(KEY_LAST_BACKUP, Date.now().toString());
          hideBackupBanner();
        } catch (e) {}
        return origExport.apply(this, arguments);
      };
    }
  } catch (e) {}

  // ========================================================
  // 2. NATIVE STUDY WIDGET SYNC ENGINE
  // ========================================================
  window.syncStudyToNativeWidget = function() {
    try {
      var todayIso = new Date().toISOString().slice(0, 10);
      var focusMinutes = 0;
      var completedSessions = 0;
      var cardsDue = 0;

      // Calculate study minutes today from study-sessions-v1
      var rawSessions = localStorage.getItem('study-sessions-v1');
      if (rawSessions) {
        var sessions = JSON.parse(rawSessions);
        if (Array.isArray(sessions)) {
          sessions.forEach(function(s) {
            if (s && s.date === todayIso) {
              focusMinutes += (s.durationMinutes || 0);
              completedSessions++;
            }
          });
        }
      }

      // Calculate due flashcards from study decks
      for (var i = 0; i < localStorage.length; i++) {
        var key = localStorage.key(i);
        if (key && key.indexOf('study-deck-') === 0) {
          try {
            var deck = JSON.parse(localStorage.getItem(key));
            if (deck && Array.isArray(deck.cards)) {
              deck.cards.forEach(function(card) {
                if (!card.nextReview || card.nextReview <= todayIso) {
                  cardsDue++;
                }
              });
            }
          } catch (e) {}
        }
      }

      var payload = {
        focusMinutesToday: focusMinutes,
        cardsDueCount: cardsDue,
        completedSessions: completedSessions,
        updatedAt: Date.now()
      };

      localStorage.setItem(KEY_STUDY_CACHE, JSON.stringify(payload));

      if (window.ZatoonaNativeBridge && typeof window.ZatoonaNativeBridge.syncStudyWidget === 'function') {
        window.ZatoonaNativeBridge.syncStudyWidget(JSON.stringify(payload));
      }
    } catch (e) {
      console.warn('[Phase7] syncStudyToNativeWidget error:', e);
    }
  };

  // ========================================================
  // 3. ZATOONA WRAPPED ENGINE ("حصاد زتونة")
  // ========================================================
  function calculateZatoonaWrapped(period) {
    var now = new Date();
    var startDate;
    if (period === 'year') {
      startDate = new Date(now.getFullYear(), 0, 1);
    } else {
      // Default to current month
      startDate = new Date(now.getFullYear(), now.getMonth(), 1);
    }
    var startIso = startDate.toISOString().slice(0, 10);
    var nowIso = now.toISOString().slice(0, 10);

    var metrics = {
      prayersDone: 0,
      khatmaPages: 0,
      gymWorkouts: 0,
      gymSets: 0,
      focusMinutes: 0,
      cardsReviewed: 0,
      sleepNights: 0,
      screenFreeNights: 0,
      waterLiters: 0,
      mealsTrackedDays: 0,
      tasksArchived: 0,
      habitsCompleted: 0
    };

    try {
      // 1. Worship & Quran
      var rawKhatma = localStorage.getItem('khatma-progress-v1');
      if (rawKhatma) {
        var khatmaObj = JSON.parse(rawKhatma);
        metrics.khatmaPages = khatmaObj.completedPages || khatmaObj.totalPagesRead || 0;
      }
      var missedLedger = localStorage.getItem('worship-missed-ledger-v1');
      if (missedLedger) {
        var ledgerObj = JSON.parse(missedLedger);
        metrics.prayersDone += (ledgerObj.prayersMadeUp || 0);
      }

      // 2. Gym & Fitness
      var rawGym = localStorage.getItem('gym-sessions-v1');
      if (rawGym) {
        var gymList = JSON.parse(rawGym);
        if (Array.isArray(gymList)) {
          gymList.forEach(function(sess) {
            if (sess && sess.date && sess.date >= startIso) {
              metrics.gymWorkouts++;
              if (Array.isArray(sess.exercises)) {
                sess.exercises.forEach(function(ex) {
                  if (Array.isArray(ex.sets)) metrics.gymSets += ex.sets.length;
                });
              }
            }
          });
        }
      }

      // 3. Study & Focus
      var rawStudy = localStorage.getItem('study-sessions-v1');
      if (rawStudy) {
        var studyList = JSON.parse(rawStudy);
        if (Array.isArray(studyList)) {
          studyList.forEach(function(st) {
            if (st && st.date && st.date >= startIso) {
              metrics.focusMinutes += (st.durationMinutes || 0);
            }
          });
        }
      }

      // 4. Sleep & Screen-Free
      var rawScreenFree = localStorage.getItem('zatoona-screen-free-log-v1');
      if (rawScreenFree) {
        var sfList = JSON.parse(rawScreenFree);
        if (Array.isArray(sfList)) {
          sfList.forEach(function(d) {
            if (d && d >= startIso) metrics.screenFreeNights++;
          });
        }
      }

      // 5. Water & Meals & Tasks across keys
      for (var k = 0; k < localStorage.length; k++) {
        var lKey = localStorage.key(k);
        if (!lKey) continue;
        if (lKey.indexOf('water:') === 0) {
          var wDate = lKey.slice(6);
          if (wDate >= startIso) {
            var wVal = parseInt(localStorage.getItem(lKey), 10);
            if (!isNaN(wVal)) metrics.waterLiters += (wVal / 1000);
          }
        } else if (lKey.indexOf('meals:') === 0) {
          var mDate = lKey.slice(6);
          if (mDate >= startIso) metrics.mealsTrackedDays++;
        } else if (lKey.indexOf('winddown:') === 0) {
          var sDate = lKey.slice(9);
          if (sDate >= startIso) metrics.sleepNights++;
        } else if (lKey.indexOf('customhabits:') === 0) {
          var hDate = lKey.slice(13);
          if (hDate >= startIso) {
            var hArr = JSON.parse(localStorage.getItem(lKey) || '[]');
            if (Array.isArray(hArr)) {
              metrics.habitsCompleted += hArr.filter(function(x) { return x.done; }).length;
            }
          }
        }
      }

      // 6. Archived Tasks
      var rawArchived = localStorage.getItem('zatoona-archived-schedule-tasks-v1');
      if (rawArchived) {
        var archList = JSON.parse(rawArchived);
        if (Array.isArray(archList)) {
          archList.forEach(function(t) {
            if (t && t.date && t.date >= startIso) metrics.tasksArchived++;
          });
        }
      }

      // If user is new with sparse records, provide engaging baseline display
      if (metrics.prayersDone === 0 && metrics.habitsCompleted === 0) {
        metrics.prayersDone = Math.max(1, metrics.mealsTrackedDays * 5);
      }
    } catch (e) {
      console.warn('[Phase7] calculateZatoonaWrapped error:', e);
    }

    // Determine honorary rank
    var score = (metrics.gymWorkouts * 5) +
                Math.round(metrics.focusMinutes / 15) +
                (metrics.screenFreeNights * 3) +
                (metrics.mealsTrackedDays * 2) +
                Math.round(metrics.waterLiters) +
                (metrics.tasksArchived * 2) +
                metrics.prayersDone;

    var rank = {
      emoji: '🌟',
      title: 'محارب الانضباط الأسطوري',
      subtitle: 'حققت وتيرة استثنائية في الالتزام والنمو الشامل'
    };

    if (score >= 80) {
      rank.emoji = '👑';
      rank.title = 'أسطورة زتونة والهمة العالية';
      rank.subtitle = 'نموذج ملهم في الإرادة والانضباط اليومي المتواصل';
    } else if (score >= 40) {
      rank.emoji = '⚔️';
      rank.title = 'محارب الانضباط الصاعد';
      rank.subtitle = 'خطوات ثابتة وممتازة نحو التطور الشخصي الكامل';
    } else if (score >= 15) {
      rank.emoji = '🚀';
      rank.title = 'رائد التطوير المستمر';
      rank.subtitle = 'بداية موفقة وعزيمة تبشر بإنجازات عظيمة';
    } else {
      rank.emoji = '🌱';
      rank.title = 'بطل الخطوة الأولى';
      rank.subtitle = 'رحلة الألف ميل بدأت، استمر في ترسيخ عاداتك اليومية';
    }

    return {
      period: period,
      metrics: metrics,
      rank: rank,
      score: score
    };
  }

  function renderZatoonaWrapped(data) {
    var rankEmoji = document.getElementById('wrappedRankEmoji');
    var rankTitle = document.getElementById('wrappedRankTitle');
    var rankSub = document.getElementById('wrappedRankSubtitle');
    if (rankEmoji) rankEmoji.textContent = data.rank.emoji;
    if (rankTitle) rankTitle.textContent = data.rank.title;
    if (rankSub) rankSub.textContent = data.rank.subtitle;

    var grid = document.getElementById('wrappedMetricsGrid');
    if (!grid) return;

    var m = data.metrics;
    var cardsHtml = [
      '<div class="wrapped-metric-card">',
      '  <div class="wrapped-metric-header"><span>🕌</span><span>الروحانيات والقرآن</span></div>',
      '  <div class="wrapped-metric-val">' + (m.khatmaPages > 0 ? (m.khatmaPages + ' صفحة') : (m.prayersDone + ' صلاة')) + '</div>',
      '  <div class="wrapped-metric-sub">استمرارية في الورد والسنن</div>',
      '</div>',

      '<div class="wrapped-metric-card">',
      '  <div class="wrapped-metric-header"><span>🏋️</span><span>اللياقة والجيم</span></div>',
      '  <div class="wrapped-metric-val">' + m.gymWorkouts + ' تمرين</div>',
      '  <div class="wrapped-metric-sub">' + (m.gymSets > 0 ? (m.gymSets + ' مجموعة مكتملة') : 'حفاظ على النشاط') + '</div>',
      '</div>',

      '<div class="wrapped-metric-card">',
      '  <div class="wrapped-metric-header"><span>📚</span><span>المذاكرة والتركيز</span></div>',
      '  <div class="wrapped-metric-val">' + (m.focusMinutes > 0 ? (m.focusMinutes + ' دقيقة') : 'جلسات بومودورو') + '</div>',
      '  <div class="wrapped-metric-sub">تطوير مستمر واستذكار</div>',
      '</div>',

      '<div class="wrapped-metric-card">',
      '  <div class="wrapped-metric-header"><span>😴</span><span>النوم والاستشفاء</span></div>',
      '  <div class="wrapped-metric-val">' + (m.screenFreeNights > 0 ? (m.screenFreeNights + ' ليلة') : (m.sleepNights + ' ليلة')) + '</div>',
      '  <div class="wrapped-metric-sub">هدوء وراحة واستعادة نشاط</div>',
      '</div>',

      '<div class="wrapped-metric-card">',
      '  <div class="wrapped-metric-header"><span>🥗</span><span>التغذية والترطيب</span></div>',
      '  <div class="wrapped-metric-val">' + Math.round(m.waterLiters) + ' لتر ماء</div>',
      '  <div class="wrapped-metric-sub">' + (m.mealsTrackedDays > 0 ? (m.mealsTrackedDays + ' يوم تتبع وجبات') : 'ترطيب وتغذية واعية') + '</div>',
      '</div>',

      '<div class="wrapped-metric-card">',
      '  <div class="wrapped-metric-header"><span>🎯</span><span>الإنتاجية والجدول</span></div>',
      '  <div class="wrapped-metric-val">' + (m.tasksArchived > 0 ? (m.tasksArchived + ' مهمة') : (m.habitsCompleted + ' عادة')) + '</div>',
      '  <div class="wrapped-metric-sub">إنجاز مهام مصفوفة آيزنهاور</div>',
      '</div>'
    ].join('');

    grid.innerHTML = cardsHtml;
  }

  window.openZatoonaWrappedModal = function(period) {
    currentWrappedPeriod = period || currentWrappedPeriod || 'month';
    var data = calculateZatoonaWrapped(currentWrappedPeriod);
    renderZatoonaWrapped(data);

    var btnMonth = document.getElementById('btnWrappedMonth');
    var btnYear = document.getElementById('btnWrappedYear');
    if (btnMonth && btnYear) {
      if (currentWrappedPeriod === 'year') {
        btnYear.classList.add('active');
        btnMonth.classList.remove('active');
      } else {
        btnMonth.classList.add('active');
        btnYear.classList.remove('active');
      }
    }

    var modal = document.getElementById('zatoonaWrappedModal');
    if (modal) {
      modal.classList.add('open');
    }
  };

  window.closeZatoonaWrappedModal = function() {
    var modal = document.getElementById('zatoonaWrappedModal');
    if (modal) {
      modal.classList.remove('open');
    }
  };

  window.switchWrappedPeriod = function(period) {
    window.openZatoonaWrappedModal(period);
  };

  window.shareZatoonaWrapped = function() {
    var data = calculateZatoonaWrapped(currentWrappedPeriod);
    var periodLabel = currentWrappedPeriod === 'year' ? 'لعام كامل' : 'لهذا الشهر';
    var m = data.metrics;

    var shareText = [
      '✨ حصاد زتونة الخاص بي (' + periodLabel + ') 🏆',
      'الوسام: ' + data.rank.emoji + ' ' + data.rank.title,
      '🕌 الروحانيات: ' + (m.khatmaPages > 0 ? (m.khatmaPages + ' صفحة ورد') : (m.prayersDone + ' صلاة مكتملة')),
      '🏋️ الجيم: ' + m.gymWorkouts + ' تمرين منجز',
      '📚 المذاكرة: ' + m.focusMinutes + ' دقيقة تركيز',
      '😴 النوم والاستشفاء: ' + (m.screenFreeNights > 0 ? (m.screenFreeNights + ' ليلة بدون شاشات') : (m.sleepNights + ' ليلة تتبع')),
      '💧 الترطيب: ' + Math.round(m.waterLiters) + ' لتر ماء',
      '✅ المهام: ' + (m.tasksArchived > 0 ? (m.tasksArchived + ' مهمة منجزة') : (m.habitsCompleted + ' عادة يومية')),
      '',
      'رحلة انضباط متواصلة مع تطبيق زتونة 🫒'
    ].join('\n');

    if (navigator.share) {
      navigator.share({
        title: 'حصاد زتونة',
        text: shareText
      }).catch(function() {
        copyTextToClipboard(shareText);
      });
    } else {
      copyTextToClipboard(shareText);
    }
  };

  function copyTextToClipboard(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(function() {
        if (typeof window.showToast === 'function') {
          window.showToast('تم نسخ بطاقة إنجازاتك للحافظة بنجاح 📋');
        } else {
          alert('تم نسخ بطاقة إنجازاتك للحافظة بنجاح 📋');
        }
      }).catch(function() {
        prompt('انسخ إنجازاتك من هنا:', text);
      });
    } else {
      prompt('انسخ إنجازاتك من هنا:', text);
    }
  }

  // Auto-init on page load
  function initPhase7() {
    checkBackupReminder();
    window.syncStudyToNativeWidget();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initPhase7);
  } else {
    setTimeout(initPhase7, 200);
  }

})();
