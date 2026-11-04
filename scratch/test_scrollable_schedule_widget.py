import os
import re

def test_scrollable_schedule_widget():
    print("=== TESTING SCROLLABLE SCHEDULE WIDGET SUITE ===")
    
    # 1. Check layout files
    layout_path = "android/app/src/main/res/layout/widget_schedule.xml"
    assert os.path.exists(layout_path), "widget_schedule.xml must exist"
    layout_txt = open(layout_path, encoding='utf-8').read()
    assert "widget_schedule_list" in layout_txt, "ListView id widget_schedule_list must exist in widget_schedule.xml"
    assert "widget_schedule_empty_view" in layout_txt, "widget_schedule_empty_view must exist in widget_schedule.xml"
    print("  [PASS] widget_schedule.xml contains ListView and empty view")

    # 2. Check item layout
    item_path = "android/app/src/main/res/layout/widget_schedule_item.xml"
    assert os.path.exists(item_path), "widget_schedule_item.xml must exist"
    item_txt = open(item_path, encoding='utf-8').read()
    assert "widget_schedule_item_root" in item_txt, "widget_schedule_item_root must exist"
    assert "widget_schedule_item_status" in item_txt, "widget_schedule_item_status must exist"
    assert "widget_schedule_item_title" in item_txt, "widget_schedule_item_title must exist"
    assert "widget_schedule_item_time" in item_txt, "widget_schedule_item_time must exist"
    print("  [PASS] widget_schedule_item.xml contains complete item views")

    # 3. Check ScheduleWidgetService.kt
    service_path = "android/app/src/main/java/com/zatoona/app/ScheduleWidgetService.kt"
    assert os.path.exists(service_path), "ScheduleWidgetService.kt must exist"
    service_txt = open(service_path, encoding='utf-8').read()
    assert "class ScheduleWidgetService : RemoteViewsService()" in service_txt, "ScheduleWidgetService must extend RemoteViewsService"
    assert "class ScheduleRemoteViewsFactory" in service_txt, "ScheduleRemoteViewsFactory must exist"
    assert "R.layout.widget_schedule_item" in service_txt, "Factory must inflate widget_schedule_item"
    assert "KEY_SCHEDULE_CACHE" in service_txt, "Factory must read from KEY_SCHEDULE_CACHE"
    print("  [PASS] ScheduleWidgetService.kt implements collection adapter")

    # 4. Check ScheduleWidgetProvider.kt
    provider_path = "android/app/src/main/java/com/zatoona/app/ScheduleWidgetProvider.kt"
    assert os.path.exists(provider_path), "ScheduleWidgetProvider.kt must exist"
    provider_txt = open(provider_path, encoding='utf-8').read()
    assert "ScheduleWidgetService::class.java" in provider_txt, "Provider must reference ScheduleWidgetService"
    assert "setRemoteAdapter" in provider_txt, "Provider must call setRemoteAdapter"
    assert "setPendingIntentTemplate" in provider_txt, "Provider must configure item click template"
    assert "notifyAppWidgetViewDataChanged" in provider_txt, "Provider must notify ListView data changed"
    print("  [PASS] ScheduleWidgetProvider.kt configures ListView collection and update notifications")

    # 5. Check AndroidManifest.xml
    manifest_path = "android/app/src/main/AndroidManifest.xml"
    manifest_txt = open(manifest_path, encoding='utf-8').read()
    assert "android:name=\".ScheduleWidgetService\"" in manifest_txt, "ScheduleWidgetService must be registered in AndroidManifest.xml"
    assert "android:permission=\"android.permission.BIND_REMOTEVIEWS\"" in manifest_txt, "BIND_REMOTEVIEWS permission required"
    print("  [PASS] AndroidManifest.xml registers ScheduleWidgetService with BIND_REMOTEVIEWS")

    # 6. Check proguard-rules.pro
    proguard_path = "android/app/proguard-rules.pro"
    proguard_txt = open(proguard_path, encoding='utf-8').read()
    assert "-keep class com.zatoona.app.ScheduleWidgetService" in proguard_txt, "ScheduleWidgetService kept in ProGuard"
    assert "-keep class com.zatoona.app.ScheduleRemoteViewsFactory" in proguard_txt, "ScheduleRemoteViewsFactory kept in ProGuard"
    print("  [PASS] proguard-rules.pro preserves ScheduleWidgetService and RemoteViewsFactory")

    # 7. Check frontend sync in index.html
    html_txt = open("index.html", encoding='utf-8').read()
    assert "function syncScheduleToNativeWidget()" in html_txt, "syncScheduleToNativeWidget must exist"
    assert "isActivity: true" in html_txt, "Must include timeline activities in widget sync"
    assert "isActivity: false" in html_txt, "Must include checklist tasks in widget sync"
    assert "items: widgetItems" in html_txt, "Must pass items array in payload"
    print("  [PASS] index.html syncs both activities and tasks to the native widget")

    # 8. Check 3-way parity
    import hashlib
    h_idx = hashlib.sha256(open("index.html", "rb").read()).hexdigest()
    h_zat = hashlib.sha256(open("zatoona.html", "rb").read()).hexdigest()
    h_ast = hashlib.sha256(open("android/app/src/main/assets/index.html", "rb").read()).hexdigest()
    assert h_idx == h_zat == h_ast, f"Parity mismatch! idx={h_idx}, zat={h_zat}, ast={h_ast}"
    print(f"  [PASS] 3-way HTML parity verified (SHA256: {h_idx})")

    print("\nALL 8 SCROLLABLE SCHEDULE WIDGET CHECKS PASSED 100%!")

if __name__ == '__main__':
    test_scrollable_schedule_widget()
