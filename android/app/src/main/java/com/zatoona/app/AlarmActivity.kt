package com.zatoona.app

import android.annotation.SuppressLint
import android.content.Context
import android.content.Intent
import android.os.Build
import android.os.Bundle
import android.os.VibrationEffect
import android.os.Vibrator
import android.os.VibratorManager
import android.view.MotionEvent
import android.view.View
import android.view.ViewGroup
import android.view.WindowManager
import android.view.animation.OvershootInterpolator
import android.widget.FrameLayout
import android.widget.ImageView
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import com.google.android.material.button.MaterialButton
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

/**
 * AlarmActivity
 * Native full-screen interactive alarm display over Android lock screen.
 * Provides continuous visual alert, swipe-to-dismiss gesture, and fallback dismiss button.
 */
class AlarmActivity : AppCompatActivity() {

    private var scheduleId: String = ""
    private var triggerMs: Long = 0L
    private var isDismissed = false

    private lateinit var swipeTrack: FrameLayout
    private lateinit var swipeHandle: FrameLayout
    private lateinit var tvSwipeHint: TextView
    private lateinit var btnDismiss: MaterialButton
    private lateinit var tvAlarmTime: TextView
    private lateinit var tvAlarmTitle: TextView
    private lateinit var tvAlarmBody: TextView
    private lateinit var ivBellLarge: ImageView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        configureLockScreenFlags()
        setContentView(R.layout.activity_alarm)

        initViews()
        unpackIntent(intent)
        setupSwipeToDismiss()
        setupListeners()
    }

    override fun onNewIntent(intent: Intent?) {
        super.onNewIntent(intent)
        setIntent(intent)
        intent?.let { unpackIntent(it) }
    }

    private fun configureLockScreenFlags() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O_MR1) {
            setShowWhenLocked(true)
            setTurnScreenOn(true)
        } else {
            @Suppress("DEPRECATION")
            window.addFlags(
                WindowManager.LayoutParams.FLAG_SHOW_WHEN_LOCKED or
                WindowManager.LayoutParams.FLAG_TURN_SCREEN_ON
            )
        }
        window.addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)
    }

    private fun initViews() {
        swipeTrack = findViewById(R.id.swipeTrack)
        swipeHandle = findViewById(R.id.swipeHandle)
        tvSwipeHint = findViewById(R.id.tvSwipeHint)
        btnDismiss = findViewById(R.id.btnDismiss)
        tvAlarmTime = findViewById(R.id.tvAlarmTime)
        tvAlarmTitle = findViewById(R.id.tvAlarmTitle)
        tvAlarmBody = findViewById(R.id.tvAlarmBody)
        ivBellLarge = findViewById(R.id.ivBellLarge)
    }

    private fun unpackIntent(intent: Intent) {
        scheduleId = intent.getStringExtra(AlarmService.EXTRA_SCHEDULE_ID) ?: ""
        triggerMs = intent.getLongExtra(AlarmService.EXTRA_TRIGGER_MS, System.currentTimeMillis())
        val title = intent.getStringExtra(AlarmService.EXTRA_TITLE) ?: "تذكير زتونة"
        val body = intent.getStringExtra(AlarmService.EXTRA_BODY) ?: ""

        val displayTimeMs = if (triggerMs > 0) triggerMs else System.currentTimeMillis()
        val timeFormat = SimpleDateFormat("hh:mm a", Locale("ar"))
        tvAlarmTime.text = timeFormat.format(Date(displayTimeMs))

        tvAlarmTitle.text = title
        tvAlarmBody.text = if (body.isNotBlank()) body else "حان موعد التذكير المجدول"
    }

    @SuppressLint("ClickableViewAccessibility")
    private fun setupSwipeToDismiss() {
        var startX = 0f

        swipeHandle.setOnTouchListener { view, event ->
            val marginStart = (view.layoutParams as? ViewGroup.MarginLayoutParams)?.marginStart ?: 0
            val maxTravel = (swipeTrack.width - view.width - (marginStart * 2)).coerceAtLeast(1)

            when (event.actionMasked) {
                MotionEvent.ACTION_DOWN -> {
                    startX = event.rawX
                    true
                }

                MotionEvent.ACTION_MOVE -> {
                    if (isDismissed) return@setOnTouchListener true

                    val deltaX = event.rawX - startX
                    val clampedX = deltaX.coerceIn(0f, maxTravel.toFloat())
                    view.translationX = clampedX

                    val progress = clampedX / maxTravel.toFloat()
                    tvSwipeHint.alpha = (1f - progress * 1.5f).coerceAtLeast(0.1f)

                    if (progress >= 0.70f) {
                        isDismissed = true
                        triggerDismiss()
                    }
                    true
                }

                MotionEvent.ACTION_UP, MotionEvent.ACTION_CANCEL -> {
                    if (!isDismissed) {
                        view.animate()
                            .translationX(0f)
                            .setDuration(250)
                            .setInterpolator(OvershootInterpolator(1.2f))
                            .start()
                        tvSwipeHint.animate().alpha(1f).setDuration(250).start()
                    }
                    true
                }

                else -> false
            }
        }
    }

    private fun setupListeners() {
        btnDismiss.setOnClickListener {
            if (!isDismissed) {
                isDismissed = true
                triggerDismiss()
            }
        }

        // Listen for dismissal triggered externally (e.g., from notification action button)
        AlarmService.onAlarmDismissed = {
            runOnUiThread {
                if (!isFinishing) {
                    finish()
                }
            }
        }
    }

    private fun triggerDismiss() {
        performHapticClick()

        // Send dismiss command to AlarmService
        val dismissIntent = Intent(this, AlarmService::class.java).apply {
            action = AlarmService.ACTION_DISMISS_ALARM
            putExtra(AlarmService.EXTRA_SCHEDULE_ID, scheduleId)
        }
        startService(dismissIntent)

        // Mark dismissed in repository to prevent duplicate alerts
        if (scheduleId.isNotBlank()) {
            val repository = ZatoonaScheduleRepository(this)
            repository.markDispatched("$scheduleId:dismissed", System.currentTimeMillis())
        }

        // Finish activity cleanly
        finish()
        overridePendingTransition(0, android.R.anim.fade_out)
    }

    private fun performHapticClick() {
        try {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
                val vm = getSystemService(Context.VIBRATOR_MANAGER_SERVICE) as? VibratorManager
                vm?.defaultVibrator?.vibrate(VibrationEffect.createPredefined(VibrationEffect.EFFECT_CLICK))
            } else if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                @Suppress("DEPRECATION")
                val vib = getSystemService(Context.VIBRATOR_SERVICE) as? Vibrator
                vib?.vibrate(VibrationEffect.createOneShot(50, VibrationEffect.DEFAULT_AMPLITUDE))
            }
        } catch (e: Exception) {
            // Ignore haptic error
        }
    }

    override fun onDestroy() {
        AlarmService.onAlarmDismissed = null
        super.onDestroy()
    }
}
