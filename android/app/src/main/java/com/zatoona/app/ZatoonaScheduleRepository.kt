package com.zatoona.app

import android.content.Context
import android.content.SharedPreferences
import org.json.JSONArray
import org.json.JSONObject
import java.util.Calendar

/**
 * ZatoonaScheduleRepository
 * Persistent storage and recurrence calculation for native Zatoona alarms.
 */
class ZatoonaScheduleRepository(context: Context) {

    companion object {
        const val PREFS_NAME = "zatoona_alarms_prefs_v2"
        const val KEY_SCHEDULES_MAP = "schedules_definitions_v2"
        const val KEY_DISPATCHED_LOG = "dispatched_reminders_log"
        const val KEY_ACTIVE_CITY = "active_prayer_city"
        const val DEDUP_WINDOW_MS = 15 * 60 * 1000L // 15 minutes suppression window
    }

    private val prefs: SharedPreferences =
        context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)

    @Synchronized
    fun getAllSchedules(): List<ZatoonaSchedule> {
        val jsonStr = prefs.getString(KEY_SCHEDULES_MAP, null) ?: return emptyList()
        val list = mutableListOf<ZatoonaSchedule>()
        try {
            val array = JSONArray(jsonStr)
            for (i in 0 until array.length()) {
                val obj = array.optJSONObject(i) ?: continue
                val sched = ZatoonaSchedule.fromJSONObject(obj)
                if (sched != null) {
                    list.add(sched)
                }
            }
        } catch (e: Exception) {
            // Safe fallback on corrupted JSON
        }
        return list
    }

    @Synchronized
    fun getSchedule(id: String): ZatoonaSchedule? {
        return getAllSchedules().firstOrNull { it.id == id }
    }

    @Synchronized
    fun saveSchedules(schedules: List<ZatoonaSchedule>) {
        val array = JSONArray()
        schedules.forEach { array.put(it.toJSONObject()) }
        prefs.edit().putString(KEY_SCHEDULES_MAP, array.toString()).apply()
    }

    @Synchronized
    fun putSchedule(schedule: ZatoonaSchedule) {
        val current = getAllSchedules().filter { it.id != schedule.id }.toMutableList()
        current.add(schedule)
        saveSchedules(current)
    }

    @Synchronized
    fun deleteSchedule(id: String) {
        val filtered = getAllSchedules().filter { it.id != id }
        saveSchedules(filtered)
    }

    @Synchronized
    fun clearAll() {
        prefs.edit().remove(KEY_SCHEDULES_MAP).apply()
    }

    @Synchronized
    fun getActivePrayerCity(): String {
        return prefs.getString(KEY_ACTIVE_CITY, "Cairo") ?: "Cairo"
    }

    @Synchronized
    fun setActivePrayerCity(city: String) {
        prefs.edit().putString(KEY_ACTIVE_CITY, city).apply()
    }

    @Synchronized
    fun purgeStaleCityPrayers(newCity: String): List<ZatoonaSchedule> {
        val all = getAllSchedules()
        val (stale, kept) = all.partition { it.type == "prayer" && it.city.isNotEmpty() && !it.city.equals(newCity, ignoreCase = true) }
        saveSchedules(kept)
        setActivePrayerCity(newCity)
        return stale
    }

    /**
     * Deduplication: Checks if tag was dispatched within the last 15 minutes.
     */
    @Synchronized
    fun isDuplicateDispatch(tag: String, nowMs: Long): Boolean {
        cleanOldDispatches(nowMs)
        val logStr = prefs.getString(KEY_DISPATCHED_LOG, null) ?: return false
        return try {
            val log = JSONObject(logStr)
            val lastTime = log.optLong(tag, 0L)
            lastTime > 0 && (nowMs - lastTime) < DEDUP_WINDOW_MS
        } catch (e: Exception) {
            false
        }
    }

    @Synchronized
    fun markDispatched(tag: String, nowMs: Long) {
        val logStr = prefs.getString(KEY_DISPATCHED_LOG, null)
        val log = if (logStr != null) {
            try { JSONObject(logStr) } catch (e: Exception) { JSONObject() }
        } else {
            JSONObject()
        }
        log.put(tag, nowMs)
        prefs.edit().putString(KEY_DISPATCHED_LOG, log.toString()).apply()
    }

    private fun cleanOldDispatches(nowMs: Long) {
        val logStr = prefs.getString(KEY_DISPATCHED_LOG, null) ?: return
        try {
            val log = JSONObject(logStr)
            val updated = JSONObject()
            val keys = log.keys()
            val maxAgeMs = 24 * 60 * 60 * 1000L // 24 hours
            while (keys.hasNext()) {
                val k = keys.next()
                val ts = log.optLong(k, 0L)
                if (nowMs - ts < maxAgeMs) {
                    updated.put(k, ts)
                }
            }
            prefs.edit().putString(KEY_DISPATCHED_LOG, updated.toString()).apply()
        } catch (e: Exception) {
            // Ignore clean error
        }
    }

    /**
     * Calculates the next valid trigger timestamp in milliseconds for a schedule.
     */
    fun computeNextOccurrence(schedule: ZatoonaSchedule, afterMs: Long): Long? {
        if (!schedule.enabled) return null

        when (schedule.recurrence.lowercase()) {
            "once" -> {
                return if (schedule.triggerEpochMs > afterMs) schedule.triggerEpochMs else null
            }

            "daily" -> {
                if (schedule.timeHour < 0 || schedule.timeMinute < 0) return null
                val cal = Calendar.getInstance().apply {
                    timeInMillis = afterMs
                    set(Calendar.HOUR_OF_DAY, schedule.timeHour)
                    set(Calendar.MINUTE, schedule.timeMinute)
                    set(Calendar.SECOND, 0)
                    set(Calendar.MILLISECOND, 0)
                }
                if (cal.timeInMillis <= afterMs) {
                    cal.add(Calendar.DAY_OF_YEAR, 1)
                }
                return cal.timeInMillis
            }

            "weekdays", "sleep_routine" -> {
                if (schedule.timeHour < 0 || schedule.timeMinute < 0) return null
                val activeDays = schedule.activeDays
                val allActive = activeDays.isEmpty() || activeDays.none { it }

                for (offset in 0..7) {
                    val cal = Calendar.getInstance().apply {
                        timeInMillis = afterMs
                        add(Calendar.DAY_OF_YEAR, offset)
                        set(Calendar.HOUR_OF_DAY, schedule.timeHour)
                        set(Calendar.MINUTE, schedule.timeMinute)
                        set(Calendar.SECOND, 0)
                        set(Calendar.MILLISECOND, 0)
                    }

                    if (cal.timeInMillis > afterMs) {
                        // Calendar.DAY_OF_WEEK: Sunday=1, Monday=2..Saturday=7
                        // Our activeDays array: index 0=Sunday, 1=Monday..6=Saturday
                        val dayIndex = cal.get(Calendar.DAY_OF_WEEK) - 1
                        val isActive = allActive || (dayIndex in activeDays.indices && activeDays[dayIndex])
                        if (isActive) {
                            return cal.timeInMillis
                        }
                    }
                }
                return null
            }

            "prayer_dated" -> {
                val timings = schedule.datedTimings
                if (timings.isEmpty()) {
                    return if (schedule.triggerEpochMs > afterMs) schedule.triggerEpochMs else null
                }
                // Find smallest timestamp in datedTimings strictly after afterMs
                val upcoming = timings.values.filter { it > afterMs }.minOrNull()
                return upcoming
            }

            else -> {
                return if (schedule.triggerEpochMs > afterMs) schedule.triggerEpochMs else null
            }
        }
    }
}
