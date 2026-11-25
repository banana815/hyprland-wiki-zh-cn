# 入门教程

如果你是第一次使用 Hyprland，请从这篇教程开始。

本教程涵盖开始使用 Hyprland 所需的全部内容。
需要时，文中会给出其他页面的链接。

<a id="install-hyprland"></a>

## 安装 Hyprland

请参阅[安装指南](installation.md)，成功安装 Hyprland 后再回到这里。

安装 `kitty`（默认终端模拟器）。
大多数发行版的软件仓库都提供这个软件包。

<a id="nvidia"></a>

## 使用 NVIDIA 显卡？

> [!NOTE]
> 如果没有使用 NVIDIA 显卡，请跳过这一步。

启动前请先阅读 [NVIDIA 页面](../nvidia/_index.md)。
其中介绍了所需的环境和配置调整。

<a id="vm"></a>

## 使用虚拟机？

> [!NOTE]
> 如果没有使用虚拟机，请跳过这一步。

如果使用虚拟机，务必在 `virtio` 配置（或 `virt-manager`）中启用 3D 加速，否则 Hyprland _**无法运行**_。

也可以通过直通物理 GPU 来运行 Hyprland。

请留意，虚拟机中的 3D 加速可能相当慢。

<a id="launching-hyprland"></a>

## 启动 Hyprland

在 TTY 中输入 `start-hyprland` 即可启动 Hyprland。

> [!WARNING]
> **切勿**以 `root` 权限启动 Hyprland（不要使用 `sudo`）。

运行 `start-hyprland -- -h` 可以查看一些启动标志，例如指定配置文件路径、跳过上述权限检查等。

官方不支持登录管理器。以下是几种登录管理器的兼容情况：

- SDDM：运行正常。
  请安装 0.20.0 或更高版本的 SDDM，或使用[最新 Git 版本](https://github.com/sddm/sddm)
  （也可以从 AUR 安装 [sddm-git](https://aur.archlinux.org/packages/sddm-git)），
  以避开 SDDM 的 [1476 号缺陷](https://github.com/sddm/sddm/issues/1476)（关机耗时 90 秒）。
- plasma-login-manager：运行正常，但依赖 systemd。
- GDM：可以使用，但首次启动 Hyprland 时会导致 Hyprland 崩溃。
- greetd：运行正常，尤其是搭配 [ReGreet](https://github.com/rharish101/ReGreet) 时。
- ly：运行正常。

<a id="de-like-pre-configured-setups"></a>

## 类似桌面环境的预配置方案

想像使用桌面环境一样，直接使用配置好的 Hyprland，省去从头编写配置的步骤？

[预配置方案页面](preconfigured-setups.md)列出了几种选择。

这些配置文件应该能帮你完成所有设置，每套方案也都有自己的教程。

如果选用其中一套，可以跳过下一步。
不过，仍然建议读完再往后的各节。
其中介绍了推荐的应用、可替代旧 X11 软件的工具，以及配置显示器的方法等。

<a id="in-hyprland-with-the-default-config"></a>

## 使用 Hyprland 默认配置

到这里，已经可以用默认配置开始探索 Hyprland 了。

按 SUPER + Q 启动 kitty。
如果想先选好默认终端，可以在 `~/.config/hypr/hyprland.lua` 中设置（参见[配置示例](https://github.com/hyprwm/Hyprland/blob/main/example/hyprland.lua)）。

如果想用得更顺手，少花时间上网搜索，请继续往下读。

<a id="monitors-config"></a>

## 配置显示器

请参阅[显示器页面](../configuring/core/monitors/_index.md)，详细了解如何配置显示器。

<a id="fully-configure-hyprland"></a>

## 全面配置 Hyprland

请参阅[配置页面](../configuring/_index.md)，详细了解如何按自己的喜好配置 Hyprland。

<a id="important-software"></a>

## 重要软件

请参阅[必备软件页面](../useful-utilities/must-have.md)，了解让 Wayland、Hyprland 和其他应用正常运行所需的关键组件。

<a id="apps--x11-replacements"></a>

## 应用与 X11 软件替代品

相关介绍见[实用工具页面](../useful-utilities/_index.md)。
更完整的列表见 [Awesome-Hyprland](https://github.com/hyprland-community/awesome-hyprland) 仓库。

<a id="force-apps-to-use-wayland"></a>

## 强制应用使用 Wayland

许多应用默认使用 Wayland。
Chromium（以及其他基于 Chromium 的浏览器）和 Electron 应用默认不会使用 Wayland。
需要向这些应用传递 `--enable-features=UseOzonePlatform --ozone-platform=wayland`，或者在应用支持的情况下使用 `.conf` 文件设置这些参数。
基于 Chromium 的浏览器一般也可以在 `chrome://flags` 中切换到 Wayland。
搜索“ozone”，然后选择 Wayland。
如果使用 NixOS，还可以在配置中设置环境变量 `NIXOS_OZONE_WL=1`。

对于大多数 Electron 应用，应将上述参数写入 `~/.config/electron-flags.conf`。
请注意，已知这种方式对 VSCode **无效**。

[这里](../configuring/core/environment-variables.md)还列出了几个可强制启用 Wayland 模式的环境变量。

使用 `hyprctl clients` 可以检查应用是否通过 Xwayland 运行。

<a id="themes"></a>

## 主题

Hyprland 并非完整的桌面环境，因此需要使用 `lxappearance` 或 `nwg-look`（推荐）等工具设置 GTK 主题，使用 `hyprqt6engine` 设置 Qt 6 应用的主题。

<a id="cursors"></a>

## 光标

如果不熟悉设置方法，配置光标往往很棘手。
请参阅[常见问题中关于更改鼠标光标的条目](../faq/_index.md#how-do-i-change-my-mouse-cursor)。
