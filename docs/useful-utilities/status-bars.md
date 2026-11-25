# 状态栏

<a id="simple-status-bars"></a>

## 简易状态栏

通常只需写很少的代码，甚至无需编程，就能调整小组件的顺序和样式。

<a id="waybar"></a>

### Waybar

Waybar 是专为基于 wlroots 的合成器设计的 GTK 状态栏，默认支持 Hyprland。
建议通过发行版提供的软件包安装 Waybar。

开始配置前，先将配置文件从 `/etc/xdg/waybar/` 复制到 `~/.config/waybar/`。

要使用工作区模块，请将配置中所有的 `sway/workspaces` 替换为 `hyprland/workspaces`。
同时，将所有的 `sway/mode` 替换为 `hyprland/submap`。

有关配置的更多信息，请参阅 [Waybar Wiki](https://github.com/Alexays/Waybar/wiki/Module:-Hyprland)。

<a id="how-to-launch"></a>

#### 启动方法

在终端中输入 `waybar`。
要让 Waybar 随 Hyprland 一起启动，请将 `waybar` 添加到 Hyprland 配置的自启动项中。

Waybar 也提供 systemd 服务。
如果你通过 [uwsm](uwsm.md) 使用 Hyprland，可以用以下命令启用该服务：

```sh
systemctl --user enable --now waybar.service
```

<a id="waybar-faq"></a>

#### Waybar 常见问题

<a id="active-workspace-doesnt-show-up"></a>

##### 当前工作区未显示

在 `~/.config/waybar/style.css` 中，将 `#workspaces button.focused` 替换为 `#workspaces button.active`。

<a id="scrolling-through-workspaces"></a>

##### 滚动切换工作区

由于 `hyprland/workspaces` 缺少 `sway/workspaces` 中的许多配置选项，你可能需要自行实现部分功能。
例如，要通过滚动切换工作区，可以这样配置：

```json
"hyprland/workspaces": {
     "format": "{icon}",
     "on-scroll-up": "hyprctl dispatch 'hl.dsp.focus({workspace=\"e+1\"})' ",
     "on-scroll-down": "hyprctl dispatch 'hl.dsp.focus({workspace=\"e-1\"})' ",
}
```

<a id="window-title-is-missing"></a>

##### 窗口标题未显示

用于显示标题的窗口模块使用 `hyprland` 前缀，而非 `wlr`。
请在 Waybar 配置中添加以下模块：

```json
"modules-center": ["hyprland/window"],
```

如果使用多个显示器，可以考虑添加以下选项：

```json
"hyprland/window": {
    "separate-outputs": true
},
```

<a id="ashell"></a>

### ashell

[ashell](https://malpenzibo.github.io/ashell/) 是一款面向 Hyprland、开箱即用的 Wayland 状态栏。

- Ashell 安装后即可使用。
  装好就能启动，只需按需调整配置。
- Ashell 自带工作区、时间、电池、网络等常用模块。
  无需四处寻找插件或编写自定义脚本。
- 基于 Rust 跨平台图形界面库 iced 构建。
- 配置选项较少。
  这既是优点，也是局限。
  你可以很快配置出不错的效果，但无法像使用 Waybar 那样进行一些高度个性化的调整。

<a id="desktop-shells"></a>

## 桌面 Shell

这类软件将状态栏、启动器、通知和锁屏等工具集成在同一个软件包中。
几乎无需编程，装好就能获得类似完整桌面环境的体验。

<a id="noctalia"></a>

### Noctalia

[Noctalia](https://noctalia.dev/) 是一款美观、简约的 Wayland 桌面 Shell。

- 采用精简的现代技术栈，外观沉静且独具特色，可按个人桌面风格调整。
- 主题设置丰富，既可选用预设配色，也可根据壁纸自动生成配色。
- 通知系统支持查看历史记录和开启勿扰模式。
- 支持插件。
- 基于 Quickshell 构建。

<a id="dankmaterialshell"></a>

### DankMaterialShell

[DankMaterialShell](https://danklinux.com/) 是一款功能完整的桌面 Shell，设计灵感来自 Material 3，适用于 Hyprland 和其他 Wayland 合成器。

- 自带状态栏、启动器、通知中心、控制中心和锁屏，一个软件包即可替代 waybar、fuzzel、mako、swaylock 等工具。
- 可根据壁纸自动生成主题，并将其应用到 GTK/Qt 应用和终端。
- 可通过内置的图形设置应用进行配置，也可通过插件和小组件扩展功能。
- 基于 Quickshell 和 Go 构建。

<a id="widget-systems"></a>

## 小组件系统

如果想要自行设计菜单并完全掌控布局，可以使用小组件系统。
通常需要编写代码，但小组件系统能显著简化这项工作。
以下按字母顺序列出三种常用选择。

|   | [AGS/Astal](https://aylur.github.io/astal/) | [EWW](https://elkowar.github.io/eww/) | [Quickshell](https://quickshell.outfoxxed.me/) |
|--------------------------|--------------------|-------------------|-------------------|
| 界面工具包 | GTK 3/4 | GTK 3 | Qt |
| 配置语言 | JS(X)、TS 或其他支持 [GObject 内省](https://en.wikipedia.org/wiki/List_of_language_bindings_for_GTK)的语言 | Yuck（EWW 的 Lisp 方言） | QML |

<a id="agsastal"></a>

### AGS/Astal

- [Astal](https://aylur.github.io/astal/) 是一套工具和框架，可用 GTK 构建桌面 Shell 和 Wayland 小组件。
- [AGS](https://aylur.github.io/ags/)（Aylur's GTK Shell）是一个脚手架工具，适用于使用 TypeScript 或 JavaScript(X) 的 Astal 项目。
  它简化了使用这些语言创建 Astal 项目的过程。

要开始使用 Astal，请参阅[安装说明](https://aylur.github.io/astal/guide/installation)和[示例](https://aylur.github.io/astal/guide/introduction#supported-languages)。
要使用 AGS，请参阅其[快速入门](https://aylur.github.io/ags/guide/quick-start.html)页面。

<a id="advantages"></a>

#### 优点

- 语言选择灵活：只要你喜欢的语言支持 [GObject 内省](https://en.wikipedia.org/wiki/List_of_language_bindings_for_GTK)，就可以使用它（不过 AGS 对 JS(X) 和 TS 的支持最完善）。
- 提供丰富的库，涵盖网络（Wi-Fi 和以太网）、蓝牙等功能。

<a id="disadvantages"></a>

#### 缺点

- 默认不支持热重载。

<a id="eww"></a>

### Eww

[Eww](https://github.com/elkowar/eww)（ElKowar's Wacky Widgets）是一个用 Rust 和 GTK 构建的小组件系统，可以像在 AwesomeWM 中一样创建自定义小组件。
主要区别在于，Eww 不依赖特定的窗口管理器或合成器。

可以在发行版的软件包管理器中搜索 `eww-wayland` 并安装 Eww，也可以手动编译。
如果选择手动编译，请参阅 Eww 的[官方说明](https://elkowar.github.io/eww)。

<a id="advantages-1"></a>

#### 优点

- 与其他配置语言相比，其类似 Lisp 的配置语法较为简单。
- 原生支持使用 SCSS 设置样式。

<a id="disadvantages-1"></a>

#### 缺点

- 自带的库较少，因此很大程度上依赖外部脚本和程序。
- 性能方面有以下局限：
  - 仅支持 GTK 3，而 GTK 3 不支持 GPU 加速。
  - 调用外部脚本会产生开销，重新计算数据时也会因不必要地重新创建组件而增加开销。

<a id="configuration"></a>

#### 配置

[自述文件](https://github.com/elkowar/eww)中列出了几个示例。
也强烈建议通读[配置选项](https://elkowar.github.io/eww/configuration.html)。

> [!WARNING]
> 请仔细阅读 [Wayland 一节](https://elkowar.github.io/eww/configuration.html#wayland)，否则 Eww 将无法在 Hyprland 上运行。

以下小组件示例可能对 Hyprland 用户有所帮助：


<details><summary>工作区小组件</summary>


此小组件列出编号为 1 至 10 的工作区。
点击任一工作区即可跳转，在小组件上滚动则可循环切换工作区。
可以为当前工作区、已有窗口的工作区和空工作区分别设置样式。
此小组件依赖以下程序：
[bash](https://linux.die.net/man/1/bash)、
[awk](https://linux.die.net/man/1/awk)、
[stdbuf](https://linux.die.net/man/1/stdbuf)、
[grep](https://linux.die.net/man/1/grep)、
[seq](https://linux.die.net/man/1/seq)、
[socat](https://linux.die.net/man/1/socat)、
[jq](https://stedolan.github.io/jq/)
和 [Python 3](https://www.python.org/)。

<a id="configewwyuck"></a>

##### `~/.config/eww.yuck`

```lisp
...
(deflisten workspaces :initial "[]" "bash ~/.config/eww/scripts/get-workspaces")
(deflisten current_workspace :initial "1" "bash ~/.config/eww/scripts/get-active-workspace")
(defwidget workspaces []
  (eventbox :onscroll "bash ~/.config/eww/scripts/change-active-workspace {} ${current_workspace}" :class "workspaces-widget"
    (box :space-evenly true
      (label :text "${workspaces}${current_workspace}" :visible false)
      (for workspace in workspaces
        (eventbox :onclick "hyprctl dispatch workspace ${workspace.id}"
          (box :class "workspace-entry ${workspace.windows > 0 ? "occupied" : "empty"}"
            (label :text "${workspace.id}" :class "workspace-entry ${workspace.id == current_workspace ? "current" : ""}" )
            )
          )
        )
      )
    )
  )
...
```

<a id="configewwscriptschange-active-workspace"></a>

##### `~/.config/eww/scripts/change-active-workspace`

```sh
#!/usr/bin/env bash
function clamp {
  min=$1
  max=$2
  val=$3
  python -c "print(max($min, min($val, $max)))"
}

direction=$1
current=$2
if test "$direction" = "down"
then
  target=$(clamp 1 10 $(($current+1)))
  echo "jumping to $target"
  hyprctl dispatch workspace $target
elif test "$direction" = "up"
then
  target=$(clamp 1 10 $(($current-1)))
  echo "jumping to $target"
  hyprctl dispatch workspace $target
fi
```

<a id="configewwscriptsget-active-workspace"></a>

##### `~/.config/eww/scripts/get-active-workspace`

```sh
#!/usr/bin/env bash

hyprctl monitors -j | jq '.[] | select(.focused) | .activeWorkspace.id'

socat -u UNIX-CONNECT:$XDG_RUNTIME_DIR/hypr/$HYPRLAND_INSTANCE_SIGNATURE/.socket2.sock - |
  stdbuf -o0 awk -F '>>|,' -e '/^workspace>>/ {print $2}' -e '/^focusedmon>>/ {print $3}'
```

<a id="configewwscriptsget-workspaces"></a>

##### `~/.config/eww/scripts/get-workspaces`

```sh
#!/usr/bin/env bash

spaces (){
  WORKSPACE_WINDOWS=$(hyprctl workspaces -j | jq 'map({key: .id | tostring, value: .windows}) | from_entries')
  seq 1 10 | jq --argjson windows "${WORKSPACE_WINDOWS}" --slurp -Mc 'map(tostring) | map({id: ., windows: ($windows[.]//0)})'
}

spaces
socat -u UNIX-CONNECT:$XDG_RUNTIME_DIR/hypr/$HYPRLAND_INSTANCE_SIGNATURE/.socket2.sock - | while read -r line; do
  spaces
done
```



</details>


<details><summary>活动窗口标题小组件</summary>


此小组件仅显示当前活动窗口的标题。
它依赖以下程序：
[awk](https://linux.die.net/man/1/awk)、
[stdbuf](https://linux.die.net/man/1/stdbuf)、
[socat](https://linux.die.net/man/1/socat)
和 [jq](https://stedolan.github.io/jq/)。

<a id="configewwewwyuck"></a>

##### `~/.config/eww/eww.yuck`

```lisp
...
(deflisten window :initial "..." "sh ~/.config/eww/scripts/get-window-title")
(defwidget window_w []
  (box
    (label :text "${window}"
    )
  )
...
```

<a id="configewwscriptsget-window-title"></a>

##### `~/.config/eww/scripts/get-window-title`

```sh
#!/bin/sh
hyprctl activewindow -j | jq --raw-output .title
socat -u UNIX-CONNECT:$XDG_RUNTIME_DIR/hypr/$HYPRLAND_INSTANCE_SIGNATURE/.socket2.sock - | stdbuf -o0 awk -F '>>|,' '/^activewindow>>/{print $3}'
```



</details>

<a id="quickshell"></a>

### Quickshell

[Quickshell](https://quickshell.outfoxxed.me/) 是一款基于 QtQuick 的灵活桌面 Shell 工具包。
虽然 Qt 的主题定制出了名地困难，但 Quickshell 的样式可以独立设置。

入门请参阅[设置说明](https://quickshell.outfoxxed.me/docs/configuration/getting-started/)和 [Hello World 分步教程](https://quickshell.outfoxxed.me/docs/configuration/intro/)。

<a id="advantages-2"></a>

#### 优点

- 提供与 Wayland 和 Hyprland 深度集成的功能，例如实时窗口预览。
- 默认会在配置更改后自动重新加载。

<a id="disadvantages-2"></a>

#### 缺点

- 由于 Qt 的定位机制，使用 Qt 布置组件时可能不如 GTK 直观。
- 截至本文撰写时，尚未提供 Wi-Fi 服务。
- 仍处于 alpha 阶段，后续可能会有小幅的不兼容改动。
- 样式通过组件声明，而不是用 CSS 编写，部分用户可能不太熟悉这种方式。

<a id="tips"></a>

## 提示

<a id="blur"></a>

### 模糊效果

使用 `blur` 和 `ignore_alpha` [图层规则](../configuring/core/rules/layer-rules.md)。
前者启用模糊效果，后者让模糊效果忽略不透明度过低的区域。
理想情况下，`ignore_alpha` 的值应高于阴影的不透明度，同时低于状态栏或菜单内容的不透明度。
如果状态栏或菜单带有透明弹出窗口，还可以使用 `blur_popups` 规则。
