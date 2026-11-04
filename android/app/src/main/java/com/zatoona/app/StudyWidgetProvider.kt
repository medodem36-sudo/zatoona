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
 * StudyWidgetProvider
 * Native Android Home-Screen Widget (Phase 7 - System Polish & Zatoona Wrapped)
 * Displays daily study focus time, due flashcard reviews, and quick Pomodoro launchers.
 */
class StudyWidgetProvider : AppWidgetProvider() {

    data class StudyWidgetData(
        val focusMinutesToday: Int,
        val cardsDueCount: Int,
        val completedSessions: Int,
        val hasData: Boolean
    )

    companion object {
        const val REQUEST_CODE_STUDY_ROOT = 3001
        const val REQUEST_CODE_STUDY_START = 3002
        const val REQUEST_CODE_STUDY_REVIEW = 3003

        fun loadWidgetData(context: Context): StudyWidgetData {
            val prefs = context.getSharedPreferences(ZatoonaBridge.PREFS_NAME, Context.MODE_PRIVATE)
            val cachedJson = prefs.getString(ZatoonaBridge.KEY_STUDY_CACHE, null)
            if (cachedJson.isNullOrBlank()) {
                return StudyWidgetData(
                    focusMinutesToday = 0,
                    cardsDueCount = 0,
                    completedSessions = 0,
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
                    hasData = true
                )
            } catch (e: Exception) {
                StudyWidgetData(
                    focusMinutesToday = 0,
                    cardsDueCount = 0,
                    completedSessions = 0,
                    hasData = false
                )
            }
        }

        fun buildNavigationPendingIntent(
            context: Context,
            mode: String,
            requestCode: Int
        ): PendingIntent {
            val intent = Intent(context, MainActivity::class.java).apply {
                flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TOP
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

            if (data.hasData && data.focusMinutesToday > 0) {
                views.setTextViewText(R.id.widget_study_time_display, "${data.focusMinutesToday} دقيقة تركيز")
            } else {
                views.setTextViewText(R.id.widget_study_time_display, "ابدأ جلسة تركيز اليوم")
            }

            if (data.hasData && data.cardsDueCount > 0) {
                views.setTextViewText(R.id.widget_study_cards_display, "${data.cardsDueCount} كارت للمراجعة")
            } else {
                views.setTextViewText(R.id.widget_study_cards_display, "كل الكروت مكتملة ✨")
            }

            if (data.hasData && data.completedSessions > 0) {
                views.setTextViewText(R.id.widget_study_streak_badge, "${data.completedSessions} جلسات اليوم")
            } else {
                views.setTextViewText(R.id.widget_study_streak_badge, "جلسات اليوم")
            }

            // PendingIntents for 1-tap direct access to study view
            val studyPendingIntent = buildNavigationPendingIntent(context, "study", REQUEST_CODE_STUDY_ROOT)
            val startPendingIntent = buildNavigationPendingIntent(context, "study", REQUEST_CODE_STUDY_START)
            val reviewPendingIntent = buildNavigationPendingIntent(context, "study", REQUEST_CODE_STUDY_REVIEW)

            views.setOnClickPendingIntent(R.id.widget_study_root, studyPendingIntent)
            views.setOnClickPendingIntent(R.id.widget_study_btn_start, startPendingIntent)
            views.setOnClickPendingIntent(R.id.widget_study_btn_review, reviewPendingIntent)

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
