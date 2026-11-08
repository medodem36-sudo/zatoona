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
import android.os.IBinder
import android.os.VibrationEffect
import android.os.Vibrator
import android.os.VibratorManager
import android.provider.Settings
import android.util.Log
import android.view.Gravity
import android.view.MotionEvent
import android.view.View
import android.view.WindowManager
import android.widget.LinearLayout
import android.widget.TextView
import androidx.core.app.NotificationCompat
import androidx.core.app.ServiceCompat
import kotlin.math.abs
import kotlin.math.hypot

class FloatingCoachBubbleService : Service() {

    private var windowManager: WindowManager? = null
    private var bubbleView: View? = null
    private var dismissView: View? = null

    companion object {
        const val TAG = "FloatingCoachBubble"
        const val ACTION_START = "com.zatoona.app.ACTION_START_COACH_BUBBLE"
        const val ACTION_STOP = "com.zatoona.app.ACTION_STOP_COACH_BUBBLE"
        const val ACTION_SPEAK_NOW = "com.zatoona.app.ACTION_COACH_SPEAK_NOW"

        private const val NOTIFICATION_ID = 9002
        private const val CHANNEL_ID = "zatoona_coach_bubble_channel"

        @Volatile
        var isRunning: Boolean = false
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
                stopBubble()
                stopSelf()
                return START_NOT_STICKY
            }
            ACTION_SPEAK_NOW -> {
                launchAssistantVoice(autoListen = true)
                return START_NOT_STICKY
            }
            ACTION_START -> {
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
                    Log.e(TAG, "Error starting foreground service: ${e.message}")
                }

                if (!Settings.canDrawOverlays(this)) {
                    Log.w(TAG, "Overlay permission not granted. Running in background notification mode.")
                    isRunning = true
                    return START_STICKY
                }

                initFloatingBubble()
                isRunning = true
            }
        }

        return START_STICKY
    }

    private fun createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                CHANNEL_ID,
                "المساعد الذكي العائم",
                NotificationManager.IMPORTANCE_LOW
            ).apply {
                description = "خدمة المساعد الصوتي والزر العائم لكوتش زتونة"
                setShowBadge(false)
            }
            val manager = getSystemService(Context.NOTIFICATION_SERVICE) as? NotificationManager
            manager?.createNotificationChannel(channel)
        }
    }

    private fun buildForegroundNotification(): Notification {
        val openIntent = Intent(this, MainActivity::class.java).apply {
            flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TOP
            putExtra(MainActivity.EXTRA_AUTO_LISTEN, true)
            putExtra(ZatoonaNotificationManager.EXTRA_MODE, "home")
        }
        val openPending = PendingIntent.getActivity(
            this,
            201,
            openIntent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        val closeIntent = Intent(this, FloatingCoachBubbleService::class.java).apply {
            action = ACTION_STOP
        }
        val closePending = PendingIntent.getService(
            this,
            202,
            closeIntent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        return NotificationCompat.Builder(this, CHANNEL_ID)
            .setContentTitle("🎙️ كوتش زتونة: المساعد الذكي جاهز")
            .setContentText("اضغط للحديث مع الكوتش أو انده 'يا كوتش' في أي وقت")
            .setSmallIcon(R.mipmap.ic_launcher)
            .setOngoing(true)
            .setContentIntent(openPending)
            .addAction(R.mipmap.ic_launcher, "تحدث الآن 🗣️", openPending)
            .addAction(R.mipmap.ic_launcher, "إغلاق ❌", closePending)
            .setPriority(NotificationCompat.PRIORITY_LOW)
            .build()
    }

    @SuppressLint("ClickableViewAccessibility")
    private fun initFloatingBubble() {
        if (bubbleView != null) return

        windowManager = getSystemService(Context.WINDOW_SERVICE) as? WindowManager
        if (windowManager == null) return

        val layoutType = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY
        } else {
            @Suppress("DEPRECATION")
            WindowManager.LayoutParams.TYPE_PHONE
        }

        val density = resources.displayMetrics.density
        val sizePx = (56 * density).toInt()

        // 1. Build Floating Bubble (Coach Icon)
        val params = WindowManager.LayoutParams(
            sizePx,
            sizePx,
            layoutType,
            WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE or
                    WindowManager.LayoutParams.FLAG_LAYOUT_NO_LIMITS,
            PixelFormat.TRANSLUCENT
        ).apply {
            gravity = Gravity.TOP or Gravity.START
            x = (resources.displayMetrics.widthPixels - sizePx - 16 * density).toInt()
            y = (resources.displayMetrics.heightPixels * 0.35).toInt()
        }

        val container = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            gravity = Gravity.CENTER
            background = GradientDrawable().apply {
                shape = GradientDrawable.OVAL
                colors = intArrayOf(Color.parseColor("#10B981"), Color.parseColor("#059669"))
                orientation = GradientDrawable.Orientation.TL_BR
                setStroke((2 * density).toInt(), Color.parseColor("#34D399"))
            }
            elevation = 12 * density
        }

        val iconText = TextView(this).apply {
            text = "🌱"
            textSize = 24f
            gravity = Gravity.CENTER
        }
        container.addView(iconText)

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

        // 3. Touch & Drag with Drag-to-Dismiss Zone
        var initialX = 0
        var initialY = 0
        var initialTouchX = 0f
        var initialTouchY = 0f
        var isClick = false
        var isOverDismiss = false
        var hasVibratedForDismiss = false

        container.setOnTouchListener { _, event ->
            when (event.action) {
                MotionEvent.ACTION_DOWN -> {
                    initialX = params.x
                    initialY = params.y
                    initialTouchX = event.rawX
                    initialTouchY = event.rawY
                    isClick = true
                    isOverDismiss = false
                    hasVibratedForDismiss = false
                    container.animate().scaleX(0.92f).scaleY(0.92f).setDuration(80).start()
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
                    windowManager?.updateViewLayout(container, params)

                    // Calculate distance to dismiss target center
                    val screenWidth = resources.displayMetrics.widthPixels
                    val screenHeight = resources.displayMetrics.heightPixels
                    val bubbleCenterX = params.x + sizePx / 2
                    val bubbleCenterY = params.y + sizePx / 2
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
                            container.animate().scaleX(0.72f).scaleY(0.72f).alpha(0.7f).setDuration(120).start()
                            if (!hasVibratedForDismiss) {
                                hasVibratedForDismiss = true
                                triggerDismissHaptic()
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
                            container.animate().scaleX(1.0f).scaleY(1.0f).alpha(1.0f).setDuration(120).start()
                        }
                    }
                    true
                }
                MotionEvent.ACTION_UP -> {
                    if (isOverDismiss) {
                        // User dropped bubble onto "✕" dismiss target: remove and stop service!
                        triggerDismissHaptic()
                        container.animate().scaleX(0f).scaleY(0f).alpha(0f).setDuration(150).start()
                        dismissContainer.animate().scaleX(0f).scaleY(0f).alpha(0f).setDuration(150).withEndAction {
                            stopBubble()
                            stopSelf()
                        }.start()
                    } else {
                        // Hide bottom dismiss target
                        dismissContainer.animate().alpha(0f).scaleX(0.6f).scaleY(0.6f).setDuration(160).withEndAction {
                            dismissContainer.visibility = View.GONE
                        }.start()
                        container.animate().scaleX(1.0f).scaleY(1.0f).alpha(1.0f).setDuration(120).start()

                        if (isClick) {
                            launchAssistantVoice(autoListen = true)
                        } else {
                            // Snap to nearest edge (left or right)
                            val screenWidth = resources.displayMetrics.widthPixels
                            val targetX = if (params.x + sizePx / 2 < screenWidth / 2) {
                                (8 * density).toInt()
                            } else {
                                (screenWidth - sizePx - 8 * density).toInt()
                            }
                            params.x = targetX
                            windowManager?.updateViewLayout(container, params)
                        }
                    }
                    true
                }
                else -> false
            }
        }

        bubbleView = container
        dismissView = dismissContainer

        try {
            windowManager?.addView(dismissView, dismissParams)
            windowManager?.addView(bubbleView, params)
        } catch (e: Exception) {
            Log.e(TAG, "Failed to add floating views: ${e.message}")
        }
    }

    private fun triggerDismissHaptic() {
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

    private fun launchAssistantVoice(autoListen: Boolean) {
        val intent = Intent(this, MainActivity::class.java).apply {
            flags = Intent.FLAG_ACTIVITY_NEW_TASK or
                    Intent.FLAG_ACTIVITY_CLEAR_TOP or
                    Intent.FLAG_ACTIVITY_SINGLE_TOP
            putExtra(MainActivity.EXTRA_AUTO_LISTEN, autoListen)
            putExtra(ZatoonaNotificationManager.EXTRA_MODE, "home")
        }
        try {
            startActivity(intent)
        } catch (e: Exception) {
            Log.e(TAG, "Error launching MainActivity from coach bubble: ${e.message}")
        }
    }

    private fun stopBubble() {
        isRunning = false
        if (bubbleView != null && windowManager != null) {
            try {
                windowManager?.removeView(bubbleView)
            } catch (e: Exception) {
                Log.e(TAG, "Error removing floating coach bubble: ${e.message}")
            }
            bubbleView = null
        }
        if (dismissView != null && windowManager != null) {
            try {
                windowManager?.removeView(dismissView)
            } catch (e: Exception) {
                Log.e(TAG, "Error removing dismiss target view: ${e.message}")
            }
            dismissView = null
        }
    }

    override fun onDestroy() {
        stopBubble()
        super.onDestroy()
    }
}
