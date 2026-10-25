package com.zatoona.app

import org.json.JSONArray
import org.json.JSONObject

/**
 * ZatoonaSchedule
 * Represents a persistent schedule definition in the native alarm engine.
 */
data class ZatoonaSchedule(
    val id: String,
    val type: String,              // "prayer", "sleep", "activity", "custom"
    val title: String,
    val body: String,
    val mode: String = "home",     // Whitelisted route mode
    val channelId: String = "zatoona_reminders",
    val recurrence: String = "once", // "once", "daily", "weekdays", "prayer_dated", "sleep_routine"
    val timeHour: Int = -1,        // 0-23
    val timeMinute: Int = -1,      // 0-59
    val activeDays: List<Boolean> = emptyList(), // Sun=0..Sat=6 (length 7)
    val triggerEpochMs: Long = 0L, // Next trigger epoch timestamp
    val datedTimings: Map<String, Long> = emptyMap(), // ISO date -> trigger epoch ms for dated prayers
    val city: String = "",
    val enabled: Boolean = true,
    val schemaVersion: String = "v2"
) {
    fun toJSONObject(): JSONObject {
        return JSONObject().apply {
            put("id", id)
            put("type", type)
            put("title", title)
            put("body", body)
            put("mode", mode)
            put("channelId", channelId)
            put("recurrence", recurrence)
            put("timeHour", timeHour)
            put("timeMinute", timeMinute)
            put("triggerEpochMs", triggerEpochMs)
            put("city", city)
            put("enabled", enabled)
            put("schemaVersion", schemaVersion)

            if (activeDays.isNotEmpty()) {
                val daysArr = JSONArray()
                activeDays.forEach { daysArr.put(it) }
                put("activeDays", daysArr)
            }

            if (datedTimings.isNotEmpty()) {
                val timingsObj = JSONObject()
                datedTimings.forEach { (k, v) -> timingsObj.put(k, v) }
                put("datedTimings", timingsObj)
            }
        }
    }

    companion object {
        fun fromJSONObject(json: JSONObject): ZatoonaSchedule? {
            val id = json.optString("id", "").trim()
            if (id.isEmpty()) return null

            val type = json.optString("type", "custom").trim().lowercase()
            val title = json.optString("title", "تذكير").trim()
            val body = json.optString("body", "").trim()
            val mode = json.optString("mode", "home").trim().lowercase()
            val channelId = json.optString("channelId", "zatoona_reminders").trim()
            val recurrence = json.optString("recurrence", "once").trim().lowercase()
            val timeHour = json.optInt("timeHour", -1)
            val timeMinute = json.optInt("timeMinute", -1)
            val triggerEpochMs = json.optLong("triggerEpochMs", 0L)
            val city = json.optString("city", "").trim()
            val enabled = json.optBoolean("enabled", true)
            val schemaVersion = json.optString("schemaVersion", "v2")

            val activeDays = mutableListOf<Boolean>()
            val daysArr = json.optJSONArray("activeDays")
            if (daysArr != null) {
                for (i in 0 until daysArr.length()) {
                    activeDays.add(daysArr.optBoolean(i, false))
                }
            }

            val datedTimings = mutableMapOf<String, Long>()
            val timingsObj = json.optJSONObject("datedTimings")
            if (timingsObj != null) {
                val keys = timingsObj.keys()
                while (keys.hasNext()) {
                    val k = keys.next()
                    val v = timingsObj.optLong(k, 0L)
                    if (v > 0) datedTimings[k] = v
                }
            }

            return ZatoonaSchedule(
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
                schemaVersion = schemaVersion
            )
        }
    }
}
