# Xwayland

Xwayland 是连接传统 Xorg 程序与 Wayland 合成器的桥梁。

<a id="hidpi-xwayland"></a>

## HiDPI 屏幕上的 Xwayland

由于 Xorg 无法进行缩放，目前 Xwayland 窗口在 HiDPI 屏幕上会有明显的像素感。

将 [`force_zero_scaling`](../core/config-options.md#xwayland) 选项设为 true 可缓解此问题，此设置会强制禁用 Xwayland 窗口缩放。

这样可以消除像素感，但应用程序仍无法按合适的比例显示。要正确缩放应用程序，需使用各工具包自身的缩放机制。

```lua
-- 将显示器切换到高分辨率，最后一个参数是缩放系数
hl.monitor({ output = "", mode = "highres", position = "auto", scale = "2" })

-- 取消 Xwayland 缩放
hl.config({
  xwayland = {
    force_zero_scaling = true
  }
})

-- 各工具包的缩放设置
hl.env("GDK_SCALE", "2")
hl.env("XCURSOR_SIZE", "32")
```

GDK_SCALE 变量不会与原生 Wayland GTK 程序冲突。

> [!WARNING]
> Xwayland HiDPI 补丁已不再受支持。请勿使用这些补丁。

<a id="abstract-unix-domain-socket"></a>

## 抽象 Unix 域套接字

X11 应用程序使用 Unix 域套接字与 Xwayland 通信。在 Linux 上，libX11 优先使用抽象 Unix 域套接字。这类套接字使用单独的抽象命名空间，独立于宿主机文件系统。这使抽象套接字更加灵活，但也使 Flatpak 等沙箱更难对其进行[隔离](https://github.com/hyprwm/Hyprland/pull/8874)。不过，移除抽象套接字也会带来[潜在的](https://gitlab.gnome.org/GNOME/mutter/-/issues/1613)安全性和兼容性问题。

为帮助解决这些问题，我们提供了 [`create_abstract_socket`](../core/config-options.md#xwayland) 选项。禁用抽象套接字后，只会创建常规 Unix 域套接字。

_\* 抽象 Unix 域套接字仅适用于基于 Linux 的系统_
