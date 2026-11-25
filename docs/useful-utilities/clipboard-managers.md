# 剪贴板管理器

_启动方式：_ 手动添加到 Hyprland 配置的自启动项中

剪贴板管理器可以方便地整理和访问之前复制的内容，包括文本和图像。
常见的剪贴板管理器有：

- [`cliphist`](https://github.com/sentriz/cliphist) - 通过 `wl-clipboard` 在 Wayland 下工作，可保存文本、图像及任意二进制数据。
- [`clipman`](https://github.com/chmouel/clipman) - 通过 `wl-clipboard` 在 Wayland 下工作，仅保存文本。
- [`clipvault`](https://github.com/rolv-apneseth/clipvault) - 通过 `wl-clipboard` 在 Wayland 下工作，可保存文本、图像及任意二进制数据。
  它可替代 `cliphist`，并提供一些额外功能，例如设置条目的最长保留时间以及最短和最长长度。
- [`clipse`](https://github.com/savedra1/clipse) - 通过 `wl-clipboard` 在 Wayland 下工作，支持文本和图像。
  它提供终端用户界面（TUI），可在 Hyprland 配置中设置为在浮动窗口中打开。
  功能包括自定义主题、图像和文本预览、多选、条目置顶、自动粘贴和敏感内容处理等。
- [`copyq`](https://github.com/hluk/CopyQ) - 支持文本、图像及多种其他格式。
  它支持搜索历史记录和编辑条目，并提供脚本接口。
  你还可以用标签页整理条目，在不同设备之间同步剪贴板。
- [`wl-clip-persist`](https://github.com/Linus789/wl-clip-persist) - 在 Wayland 下复制内容后，数据会一直保留在剪贴板中，直到提供该内容的应用关闭。
  随后，数据便会消失，无法再粘贴。
  使用 `wl-clip-persist` 可以解决这个问题，让数据在应用关闭后仍保留在剪贴板中。
- [`cursor-clip`](https://github.com/Sirulex/cursor-clip) - 一款使用 Rust、GTK4、Libadwaita 和 Layer Shell 构建的现代 Wayland 剪贴板管理器，让剪贴板操作更可靠。
  它的剪贴板历史界面采用 Windows 11 风格和 GNOME 原生设计，每次都会显示在鼠标指针所在位置。
  它支持所有剪贴板格式，包括文本、图像和文件。

<a id="cliphist"></a>

## cliphist

首先，将以下自启动项添加到配置中：

- `wl-paste --type text --watch cliphist store`
- `wl-paste --type image --watch cliphist store`

你可以根据需要禁用其中任意一行。

要将 `cliphist` 绑定到快捷键，并使用 `rofi`、`dmenu`、`wofi` 或 `fuzzel` 显示剪贴板历史记录，可以编辑 `hyprland.lua`。

Bash 命令如下：





<details><summary>rofi</summary>

```sh
cliphist list | rofi -dmenu -display-columns 2 | cliphist decode | wl-copy
```


</details>


<details><summary>dmenu</summary>

```sh
cliphist list | dmenu | cliphist decode | wl-copy
```


</details>


<details><summary>wofi</summary>

```sh
cliphist list | wofi --dmenu --pre-display-cmd "echo '%s' | cut -f 2" | cliphist decode | wl-copy
```


</details>


<details><summary>fuzzel</summary>

```sh
cliphist list | fuzzel --dmenu --with-nth 2 | cliphist decode | wl-copy
```


</details>




以上键位绑定可让你按 `SUPER + V` 打开剪贴板历史记录。
更多信息请参阅上方链接中的项目 GitHub 仓库。

<a id="clipman"></a>

## clipman

首先，将以下命令添加到自启动项中：`wl-paste -t text --watch clipman store --no-persist`

如果要用它管理主选区，请改用：`wl-paste -p -t text --watch clipman store -P --histpath="~/.local/share/clipman-primary.json"`

请确保已创建 `~/.local/share/clipman-primary.json` 文件。

现在可以按以下方式为 `clipman` 设置键位绑定：





<details><summary>rofi</summary>

```lua
hl.bind("SUPER + V", hl.dsp.exec_cmd("clipman pick -t rofi))
```


</details>


<details><summary>dmenu</summary>

```lua
hl.bind("SUPER + V", hl.dsp.exec_cmd("clipman pick -t dmenu"))
```


</details>


<details><summary>wofi</summary>

```lua
hl.bind("SUPER + V", hl.dsp.exec_cmd("clipman pick -t wofi"))
```


</details>


<details><summary>fuzzel</summary>

```lua
hl.bind("SUPER + V", hl.dsp.exec_cmd("clipman pick -t STDOUT | fuzzel --dmenu | wl-copy"))
```


</details>




其他启动器也可依此类推。
更多信息请参阅上方链接中的项目 GitHub 仓库。

<a id="clipvault"></a>

## clipvault

首先，将以下自启动项添加到 `~/.config/hypr/hyprland.lua` 中：

```console
$ wl-paste --watch clipvault store              # 存储文本、图像及其他任意二进制数据
$ wl-paste --type text --watch clipvault store  # 仅存储文本数据
$ wl-paste --type image --watch clipvault store # 仅存储图像数据
$ wl-paste --watch clipvault store --min-entry-length 2 --max-entries 200 --max-entry-age 2d # 使用额外参数存储任意类型的数据
```

你可以根据需要取消上述任意一行的注释。
更多信息请参阅上方链接中的项目 GitHub 仓库，查看其中的设置说明。

要将 `clipvault` 绑定到快捷键，并使用你选择的工具（如 `rofi`、`dmenu` 或 `wofi`）显示剪贴板历史记录，可以在 `hyprland.lua` 中为以下命令之一设置键位绑定：





<details><summary>rofi</summary>

```sh
clipvault list | rofi -dmenu -display-columns 2 | clipvault get | wl-copy
```


</details>


<details><summary>dmenu</summary>

```sh
clipvault list | dmenu | clipvault get | wl-copy
```


</details>


<details><summary>wofi</summary>

```sh
clipvault list | wofi -S dmenu --pre-display-cmd "echo '%s' | cut -f 2" | clipvault get | wl-copy
```


</details>


<details><summary>fuzzel</summary>

```sh
clipvault list | fuzzel --dmenu --with-nth 2 | clipvault get | wl-copy
```


</details>


<details><summary>tofi</summary>

```sh
clipvault list | tofi | clipvault get | wl-copy
```


</details>




以上键位绑定可让你按 `SUPER + V` 打开剪贴板历史记录。
更多信息请参阅上方链接中的项目 GitHub 仓库。

<a id="clipse"></a>

## clipse

首先，将以下命令添加到自启动项中：`clipse -listen`

你可以像这样设置键位绑定，方便地打开终端用户界面：

```lua
hl.bind("SUPER + V", hl.dsp.exec_cmd("kitty --class clipse -e clipse", { float = true, size = {622, 652}, stay_focused = true }))
```

推荐使用 `kitty` 终端模拟器，因为它的图像渲染兼容性最好。你也可以换用自己喜欢的其他终端。

窗口类名是可选的。建议使用浮动窗口，让操作体验更接近传统图形界面。

有关 `clipse` 的更多详情，请参阅本页顶部链接中的项目 GitHub 仓库。

<a id="copyq"></a>

## copyq

首先，将以下命令添加到自启动项中：`copyq --start-server`

如果 `copyq` 主窗口无法正常关闭或隐藏，请尝试在“首选项”对话框的“布局”选项卡中启用“隐藏主窗口”选项。

<a id="wl-clip-persist"></a>

## wl-clip-persist

将以下命令添加到自启动项中。
无需其他更改。
这样，即使关闭了复制内容时使用的源窗口，仍可通过 Wayland 的基本复制粘贴机制粘贴该内容。

```sh
wl-clip-persist --clipboard regular
```

此方法也适用于主选区（即单击鼠标中键粘贴选中内容），但不建议这样做，因为对主选区使用此方法[会给某些 GTK 应用带来意外的副作用](https://github.com/Linus789/wl-clip-persist#primary-selection-mode-breaks-the-selection-system-3)。

```sh
wl-clip-persist --clipboard primary
```

<a id="cursor-clip"></a>

## cursor-clip

首先，将以下命令添加到自启动项中：`cursor-clip --daemon`

这会启动后台守护进程，监视剪贴板的变化。

要通过快捷键快速打开 `cursor-clip`，可以在 Hyprland 配置中添加一个运行 `cursor-clip` 的键位绑定。

触发快捷键后，`cursor-clip` 会自动在鼠标指针所在位置显示悬浮窗口，提供 Windows 11 风格的剪贴板历史界面。
该窗口使用 GTK4 和 Libadwaita 实现 GNOME 原生设计，支持所有剪贴板格式，包括文本、图像和文件。

更多信息请参阅本页顶部链接中的项目 GitHub 仓库。
