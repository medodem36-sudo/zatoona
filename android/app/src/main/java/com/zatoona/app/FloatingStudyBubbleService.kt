package com.zatoona.app

import android.annotation.SuppressLint
import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.app.Service
import android.content.Context
import android.content.Intent
import android.content.pm.ServiceInfo
import android.graphics.Color
import android.graphics.PixelFormat
import android.graphics.Typeface
import android.graphics.drawable.GradientDrawable
import android.os.Build
import android.os.CountDownTimer
import android.os.Handler
import android.os.IBinder
import android.os.Looper
import android.os.VibrationEffect
import android.os.Vibrator
import android.os.VibratorManager
import android.provider.Settings
import android.util.Log
import android.util.TypedValue
import android.view.Gravity
import android.view.MotionEvent
import android.view.View
import android.view.WindowManager
import android.widget.LinearLayout
import android.widget.TextView
import android.widget.Toast
import androidx.core.app.NotificationCompat
import androidx.core.app.ServiceCompat
import kotlin.math.abs
import kotlin.math.hypot

/**
 * FloatingStudyBubbleService
 * Foreground floating overlay for Pomodoro & Study sessions with interactive play/pause controls,
 * edge-snapping dragging, and drag-to-dismiss bottom "✕" zone that removes the bubble from the screen
 * while keeping the study countdown running continuously in the background.
 */
class FloatingStudyBubbleService : Service() {

    private val mainHandler = Handler(Looper.getMainLooper())
    private var windowManager: WindowManager? = null
    private var bubbleView: View? = null
    private var dismissView: View? = null
    private var timerText: TextView? = null
    private var btnPlayPause: TextView? = null
    private var countDownTimer: CountDownTimer? = null

    private var remainingSeconds: Long = 25 * 60
    private var isPaused: Boolean = false
    private var timerTitle: String = "جلسة تركيز"

    companion object {
        const val TAG = "FloatingStudyBubble"
        const val ACTION_START = "com.zatoona.app.ACTION_START_STUDY_BUBBLE"
        const val ACTION_STOP = "com.zatoona.app.ACTION_STOP_STUDY_BUBBLE"
        const val ACTION_SHOW_BUBBLE = "com.zatoona.app.ACTION_SHOW_STUDY_BUBBLE"
        const val ACTION_HIDE_BUBBLE = "com.zatoona.app.ACTION_HIDE_STUDY_BUBBLE"
        const val ACTION_TOGGLE_PAUSE = "com.zatoona.app.ACTION_TOGGLE_STUDY_PAUSE"

        const val EXTRA_TITLE = "extra_study_title"
        const val EXTRA_DURATION_SECONDS = "extra_study_duration"

        private const val NOTIFICATION_ID = 9001
        private const val CHANNEL_ID = "zatoona_study_bubble_channel"

        @Volatile
        var isRunning: Boolean = false
            private set

        @Volatile
        var isBubbleVisibleOnScreen: Boolean = false
            private set

        @Volatile
        var wasDismissedToBackground: Boolean = false
            private set

        @Volatile
        var currentRemainingSeconds: Long = 25 * 60
            private set
    }

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onCreate() {
        super.onCreate()
        createNotificationChannel()
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        if (intent == null) return START_NOT_STICKY

        when (intent.action) {
            ACTION_STOP -> {
                Log.i(TAG, "Stopping FloatingStudyBubbleService")
                stopBubbleFromScreen()
                stopForeground(STOP_FOREGROUND_REMOVE)
                stopSelf()
                isRunning = false
                return START_NOT_STICKY
            }
            ACTION_SHOW_BUBBLE -> {
                wasDismissedToBackground = false
                showOrUpdateBubble()
                return START_STICKY
            }
            ACTION_HIDE_BUBBLE -> {
                hideBubbleFromScreenOnly()
                return START_STICKY
            }
            ACTION_TOGGLE_PAUSE -> {
                togglePlayPause()
                return START_STICKY
            }
            ACTION_START -> {
                val title = intent.getStringExtra(EXTRA_TITLE) ?: "جلسة تركيز"
                val duration = intent.getLongExtra(EXTRA_DURATION_SECONDS, 25 * 60)
                timerTitle = title
                remainingSeconds = duration
                currentRemainingSeconds = duration
                isPaused = false
                wasDismissedToBackground = false

                val notification = buildForegroundNotification()
                try {
                    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.UPSIDE_DOWN_CAKE) {
                        ServiceCompat.startForeground(
                            this,
                            NOTIFICATION_ID,
                            notification,
                            ServiceInfo.FOREGROUND_SERVICE_TYPE_SPECIAL_USE
                        )
                    } else {
                        startForeground(NOTIFICATION_ID, notification)
                    }
                } catch (e: Exception) {
                    Log.e(TAG, "startForeground error: ${e.message}")
                }

                isRunning = true
                startCountDown()

                // If overlay permission granted, display floating bubble
                if (Settings.canDrawOverlays(this)) {
                    showOrUpdateBubble()
                } else {
                    Log.w(TAG, "Overlay permission not granted. Running in background notification mode.")
                }
            }
        }
        return START_STICKY
    }

    private fun createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                CHANNEL_ID,
                "مؤقت المذاكرة العائم",
                NotificationManager.IMPORTANCE_LOW
            ).apply {
                description = "مؤقت بومودورو وجلسات التركيز في الخلفية وفوق التطبيقات"
                setShowBadge(false)
            }
            val manager = getSystemService(Context.NOTIFICATION_SERVICE) as? NotificationManager
            manager?.createNotificationChannel(channel)
        }
    }

    private fun buildForegroundNotification(): Notification {
        val openIntent = Intent(this, MainActivity::class.java).apply {
            flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_SINGLE_TOP
            putExtra(ZatoonaNotificationManager.EXTRA_MODE, "study")
        }
        val openPending = PendingIntent.getActivity(
            this,
            101,
            openIntent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        val pauseIntent = Intent(this, FloatingStudyBubbleService::class.java).apply {
            action = ACTION_TOGGLE_PAUSE
        }
        val pausePending = PendingIntent.getService(
            this,
            102,
            pauseIntent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        val showBubbleIntent = Intent(this, FloatingStudyBubbleService::class.java).apply {
            action = ACTION_SHOW_BUBBLE
        }
        val showBubblePending = PendingIntent.getService(
            this,
            103,
            showBubbleIntent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        val stopIntent = Intent(this, FloatingStudyBubbleService::class.java).apply {
            action = ACTION_STOP
        }
        val stopPending = PendingIntent.getService(
            this,
            104,
            stopIntent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        val statusText = if (isPaused) {
            "⏸ متوقف مؤقتاً: ${formatTime(remainingSeconds)}"
        } else {
            "⏳ جاري التركيز: ${formatTime(remainingSeconds)}"
        }

        val pauseLabel = if (isPaused) "استئناف ▶" else "إيقاف مؤقت ⏸"

        val builder = NotificationCompat.Builder(this, CHANNEL_ID)
            .setContentTitle("⏳ $timerTitle")
            .setContentText(statusText)
            .setSmallIcon(R.mipmap.ic_launcher)
            .setOngoing(true)
            .setPriority(NotificationCompat.PRIORITY_LOW)
            .setContentIntent(openPending)
            .addAction(R.mipmap.ic_launcher, pauseLabel, pausePending)

        if (!isBubbleVisibleOnScreen) {
            builder.addAction(R.mipmap.ic_launcher, "إظهار الفقاعة 📌", showBubblePending)
        }

        builder.addAction(R.mipmap.ic_launcher, "إنهاء الجلسة ⏹️", stopPending)

        return builder.build()
    }

    private fun updateNotification() {
        val manager = getSystemService(Context.NOTIFICATION_SERVICE) as? NotificationManager
        manager?.notify(NOTIFICATION_ID, buildForegroundNotification())
    }

    @SuppressLint("ClickableViewAccessibility")
    private fun showOrUpdateBubble() {
        if (!Settings.canDrawOverlays(this)) return

        if (bubbleView != null) {
            updateBubbleUI()
            return
        }

        windowManager = getSystemService(Context.WINDOW_SERVICE) as? WindowManager
        if (windowManager == null) return

        val layoutType = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY
        } else {
            @Suppress("DEPRECATION")
            WindowManager.LayoutParams.TYPE_PHONE
        }

        val density = resources.displayMetrics.density

        // 1. Main Floating Pill Layout
        val params = WindowManager.LayoutParams(
            WindowManager.LayoutParams.WRAP_CONTENT,
            WindowManager.LayoutParams.WRAP_CONTENT,
            layoutType,
            WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE or
                    WindowManager.LayoutParams.FLAG_LAYOUT_NO_LIMITS,
            PixelFormat.TRANSLUCENT
        ).apply {
            gravity = Gravity.TOP or Gravity.START
            x = (resources.displayMetrics.widthPixels - (175 * density).toInt() - (16 * density).toInt())
            y = (resources.displayMetrics.heightPixels * 0.28).toInt()
        }

        val pillLayout = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER_VERTICAL
            setPadding((12 * density).toInt(), (8 * density).toInt(), (12 * density).toInt(), (8 * density).toInt())
            background = GradientDrawable().apply {
                shape = GradientDrawable.RECTANGLE
                cornerRadius = 28 * density
                setColor(Color.parseColor("#0F172A")) // Dark Slate
                setStroke((2 * density).toInt(), Color.parseColor("#10B981")) // Emerald Accent
            }
            elevation = 14 * density
        }

        // Icon
        val iconText = TextView(this).apply {
            text = "⏳"
            textSize = 16f
            gravity = Gravity.CENTER
            setPadding(0, 0, (6 * density).toInt(), 0)
        }
        pillLayout.addView(iconText)

        // Timer Text (MM:SS)
        timerText = TextView(this).apply {
            text = formatTime(remainingSeconds)
            setTextColor(Color.WHITE)
            textSize = 15f
            typeface = Typeface.MONOSPACE
            paint.isFakeBoldText = true
            setPadding((2 * density).toInt(), 0, (8 * density).toInt(), 0)
        }
        pillLayout.addView(timerText)

        // Interactive Play / Pause Button right on the bubble
        btnPlayPause = TextView(this).apply {
            text = if (isPaused) "▶" else "⏸"
            setTextColor(Color.parseColor("#10B981"))
            textSize = 13f
            typeface = Typeface.DEFAULT_BOLD
            gravity = Gravity.CENTER
            setPadding((8 * density).toInt(), (4 * density).toInt(), (8 * density).toInt(), (4 * density).toInt())
            background = GradientDrawable().apply {
                shape = GradientDrawable.RECTANGLE
                cornerRadius = 14 * density
                setColor(Color.parseColor("#1E293B"))
                setStroke((1 * density).toInt(), Color.parseColor("#334155"))
            }
            setOnClickListener {
                togglePlayPause()
            }
        }
        pillLayout.addView(btnPlayPause)

        // 2. Build Dismiss Target (Bottom "✕" Drop Zone)
        val dismissSize = (64 * density).toInt()
        val dismissParams = WindowManager.LayoutParams(
            dismissSize,
            dismissSize,
            layoutType,
            WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE or
                    WindowManager.LayoutParams.FLAG_LAYOUT_NO_LIMITS,
            PixelFormat.TRANSLUCENT
        ).apply {
            gravity = Gravity.BOTTOM or Gravity.CENTER_HORIZONTAL
            y = (42 * density).toInt()
        }

        val dismissContainer = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            gravity = Gravity.CENTER
            background = GradientDrawable().apply {
                shape = GradientDrawable.OVAL
                setColor(Color.parseColor("#1F2937"))
                setStroke((2 * density).toInt(), Color.parseColor("#4B5563"))
            }
            elevation = 16 * density
            alpha = 0f
            visibility = View.GONE
        }

        val dismissIcon = TextView(this).apply {
            text = "✕"
            textSize = 22f
            setTextColor(Color.WHITE)
            typeface = Typeface.DEFAULT_BOLD
            gravity = Gravity.CENTER
        }
        dismissContainer.addView(dismissIcon)

        // 3. Touch, Drag & Drop-to-Dismiss on "✕"
        var initialX = 0
        var initialY = 0
        var initialTouchX = 0f
        var initialTouchY = 0f
        var isClick = false
        var isOverDismiss = false
        var hasVibratedForDismiss = false

        pillLayout.setOnTouchListener { _, event ->
            when (event.action) {
                MotionEvent.ACTION_DOWN -> {
                    initialX = params.x
                    initialY = params.y
                    initialTouchX = event.rawX
                    initialTouchY = event.rawY
                    isClick = true
                    isOverDismiss = false
                    hasVibratedForDismiss = false
                    pillLayout.animate().scaleX(0.94f).scaleY(0.94f).setDuration(80).start()
                    true
                }
                MotionEvent.ACTION_MOVE -> {
                    val dx = event.rawX - initialTouchX
                    val dy = event.rawY - initialTouchY
                    if (abs(dx) > 8 || abs(dy) > 8) {
                        isClick = false
                        // Show bottom dismiss target with smooth animation
                        if (dismissContainer.visibility != View.VISIBLE) {
                            dismissContainer.visibility = View.VISIBLE
                            dismissContainer.animate().alpha(0.9f).scaleX(1.0f).scaleY(1.0f).setDuration(160).start()
                        }
                    }

                    params.x = (initialX + dx).toInt()
                    params.y = (initialY + dy).toInt()
                    try {
                        windowManager?.updateViewLayout(pillLayout, params)
                    } catch (e: Exception) {}

                    // Calculate distance to dismiss target center
                    val screenWidth = resources.displayMetrics.widthPixels
                    val screenHeight = resources.displayMetrics.heightPixels
                    val bubbleCenterX = params.x + pillLayout.width / 2
                    val bubbleCenterY = params.y + pillLayout.height / 2
                    val dismissCenterX = screenWidth / 2
                    val dismissCenterY = screenHeight - (42 * density).toInt() - dismissSize / 2
                    val distance = hypot((bubbleCenterX - dismissCenterX).toDouble(), (bubbleCenterY - dismissCenterY).toDouble())

                    // Dismiss zone threshold (within 85dp)
                    val dismissThreshold = 85 * density
                    if (distance < dismissThreshold) {
                        if (!isOverDismiss) {
                            isOverDismiss = true
                            // Highlight dismiss target to bright red
                            (dismissContainer.background as? GradientDrawable)?.apply {
                                setColor(Color.parseColor("#DC2626"))
                                setStroke((3 * density).toInt(), Color.parseColor("#FCA5A5"))
                            }
                            dismissContainer.animate().scaleX(1.24f).scaleY(1.24f).setDuration(120).start()
                            pillLayout.animate().scaleX(0.72f).scaleY(0.72f).alpha(0.7f).setDuration(120).start()
                            if (!hasVibratedForDismiss) {
                                hasVibratedForDismiss = true
                                triggerHapticPulse()
                            }
                        }
                    } else {
                        if (isOverDismiss) {
                            isOverDismiss = false
                            hasVibratedForDismiss = false
                            // Revert dismiss target to neutral dark
                            (dismissContainer.background as? GradientDrawable)?.apply {
                                setColor(Color.parseColor("#1F2937"))
                                setStroke((2 * density).toInt(), Color.parseColor("#4B5563"))
                            }
                            dismissContainer.animate().scaleX(1.0f).scaleY(1.0f).setDuration(120).start()
                            pillLayout.animate().scaleX(1.0f).scaleY(1.0f).alpha(1.0f).setDuration(120).start()
                        }
                    }
                    true
                }
                MotionEvent.ACTION_UP -> {
                    if (isOverDismiss) {
                        // User dropped bubble onto "✕" dismiss target:
                        // REMOVE BUBBLE FROM SCREEN BUT KEEP TIMER RUNNING IN BACKGROUND!
                        triggerHapticPulse()
                        pillLayout.animate().scaleX(0f).scaleY(0f).alpha(0f).setDuration(150).start()
                        dismissContainer.animate().scaleX(0f).scaleY(0f).alpha(0f).setDuration(150).withEndAction {
                            hideBubbleFromScreenOnly()
                            wasDismissedToBackground = true
                            updateNotification()
                            Toast.makeText(
                                this@FloatingStudyBubbleService,
                                "المؤقت مستمر في الخلفية.. يمكنك إعادته من الإشعارات ⏳",
                                Toast.LENGTH_SHORT
                            ).show()
                        }.start()
                    } else {
                        // Hide bottom dismiss target
                        dismissContainer.animate().alpha(0f).scaleX(0.6f).scaleY(0.6f).setDuration(160).withEndAction {
                            dismissContainer.visibility = View.GONE
                        }.start()
                        pillLayout.animate().scaleX(1.0f).scaleY(1.0f).alpha(1.0f).setDuration(120).start()

                        if (isClick) {
                            // Tap on bubble body: launch MainActivity study section
                            launchStudyView()
                        } else {
                            // Snap to nearest edge (left or right)
                            val screenWidth = resources.displayMetrics.widthPixels
                            val pillWidth = pillLayout.width.takeIf { it > 0 } ?: (160 * density).toInt()
                            val targetX = if (params.x + pillWidth / 2 < screenWidth / 2) {
                                (12 * density).toInt()
                            } else {
                                (screenWidth - pillWidth - 12 * density).toInt()
                            }
                            params.x = targetX
                            try {
                                windowManager?.updateViewLayout(pillLayout, params)
                            } catch (e: Exception) {}
                        }
                    }
                    true
                }
                else -> false
            }
        }

        bubbleView = pillLayout
        dismissView = dismissContainer

        try {
            windowManager?.addView(dismissView, dismissParams)
            windowManager?.addView(bubbleView, params)
            isBubbleVisibleOnScreen = true
            updateNotification()
        } catch (e: Exception) {
            Log.e(TAG, "Failed to add floating study bubble views: ${e.message}")
            bubbleView = null
            dismissView = null
            isBubbleVisibleOnScreen = false
        }
    }

    private fun togglePlayPause() {
        isPaused = !isPaused
        if (isPaused) {
            countDownTimer?.cancel()
            countDownTimer = null
            triggerHapticPulse()
        } else {
            startCountDown()
            triggerHapticPulse()
        }
        updateBubbleUI()
        updateNotification()
    }

    private fun startCountDown() {
        countDownTimer?.cancel()
        countDownTimer = object : CountDownTimer(remainingSeconds * 1000L, 1000L) {
            override fun onTick(millisUntilFinished: Long) {
                if (!isPaused) {
                    remainingSeconds = millisUntilFinished / 1000L
                    currentRemainingSeconds = remainingSeconds
                    updateBubbleUI()
                    // Update notification periodically every 30 seconds
                    if (remainingSeconds % 30 == 0L) {
                        updateNotification()
                    }
                }
            }

            override fun onFinish() {
                remainingSeconds = 0
                currentRemainingSeconds = 0
                updateBubbleUI()
                onSessionFinished()
            }
        }.start()
    }

    private fun onSessionFinished() {
        triggerHapticCompletion()

        val notifManager = getSystemService(Context.NOTIFICATION_SERVICE) as? NotificationManager
        val openIntent = Intent(this, MainActivity::class.java).apply {
            flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_SINGLE_TOP
            putExtra(ZatoonaNotificationManager.EXTRA_MODE, "study")
        }
        val openPending = PendingIntent.getActivity(
            this,
            105,
            openIntent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        val finishNotif = NotificationCompat.Builder(this, CHANNEL_ID)
            .setContentTitle("🎯 انتهت جلسة التركيز!")
            .setContentText("أحسنت يا بطل! أتممت جلسة المذاكرة بنجاح.")
            .setSmallIcon(R.mipmap.ic_launcher)
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .setContentIntent(openPending)
            .setAutoCancel(true)
            .build()
        notifManager?.notify(9003, finishNotif)

        // Notify MainActivity webview if active
        MainActivity.instance?.runOnUiThread {
            MainActivity.instance?.let {
                // Trigger phase complete in web if page loaded
            }
        }

        stopBubbleFromScreen()
        stopForeground(STOP_FOREGROUND_REMOVE)
        stopSelf()
        isRunning = false
    }

    private fun updateBubbleUI() {
        mainHandler.post {
            timerText?.text = formatTime(remainingSeconds)
            btnPlayPause?.text = if (isPaused) "▶" else "⏸"
            if (isPaused) {
                timerText?.setTextColor(Color.parseColor("#94A3B8"))
                btnPlayPause?.setTextColor(Color.parseColor("#F59E0B")) // Amber for pause
            } else {
                timerText?.setTextColor(Color.WHITE)
                btnPlayPause?.setTextColor(Color.parseColor("#10B981")) // Emerald for running
            }
        }
    }

    private fun launchStudyView() {
        val intent = Intent(this, MainActivity::class.java).apply {
            flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_SINGLE_TOP
            putExtra(ZatoonaNotificationManager.EXTRA_MODE, "study")
        }
        try {
            startActivity(intent)
        } catch (e: Exception) {
            Log.e(TAG, "Error launching MainActivity: ${e.message}")
        }
    }

    private fun hideBubbleFromScreenOnly() {
        isBubbleVisibleOnScreen = false
        if (bubbleView != null && windowManager != null) {
            try {
                windowManager?.removeView(bubbleView)
            } catch (e: Exception) {
                Log.e(TAG, "Error removing bubbleView: ${e.message}")
            }
            bubbleView = null
        }
        if (dismissView != null && windowManager != null) {
            try {
                windowManager?.removeView(dismissView)
            } catch (e: Exception) {
                Log.e(TAG, "Error removing dismissView: ${e.message}")
            }
            dismissView = null
        }
    }

    private fun stopBubbleFromScreen() {
        hideBubbleFromScreenOnly()
        countDownTimer?.cancel()
        countDownTimer = null
    }

    private fun triggerHapticPulse() {
        try {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
                val vm = getSystemService(Context.VIBRATOR_MANAGER_SERVICE) as? VibratorManager
                vm?.defaultVibrator?.vibrate(VibrationEffect.createOneShot(35, VibrationEffect.DEFAULT_AMPLITUDE))
            } else {
                @Suppress("DEPRECATION")
                val v = getSystemService(Context.VIBRATOR_SERVICE) as? Vibrator
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                    v?.vibrate(VibrationEffect.createOneShot(35, VibrationEffect.DEFAULT_AMPLITUDE))
                } else {
                    @Suppress("DEPRECATION")
                    v?.vibrate(35)
                }
            }
        } catch (e: Exception) {}
    }

    private fun triggerHapticCompletion() {
        try {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
                val vm = getSystemService(Context.VIBRATOR_MANAGER_SERVICE) as? VibratorManager
                vm?.defaultVibrator?.vibrate(VibrationEffect.createWaveform(longArrayOf(0, 150, 80, 200), -1))
            } else {
                @Suppress("DEPRECATION")
                val v = getSystemService(Context.VIBRATOR_SERVICE) as? Vibrator
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                    v?.vibrate(VibrationEffect.createWaveform(longArrayOf(0, 150, 80, 200), -1))
                } else {
                    @Suppress("DEPRECATION")
                    v?.vibrate(200)
                }
            }
        } catch (e: Exception) {}
    }

    private fun formatTime(seconds: Long): String {
        val m = seconds / 60
        val s = seconds % 60
        return String.format("%02d:%02d", m, s)
    }

    override fun onDestroy() {
        isRunning = false
        stopBubbleFromScreen()
        super.onDestroy()
    }
}
