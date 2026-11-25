# Lua 代码片段

<a id="code-snippets"></a>

## 代码片段

本页的代码片段可供参考，也可以直接复制粘贴使用。



<a id="per-layout-binds"></a>

### 为不同布局设置按键绑定

```lua
---@param bind_table table<HL.LayoutNamespace, HL.Dispatcher>
---@return fun()
local function layout_bind(bind_table)
    return function ()
        local workspace = hl.get_active_special_workspace() or hl.get_active_workspace()
        if not workspace then return end

        local layout = workspace.tiled_layout

        if bind_table[layout] then
            hl.dispatch(bind_table[layout])
        end
    end
end
```

用法：

```lua
hl.bind("SUPER + A", layout_bind({
    scrolling = hl.dsp.layout("swapcol l"),  -- Scrolling 布局：将当前列与左侧相邻列互换
    dwindle   = hl.dsp.layout("swapsplit"),  -- Dwindle 布局：交换窗口在分割中的位置
    monocle   = hl.dsp.layout("cycleprev"),  -- Monocle 和 master 布局：循环切换到上一个窗口
    master    = hl.dsp.layout("cycleprev"),
}))

hl.bind("SUPER + D", layout_bind({
    scrolling = hl.dsp.layout("swapcol r"),   -- Scrolling 布局：将当前列与右侧相邻列互换
    dwindle   = hl.dsp.layout("togglesplit"), -- Dwindle 布局：切换窗口的分割方向
    monocle   = hl.dsp.layout("cyclenext"),   -- Monocle 和 master 布局：循环切换到下一个窗口
    master    = hl.dsp.layout("cyclenext"),
}))
```

<a id="minimize-windows-using-special-workspaces"></a>

### 使用特殊工作区最小化窗口

这种方法借助特殊工作区模拟“最小化窗口”功能，用一个按键绑定即可在最小化和还原之间切换。请注意，每个按键绑定只能控制一个窗口。

```lua
hl.bind("SUPER + X", function ()
    if hl.get_workspace("special:minimized") then
        hl.dispatch(hl.dsp.window.move({ workspace = hl.get_active_workspace(), window = "tag:minimized" }))
        hl.dispatch(hl.dsp.window.clear_tags({ window = "tag:minimized" }))
    else
        hl.dispatch(hl.dsp.window.tag({ tag = "minimized", window = hl.get_active_window() }))
        hl.dispatch(hl.dsp.window.move({ workspace = "special:minimized", follow = false }))
    end
end)
```

<a id="share-keybinds-with-nested-sessions"></a>

### 与嵌套会话共享按键绑定

在为 Hyprland 做开发（或编写插件）时，你可能希望常用的 Hyprland 会话与嵌套会话共用按键绑定。为此，请将以下内容添加到 Lua 配置中：

```lua
hl.define_submap("locked", function()
    hl.bind("catchall", hl.dsp.no_op(), { non_consuming = true })

    -- 紧急退出方式
    hl.bind("CTRL + SHIFT + Escape", hl.dsp.submap("reset"))
end)

hl.on("window.active", function(window)
    if window and window.class == "aquamarine" then
        hl.dispatch(hl.dsp.submap("locked"))
    else
        hl.dispatch(hl.dsp.submap("reset"))
    end
end)
```

当焦点位于嵌套会话时，这段配置会阻止宿主会话接收按键事件，让你能在宿主和嵌套 Hyprland 会话中使用相同的快捷键。切换活动窗口或关闭嵌套会话后，默认按键绑定就会恢复。需要时，也可以按 `CTRL + SHIFT + Escape` 强制恢复默认按键绑定。

<a id="smart-gaps"></a>

### 智能间距

要实现其他窗口管理器或合成器中的“智能间距”功能，即“只有一个窗口时不留间距”，可使用以下配置：

```lua
hl.workspace_rule({ workspace = "w[tv1]", gaps_out = 0, gaps_in = 0 })
hl.workspace_rule({ workspace = "f[1]", gaps_out = 0, gaps_in = 0 })
hl.window_rule({ match = { float = false, workspace = "w[tv1]" }, border_size = 0 })
hl.window_rule({ match = { float = false, workspace = "w[tv1]" }, rounding = 0 })
hl.window_rule({ match = { float = false, workspace = "f[1]" }, border_size = 0 })
hl.window_rule({ match = { float = false, workspace = "f[1]" }, rounding = 0 })
```

<a id="smart-gaps-ignoring-special-workspaces"></a>

#### 智能间距（忽略特殊工作区）

你可以组合工作区选择器，更精细地控制规则的适用范围。例如，要忽略特殊工作区：

```lua
hl.workspace_rule({ workspace = "w[tv1]s[false]", gaps_out = 0, gaps_in = 0 })
hl.workspace_rule({ workspace = "f[1]s[false]", gaps_out = 0, gaps_in = 0 })
hl.window_rule({ match = { float = false, workspace = "w[tv1]s[false]" }, border_size = 0 })
hl.window_rule({ match = { float = false, workspace = "w[tv1]s[false]" }, rounding = 0 })
hl.window_rule({ match = { float = false, workspace = "f[1]s[false]" }, border_size = 0 })
hl.window_rule({ match = { float = false, workspace = "f[1]s[false]" }, rounding = 0 })
```

<a id="float-browsers-extension-windows"></a>

### 让浏览器扩展窗口浮动

所有已知浏览器都有一个恼人的“特性”：它们会把扩展窗口的标题设为浏览器自身的名称。以下函数会监听窗口打开事件，并将匹配的窗口设为浮动：

```lua
hl.on("window.open", function(w)
    if w.class ~= "firefox" then return end
    if w.initial_title ~= "Mozilla Firefox" then return end

    local ff_windows = hl.get_windows({ class = "firefox" })
    if #ff_windows <= 1 then return end

    hl.dispatch(hl.dsp.window.float({ action = "set", window = w }))

    local sub
    sub = hl.on("window.title", function(tw)
        if tw.address ~= w.address then return end
        if tw.title == ""
            or tw.title == "Mozilla Firefox"
            or tw.title == "about:blank"
            or tw.title:match("^about:.*Mozilla Firefox$") then return end

        sub:remove()

        if tw.title:match("^Extension:") then
            hl.dispatch(hl.dsp.window.resize({ x = 800, y = 600, window = tw }))
            hl.dispatch(hl.dsp.window.center({ window = tw }))
            hl.dispatch(hl.dsp.focus({ window = tw }))
        else
            hl.dispatch(hl.dsp.window.float({ action = "unset", window = tw }))
        end
    end)
end)
```

<a id="open-tor-browser-and-mullvad-browser-at-their-default-window-size"></a>

### 以默认窗口大小打开 Tor Browser 和 Mullvad Browser

Tor Browser 和 Mullvad Browser 都会以各自所有用户共用的窗口大小启动，这样就不会有用户因屏幕尺寸而显得与众不同。平铺、最大化或全屏时，窗口大小取决于实际布局，浏览器会在内容周围留白以作补偿。详见 [Tor Browser 9.0 发行说明](https://blog.torproject.org/new-release-tor-browser-90/)和 [TZP](https://github.com/arkenfox/TZP)。

将这两个浏览器的窗口设为浮动，即可保留默认大小：

```lua
hl.window_rule({
    name = "privacy-browsers-float",
    match = { class = "^(Tor Browser|Mullvad Browser)$" },
    float = true,
    center = true,
    fullscreen_state = "0 0",
    suppress_event = "maximize",
})
```

请勿为这些窗口添加 `size` 规则。

<a id="config-versioning"></a>

### 按版本调整配置

有些更新会引入不兼容的改动，你可以根据 Hyprland 版本提前在配置中作出相应处理。

你可以使用 `hl.version()` 为配置添加版本条件，例如：

```lua
if hl.version() == "0.55.2" then
    hl.config({
        general = {
            changed_property = "value"
        }
    })
else
    hl.notification.create({
        text = "You're using: ".. hl.version(),
        timeout = 10000
    })
end
```

<a id="starts-with-helper-function"></a>

### 判断字符串是否以指定前缀开头的辅助函数

```lua
---@param string string
---@param prefix string
---@return boolean
local function starts_with(string, prefix)
    return string:find(prefix, 1, true) == 1
end
```

<a id="toggle-animationsbluretc-hotkey"></a>

### 用于开关动画、模糊等效果的快捷键

你可以通过一个按键绑定轻松开关动画和其他效果，暂时减少干扰，或在笔记本电脑上节省电量：

```lua
local game_mode = false

hl.bind("SUPER + F1", function ()
    if game_mode then
        hl.dispatch(hl.dsp.reload_config())
        return
    end

    hl.config({
        general = {
            gaps_in = 0,
            gaps_out = 0,
            border_size = 0,
        },

        animations = {
            enabled = false,
        },

        decoration = {
            shadow = { enabled = false },
            blur = { enabled = false },
            rounding = 0,
        }
    })

    game_mode = true
end)
```

<a id="cycle-layout-for-current-workspace"></a>

### 循环切换当前工作区的布局

要更改当前工作区的布局，可以使用以下按键绑定：

```lua
hl.bind("SUPER + tab", function ()
    local layouts   = { "scrolling", "dwindle", "master", "monocle" }
    local next_layout

    local workspace = hl.get_active_special_workspace() or hl.get_active_workspace()
    if not workspace then return end

    for i = 1, #layouts do
        if layouts[i] == workspace.tiled_layout then
            next_layout = layouts[ i % #layouts + 1 ]
            goto dispatch
        end
    end

    ::dispatch::
    hl.workspace_rule({ workspace = workspace.addressable_name, layout = next_layout })
end)
```

<a id="windows-magnifier-like-cursor-zoom"></a>

### 类似 Windows 放大镜的光标跟随缩放

这些按键绑定可调整整个屏幕的缩放倍数。放大后的视图会随光标移动，让光标始终可见，效果类似于 Windows 放大镜的全屏模式。

```lua
local MAX_ZOOM = 3
local MIN_ZOOM = 1
local ZOOM_TOGGLE_FACTOR = 0.5

---@param offset number
---@return nil
local function zoom(offset)
    local current = hl.get_config("cursor.zoom_factor")

    -- 如果未提供偏移量，切换后默认执行缩放；否则使用传入的缩放值
    current = current + (offset and offset or ZOOM_TOGGLE_FACTOR)
    if current < MIN_ZOOM then current = MIN_ZOOM end
    if current > MAX_ZOOM then current = MAX_ZOOM end

    hl.config({ cursor = { zoom_factor = current } })
end

hl.bind("SUPER + Z", zoom)
hl.bind("SUPER + KP_ADD", function()
    zoom(0.5)
end)
hl.bind("SUPER + Minus", function()
    zoom(-0.5)
end)
```

<a id="launching-programs-on-workspace-creation"></a>

### 创建工作区时启动程序

要实现旧版 `on_created_empty` 工作区规则的效果，可通过 `workspace.created` [事件](core/advanced-configuration/events.md)启动程序。例如：

```lua
local workspace_programs = {
    ["5"]               = { "firefox", { float = true } },
    ["6"]               = { "kitty",   { fullscreen = true } },
    ["special:special"] = { "discord", {} },
}

hl.on("workspace.created", function(ws)
    if not ws.is_empty then return end

    local program = workspace_programs[ws.addressable_name]
    if not program then return end

    local cmd, rules = table.unpack(program)

    -- 浅拷贝规则表
    -- 如果不创建副本，就会修改 workspace_programs 中的原始表
    local shallow_rules = {}
    for k, v in pairs(rules) do shallow_rules[k] = v end
    shallow_rules.workspace = ws.addressable_name .. " silent"

    hl.exec_cmd(cmd, shallow_rules)
end)
```

<a id="move-focus-between-tiled-and-floating-windows"></a>

### 在平铺窗口和浮动窗口之间切换焦点

其作用类似于 i3 的 `focus mode_toggle` 按键绑定。

```lua
hl.bind("SUPER + space", function()
    local window = hl.get_active_window()
    if not window then return end

    hl.dispatch(hl.dsp.window.cycle_next({
        floating = not window.floating,
        tiled = window.floating,
    }))
end, { description = "Switch focus between tiled and floating windows" })
```

<a id="pin-floating-windows-with-no_focus-and-restore-them"></a>

### 使用 no_focus 固定浮动窗口并将其还原

这个函数能让歌词窗口等浮动窗口在每个工作区都保持可见，同时避免抢占其他窗口的焦点。需要移动这些窗口时，也可以用这个函数将它们还原为普通浮动窗口。
注意：在普通窗口上再次调用此函数，会还原之前被设为该状态的所有窗口。

```lua
local function pin_nofocus_toggle()
    local tag = "pin_nofocus"

    local function has_tag(window)
        for _, t in ipairs(window.tags or {}) do
            if t == tag then
                return true
            end
        end
        return false
    end

    return function()
        local window = hl.get_active_window()
        if not window then return end

        if window.floating and window.fullscreen == 0 and not window.pinned and not has_tag(window) then
            -- 给窗口添加标签，并将其设为置顶，同时启用 no_focus
            hl.dispatch(hl.dsp.window.tag({ tag = "+" .. tag, window = window }))
            hl.dispatch(hl.dsp.window.pin({ window = window }))
            hl.dispatch(hl.dsp.window.set_prop({ prop = "no_focus", value = "1", window = window }))
        else
            -- 恢复所有以这种方式标记的窗口
            for _, marked_window in ipairs(hl.get_windows({ tag = tag })) do
                hl.dispatch(hl.dsp.window.set_prop({ prop = "no_focus", value = "unset", window = marked_window }))
                if marked_window.pinned then
                    hl.dispatch(hl.dsp.window.pin({ window = marked_window }))
                end
                hl.dispatch(hl.dsp.window.tag({ tag = "-" .. tag, window = marked_window }))
            end
        end
    end
end
hl.bind("SUPER + P", pin_nofocus_toggle())
```

<a id="vim-like-keymaps"></a>

### 类似 Vim 的按键映射

Hyprland 的功能很多，如果想为每项功能都设置按键绑定，键盘上的键可能不够用。不用担心，如果需要更多绑定，可以利用子映射创建按键映射。与需要同时按下多个修饰键的单个按键绑定相比，这些映射也更容易操作。

下面是用这种方式管理窗口组的示例：

```lua
hl.bind("SUPER + G", hl.dsp.submap("group_management"), { description = "Enter a group management submap" })

---@param keys string
---@param action HL.Dispatcher
---@param description string
---@return HL.Keybind
local map = function(key, action, description)
    hl.bind(key, function()
        hl.dispatch(action)
        hl.dispatch(hl.dsp.submap("reset"))
    end, { description = description })
end

hl.define_submap("group_management", function()
    map("G", hl.dsp.group.toggle(), "Toggle window group")

    map("H", hl.dsp.window.move({ into_group = "l" }), "Move window into a group on the left")
    map("J", hl.dsp.window.move({ into_group = "d" }), "Move window into a group on the bottom")
    map("K", hl.dsp.window.move({ into_group = "u" }), "Move window into a group on the top")
    map("L", hl.dsp.window.move({ into_group = "r" }), "Move window into a group on the right")

    map("E", hl.dsp.window.move({ out_of_group = true }), "Move window out of group")

    map("N", hl.dsp.group.next(), "Next window in group")
    map("P", hl.dsp.group.prev(), "Previous window in group")

    map("F", hl.dsp.group.move_window(), "Move window forward in the group order")
    map("B", hl.dsp.group.move_window({ forward = false }), "Move window backward in the group order")

    map("T", hl.dsp.group.lock_active(), "Toggle group lock")

    for i = 1, 10 do
        map(tostring(i % 10), hl.dsp.group.active({ index = i }), "Focus window " .. i .. " in a group")
    end

    hl.bind("Escape", hl.dsp.submap("reset"), { description = "Quit submap" })
end)
```

<a id="close-all-windows-at-once"></a>

### 一次关闭所有窗口

```lua
local function closeAllWindows()
    local windows = hl.get_windows()

    for _,w in pairs(windows) do
        hl.dispatch(hl.dsp.window.close({ window = w }))
    end
end

local function closeAllWindowsCurrentWorkspace()
    local cws = hl.get_active_special_workspace() or hl.get_active_workspace()
    local windows = hl.get_windows({ workspace = cws })

    for _,w in pairs(windows) do
        hl.dispatch(hl.dsp.window.close({ window = w }))
    end
end

hl.bind("SUPER + BackSpace", closeAllWindowsCurrentWorkspace )
hl.bind("SUPER + Delete", closeAllWindows )
```

<a id="move-all-windows-in-current-workspace-to-another"></a>

### 将当前工作区的所有窗口移至另一个工作区

```lua
---@param ws HL.Workspace
---@param follow boolean
---@return nil
local function moveWindowsCurrentWorkspace(ws, follow)
    local cws = hl.get_active_special_workspace() or hl.get_active_workspace()
    local windows = hl.get_windows({ workspace = cws })

    for _, w in pairs(windows) do
        hl.dispatch(
            hl.dsp.window.move({
                window = w,
                workspace = ws,
                follow = follow
            })
        )
    end
end

for i = 1, 10 do
    local key = i % 10
    hl.bind("SUPER + SHIFT + ALT + " .. key, function()
        moveWindowsCurrentWorkspace(i, true)
    end)
end

for i = 1, 10 do
    local key = i % 10
    hl.bind("SUPER + CTRL + ALT + " .. key, function()
        moveWindowsCurrentWorkspace(i, false)
    end)
end
```

<a id="switch-to-workspaces-01-99"></a>

### 切换到 01 至 99 号工作区

```lua
hl.bind("SUPER + P", hl.dsp.submap("ws_tens"), { description = "Workspace picker (01-99)" })

hl.define_submap("ws_tens", function()
    for tens = 0, 9 do
        hl.bind(tostring(tens), hl.dsp.submap("ws_units_" .. tens))
    end

    local letters = "abcdefghijklmnopqrstuvwxyz"
    for i = 1, #letters do
        hl.bind(letters:sub(i, i), hl.dsp.submap("reset"))
    end
    hl.bind("Escape", hl.dsp.submap("reset"))
end)

for tens = 0, 9 do
    hl.define_submap("ws_units_" .. tens, "reset", function()
        for units = 0, 9 do
            local target = tens * 10 + units
            if target > 0 then
                hl.bind(tostring(units), hl.dsp.focus({ workspace = target }))
            end
        end
        hl.bind("Escape", hl.dsp.submap("reset"))
        hl.bind("catchall", hl.dsp.submap("reset"))
    end)
end
```
