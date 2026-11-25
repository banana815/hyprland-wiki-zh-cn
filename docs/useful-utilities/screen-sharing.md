# 屏幕共享

在 Wayland 上，屏幕共享通过 PipeWire 实现。

<a id="prerequisites"></a>

## 前提条件

确保已安装并启用 `pipewire`、`wireplumber` 和 [`xdg-desktop-portal-hyprland`](../hypr-ecosystem/user/xdg-desktop-portal-hyprland.md)，且三者均在运行。

确保配置中的 `bitdepth` 与实际显示器的色深一致。
参见[显示器](../configuring/core/monitors/_index.md)。

<a id="xwayland"></a>

## Xwayland

如果屏幕共享应用（如 Discord 或 Skype）运行在 Xwayland 下，它就只能看到其他 Xwayland 窗口，无法共享整个屏幕或 Wayland 窗口。

KDE 团队为此开发了 [xwaylandvideobridge](https://invent.kde.org/system/xwaylandvideobridge) 作为变通方案。
在 Arch Linux 上，可以使用[这个 AUR 软件包](https://aur.archlinux.org/packages/xwaylandvideobridge-git)。
请注意，Hyprland 目前不支持 xwaylandvideobridge 隐藏主窗口的方式，因此需要自行添加窗口规则来实现相同的效果。
详情参见[这个 issue](https://invent.kde.org/system/xwaylandvideobridge/-/issues/1)。
例如：

```lua
hl.window_rule({
    name = "xwayland-video-bridge-fixes",
    match = {
        class = "xwaylandvideobridge"
    },

    no_initial_focus = true,
    no_focus = true,
    no_anim = true,
    no_blur = true,
    max_size = {1,1},
    opacity = 0.0
})
```
