# 环境变量

你可以使用 `hl.env()` 方法在显示服务器初始化之前设置环境变量。例如：

```lua
hl.env("GTK_THEME", "Nord")
```

> [!NOTE]
> 引用 `$XDG_RUNTIME_DIR` 等已有的环境变量时，请使用 `os.getenv()`。例如：`hl.env("SSH_AUTH_SOCK", os.getenv("XDG_RUNTIME_DIR") .. "/ssh-agent.socket")`

> [!WARNING]
> 请避免将 Wayland 专用的环境变量写入 `/etc/environment`。在传统发行版上，这会使所有会话（包括 Xorg 会话）都加载这些变量，很可能导致会话无法正常工作。

复制粘贴此处列出的环境变量之前，请先确认你了解它们的作用。其中一些用于调试，另一些如果使用不当，可能导致系统不稳定。

<a id="hyprland-environment-variables"></a>

## Hyprland 环境变量

- `hl.env("HYPRLAND_TRACE", "1")` - 启用更详细的日志记录。
- `hl.env("HYPRLAND_NO_RT", "1")` - 禁止 Hyprland 设置实时优先级。
- `hl.env("HYPRLAND_NO_SD_NOTIFY", "1")` - 使用 systemd 时，禁用 `sd_notify` 调用。
- `hl.env("HYPRLAND_NO_SD_VARS", "1")` - 禁止 Hyprland 管理 systemd 和 D-Bus 激活环境中的变量。
- `hl.env("HYPRLAND_CONFIG", "/path/to/hyprland.lua")` - 指定 Hyprland 配置文件的位置。

<a id="aquamarine"></a>

## [Aquamarine](../../hypr-ecosystem/dev/aquamarine.md)


- `hl.env("AQ_TRACE", "1")` - 启用跟踪日志（输出非常详细）。
- `hl.env("AQ_DRM_DEVICES", "...")` - 显式指定要使用的 DRM 设备（GPU）列表。设备路径以冒号分隔，第一个设备将用作主 GPU。例如：`/dev/dri/card1:/dev/dri/card0`。
- `hl.env("AQ_FORCE_LINEAR_BLIT", "0")` - 不再强制多 GPU 缓冲区使用显式线性修饰符，这可能有助于规避 NVIDIA 相关问题。
- `hl.env("AQ_MGPU_NO_EXPLICIT", "1")` - 在多 GPU 显示扫描输出时禁用显式同步栅栏的传递。
- `hl.env("AQ_NO_MODIFIERS", "1")` - 禁用 DRM 缓冲区的修饰符。
- `hl.env("AQ_NO_KMS_REQUIREMENT", "1")` - 允许在无显示输出的 GPU 上启动时无需满足 KMS 要求。
- `hl.env("AQ_NO_ATOMIC", "1")` - **（强烈不建议）**禁用原子模式设置。

<a id="mouse-cursor"></a>

## 鼠标光标

- `hl.env("XCURSOR_THEME", "MyCursorTheme")` - 设置光标主题。该主题必须已安装，且当前用户必须有权读取。
- `hl.env("XCURSOR_SIZE", "24")` - 设置光标大小。有关设置此变量的原因，请参阅[常见问题](../../faq/_index.md)。
- `hl.env("HYPRCURSOR_THEME", "MyHyprcursorTheme")` - 有关 hyprcursor 的信息，请参阅 [hyprcursor 页面](../../hypr-ecosystem/user/hyprcursor.md)。
- `hl.env("HYPRCURSOR_SIZE", "24")`

<a id="qt"></a>

## Qt

- `hl.env("QT_QPA_PLATFORMTHEME", "qt6ct")` - 让基于 Qt 的应用程序使用你在 qt6ct 中选择的主题。
- `hl.env("QT_AUTO_SCREEN_SCALE_FACTOR", "1")` - [（摘自 Qt 文档）](https://doc.qt.io/qt-5/highdpi.html)启用自动缩放，缩放比例取决于显示器的像素密度。
- `hl.env("QT_WAYLAND_DISABLE_WINDOWDECORATION", "1")` - 禁用 Qt 应用程序的窗口装饰。

<a id="gtk"></a>

## GTK

- `hl.env("GTK_THEME", "yourVeryPrettyTheme")` - 手动设置 GTK 主题，适合不想使用 lxappearance 或 nwg-look 等外观配置工具的用户。

<a id="gui-toolkits-backend"></a>

## GUI 工具包的后端

- `hl.env("GDK_BACKEND", "wayland,x11,*")` - GTK：优先使用 Wayland；如果不可用，则尝试 X11，再尝试其他可用的 GDK 后端。
- `hl.env("QT_QPA_PLATFORM", "wayland;xcb")` - Qt：优先使用 Wayland，如果不可用则回退到 X11。
- `hl.env("SDL_VIDEODRIVER", "wayland")` - 让 SDL2 应用程序在 Wayland 上运行。如果自带旧版 SDL 的游戏出现兼容性问题，请移除此变量或将其设为 `x11`。
- `hl.env("CLUTTER_BACKEND", "wayland")` - Clutter 软件包已启用 Wayland 支持。设置此变量会强制 Clutter 应用程序尝试使用 Wayland 后端。
