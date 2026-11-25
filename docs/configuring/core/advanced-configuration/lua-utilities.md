# Lua 实用函数

<a id="lua-utilities"></a>

## Lua 实用工具

Hyprland 提供了多种 Lua 实用工具，你可以用它们编写脚本，为桌面添加自定义功能等。


<details><summary>示例</summary>

```lua
-- 将按键绑定为切换窗口的浮动状态；如果窗口是 htop，
-- 则只将其设为浮动

hl.bind("SUPER + X", function()
  local w = hl.get_active_window()
  if w ~= nil and w.title == "htop" do
    hl.dispatch(hl.dsp.window.float({ action = "set" }))
  else
    hl.dispatch(hl.dsp.window.float({ action = "toggle" }))
  end
end)
```


</details>

<a id="convenience-functions"></a>

### 便捷函数

Hyprland 提供以下便捷函数：
- `hl.get_config()`
- `hl.get_active_window()`
- `hl.get_windows()`
- `hl.get_window(selector)`
- `hl.get_urgent_window()`
- `hl.get_workspaces()`
- `hl.get_workspace(selector)`
- `hl.get_active_workspace()`
- `hl.get_active_special_workspace()`
- `hl.get_monitors({ all? })`
- `hl.get_monitor(selector)`
- `hl.get_active_monitor()`
- `hl.get_monitor_at({ x = int, y = int })`
- `hl.get_monitor_at_cursor()`
- `hl.get_cursor_pos()`
- `hl.get_last_window()`
- `hl.get_last_workspace()`
- `hl.get_layers()`
- `hl.get_workspace_windows(workspace_selector)`
- `hl.get_current_submap()`
- `hl.version()`
- `hl.exec_cmd()`
- `hl.exec_scheduled_prop_refresh_immediately()`
- `hl.get_loaded_plugins()`
- `hl.is_key_down(key = int/string)`

要查看这些函数的返回值（类及其参数），可以使用 LSP，也可以直接查阅存根文件。有关如何在代码编辑器中配置 LSP，请参阅[编辑器自动补全](../_index.md#editor-autocompletion)。

<a id="hlexec_cmd-function"></a>

### `hl.exec_cmd` 函数

`hl.exec_cmd()` 会异步启动进程，因此无需在命令末尾添加 `& disown`。

<a id="dynamically-changing-a-config-option"></a>

### 动态更改配置选项：

使用 `hl.get_config()` 可以获取配置选项的当前值。调用时传入配置选项名，例如 `"general.layout"`。

请注意，`hl.get_config()` 的返回类型反映了该配置选项实际的底层类型。

例如，如果在 `hl.config()` 中通过 `gaps_in = 3` 设置 `general.gaps_in`，`hl.get_config()` 会返回如下形式的表：
```lua
{
  top = 3,
  left = 3,
  right = 3,
  bottom = 3
}
```
这是因为 `gaps_in` 也接受 `{ top?, left?, right?, bottom? }` 形式的表。

你可以通过按键绑定更改配置选项的值，脚本示例如下：
```lua
-- 在 0 和 3 之间切换 gaps_in（其中 3 等价于 {3, 3, 3, 3}）
hl.bind(mainMod .. " + SHIFT + G", function()
    if hl.get_config("general.gaps_in").top == 3 then
        hl.config({ ["general.gaps_in"] = 0 })
    else
        hl.config({ ["general.gaps_in"] = 3 })
    end
end)
```

<a id="prop-refresh"></a>

### 属性刷新

属性刷新是指 Hyprland 更新或刷新多项可配置选项的事件，例如键盘布局、设备配置、显示器状态、窗口间距等。

创建工作区规则等事件会安排一次属性刷新，在当前事件结束后执行。

为避免重复刷新属性，Hyprland 会安排在当前事件（例如一次 Lua 函数调用）结束时执行**一次**属性刷新。

具体来说，如果你创建一条新工作区规则来移除当前工作区的 `gaps_in`，`gaps_in` 的值要到 Lua 函数结束时才会改变。因此，函数中设置工作区规则之后的代码仍会使用旧值。只有在函数结束后，当前工作区的 `gaps_in` 值才会更新，以反映新规则。

如果你的代码依赖工作区的 `gaps_in` 值在规则创建后立即更新，这种行为可能会导致问题。

要立即执行已安排的属性刷新，请使用 `hl.exec_scheduled_prop_refresh_immediately()`。请注意，提前执行后，该事件会从事件循环中移除，从而允许下一次属性刷新进入队列。

> [!WARNING]
> 过于频繁地调用此函数可能会降低性能！你可以使用 `config.props_refreshed` 事件查看每个事件触发了多少次属性刷新。

<a id="timers"></a>

### 定时器

你可以通过 `hl.timer()` 创建和管理定时器：

```lua
local demoTimer = hl.timer(function()
  print("hello from timer")
end, { timeout = 1000, type = "repeat" })

demoTimer:set_enabled(false)

hl.bind("SUPER + X", function()
  -- 切换计时器的启用状态
  demoTimer:set_enabled(not demoTimer:is_enabled())
end)
```

<a id="sockets-ipc"></a>

## 套接字（IPC）

大多数情况下建议使用 Lua。Lua 速度更快，更不容易出错，功能也更丰富，而且与 Hyprland 的集成通常更紧密。如果你想使用 IPC，请参阅[进程间通信（IPC）](../../../ipc/_index.md)页面。
