import hashlib

HTML_FILES = [
    'index.html',
    'zatoona.html',
    'android/app/src/main/assets/index.html'
]

def update_file(path):
    # newline='' preserves exact \r\n line endings
    with open(path, 'r', encoding='utf-8', newline='') as f:
        content = f.read()

    # 1. syncRemindersToNativeBridge top check
    t1 = "function syncRemindersToNativeBridge(){\r\n  if(!isNativeBridgeAvailable()) return;\r\n  if(!notificationSettings || !notificationSettings.enabled) return;\r\n\r\n  const schedules = [];\r\n  const now = new Date();\r\n  const today = toISO(now);\r\n\r\n  // Helper: build ISO dates for the next N days\r\n  function nextNDays(n){\r\n    const dates = [];\r\n    for(let i = 0; i < n; i++){\r\n      const d = new Date(now);\r\n      d.setDate(d.getDate() + i);\r\n      dates.push(toISO(d));\r\n    }\r\n    return dates;\r\n  }\r\n\r\n  // 1. Prayer notifications — push cached dated timings for the next 30 days\r\n  if(notificationSettings.prayers){"
    
    r1 = "function syncRemindersToNativeBridge(){\r\n  if(!isNativeBridgeAvailable()) return;\r\n\r\n  const schedules = [];\r\n  const now = new Date();\r\n  const today = toISO(now);\r\n\r\n  // Helper: build ISO dates for the next N days\r\n  function nextNDays(n){\r\n    const dates = [];\r\n    for(let i = 0; i < n; i++){\r\n      const d = new Date(now);\r\n      d.setDate(d.getDate() + i);\r\n      dates.push(toISO(d));\r\n    }\r\n    return dates;\r\n  }\r\n\r\n  // 1. Prayer notifications — push cached dated timings for the next 30 days (only if general notifications & prayers enabled)\r\n  if(notificationSettings && notificationSettings.enabled && notificationSettings.prayers){"

    if t1 not in content:
        raise ValueError(f"Target 1 not found in {path}")
    content = content.replace(t1, r1, 1)

    # 2. Push to native bridge always
    t2 = "  // Push to native bridge\r\n  if(schedules.length > 0){\r\n    try {\r\n      window.ZatoonaNativeBridge.syncSchedules(JSON.stringify(schedules));\r\n    } catch(e){\r\n      console.warn('[native-bridge] syncSchedules error:', e);\r\n    }\r\n  }\r\n}"
    r2 = "  // Push to native bridge (always push, even if empty, so that cancelled/deleted schedules are purged from AlarmManager)\r\n  try {\r\n    window.ZatoonaNativeBridge.syncSchedules(JSON.stringify(schedules));\r\n  } catch(e){\r\n    console.warn('[native-bridge] syncSchedules error:', e);\r\n  }\r\n}"

    if t2 not in content:
        raise ValueError(f"Target 2 not found in {path}")
    content = content.replace(t2, r2, 1)

    # 3. deleteReminder explicit cancelSchedule
    t3 = "function deleteReminder(id){\r\n  if(!confirm('تمسح التذكير ده؟ الخطوة دي مش هترجع.')) return;\r\n  reminders = reminders.filter(x=>x.id!==id);\r\n  saveReminders(reminders);\r\n  if(editingReminderId===id) resetReminderForm();\r\n  renderReminders();\r\n}"
    r3 = "function deleteReminder(id){\r\n  if(!confirm('تمسح التذكير ده؟ الخطوة دي مش هترجع.')) return;\r\n  const remId = 'rem-' + id;\r\n  reminders = reminders.filter(x=>x.id!==id);\r\n  saveReminders(reminders);\r\n  if(isNativeBridgeAvailable() && typeof window.ZatoonaNativeBridge.cancelSchedule === 'function'){\r\n    try { window.ZatoonaNativeBridge.cancelSchedule(remId); } catch(e){}\r\n  }\r\n  if(editingReminderId===id) resetReminderForm();\r\n  renderReminders();\r\n}"

    if t3 not in content:
        raise ValueError(f"Target 3 not found in {path}")
    content = content.replace(t3, r3, 1)

    # 4. renderReminders clear status indicator
    t4 = "function renderReminders(){\r\n  const listEl = document.getElementById('remindersList'), emptyEl = document.getElementById('remindersEmptyState');\r\n  if(!listEl || !emptyEl) return;\r\n  if(reminders.length===0){ listEl.classList.add('hidden'); emptyEl.classList.remove('hidden'); return; }\r\n  emptyEl.classList.add('hidden'); listEl.classList.remove('hidden');\r\n  listEl.innerHTML = reminders.map(r=>{\r\n    const meta = REMINDER_TYPE_META[r.type] || {label:r.type, icon:'⏰'};\r\n    const timeLabel = r.type==='prayer' ? ((REMINDER_PRAYER_REFS.find(p=>p.key===r.reference)||{}).name || '—') : (r.time || '—');\r\n    return `<div class=\"check-row\">\r\n      <div class=\"check-left\">\r\n        <div class=\"cname\">${meta.icon} ${escapeHtml(r.title||'(من غير عنوان)')}</div>\r\n        <div class=\"rem-meta\"><span><b>${meta.label}</b></span><span>🕐 ${timeLabel}</span><span>🔁 ${reminderRecurrenceLabel(r)}</span></div>\r\n      </div>"
    
    r4 = "function renderReminders(){\r\n  const listEl = document.getElementById('remindersList'), emptyEl = document.getElementById('remindersEmptyState');\r\n  if(!listEl || !emptyEl) return;\r\n  if(reminders.length===0){ listEl.classList.add('hidden'); emptyEl.classList.remove('hidden'); return; }\r\n  emptyEl.classList.add('hidden'); listEl.classList.remove('hidden');\r\n  const isNative = isNativeBridgeAvailable();\r\n  listEl.innerHTML = reminders.map(r=>{\r\n    const meta = REMINDER_TYPE_META[r.type] || {label:r.type, icon:'⏰'};\r\n    const timeLabel = r.type==='prayer' ? ((REMINDER_PRAYER_REFS.find(p=>p.key===r.reference)||{}).name || '—') : (r.time || '—');\r\n    const statusBadge = r.enabled\r\n      ? (isNative\r\n          ? '<span style=\"color:var(--good); font-size:.72rem;\">⚡ مجدول كمنبه</span>'\r\n          : '<span style=\"color:var(--muted); font-size:.72rem;\">🌐 تذكير متصفح (أثناء الفتح)</span>')\r\n      : '<span style=\"color:var(--muted); font-size:.72rem;\">🔕 موقّف</span>';\r\n    return `<div class=\"check-row\">\r\n      <div class=\"check-left\">\r\n        <div class=\"cname\">${meta.icon} ${escapeHtml(r.title||'(من غير عنوان)')}</div>\r\n        <div class=\"rem-meta\"><span><b>${meta.label}</b></span><span>🕐 ${timeLabel}</span><span>🔁 ${reminderRecurrenceLabel(r)}</span><span>${statusBadge}</span></div>\r\n      </div>"

    if t4 not in content:
        raise ValueError(f"Target 4 not found in {path}")
    content = content.replace(t4, r4, 1)

    # 5. renderNotificationSettingsUI hint under master toggle
    t5 = "      <label style=\"display:flex; align-items:center; gap:8px;\">\r\n        <input type=\"checkbox\" id=\"notifOptMaster\" ${notificationSettings.enabled?'checked':''}>\r\n        <b>تفعيل نظام التنبيهات بالكامل</b>\r\n      </label>\r\n      <label style=\"display:flex; align-items:center; gap:8px; margin-right:16px;\">"
    
    r5 = "      <label style=\"display:flex; align-items:center; gap:8px;\">\r\n        <input type=\"checkbox\" id=\"notifOptMaster\" ${notificationSettings.enabled?'checked':''}>\r\n        <b>تفعيل نظام التنبيهات بالكامل</b>\r\n      </label>\r\n      <div style=\"font-size:.72rem; color:var(--muted); margin-right:24px; margin-bottom:4px;\">\r\n        (يشمل مواقيت الصلاة وأنشطة الجدول والنافذة المنبثقة؛ التذكيرات المخصصة في تبويب &quot;تذكيرات&quot; تُدار كمنبهات مستقلة بمفتاح تفعيل خاص بكل تذكير)\r\n      </div>\r\n      <label style=\"display:flex; align-items:center; gap:8px; margin-right:16px;\">"

    if t5 not in content:
        raise ValueError(f"Target 5 not found in {path}")
    content = content.replace(t5, r5, 1)

    with open(path, 'w', encoding='utf-8', newline='') as f:
        f.write(content)
    print(f"Successfully updated {path}")

def verify_hashes():
    hashes = {}
    sizes = {}
    for path in HTML_FILES:
        with open(path, 'rb') as f:
            d = f.read()
        sizes[path] = len(d)
        hashes[path] = hashlib.sha256(d).hexdigest()
        print(f"{path}: size={sizes[path]} sha256={hashes[path]}")
    
    vals = list(hashes.values())
    szs = list(sizes.values())
    if len(set(vals)) == 1 and len(set(szs)) == 1:
        print("ALL 3 HTML FILES ARE 100% BYTE-IDENTICAL!")
    else:
        print("MISMATCH DETECTED!")

if __name__ == '__main__':
    for p in HTML_FILES:
        update_file(p)
    verify_hashes()
