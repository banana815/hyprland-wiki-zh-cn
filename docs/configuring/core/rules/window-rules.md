# 窗口规则

<a id="syntax"></a>

## 语法

```lua
hl.window_rule({
    name? = string,
    match = {
        prop = some_prop_value,
    },
    effect = some_effect_value,
})
```

<a id="window-rules"></a>

## 窗口规则

可以设置窗口规则，根据窗口属性为不同窗口指定不同的行为。

<a id="props"></a>

### 匹配属性

`match` 表支持以下字段：

| 属性 | 说明 | 类型 |
| --- | --- | --- |
| class | `class` 与 `RegEx` 匹配的窗口 | [RegEx] |
| content | 具有指定内容类型（none、photo、video、game）的窗口 | string |
| focus | 当前获得焦点的窗口 | bool |
| fullscreen | 全屏窗口（包括覆盖式和非覆盖式） | bool |
| fullscreen_state_client | `fullscreenstate` 匹配的窗口。`0` - 无，`1` - 最大化，`2` - 全屏，`3` - 同时最大化和全屏 | int |
| fullscreen_state_internal | `fullscreenstate` 匹配的窗口。`0` - 无，`1` - 最大化，`2` - 全屏，`3` - 同时最大化和全屏 | int |
| float | 浮动窗口 | bool |
| group | 已加入窗口组的窗口 | bool |
| initial_class | `initialClass` 与 `RegEx` 匹配的窗口 | [RegEx] |
| initial_title | `initialTitle` 与 `RegEx` 匹配的窗口 | [RegEx] |
| modal | 模态窗口（例如询问“是否确定”的弹窗） | bool |
| pin | 固定窗口（即在所有工作区上显示该窗口）。**重要：非浮动窗口会忽略固定设置** | bool |
| tag | `tag` 匹配的窗口 | string |
| title | `title` 与 `RegEx` 匹配的窗口 | [RegEx] |
| workspace | 位于匹配工作区中的窗口 | 工作区选择器 |
| xdg_tag | 根据窗口的 xdgTag 匹配窗口 | [RegEx] |
| xwayland | Xwayland 窗口 | bool |

<a id="effects"></a>

## 效果

<a id="static-effects"></a>

### 静态效果

> [!WARNING]
> 窗口创建后，无法根据 `title` 的变化对窗口应用 `float` 或其他静态规则。此限制适用于这里列出的所有静态效果。
>
> 请改用[事件](../advanced-configuration/events.md)监听器触发一次[调度调用](../dispatchers.md)，在窗口创建后应用该效果：
> ```lua
> hl.on("window.title", function(w)
>     if w ~= nil and w.title == "foo" then
>         hl.dispatch(hl.dsp.window.float({ action = "set" }))
>     end
> end)
> ```

静态效果只在窗口打开时求值一次，之后不会再次求值。因此，按 `title` 和 `class` 匹配时，实际匹配到的始终分别是 `initialTitle` 和 `initialClass`。

| 效果 | 说明 | 类型 |
| --- | --- | --- |
| center | 如果窗口为浮动窗口，则将其置于所在显示器的中央 | bool |
| content | 设置内容类型：`"none"`、`"photo"`、`"video"` 或 `"game"` | string |
| float | 使窗口浮动 | bool |
| fullscreen | 使窗口全屏显示 | bool |
| fullscreen_state | 设置内部客户端的全屏模式（例如 `"1 2"`）。可用值：`0` 表示无，`1` 表示最大化，`2` 表示全屏，`3` 表示同时最大化和全屏 | string |
| group | 设置窗口组属性。请参阅下文的[窗口组选项](#group-window-rule-options) | string |
| maximize | 使窗口最大化 | bool |
| monitor | 指定窗口应在哪台显示器上打开（例如 `"1"`、`"DP-1"`）。可在末尾追加 `" silent"` | string |
| move | 将浮动窗口移动到指定位置，坐标相对于所在显示器。请参阅下文的[位置和大小](#position-and-size) | table 或 string |
| no_close_for | 在窗口打开后的指定毫秒数内，禁止使用 `killactive` 关闭该窗口 | int |
| no_initial_focus | 禁止窗口在打开时获得初始焦点 | bool |
| pin | 固定窗口，使其显示在所有工作区上。_注意：固定设置对非浮动窗口无效。通常应与 `float = true` 配合使用。_ | bool |
| pseudo | 使窗口采用伪平铺模式 | bool |
| scrolling_width | 设置窗口在使用滚动布局的工作区中打开时所在列的宽度 | float |
| size | 调整浮动窗口的大小。参见下文的[位置和大小](#position-and-size) | table 或 string |
| suppress_event | 忽略指定事件。多个事件用空格分隔：`"fullscreen"`、`"maximize"`、`"activate"`、`"activatefocus"`、`"fullscreenoutput"`、`"x11configurerequest"` | string |
| tile | 平铺窗口 | bool |
| workspace | 设置窗口打开时所在的工作区。也可以设为 `"unset"`，或在工作区标识后追加 `" silent"` | string |

<a id="position-and-size"></a>

#### 位置和大小



位置和大小参数接受 Lua 表或字符串。每个值可以是数字或[表达式](#expressions)。字符串参数在第一个空白字符处分割。

只提供一个值、表中的元素个数不等于两个，或使用空白字符以外的分隔符（如 `"800,600"`、`"800x600"`），都会导致配置错误。

<a id="expressions"></a>

##### 表达式

表达式是表示基本信息的简写。所有位置变量都使用相对于显示器的坐标。在字符串参数中，表达式不能含有空格，否则无法正确解析。

- `monitor_w` 和 `monitor_h` 分别表示显示器的宽度和高度
- `window_x` 和 `window_y` 分别表示窗口的横坐标和纵坐标
- `window_w` 和 `window_h` 分别表示窗口的宽度和高度
- `cursor_x` 和 `cursor_y` 分别表示光标的横坐标和纵坐标


<details><summary>示例</summary>


```lua
-- 将尺寸设为 x = 800, y = 600
size = { 800, 600 }

-- 尺寸相同，但通过字符串指定
size = "800 600"

-- 将窗口中心移到光标位置
move = { "cursor_x - (window_w * 0.5)", "cursor_y - (window_h * 0.5)" }

-- 将窗口与显示器左边缘对齐，并置于显示器中心下方 17 像素处
move = { "window_w * 0.5", "(monitor_h / 2) + 17" }

-- 将窗口的宽和高分别设为显示器分辨率对应尺寸的一半
size = { "monitor_w * 0.5", "monitor_h * 0.5" }

-- 将 max_size 的宽和高分别设为显示器宽度和高度的一半
max_size = "monitor_w*0.5 monitor_h*0.5"
```



</details>

<a id="dynamic-effects"></a>

### 动态效果

每当属性发生变化时，都会重新计算动态效果。


| 效果 | 说明 | 参数 | 范围 |
| --- | --- | --- | --- |
| allows_input | 强制 Xwayland 窗口接收输入，即使窗口请求不接收输入 | bool |  |
| animation | 强制对窗口应用动画，可指定动画样式（如 `"popin"`、`"popin 80%"`） | string |  |
| border_color | 将窗口边框设为纯色或渐变色。参见下文的 [border_color 窗口规则](#border_color-window-rule) | gradient |  |
| border_size | 设置边框宽度 | int |  |
| confine_pointer | 将鼠标光标限制在窗口内。主要用于在游戏时将光标限制在一台显示器上 | bool |  |
| dim_around | 使窗口周围的一切变暗。此效果适用于浮动窗口 | bool |  |
| decorate | 是否绘制窗口装饰（默认值：`true`） | bool |  |
| focus_on_activate | 当应用请求获得焦点时，Hyprland 是否将焦点移至该应用 | bool |  |
| idle_inhibit | 设置阻止系统进入空闲状态的规则。可用模式：`"none"`、`"always"`、`"focus"`、`"fullscreen"` | string |  |
| immediate | 强制允许该窗口出现画面撕裂 | bool |  |
| keep_aspect_ratio | 使用鼠标调整窗口大小时强制保持宽高比 | bool |  |
| max_size | 设置浮动窗口的最大尺寸。参见上文的[位置和大小](#position-and-size) | 表或字符串 |  |
| min_size | 设置浮动窗口的最小尺寸。参见上文的[位置和大小](#position-and-size) | 表或字符串 |  |
| nearest_neighbor | 强制使用最近邻过滤 | bool |  |
| no_anim | 禁用该窗口的动画 | bool |  |
| no_auto_hdr | 禁用该窗口的 AutoHDR，可防止 `foot` 等程序在全屏时触发 AutoHDR | bool |  |
| no_blur | 禁用该窗口的模糊效果 | bool |  |
| no_dim | 禁用该窗口的变暗效果 | bool |  |
| no_focus | 禁止该窗口获得焦点 | bool |  |
| no_follow_mouse | 设置了 `input.follow_mouse=1` 时，阻止该窗口在鼠标移入时获得焦点 | bool |  |
| no_glow | 禁用该窗口的辉光效果 | bool |  |
| no_max_size | 移除窗口的最大尺寸限制 | bool |  |
| no_screen_share | 在屏幕共享画面中用黑色矩形遮住该窗口及其弹出窗口 | bool |  |
| no_shadow | 禁用该窗口的阴影 | bool |  |
| no_shortcuts_inhibit | 禁止应用屏蔽快捷键 | bool |  |
| no_vrr | 禁用该窗口的可变刷新率（VRR）。仅在 `misc.vrr` 设为 `2` 或 `3` 时生效 | bool |  |
| no_wobble | 禁用该窗口的晃动效果 | bool |  |
| no_xdg_drags | 设为 true 时，禁用该窗口由 XDG 驱动的拖动操作（如拖动客户端装饰的顶栏） | bool |  |
| opacity | 设置额外的不透明度乘数（例如，`"0.8"` 用于所有状态，`"0.9 0.7"` 分别用于活动和非活动状态，`"1.0 0.8 0.9"` 分别用于活动、非活动和全屏状态）。在每个值后追加 `" override"`，即可将该值用作绝对不透明度，而非乘数 | string |  |
| opaque | 将该窗口的 `decoration.active/inactive/fullscreen_opacity` 设为 `1` | bool |  |
| force_rgbx | 禁用窗口自身的透明效果*（与 opaque 规则不同，此设置不影响 Hyprland 为窗口指定的透明度）* | bool |  |
| persistent_size | 在内部保存浮动窗口的大小。打开类名和标题均相同的新浮动窗口时，恢复已保存的大小 | bool |  |
| render_unfocused | 即使窗口不可见，也强制让它认为自身正在被渲染 | bool |  |
| rounding | 强制将圆角半径设为 X 像素，忽略默认值 | int / `{ top_left?, top_right?, bottom_left?, bottom_right?}` |  |
| rounding_power | 覆盖该窗口的圆角曲线指数 | float |  |
| scroll_mouse | 强制该窗口覆盖 `input.scroll_factor` 的设置 | float |  |
| scroll_touchpad | 强制该窗口覆盖 `input.touchpad.scroll_factor` 的设置 | float |  |
| stay_focused | 只要该窗口可见，就强制它保持焦点 | bool |  |
| sync_fullscreen | 实际使用的全屏模式是否应始终与发送给窗口的全屏模式一致 | bool |  |
| tag | 应用标签。使用前缀 `+` 添加标签，使用 `-` 移除标签，省略前缀则切换标签状态（如 `"+myTag"`） | string |  |
| tonemap | 色调映射方式：`on` 启用色调映射（默认），`off` 禁用色调映射，`clamp` 将源亮度限制在目标亮度范围内，`limited` 使用动态曲线，仅对超出目标亮度上限的高亮部分进行色调映射 | string |  |
| xray | 设置该窗口的模糊效果 xray 模式 | bool |  |

所有动态效果都可以通过 [`set_prop()`](../dispatchers.md#set_prop) 设置。

<a id="group-window-rule-options"></a>

### `group` 窗口规则选项

`group` 效果接受一个字符串，其中的选项用空格分隔：

- `"barred"` - 禁止将窗口自动加入当前拥有焦点且未锁定的组。
- `"deny"` - 禁止将窗口切换为组或加入已有的组。
- `"invade"` - 强制在已锁定的组中打开窗口。
- `"lock"` [`"always"`] - 锁定组。与 `"set"` 或 `"new"` 配合使用。
- `"new"` - `"barred set"` 的简写。
- `"override"` [其他选项] - 覆盖其他 `group` 规则。
- `"set"` [`"always"`] - 将窗口作为一个组打开。
- `"unset"` - 清除所有 `group` 规则。

> [!NOTE]
> 不带选项的 `group` 是 `group = "set"` 的简写。
>
> 默认情况下，`set` 和 `lock` 仅对新窗口生效一次。使用 `always` 限定符可使它们持续生效。

<a id="border_color-window-rule"></a>

### `border_color` 窗口规则

`border_color` 规则接受单一颜色或渐变色：

```lua
-- 单色
border_color = "rgb(FF0000)"
-- 渐变色
border_color = { colors = { "rgba(33ccffee)", "rgba(00ff99ee)" }, angle = 45 }
```

`border_color` 规则也可以与 `focus` 属性配合使用，分别设置窗口在活动和非活动状态下的边框颜色。例如：

```lua
-- 将 Firefox 非活动窗口的边框颜色设为从品红到青色的渐变
hl.window_rule(
    match = { class = "firefox", focus = false },
    border_color = { colors = { "rgba(ffff00ee)", "rgba(00ffffee)" }, angle = 33 }
)
```

> [!TIP]
> 组合使用两条规则，一条设置 `focus = true`，另一条设置 `focus = false`，即可分别指定特定窗口在活动和非活动状态下的边框颜色（类似于 `general.col.active_border` 和 `general.col.inactive_border` 通常对窗口起到的作用）。

<a id="tags"></a>

### 标签

窗口标签分为静态标签和动态标签。动态标签带有 `*` 后缀。使用 `hyprctl clients` 可查看窗口标签。

使用 `hl.dsp.window.tag` 调度器添加静态标签，使用 `tag` 窗口规则添加动态标签。

`tag` 规则只能操作动态标签，`hl.dsp.window.tag` 只能操作静态标签（调用该调度器时会清除动态标签）。


<details><summary>示例</summary>


```bash
hyprctl dispatch 'hl.dsp.window.tag({ tag = "+code" })' # 为当前窗口添加标签。
hyprctl dispatch 'hl.dsp.window.tag({ tag = "-code" })' # 从当前窗口移除标签。
hyprctl dispatch 'hl.dsp.window.tag({ tag = "code" })'  # 切换当前窗口的标签。

# 也可以指定目标窗口
hyprctl dispatch 'hl.dsp.window.tag({ tag = "+music", window = "class:Celluloid" })'
```

```lua
-- 将 kitty 移至 100 100，并设置动画样式（命名规则）
hl.window_rule({
  name      = "move-kitty",
  match     = { class = "kitty" },
  move      = {100, 100},
  animation = "popin",
})

-- 为 firefox 禁用模糊效果
hl.window_rule({ match = { class = "firefox" }, no_blur = true })

-- 将 kitty 窗口的中心移到光标位置
hl.window_rule({
  match = { class = "kitty" },
  move  = {"cursor_x-(window_w*0.5)", "cursor_y-(window_h*0.5)"},
})

-- 窗口全屏时将边框颜色设为红色
hl.window_rule({
  match        = { fullscreen = true },
  border_color = "rgb(FF0000) rgb(880808)",
})

-- 标题包含 Hyprland 时将边框颜色设为黄色
hl.window_rule({
  match        = { title = ".*Hyprland.*" },
  border_color = "rgb(FFFF00)",
})

-- 将 kitty 的不透明度设为活动时 1.0、非活动时 0.5、全屏时 0.8
hl.window_rule({
  match   = { class = "kitty" },
  opacity = "1.0 override 0.5 override 0.8 override",
})

-- 将 kitty 的圆角半径设为 10
hl.window_rule({ match = { class = "kitty" }, rounding = 10 })

-- 修复 pinentry 丢失焦点的问题
hl.window_rule({
  match        = { class = "(pinentry-)(.*)" },
  stay_focused = true,
})

hl.window_rule({ match = { class = "footclient" }, tag = "+term" })   -- 添加动态标签 `term*`
hl.window_rule({ match = { class = "footclient" }, tag = "term" })    -- 切换动态标签 `term*`
hl.window_rule({ match = { tag = "cpp" },          tag = "+code" })   -- 为带有 `cpp` 标签的窗口添加 `code*`
hl.window_rule({ match = { tag = "code" },         opacity = "0.8" }) -- 为带有 `code` 或 `code*` 标签的窗口设置不透明度
hl.window_rule({ match = { tag = "cpp" },          opacity = "0.7" }) -- `cpp`-tagged windows match both; last wins
hl.window_rule({ match = { tag = "term*" },        opacity = "0.6" }) -- 仅匹配 `term*`，不匹配不带星号的 `term`
hl.window_rule({ match = { tag = "term" },         tag = "-code" })   -- 从带有 `term`/`term*` 标签的窗口移除动态标签 `code*`

-- 也可以使用按键绑定
hl.bind("SUPER + CTRL + 2", hl.dsp.window.tag({ tag = "alpha_0.2" }))
hl.bind("SUPER + CTRL + 4", hl.dsp.window.tag({ tag = "alpha_0.4" }))
hl.window_rule({ match = { tag = "alpha_0.2" }, opacity = "0.2 override" })
hl.window_rule({ match = { tag = "alpha_0.4" }, opacity = "0.4 override" })
```



</details>

<a id="notes"></a>

### 注意事项

每当窗口用于匹配规则的属性发生变化时，都会重新计算标记为_动态_的效果。例如，如果某条规则在窗口浮动时更改其 `border_color`，那么当窗口恢复平铺时，边框颜色也会恢复为默认值。

效果按从上到下的顺序处理，_最后_匹配的规则优先。

在这个例子中，所有非全屏的 kitty 窗口都应用 `opacity 0.8`，其中浮动窗口的不透明度则为 `0.5`。其他所有浮动窗口的不透明度也为 `0.5`。

```lua
hl.window_rule({ match = { float = true },    opacity = "0.5 override 0.5 override" })
hl.window_rule({ match = { class = "kitty" }, opacity = "0.8 override 0.8 override" })
```

<a id="dynamically-enabling--disabling--changing-rules"></a>

### 动态启用、禁用或更改规则

只有具名规则才能动态更改、启用或禁用。`hl.window_rule()` 返回一个句柄对象：

```lua
local myRule = hl.window_rule({
  name        = "my-rule",
  match       = { class = "kitty" },
  border_size = 5,
})

myRule:set_enabled(false)  -- 禁用
myRule:set_enabled(true)   -- 重新启用
myRule:is_enabled()        -- 查询状态
```
