package com.github.tvbox.osc.bbox.receiver;

import android.app.Activity;
import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.net.Uri;
import android.os.Build;
import android.provider.Settings;
import android.text.TextUtils;

import com.github.tvbox.osc.bbox.ui.activity.HomeActivity;
import com.orhanobut.hawk.Hawk;

/**
 * 引导用户开启电视自启动白名单。
 *
 * 国产电视（小米/华为/创维/海信/TCL/康佳/索尼）的"自启动管理"入口各不相同，
 * 且部分厂商把入口隐藏在二级页面。本工具依次尝试跳到：
 *   1) 应用详情页（设置 → 应用管理 → 该应用 → 自启动）
 *   2) 厂商自启动白名单（小米/华为/OPPO 等有特定的 component）
 *   3) 安全中心首页
 * 用户在其中任一项里勾选即可。
 */
public final class BootHelper {

    private static final String KEY_AUTOSTART_TIP_SHOWN = "autostart_tip_shown_v1";

    /**
     * 第一次启动时调用：弹一次提示，让用户去电视"自启动管理"中勾选本应用。
     * 之后不再弹，避免骚扰。
     */
    public static void showAutostartTipIfNeeded(Activity activity) {
        if (Hawk.get(KEY_AUTOSTART_TIP_SHOWN, false)) return;
        Hawk.put(KEY_AUTOSTART_TIP_SHOWN, true);

        new android.app.AlertDialog.Builder(activity)
                .setTitle("设置开机自启动")
                .setMessage(
                        "为保证电视开机后自动打开本应用，请在电视的"
                                + "「设置 → 应用管理 → 花都影视 → 自启动」中"
                                + "勾选允许。"
                                + "\n\n如果找不到该入口，请检查电视是否有"
                                + "「安全中心」或「自启动白名单」，"
                                + "在应用列表中找到「花都影视」并允许后台运行。"
                                + "\n\n现在打开应用详情页？"
                )
                .setPositiveButton("去设置", (d, w) -> openAppDetailSettings(activity))
                .setNegativeButton("知道了", null)
                .show();
    }

    /**
     * 跳转到本应用的应用详情页。电视系统一般会在此页放"自启动"开关。
     */
    public static void openAppDetailSettings(Context context) {
        Intent intent = new Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS);
        intent.setData(Uri.fromParts("package", context.getPackageName(), null));
        intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
        try {
            context.startActivity(intent);
        } catch (Exception e) {
            // fallback 到通用设置
            try {
                context.startActivity(new Intent(Settings.ACTION_SETTINGS)
                        .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK));
            } catch (Exception ignored) {}
        }
    }

    /**
     * 尝试跳到各厂商的自启动白名单。
     * 命中第一个能打开的就返回 true。
     */
    public static boolean openManufacturerAutostart(Context context) {
        if (Build.MANUFACTURER == null) return false;
        String m = Build.MANUFACTURER.toLowerCase();
        Intent intent = null;

        // 小米 / 红米
        if (m.contains("xiaomi") || m.contains("redmi")) {
            intent = new Intent();
            intent.setComponent(new ComponentName(
                    "com.miui.securitycenter",
                    "com.miui.permcenter.autostart.AutoStartManagementActivity"));
        }
        // 华为 / 荣耀
        else if (m.contains("huawei") || m.contains("honor")) {
            intent = new Intent();
            intent.setComponent(new ComponentName(
                    "com.huawei.systemmanager",
                    "com.huawei.systemmanager.startupmgr.ui.StartupNormalAppListActivity"));
        }
        // OPPO / realme / 一加
        else if (m.contains("oppo") || m.contains("realme") || m.contains("oneplus")) {
            intent = new Intent();
            intent.setComponent(new ComponentName(
                    "com.coloros.safecenter",
                    "com.coloros.safecenter.permission.startup.StartupAppListActivity"));
        }
        // VIVO / iQOO
        else if (m.contains("vivo") || m.contains("iqoo")) {
            intent = new Intent();
            intent.setComponent(new ComponentName(
                    "com.vivo.permissionmanager",
                    "com.vivo.permissionmanager.activity.BgStartUpManagerActivity"));
        }
        // 三星
        else if (m.contains("samsung")) {
            intent = new Intent();
            intent.setComponent(new ComponentName(
                    "com.samsung.android.lool",
                    "com.samsung.android.sm.ui.battery.BatteryActivity"));
        }
        // 魅族
        else if (m.contains("meizu")) {
            intent = new Intent();
            intent.setComponent(new ComponentName(
                    "com.meizu.safe",
                    "com.meizu.safe.security.SHOW_APPSEC"));
        }
        // 乐视
        else if (m.contains("letv")) {
            intent = new Intent();
            intent.setComponent(new ComponentName(
                    "com.letv.android.letvsafe",
                    "com.letv.android.letvsafe.AutobootManageActivity"));
        }

        if (intent == null) return false;
        intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
        try {
            context.startActivity(intent);
            return true;
        } catch (Exception e) {
            return false;
        }
    }

    /**
     * 主动把 HomeActivity 拉起到前台（用于 BootReceiver 等）。
     */
    public static void launchHome(Context context) {
        try {
            Intent launch = new Intent(context, HomeActivity.class);
            launch.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                launch.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
            }
            context.startActivity(launch);
        } catch (Exception ignored) {}
    }

    private BootHelper() {}
}
