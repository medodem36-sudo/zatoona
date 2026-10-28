package com.zatoona.app

import android.app.PendingIntent
import android.appwidget.AppWidgetManager
import android.appwidget.AppWidgetProvider
import android.content.ComponentName
import android.content.Context
import android.content.Intent
import android.widget.RemoteViews
import java.text.SimpleDateFormat
import java.util.Calendar
import java.util.Date
import java.util.Locale

/**
 * NextPrayerWidgetProvider
 * Native Android Home-Screen Widget (Proposal #8 / Phase 13.5 Extension)
 * Displays upcoming prayer name, scheduled time, remaining countdown, and active city.
 */
class NextPrayerWidgetProvider : AppWidgetProvider() {

    data class NextPrayerInfo(
        val prayerName: String,
        val timeLabel: String,
        val countdownLabel: String,
        val cityName: String,
        val hasData: Boolean
    )

    companion object {
        const val REQUEST_CODE_PRAYER_WIDGET = 2001

        fun getCityDisplayName(cityKey: String): String {
            return when (cityKey.lowercase()) {
                "cairo", "القاهرة" -> "القاهرة"
                "alexandria", "alex", "الإسكندرية" -> "الإسكندرية"
                "minya", "المنيا" -> "المنيا"
                else -> if (cityKey.isNotBlank()) cityKey else "القاهرة"
            }
        }

        fun getCleanPrayerName(title: String): String {
            return title
                .replace("🕌", "")
                .replace("موعد", "")
                .replace("أذان", "")
                .replace("تذكير", "")
                .replace(":", "")
                .trim()
        }

        fun formatCountdown(targetMs: Long, nowMs: Long): String {
            val diffMs = targetMs - nowMs
            if (diffMs <= 0) return "حان وقت الصلاة الآن"

            val totalMinutes = (diffMs / (60 * 1000)).toInt()
            val hours = totalMinutes / 60
            val minutes = totalMinutes % 60

            return if (hours > 0) {
                when (hours) {
                    1 -> if (minutes > 0) "⏳ باقي ساعة و $minutes دقيقة" else "⏳ باقي ساعة"
                    2 -> if (minutes > 0) "⏳ باقي ساعتين و $minutes دقيقة" else "⏳ باقي ساعتين"
                    else -> if (minutes > 0) "⏳ باقي $hours ساعات و $minutes دقيقة" else "⏳ باقي $hours ساعات"
                }
            } else {
                when (minutes) {
                    0 -> "⏳ أقل من دقيقة"
                    1 -> "⏳ باقي دقيقة واحدة"
                    2 -> "⏳ باقي دقيقتان"
                    else -> "⏳ باقي $minutes دقيقة"
                }
            }
        }

        fun formatTime12h(hour: Int, minute: Int): String {
            val h12 = if (hour == 0) 12 else if (hour > 12) hour - 12 else hour
            val suffix = if (hour < 12) "ص" else "م"
            val mStr = if (minute < 10) "0$minute" else "$minute"
            return "$h12:$mStr $suffix"
        }

        fun findNextPrayer(context: Context, nowMs: Long = System.currentTimeMillis()): NextPrayerInfo {
            val repo = ZatoonaScheduleRepository(context)
            val activeCity = repo.getActivePrayerCity()
            val allSchedules = repo.getAllSchedules()

            val prayerSchedules = allSchedules.filter {
                it.type == "prayer" && it.enabled && (it.city.isEmpty() || it.city.equals(activeCity, ignoreCase = true))
            }

            if (prayerSchedules.isEmpty()) {
                return NextPrayerInfo(
                    prayerName = "مواقيت الصلاة",
                    timeLabel = "—:—",
                    countdownLabel = "افتح زتونة لمزامنة المواقيت",
                    cityName = getCityDisplayName(activeCity),
                    hasData = false
                )
            }

            val todayIso = SimpleDateFormat("yyyy-MM-dd", Locale.US).format(Date(nowMs))

            data class Candidate(val schedule: ZatoonaSchedule, val targetMs: Long)
            val candidates = mutableListOf<Candidate>()

            for (sched in prayerSchedules) {
                // 1. Try datedTimings for today first
                val datedTodayMs = sched.datedTimings[todayIso]
                if (datedTodayMs != null && datedTodayMs > nowMs) {
                    candidates.add(Candidate(sched, datedTodayMs))
                    continue
                }

                // 2. Try triggerEpochMs if future
                if (sched.triggerEpochMs > nowMs) {
                    candidates.add(Candidate(sched, sched.triggerEpochMs))
                    continue
                }

                // 3. Fallback: calculate from timeHour and timeMinute
                if (sched.timeHour in 0..23 && sched.timeMinute in 0..59) {
                    val calTarget = Calendar.getInstance().apply {
                        timeInMillis = nowMs
                        set(Calendar.HOUR_OF_DAY, sched.timeHour)
                        set(Calendar.MINUTE, sched.timeMinute)
                        set(Calendar.SECOND, 0)
                        set(Calendar.MILLISECOND, 0)
                    }
                    if (calTarget.timeInMillis > nowMs) {
                        candidates.add(Candidate(sched, calTarget.timeInMillis))
                    } else {
                        // Rolls to tomorrow
                        calTarget.add(Calendar.DAY_OF_YEAR, 1)
                        candidates.add(Candidate(sched, calTarget.timeInMillis))
                    }
                }
            }

            if (candidates.isEmpty()) {
                return NextPrayerInfo(
                    prayerName = "مواقيت الصلاة",
                    timeLabel = "—:—",
                    countdownLabel = "افتح زتونة لمزامنة المواقيت",
                    cityName = getCityDisplayName(activeCity),
                    hasData = false
                )
            }

            candidates.sortBy { it.targetMs }
            val next = candidates.first()

            val cleanName = getCleanPrayerName(next.schedule.title)
            val displayName = if (cleanName.startsWith("صلاة")) cleanName else "صلاة $cleanName"

            val calTarget = Calendar.getInstance().apply { timeInMillis = next.targetMs }
            val timeLabel = formatTime12h(calTarget.get(Calendar.HOUR_OF_DAY), calTarget.get(Calendar.MINUTE))
            val countdown = formatCountdown(next.targetMs, nowMs)

            return NextPrayerInfo(
                prayerName = displayName,
                timeLabel = timeLabel,
                countdownLabel = countdown,
                cityName = getCityDisplayName(activeCity),
                hasData = true
            )
        }

        fun updateAppWidget(
            context: Context,
            appWidgetManager: AppWidgetManager,
            appWidgetId: Int
        ) {
            val info = findNextPrayer(context)
            val views = RemoteViews(context.packageName, R.layout.widget_next_prayer)

            views.setTextViewText(R.id.widget_prayer_name, info.prayerName)
            views.setTextViewText(R.id.widget_prayer_time, info.timeLabel)
            views.setTextViewText(R.id.widget_prayer_countdown, info.countdownLabel)
            views.setTextViewText(R.id.widget_prayer_city, info.cityName)

            // Tap action: launches MainActivity into prayer mode
            val intent = Intent(context, MainActivity::class.java).apply {
                flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TOP
                putExtra(ZatoonaNotificationManager.EXTRA_MODE, "prayer")
            }
            val pendingIntent = PendingIntent.getActivity(
                context,
                REQUEST_CODE_PRAYER_WIDGET,
                intent,
                PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
            )
            views.setOnClickPendingIntent(R.id.widget_prayer_root, pendingIntent)

            appWidgetManager.updateAppWidget(appWidgetId, views)
        }

        /**
         * Trigger refresh across all active Next Prayer widgets on home-screen.
         */
        fun updateAllWidgets(context: Context) {
            try {
                val appWidgetManager = AppWidgetManager.getInstance(context)
                val component = ComponentName(context, NextPrayerWidgetProvider::class.java)
                val appWidgetIds = appWidgetManager.getAppWidgetIds(component)
                for (id in appWidgetIds) {
                    updateAppWidget(context, appWidgetManager, id)
                }
            } catch (e: Exception) {
                // Safe ignore if widget manager unavailable
            }
        }
    }

    override fun onUpdate(
        context: Context,
        appWidgetManager: AppWidgetManager,
        appWidgetIds: IntArray
    ) {
        for (appWidgetId in appWidgetIds) {
            updateAppWidget(context, appWidgetManager, appWidgetId)
        }
    }
}
