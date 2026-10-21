import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

def find_fn(name):
    idx = text.find('function ' + name)
    if idx == -1:
        idx = text.find(name + ' = function')
    if idx == -1:
        idx = text.find('const ' + name + ' =')
    if idx != -1:
        line_no = text[:idx].count('\n') + 1
        return f'{name} @ line {line_no}'
    return f'{name}: NOT FOUND'

print('=== PHASE 8: SCHEDULE, PRAYER, SLEEP, HABITS, REMINDERS, RECOVERY ===')
target_fns = [
    # Schedule
    'renderSchedule', 'renderScheduleDayView', 'addActivity', 'updateActivity', 'deleteActivity',
    'duplicateActivity', 'saveDayActs', 'getDaySchedRecord', 'cascadeResolveOverlaps',
    'SCHED_ACTIVITY_PRIORITIES', 'computeDaySchedule', 'schedActivityCollides',
    # Prayer
    'fetchPrayerTimes', 'loadPrayerTimesCache', 'savePrayerTimesCache', 'getPrayerTimesForDate',
    'renderPrayerView', 'togglePrayer', 'loadPrayer', 'savePrayer', 'calcPrayerTimes',
    # Sleep
    'renderSleepView', 'loadSleepTimes', 'saveSleepTimes', 'sleepHours', 'loadSleepQuality', 'saveSleepQuality',
    'clockToMinutesBedtime', 'clockToMinutesWake',
    # Reminders
    'renderReminders', 'loadReminders', 'saveReminders', 'addReminder', 'deleteReminder',
    'reminderNextTrigger', 'scheduleNotification',
    # Water & Habits
    'loadWater', 'saveWater', 'loadScheduleCheck', 'saveScheduleCheck', 'loadQuran', 'saveQuran',
    # Recovery
    'renderRecoveryStatus', 'computeRecoveryScore', 'loadRecovery', 'saveRecovery'
]

for fn in target_fns:
    print(' ', find_fn(fn))
