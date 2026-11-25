# 必备软件

为了让 Hyprland 用起来更顺畅，**强烈建议**运行本页介绍的软件。

Plasma、GNOME 等桌面环境会自动处理这些事项。
Hyprland 把选择留给你，因为你可能想使用其他软件。

<a id="a-notification-daemon"></a>

### 通知守护进程

_启动方式：_ 应用发出通知时，由 D-Bus 自动激活。
也可以在 `hyprland.lua` 中添加自启动项。
如果系统中安装了多个通知守护进程，使用自启动项可能更合适。

如果没有通知守护进程在运行，许多应用（如 Discord）可能会卡住。

例如 `dunst`、`mako`、`fnott` 和 `swaync`。

<a id="pipewire"></a>

### PipeWire

_启动方式：_ 使用 systemd 时自动启动，否则需手动启动。

PipeWire 并非必需，但屏幕共享需要它才能工作。

请安装 `pipewire` 和 `wireplumber`（**不要**安装 `pipewire-media-session`）。

<a id="non-systemd-distros"></a>

#### 不使用 systemd 的发行版

在 systemd 之外，启动图形 shell 时加载 PipeWire 的方式尚无统一标准，[^1]因此 Gentoo、Artix 等不使用 systemd 的发行版提供了专用启动器。

通常可以运行 `whereis <distro>-pipewire-launcher` 找到它。
如果你的系统中没有这个文件，请查阅所用发行版的文档。

[^1]: https://wiki.gentoo.org/wiki/PipeWire#OpenRC

<a id="xdg-desktop-portal"></a>

### XDG 桌面门户

_启动方式：_ 使用 systemd 时自动启动，否则需手动启动。

XDG Desktop Portal 负责处理许多桌面功能，例如文件选择和屏幕共享。

参见 [Hyprland 桌面门户页面](../hypr-ecosystem/user/xdg-desktop-portal-hyprland.md)。

<a id="authentication-agent"></a>

### 身份验证代理

_启动方式：_ 手动配置（在配置文件中添加自启动项）。

每当应用请求提升权限时，身份验证代理就会弹出窗口，提示你输入密码。

参见 [hyprpolkitagent](../hypr-ecosystem/user/hyprpolkitagent.md)

<a id="qt-wayland-support"></a>

### Qt Wayland 支持

_启动方式：_ 无需启动（仅为库）。

安装 `qt5-wayland` 和 `qt6-wayland`。

<a id="fonts"></a>

### 字体

_启动方式：_ 无需启动（仅为库）。

渲染文本需要 `sans-serif` 字体。
如果缺少这类字体，文字可能会显示成方框。
常见的选择是 `noto-fonts`。

为使图标正确显示，建议安装一款 Nerd Font 字体或 FontAwesome。
显示图标时，默认优先使用 Nerd Fonts，其次是 FontAwesome，两者都不可用时才显示文本。
