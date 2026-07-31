package com.github.tvbox.osc.bbox.receiver;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.os.Build;

import com.github.tvbox.osc.bbox.ui.activity.HomeActivity;
import com.orhanobut.hawk.Hawk;

/**
 * 开机广播接收器。
 *
 * 策略（参考 AK APK）：
 * - 仅监听 BOOT_COMPLETED
 * - 直接启动，无延迟
 * - 通过 HawkConfig.BOOT_LAUNCH 用户开关控制
 *
 * 国产电视如需自启动，还需在电视系统设置中：
 *   设置 → 应用管理 → 本应用 → 允许自启动
 */
public class BootReceiver extends BroadcastReceiver {

    @Override
    public void onReceive(Context context, Intent intent) {
        if (intent == null) return;

        String action = intent.getAction();
        if (action == null) return;

        // 仅响应 BOOT_COMPLETED
        if (!"android.intent.action.BOOT_COMPLETED".equals(action)) {
            return;
        }

        // 检查用户是否开启了开机自启
        if (!Hawk.get("boot_launch", true)) {
            return;
        }

        try {
            Intent launchIntent = new Intent(context, HomeActivity.class);
            launchIntent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                launchIntent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
            }
            context.startActivity(launchIntent);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
