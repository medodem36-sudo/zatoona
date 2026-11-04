package com.zatoona.app

import android.app.PendingIntent
import android.appwidget.AppWidgetManager
import android.appwidget.AppWidgetProvider
import android.content.ComponentName
import android.content.Context
import android.content.Intent
import android.os.SystemClock
import android.widget.RemoteViews
import org.json.JSONObject

/**
 * StudyWidgetProvider
 * Interactive Native Android Home-Screen Widget for Study & Deep Focus.
 * Features an interactive live Chronometer that runs directly on the home screen
 * without requiring the user to open the app, automatically synchronizing focus minutes.
 */
class StudyWidgetProvider : AppWidgetProvider() {

    data class StudyWidgetData(
        val focusMinutesToday: Int,
        val cardsDueCount: Int,
        val completedSessions: Int,
        val isTimerRunning: Boolean,
        val timerStartTimeMs: Long,
        val hasData: Boolean
    )

    companion object {
        const val ACTION_TOGGLE_TIMER = "com.zatoona.app.ACTION_TOGGLE_STUDY_TIMER"
        const val ACTION_RESET_TIMER = "com.zatoona.app.ACTION_RESET_STUDY_TIMER"

        const val REQUEST_CODE_STUDY_ROOT = 3001
        const val REQUEST_CODE_STUDY_START = 3002
        const val REQUEST_CODE_STUDY_REVIEW = 3003

        fun loadWidgetData(context: Context): StudyWidgetData {
            val prefs = context.getSharedPreferences(ZatoonaBridge.PREFS_NAME, Context.MODE_PRIVATE)
            val cachedJson = prefs.getString(ZatoonaBridge.KEY_STUDY_CACHE, null)
            val isRunning = prefs.getBoolean("study_timer_running", false)
            val startMs = prefs.getLong("study_timer_start_ms", 0L)

            if (cachedJson.isNullOrBlank()) {
                return StudyWidgetData(
                    focusMinutesToday = 0,
                    cardsDueCount = 0,
                    completedSessions = 0,
                    isTimerRunning = isRunning,
                    timerStartTimeMs = startMs,
                    hasData = false
                )
            }

            return try {
                val obj = JSONObject(cachedJson)
                val focusMinutes = obj.optInt("focusMinutesToday", 0)
                val cardsDue = obj.optInt("cardsDueCount", 0)
                val sessions = obj.optInt("completedSessions", 0)
                StudyWidgetData(
                    focusMinutesToday = focusMinutes,
                    cardsDueCount = cardsDue,
                    completedSessions = sessions,
                    isTimerRunning = isRunning,
                    timerStartTimeMs = startMs,
                    hasData = true
                )
            } catch (e: Exception) {
                StudyWidgetData(
                    focusMinutesToday = 0,
                    cardsDueCount = 0,
                    completedSessions = 0,
                    isTimerRunning = isRunning,
                    timerStartTimeMs = startMs,
                    hasData = false
                )
            }
        }

        fun saveWidgetData(context: Context, data: StudyWidgetData) {
            val prefs = context.getSharedPreferences(ZatoonaBridge.PREFS_NAME, Context.MODE_PRIVATE)
            val obj = JSONObject().apply {
                put("focusMinutesToday", data.focusMinutesToday)
                put("cardsDueCount", data.cardsDueCount)
                put("completedSessions", data.completedSessions)
                put("timestamp", System.currentTimeMillis())
            }
            prefs.edit()
                .putString(ZatoonaBridge.KEY_STUDY_CACHE, obj.toString())
                .putBoolean("study_timer_running", data.isTimerRunning)
                .putLong("study_timer_start_ms", data.timerStartTimeMs)
                .apply()
        }

        fun buildBroadcastPendingIntent(context: Context, action: String, requestCode: Int): PendingIntent {
            val intent = Intent(context, StudyWidgetProvider::class.java).apply {
                this.action = action
            }
            val flags = PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
            return PendingIntent.getBroadcast(context, requestCode, intent, flags)
        }

        fun buildNavigationPendingIntent(
            context: Context,
            mode: String,
            requestCode: Int
        ): PendingIntent {
            val intent = Intent(context, MainActivity::class.java).apply {
                addFlags(Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TOP)
                putExtra(ZatoonaNotificationManager.EXTRA_MODE, mode)
            }
            val flags = PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
            return PendingIntent.getActivity(context, requestCode, intent, flags)
        }

        fun updateAppWidget(
            context: Context,
            appWidgetManager: AppWidgetManager,
            appWidgetId: Int
        ) {
            val data = loadWidgetData(context)
            val views = RemoteViews(context.packageName, R.layout.widget_study)

            if (data.focusMinutesToday > 0) {
                views.setTextViewText(R.id.widget_study_time_display, "${data.focusMinutesToday} دقيقة تركيز اليوم")
            } else {
                views.setTextViewText(R.id.widget_study_time_display, "0 دقيقة تركيز اليوم")
            }

            if (data.cardsDueCount > 0) {
                views.setTextViewText(R.id.widget_study_cards_display, "${data.cardsDueCount} كروت للمراجعة")
            } else {
                views.setTextViewText(R.id.widget_study_cards_display, "مراجعة الكروت")
            }

            if (data.completedSessions > 0) {
                views.setTextViewText(R.id.widget_study_streak_badge, "${data.completedSessions} جلسات اليوم")
            } else {
                views.setTextViewText(R.id.widget_study_streak_badge, "جلسات اليوم")
            }

            // Live interactive Chronometer setup
            if (data.isTimerRunning && data.timerStartTimeMs > 0L) {
                val elapsedSinceStart = System.currentTimeMillis() - data.timerStartTimeMs
                val chronometerBase = SystemClock.elapsedRealtime() - elapsedSinceStart
                views.setChronometer(R.id.widget_study_chronometer, chronometerBase, null, true)
                views.setTextViewText(R.id.widget_study_timer_label, "المؤقت قيد التشغيل ⚡")
                views.setTextViewText(R.id.widget_study_btn_start, context.getString(R.string.widget_study_pause))
            } else {
                views.setChronometer(R.id.widget_study_chronometer, SystemClock.elapsedRealtime(), null, false)
                views.setTextViewText(R.id.widget_study_timer_label, "المؤقت متوقف")
                views.setTextViewText(R.id.widget_study_btn_start, context.getString(R.string.widget_study_start))
            }

            // PendingIntents for interactive buttons
            val startPending = buildBroadcastPendingIntent(context, ACTION_TOGGLE_TIMER, REQUEST_CODE_STUDY_START)
            val reviewPending = buildNavigationPendingIntent(context, "study", REQUEST_CODE_STUDY_REVIEW)
            val rootPending = buildNavigationPendingIntent(context, "study", REQUEST_CODE_STUDY_ROOT)

            views.setOnClickPendingIntent(R.id.widget_study_btn_start, startPending)
            views.setOnClickPendingIntent(R.id.widget_study_btn_review, reviewPending)
            views.setOnClickPendingIntent(R.id.widget_study_root, rootPending)

            appWidgetManager.updateAppWidget(appWidgetId, views)
        }

        fun updateAllWidgets(context: Context) {
            val appWidgetManager = AppWidgetManager.getInstance(context)
            val componentName = ComponentName(context, StudyWidgetProvider::class.java)
            val appWidgetIds = appWidgetManager.getAppWidgetIds(componentName)
            for (appWidgetId in appWidgetIds) {
                updateAppWidget(context, appWidgetManager, appWidgetId)
            }
        }
    }

    override fun onReceive(context: Context, intent: Intent) {
        super.onReceive(context, intent)
        when (intent.action) {
            ACTION_TOGGLE_TIMER -> {
                val current = loadWidgetData(context)
                if (current.isTimerRunning) {
                    val elapsedMs = System.currentTimeMillis() - current.timerStartTimeMs
                    val addedMinutes = if (elapsedMs >= 30000L) {
                        ((elapsedMs + 30000L) / 60000L).toInt().coerceAtLeast(1)
                    } else {
                        0
                    }
                    val newSessions = if (addedMinutes > 0) current.completedSessions + 1 else current.completedSessions
                    val updated = current.copy(
                        focusMinutesToday = current.focusMinutesToday + addedMinutes,
                        completedSessions = newSessions,
                        isTimerRunning = false,
                        timerStartTimeMs = 0L,
                        hasData = true
                    )
                    saveWidgetData(context, updated)
                } else {
                    val updated = current.copy(
                        isTimerRunning = true,
                        timerStartTimeMs = System.currentTimeMillis()
                    )
                    saveWidgetData(context, updated)
                }
                updateAllWidgets(context)
            }
            ACTION_RESET_TIMER -> {
                val current = loadWidgetData(context)
                val updated = current.copy(
                    isTimerRunning = false,
                    timerStartTimeMs = 0L
                )
                saveWidgetData(context, updated)
                updateAllWidgets(context)
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
