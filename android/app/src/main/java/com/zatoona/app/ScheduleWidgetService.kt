package com.zatoona.app

import android.content.Context
import android.content.Intent
import android.graphics.Color
import android.widget.RemoteViews
import android.widget.RemoteViewsService
import org.json.JSONObject

/**
 * ScheduleWidgetService
 * RemoteViewsService providing the data adapter for the scrollable
 * schedule activities and daily tasks ListView inside ScheduleWidgetProvider.
 */
class ScheduleWidgetService : RemoteViewsService() {
    override fun onGetViewFactory(intent: Intent): RemoteViewsFactory {
        return ScheduleRemoteViewsFactory(applicationContext, intent)
    }
}

class ScheduleRemoteViewsFactory(
    private val context: Context,
    private val intent: Intent
) : RemoteViewsService.RemoteViewsFactory {

    data class ScheduleItem(
        val title: String,
        val time: String,
        val isCompleted: Boolean,
        val isActivity: Boolean
    )

    private val items = ArrayList<ScheduleItem>()

    override fun onCreate() {
        loadData()
    }

    override fun onDataSetChanged() {
        loadData()
    }

    override fun onDestroy() {
        items.clear()
    }

    override fun getCount(): Int = items.size

    override fun getViewAt(position: Int): RemoteViews {
        if (position < 0 || position >= items.size) {
            return RemoteViews(context.packageName, R.layout.widget_schedule_item)
        }
        val item = items[position]
        val views = RemoteViews(context.packageName, R.layout.widget_schedule_item)

        views.setTextViewText(R.id.widget_schedule_item_title, item.title)
        views.setTextViewText(R.id.widget_schedule_item_time, item.time)

        if (item.isCompleted) {
            views.setTextViewText(R.id.widget_schedule_item_status, "✓")
            views.setTextColor(R.id.widget_schedule_item_status, Color.parseColor("#34D399"))
            views.setTextColor(R.id.widget_schedule_item_title, Color.parseColor("#94A3B8"))
        } else if (item.isActivity) {
            views.setTextViewText(R.id.widget_schedule_item_status, "⏰")
            views.setTextColor(R.id.widget_schedule_item_status, Color.parseColor("#F59E0B"))
            views.setTextColor(R.id.widget_schedule_item_title, Color.parseColor("#FFFFFF"))
        } else {
            views.setTextViewText(R.id.widget_schedule_item_status, "○")
            views.setTextColor(R.id.widget_schedule_item_status, Color.parseColor("#60A5FA"))
            views.setTextColor(R.id.widget_schedule_item_title, Color.parseColor("#FFFFFF"))
        }

        // Fill-in intent to open schedule section in app
        val fillInIntent = Intent().apply {
            putExtra(ZatoonaNotificationManager.EXTRA_MODE, "schedule")
        }
        views.setOnClickFillInIntent(R.id.widget_schedule_item_root, fillInIntent)

        return views
    }

    override fun getLoadingView(): RemoteViews? = null

    override fun getViewTypeCount(): Int = 1

    override fun getItemId(position: Int): Long = position.toLong()

    override fun hasStableIds(): Boolean = true

    private fun loadData() {
        items.clear()
        val prefs = context.getSharedPreferences(ZatoonaBridge.PREFS_NAME, Context.MODE_PRIVATE)
        val cachedJson = prefs.getString(ZatoonaBridge.KEY_SCHEDULE_CACHE, null)
        if (cachedJson.isNullOrBlank()) {
            return
        }
        try {
            val obj = JSONObject(cachedJson)
            val itemsArray = obj.optJSONArray("items")
            if (itemsArray != null) {
                for (i in 0 until itemsArray.length()) {
                    val itObj = itemsArray.getJSONObject(i)
                    val title = itObj.optString("title", "")
                    val time = itObj.optString("time", "")
                    val completed = itObj.optBoolean("completed", false)
                    val isActivity = itObj.optBoolean("isActivity", false)
                    if (title.isNotBlank()) {
                        items.add(ScheduleItem(title, time, completed, isActivity))
                    }
                }
            }
        } catch (e: Exception) {
            // keep items empty on malformed cache
        }
    }
}
