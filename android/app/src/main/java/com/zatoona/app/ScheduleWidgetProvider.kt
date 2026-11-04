package com.zatoona.app

import android.app.PendingIntent
import android.appwidget.AppWidgetManager
import android.appwidget.AppWidgetProvider
import android.content.ComponentName
import android.content.Context
import android.content.Intent
import android.widget.RemoteViews
import org.json.JSONObject
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

/**
 * ScheduleWidgetProvider
 * Native Android Home-Screen Widget for displaying today's schedule and timeline.
 * Displays the current/next scheduled activity, time block, and completion progress.
 */
class ScheduleWidgetProvider : AppWidgetProvider() {

    data class ScheduleWidgetData(
        val currentTaskTitle: String,
        val currentTaskTime: String,
        val summaryText: String,
        val completedCount: Int,
        val totalCount: Int,
        val hasData: Boolean
    )

    companion object {
        const val REQUEST_CODE_SCHEDULE_ROOT = 5001
        const val REQUEST_CODE_SCHEDULE_OPEN = 5002

        fun loadWidgetData(context: Context): ScheduleWidgetData {
            val prefs = context.getSharedPreferences(ZatoonaBridge.PREFS_NAME, Context.MODE_PRIVATE)
            val cachedJson = prefs.getString(ZatoonaBridge.KEY_SCHEDULE_CACHE, null)

            if (cachedJson.isNullOrBlank()) {
                return ScheduleWidgetData(
                    currentTaskTitle = "جدول اليوم منظم ومحدد",
                    currentTaskTime = "اضغط لعرض الأنشطة والمواعيد",
                    summaryText = "تابع يومك أولاً بأول",
                    completedCount = 0,
                    totalCount = 0,
                    hasData = false
                )
            }

            return try {
                val obj = JSONObject(cachedJson)
                val title = obj.optString("currentTaskTitle", "جدول اليوم منظم ومحدد")
                val time = obj.optString("currentTaskTime", "اضغط لعرض الأنشطة والمواعيد")
                val summary = obj.optString("summaryText", "تابع يومك أولاً بأول")
                val completed = obj.optInt("completedCount", 0)
                val total = obj.optInt("totalCount", 0)

                ScheduleWidgetData(
                    currentTaskTitle = title,
                    currentTaskTime = time,
                    summaryText = summary,
                    completedCount = completed,
                    totalCount = total,
                    hasData = true
                )
            } catch (e: Exception) {
                ScheduleWidgetData(
                    currentTaskTitle = "جدول اليوم منظم ومحدد",
                    currentTaskTime = "اضغط لعرض الأنشطة والمواعيد",
                    summaryText = "تابع يومك أولاً بأول",
                    completedCount = 0,
                    totalCount = 0,
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
            val views = RemoteViews(context.packageName, R.layout.widget_schedule)

            views.setTextViewText(R.id.widget_schedule_current_title, data.currentTaskTitle)
            views.setTextViewText(R.id.widget_schedule_current_time, data.currentTaskTime)

            val summary = if (data.totalCount > 0) {
                "${data.completedCount} من ${data.totalCount} مهام مكتملة"
            } else {
                data.summaryText
            }
            views.setTextViewText(R.id.widget_schedule_summary_text, summary)

            // 1-tap navigation to schedule mode
            val rootPending = buildNavigationPendingIntent(context, "schedule", REQUEST_CODE_SCHEDULE_ROOT)
            val openPending = buildNavigationPendingIntent(context, "schedule", REQUEST_CODE_SCHEDULE_OPEN)

            views.setOnClickPendingIntent(R.id.widget_schedule_root, rootPending)
            views.setOnClickPendingIntent(R.id.widget_schedule_btn_open, openPending)

            appWidgetManager.updateAppWidget(appWidgetId, views)
        }

        fun updateAllWidgets(context: Context) {
            val appWidgetManager = AppWidgetManager.getInstance(context)
            val componentName = ComponentName(context, ScheduleWidgetProvider::class.java)
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
