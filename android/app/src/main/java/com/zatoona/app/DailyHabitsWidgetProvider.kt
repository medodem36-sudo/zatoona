package com.zatoona.app

import android.app.PendingIntent
import android.appwidget.AppWidgetManager
import android.appwidget.AppWidgetProvider
import android.content.ComponentName
import android.content.Context
import android.content.Intent
import android.view.View
import android.widget.RemoteViews
import org.json.JSONObject

/**
 * DailyHabitsWidgetProvider
 * Native Android Home-Screen Widget (Proposal #9 / Phase 13.5 Extension)
 * Displays daily habits checklist, current streak, and day completion progress.
 */
class DailyHabitsWidgetProvider : AppWidgetProvider() {

    data class HabitItem(
        val title: String,
        val streak: Int,
        val done: Boolean
    )

    data class DailyHabitsWidgetData(
        val totalCount: Int,
        val doneCount: Int,
        val habits: List<HabitItem>,
        val hasData: Boolean
    )

    companion object {
        const val REQUEST_CODE_HABITS_WIDGET = 2002

        fun loadWidgetData(context: Context): DailyHabitsWidgetData {
            val prefs = context.getSharedPreferences(ZatoonaBridge.PREFS_NAME, Context.MODE_PRIVATE)
            val cachedJson = prefs.getString(ZatoonaBridge.KEY_DAILY_HABITS_CACHE, null)
            if (cachedJson.isNullOrBlank()) {
                return DailyHabitsWidgetData(
                    totalCount = 0,
                    doneCount = 0,
                    habits = emptyList(),
                    hasData = false
                )
            }

            return try {
                val obj = JSONObject(cachedJson)
                val totalCount = obj.optInt("totalCount", 0)
                val doneCount = obj.optInt("doneCount", 0)
                val habitsArray = obj.optJSONArray("habits")
                val habitList = mutableListOf<HabitItem>()

                if (habitsArray != null) {
                    for (i in 0 until habitsArray.length()) {
                        val item = habitsArray.optJSONObject(i) ?: continue
                        val title = item.optString("title", "").trim()
                        val streak = item.optInt("streak", 0)
                        val done = item.optBoolean("done", false)
                        if (title.isNotEmpty()) {
                            habitList.add(HabitItem(title = title, streak = streak, done = done))
                        }
                    }
                }

                DailyHabitsWidgetData(
                    totalCount = if (totalCount > 0) totalCount else habitList.size,
                    doneCount = doneCount,
                    habits = habitList,
                    hasData = true
                )
            } catch (e: Exception) {
                DailyHabitsWidgetData(
                    totalCount = 0,
                    doneCount = 0,
                    habits = emptyList(),
                    hasData = false
                )
            }
        }

        fun updateAppWidget(
            context: Context,
            appWidgetManager: AppWidgetManager,
            appWidgetId: Int
        ) {
            val data = loadWidgetData(context)
            val views = RemoteViews(context.packageName, R.layout.widget_daily_habits)

            // Slot identifiers
            val slotRowIds = intArrayOf(
                R.id.widget_habit_row_1,
                R.id.widget_habit_row_2,
                R.id.widget_habit_row_3
            )
            val slotStatusIds = intArrayOf(
                R.id.widget_habit_status_1,
                R.id.widget_habit_status_2,
                R.id.widget_habit_status_3
            )
            val slotTitleIds = intArrayOf(
                R.id.widget_habit_title_1,
                R.id.widget_habit_title_2,
                R.id.widget_habit_title_3
            )
            val slotStreakIds = intArrayOf(
                R.id.widget_habit_streak_1,
                R.id.widget_habit_streak_2,
                R.id.widget_habit_streak_3
            )

            if (data.hasData && data.totalCount > 0) {
                views.setTextViewText(R.id.widget_habits_badge, "${data.doneCount} / ${data.totalCount}")
                val progress = if (data.totalCount > 0) (data.doneCount * 100) / data.totalCount else 0
                views.setProgressBar(R.id.widget_habits_progress_bar, 100, progress, false)
                views.setViewVisibility(R.id.widget_habits_empty, View.GONE)

                for (i in 0 until 3) {
                    if (i < data.habits.size) {
                        val habit = data.habits[i]
                        views.setViewVisibility(slotRowIds[i], View.VISIBLE)
                        views.setTextViewText(slotStatusIds[i], if (habit.done) "✅" else "⚪")
                        views.setTextViewText(slotTitleIds[i], habit.title)
                        views.setTextViewText(slotStreakIds[i], if (habit.streak > 0) "🔥 ${habit.streak}" else "")
                    } else {
                        views.setViewVisibility(slotRowIds[i], View.GONE)
                    }
                }
            } else if (data.hasData && data.totalCount == 0) {
                views.setTextViewText(R.id.widget_habits_badge, "0 / 0")
                views.setProgressBar(R.id.widget_habits_progress_bar, 100, 0, false)
                views.setViewVisibility(R.id.widget_habits_empty, View.VISIBLE)
                views.setTextViewText(R.id.widget_habits_empty, context.getString(R.string.widget_habits_empty))
                for (rowId in slotRowIds) {
                    views.setViewVisibility(rowId, View.GONE)
                }
            } else {
                views.setTextViewText(R.id.widget_habits_badge, "—")
                views.setProgressBar(R.id.widget_habits_progress_bar, 100, 0, false)
                views.setViewVisibility(R.id.widget_habits_empty, View.VISIBLE)
                views.setTextViewText(R.id.widget_habits_empty, "افتح زتونة لمزامنة عادات اليوم")
                for (rowId in slotRowIds) {
                    views.setViewVisibility(rowId, View.GONE)
                }
            }

            // Click pending intent -> MainActivity with mode "schedule"
            val intent = Intent(context, MainActivity::class.java).apply {
                flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TOP
                putExtra(ZatoonaNotificationManager.EXTRA_MODE, "schedule")
            }
            val pendingIntent = PendingIntent.getActivity(
                context,
                REQUEST_CODE_HABITS_WIDGET,
                intent,
                PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
            )
            views.setOnClickPendingIntent(R.id.widget_habits_root, pendingIntent)

            appWidgetManager.updateAppWidget(appWidgetId, views)
        }

        fun updateAllWidgets(context: Context) {
            try {
                val appWidgetManager = AppWidgetManager.getInstance(context)
                val component = ComponentName(context, DailyHabitsWidgetProvider::class.java)
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
