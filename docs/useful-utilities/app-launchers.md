# 应用启动器

<a id="hyprlauncher"></a>

## Hyprlauncher

Hyprlauncher 是 Hyprland 官方提供的多用途工具，既可作为启动器，也可作为选择器。
有关用法和配置，请参阅[使用与配置说明](../hypr-ecosystem/user/hyprlauncher.md)。

<a id="rofi"></a>

## Rofi

Rofi 既是窗口切换器和应用启动器，也可替代 `dmenu`。
自 2025 年起，Rofi 支持 Wayland。
[GitHub](https://github.com/davatorium/rofi)

<a id="wofi"></a>

## Wofi

Wofi 是一款基于 GTK、可自定义的 Wayland 启动器。
[SourceHut](https://hg.sr.ht/~scoopta/wofi)

<a id="bemenu"></a>

## bemenu

bemenu 是 dmenu 的 Wayland 原生替代品。
[GitHub](https://github.com/Cloudef/bemenu)




<a id="fuzzel"></a>

## fuzzel

Fuzzel 是一款适用于基于 wlroots 的 Wayland 合成器的应用启动器，用法类似于 Rofi 的 `drun` 模式。
[Codeberg](https://codeberg.org/dnkl/fuzzel)

<a id="tofi"></a>

## tofi

tofi 可在基于 wlroots 的 Wayland 合成器中替代 dmenu 或 Rofi，速度极快、简单易用，而且支持高度自定义。
配置得当时，tofi 的界面可以在一帧之内显示出来。
[GitHub](https://github.com/philj56/tofi)

<a id="emacs"></a>

## Emacs

如果你已经在运行 Emacs 服务器，可以直接用 Emacs 启动应用。

配置方法可参考 [DistroTube 的 Configuring Emacs](https://gitlab.com/dwt1/configuring-emacs/-/blob/main/07-the-final-touches/scripts/app-launchers.el?ref_type=heads) 或 [Sebastian Wae 的 `app-launcher`](https://github.com/SebastienWae/app-launcher) 仓库。

<a id="anyrun"></a>

## Anyrun

Anyrun 是一款类似 krunner 的 Wayland 原生启动器，设计时注重可定制性。
它采用模块化设计，可通过插件扩展。
启用 Applications 插件后，即可将它用作应用启动器。
[GitHub](https://github.com/anyrun-org/anyrun)

<a id="walker"></a>

## Walker

Walker 是一款可扩展的 Wayland 原生启动器，内置多种模块（截至 2024-03-15，包括应用程序、命令运行器、Hyprland 窗口和网页搜索）。
它可以作为服务运行，以缩短启动时间。
[GitHub](https://github.com/abenz1267/walker)

<a id="vicinae"></a>

## Vicinae

Vicinae 是一款使用 C++ 和 Qt 开发的原生启动器，主要面向 Wayland。
它内置多种模块。
它以服务器形式在后台运行。
它通过兼容层支持 Raycast 扩展。
[GitHub](https://github.com/vicinaehq/vicinae)

---

更完整的启动器列表见 [awesome-hyprland](https://github.com/hyprland-community/awesome-hyprland#runners-menus-and-application-launchers)。
