package com.zatoona.app

import android.content.Context
import android.content.SharedPreferences
import android.os.Build
import android.webkit.JavascriptInterface
import org.json.JSONArray
import org.json.JSONException
import org.json.JSONObject

/**
 * ZatoonaBridge
 * Secure, versioned JavaScript bridge contract for Zatoona native shell.
 *
 * Responsibilities:
 * - Accepts upcoming alarm definitions from the PWA (v1 backward-compatible).
 * - Accepts persistent recurring schedule definitions (v2 local alarm engine).
 * - Schedules alarms via AlarmManager (setExactAndAllowWhileIdle with graceful fallback).
 * - Provides queryable engine status and permissions state.
 */
class ZatoonaBridge(private val context: Context) {

    companion object {
        const val BRIDGE_NAME = "ZatoonaNativeBridge"
        const val SCHEMA_VERSION = "v1"
        const val SCHEMA_VERSION_V2 = "v2"
        const val PREFS_NAME = "zatoona_alarms_prefs"
        const val KEY_ALARMS_CACHE = "cached_upcoming_alarms_v1"
        const val MAX_PAYLOAD_LENGTH = 131072 // 128 KB
        const val MAX_ALARM_ITEMS = 60
        const val MAX_TITLE_LENGTH = 120
        const val MAX_BODY_LENGTH = 300
        const val MAX_ID_LENGTH = 80

        val ALLOWED_TYPES = setOf("prayer", "sleep", "activity", "custom")
        val ALLOWED_MODES = setOf(
            "home", "meal", "gym", "sleep", "prayer", "schedule",
            "recovery", "overview", "search", "budget", "notes", "stretches"
        )
        val ID_REGEX = Regex("^[a-zA-Z0-9_\\-:]+$")
    }

    private val prefs: SharedPreferences by lazy {
        context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
    }

    private val repository by lazy { ZatoonaScheduleRepository(context) }
    private val scheduler by lazy { ZatoonaAlarmScheduler(context) }
    private val notificationManager by lazy { ZatoonaNotificationManager(context) }

    /**
     * V1 Backward-Compatible Alarm Sync:
     * Accepts a list of upcoming alarm objects and registers them with AlarmManager.
     */
    @JavascriptInterface
    fun syncUpcomingAlarms(payloadJson: String?): String {
        val result = JSONObject()
        try {
            if (payloadJson == null || payloadJson.isBlank()) {
                return errorResponse("EMPTY_PAYLOAD", "Payload cannot be null or empty.")
            }

            if (payloadJson.length > MAX_PAYLOAD_LENGTH) {
                return errorResponse("PAYLOAD_OVERSIZED", "Payload exceeds maximum allowed size (128 KB).")
            }

            val array = try {
                JSONArray(payloadJson)
            } catch (e: JSONException) {
                return errorResponse("INVALID_JSON", "Payload is not a valid JSON array: ${e.message}")
            }

            if (array.length() > MAX_ALARM_ITEMS) {
                return errorResponse("TOO_MANY_ITEMS", "Alarm count exceeds maximum limit (${MAX_ALARM_ITEMS}).")
            }

            val validatedList = JSONArray()
            val nowMs = System.currentTimeMillis()
            val maxFutureMs = nowMs + (35L * 24 * 60 * 60 * 1000) // max 35 days in future

            for (i in 0 until array.length()) {
                val item = array.optJSONObject(i)
                    ?: return errorResponse("INVALID_ITEM", "Item at index $i is not a JSON object.")

                val version = item.optString("schemaVersion", SCHEMA_VERSION)
                if (version != SCHEMA_VERSION && version != SCHEMA_VERSION_V2) {
                    return errorResponse("UNSUPPORTED_SCHEMA", "Item at index $i has unsupported schemaVersion: $version")
                }

                val id = item.optString("id", "").trim()
                if (id.isEmpty() || id.length > MAX_ID_LENGTH || !ID_REGEX.matches(id)) {
                    return errorResponse("INVALID_ID", "Item at index $i has invalid or missing ID.")
                }

                val type = item.optString("type", "").trim().lowercase()
                if (!ALLOWED_TYPES.contains(type)) {
                    return errorResponse("INVALID_TYPE", "Item at index $i has disallowed type: $type")
                }

                val title = item.optString("title", "").trim()
                if (title.isEmpty() || title.length > MAX_TITLE_LENGTH) {
                    return errorResponse("INVALID_TITLE", "Item at index $i has invalid title length.")
                }

                val body = item.optString("body", "").trim()
                if (body.length > MAX_BODY_LENGTH) {
                    return errorResponse("INVALID_BODY", "Item at index $i has body exceeding maximum length.")
                }

                val triggerEpochMs = item.optLong("triggerEpochMs", -1L)
                if (triggerEpochMs <= 0 || triggerEpochMs > maxFutureMs) {
                    return errorResponse("INVALID_TIMESTAMP", "Item at index $i has trigger timestamp out of bounds.")
                }

                val mode = item.optString("mode", "home").trim().lowercase()
                if (!ALLOWED_MODES.contains(mode)) {
                    return errorResponse("INVALID_MODE", "Item at index $i has disallowed mode route: $mode")
                }

                val channelId = item.optString("channelId", "zatoona_reminders").trim()

                val cleanItem = JSONObject().apply {
                    put("schemaVersion", SCHEMA_VERSION)
                    put("id", id)
                    put("type", type)
                    put("title", title)
                    put("body", body)
                    put("triggerEpochMs", triggerEpochMs)
                    put("mode", mode)
                    put("channelId", channelId)
                }
                validatedList.put(cleanItem)

                // Schedule native alarm in AlarmManager
                val schedule = ZatoonaSchedule(
                    id = id,
                    type = type,
                    title = title,
                    body = body,
                    mode = mode,
                    channelId = channelId,
                    recurrence = "once",
                    triggerEpochMs = triggerEpochMs,
                    enabled = true,
                    schemaVersion = SCHEMA_VERSION
                )
                repository.putSchedule(schedule)
                scheduler.scheduleAlarm(schedule)
            }

            // Save validated alarms cache locally
            prefs.edit().putString(KEY_ALARMS_CACHE, validatedList.toString()).apply()

            result.put("status", "ok")
            result.put("schemaVersion", SCHEMA_VERSION)
            result.put("syncedCount", validatedList.length())
            result.put("timestamp", nowMs)
            return result.toString()

        } catch (t: Throwable) {
            return errorResponse("INTERNAL_ERROR", "Bridge synchronization error occurred: ${t.message}")
        }
    }

    /**
     * V2 Rich Persistent Schedule Sync:
     * Accepts recurring schedules (daily, weekdays, sleep_routine, prayer_dated, once).
     */
    @JavascriptInterface
    fun syncSchedules(payloadJson: String?): String {
        val result = JSONObject()
        try {
            if (payloadJson == null || payloadJson.isBlank()) {
                return errorResponse("EMPTY_PAYLOAD", "Payload cannot be null or empty.")
            }

            if (payloadJson.length > MAX_PAYLOAD_LENGTH) {
                return errorResponse("PAYLOAD_OVERSIZED", "Payload exceeds maximum allowed size (128 KB).")
            }

            val array = try {
                JSONArray(payloadJson)
            } catch (e: JSONException) {
                return errorResponse("INVALID_JSON", "Payload is not a valid JSON array: ${e.message}")
            }

            if (array.length() > MAX_ALARM_ITEMS) {
                return errorResponse("TOO_MANY_ITEMS", "Schedule count exceeds maximum limit (${MAX_ALARM_ITEMS}).")
            }

            val nowMs = System.currentTimeMillis()
            var scheduledCount = 0
            val incomingIds = mutableSetOf<String>()

            for (i in 0 until array.length()) {
                val item = array.optJSONObject(i)
                    ?: return errorResponse("INVALID_ITEM", "Item at index $i is not a JSON object.")

                val id = item.optString("id", "").trim()
                if (id.isEmpty() || id.length > MAX_ID_LENGTH || !ID_REGEX.matches(id)) {
                    return errorResponse("INVALID_ID", "Item at index $i has invalid ID: '$id'")
                }
                incomingIds.add(id)

                val type = item.optString("type", "custom").trim().lowercase()
                if (!ALLOWED_TYPES.contains(type)) {
                    return errorResponse("INVALID_TYPE", "Item at index $i has disallowed type: $type")
                }

                val title = item.optString("title", "").trim()
                if (title.isEmpty() || title.length > MAX_TITLE_LENGTH) {
                    return errorResponse("INVALID_TITLE", "Item at index $i has invalid title length.")
                }

                val body = item.optString("body", "").trim()
                if (body.length > MAX_BODY_LENGTH) {
                    return errorResponse("INVALID_BODY", "Item at index $i has body exceeding maximum length.")
                }

                val mode = item.optString("mode", "home").trim().lowercase()
                if (!ALLOWED_MODES.contains(mode)) {
                    return errorResponse("INVALID_MODE", "Item at index $i has disallowed mode route: $mode")
                }

                val recurrence = item.optString("recurrence", "once").trim().lowercase()
                val timeHour = item.optInt("timeHour", -1)
                val timeMinute = item.optInt("timeMinute", -1)
                val triggerEpochMs = item.optLong("triggerEpochMs", 0L)
                val city = item.optString("city", "").trim()
                val enabled = item.optBoolean("enabled", true)
                val channelId = item.optString("channelId", "zatoona_reminders").trim()

                val activeDays = mutableListOf<Boolean>()
                val daysArr = item.optJSONArray("activeDays")
                if (daysArr != null) {
                    for (d in 0 until daysArr.length()) {
                        activeDays.add(daysArr.optBoolean(d, false))
                    }
                }

                val datedTimings = mutableMapOf<String, Long>()
                val timingsObj = item.optJSONObject("datedTimings")
                if (timingsObj != null) {
                    val keys = timingsObj.keys()
                    while (keys.hasNext()) {
                        val k = keys.next()
                        val v = timingsObj.optLong(k, 0L)
                        if (v > 0) datedTimings[k] = v
                    }
                }

                val schedule = ZatoonaSchedule(
                    id = id,
                    type = type,
                    title = title,
                    body = body,
                    mode = mode,
                    channelId = channelId,
                    recurrence = recurrence,
                    timeHour = timeHour,
                    timeMinute = timeMinute,
                    activeDays = activeDays,
                    triggerEpochMs = triggerEpochMs,
                    datedTimings = datedTimings,
                    city = city,
                    enabled = enabled,
                    schemaVersion = SCHEMA_VERSION_V2
                )

                repository.putSchedule(schedule)
                if (enabled) {
                    if (scheduler.scheduleAlarm(schedule)) {
                        scheduledCount++
                    }
                } else {
                    scheduler.cancelAlarm(id)
                }
            }

            // Cancel and remove any previously persisted schedules that were omitted from this sync
            val allSchedules = repository.getAllSchedules()
            for (oldSched in allSchedules) {
                if (!incomingIds.contains(oldSched.id)) {
                    scheduler.cancelAlarm(oldSched.id)
                    repository.deleteSchedule(oldSched.id)
                }
            }

            result.put("status", "ok")
            result.put("schemaVersion", SCHEMA_VERSION_V2)
            result.put("syncedCount", array.length())
            result.put("scheduledCount", scheduledCount)
            result.put("timestamp", nowMs)

            // Refresh home-screen Next Prayer widgets if prayer schedules were updated
            NextPrayerWidgetProvider.updateAllWidgets(context)

            return result.toString()

        } catch (t: Throwable) {
            return errorResponse("INTERNAL_ERROR", "Bridge syncSchedules error: ${t.message}")
        }
    }

    @JavascriptInterface
    fun cancelSchedule(scheduleId: String?): String {
        if (scheduleId.isNullOrBlank()) {
            return errorResponse("INVALID_ID", "Schedule ID cannot be empty.")
        }
        val cleanId = scheduleId.trim()
        scheduler.cancelAlarm(cleanId)
        repository.deleteSchedule(cleanId)

        return JSONObject().apply {
            put("status", "ok")
            put("cancelledId", cleanId)
            put("timestamp", System.currentTimeMillis())
        }.toString()
    }

    @JavascriptInterface
    fun updateActivePrayerCity(city: String?): String {
        if (city.isNullOrBlank()) {
            return errorResponse("INVALID_CITY", "City cannot be empty.")
        }
        val cleanCity = city.trim()
        val staleSchedules = repository.purgeStaleCityPrayers(cleanCity)
        staleSchedules.forEach { scheduler.cancelAlarm(it.id) }

        // Refresh home-screen Next Prayer widgets with newly selected city
        NextPrayerWidgetProvider.updateAllWidgets(context)

        return JSONObject().apply {
            put("status", "ok")
            put("activeCity", cleanCity)
            put("purgedStaleCount", staleSchedules.size)
            put("timestamp", System.currentTimeMillis())
        }.toString()
    }

    @JavascriptInterface
    fun getAlarmEngineStatus(): String {
        return JSONObject().apply {
            put("status", "ok")
            put("notificationsEnabled", notificationManager.areNotificationsEnabled())
            put("exactAlarmsAllowed", scheduler.canScheduleExactAlarms())
            put("activeScheduleCount", repository.getAllSchedules().count { it.enabled })
            put("activeCity", repository.getActivePrayerCity())
            put("sdkVersion", Build.VERSION.SDK_INT)
            put("timestamp", System.currentTimeMillis())
        }.toString()
    }

    private fun errorResponse(code: String, message: String): String {
        return JSONObject().apply {
            put("status", "error")
            put("code", code)
            put("message", message)
            put("timestamp", System.currentTimeMillis())
        }.toString()
    }
}
