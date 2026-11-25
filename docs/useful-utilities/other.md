# 其他

这里列出了一些可能不属于上述任何类别的项目。

<a id="workspace-management"></a>

### 工作区管理

[split-monitor-workspaces](https://github.com/Duckonaut/split-monitor-workspaces) 由 _Stanisław Zagórowski_ 开发：
为 Hyprland 提供类似 Awesome 的工作区。

<a id="window-switchers"></a>

### 窗口切换器

[snappy-switcher](https://github.com/OpalAayan/snappy-switcher) 由 _OpalAayan_ 开发：
适用于 Hyprland 的高速 Alt+Tab 窗口切换器，带有动画效果，用 C 编写（使用 Pango 和 Cairo）。

<a id="keyboard-layout-management"></a>

### 键盘布局管理

[hyprland-per-window-layout](https://github.com/coffebar/hyprland-per-window-layout/) 由 _MahouShoujoMivutilde 和 coffebar_ 开发：
让 Hyprland 的每个窗口都能使用独立的键盘布局。

<a id="editor-support-for-config-files"></a>

### 编辑器对配置文件的支持

[HyprLS](https://github.com/hyprland-community/hyprls) 由 _gwennlbh_ 开发：
一款 LSP 服务器，在 Neovim、VS Code 等编辑器中为 Hyprland 配置文件提供自动补全等功能。

<a id="keybind-management"></a>

### 键位绑定管理

[hyprKCS](https://github.com/kosa12/hyprKCS) 由 _kosa12_ 开发：
用 Rust 和 GTK4 编写的 Hyprland 键位绑定管理器，快速而精简。

<a id="ipc-wrappers"></a>

### IPC 封装

[hyprland-rs](https://github.com/yavko/hyprland-rs) 由 _yavko_ 开发：
用 Rust 为 Hyprland 的 IPC 提供了简洁的封装。

<a id="screen-shaders--color-temperature"></a>

### 屏幕着色器与色温

- [hyprshade](https://github.com/loqusion/hyprshade) 由 _loqusion_ 开发：
  可手动或定时切换屏幕着色器，也可用作[自动色温调节工具](https://en.wikipedia.org/wiki/F.lux)。
- [gammastep](https://gitlab.com/chinstrap/gammastep) 由 _Chinstrap_ 开发：
  根据一天中的时刻和地理位置自动调节色温。

<a id="wireless-settings"></a>

### 无线设置

- [iwgtk](https://github.com/J-Lentz/iwgtk) 由 _Jesse Lentz_ 开发：
  用 GTK 编写的 `iwd` Wi-Fi 设置前端。
- [blueberry](https://github.com/linuxmint/blueberry) 由 _Linux Mint_ 开发：
  用 GTK 编写的蓝牙设置前端。
- [Overskride](https://github.com/kaii-lb/overskride) 由 _kaii-lb_ 开发：
  用 GTK4 编写的蓝牙客户端，简单易用，功能强大。
- [nm-applet](https://gitlab.gnome.org/GNOME/network-manager-applet) 由 _GNOME_ 开发：
  用于与 NetworkManager 交互的 GTK 小程序。

<a id="automatically-mounting-using-udiskie"></a>

### 使用 `udiskie` 自动挂载设备

_启动方式：_ 手动配置（在 Hyprland 配置文件中添加自启动项）。

USB 大容量存储设备（如 U 盘、手机和数码相机等）不会自动挂载到文件系统。

通常需要手动挂载这些设备，常见做法是以 root 权限运行 `mount`。
许多流行的桌面环境通过封装 `udisks2` 的工具自动处理挂载。
`udiskie` 是 udisks2 的前端，可让你在用户空间管理光盘、U 盘等可移动介质。

通过软件包管理器安装 `udiskie`，也可以[手动构建](https://github.com/coldfix/udiskie/wiki/installation)。
打开 `hyprland.lua`，将 `udiskie` 加入自启动项。

[查看更多用法](https://github.com/coldfix/udiskie/wiki/Usage)。

<a id="other-useful-utilities"></a>

### 其他实用工具

[We Are Wayland Now](https://wearewaylandnow.com/) 网站详细介绍了其他适用于 Wayland 的实用工具和应用，例如程序坞和电子邮件客户端等，也提供了有关 Wayland 兼容性的实用信息。
