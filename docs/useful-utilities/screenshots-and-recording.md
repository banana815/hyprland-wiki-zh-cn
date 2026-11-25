# 截图与录屏

本页列出了在 Hyprland 上截图和录屏的常用工具。

<a id="screenshot-utilities"></a>

## 截图工具

<a id="grim-and-swappy"></a>

### Grim 和 swappy

[Grim](https://gitlab.freedesktop.org/emersion/grim) 是一款简单的 Wayland 截图工具。
它通常与 [`slurp`](https://github.com/emersion/slurp) 和 [`swappy`](https://github.com/jtheoof/swappy) 搭配使用，前者用于选择截图区域，后者用于标注截图。


<details><summary>示例</summary>


```lua
-- 选取一块屏幕区域并在 swappy 中打开其截图：
hl.bind("Print", hl.dsp.exec_cmd('grim -g "$(slurp)" - | swappy -f -'))

-- 要将所选区域的截图直接复制到剪贴板，请安装 wl-clipboard 并使用以下命令：
hl.bind("SUPER + Print", hl.dsp.exec_cmd('grim -g "$(slurp -d)" - | wl-copy'))
```



</details>

<a id="satty"></a>

### Satty

[Satty](https://github.com/Satty-org/Satty) 是一款功能强大的现代截图标注工具，设计灵感来自 [`swappy`](https://github.com/jtheoof/swappy) 和 [Flameshot](https://github.com/flameshot-org/flameshot)。
它旨在改进现有截图工具，几乎无需调整即可替代 `swappy`。

例如，以下命令会截图并用 `satty` 打开，同时显式配置复制到剪贴板和保存到文件的操作：

```lua
hl.bind("Print", hl.dsp.exec_cmd('grim - | satty -f - --copy-command wl-copy -o "~/Pictures/Screenshots/%Y%m%d_%H%M%S.png"'))
```

<a id="waytator"></a>

### Waytator

[Waytator](https://github.com/faetalize/waytator) 是一款用 C 编写的截图标注工具，也可用作轻量级图像编辑器。

```lua
hl.bind("Print", hl.dsp.exec_cmd("grim -t ppm - | waytator"))
```

<a id="flameshot"></a>

### Flameshot

[Flameshot](https://github.com/flameshot-org/flameshot) 是一款内置标注界面的截图工具。
在 Wayland 上，它依赖桌面门户来截取屏幕。
如果无法截图，请确认桌面门户配置正常，也可以改用 `grim` 搭配 `swappy`。

<a id="hyprcapture"></a>

### HyprCapture

[HyprCapture](https://github.com/gfhdhytghd/HyprCapture) 是一款面向 Hyprland 的截图和录屏工具。
如果你希望截图和录屏流程与 Hyprland 集成，又不想自行组合多个小工具，可以使用 HyprCapture。

<a id="wechat-screenshot"></a>

### 微信截图

微信自带截图快捷键。
如果 Hyprland 先截获了这个键位绑定，就需要将按键显式转发给微信窗口，微信才能收到。

使用 `pass` 调度器将 `ALT + A` 转发给微信：

```lua
hl.bind("ALT + A", hl.dsp.pass({ class = "wechat" }))
```

<a id="recording-utilities"></a>

## 录屏工具

如果 Hyprland 的权限系统阻止了屏幕捕获工具，请参见[权限](../configuring/core/advanced-configuration/permissions.md)。

<a id="obs-studio"></a>

### OBS Studio

[OBS Studio](https://obsproject.com/) 可以通过 PipeWire 和桌面门户录制屏幕。
请确保已安装 `pipewire`、`wireplumber`、[`xdg-desktop-portal-hyprland`](../hypr-ecosystem/user/xdg-desktop-portal-hyprland.md) 和 `qt6-wayland`。
有关桌面门户的配置说明，请参见[屏幕共享](screen-sharing.md)。

<a id="wf-recorder"></a>

### wf-recorder

[wf-recorder](https://github.com/ammen99/wf-recorder) 是一款轻量级 Wayland 录屏工具。


<details><summary>示例</summary>


```sh
# 录制整个屏幕：
wf-recorder -f ~/Videos/recording.mp4

# 录制所选区域：
wf-recorder -g "$(slurp)" -f ~/Videos/recording.mp4
```



</details>

<a id="wl-screenrec"></a>

### wl-screenrec

[wl-screenrec](https://github.com/russelltg/wl-screenrec) 是一款用于 wlroots 的高性能录屏工具，支持硬件编码。


<details><summary>示例</summary>


```sh
# 录制整个屏幕：
wl-screenrec -f ~/Videos/recording.mp4

# 录制所选区域：
wl-screenrec -g "$(slurp)" -f ~/Videos/recording.mp4

```


</details>

<a id="gpu-screen-recorder"></a>

### GPU Screen Recorder

[GPU Screen Recorder](https://git.dec05eba.com/gpu-screen-recorder/about/) 是一款仅使用 GPU 录制显示器画面的录屏工具，对系统性能的影响很小，类似于 Windows 上的 ShadowPlay。

```sh
# 以 60 FPS 录制整个屏幕，同时录制音频：
gpu-screen-recorder -w screen -f 60 -a default_output -o ~/Videos/recording.mp4
```
