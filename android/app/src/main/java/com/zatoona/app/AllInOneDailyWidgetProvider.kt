package com.zatoona.app

import android.app.PendingIntent
import android.appwidget.AppWidgetManager
import android.appwidget.AppWidgetProvider
import android.content.ComponentName
import android.content.Context
import android.content.Intent
import android.widget.RemoteViews
import org.json.JSONObject

/**
 * AllInOneDailyWidgetProvider
 * Native Android Home-Screen Widget (Package F / Feature 88)
 * Displays combined daily summary: Next Prayer, Workout, Water intake, and Streak.
 */
class AllInOneDailyWidgetProvider : AppWidgetProvider() {

    data class DailySummaryData(
        val nextPrayerName: String,
        val nextPrayerTime: String,
        val workoutDayName: String,
        val waterLiters: Double,
        val waterTarget: Double,
        val streakDays: Int,
        val hasData: Boolean
    )

    companion object {
        const val REQUEST_CODE_AIO_ROOT = 4001
        const val REQUEST_CODE_AIO_PRAYER = 4002
        const val REQUEST_CODE_AIO_GYM = 4003

        fun updateAllWidgets(context: Context) {
            val appWidgetManager = AppWidgetManager.getInstance(context)
            val thisWidget = ComponentName(context, AllInOneDailyWidgetProvider::class.java)
            val allWidgetIds = appWidgetManager.getAppWidgetIds(thisWidget)
            val intent = Intent(context, AllInOneDailyWidgetProvider::class.java).apply {
                action = AppWidgetManager.ACTION_APPWIDGET_UPDATE
                putExtra(AppWidgetManager.EXTRA_APPWIDGET_IDS, allWidgetIds)
            }
            context.sendBroadcast(intent)
        }

        fun loadDailySummary(context: Context): DailySummaryData {
            val prefs = context.getSharedPreferences(ZatoonaBridge.PREFS_NAME, Context.MODE_PRIVATE)
            val raw = prefs.getString(ZatoonaBridge.KEY_ALL_IN_ONE_CACHE, null)
            if (raw.isNullOrBlank()) {
                return DailySummaryData(
                    nextPrayerName = "العصر",
                    nextPrayerTime = "03:15 م",
                    workoutDayName = "تمارين اليوم",
                    waterLiters = 2.0,
                    waterTarget = 3.0,
                    streakDays = 5,
                    hasData = false
                )
            }
            return try {
                val json = JSONObject(raw)
                DailySummaryData(
                    nextPrayerName = json.optString("nextPrayerName", "العصر"),
                    nextPrayerTime = json.optString("nextPrayerTime", "03:15 م"),
                    workoutDayName = json.optString("workoutDayName", "تمارين اليوم"),
                    waterLiters = json.optDouble("waterLitersToday", 2.0),
                    waterTarget = json.optDouble("waterTargetLiters", 3.0),
                    streakDays = json.optInt("streakDays", 5),
                    hasData = true
                )
            } catch (e: Exception) {
                DailySummaryData(
                    nextPrayerName = "العصر",
                    nextPrayerTime = "03:15 م",
                    workoutDayName = "تمارين اليوم",
                    waterLiters = 2.0,
                    waterTarget = 3.0,
                    streakDays = 5,
                    hasData = false
                )
            }
        }
    }

    override fun onUpdate(
        context: Context,
        appWidgetManager: AppWidgetManager,
        appWidgetIds: IntArray
    ) {
        val summary = loadDailySummary(context)
        for (widgetId in appWidgetIds) {
            val views = RemoteViews(context.packageName, R.layout.widget_all_in_one)

            // 1. Populate text fields
            views.setTextViewText(R.id.txt_aio_prayer, "${summary.nextPrayerName} ${summary.nextPrayerTime}")
            views.setTextViewText(R.id.txt_aio_workout, summary.workoutDayName)
            views.setTextViewText(R.id.txt_aio_water, "💧 الماء: ${String.format("%.1f", summary.waterLiters)} / ${String.format("%.1f", summary.waterTarget)} لتر")
            views.setTextViewText(R.id.txt_aio_streak, "🔥 ${summary.streakDays} أيام")

            // 2. Wire PendingIntents
            val flags = PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE

            // Root / open app
            val rootIntent = Intent(context, MainActivity::class.java).apply {
                putExtra(MainActivity.EXTRA_TARGET_MODE, "home")
                flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TOP
            }
            val rootPending = PendingIntent.getActivity(context, REQUEST_CODE_AIO_ROOT, rootIntent, flags)
            views.setOnClickPendingIntent(R.id.widget_aio_root, rootPending)
            views.setOnClickPendingIntent(R.id.btn_aio_open_app, rootPending)

            // Prayer shortcut
            val prayerIntent = Intent(context, MainActivity::class.java).apply {
                putExtra(MainActivity.EXTRA_TARGET_MODE, "prayer")
                flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TOP
            }
            val prayerPending = PendingIntent.getActivity(context, REQUEST_CODE_AIO_PRAYER, prayerIntent, flags)
            views.setOnClickPendingIntent(R.id.btn_aio_prayer, prayerPending)

            // Gym shortcut
            val gymIntent = Intent(context, MainActivity::class.java).apply {
                putExtra(MainActivity.EXTRA_TARGET_MODE, "gym")
                flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TOP
            }
            val gymPending = PendingIntent.getActivity(context, REQUEST_CODE_AIO_GYM, gymIntent, flags)
            views.setOnClickPendingIntent(R.id.btn_aio_gym, gymPending)

            appWidgetManager.updateAppWidget(widgetId, views)
        }
    }
}
