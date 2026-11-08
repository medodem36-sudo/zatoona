package com.zatoona.app

import android.annotation.SuppressLint
import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.app.Service
import android.content.Context
import android.content.Intent
import android.graphics.Color
import android.graphics.PixelFormat
import android.graphics.Typeface
import android.graphics.drawable.GradientDrawable
import android.os.Build
import android.os.CountDownTimer
import android.os.IBinder
import android.provider.Settings
import android.util.TypedValue
import android.view.Gravity
import android.view.MotionEvent
import android.view.View
import android.view.WindowManager
import android.widget.ImageView
import android.widget.LinearLayout
import android.widget.TextView
import androidx.core.app.NotificationCompat

class FloatingStudyBubbleService : Service() {

    private var windowManager: WindowManager? = null
    private var bubbleView: View? = null
    private var timerText: TextView? = null
    private var countDownTimer: CountDownTimer? = null

    private var remainingSeconds: Long = 25 * 60
    private var isPaused: Boolean = false
    private var timerTitle: String = "جلسة تركيز"

    companion object {
        const val ACTION_START = "com.zatoona.app.ACTION_START_STUDY_BUBBLE"
        const val ACTION_STOP = "com.zatoona.app.ACTION_STOP_STUDY_BUBBLE"
        const val EXTRA_TITLE = "extra_study_title"
        const val EXTRA_DURATION_SECONDS = "extra_study_duration"

        private const val NOTIFICATION_ID = 9001
        private const val CHANNEL_ID = "zatoona_study_bubble_channel"
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
                stopBubble()
                stopSelf()
                return START_NOT_STICKY
            }
            ACTION_START -> {
                val title = intent.getStringExtra(EXTRA_TITLE) ?: "جلسة تركيز"
                val duration = intent.getLongExtra(EXTRA_DURATION_SECONDS, 25 * 60)
                timerTitle = title
                remainingSeconds = duration

                // Android 14 requirement: startForeground must be invoked immediately before any stopSelf
                try {
                    startForeground(NOTIFICATION_ID, buildForegroundNotification())
                } catch (e: Exception) {
                    stopSelf()
                    return START_NOT_STICKY
                }

                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M && !Settings.canDrawOverlays(this)) {
                    stopBubble()
                    stopSelf()
                    return START_NOT_STICKY
                }

                showOrUpdateBubble()
                startTimer()
            }
        }
        return START_NOT_STICKY
    }

    private fun createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                CHANNEL_ID,
                "مؤقت المذاكرة العائم",
                NotificationManager.IMPORTANCE_LOW
            ).apply {
                description = "عرض مؤقت بومودورو والمذاكرة العائم فوق التطبيقات"
                setShowBadge(false)
            }
            val manager = getSystemService(NotificationManager::class.java)
            manager?.createNotificationChannel(channel)
        }
    }

    private fun buildForegroundNotification(): Notification {
        val openIntent = Intent(this, MainActivity::class.java).apply {
            this.flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_SINGLE_TOP
            putExtra("mode", "study")
        }
        val pendingOpen = PendingIntent.getActivity(
            this,
            0,
            openIntent,
            PendingIntent.FLAG_UPDATE_CURRENT or (if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) PendingIntent.FLAG_IMMUTABLE else 0)
        )

        val stopIntent = Intent(this, FloatingStudyBubbleService::class.java).apply {
            action = ACTION_STOP
        }
        val pendingStop = PendingIntent.getService(
            this,
            1,
            stopIntent,
            PendingIntent.FLAG_UPDATE_CURRENT or (if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) PendingIntent.FLAG_IMMUTABLE else 0)
        )

        return NotificationCompat.Builder(this, CHANNEL_ID)
            .setContentTitle("⏳ $timerTitle")
            .setContentText("المؤقت قيد التشغيل: ${formatTime(remainingSeconds)}")
            .setSmallIcon(R.mipmap.ic_launcher)
            .setContentIntent(pendingOpen)
            .addAction(0, "إغلاق المؤقت", pendingStop)
            .setOngoing(true)
            .setPriority(NotificationCompat.PRIORITY_LOW)
            .build()
    }

    @SuppressLint("ClickableViewAccessibility")
    private fun showOrUpdateBubble() {
        if (bubbleView != null) {
            updateBubbleText()
            return
        }

        windowManager = getSystemService(Context.WINDOW_SERVICE) as? WindowManager ?: return

        val layoutType = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY
        } else {
            @Suppress("DEPRECATION")
            WindowManager.LayoutParams.TYPE_PHONE
        }

        val params = WindowManager.LayoutParams(
            WindowManager.LayoutParams.WRAP_CONTENT,
            WindowManager.LayoutParams.WRAP_CONTENT,
            layoutType,
            WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE or
                    WindowManager.LayoutParams.FLAG_LAYOUT_NO_LIMITS,
            PixelFormat.TRANSLUCENT
        ).apply {
            gravity = Gravity.TOP or Gravity.START
            x = 120
            y = 250
        }

        // Programmatically build modern pill bubble view
        val bubbleLayout = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER_VERTICAL
            setPadding(dpToPx(12), dpToPx(8), dpToPx(12), dpToPx(8))

            val bg = GradientDrawable().apply {
                shape = GradientDrawable.RECTANGLE
                cornerRadius = dpToPx(24).toFloat()
                setColor(Color.parseColor("#0f172a")) // Dark Slate
                setStroke(dpToPx(2), Color.parseColor("#10b981")) // Emerald Accent
            }
            background = bg
            elevation = dpToPx(8).toFloat()
        }

        // Icon
        val iconView = TextView(this).apply {
            text = "⏳"
            setTextSize(TypedValue.COMPLEX_UNIT_SP, 15f)
            setPadding(0, 0, dpToPx(6), 0)
        }
        bubbleLayout.addView(iconView)

        // Time Text
        timerText = TextView(this).apply {
            text = formatTime(remainingSeconds)
            setTextColor(Color.WHITE)
            setTextSize(TypedValue.COMPLEX_UNIT_SP, 14f)
            typeface = Typeface.MONOSPACE
            paint.isFakeBoldText = true
            setPadding(dpToPx(4), 0, dpToPx(8), 0)
        }
        bubbleLayout.addView(timerText)

        // Close 'X' Button
        val closeBtn = TextView(this).apply {
            text = "✕"
            setTextColor(Color.parseColor("#94a3b8"))
            setTextSize(TypedValue.COMPLEX_UNIT_SP, 13f)
            setPadding(dpToPx(6), dpToPx(2), dpToPx(4), dpToPx(2))
            setOnClickListener {
                stopBubble()
                stopSelf()
            }
        }
        bubbleLayout.addView(closeBtn)

        // Touch listener for dragging and click detection
        bubbleLayout.setOnTouchListener(object : View.OnTouchListener {
            private var initialX = 0
            private var initialY = 0
            private var initialTouchX = 0f
            private var initialTouchY = 0f
            private var isMoving = false

            override fun onTouch(v: View?, event: MotionEvent?): Boolean {
                if (event == null) return false
                when (event.action) {
                    MotionEvent.ACTION_DOWN -> {
                        initialX = params.x
                        initialY = params.y
                        initialTouchX = event.rawX
                        initialTouchY = event.rawY
                        isMoving = false
                        return true
                    }
                    MotionEvent.ACTION_MOVE -> {
                        val dx = (event.rawX - initialTouchX).toInt()
                        val dy = (event.rawY - initialTouchY).toInt()
                        if (Math.abs(dx) > 10 || Math.abs(dy) > 10) {
                            isMoving = true
                            params.x = initialX + dx
                            params.y = initialY + dy
                            try {
                                windowManager?.updateViewLayout(bubbleLayout, params)
                            } catch (e: Exception) {}
                        }
                        return true
                    }
                    MotionEvent.ACTION_UP -> {
                        if (!isMoving) {
                            // Tap detected: bring MainActivity to front
                            val intent = Intent(this@FloatingStudyBubbleService, MainActivity::class.java).apply {
                                flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_SINGLE_TOP
                                putExtra("mode", "study")
                            }
                            startActivity(intent)
                        }
                        return true
                    }
                }
                return false
            }
        })

        bubbleView = bubbleLayout
        try {
            windowManager?.addView(bubbleView, params)
        } catch (e: Exception) {
            bubbleView = null
        }
    }

    private fun startTimer() {
        countDownTimer?.cancel()
        countDownTimer = object : CountDownTimer(remainingSeconds * 1000, 1000) {
            override fun onTick(millisUntilFinished: Long) {
                remainingSeconds = millisUntilFinished / 1000
                updateBubbleText()
            }

            override fun onFinish() {
                remainingSeconds = 0
                updateBubbleText()
                // Show completion notification
                val notifManager = getSystemService(Context.NOTIFICATION_SERVICE) as? NotificationManager
                val finishNotif = NotificationCompat.Builder(this@FloatingStudyBubbleService, CHANNEL_ID)
                    .setContentTitle("انتهت جلسة التركيز! 🎯")
                    .setContentText("أحسنت! أتممت وقت جلسة المذاكرة بنجاح.")
                    .setSmallIcon(R.mipmap.ic_launcher)
                    .setPriority(NotificationCompat.PRIORITY_HIGH)
                    .setAutoCancel(true)
                    .build()
                notifManager?.notify(9002, finishNotif)
                stopBubble()
                stopSelf()
            }
        }.start()
    }

    private fun updateBubbleText() {
        timerText?.post {
            timerText?.text = formatTime(remainingSeconds)
        }
    }

    private fun formatTime(seconds: Long): String {
        val m = seconds / 60
        val s = seconds % 60
        return String.format("%02d:%02d", m, s)
    }

    private fun stopBubble() {
        countDownTimer?.cancel()
        countDownTimer = null
        if (bubbleView != null && windowManager != null) {
            try {
                windowManager?.removeView(bubbleView)
            } catch (e: Exception) {}
            bubbleView = null
        }
    }

    override fun onDestroy() {
        stopBubble()
        super.onDestroy()
    }

    private fun dpToPx(dp: Int): Int {
        return (dp * resources.displayMetrics.density).toInt()
    }
}
