# 常见问题

<a id="symbol-lookup-errors"></a>

### 符号查找错误

如果你看到类似这样的错误：

```
<app>: symbol lookup error: <app>: undefined symbol: <symbol>
```

或：

```
<app>: error while loading shared libraries: <lib>: cannot open shared object file: No such file or directory.
```

或者有时没有任何报错，Hyprland 却在启动时或运行中随机崩溃，那么很可能是你自行构建了 Hyprland，而相关组件的版本已经不匹配。
每个 hypr\* 应用都依赖多个库。
如果更新了这些库，却没有重新构建整套 hypr\* 组件，就会出现上述错误或崩溃。

要彻底避免这类错误，_请使用预编译软件包，不要自行构建_。
如果选择自行构建，就得由**你**负责确保各组件的版本保持一致！

自行构建时，_所有 hypr\* 组件都必须自行构建_，不能一部分安装预编译软件包，另一部分从源码仓库构建。

**Arch 用户请注意：** 安装 `-git` 软件包也算自行构建。

构建顺序请见[这里](../getting-started/installation.md#manual-build)。

<a id="will-rest-of-the-hypr-ecosystem-switch-to-lua-from-hyprlang"></a>

### Hypr\* 生态中的其他项目也会从 hyprlang 切换到 Lua 吗？

Hyprland 将继续使用 Lua。
其他 Hypr\* 项目目前没有从 Hyprlang 迁移的计划。

<a id="my-apps-are-pixelated"></a>

### 我的应用显示有锯齿

这说明它们是通过 Xwayland 运行的，而 Xwayland 本身无法进行分数缩放。

要强制它们以原生 Wayland 模式运行，请参阅[主教程](../getting-started/master-tutorial.md#force-apps-to-use-wayland)。

如果它们无法以原生 Wayland 模式运行，请参阅 [Xwayland 页面](../configuring/extra/xwayland.md)。

<a id="my-external-monitor-is-blank--doesnt-render--receives-no-signal-laptop"></a>

### 笔记本电脑的外接显示器黑屏、没有画面或收不到信号

对于使用 NVIDIA 显卡的系统，525.60.11 及更高版本的 NVIDIA 驱动似乎已解决此问题，但旧版驱动可能仍有这个问题。

对于硬件受限的系统（例如使用集成显卡、USB-C 或 USB 集线器的系统），请在配置中将环境变量 `AQ_NO_MODIFIERS` 设为 `1`。
要确认你遇到的是否正是这个问题，可以获取 [DRM 日志](../crashes-and-bugs/_index.md#debugging-drm-issues)，并在其中查找以下内容：

```plain
Requested display configuration exceeds system DDB limitations
```

除此之外，还可以尝试以下几种方法，_可能_对你有效：

1. _只用_外接显示器。  
   设置环境变量 `AQ_DRM_DEVICES=/dev/dri/card1`（也可能是 `card0`），可以强制 Hyprland 只使用独立显卡。这样笔记本内置屏幕将不再显示画面，但外接显示器可以正常工作。
1. 使用所有显示输出，代价是电池续航缩短。  
   在 BIOS 中将笔记本设为只使用独立显卡，_可能_就能让所有显示输出正常工作，但耗电量会很高。

> [!NOTE]
> 这些方法的效果很大程度上取决于具体机型，未必有效。
> 如果都不奏效，恐怕就没有什么办法了。

不过，你还可以试试 USB-C 转 HDMI 适配器，这样外接显示器或许能通过集成显卡输出画面。

<a id="how-do-i-screenshot"></a>

### 如何截图？

从[截图与录屏](../useful-utilities/screenshots-and-recording.md)中选择一个工具并完成配置即可。

<a id="screenshare--obs-no-worky"></a>

### 屏幕共享或 OBS 无法使用

请参阅[屏幕共享](../useful-utilities/screen-sharing.md)。

要使用 OBS，还必须安装 `qt6-wayland`。

<a id="how-do-i-change-my-wallpaper"></a>

### 如何更换壁纸？

请参阅[壁纸](../useful-utilities/wallpapers.md)。

<a id="how-heavy-is-this"></a>

### Hyprland 的资源占用有多高？

只比 Xorg 高一点。
如果想获得最佳性能，可以考虑关闭模糊效果和动画。

<a id="my-monitor-no-worky"></a>

### 我的显示器无法正常工作

试着在配置中更改显示模式。
如果首选模式无法使用，请尝试分辨率或刷新率较低的模式。
要查看显示器报告的模式列表，请运行 `hyprctl monitors`。

<a id="my-monitor-has-flickering-brightness-when-i-turn-on-vrr"></a>

### 开启 VRR 后，显示器亮度忽明忽暗

将 VRR 选项设为 `2`（全屏），让它只在玩游戏时启用。
有些显示器的亮度会随刷新率变化。如果刷新率快速变化（例如按键后屏幕短暂刷新），亮度也会随之快速变化。

如果仍想始终开启 VRR，可以修改显示器 EDID 中的 VRR 范围，以减轻甚至消除闪烁。
详情请参阅 [Arch Wiki](https://wiki.archlinux.org/title/Kernel_mode_setting#Forcing_modes_and_EDID)。

<a id="how-do-i-update"></a>

### 如何更新？

在克隆的仓库目录中打开终端。

```bash
git pull
make all && sudo make install
```

如果使用 AUR 软件包（`hyprland-git`），更新时需要清理旧的构建文件并重新构建。
Paru 以前在更新时出过问题，请使用 Yay。

<a id="how-do-i-screen-lock"></a>

### 如何锁屏？

请使用兼容 Wayland 且支持 WLR 协议的锁屏工具（例如 `swaylock`）。
请注意，即使已锁屏，仍可使用 `Ctrl-Alt-F1` 至 `F7` 这组快捷键切换 TTY。

<a id="how-do-i-change-my-mouse-cursor"></a>

### 如何更换鼠标指针？

请参阅 [hyprcursor](../hypr-ecosystem/user/hyprcursor.md)。

1. 使用 [nwg-look](https://github.com/nwg-piotr/nwg-look) 设置 GTK 指针。
1. 将 `hyprctl setcursor [THEME] [SIZE]` 添加到配置的自动启动命令中，然后重启 Hyprland。

如果使用 flatpak，请运行 `flatpak override --filesystem=~/.themes:ro --filesystem=~/.icons:ro --user`。
将主题同时放入 `/usr/share/themes` 和 `~/.themes`，并将图标和指针同时放入 `/usr/share/icons` 和 `~/.icons`。

对于 Qt 应用，Hyprland 会将环境变量 XCURSOR_SIZE 导出为默认值 24。
可以使用 `env` 将 XCURSOR_SIZE 设为其他值，覆盖默认设置。

也可以尝试运行 `gsettings set org.gnome.desktop.interface cursor-theme 'theme-name'`，或将这条命令添加到配置中的自动启动命令之后。

如果不想安装 GTK 设置编辑器，请按照 [XDG 规范](https://wiki.archlinux.org/title/Cursor_themes#Configuration)修改配置文件。
如果没有使用 `nwg-look` 之类的工具，请务必同时编辑 `~/.config/gtk-4.0/settings.ini` 和 `~/.gtkrc-2.0`。

<a id="gtk-settings-no-work--whatever"></a>

### GTK 设置不生效或有其他问题

[https://github.com/swaywm/sway/wiki/GTK-3-settings-on-Wayland](https://github.com/swaywm/sway/wiki/GTK-3-settings-on-Wayland)

<a id="my-program-name-is-freezing"></a>

### 我的 [程序名] 卡住了

请确保通知守护进程正在运行，例如 `dunst`。
如果常规的 D-Bus 自动启动机制失效，可以在配置中设置自动启动通知守护进程。

<a id="waybar-workspaces-no-worky"></a>

### Waybar 的工作区功能无法使用？

使用 Waybar 时，有一些注意事项和设置需要了解。
解决方法请参阅[状态栏](../useful-utilities/status-bars.md)。

<a id="how-do-i-autostart-my-favorite-apps"></a>

### 如何自动启动常用应用？

可以使用窗口规则将应用分配到工作区，这样就能在不同工作区打开多个应用。
以下方法可以静默启动这些应用（即屏幕不会因来回切换工作区而闪烁）。

例如，在 `hyprland.lua` 中添加以下内容：

```lua
hl.on("hyprland.start", function()
  hl.exec_cmd("kitty")
  hl.exec_cmd("dolphin")
  hl.exec_cmd("dunst")
  hl.exec_cmd("amongus", { workspace = "1 silent" })
end)
```

<a id="how-do-i-move-my-favorite-workspaces-to-a-new-monitor-when-i-plug-it-in"></a>

### 插入新显示器时，如何将常用工作区移到上面？

可以监听 `monitor.added` 事件，并在事件触发时将工作区移到新显示器上。

<a id="my-tablet-no-worky"></a>

### 我的数位板无法使用？

请使用 [Open Tablet Driver](https://github.com/OpenTabletDriver/OpenTabletDriver) 配置数位板。
今后将支持直接在配置文件中设置数位板。
在此之前，请使用 OTD。

<a id="some-of-my-apps-take-a-really-long-time-to-open"></a>

### 为什么有些应用要等很久才能打开？

```lua {filename="~/.config/hypr/hyprland.lua"}
hl.on("hyprland.start", function()
  hl.exec_cmd("dbus-update-activation-environment --systemd WAYLAND_DISPLAY XDG_CURRENT_DESKTOP")
end)
```

请确保桌面门户（portal）在上述命令_执行之后_才启动。
在某些系统上，桌面门户可能会提前启动。

在这种情况下，可以使用类似下面的脚本：

```bash
#!/usr/bin/env bash
sleep 4
killall -e xdg-desktop-portal-hyprland
killall xdg-desktop-portal
/usr/lib/xdg-desktop-portal-hyprland &
sleep 4
/usr/lib/xdg-desktop-portal &
```

在系统启动时运行这个脚本，应该就能解决上述问题。
可以根据需要调整脚本中的等待时间。

<a id="how-do-i-export-env-vars-for-hyprland"></a>

### 如何为 Hyprland 导出环境变量？

可以使用 `hl.env()` 函数。例如：

```lua
hl.env("XDG_CURRENT_DESKTOP", "Hyprland")
```

详情请参阅[环境变量](../configuring/core/environment-variables.md)。

<a id="how-to-disable-middle-click-paste"></a>

### 如何禁用鼠标中键粘贴？

将 `misc.middle_click_paste` 设为 `false` 即可彻底禁用中键粘贴，但某些浏览器（尤其是 Firefox）会通过自身的内置机制模拟此功能。
这种情况下，还必须在浏览器设置中禁用该功能。

<a id="my-apps-take-a-long-time-to-start--cant-screenshare"></a>

### 我的应用启动缓慢或无法共享屏幕

请参阅 [XDPH 页面](../hypr-ecosystem/user/xdg-desktop-portal-hyprland.md#debugging)。

很可能是系统中安装了多个桌面门户实现，或某个实现未能启动。

<a id="my-screenshot-utilities-wont-work-with-multiple-screens"></a>

### 我的截图工具在多显示器环境下无法使用

Flameshot 等程序目前对 Wayland 的支持有限，可以考虑使用专为 Wayland 开发的原生截图工具。

<a id="i-cannot-bind-super-as-my-mod-key-on-my-laptop"></a>

### 笔记本电脑上无法将 SUPER 绑定为修饰键

许多笔记本电脑内置了切换功能，可将 `SUPER` 键切换到单次按键模式或按住模式。
`SUPER` 键上的挂锁图标通常表示它支持这项功能。

先安装并运行 `wev`，然后按住 `SUPER`。
如果看到按键按下事件后立即出现释放事件，那么 `SUPER` 键很可能处于单次按键模式。

在大多数笔记本电脑上，按 `FN+SUPER` 即可解决这个问题，然后可以用 `wev` 验证。
按住 `SUPER` 时，应该不会立即出现按键释放事件。
如果 `FN+SUPER` 不起作用，请查阅笔记本电脑的使用手册。

<a id="my-vm-doesnt-receive-keybinds-i-have-set-in-hyprland"></a>

### 虚拟机收不到我在 Hyprland 中设置的键位绑定

这是正常现象，因为 Hyprland 会优先处理这些按键。
一个简单的解决办法是创建一个空的“直通”子映射：

```lua
hl.define_submap("passthru", function()
  hl.bind("SUPER + Escape", hl.dsp.submap("reset"))
end)
hl.bind("...", hl.dsp.submap("passthru"))
```

按下选定的组合键后，就会进入直通模式。在此模式下，Hyprland 会忽略你的键位绑定，将按键事件传给虚拟机。
按 `SUPER + Escape` 即可退出该模式。

<a id="steams-file-picker-no-worky"></a>

### Steam 的文件选择器用不了

如果你的 Steam 库位于另一个驱动器上，需要将其添加到 Steam，那么在 Steam 中选择目录时，Hyprland 的文件选择器通常不会弹出。

Steam 自带文件选择器，但它无法正常工作。
安装 `xdg-desktop-portal-gtk` 即可调出桌面的文件选择器。



<a id="i-get-a-so-file-missing-error-on-launch"></a>

### 启动时提示缺少 .so 文件

如果你使用 -git 软件包，遇到破坏 ABI 兼容性的更新时，这种情况很常见。

> [!WARNING]
> ***千万不要***在不同版本的 .so 文件之间创建符号链接，这会导致程序崩溃！

请找出所有已安装且名称中带 `-git` 的 hypr\* 软件包，卸载后重新安装（可能还需要卸载它们的依赖包）。

如果使用 yay，请确保对每个软件包都执行 `CleanBuild`。
如果使用 paru，请手动删除 `~/.cache/paru` 中 hypr\* 软件包的缓存。

如果你没有使用任何 -git 软件包，那就是发行版的打包出了问题，应由发行版修复。

<a id="my-cursor-is-a-hyprland-icon"></a>

### 为什么我的光标变成了 Hyprland 图标？

这表示你没有安装 hyprcursor 主题，而且 Hyprland 也找不到 XCursor 主题。
请安装一个光标主题。

<a id="smart-gaps-please"></a>

### 怎么设置智能间距？

请看[这里](../configuring/code-snippets.md#smart-gaps)。

<a id="i-cant-create-discord-binds"></a>

### 我无法在 Discord 中创建键位绑定

你的配置里很可能设置了 `ELECTRON_OZONE_PLATFORM_HINT = wayland`。

试着用 `ELECTRON_OZONE_PLATFORM_HINT= discord` 启动 Discord。

> [!WARNING]
> 请注意，这会让 Discord 在 Xwayland 下运行。

如果有效，请找到 Discord 的桌面条目文件（通常位于 `/usr/share/applications/`）。
复制一份，将副本中的 `Exec=/usr/bin/discord` 替换为 `Exec=env -u ELECTRON_OZONE_PLATFORM_HINT /usr/bin/discord`。
你也可以给副本起个新名字（例如 `Name=DiscordX`），方便区分两个条目。

<a id="fullscreen-applicationssteam-games-open-with-secondary-monitors-resolution"></a>

### 全屏应用和 Steam 游戏启动时使用副显示器的分辨率

原因很可能是 X11 的默认显示器并非你想用的主显示器。
可以按以下步骤解决：

在配置的自动启动项中添加 `xrandr --output [MONITOR_ID] --primary`，并将 `[MONITOR_ID]` 替换为主显示器的 ID（例如 `DP-3`）。
运行 `hyprctl monitors` 即可查看显示器 ID。

将这条命令添加到 Hyprland 配置后，X11 应用就会默认使用你的主显示器。

<a id="my-mouse-cursor-keeps-escaping-the-game-window"></a>

### 我的鼠标光标总是跑出游戏窗口！

大多数游戏都能自动将光标锁定在窗口内，你也可以使用 `confine_pointer` 窗口规则，让 Hyprland 来锁定光标。
要对所有内容类型为 'game' 的全屏应用生效，使用以下规则即可：

```lua
hl.window_rule({ match = { content = "game", fullscreen = true }, confine_pointer = true })
```

<a id="spring-damping"></a>

### 弹簧阻尼拼作 `damping`？

是的，拼作 `damping`。是 `damping`，不是 `dampening`。

https://en.wikipedia.org/wiki/Damping

<a id="blur"></a>

### 模糊效果

如果模糊效果在某些应用中不起作用，可能是因为这些应用使用了背景效果协议，而应用设置中禁用了模糊效果。

已知 GTK 4 默认在整个工具包中禁用了模糊效果。
你可以设置环境变量 `GDK_WAYLAND_DISABLE=ext_background_effect_manager_v1` 来禁用 GTK 中的这一协议，也可以在 gtk.css 中为特定元素启用模糊效果，例如使用 `window { backdrop-filter: blur(20px); }`。
要了解应为哪些元素设置样式，请查阅客户端文档。
