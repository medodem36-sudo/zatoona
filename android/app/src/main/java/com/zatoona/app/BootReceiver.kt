package com.zatoona.app

import android.app.AlarmManager
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.os.Build
import android.util.Log
import androidx.core.app.NotificationCompat

/**
 * BootReceiver
 * Reschedules active local alarms upon device reboot, timezone change, clock change,
 * app update, or exact-alarm permission state change.
 */
class BootReceiver : BroadcastReceiver() {

    companion object {
        const val TAG = "ZatoonaBootReceiver"
        private const val WAKE_PROMPT_NOTIF_ID = 7771
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

            val prefs = context.getSharedPreferences("zatoona_settings", Context.MODE_PRIVATE)
            val wakeWordEnabled = prefs.getBoolean("wake_word_continuous_enabled", false)
            if (wakeWordEnabled) {
                // In Android 14+ (API 34), starting a ForegroundService with MICROPHONE type from
                // a background BOOT_COMPLETED receiver throws ForegroundServiceStartNotAllowedException.
                // We show an interactive notification allowing the user to resume listening with 1 tap.
                try {
                    val nm = context.getSystemService(Context.NOTIFICATION_SERVICE) as? NotificationManager
                    val launchIntent = Intent(context, MainActivity::class.java).apply {
                        flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TOP
                        putExtra(MainActivity.EXTRA_AUTO_LISTEN, true)
                    }
                    val pi = PendingIntent.getActivity(
                        context,
                        WAKE_PROMPT_NOTIF_ID,
                        launchIntent,
                        PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
                    )
                    val notif = NotificationCompat.Builder(context, ZatoonaNotificationManager.CHANNEL_REMINDERS)
                        .setSmallIcon(R.mipmap.ic_launcher)
                        .setContentTitle("المساعد الصوتي لزتونة 🎙️")
                        .setContentText("انقر هنا لتفعيل الاستماع التلقائي بكلمة النداء")
                        .setContentIntent(pi)
                        .setAutoCancel(true)
                        .setPriority(NotificationCompat.PRIORITY_DEFAULT)
                        .build()
                    nm?.notify(WAKE_PROMPT_NOTIF_ID, notif)
                    Log.i(TAG, "Posted WakeWord activation prompt notification following broadcast: $action")
                } catch (e: Exception) {
                    Log.e(TAG, "Failed to post WakeWord notification: ${e.message}")
                }
            }
        }
    }
}
