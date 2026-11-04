package com.zatoona.app

import android.app.PendingIntent
import android.appwidget.AppWidgetManager
import android.appwidget.AppWidgetProvider
import android.content.ComponentName
import android.content.Context
import android.content.Intent
import android.net.Uri
import android.widget.RemoteViews
import org.json.JSONObject
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

/**
 * ScheduleWidgetProvider
 * Native Android Home-Screen Widget for displaying today's schedule and timeline.
 * Features a scrollable ListView of today's schedule activities and daily tasks,
 * with real-time sync with Zatoona and 1-tap navigation.
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
        const val REQUEST_CODE_SCHEDULE_ITEM = 5003

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

            views.setTextViewText(R.id.widget_schedule_header_title, context.getString(R.string.widget_schedule_header))
            views.setTextViewText(R.id.widget_schedule_day_badge, SimpleDateFormat("EEEE", Locale("ar")).format(Date()))

            val summary = if (data.totalCount > 0) {
                "${data.completedCount} من ${data.totalCount} مهام مكتملة"
            } else {
                data.summaryText
            }
            views.setTextViewText(R.id.widget_schedule_summary_text, summary)

            // Bind RemoteViewsService adapter to scrollable ListView
            val serviceIntent = Intent(context, ScheduleWidgetService::class.java).apply {
                putExtra(AppWidgetManager.EXTRA_APPWIDGET_ID, appWidgetId)
                setData(Uri.parse(toUri(Intent.URI_INTENT_SCHEME)))
            }
            views.setRemoteAdapter(R.id.widget_schedule_list, serviceIntent)
            views.setEmptyView(R.id.widget_schedule_list, R.id.widget_schedule_empty_view)

            // Pending intent template for ListView items
            val itemClickIntent = Intent(context, MainActivity::class.java).apply {
                putExtra(ZatoonaNotificationManager.EXTRA_MODE, "schedule")
                flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TOP
            }
            val itemClickPending = PendingIntent.getActivity(
                context,
                REQUEST_CODE_SCHEDULE_ITEM,
                itemClickIntent,
                PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_MUTABLE
            )
            views.setPendingIntentTemplate(R.id.widget_schedule_list, itemClickPending)

            // 1-tap navigation to schedule mode
            val rootPending = buildNavigationPendingIntent(context, "schedule", REQUEST_CODE_SCHEDULE_ROOT)
            val openPending = buildNavigationPendingIntent(context, "schedule", REQUEST_CODE_SCHEDULE_OPEN)

            views.setOnClickPendingIntent(R.id.widget_schedule_root, rootPending)
            views.setOnClickPendingIntent(R.id.widget_schedule_btn_open, openPending)

            appWidgetManager.updateAppWidget(appWidgetId, views)
            appWidgetManager.notifyAppWidgetViewDataChanged(appWidgetId, R.id.widget_schedule_list)
        }

        fun updateAllWidgets(context: Context) {
            val appWidgetManager = AppWidgetManager.getInstance(context)
            val componentName = ComponentName(context, ScheduleWidgetProvider::class.java)
            val appWidgetIds = appWidgetManager.getAppWidgetIds(componentName)
            for (appWidgetId in appWidgetIds) {
                updateAppWidget(context, appWidgetManager, appWidgetId)
            }
            if (appWidgetIds.isNotEmpty()) {
                appWidgetManager.notifyAppWidgetViewDataChanged(appWidgetIds, R.id.widget_schedule_list)
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
        if (appWidgetIds.isNotEmpty()) {
            appWidgetManager.notifyAppWidgetViewDataChanged(appWidgetIds, R.id.widget_schedule_list)
        }
    }
}
