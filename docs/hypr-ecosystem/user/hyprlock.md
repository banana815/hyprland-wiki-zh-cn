# hyprlock

[hyprlock](https://github.com/hyprwm/hyprlock) 是一款适用于 Hyprland 的锁屏程序，简洁快速，支持多线程和 GPU 加速。

> [!WARNING]
> 如果在所有搜索路径中都找不到配置文件，hyprlock **会报错退出**，会话也不会锁定。
>
> 可以使用[示例配置](https://github.com/hyprwm/hyprlock/blob/main/assets/example.conf)快速上手。

<a id="command-line-arguments"></a>

## 命令行参数

另见 `hyprlock --help`。

| 参数 | 说明 |
| --- | --- |
| `-v`/`--verbose` | 启用详细日志 |
| `-q`/`--quiet` | 禁用日志 |
| `-c`/`--config` FILE | 指定要使用的配置文件 |
| `--display` NAME | 指定要连接的 Wayland 显示器 |
| `--grace` SECONDS | 设置要求身份验证前的宽限期，单位为秒 |
| `--immediate-render` | 立即绘制背景，无需等待资源就绪（与 `general:immediate_render` 相同） |
| `--no-fade-in` | 禁用锁屏界面出现时的淡入动画 |
| `-V`/`--version` | 显示版本信息并退出 |
| `-h`/`--help` | 显示帮助并退出 |

<a id="configuration"></a>

## 配置

hyprlock 通过名为 `hyprlock.conf` 的配置文件进行配置。
hyprlock 会依次在以下位置查找该文件：

1. `$XDG_CONFIG_HOME/hypr/hyprlock.conf`
1. `$HOME/.config/hypr/hyprlock.conf`
1. `$XDG_CONFIG_DIRS` 中的每个目录（例如 `<dir>/hypr/hyprlock.conf`）
1. `/etc/xdg/hypr/hyprlock.conf`

hyprlock 使用找到的第一个配置文件。
也可以用 `hyprlock --config <path>` 直接指定路径。

<a id="variable-types"></a>

### 变量类型

除了 Hyprland 的[数据类型](../../configuring/naming-conventions.md#data-types)，hyprlock 还支持以下类型。

| 类型 | 说明 |
| --- | --- |
| layoutxy | 带有可选 `%` 后缀的 vec2，可按输出尺寸的百分比指定大小。支持浮点数（例如 10.5），但只有使用 `%` 时才会保留小数部分。直接指定的像素值会四舍五入为整数 |

<a id="general"></a>

### 常规设置

`general` 类别中的变量如下：

| 变量 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| `compositor_fade` | 由合成器控制不透明度，使锁屏表面的内容与合成器的模糊效果一起平滑淡入淡出 | bool | `false` |
| `disable_screencopy` | 禁止为应用背景效果而复制屏幕内容。使用半透明背景并启用 Hyprland 的 `misc:session_lock_xray` 时，此选项很有用 | bool | `false` |
| `fail_timeout` | 身份验证失败后，界面恢复初始状态前的等待时间，单位为毫秒 | int | `2000` |
| `fractional_scaling` | 是否使用分数缩放。`0` 表示禁用，`1` 表示启用，`2` 表示自动 | int | `2` |
| `hide_cursor` | 隐藏光标 | bool | `false` |
| `ignore_empty_input` | 未输入密码时跳过验证 | bool | `false` |
| `immediate_render` | 让 hyprlock 立即开始绘制组件。在 `background:path` 指定的资源就绪前，背景显示为 `background:color` 指定的颜色 | bool | `false` |
| `screencopy_mode` | 选择屏幕复制模式。`0` 表示使用 GPU 加速，`1` 表示使用 CPU（较慢） | int | `0` |
| `text_trim` | 是否去除文本首尾的空白字符，可用于去除命令输出末尾的换行符 | bool | `true` |

<a id="compositor-fade-and-live-background"></a>

#### 合成器淡入淡出与实时背景

启用 `general:compositor_fade` 后，锁屏表面的内容与合成器的模糊效果会使用现有的 [`fadeIn` 和 `fadeOut` 动画](#animations)一起淡入淡出。
动画改变的是合成器模糊效果在画面中所占的比重，**而非模糊半径本身**。
如果合成器未声明支持 `hyprland_surface_manager_v1` Wayland 协议，hyprlock 会自动回退到标准的客户端淡入淡出效果。

要将实时模糊的桌面用作背景，请在 Hyprland 的 `hyprland.lua` 中启用 `misc:session_lock_xray` 和 `misc:session_lock_blur`：

```lua
hl.config({
    misc = {
        session_lock_xray = true,
        session_lock_blur = true,
    },
})
```

在 `hyprlock.conf` 中使用透明[背景](#background)，并将 `path` 留空：

```ini
general {
    compositor_fade = true
}

background {
    monitor =
    path =
    color = rgba(0, 0, 0, 0.0)
}

animations {
    enabled = true
    bezier = linear, 1, 1, 0, 0
    animation = fadeIn, 1, 5, linear
    animation = fadeOut, 1, 5, linear
}
```

这样配置后，锁屏界面后方的桌面会持续实时更新。
如果显式设置 `background:path = screenshot`，即使启用了 `compositor_fade`，hyprlock 仍会在启动时截取静态图像作为背景，而不会显示实时桌面。

<a id="authentication"></a>

### 身份验证

`auth` 类别中的变量如下：

| 变量 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| `pam:enabled` | 是否启用 PAM 身份验证 | bool | `true` |
| `pam:module` | 设置用于身份验证的 PAM 模块。如果在 `/etc/pam.d` 中找不到该模块，则使用 "su" 作为后备模块 | string | `hyprlock` |
| `fingerprint:enabled` | 启用 fprintd 指纹验证，使其可与其他验证方式并行运行 | bool | `false` |
| `fingerprint:ready_message` | 设置 fprintd 准备好扫描指纹时显示的消息 | string | `(Scan fingerprint to unlock)` |
| `fingerprint:present_message` | 设置手指放到扫描器上时显示的消息 | string | `Scanning fingerprint` |
| `fingerprint:retry_delay` | 设置扫描到无法识别的指纹后，到可以再次扫描指纹前的等待时间，单位为毫秒 | int | `250` |

> [!NOTE]
> 必须至少启用一种身份验证方式。

<a id="animations"></a>

### 动画

`animations` 类别中的变量如下：

| 变量 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| enabled | 是否启用动画 | bool | `true` |

<a id="keywords"></a>

#### 关键字

可以使用 `animation` 和 `bezier` 两个关键字。

例如：

```ini
bezier = linear, 1, 1, 0, 0
animation = fade, 1, 1.8, linear
```

可用动画见[动画树](#animation-tree)。
hyprlock 目前未使用 `animation` 关键字的可选参数 `STYLE`。

更多信息见 Hyprland 的[动画文档](../../configuring/core/animations.md)。

<a id="animation-tree"></a>

#### 动画树

```plain
global
  ↳ fade
    ↳ fadeIn - fade to lock screen
    ↳ fadeOut - fade back to the Wayland session
  ↳ inputField
    ↳ inputFieldColors - fade between colors and gradients
    ↳ inputFieldFade - fade_on_empty animation
    ↳ inputFieldWidth - adaptive width animation
    ↳ inputFieldDots - fade in/out for individual dots in the input field
```

<a id="system-configuration"></a>

### 系统配置

在 Arch Linux 上，hyprlock 默认通过 `pam_faillock.so` 与 [pambase](https://archlinux.org/packages/?name=pambase) 集成，解锁失败 3 次后必须等待 10 分钟才能重试。
如需更改此行为，请参阅 [Arch Linux Wiki](https://wiki.archlinux.org/title/Security#Lock_out_user_after_three_failed_login_attempts)，按需修改 `/etc/security/faillock.conf` 文件中的 `unlock_time`、`fail_interval` 和 `deny` 参数。

<a id="keyboard-shortcuts-and-actions"></a>

## 键盘快捷键与操作

下表列出了 hyprlock 中各按键及组合键的默认操作：

| 输入 | 说明 |
| --- | --- |
| `ESC` | 清空密码缓冲区 |
| `Ctrl + u` | 清空密码缓冲区 |
| `Ctrl + Backspace` | 清空密码缓冲区 |

使用 [`locked` 标志](../../configuring/core/binds/flags.md#bind-flags)可以让指定的 Hyprland 键位绑定在 hyprlock 锁屏期间仍然生效，例如用于调节亮度、音量或控制媒体播放的键位绑定。

<a id="widgets"></a>

## 组件

hyprlock 的外观完全通过组件配置。

```ini
widget_name {
    monitor =
    # 更多选项
}
```

<a id="monitor-selection"></a>

### 选择显示器

所有组件都支持 `monitor` 选项，留空表示“所有显示器”。

该选项使用与 Hyprland 配置中相同的字符串来指定显示器。
可以使用端口名称（例如 `eDP-1`），也可以使用显示器描述（例如 `desc:Chimei Innolux Corporation 0x150C`）。

参见[显示器](../../configuring/core/monitors/_index.md)。

<a id="variable-substitution"></a>

### 变量替换

组件的文本选项中可以使用以下变量，显示时会替换为对应的值。

- `$USER` - 用户名（例如 `linux-user`）
- `$DESC` - 用户描述（例如 `Linux User`）
- `$TIME` - 24 小时制的当前时间（例如 `13:37`）
- `$TIME12` - 12 小时制的当前时间（例如 `1:37 PM`）
- `$LAYOUT` - 当前键盘布局
- `$ATTEMPTS` - 身份验证失败次数
- `$FAIL` - 上一次身份验证失败的原因
- `$PAMPROMPT` - PAM 身份验证的最近一条提示
- `$PAMFAIL` - 上一次 PAM 身份验证失败的原因
- `$FPRINTPROMPT` - 指纹验证的最近一条提示
- `$FPRINTFAIL` - 上一次指纹验证失败的原因

<a id="widget-list"></a>

## 组件列表

<a id="general-remarks"></a>

### 通用说明

- 所有渲染的文本都支持 [Pango 标记语言](https://docs.gtk.org/Pango/pango_markup.html)。
  - 为方便使用，hyprlock 还会解析 `<br>`（换行符）。
    记得在 span 标签中设置 `allow_breaks="true"` 以允许换行。
- 使用 halign、valign、position 和 zindex 控制组件的位置和层叠顺序。
  position 指定相对于对齐后位置的偏移量。
  - halign：`left`、`center`、`right`、`none`。
  - valign：`top`、`center`、`bottom`、`none`。
  - zindex：数值较大的组件会显示在数值较小的组件上方。
    除 background 默认为 -1 外，所有组件的默认值均为 0。
- 所有 `position` 和 `size` 选项都可以使用像素值，也可以使用相对于输出尺寸的百分比。
  - 像素：`10, 10` 或 `10px, 10px`
  - 百分比：`10%, 10.5%`
  - 混合使用：`10%, 5px`
- 支持 png、jpg 和 webp 图像格式（不支持动画）。

<a id="shadowable"></a>

### 阴影

部分组件可以显示阴影。
这些组件支持以下选项：

| 变量 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| `shadow_passes` | 阴影渲染次数，设为 0 可禁用阴影 | int | `0` |
| `shadow_size` | 阴影大小 | int | `3` |
| `shadow_color` | 阴影颜色 | color | `rgb(0,0,0)` |
| `shadow_boost` | 阴影不透明度的增强系数 | float | `1.2` |

<a id="clickable"></a>

### 点击操作

部分组件支持点击，包括 `label`、`image` 和 `shape`。

在组件内配置以下选项，即可在点击该组件时运行任意命令：

| 变量 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| `onclick` | 点击时运行的命令 | string | [[Empty]] |

<a id="background"></a>

### 背景

绘制背景图像或用颜色填充背景。

如果 `path` 为空或未设置，则使用 `color` 填充背景，否则使用图像。
如果 `path` 为 `screenshot`，则使用 hyprlock 启动时截取的桌面画面。

| 变量 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| `monitor` | 绘制背景的目标显示器 | string | [[Empty]] |
| `path` | 图像路径，也可设为 `screenshot`，留空则使用 `color` 填充 | string | [[Empty]] |
| `color` | 备用背景色 | color | `rgba(17, 17, 17, 1.0)` |
| `blur_passes` | 模糊处理次数，设为 `0` 可禁用模糊 | int | `0` |
| `blur_size` | 模糊范围（距离） | int | `7` |
| `noise` | 添加的噪点强度 | float | `0.0117` |
| `contrast` | 模糊处理的对比度调节系数 | float | `0.8916` |
| `brightness` | 模糊处理的亮度调节系数 | float | `0.8172` |
| `vibrancy` | 模糊后颜色的饱和度提升幅度 | float | `0.1696` |
| `vibrancy_darkness` | vibrancy 对暗部的影响强度 | float | `0.05` |
| `reload_time` | 重新加载的间隔（秒）。设为 `0` 时，收到 `SIGUSR2` 后重新加载。`path` 为 `screenshot` 时忽略此项 | int | `-1` |
| `reload_cmd` | 用于获取新路径的命令。留空则沿用原路径 | string | [[Empty]] |
| `crossfade_time` | 重新加载时新旧背景交叉淡化的时长（秒）。负值表示禁用交叉淡化 | float | `-1.0` |
| `zindex` | 组件的层叠顺序 | int | `-1` |

> [!NOTE]
> 模糊选项沿用 Hyprland 的设置项。
> 参见[模糊](../../configuring/core/config-options.md#blur)。


<details><summary>背景示例</summary>


```ini
background {
    monitor =
    path = screenshot
    color = rgba(25, 20, 20, 1.0)
    blur_passes = 2
}
```



</details>

<a id="image"></a>

### 图像

&check; 支持阴影  
&check; 支持点击

绘制图像。

如果 `path` 为空或未设置，则不显示任何内容。

| 变量 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| `monitor` | 绘制图像的目标显示器 | string | [[Empty]] |
| `path` | 图像路径 | string | [[Empty]] |
| `size` | 缩放后图像短边的长度 | int | `150` |
| `rounding` | 圆角半径，设为负值时呈圆形 | int | `-1` |
| `border_size` | 边框宽度 | int | `4` |
| `border_color` | 边框颜色 | gradient | `rgba(221, 221, 221, 1.0)` |
| `rotate` | 逆时针旋转角度（度） | int | `0` |
| `reload_time` | 重新加载的间隔（秒）。设为 `0` 时，收到 `SIGUSR2` 后重新加载 | int | `-1` |
| `reload_cmd` | 用于获取新路径的命令。留空则沿用原路径。不要运行 `tail -F` 这类持续跟踪变化的命令 | string | [[Empty]] |
| `position` | 图像位置 | layoutxy | `0, 0` |
| `halign` | 水平对齐方式 | string | `center` |
| `valign` | 垂直对齐方式 | string | `center` |
| `zindex` | 组件的层叠顺序 | int | `0` |


<details><summary>图像示例</summary>


```ini
image {
    monitor =
    path = /home/me/cutie.png
    size = 150
    rounding = 0 # 无圆角

    position = 0, 200
    halign = center
    valign = center
}
```



</details>

<a id="shape"></a>

### 形状

&check; 支持阴影  
&check; 支持点击

绘制形状。

| 变量 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| `monitor` | 绘制形状的目标显示器 | string | [[Empty]] |
| `size` | 形状尺寸 | layoutxy | 100, 100 |
| `color` | 形状颜色 | color | `rgba(17, 17, 17, 1.0)` |
| `rounding` | 圆角半径，设为负值时呈圆形 | int | `-1` |
| `rotate` | 逆时针旋转角度（度） | int | `0` |
| `border_size` | 边框宽度 | int | `0` |
| `border_color` | 边框颜色 | gradient | `rgba(0, 207, 230, 1.0)` |
| `xray` | 设为 `true` 时，在背景上挖出一个指定尺寸的矩形孔洞，孔洞不会旋转 | bool | `false` |
| `position` | 形状位置 | layoutxy | `0, 0` |
| `halign` | 水平对齐方式 | string | `center` |
| `valign` | 垂直对齐方式 | string | `center` |
| `zindex` | 组件的层叠顺序 | int | `0` |


<details><summary>形状示例</summary>


```ini
shape {
    monitor =
    size = 360, 60
    color = rgba(0, 0, 0, 0.0) # 无填充
    rounding = -1 # 圆形
    border_size = 4
    border_color = rgba(0, 207, 230, 1.0)

    position = 0, 80
    halign = center
    valign = center
}
```



</details>

<a id="input-field"></a>

### 输入框

&check; 支持阴影

绘制密码输入框。

| 变量 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| `monitor` | 绘制输入框的目标显示器 | string | [[Empty]] |
| `size` | 输入框大小 | layoutxy | `400, 90` |
| `outline_thickness` | 边框粗细 | int | `4` |
| `dots_size` | 圆点大小，范围为 [0.001 - 0.8] | float | `0.25` |
| `dots_spacing` | 圆点间距，范围为 [-1.0 - 1.0] | float | `0.15` |
| `dots_center` | 是否将圆点居中。关闭时左对齐 | bool | `true` |
| `dots_rounding` | 圆点的圆角半径 | int | `-1` |
| `dots_text_format` | 用作输入指示符的一个或多个字符。默认使用圆角矩形 | string | [[Empty]] |
| `outer_color` | 边框颜色 | gradient | `rgba(17, 17, 17, 1.0)` |
| `inner_color` | 输入框的填充色 | color | `rgba(200, 200, 200, 1.0)` |
| `font_color` | 字体颜色 | color | `rgba(10, 10, 10, 1.0)` |
| `font_family` | 字体族 | string | `Noto Sans` |
| `fade_on_empty` | 输入框为空时将其淡出 | bool | `true` |
| `fade_timeout` | 触发 `fade_on_empty` 前的等待时间，单位为毫秒 | int | `2000` |
| `placeholder_text` | 输入框为空时显示的文本 | string | `<i>Input Password...</i>` |
| `hide_input` | 设为 `true` 时，以类似 swaylock 的输入指示符代替圆点 | bool | `false` |
| `hide_input_base_color` | 在 Oklab 色彩空间中随机旋转此颜色的色相，生成 `hide_input` 使用的颜色 | color | `rgba(153, 170, 187)` |
| `rounding` | `-1` 表示使用最大圆角，呈圆形或椭圆形 | int | `-1` |
| `check_color` | 等待认证结果时的强调色 | gradient | `rgba(204, 136, 34, 1.0)` |
| `check_text` | 等待认证结果时显示的文本 | string | [[Empty]] |
| `fail_color` | 认证失败时的强调色 | gradient | `rgba(204, 34, 34, 1.0)` |
| `fail_text` | 认证失败时显示的文本 | string | `<i>$FAIL <b>($ATTEMPTS)</b></i>` |
| `capslock_color` | Caps Lock 开启时的强调色 | gradient | [[Empty]] |
| `numlock_color` | Num Lock 开启时的强调色 | gradient | [[Empty]] |
| `bothlock_color` | Caps Lock 和 Num Lock 同时开启时的强调色 | gradient | [[Empty]] |
| `invert_numlock` | 在 Num Lock 关闭时改变颜色 | bool | `false` |
| `swap_font_color` | 颜色变化时交换字体颜色和输入框填充色 | bool | `false` |
| `position` | 输入框位置 | layoutxy | `0, 0` |
| `halign` | 水平对齐方式 | string | `center` |
| `valign` | 垂直对齐方式 | string | `center` |
| `zindex` | 控件的堆叠层级（z-index） | int | `0` |

> [!NOTE] **颜色说明**
> 当 `outline_thickness` 设为 `0` 时，颜色变化会作用于输入框的填充色，而非边框颜色。
>
> `swap_font_color` 的行为如下：
> - `outline_thickness` 为 `0` 时：若启用此选项，颜色变化时（如开启 Caps Lock 或校验密码时）会交换字体颜色和输入框填充色。
> - `outline_thickness` 不为 `0` 时：若启用此选项，校验密码和认证失败时会交换字体颜色和输入框填充色。
> - 启用 `swap_font_color` 后，强调色仅使用渐变中指定的第一种颜色。

`placeholder_text` 和 `fail_text` 均支持[变量替换](#variable-substitution)。


<details><summary>输入框示例</summary>


```ini
input-field {
    monitor =
    size = 20%, 5%
    outline_thickness = 3
    inner_color = rgba(0, 0, 0, 0.0) # 无填充

    outer_color = rgba(33ccffee) rgba(00ff99ee) 45deg
    check_color = rgba(00ff99ee) rgba(ff6633ee) 120deg
    fail_color = rgba(ff6633ee) rgba(ff0066ee) 40deg

    font_color = rgb(143, 143, 143)
    fade_on_empty = false
    rounding = 15

    position = 0, -20
    halign = center
    valign = center
}
```


</details>

<a id="label"></a>

### 标签

&check; 支持阴影  
&check; 可点击

绘制一个标签。

| 变量 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| `monitor` | 绘制标签的目标显示器 | string | [[Empty]] |
| `text` | 要显示的文本 | string | `Sample Text` |
| `text_align` | 标签容器内多行文本的对齐方式。center 表示居中，right 表示右对齐，其他值均使用默认的左对齐 | string | `center` |
| `color` | 文本颜色 | color | `rgba(254, 254, 254, 1.0)` |
| `font_size` | 字体大小 | int | `16` |
| `font_family` | 字体族 | string | `Sans` |
| `rotate` | 逆时针旋转角度，单位为度 | int | `0` |
| `position` | 标签位置 | layoutxy | `0, 0` |
| `halign` | 水平对齐方式 | string | `center` |
| `valign` | 垂直对齐方式 | string | `center` |

<a id="dynamic-labels"></a>

#### 动态标签

`text` 选项支持[变量替换](#variable-substitution)，也可以运行 shell 命令。
例如：

```ini
text = cmd[update:1000] echo "<span foreground='##ff2222'>$(date)</span>"
```

> [!NOTE]
> - `update:` 的时间单位为毫秒。
> - 指定 `update:<time>:1` 或 `update:<time>:true` 后，可向 hyprlock 发送 `SIGUSR2` 强制更新标签。此时 `<time>` 可以为 `0`。
> - 使用 `$ATTEMPTS[<string>]` 格式可在尚无认证失败记录时显示 `<string>`。
>   这里支持 Pango 标记。将 `<string>` 留空即可隐藏这段文本。
> - 使用 `$LAYOUT[<string0>,<string1>,...]` 格式可按索引替换各键盘布局的显示文本。
>   可以使用 `hyprland.lua` 中的设置（例如 `$LAYOUT[en,ru,de]`）。
>   单个 `!` 字符可隐藏对应的布局（例如，`$LAYOUT[!]` 会隐藏索引为 0 的默认布局，并显示其他布局）。
> - `$TIME` 和 `$TIME12` 使用 TZ 环境变量指定的时区。
>   若未设置该变量，则使用系统时区；出错时回退到 UTC。
> - 上述变量会在命令运行_之前_解析。
> - **不要**运行永不退出的命令。
>   这会使 `AsyncResourceGatherer` 卡住，给你带来麻烦。


<details><summary>标签示例</summary>


```ini
label {
    monitor =
    text = Hi there, $USER
    color = rgba(200, 200, 200, 1.0)
    font_size = 25
    font_family = Noto Sans

    position = 0, 80
    halign = center
    valign = center
}
```



</details>

<a id="user-signals"></a>

## 用户信号

- `SIGUSR1`：解锁 hyprlock。
  例如，可以切换到另一个 TTY 并运行 `pkill -USR1 hyprlock`。
- `SIGUSR2`：更新标签和图像。
  详见上文。
