# 花都影视

基于 [TVBoxOSC](https://github.com/CatVodTVspain/TVBoxOSC) 定制修改的电视直播点播应用。

## 已集成的修改

| 功能 | 说明 |
|------|------|
| DNS 修复 | 解决部分网络环境下的 DNS 解析失败问题 |
| 默认直播源 | 线路配置默认 `ghfast.top`，多仓默认 `cdn.jsdelivr.net` |
| 直播源空值覆盖 | 解决历史遗留空值导致默认源无法生效的问题 |
| 开机自启 | 支持多种触发方式（BOOT/ScreenOn/UserPresent），兼容国产电视品牌 |
| 自启动引导 | 首次启动弹框引导用户开启自启动权限 |
| 配置源名键盘可点 | 修复某些设备上"配置源名"按钮无法点击的问题 |

## 安装

1. 进入 [Releases](https://github.com/zhongyuan689/huadutv/releases) 下载最新 APK
2. 安装到电视/机顶盒（建议先卸载旧版本）
3. 首次启动会弹出引导，按提示在电视设置中开启自启动

## 构建

```bash
# 环境要求
# - JDK 11 或 JDK 17
# - Android SDK
# - Gradle 7.6.3（项目已自带 gradle wrapper）

./gradlew assembleRelease
```

签名文件（内置 demo 签名，仅供测试）：
- keystore: `cert/bunny.jks`
- alias: `bunny`
- password: `000624`

**正式发布请替换为自己的签名文件。**

## 电视自启动说明

国产电视（小米/华为/创维/海信/TCL/OPPO/vivo 等）的自启动管理入口各不相同，一般在：
- 设置 → 应用管理 → 本应用 → 自启动
- 安全中心 → 自启动白名单
- 设备管理器 → 自启动管理

本应用已注册多种开机触发广播以提高兼容性，但如果电视系统的自启动管理中找不到本应用，可能需要：
1. 在电视设置中允许安装未知来源应用
2. 确认已将本应用加入系统白名单

## 许可证

继承 [TVBoxOSC](https://github.com/CatVodTVspain/TVBoxOSC) 的许可证。
