package com.zatoona.app

import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import android.os.Build
import androidx.core.app.NotificationCompat
import androidx.core.app.NotificationManagerCompat
import kotlin.math.abs

/**
 * ZatoonaNotificationManager
 * Manages localized notification channels and builds actionable local notifications.
 */
class ZatoonaNotificationManager(private val context: Context) {

    companion object {
        const val CHANNEL_REMINDERS = "zatoona_reminders"
        const val CHANNEL_PRAYERS = "zatoona_prayers"
        const val CHANNEL_SLEEP = "zatoona_sleep"
        const val CHANNEL_ALARMS = "zatoona_alarms"

        const val EXTRA_MODE = "com.zatoona.app.EXTRA_MODE"
        const val EXTRA_SCHEDULE_ID = "com.zatoona.app.EXTRA_SCHEDULE_ID"
        const val EXTRA_TYPE = "com.zatoona.app.EXTRA_TYPE"
    }

    private val notificationManager =
        context.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager

    init {
        createNotificationChannels()
    }

    fun createNotificationChannels() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val generalChannel = NotificationChannel(
                CHANNEL_REMINDERS,
                "تذكيرات زتونة",
                NotificationManager.IMPORTANCE_HIGH
            ).apply {
                description = "إشعارات المهام والأنشطة اليومية المجدولة"
                enableVibration(true)
            }

            val prayerChannel = NotificationChannel(
                CHANNEL_PRAYERS,
                "مواقيت الصلاة",
                NotificationManager.IMPORTANCE_HIGH
            ).apply {
                description = "تنبيهات مواقيت الأذان والصلوات المفروضة"
                enableVibration(true)
            }

            val sleepChannel = NotificationChannel(
                CHANNEL_SLEEP,
                "عادات النوم والراحة",
                NotificationManager.IMPORTANCE_HIGH
            ).apply {
                description = "تنبيهات الاستعداد للنوم ومواعيد الروتين المسائي"
                enableVibration(true)
            }

            val alarmsChannel = NotificationChannel(
                CHANNEL_ALARMS,
                "منبهات زتونة",
                NotificationManager.IMPORTANCE_HIGH
            ).apply {
                description = "تنبيهات المنبه التفاعلية مع شاشة القفل والصوت المستمر"
                enableVibration(true)
                setBypassDnd(true)
                lockscreenVisibility = android.app.Notification.VISIBILITY_PUBLIC
                setSound(null, null)
            }

            notificationManager.createNotificationChannels(
                listOf(generalChannel, prayerChannel, sleepChannel, alarmsChannel)
            )
        }
    }

    fun areNotificationsEnabled(): Boolean {
        return NotificationManagerCompat.from(context).areNotificationsEnabled()
    }

    fun showNotification(schedule: ZatoonaSchedule): Boolean {
        if (!areNotificationsEnabled()) {
            return false
        }

        val channelId = when (schedule.type) {
            "prayer" -> CHANNEL_PRAYERS
            "sleep" -> CHANNEL_SLEEP
            else -> schedule.channelId.ifBlank { CHANNEL_REMINDERS }
        }

        // Tap action: opens MainActivity and passes destination mode
        val intent = Intent(context, MainActivity::class.java).apply {
            flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TOP
            putExtra(EXTRA_MODE, schedule.mode)
            putExtra(EXTRA_SCHEDULE_ID, schedule.id)
            putExtra(EXTRA_TYPE, schedule.type)
        }

        val requestCode = abs(schedule.id.hashCode())
        val pendingIntent = PendingIntent.getActivity(
            context,
            requestCode,
            intent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        val builder = NotificationCompat.Builder(context, channelId)
            .setSmallIcon(R.mipmap.ic_launcher)
            .setContentTitle(schedule.title)
            .setContentText(schedule.body)
            .setStyle(NotificationCompat.BigTextStyle().bigText(schedule.body))
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .setContentIntent(pendingIntent)
            .setAutoCancel(true)
            .setDefaults(NotificationCompat.DEFAULT_ALL)

        val notifId = abs(schedule.id.hashCode())
        notificationManager.notify(notifId, builder.build())
        return true
    }

    fun cancelNotification(scheduleId: String) {
        val notifId = abs(scheduleId.hashCode())
        notificationManager.cancel(notifId)
    }
}
