package com.zatoona.app

import android.app.AlarmManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import android.os.Build
import android.util.Log
import androidx.core.content.ContextCompat
import kotlin.math.abs

/**
 * ZatoonaAlarmScheduler
 * Manages low-level AlarmManager scheduling, exact-alarm checking, and automatic recurrence rolling.
 */
class ZatoonaAlarmScheduler(private val context: Context) {

    companion object {
        const val TAG = "ZatoonaAlarmScheduler"
        const val ACTION_ALARM_TRIGGER = "com.zatoona.app.ALARM_TRIGGER"
        const val EXTRA_SCHEDULE_ID = "com.zatoona.app.EXTRA_SCHEDULE_ID"
        const val EXTRA_TRIGGER_MS = "com.zatoona.app.EXTRA_TRIGGER_MS"
    }

    private val alarmManager =
        context.getSystemService(Context.NOTIFICATION_SERVICE.let { Context.ALARM_SERVICE }) as AlarmManager
    private val repository = ZatoonaScheduleRepository(context)
    private val notificationManager = ZatoonaNotificationManager(context)

    fun canScheduleExactAlarms(): Boolean {
        return if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
            alarmManager.canScheduleExactAlarms()
        } else {
            true
        }
    }

    fun scheduleAlarm(schedule: ZatoonaSchedule): Boolean {
        if (!schedule.enabled) return false

        val nowMs = System.currentTimeMillis()
        val triggerMs = if (schedule.triggerEpochMs > nowMs) {
            schedule.triggerEpochMs
        } else {
            repository.computeNextOccurrence(schedule, nowMs) ?: return false
        }

        val intent = Intent(context, AlarmReceiver::class.java).apply {
            action = ACTION_ALARM_TRIGGER
            putExtra(EXTRA_SCHEDULE_ID, schedule.id)
            putExtra(EXTRA_TRIGGER_MS, triggerMs)
        }

        val requestCode = abs(schedule.id.hashCode())
        val pendingIntent = PendingIntent.getBroadcast(
            context,
            requestCode,
            intent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        try {
            if (canScheduleExactAlarms()) {
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
                    alarmManager.setExactAndAllowWhileIdle(
                        AlarmManager.RTC_WAKEUP,
                        triggerMs,
                        pendingIntent
                    )
                } else {
                    alarmManager.setExact(
                        AlarmManager.RTC_WAKEUP,
                        triggerMs,
                        pendingIntent
                    )
                }
            } else {
                // Inexact graceful fallback
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
                    alarmManager.setAndAllowWhileIdle(
                        AlarmManager.RTC_WAKEUP,
                        triggerMs,
                        pendingIntent
                    )
                } else {
                    alarmManager.set(
                        AlarmManager.RTC_WAKEUP,
                        triggerMs,
                        pendingIntent
                    )
                }
            }

            // Persist the active trigger timestamp
            if (schedule.triggerEpochMs != triggerMs) {
                repository.putSchedule(schedule.copy(triggerEpochMs = triggerMs))
            }
            return true
        } catch (e: SecurityException) {
            Log.w(TAG, "Exact alarm permission rejected, scheduling inexact fallback: ${e.message}")
            try {
                alarmManager.set(AlarmManager.RTC_WAKEUP, triggerMs, pendingIntent)
                return true
            } catch (fallbackEx: Exception) {
                Log.e(TAG, "Failed fallback alarm scheduling: ${fallbackEx.message}")
                return false
            }
        } catch (e: Exception) {
            Log.e(TAG, "Error scheduling alarm for ${schedule.id}: ${e.message}")
            return false
        }
    }

    fun cancelAlarm(scheduleId: String) {
        val intent = Intent(context, AlarmReceiver::class.java).apply {
            action = ACTION_ALARM_TRIGGER
            putExtra(EXTRA_SCHEDULE_ID, scheduleId)
        }
        val requestCode = abs(scheduleId.hashCode())
        val pendingIntent = PendingIntent.getBroadcast(
            context,
            requestCode,
            intent,
            PendingIntent.FLAG_NO_CREATE or PendingIntent.FLAG_IMMUTABLE
        )
        if (pendingIntent != null) {
            alarmManager.cancel(pendingIntent)
            pendingIntent.cancel()
        }
        notificationManager.cancelNotification(scheduleId)

        // Stop active alarm sound/service if running
        try {
            val dismissIntent = Intent(context, AlarmService::class.java).apply {
                action = AlarmService.ACTION_DISMISS_ALARM
                putExtra(AlarmService.EXTRA_SCHEDULE_ID, scheduleId)
            }
            context.startService(dismissIntent)
        } catch (e: Exception) {
            Log.w(TAG, "Could not send dismiss to AlarmService: ${e.message}")
        }
    }

    fun rescheduleAll(): Int {
        val schedules = repository.getAllSchedules()
        var scheduledCount = 0
        val nowMs = System.currentTimeMillis()

        for (sched in schedules) {
            if (!sched.enabled) continue
            val nextMs = repository.computeNextOccurrence(sched, nowMs)
            if (nextMs != null) {
                val updated = sched.copy(triggerEpochMs = nextMs)
                repository.putSchedule(updated)
                if (scheduleAlarm(updated)) {
                    scheduledCount++
                }
            }
        }
        return scheduledCount
    }

    fun onAlarmFired(scheduleId: String, firedEpochMs: Long) {
        val nowMs = System.currentTimeMillis()
        val dedupTag = "$scheduleId:$firedEpochMs"

        if (repository.isDuplicateDispatch(dedupTag, nowMs)) {
            Log.d(TAG, "Ignoring duplicate alarm dispatch for $dedupTag")
            return
        }
        repository.markDispatched(dedupTag, nowMs)

        val schedule = repository.getSchedule(scheduleId)
        if (schedule == null || !schedule.enabled) {
            Log.w(TAG, "Alarm fired for non-existent or disabled schedule: $scheduleId")
            return
        }

        // Start native AlarmService (Foreground Service with looping audio + swipe UI + notification)
        val serviceIntent = Intent(context, AlarmService::class.java).apply {
            action = AlarmService.ACTION_START_ALARM
            putExtra(AlarmService.EXTRA_SCHEDULE_ID, schedule.id)
            putExtra(AlarmService.EXTRA_TRIGGER_MS, firedEpochMs)
            putExtra(AlarmService.EXTRA_TITLE, schedule.title)
            putExtra(AlarmService.EXTRA_BODY, schedule.body)
            putExtra(AlarmService.EXTRA_MODE, schedule.mode)
            putExtra(AlarmService.EXTRA_TYPE, schedule.type)
        }
        try {
            ContextCompat.startForegroundService(context, serviceIntent)
        } catch (e: Exception) {
            Log.e(TAG, "Failed to start AlarmService, falling back to notification: ${e.message}")
            notificationManager.showNotification(schedule)
        }

        // Local Recurrence Calculation (sustainable without WebView or internet)
        val nextOccurrence = repository.computeNextOccurrence(schedule, nowMs)
        if (nextOccurrence != null && nextOccurrence > nowMs) {
            val updated = schedule.copy(triggerEpochMs = nextOccurrence)
            repository.putSchedule(updated)
            scheduleAlarm(updated)
            Log.i(TAG, "Successfully rolled recurring schedule $scheduleId to next occurrence: $nextOccurrence")
        } else {
            // Non-recurring or horizon-exhausted schedule
            if (schedule.recurrence.equals("once", ignoreCase = true)) {
                repository.putSchedule(schedule.copy(enabled = false))
            }
            Log.i(TAG, "Schedule $scheduleId completed with no further immediate occurrences.")
        }
    }
}
