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

        // Phase 13.10 / Proposal #14: Android notification grouping & summary
        const val GROUP_ZATOONA_REMINDERS = "com.zatoona.app.REMINDERS_GROUP"
        const val NOTIFICATION_ID_GROUP_SUMMARY = 999999
        const val NOTIFICATION_ID_WORKOUT = 888888

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
                lockscreenVisibility = android.app.Notification.VISIBILITY_PUBLIC
            }

            val prayerChannel = NotificationChannel(
                CHANNEL_PRAYERS,
                "مواقيت الصلاة",
                NotificationManager.IMPORTANCE_HIGH
            ).apply {
                description = "تنبيهات مواقيت الأذان والصلوات المفروضة"
                enableVibration(true)
                setBypassDnd(true)
                lockscreenVisibility = android.app.Notification.VISIBILITY_PUBLIC
            }

            val sleepChannel = NotificationChannel(
                CHANNEL_SLEEP,
                "عادات النوم والراحة",
                NotificationManager.IMPORTANCE_HIGH
            ).apply {
                description = "تنبيهات الاستعداد للنوم ومواعيد الروتين المسائي"
                enableVibration(true)
                lockscreenVisibility = android.app.Notification.VISIBILITY_PUBLIC
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
            .setVisibility(NotificationCompat.VISIBILITY_PUBLIC)
            .setContentIntent(pendingIntent)
            .setAutoCancel(true)
            .setDefaults(NotificationCompat.DEFAULT_ALL)
            .setGroup(GROUP_ZATOONA_REMINDERS)

        val notifId = abs(schedule.id.hashCode())
        notificationManager.notify(notifId, builder.build())

        // Post / update Android notification group summary (Proposal #14)
        val summaryIntent = Intent(context, MainActivity::class.java).apply {
            flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TOP
            putExtra(EXTRA_MODE, "home")
        }
        val summaryPendingIntent = PendingIntent.getActivity(
            context,
            NOTIFICATION_ID_GROUP_SUMMARY,
            summaryIntent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )
        val summaryBuilder = NotificationCompat.Builder(context, channelId)
            .setSmallIcon(R.mipmap.ic_launcher)
            .setContentTitle("تذكيرات زتونة")
            .setContentText("تنبيهات مجدولة نشطة")
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .setVisibility(NotificationCompat.VISIBILITY_PUBLIC)
            .setGroup(GROUP_ZATOONA_REMINDERS)
            .setGroupSummary(true)
            .setContentIntent(summaryPendingIntent)
            .setAutoCancel(true)

        notificationManager.notify(NOTIFICATION_ID_GROUP_SUMMARY, summaryBuilder.build())
        return true
    }

    fun showAlarmNotification(schedule: ZatoonaSchedule, triggerEpochMs: Long): Boolean {
        if (!areNotificationsEnabled()) {
            return false
        }

        val channelId = CHANNEL_ALARMS

        val fullScreenIntent = Intent(context, AlarmActivity::class.java).apply {
            flags = Intent.FLAG_ACTIVITY_NEW_TASK or
                    Intent.FLAG_ACTIVITY_NO_USER_ACTION or
                    Intent.FLAG_ACTIVITY_CLEAR_TOP
            putExtra(AlarmService.EXTRA_SCHEDULE_ID, schedule.id)
            putExtra(AlarmService.EXTRA_TRIGGER_MS, triggerEpochMs)
            putExtra(AlarmService.EXTRA_TITLE, schedule.title)
            putExtra(AlarmService.EXTRA_BODY, schedule.body)
            putExtra(AlarmService.EXTRA_MODE, schedule.mode)
            putExtra(AlarmService.EXTRA_TYPE, schedule.type)
        }

        val requestCode = abs(schedule.id.hashCode())
        val fullScreenPendingIntent = PendingIntent.getActivity(
            context,
            requestCode,
            fullScreenIntent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        val dismissIntent = Intent(context, AlarmService::class.java).apply {
            action = AlarmService.ACTION_DISMISS_ALARM
            putExtra(AlarmService.EXTRA_SCHEDULE_ID, schedule.id)
        }
        val dismissPendingIntent = PendingIntent.getService(
            context,
            requestCode + 5000,
            dismissIntent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        val builder = NotificationCompat.Builder(context, channelId)
            .setSmallIcon(R.mipmap.ic_launcher)
            .setContentTitle(schedule.title)
            .setContentText(schedule.body.ifBlank { "منبه نشط — اسحب أو اضغط للإيقاف" })
            .setStyle(NotificationCompat.BigTextStyle().bigText(schedule.body.ifBlank { "منبه نشط — اسحب أو اضغط للإيقاف" }))
            .setPriority(NotificationCompat.PRIORITY_MAX)
            .setCategory(NotificationCompat.CATEGORY_ALARM)
            .setVisibility(NotificationCompat.VISIBILITY_PUBLIC)
            .setOngoing(true)
            .setAutoCancel(false)
            .setDefaults(NotificationCompat.DEFAULT_ALL)
            .setContentIntent(fullScreenPendingIntent)
            .addAction(
                android.R.drawable.ic_menu_close_clear_cancel,
                "إيقاف",
                dismissPendingIntent
            )

        builder.setFullScreenIntent(fullScreenPendingIntent, true)

        val notifId = abs(schedule.id.hashCode())
        notificationManager.notify(notifId, builder.build())
        return true
    }

    fun cancelNotification(scheduleId: String) {
        val notifId = abs(scheduleId.hashCode())
        notificationManager.cancel(notifId)
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            val active = notificationManager.activeNotifications
            val groupCount = active.count { it.notification.group == GROUP_ZATOONA_REMINDERS && it.id != NOTIFICATION_ID_GROUP_SUMMARY }
            if (groupCount == 0) {
                notificationManager.cancel(NOTIFICATION_ID_GROUP_SUMMARY)
            }
        }
    }

    fun showWorkoutNotification(title: String, text: String): Boolean {
        return try {
            val intent = Intent(context, MainActivity::class.java).apply {
                flags = Intent.FLAG_ACTIVITY_SINGLE_TOP or Intent.FLAG_ACTIVITY_CLEAR_TOP
                putExtra(EXTRA_MODE, "gym")
            }
            val pendingIntent = PendingIntent.getActivity(
                context,
                NOTIFICATION_ID_WORKOUT,
                intent,
                PendingIntent.FLAG_UPDATE_CURRENT or (if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) PendingIntent.FLAG_IMMUTABLE else 0)
            )

            val builder = NotificationCompat.Builder(context, CHANNEL_REMINDERS)
                .setSmallIcon(R.mipmap.ic_launcher)
                .setContentTitle(title.ifBlank { "تمرين الجيم نشط 🏋️" })
                .setContentText(text.ifBlank { "مؤقت الراحة والمجموعات قيد التشغيل" })
                .setPriority(NotificationCompat.PRIORITY_LOW)
                .setOngoing(true)
                .setAutoCancel(false)
                .setContentIntent(pendingIntent)

            notificationManager.notify(NOTIFICATION_ID_WORKOUT, builder.build())
            true
        } catch (e: Exception) {
            false
        }
    }

    fun hideWorkoutNotification(): Boolean {
        return try {
            notificationManager.cancel(NOTIFICATION_ID_WORKOUT)
            true
        } catch (e: Exception) {
            false
        }
    }
}
