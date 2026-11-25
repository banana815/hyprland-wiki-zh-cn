# 使用 hyprctl

`hyprctl` 是一个实用工具，可通过命令行或脚本控制合成器的部分功能。它会随 Hyprland 自动安装。

> [!WARNING]
> 合成器会 _同步_ 处理 `hyprctl` 调用，因此短时间内大量调用该工具会导致运行变慢。建议在执行大量控制操作时使用 `--batch`，并限制信息查询的次数。
>
> 有关实时事件处理，请参阅[事件](events.md)。

<a id="commands"></a>

## 命令

<a id="eval"></a>

### eval

提交一段 Lua 代码字符串以动态执行。成功时返回 "ok"，出错时返回引发的错误。

```sh
hyprctl eval 'hl.dispatch(hl.dsp.focus({ workspace = "3" }))'
```

<a id="repl"></a>

### repl

启动交互式 Lua REPL 会话，或提交一段 Lua 代码字符串，并通过 `tostring()` 打印结果。其用法与 `lua` 的交互模式类似。按 Ctrl+D 退出。

用法：

```sh
hyprctl repl        # 启动 REPL 会话
hyprctl repl [code] # 执行代码并打印结果
```

示例：

```sh
$ hyprctl repl 'hl.get_active_window().class'
foot

$ hyprctl repl
> for i,w in pairs(hl.get_windows()) do print(i, w.class) end
1       foot
2       firefox
3       codium
> hl.notification.create({ text = "Hello World", timeout = 2000})
HL.Notification(0x563c0a1ebe70)
```

<a id="dispatch"></a>

### dispatch

dispatch 是 `eval 'hl.dispatch(...)'` 的简写：

```sh
hyprctl dispatch 'hl.dsp.focus({ workspace = "3" })'
```

调度器列表请参阅[调度器](../dispatchers.md)。

<a id="reload"></a>

### reload

执行 `reload` 可强制重载配置。`reload full-reset` 会重新创建整个配置上下文，允许在 Lua 和 hyprlang 之间切换。仅在确有必要时才应使用 `full-reset`。

<a id="kill"></a>

### kill

执行 `kill` 可进入终止模式，在该模式下单击应用即可将其终止。按 ESCAPE 可退出此模式。

用法有点像 `xkill`。

<a id="setcursor"></a>

### setcursor

设置光标主题并重新加载光标管理器。主题设置对 GTK 以外的所有应用都生效，因为 GTK 就是这样。

请注意，从 0.37.0 版起，此命令仅接受 hyprcursor 主题。对于旧式 XCursor 主题，请使用 `XCURSOR_THEME` 和 `XCURSOR_SIZE` 环境变量。

参数：主题和大小

例如：

```sh
hyprctl setcursor Bibata-Modern-Classic 24
```

<a id="output"></a>

### output

允许你在所选后端上添加和移除虚拟输出。

用法：

```sh
hyprctl output create [backend] (name)
# 或者
hyprctl output remove [name]
```

其中，`[backend]` 是后端名称，`(name)` 是可选的输出名称。如果未指定 `(name)`，则使用默认命名方案（如 `HEADLESS-2`、`WL-1` 等）。

> [!NOTE]
> `create` 和 `remove` 也可以分别写作 `add` 和 `destroy`。

可用的后端如下：

- `wayland`：创建一个以 Wayland 窗口形式呈现的输出。仅当 Hyprland 已使用 Wayland 后端运行（即作为嵌套会话运行）时才有效。
- `headless`：创建一个无头显示器输出。如果你正在运行 VNC、RDP 或 Sunshine 服务器，应使用此后端。
- `auto`：自动选择后端。例如，如果你从 TTY 启动 Hyprland，就会选用 `headless`。

例如，要创建名为 "test" 的无头输出：

```sh
hyprctl output create headless test
```

要移除该输出：

```sh
hyprctl output remove test
```

<a id="switchxkblayout"></a>

### switchxkblayout

设置键盘的 XKB 布局索引。

例如，如果你进行了如下设置：

```lua
hl.device({
  name = "my-epic-keyboard-v1",
  kb_layout = "us,pl,de"
})
```

就可以使用此命令在这些布局之间切换。

```sh
hyprctl switchxkblayout <DEVICE> <CMD>
```

其中，`CMD` 可以是 `next`（下一个布局）、`prev`（上一个布局）或 `ID`（指定布局的索引，上例中 `us` 为 0，`pl` 为 1，`de` 为 2）。可以使用 `hyprctl devices` 命令查找 `DEVICE`。

`DEVICE` 也可以是 `current` 或 `all`，分别表示当前键盘或所有键盘。当前键盘是 `devices` 中标记为 `main` 的键盘。

适用于常见键盘的命令示例：

```sh
hyprctl switchxkblayout at-translated-set-2-keyboard next
```

> [!NOTE]
> 如果只想为一个布局指定变体（例如，一个布局使用 pl/dvorak，另一个使用 us/qwerty），相应的 XKB 参数仍可留空，但各组逗号分隔的参数数量必须一致。也可以只指定一个参数，让它对这三个布局都生效。
>
> ```lua
> hl.config({
>   input = {
>     kb_layout = "pl,us,ru",
>      kb_variant = "dvorak,,",
>      kb_options = "caps:ctrl_modifier"
>   }
> })
> ```

<a id="seterror"></a>

### seterror

设置 hyprctl 的错误消息字符串。重新加载 Hyprland 配置时，该字符串会重置。

```sh
hyprctl seterror 'rgba(66ee66ff)' hello world this is my problem
```

要禁用错误消息：

```sh
hyprctl seterror disable
```

<a id="getprop"></a>

### getprop

获取窗口某个属性的值。

```sh
hyprctl getprop <window> <property>
```

其中，`window` 的含义见[窗口参数说明](../dispatchers.md#parameter-explanation)，`property` 可以是任何可通过 [set_prop](../dispatchers.md#set_prop) 设置的属性。

请注意：

- 如果未设置 `animationstyle`，则返回 `(unset)`。
- `min_size` 的默认值为 `20 20`。
- `max_size` 的默认值为 `inf inf`，在 JSON 中表示为 `[null,null]`。

<a id="notify"></a>

### notify

通过 Hyprland 内置的通知系统发送通知。更多信息请参阅[通知文档](notifications.md)，尤其是其中关于图标和颜色选项的说明。

```sh
hyprctl notify <ICON> <TIME_MS> <COLOR> <MESSAGE>
```

要指定字号，请添加 `fonstsize:<SIZE = int>`。


<details><summary>示例</summary>


```sh
hyprctl notify -1 10000 "rgb(ff1ea3)" "Hello everyone!"
hyprctl notify -1 10000 "rgb(ff0000)" "fontsize:35 This text is big"
```

<a id="dismissnotify"></a>

### dismissnotify

关闭全部通知，或最多关闭 AMOUNT 条通知。

```sh
hyprctl dismissnotify    # 关闭所有通知
hyprctl dismissnotify -1 # 关闭所有通知（与不传参数相同）
hyprctl dismissnotify 2  # 关闭最早的两条通知
```



</details>

<a id="usage"></a>

## 用法

```plain
version              - prints the Hyprland version along with flags, commit and branch of build.
monitors             - lists active outputs with their properties, 'monitors all' lists active and inactive outputs
workspaces           - lists all workspaces with their properties
activeworkspace      - gets the active workspace and its properties
workspacerules       - gets the list of defined workspace rules
clients              - lists all windows with their properties
devices              - lists all connected keyboards and mice
decorations [window] - lists all decorations and their info
binds                - lists all registered binds
activewindow         - gets the active window name and its properties
layers               - lists all the layers
splash               - prints the current random splash
getoption [option]   - gets the config option status (values)
cursorpos            - gets the current cursor position in global layout coordinates
animations           - gets the currently configured info about animations and beziers
instances            - lists all running instances of Hyprland with their info
layouts              - lists all layouts available (including from plugins)
configerrors         - lists all current config parsing errors
rollinglog           - prints tail of the log. Also supports -f/--follow option
locked               - prints whether the current session is locked.
descriptions         - returns a JSON with all config options, their descriptions and types.
submap               - prints the current submap the keybinds are in
```

使用 `getoption` 命令时，选项名称应写成 `section.option` 的形式，例如：

```sh
hyprctl getoption general.border_size

# 对于嵌套配置段：
hyprctl getoption input.touchpad.disable_while_typing
```

可用的配置节和选项见[配置选项](../config-options.md)。

<a id="batch"></a>

## 批处理

使用 `--batch` 标志可一次执行多条命令，命令之间用 `;` 分隔。

> [!NOTE]
> 批处理中，单条命令内部的所有分号（例如多条 Lua 语句之间的分号）都必须用反斜杠转义，表示反斜杠本身的字符也必须转义。完成 shell 所要求的转义后，*还需要*进行上述转义。

<a id="flags"></a>

## 标志

可以按以下方式为请求指定标志：

```sh
hyprctl -j monitors
```

标志列表：
- `j` - 以 JSON 格式输出
- `i` - 选择实例（使用 hyprctl instances 列出的实例 ID 或索引）
- `r` - 执行命令后强制刷新状态（例如更改布局或规则后）
