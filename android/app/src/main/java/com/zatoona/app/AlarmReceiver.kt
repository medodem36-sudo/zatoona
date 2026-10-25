package com.zatoona.app

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.util.Log

/**
 * AlarmReceiver
 * Receives AlarmManager triggers when Zatoona is closed or in background.
 */
class AlarmReceiver : BroadcastReceiver() {

    companion object {
        const val TAG = "ZatoonaAlarmReceiver"
    }

    override fun onReceive(context: Context?, intent: Intent?) {
        if (context == null || intent == null) return

        val scheduleId = intent.getStringExtra(ZatoonaAlarmScheduler.EXTRA_SCHEDULE_ID) ?: return
        val triggerMs = intent.getLongExtra(ZatoonaAlarmScheduler.EXTRA_TRIGGER_MS, System.currentTimeMillis())

        Log.i(TAG, "Alarm trigger received for schedule: $scheduleId at $triggerMs")

        val scheduler = ZatoonaAlarmScheduler(context)
        scheduler.onAlarmFired(scheduleId, triggerMs)
    }
}
