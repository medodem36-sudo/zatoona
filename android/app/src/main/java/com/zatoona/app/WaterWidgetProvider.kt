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
 * WaterWidgetProvider
 * Interactive Native Android Home-Screen Widget for logging and tracking hydration.
 * Allows +250ml, +500ml, and -250ml logging directly on the home screen without opening the app,
 * and automatically synchronizes with the app's nutrition engine.
 */
class WaterWidgetProvider : AppWidgetProvider() {

    data class WaterWidgetData(
        val waterMl: Int,
        val targetMl: Int,
        val dateIso: String
    )

    companion object {
        const val ACTION_ADD_WATER = "com.zatoona.app.ACTION_ADD_WATER"
        const val EXTRA_AMOUNT = "extra_amount"

        const val REQUEST_CODE_WATER_ROOT = 4001
        const val REQUEST_CODE_WATER_ADD_250 = 4002
        const val REQUEST_CODE_WATER_ADD_500 = 4003
        const val REQUEST_CODE_WATER_SUB_250 = 4004

        private val isoDateFormat = SimpleDateFormat("yyyy-MM-dd", Locale.US)

        fun getTodayIso(): String = isoDateFormat.format(Date())

        fun loadWidgetData(context: Context): WaterWidgetData {
            val prefs = context.getSharedPreferences(ZatoonaBridge.PREFS_NAME, Context.MODE_PRIVATE)
            val cachedJson = prefs.getString(ZatoonaBridge.KEY_WATER_CACHE, null)
            val today = getTodayIso()

            if (cachedJson.isNullOrBlank()) {
                return WaterWidgetData(waterMl = 0, targetMl = 3000, dateIso = today)
            }

            return try {
                val obj = JSONObject(cachedJson)
                val date = obj.optString("date", today)
                if (date != today) {
                    // New day: reset daily count
                    WaterWidgetData(waterMl = 0, targetMl = 3000, dateIso = today)
                } else {
                    val amount = obj.optInt("waterMl", 0)
                    val target = obj.optInt("targetMl", 3000).coerceAtLeast(1000)
                    WaterWidgetData(waterMl = amount, targetMl = target, dateIso = today)
                }
            } catch (e: Exception) {
                WaterWidgetData(waterMl = 0, targetMl = 3000, dateIso = today)
            }
        }

        fun saveWidgetData(context: Context, data: WaterWidgetData) {
            val prefs = context.getSharedPreferences(ZatoonaBridge.PREFS_NAME, Context.MODE_PRIVATE)
            val obj = JSONObject().apply {
                put("date", data.dateIso)
                put("waterMl", data.waterMl)
                put("targetMl", data.targetMl)
                put("timestamp", System.currentTimeMillis())
            }
            prefs.edit().putString(ZatoonaBridge.KEY_WATER_CACHE, obj.toString()).apply()
        }

        fun buildWaterBroadcastPendingIntent(
            context: Context,
            amount: Int,
            requestCode: Int
        ): PendingIntent {
            val intent = Intent(context, WaterWidgetProvider::class.java).apply {
                action = ACTION_ADD_WATER
                putExtra(EXTRA_AMOUNT, amount)
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
            val views = RemoteViews(context.packageName, R.layout.widget_water)

            views.setTextViewText(R.id.widget_water_amount_display, "${data.waterMl} / ${data.targetMl} مل")
            views.setTextViewText(R.id.widget_water_target_badge, "الهدف: ${data.targetMl} مل")

            val percent = if (data.targetMl > 0) {
                ((data.waterMl.toDouble() / data.targetMl.toDouble()) * 100).toInt().coerceAtMost(200)
            } else 0
            views.setTextViewText(R.id.widget_water_percent_display, "$percent%")

            // Set interactive BroadcastPendingIntents on buttons
            val add250Pending = buildWaterBroadcastPendingIntent(context, 250, REQUEST_CODE_WATER_ADD_250)
            val add500Pending = buildWaterBroadcastPendingIntent(context, 500, REQUEST_CODE_WATER_ADD_500)
            val sub250Pending = buildWaterBroadcastPendingIntent(context, -250, REQUEST_CODE_WATER_SUB_250)

            views.setOnClickPendingIntent(R.id.widget_water_btn_add250, add250Pending)
            views.setOnClickPendingIntent(R.id.widget_water_btn_add500, add500Pending)
            views.setOnClickPendingIntent(R.id.widget_water_btn_sub250, sub250Pending)

            // 1-tap on root navigates to meal/nutrition section
            val rootPending = buildNavigationPendingIntent(context, "meal", REQUEST_CODE_WATER_ROOT)
            views.setOnClickPendingIntent(R.id.widget_water_root, rootPending)

            appWidgetManager.updateAppWidget(appWidgetId, views)
        }

        fun updateAllWidgets(context: Context) {
            val appWidgetManager = AppWidgetManager.getInstance(context)
            val componentName = ComponentName(context, WaterWidgetProvider::class.java)
            val appWidgetIds = appWidgetManager.getAppWidgetIds(componentName)
            for (appWidgetId in appWidgetIds) {
                updateAppWidget(context, appWidgetManager, appWidgetId)
            }
        }
    }

    override fun onReceive(context: Context, intent: Intent) {
        super.onReceive(context, intent)
        if (intent.action == ACTION_ADD_WATER) {
            val delta = intent.getIntExtra(EXTRA_AMOUNT, 250)
            val current = loadWidgetData(context)
            val newAmount = (current.waterMl + delta).coerceIn(0, 10000)
            val updated = current.copy(waterMl = newAmount, dateIso = getTodayIso())
            saveWidgetData(context, updated)
            updateAllWidgets(context)
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
