# 滚动布局

在滚动布局中，窗口沿着一条可无限延伸的滚动带排列。

<video width="1024" height="566" autoplay muted loop>
  <source src="https://dl.hypr.land/wiki/demo_scrolling.mp4" type="video/mp4">
</video>

<a id="config"></a>

## 配置

类别：`scrolling`

| 名称 | 说明 | 类型 | 默认值 | 范围 |
| --- | --- | --- | --- | --- |
| fullscreen_on_one_column | 启用后，如果工作区只有一列，该列将始终占满整个屏幕。 | bool | `true` |  |
| column_width | 列的默认宽度 | float | `0.5` | [0.1 - 1.0] |
| focus_fit_method | 列获得焦点时，使其进入视野所采用的方式。0 对应 center（居中），1 对应 fit（使整列可见），2 对应 clamped_center（在边界限制内居中）。 | int | `1` | [0 - 2] |
| follow_focus | 窗口获得焦点时滚动带的行为。0：焦点变化不会使滚动带移动。1：焦点变化可能使滚动带移动，鼠标点击总会使滚动带移动。2：焦点变化可能使滚动带移动。 | int | `1` | [0 - 2] |
| follow_min_visible | 窗口获得焦点时，只有当窗口的可见比例达到指定值，视图才会跟随焦点。通过按键绑定、点击等直接输入切换焦点时，视图始终跟随。 | float | `0.4` | [0.0 - 1.0] |
| explicit_column_widths | 以逗号分隔的预设宽度列表，供 `colresize +conf/-conf` 使用 | string | `"0.333, 0.5, 0.667, 1.0"` |  |
| wrap_focus | 启用后，`hl.dsp.layout("focus l/r")` 可在首尾两端循环切换焦点。 | bool | `true` |  |
| wrap_swapcol | 启用后，`hl.dsp.layout("swapcol l/r")` 可跨越首尾边界交换列。 | bool | `true` |  |
| direction | 新窗口出现的方向及布局滚动的方向。可选值为 `"left"`/`"right"`/`"down"`/`"up"`。 | string | `"right"` |  |

<a id="workspace-rules"></a>

## 工作区规则

| 名称 | 说明 | 类型 |
| --- | --- | --- |
| direction | 与 `scrolling.direction` 配置选项相同，可按工作区单独设置。 | string |

例如：

```lua
hl.workspace_rule({ workspace = "2", layout_opts = { direction = "right" } })
```

<a id="layout-messages"></a>

## 布局消息

调度器 `hl.dsp.layout()` 的参数：

| 名称 | 说明 | 参数 |
| --- | --- | --- |
| center | 将当前拥有焦点的列居中 | 无 |
| colresize | 调整当前列的宽度。可以指定目标宽度或相对变化量（例如 `0.5`、`+0.2`、`-0.2`），也可以用 `+conf` 或 `-conf` 循环切换预设宽度。还可以使用 `all (number)` 将所有列设为指定宽度。 | 相对浮点值或相对 `conf` 步进值 |
| consume | 将当前窗口移入上一列 | 无 |
| consume_or_expel | 如果当前列还有其他窗口，则将当前窗口移出并单独成列；如果当前列只有这一个窗口，则从相邻列并入一个窗口。 | `prev` 或 `next` |
| expel | 将当前窗口移到单独的新列中（如果窗口位于屏幕上半部分，则向后移动，否则向前移动） | 无 |
| fit | 根据参数执行适配操作。可用值为 `active`、`visible`、`all`、`toend`、`tobeg`、`expand`。`expand` 会扩展当前窗口，使其占满显示器上剩余的可用空间。 | 适配模式 |
| fit_into_view | 使当前活动列完整显示在视野中 | 无 |
| focus | 移动焦点并使布局居中。到达边界时，焦点会循环到另一端，不会移到相邻显示器。 | direction |
| inhibit_scroll | 禁止当前活动工作区的滚动视图移动。每个工作区的开关彼此独立。 | 留空表示切换状态，也可使用 `bool` 显式启用或禁用。 |
| move | 水平移动布局，可按相对逻辑像素数（`-200`、`+200`）或按列（`+col`、`-col`）移动。 | 移动参数 |
| promote | 将窗口向前移到单独的新列中 | 无 |
| swapcol | 将当前列与左侧（`l`）或右侧（`r`）的相邻列交换。交换时首尾相接（例如，将第一列向左交换会使其移至末尾）。 | `l` 或 `r` |

Hyprland 配置中的按键绑定示例：

```lua
hl.bind(mainMod .. " + period", hl.dsp.layout("move +col"))
hl.bind(mainMod .. " + comma", hl.dsp.layout("swapcol l"))
```

<a id="convenience-functions"></a>

## 便捷函数

- `hl.get_scrolling_offset()`
- `hl.set_scrolling_offset(double)`

可通过 LSP 查看返回值，也可以自行查阅存根文件。要在代码编辑器中配置 LSP，请参阅[此处](../core/_index.md#editor-autocompletion)。

<a id="window-rules"></a>

## 窗口规则

使用静态规则 scrolling_width 可以为窗口设置初始列宽。

```lua
hl.window_rule({ name = "kitty_starting_width", match = { class = "kitty" }, scrolling_width = 0.5})
```

<a id="layout-handled-fullscreen"></a>

## 由布局处理的全屏模式

滚动布局提供一种可选的全屏模式，由布局自身的全屏处理器控制。在这种模式下，你可以滚动到其他位置，全屏窗口仍会保持全屏状态。

在采用滚动布局的工作区中，调用全屏调度器时设置 `layout_aware = true`（或直接省略 `layout_aware` 选项）即可使用此模式。此模式也支持现有的窗口和工作区全屏状态选择器。

> [!NOTE]
> 当全屏窗口获得焦点时，`hl.dsp.focus({ direction })` 调度器默认会在指定方向上查找其他显示器，而不会在当前显示器上切换窗口。要使用布局提供的滚动功能离开全屏窗口，可以设置 `binds.movefocus_cycles_fullscreen = true`，让焦点调度器恢复查找窗口的行为，也可以改用滚动布局的 `focus` 布局消息。

有关全屏处理器的更多信息，请参阅[此处](../core/dispatchers.md#fullscreen-handlers)。
