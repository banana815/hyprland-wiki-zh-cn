# 连接手机

本页列出了将手机连接到 Hyprland 会话的工具，涵盖设备集成、文件访问、屏幕镜像和局域网内的快速文件共享。

<a id="phone-integration"></a>

## 手机与桌面集成

<a id="kde-connect"></a>

### KDE Connect

[KDE Connect](https://kdeconnect.kde.org/) 可将手机与桌面集成。
它可以共享文件和剪贴板内容、显示手机通知、让设备响铃或查找设备，还提供远程输入功能。

安装 [hypr-kdeconnect-fix](https://github.com/gfhdhytghd/hypr-kdeconnect-fix) 即可使用 KDE Connect 的远程输入功能。
**警告：** 此工具的代码完全是通过自然语言提示让 AI 编写的（vibe coding）。

<a id="device-access"></a>

## 访问设备

<a id="android-adb-and-mtp"></a>

### Android：adb 和 MTP

安装 `android-tools` 即可使用 `adb`。
在手机上启用 USB 调试，然后检查系统能否识别设备。

要通过 MTP 在文件管理器中访问手机文件，请安装 `gvfs-mtp`。
解锁手机并切换到文件传输模式后，即可使用支持 GVfs 的文件管理器浏览 Android 设备上的文件。

<a id="ios-libimobiledevice-and-ifuse"></a>

### iOS：libimobiledevice 和 ifuse

安装 [`libimobiledevice`](https://libimobiledevice.org/) 和 [`ifuse`](https://github.com/libimobiledevice/ifuse) 即可访问 iPhone 和 iPad。

软件包名称和服务管理方式因发行版而异。
在某些环境中，访问 iOS 设备还需要运行 `usbmuxd`。

<a id="screen-mirroring"></a>

## 屏幕镜像

<a id="scrcpy"></a>

### scrcpy

[`scrcpy`](https://github.com/Genymobile/scrcpy) 使用 `adb`，通过 USB 或 TCP/IP 显示 Android 设备的屏幕并控制设备。
它轻量小巧，在启用 USB 调试后表现良好。

<a id="escrcpy"></a>

### Escrcpy

[Escrcpy](https://github.com/viarotel-org/escrcpy) 是基于 `scrcpy` 的图形前端。
如果你更喜欢通过图形界面管理多台 Android 设备、调整镜像选项和执行常用操作，Escrcpy 可以省去输入命令行参数的步骤。

<a id="quick-local-file-sharing"></a>

## 在局域网内快速共享文件

<a id="localsend"></a>

### LocalSend

[LocalSend](https://localsend.org/) 是一款跨平台的局域网文件共享应用。
在两台设备上都安装 LocalSend，并确保它们连接到同一网络，即可发送文件，无需配置 SSH、SMB 或云存储。

<a id="fyde-drop"></a>

### Fyde Drop

[Fyde Drop](https://drop.fydeos.io/) 是一款基于浏览器的局域网文件共享工具。
如果只是临时传一次文件，又不想安装应用，在两台设备上打开该网页即可快速传输。
