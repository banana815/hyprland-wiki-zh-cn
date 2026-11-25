# 调度器

<a id="dispatchers"></a>

## 调度器

调度器返回一个表，描述你想执行的操作。**调度器不会立即执行任何操作，其返回的表内容也没有任何稳定性保证。**这些表用于传给 `hl.bind()` 或 `hl.dispatch()`。

请注意，某些布局专用的调度器会列在相应的布局页面中（见侧边栏）。

要在函数中使用调度器（即任意 `hl.dsp.*`），必须将其传给 `hl.dispatch()`，相应操作才会执行。**单独写 `hl.dsp.whatever()` 不会执行任何操作。**


<details><summary>示例</summary>


在第一段代码中，`function()` 通过调用 `hl.dispatch()` 实际触发了相应操作。

```lua
hl.bind("ALT + Tab", function()
    hl.dispatch(hl.dsp.window.cycle_next())
    hl.dispatch(hl.dsp.window.alter_zorder({ mode = "top" }))
end)
```

在第二段代码中，虽然创建了调度器，却没有将它们传给 `hl.dispatch`。由于没有执行这些调度器，因此不会产生任何效果。

```lua
hl.bind("ALT + Tab", function()
    hl.dsp.window.cycle_next()
    hl.dsp.window.alter_zorder({ mode = "top" })
end)
```



</details>

<a id="parameter-explanation"></a>

### 参数说明

| 参数类型 | 说明 |
| --- | --- |
| `window` | 未设置时默认为 `"activewindow"`。可以使用任一[窗口选择器](../selectors.md#window-selector) |
| `action` | 未设置时默认为 `"toggle"`。可选值为 `"toggle"`、`"enable"`/`"on"`、`"disable"`/`"off"` |
| `relative` | 未设置时默认为 `"false"`。可选值为 `"false"`、`"true"` |

<a id="dispatchers-1"></a>

## 调度器



<a id="general"></a>

### 概述

`hl.dsp.` 包含以下调度器：

| 方法 | 说明 |
| --- | --- |
| `dpms({ monitor?, action? })` | 切换显示器的开关状态（类似空闲时启动屏保，并非切断显示器电源）。请勿直接通过按键绑定调用！ |
| `event( string )` | 向 socket2 发送事件 |
| `exec_cmd( cmd, { rules }? )` | 执行命令。规则可以是一个表，其中列出要应用的窗口规则效果（见[下文](#executing-with-rules)） |
| `exec_raw( cmd )` | 直接执行原始命令。`exec_cmd` 会通过 `sh -c` 执行命令，而此调度器不会 |
| `exit()` | 退出 Hyprland。建议使用 `hyprshutdown` 代替此调度器 |
| `focus({ direction })` | 向指定方向移动焦点 |
| `focus({ monitor })` | 将焦点移至指定显示器 |
| `focus({ workspace, on_current_monitor? })` | 将焦点移至指定工作区 |
| `focus({ window })` | 将焦点移至指定窗口 |
| `focus({ urgent_or_last })` | 将焦点移至请求紧急关注的窗口，或移至上一个获得焦点的窗口 |
| `focus({ last })` | 将焦点移至上一个获得焦点的窗口 |
| `force_idle( int )` | 设置所有空闲计时器已经过的时间（以秒为单位），忽略空闲抑制器。下次有活动时，计时器将恢复正常行为。请勿直接通过按键绑定调用！ |
| `force_renderer_reload()` | 强制重新加载所有显示器的渲染器 |
| `global( string, activate? )` | 触发 D-Bus 全局快捷键，也可指定发送激活事件或停用事件。参见[全局快捷键](binds/globals.md#d-bus-global-shortcuts) |
| `layout( message )` | 以字符串形式发送布局消息 |
| `no_op()` | 不执行任何操作。适用于条件按键绑定 |
| `pass({ window? })` | 将快捷键传递给指定窗口 |
| `release_input_capture()` | 释放所有活动的输入捕获会话 |
| `reload_config()` | 重新加载配置，效果与 `hyprctl reload` 相同 |
| `send_key_state({ window?, mods, key, state })` | 与 send_shortcut 相同，但可以将 `state` 设为 `"down"`/`"up"` 来控制按下或释放状态 |
| `send_shortcut({ window?, mods, key })` | 向指定窗口发送特定快捷键 |
| `submap( name )` | 切换到指定的按键绑定子映射 |

> [!WARNING]
> 不建议直接通过按键绑定设置 DPMS 或 force_idle，因为这样做可能导致未定义行为。可以考虑采用类似下面的做法：
> ```lua
> hl.bind("...", function()
>     hl.timer(function()
>         hl.dispatch(hl.dsp.dpms({ action = "disable" }))
>     end, {timeout = 500, type = "oneshot"})
> end)
> ```

<a id="window"></a>

### Window

`hl.dsp.window.` 包含以下调度器：

| 方法 | 说明 |
| --- | --- |
| `alter_zorder({ window?, mode })` | 模式可以是 "top" 或 "bottom"。 |
| `center({ window? })` | 将当前窗口置于屏幕中央。 |
| `clear_tags({ window? })` | 清除窗口的所有标签。 |
| `close({ window? })` | 请求窗口正常关闭。 |
| `cycle_next({ window?, next?, tiled?, floating? })` | 将焦点移至下一个窗口。 |
| `deny_from_group({ action? })` | 禁止窗口加入窗口组。 |
| `drag()` | 开始交互式拖动，与鼠标按键绑定配合使用。 |
| `float({ window?, action? })` | 设置窗口的浮动状态。 |
| `fullscreen_state({ window?, action?, internal, client, layout_aware? })` | 更精细地设置窗口的全屏状态。`action` 可取 `toggle`/`set`/`unset`。`layout_aware` 可取 `true`（默认）或 `false`，用于选择由布局处理全屏行为，还是使用默认处理方式。参见[全屏状态](#fullscreen_state)和[全屏处理器](#fullscreen-handlers)。 |
| `fullscreen({ window?, action?, mode?, layout_aware? })` | 设置窗口的全屏状态。`mode` 可取 "maximized" 或 "fullscreen"。`action` 可取 `toggle`/`set`/`unset`。`layout_aware` 可取 `true`（默认）或 `false`，用于选择由布局处理全屏行为，还是使用默认处理方式。 |
| `kill({ window? })` | 发送 `SIGKILL` 信号，强制终止窗口所属的进程。 |
| `move({ window?, direction, group_aware? })` | 沿指定方向移动窗口。设置 `group_aware = true` 后，窗口可沿该方向移入或移出窗口组。 |
| `move({ window?, workspace, follow? })` | 将窗口移至指定工作区。 |
| `move({ window?, monitor, follow? })` | 将窗口移至指定显示器。 |
| `move({ window?, x, y, relative? })` | 按给定坐标偏移量移动窗口（`relative = true`），或将窗口移至给定的绝对坐标（`relative = false`）。 |
| `move({ window?, into_group = direction })` | 将窗口移入指定方向上的窗口组。 |
| `move({ window?, into_or_create_group = direction })` | 将窗口移入指定方向上的窗口组。如果该方向上没有窗口组，则创建一个。 |
| `move({ window?, out_of_group })` | 将窗口移出窗口组。无需指定方向时传入 `true`，需要指定方向时传入相应的方向值。 |
| `pin({ window?, action? })` | 固定窗口。 |
| `pseudo({ window?, action? })` | 设置窗口的伪平铺状态。 |
| `resize({ keep_aspect_ratio? })` | 开始交互式调整窗口大小，与鼠标按键绑定配合使用。此操作会覆盖窗口的 `keep_aspect_ratio` 属性。 |
| `resize({ window?, x, y, relative? })` | 调整窗口大小。 |
| `set_prop({ window?, prop, value })` | 设置窗口属性。 |
| `signal({ window?, signal })` | 向窗口所属的进程发送 POSIX 信号。 |
| `swap({ direction })` | 将当前窗口与指定方向上的另一个窗口交换位置。 |
| `swap({ target })` | 将当前窗口与另一个窗口交换位置。 |
| `swap({ next })` | 将当前窗口与下一个窗口交换位置。 |
| `swap({ prev })` | 将当前窗口与上一个窗口交换位置。 |
| `tag({ window?, tag })` | 为窗口添加标签。 |
| `toggle_swallow()` | 切换所有被吞并窗口的显示与隐藏状态。 |

<a id="workspace"></a>

### Workspace

`hl.dsp.workspace.` 包含以下调度器：

| 方法 | 说明 |
| --- | --- |
| `change_id({ workspace, id })` | 更改编号工作区的 ID。新 ID 必须大于 0，且尚未被使用。 |
| `move({ workspace?, monitor })` | 将工作区移至指定显示器。 |
| `rename({ workspace, name? })` | 重命名工作区。此操作仅更改显示名称，工作区的标识保持不变。配置中的操作仍使用工作区创建时的标识来引用它。 |
| `swap_monitors({ monitor1, monitor2 })` | 交换两台显示器各自当前显示的工作区。 |
| `show({ workspace })` | 在工作区关联的显示器上显示该工作区，同时保持当前焦点不变。 |
| `toggle_special( special_name )` | 按名称切换特殊工作区的显示与隐藏状态。 |

> [!NOTE]
> 使用 `toggle_special()` 时，**不要**在工作区名称中包含 `special:` 前缀。详情请参阅[命名约定](../naming-conventions.md)中的说明。

<a id="group"></a>

### 窗口组

`hl.dsp.group.` 包含以下调度器：

| 方法 | 说明 |
| --- | --- |
| `active({ window?, index })` | 按索引切换到组内的指定窗口。 |
| `lock({ all?, action? })` | 锁定所有窗口组。 |
| `lock({ window?, action? })` | 锁定指定窗口所在的窗口组。 |
| `move_window({ window?, forward? })` | 调整窗口在组内的排列顺序。 |
| `next({ window? })` | 切换到组内的下一个窗口。 |
| `prev({ window? })` | 切换到组内的上一个窗口。 |
| `toggle({ window? })` | 切换窗口的分组状态。 |

<a id="cursor"></a>

### 光标

`hl.dsp.cursor.` 包含以下调度器：

| 方法 | 说明 |
| --- | --- |
| `move({ x, y })` | 将光标移至指定坐标。 |
| `move_to_corner({ window?, corner })` | 将光标移至窗口的指定角落。角落编号范围为 [0 - 3]。 |

<a id="grouped-tabbed-windows"></a>

### 窗口分组（标签页）

在 Hyprland 中，你可以使用 `hl.dsp.group.toggle()` 按键绑定调度器，用当前活动窗口创建一个窗口组。

窗口组类似于 i3wm 的 "tabbed"（标签页式）容器。它只占用一个窗口的空间，你可以在组内的窗口之间切换。

你可以使用 `lock` 调度器锁定窗口组，阻止新窗口加入该组。

你可以使用 `window.deny_from_group` 调度器，禁止某个窗口加入窗口组或自行成组。

<a id="special-workspaces"></a>

## 特殊工作区

> [!NOTE]
> 你可以定义多个具名特殊工作区，但同时最多只能存在 97 个。

特殊工作区在其他一些环境中称为 “scratchpad”（暂存区）。你可以在任意显示器上显示或隐藏它。

例如，要将窗口移至具名特殊工作区，可以使用以下语法：

```lua
hl.bind("SUPER + SHIFT + S", hl.dsp.window.move({ workspace = "special:magic" }))
-- 显示或隐藏工作区及其所有窗口：
hl.bind("SUPER + S", hl.dsp.workspace.toggle_special("magic"))
```

> [!NOTE]
> 仅处理特殊工作区的调度器（如 `hl.dsp.workspace.toggle_special()`）接受工作区名称，并会自行添加 `special:` 前缀。对于接受*任意*工作区的调度器，必须显式添加 `special:` 前缀，才能指定正确的特殊工作区。上例演示了这一用法。

<a id="executing-with-rules"></a>

## 执行命令时应用规则

`exec_cmd` 调度器支持添加[窗口规则](rules/_index.md)。实际效果因窗口而异。调度器会记录新启动进程的 PID，并据此应用规则。例如，如果该进程派生出子进程，然后由子进程打开窗口，这种方式就不会生效。


<details><summary>示例</summary>


```lua
hl.bind("SUPER + E", hl.dsp.exec_cmd("kitty", { float = true, move = {0, 0} }))
```



</details>

<a id="set_prop"></a>

## set_prop

可设置的属性包括[窗口规则](rules/window-rules.md#dynamic-effects)中的所有_动态效果_。

例如：
```lua
hl.dsp.window.set_prop({ prop = "no_anim", value = "1" })
hl.dsp.window.set_prop({ prop = "no_anim", value = "1", window = "class:abc" })
```

有些属性是只读的，其值取自窗口规则。如果没有匹配的规则，则根据窗口状态，从其他相关的可写属性中取值：
- `border_color`：取值由 `active_border_color`、`inactive_border_color` 决定。
- `opacity`：取值由 `opacity`、`opacity_inactive`、`opacity_fullscreen`、`opacity_override`、`opacity_inactive_override`、`opacity_fullscreen_override` 决定。

<a id="fullscreen_state"></a>

## fullscreen_state

`fullscreen_state` 调度器将 Hyprland 为窗口维护的状态与告知客户端的全屏状态分开，使两者可以独立设置。

`internal` 指 Hyprland 维护的状态，`client` 指应用程序接收到的状态。

| 值 | 状态 | 说明 |
| --- | --- | --- |
| -1 | 当前状态 | 保持当前的全屏状态。 |
| 0 | 非全屏 | 窗口占用当前布局为其分配的空间。 |
| 1 | 最大化 | 窗口占满整个工作区域，同时保留边距。 |
| 2 | 全屏 | 窗口占满整个屏幕。 |

例如：
- `{internal = 2, client = 0}` 将应用程序窗口设为全屏，同时告知客户端窗口仍处于非全屏模式。这有助于防止基于 Chromium 的浏览器因检测到窗口已全屏而进入演示模式。
- `{internal = 0, client = 2}` 使窗口保持非全屏状态，同时告知客户端窗口已进入全屏模式。

<a id="restore-client-maximized-state"></a>

### 恢复客户端的最大化状态

用户无法直接选择此模式。当窗口的内部模式为最大化，而客户端又请求全屏时，窗口就会进入这一状态。

此时，下一次请求退出全屏时，窗口将恢复为最大化状态。例如，在最大化的窗口中观看视频时，将视频切换为全屏就会出现这种情况。

<a id="fullscreen-handlers"></a>

### 全屏处理器

某些布局（如 scrolling 滚动布局）提供自己的全屏处理方式，会覆盖默认行为。

在这些布局中，你可以通过全屏调度器的 `layout_aware` 选项，选择由布局处理的全屏模式，或使用默认处理方式的全屏模式。

可以通过 Lua 代码查看指定窗口正在使用哪个全屏处理器。例如：
```lua
local win = hl.get_active_window()
if win.fullscreen_handler == "default" then
    -- 执行一些操作
end
```
