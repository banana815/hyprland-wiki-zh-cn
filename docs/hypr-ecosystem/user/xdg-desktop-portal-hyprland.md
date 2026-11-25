# xdg-desktop-portal-hyprland

XDG 桌面门户是一种程序，其他应用程序可以通过它使用 D-Bus 与合成器通信。

门户提供特定功能，例如打开文件选择器或共享屏幕。

[xdg-desktop-portal-hyprland](https://github.com/hyprwm/xdg-desktop-portal-hyprland) 是 Hyprland 的 xdg-desktop-portal 实现。
它支持屏幕共享、全局快捷键等功能。

> [!NOTE]
> 本文将 `xdg-desktop-portal-hyprland` 简称为 XDPH。

> [!WARNING]
> XDPH 没有实现文件选择器。
> 如需此功能，建议在安装 XDPH 的同时安装 `xdg-desktop-portal-gtk`。

<a id="installing"></a>

## 安装





<details><summary>Arch Linux</summary>


```sh
pacman -S xdg-desktop-portal-hyprland
```

如果要安装 -git 版本，则使用：

```sh
yay -S xdg-desktop-portal-hyprland-git
```



</details>


<details><summary>NixOS</summary>


在 NixOS 上，设置 `programs.hyprland.enable = true;` 时，[Hyprland 的 NixOS 模块](../../nix/installing-hyprland-on-nixos.md) 就会启用 XDPH。



</details>


<details><summary>Gentoo</summary>


<a id="unmask-dependencies"></a>

### 解除对依赖包的屏蔽

```plain {filename="/etc/portage/profile/package.unmask"}
dev-qt/qtbase
dev-qt/qtwayland
dev-qt/qtdeclarative
dev-qt/qtshadertools
```

<a id="apply-necessary-useflags"></a>

### 设置所需的 USE 标志

```plain {filename="/etc/portage/package.use"}
dev-qt/qtbase opengl egl eglfs gles2-only
dev-qt/qtdeclarative opengl
sys-apps/xdg-desktop-portal screencast
```

<a id="unmask-dependencies-and-xdph"></a>

### 解除对依赖包和 XDPH 的屏蔽

```plain {filename="/etc/portage/package.accept_keywords"}
gui-libs/xdg-desktop-portal-hyprland
dev-qt/qtbase
dev-qt/qtwayland
dev-qt/qtdeclarative
dev-qt/qtshadertools
```

<a id="installation"></a>

### 安装

```sh
eselect repository enable hyprovelay
emaint sync -r hyproverlay
emerge --ask --verbose gui-libs/xdg-desktop-portal-hyprland
```



</details>


<details><summary>手动安装</summary>


参见 [GitHub 仓库的 README](https://github.com/hyprwm/xdg-desktop-portal-hyprland)。



</details>




<a id="usage"></a>

## 使用

Hyprland 启动后，D-Bus 会自动启动 XDPH。

要检查一切是否正常，可以尝试共享任意屏幕内容，或者打开 OBS 并选择 PipeWire 来源。
如果 XDPH 正在运行，就会弹出一个 Qt 菜单，让你选择要共享的内容。

XDPH 也可以在其他基于 wlroots 的合成器上运行，但窗口共享等 Hyprland 专属功能将不可用。

作为最后的手段，你可以使用以下脚本，并将其设为自动启动：

```sh
#!/bin/sh
sleep 1
killall -e xdg-desktop-portal-hyprland
killall xdg-desktop-portal
/usr/lib/xdg-desktop-portal-hyprland &
sleep 2
/usr/lib/xdg-desktop-portal &
```

如果路径不正确，请按实际情况调整。

<a id="share-picker-doesnt-use-the-system-theme"></a>

## 共享选择器未使用系统主题

可以尝试以下两种方法中的一种，也可以两种都试：

```sh
dbus-update-activation-environment --systemd --all
systemctl --user import-environment QT_QPA_PLATFORMTHEME
```

如果有效，请将相应命令添加到配置的自动启动项中。

<a id="using-the-kde-file-picker-with-xdph"></a>

## 在 XDPH 中使用 KDE 文件选择器

XDPH 没有实现文件选择器，默认使用 GTK 文件选择器作为后备（参见 `/usr/share/xdg-desktop-portal/hyprland-portals.conf`）。
如果你想使用 KDE 文件选择器，同时让 XDPH 处理其他所有功能，请创建文件 `~/.config/xdg-desktop-portal/hyprland-portals.conf`，并写入以下内容：

```ini { filename="~/.config/xdg-desktop-portal/hyprland-portals.conf" }
[preferred]
default = hyprland;gtk
org.freedesktop.impl.portal.FileChooser = kde
```

更多信息请参阅 [Arch Wiki 上的 xdg-desktop-portal 文档](https://wiki.archlinux.org/title/XDG_Desktop_Portal)。
请注意，Firefox 等应用程序可能需要额外配置才能使用 KDE 文件选择器。

<a id="debugging"></a>

## 调试

如果应用程序启动缓慢，或屏幕共享无法使用，请查看日志。

```sh
systemctl --user status xdg-desktop-portal-hyprland
```

如果出现崩溃，很可能是因为缺少 `qt6-wayland` 或 `qt5-wayland`。

如果门户没有自动启动，手动启动后也无法正常工作，而且没有生成任何错误日志，那么很可能是 XDG [环境变量](../../configuring/core/environment-variables.md)设置有误。
Hyprland 默认会为你设置这些变量，除非你很清楚修改的影响，否则请避免覆盖它们。

<a id="configuration"></a>

## 配置

配置文件 `~/.config/hypr/xdph.conf` 支持以下变量：

<a id="screencopy"></a>

### 屏幕复制

`screencopy` 类别中的变量：

| 变量 | 说明 | 类型 | 默认值 |
| -- | -- | -- | -- |
| `max_fps` | 屏幕共享会话的最高帧率。`0` 表示不限帧率 | int | `120` |
| `allow_token_by_default` | 启用后，默认勾选“允许恢复令牌”复选框 | bool | `false` |
| `custom_picker_binary` | 如果值非空，则使用指定的**二进制程序**作为共享选择器。该程序必须遵循 `hyprland-share-picker` 将选择结果写入标准输出时所用的格式 | string | `"hyprland-share-picker"` |
| `force_shm` | 启用后，屏幕共享会跳过 DMA-BUF，始终使用 SHM。SHM 比 DMA-BUF 慢，尤其是在高分辨率下，但它可以绕过多 GPU 系统上的 DMA-BUF 分配失败问题 | bool | `false` |
| `cursor_mode` | 客户端（如浏览器）未指定光标模式时使用的默认模式。可设为 [XDG 屏幕投射门户](https://flatpak.github.io/xdg-desktop-portal/docs/doc-org.freedesktop.portal.ScreenCast.html#org-freedesktop-portal-screencast-availablecursormodes)已实现的任一模式，即 `1` 表示隐藏，`2` 表示嵌入。默认采用协议的默认模式（隐藏） | int | `0` |


<details><summary>示例</summary>


```ini { filename="~/.config/hypr/xdph.conf" }
screencopy {
    max_fps = 60
}
```



</details>
