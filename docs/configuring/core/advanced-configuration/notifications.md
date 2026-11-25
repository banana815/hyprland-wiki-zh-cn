# 通知

Hyprland 内置了一个简单的通知系统。通知以简单的文本框形式显示在当前活动显示器的右上角，可选择附带图标。**这些通知并非用于处理系统通知。**

<a id="parameters"></a>

## 参数

| 名称 | 说明 | 类型 | 默认值 | 范围 |
| --- | --- | --- | --- | --- |
| text | 通知文本 | string | [[Empty]] |  |
| timeout | 超时时间（即通知显示时长），单位为毫秒 | int | [[Required]] |  |
| icon | 图标类型，参见[下方的图标说明](#icon) | string | `"none"` |  |
| color | 通知颜色。`0` 表示使用该图标的默认颜色 | color | 0 |  |
| font_size | 显示通知时使用的字号 | int | 13 |  |

<a id="icon"></a>

### 图标

可用的图标如下，可通过 Lua 名称或 hyprctl ID 选择：

| 名称 | Lua 名称 | hyprctl ID | 默认颜色 |
| --- | --- | --- | --- |
| 无 | none | -1 | <code style="background-color:#000000;color:#FFFFFF">#000000</code> |
| 警告 | warn/warning | 0 | <code style="background-color:#FFCC66;color:#000000">#FFCC66</code> |
| 信息 | info | 1 | <code style="background-color:#80FFFF;color:#000000">#80FFFF</code> |
| 提示 | hint | 2 | <code style="background-color:#B3FFCC;color:#000000">#B3FFCC</code> |
| 错误 | err/error | 3 | <code style="background-color:#FF4D4D;color:#000000">#FF4D4D</code> |
| 困惑 | confused/question | 4 | <code style="background-color:#FFCC99;color:#000000">#FFCC99</code> |
| 成功 | ok | 5 | <code style="background-color:#80FF80;color:#000000">#80FF80</code> |

<a id="creating-a-notification"></a>

## 创建通知

<a id="lua"></a>

### Lua

```lua
-- 直接推送一条通知
hl.notification.create({ text = "Hello from Lua!", timeout = 15000, icon = "info", font_size = 20 })

-- 将 "HL.Notification" 对象赋给 "somevar" 以供后续使用，并推送该通知
local somevar = hl.notification.create({ text = "Please store me", timeout = 228638, icon = "hint" })

-- 获取包含所有活动通知的表，其中每条通知都是一个 "HL.Notification" 对象
hl.notification.get()
```

<a id="hyprctl"></a>

### Hyprctl

要通过 hyprctl 创建通知，可以使用 `hyprctl notify` 命令。它所需的信息与 `hl.notification.create()` 相同，只是格式略有不同。详情请见[此处](using-hyprctl.md#notify)。
