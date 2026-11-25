# 手势

<a id="general"></a>

## 概述

Hyprland 的部分操作支持 1:1 跟随手指移动的触摸板手势。基本语法如下：

```lua
hl.gesture({
    action = "...",
    direction = "...",
    fingers = int,
})
```

可以使用 `mods` 限定手势仅在按住指定修饰键时生效，也可以使用 `scale` 按比例调整动画速度：

```lua
hl.gesture({ fingers = 3, direction = "horizontal", action = "workspace" })
hl.gesture({ fingers = 3, direction = "down", mods = "ALT", action = "close" })
hl.gesture({ fingers = 3, direction = "up", mods = "SUPER", scale = 1.5, action = "fullscreen" })
hl.gesture({ fingers = 3, direction = "left", scale = 1.5, action = "float" })
```

<a id="fields"></a>

### 字段



| 字段 | 说明 | 类型 | 范围 |
| --- | --- | --- | --- |
| action | 要执行的操作 | string |  |
| direction | 手势方向 | string |  |
| fingers | 手指数量 | int | [2 - 9] |
| disable_inhibit | 设为 true 时，允许手势绕过快捷键抑制器 | bool |  |
| mods | 修饰键掩码，例如 `"SUPER"` 或 `"ALT SHIFT"` | string |  |
| scale | 手势变化量的倍率 | float | [0.1 - 10.0] |

某些手势还有专用的附加字段，详见[操作](#actions)表。

<a id="directions"></a>

### 方向

支持以下方向：



| 方向 | 说明 |
| --- | --- |
| swipe | 任意方向滑动 |
| horizontal | 水平滑动 |
| vertical | 垂直滑动 |
| left | 向左滑动 |
| right | 向右滑动 |
| up | 向上滑动 |
| down | 向下滑动 |
| pinch | 捏合或张开 |
| pinchin | 向内捏合 |
| pinchout | 向外张开 |

<a id="actions"></a>

### 操作

将操作指定为 `unset` 即可取消先前设置的特定手势。各项参数必须与原手势完全一致，包括方向、修饰键、手指数量和缩放系数。



| 动作 | 说明 | 附加参数 |
| --- | --- | --- |
| _Lua 函数_ | 执行具名 Lua 函数或 Lua 匿名函数。详见下文 | 无 |
| close | 关闭活动窗口 | 无 |
| cursor_zoom | 以指针为中心放大画面 | `zoom_level` 指定缩放倍数。将 `mode` 设为 `"mult"` 可按倍率缩放，设为 `"live"` 则会在捏合手势过程中持续更新缩放比例 |
| float | 使活动窗口浮动 | 可将 `mode` 设为 `"float"` 或 `"tile"`，强制窗口进入浮动或平铺状态 |
| fullscreen | 使活动窗口全屏显示 | 可将 `mode` 设为 `"maximize"`，使窗口最大化而非全屏显示 |
| move | 移动活动窗口 | 无 |
| resize | 调整活动窗口的大小 | 无 |
| scroll_move | 如果当前使用滚动布局，则滚动窗口带 | 无 |
| special | 切换特殊工作区的显示状态 | 特殊工作区的名称 |
| workspace | 用于切换工作区的滑动手势 | 无 |

<a id="cursor_zoom"></a>

#### cursor_zoom

示例：

```lua
hl.gesture({ fingers = 2, direction = "pinch", action = "cursor_zoom", zoom_level = 2 })
hl.gesture({ fingers = 2, direction = "pinch", action = "cursor_zoom", zoom_level = 1.2, mode = "mult" })
hl.gesture({ fingers = 2, direction = "pinch", action = "cursor_zoom", zoom_level = 1, mode = "live" })
```

`cursor_zoom` 默认在缩放和原始大小之间切换。`mult` 将当前缩放值乘以指定倍率。`live` 会随手指捏合或张开的幅度持续调整缩放比例，并始终以手势开始时的指针位置为缩放中心。`live` 模式不使用数值参数，因此可以用 `1` 占位。

<a id="lua-functions"></a>

#### Lua 函数

Lua 函数可以是具名函数，也可以是匿名函数。

使用匿名函数的示例：

```lua
hl.gesture({
    fingers = 3,
    direction = "up",
    action = function()
        hl.notification.create({ text = "I just swiped on my trackpad!", timeout = 5000, icon = "ok" })
    end
})
```

使用具名函数的示例：



```lua
local function swipe()
    hl.notification.create({ text = "I just swiped on my trackpad!", timeout = 5000, icon = "ok" })
end

hl.gesture({
    fingers = 3,
    direction = "up",
    action = swipe
})
```

<a id="live-lua-gestures"></a>

#### 实时 Lua 手势

对于实时手势（即会随手势状态变化而作出响应的手势），请传入一个包含 `start`、`update` 和 `finish` 方法的表，而非匿名函数。

`start` 和 `update` 方法会收到一个包含以下字段的表：

| 字段 | 说明 | 类型 |
| --- | --- | --- |
| delta.x | 相对于上次更新的水平位移。向右为正，向左为负。 | float |
| delta.y | 相对于上次更新的垂直位移。向下为正，向上为负。 | float |
| fingers | 手指数量（2–9） | int |
| rotation | 相对于上次更新，各手指构成的图形所转过的角度。顺时针为正，逆时针为负。手势类型不是 `pinch` 时，值为 `Nil`。 | float |
| scale | 相对于手势开始时，各手指构成的图形的大小变化量。手指张开为正，捏合为负。手势类型不是 `pinch` 时，值为 `Nil`。 | float |
| time_ms | 事件发生时的时间戳，从系统启动时开始计算。 | int |
| type | 取值为 `swipe` 或 `pinch`。 | string |

`finish` 方法会收到一个包含以下字段的表：

| 字段 | 说明 | 类型 |
| --- | --- | --- |
| cancelled | 如果后端异常终止了手势，则为真，否则为假。 | bool |
| time_ms | 事件发生时的时间戳，从系统启动时开始计算。 | int |
| type | 取值为 `swipe` 或 `pinch`。 | string |


<details><summary>示例</summary>


```lua
-- 用四指上滑运行 Lua 匿名函数，打开终端：
hl.gesture({ fingers = 4, direction = "up", action = function() hl.exec_cmd("kitty") end })

-- 按住 SUPER 时用四指下滑切换特殊工作区，绕过抑制器：
hl.gesture({ fingers = 4, direction = "down", mods = "SUPER", action = "special", workspace_name = "scratchpad", disable_inhibit = true })

-- 通过捏合手势以光标为中心缩放，使用缩放倍率而非固定缩放级别：
hl.gesture({ fingers = 2, direction = "pinchin", action = "cursor_zoom", zoom_level = 2.0, mode = "mult" })

-- 将所有事件以通知形式输出，以供测试
hl.gesture({
    fingers = 3,
    direction = "horizontal",
    action = {
        start = function(e) hl.notification.create({ text = "start: type=" .. e.type .. " time_ms=" .. e.time_ms .. " fingers=" .. e.fingers .. " delta=(" .. e.delta.x .. ", " .. e.delta.y .. ")", timeout = 1000, icon = 1}) end,
        update = function(e) hl.notification.create({ text = "update: type=" .. e.type .. " time_ms=" .. e.time_ms .. " fingers=" .. e.fingers .. " delta=(" .. e.delta.x .. ", " .. e.delta.y .. ")", timeout = 1000, icon = 1}) end,
        finish = function(e) hl.notification.create({ text = "finish: type=" .. e.type .. " time_ms=" .. e.time_ms .. " cancelled=" .. tostring(e.cancelled), timeout = 1000, icon = 1}) end
    }
})

-- 将所有事件以通知形式输出，以供测试
hl.gesture({
    fingers = 3,
    direction = "pinch",
    action = {
        start = function(e) hl.notification.create({ text = "start: type=" .. e.type .. " time_ms=" .. e.time_ms .. " fingers=" .. e.fingers .. " delta=(" .. e.delta.x .. ", " .. e.delta.y .. ") scale=" .. e.scale .. " rotation=" .. e.rotation, timeout = 1000, icon = 1}) end,
        update = function(e) hl.notification.create({ text = "update: type=" .. e.type .. " time_ms=" .. e.time_ms .. " fingers=" .. e.fingers .. " delta=(" .. e.delta.x .. ", " .. e.delta.y .. ") scale=" .. e.scale .. " rotation=" .. e.rotation, timeout = 1000, icon = 1}) end,
        finish = function(e) hl.notification.create({ text = "finish: type=" .. e.type .. " time_ms=" .. e.time_ms .. " cancelled=" .. tostring(e.cancelled), timeout = 1000, icon = 1}) end
    }
})

-- 调节音量
local volume_gesture = function(change) hl.exec_cmd("wpctl set-volume @DEFAULT_AUDIO_SINK@ " .. math.abs(change) .. "%" .. (change<0 and "-" or "+")) end
hl.gesture({
    fingers = 3,
    direction = "vertical",
    action = {
        start = function(e) volume_gesture(-0.25 * e.delta.y) end,
        update = function(e) volume_gesture(-0.25 * e.delta.y) end
    }
})
```



</details>
