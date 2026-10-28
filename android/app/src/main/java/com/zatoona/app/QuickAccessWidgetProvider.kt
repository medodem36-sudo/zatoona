package com.zatoona.app

import android.app.PendingIntent
import android.appwidget.AppWidgetManager
import android.appwidget.AppWidgetProvider
import android.content.Context
import android.content.Intent
import android.widget.RemoteViews

/**
 * QuickAccessWidgetProvider
 * Native Android Home-Screen Widget (Phase 13.5 / Proposal #7)
 * Provides 1-tap direct access to core Zatoona application modules:
 * - Prayer (الصلوات)
 * - Gym & Exercises (التمارين)
 * - Nutrition & Meals (التغذية)
 * - Daily Schedule & Habits (الجدول)
 */
class QuickAccessWidgetProvider : AppWidgetProvider() {

    companion object {
        const val REQUEST_CODE_HOME = 1001
        const val REQUEST_CODE_PRAYER = 1002
        const val REQUEST_CODE_GYM = 1003
        const val REQUEST_CODE_MEAL = 1004
        const val REQUEST_CODE_SCHEDULE = 1005

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
            val views = RemoteViews(context.packageName, R.layout.widget_quick_access)

            // Header tap -> opens home view
            views.setOnClickPendingIntent(
                R.id.widget_header,
                buildNavigationPendingIntent(context, "home", REQUEST_CODE_HOME)
            )

            // Prayer button -> opens prayer view
            views.setOnClickPendingIntent(
                R.id.widget_btn_prayer,
                buildNavigationPendingIntent(context, "prayer", REQUEST_CODE_PRAYER)
            )

            // Gym button -> opens gym view
            views.setOnClickPendingIntent(
                R.id.widget_btn_gym,
                buildNavigationPendingIntent(context, "gym", REQUEST_CODE_GYM)
            )

            // Nutrition / Meal button -> opens meal view
            views.setOnClickPendingIntent(
                R.id.widget_btn_meal,
                buildNavigationPendingIntent(context, "meal", REQUEST_CODE_MEAL)
            )

            // Schedule button -> opens schedule view
            views.setOnClickPendingIntent(
                R.id.widget_btn_schedule,
                buildNavigationPendingIntent(context, "schedule", REQUEST_CODE_SCHEDULE)
            )

            appWidgetManager.updateAppWidget(appWidgetId, views)
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
