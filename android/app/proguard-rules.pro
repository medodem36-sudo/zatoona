# Keep JavaScript interface methods from being stripped or obfuscated
-keepclassmembers class * {
    @android.webkit.JavascriptInterface <methods>;
}

# Keep Zatoona bridge classes
-keep class com.zatoona.app.ZatoonaBridge { *; }

# Keep QuickAccessWidgetProvider
-keep class com.zatoona.app.QuickAccessWidgetProvider { *; }

# Keep NextPrayerWidgetProvider
-keep class com.zatoona.app.NextPrayerWidgetProvider { *; }

# Keep DailyHabitsWidgetProvider
-keep class com.zatoona.app.DailyHabitsWidgetProvider { *; }

# Keep StudyWidgetProvider and Quick Settings Tile Services (Phase 7)
-keep class com.zatoona.app.StudyWidgetProvider { *; }
-keep class com.zatoona.app.ZatoonaStudyTileService { *; }
-keep class com.zatoona.app.ZatoonaGymTileService { *; }

# Keep AllInOneDailyWidgetProvider (Package F / Feature 88)
-keep class com.zatoona.app.AllInOneDailyWidgetProvider { *; }
# Keep WaterWidgetProvider & ScheduleWidgetProvider
-keep class com.zatoona.app.WaterWidgetProvider { *; }
-keep class com.zatoona.app.ScheduleWidgetProvider { *; }
-keep class com.zatoona.app.ScheduleWidgetService { *; }
-keep class com.zatoona.app.ScheduleRemoteViewsFactory { *; }

# Keep Alarm, Boot & Foreground Services (Phase 22)
-keep class com.zatoona.app.AlarmService { *; }
-keep class com.zatoona.app.AlarmReceiver { *; }
-keep class com.zatoona.app.BootReceiver { *; }
-keep class com.zatoona.app.AlarmActivity { *; }
-keep class com.zatoona.app.FloatingStudyBubbleService { *; }
-keep class com.zatoona.app.ZatoonaAlarmScheduler { *; }
-keep class com.zatoona.app.ZatoonaNotificationManager { *; }
