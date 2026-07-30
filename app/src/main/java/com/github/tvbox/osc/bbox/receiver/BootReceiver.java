package com.github.tvbox.osc.bbox.receiver;

import android.app.AlarmManager;
import android.app.PendingIntent;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Build;
import android.os.Handler;
import android.os.Looper;
import android.os.SystemClock;
import android.util.Log;

import com.github.tvbox.osc.bbox.util.HawkConfig;
import com.orhanobut.hawk.Hawk;

/**
 * 开机自启接收器。
 *
 * 国产电视系统（小米/华为/创维/海信/TCL 等）会拦截 BOOT_COMPLETED 广播，
 * 为了提升开机自启成功率，监听多种系统事件：
 *   - BOOT_COMPLETED            标准开机完成
 *   - LOCKED_BOOT_COMPLETED     锁屏态启动（directBootAware 已声明）
 *   - QUICKBOOT_POWERON         部分 HTC/联想设备
 *   - USER_PRESENT              用户解锁屏幕
 *   - SCREEN_ON                 屏幕点亮
 *
 * 启动前延迟 8 秒，等电视主界面与系统服务就绪后再拉起 HomeActivity，
 * 避免启动太早被系统回收；同时使用 AlarmManager 每 30 分钟兜底检查一次。
 *
 * 实际生效还需要用户在电视"设置 → 应用管理 → 花都影视 → 自启动"
 * 中手动勾选（仅当用户从未开启过才会被拦截）。
 */
public class BootReceiver extends BroadcastReceiver {
    private static final String TAG = "BootReceiver";
    private static final long START_DELAY_MS = 8_000L;
    private static final long FALLBACK_INTERVAL_MS = 30 * 60 * 1000L;
    private static final String PREFS = "boot_receiver_prefs";
    private static final String KEY_LAST_BOOT = "last_boot_ts";

    @Override
    public void onReceive(Context context, Intent intent) {
        String action = intent == null ? null : intent.getAction();
        Log.i(TAG, "BootReceiver received action: " + action);

        if (!shouldHandle(action)) {
            return;
        }

        // 检查用户是否开启了自启动（默认 true）
        boolean bootLaunchEnabled = Hawk.get(HawkConfig.BOOT_LAUNCH, true);
        if (!bootLaunchEnabled) {
            Log.i(TAG, "BootReceiver skip, boot_launch disabled by user");
            return;
        }

        // 防抖：同一分钟内已触发过就不再启动，避免重启/解锁循环里反复拉起
        long now = System.currentTimeMillis();
        SharedPreferences sp = context.getSharedPreferences(PREFS, Context.MODE_PRIVATE);
        long last = sp.getLong(KEY_LAST_BOOT, 0L);
        if (now - last < 60_000L) {
            Log.i(TAG, "BootReceiver skip, last triggered " + (now - last) + "ms ago");
            return;
        }
        sp.edit().putLong(KEY_LAST_BOOT, now).apply();

        // 延迟拉起，等系统就绪
        scheduleStart(context);

        // 兜底：注册 30 分钟后的定时检查（应用未存活时由 AlarmManager 唤醒）
        scheduleFallback(context);
    }

    private boolean shouldHandle(String action) {
        if (action == null) return false;
        return Intent.ACTION_BOOT_COMPLETED.equals(action)
                || Intent.ACTION_LOCKED_BOOT_COMPLETED.equals(action)
                || "android.intent.action.QUICKBOOT_POWERON".equals(action)
                || Intent.ACTION_USER_PRESENT.equals(action)
                || Intent.ACTION_SCREEN_ON.equals(action);
    }

    private void scheduleStart(Context context) {
        try {
            new Handler(Looper.getMainLooper()).postDelayed(() -> BootHelper.launchHome(context), START_DELAY_MS);
            Log.i(TAG, "HomeActivity scheduled to start in " + START_DELAY_MS + "ms");
        } catch (Exception e) {
            Log.e(TAG, "scheduleStart failed: " + e.getMessage());
        }
    }

    private void scheduleFallback(Context context) {
        try {
            AlarmManager am = (AlarmManager) context.getSystemService(Context.ALARM_SERVICE);
            if (am == null) return;
            Intent i = new Intent(context, BootReceiver.class);
            i.setAction("com.github.tvbox.osc.bbox.action.BOOT_FALLBACK");
            int flags = PendingIntent.FLAG_UPDATE_CURRENT;
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
                flags |= PendingIntent.FLAG_IMMUTABLE;
            }
            PendingIntent pi = PendingIntent.getBroadcast(context, 1001, i, flags);
            long triggerAt = SystemClock.elapsedRealtime() + FALLBACK_INTERVAL_MS;
            am.set(AlarmManager.ELAPSED_REALTIME_WAKEUP, triggerAt, pi);
        } catch (Exception e) {
            Log.e(TAG, "scheduleFallback failed: " + e.getMessage());
        }
    }
}
