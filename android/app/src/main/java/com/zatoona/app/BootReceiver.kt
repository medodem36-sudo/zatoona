package com.zatoona.app

import android.app.AlarmManager
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.os.Build
import android.util.Log

/**
 * BootReceiver
 * Reschedules active local alarms upon device reboot, timezone change, clock change,
 * app update, or exact-alarm permission state change.
 */
class BootReceiver : BroadcastReceiver() {

    companion object {
        const val TAG = "ZatoonaBootReceiver"
    }

    override fun onReceive(context: Context?, intent: Intent?) {
        if (context == null || intent == null) return

        val action = intent.action ?: return
        Log.i(TAG, "System broadcast received: $action")

        val relevantActions = setOf(
            Intent.ACTION_BOOT_COMPLETED,
            Intent.ACTION_MY_PACKAGE_REPLACED,
            Intent.ACTION_TIME_CHANGED,
            Intent.ACTION_TIMEZONE_CHANGED
        )

        var isRelevant = relevantActions.contains(action)
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
            if (action == AlarmManager.ACTION_SCHEDULE_EXACT_ALARM_PERMISSION_STATE_CHANGED) {
                isRelevant = true
            }
        }

        if (isRelevant) {
            val scheduler = ZatoonaAlarmScheduler(context)
            val count = scheduler.rescheduleAll()
            Log.i(TAG, "Rescheduled $count alarms following broadcast: $action")
        }
    }
}
