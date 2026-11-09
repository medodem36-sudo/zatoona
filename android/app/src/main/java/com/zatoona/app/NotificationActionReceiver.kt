package com.zatoona.app

import android.app.NotificationManager
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.util.Log
import android.widget.Toast

/**
 * NotificationActionReceiver
 * Handles direct interactive action button clicks from Android notifications
 * without requiring the full app WebView to launch into the foreground.
 */
class NotificationActionReceiver : BroadcastReceiver() {

    companion object {
        const val TAG = "ZatoonaNotifAction"
        const val ACTION_QUICK_WATER = "com.zatoona.app.ACTION_QUICK_WATER"
        const val ACTION_MARK_DONE = "com.zatoona.app.ACTION_MARK_DONE"
        const val EXTRA_NOTIFICATION_ID = "com.zatoona.app.EXTRA_NOTIFICATION_ID"
        const val EXTRA_SCHEDULE_ID = "com.zatoona.app.EXTRA_SCHEDULE_ID"
    }

    override fun onReceive(context: Context?, intent: Intent?) {
        if (context == null || intent == null) return
        val action = intent.action ?: return
        val notifId = intent.getIntExtra(EXTRA_NOTIFICATION_ID, -1)
        val notifManager = context.getSystemService(Context.NOTIFICATION_SERVICE) as? NotificationManager

        when (action) {
            ACTION_QUICK_WATER -> {
                Log.i(TAG, "Quick water action triggered from notification")
                val waterIntent = Intent(context, WaterWidgetProvider::class.java).apply {
                    this.action = WaterWidgetProvider.ACTION_ADD_WATER
                    putExtra(WaterWidgetProvider.EXTRA_AMOUNT, 250)
                }
                context.sendBroadcast(waterIntent)
                Toast.makeText(context, "تم تسجيل +250 مل ماء بنجاح 💧", Toast.LENGTH_SHORT).show()
                if (notifId != -1) {
                    notifManager?.cancel(notifId)
                }
            }
            ACTION_MARK_DONE -> {
                val scheduleId = intent.getStringExtra(EXTRA_SCHEDULE_ID) ?: ""
                Log.i(TAG, "Task marked done from notification: $scheduleId")
                Toast.makeText(context, "تم الإنجاز بنجاح ✅", Toast.LENGTH_SHORT).show()
                if (notifId != -1) {
                    notifManager?.cancel(notifId)
                }
            }
        }
    }
}
