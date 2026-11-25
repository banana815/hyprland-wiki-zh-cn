# 主从布局

主从布局将一个或多个窗口设为“主窗口”，默认占据屏幕左侧，其余窗口平铺在右侧。如果想使用默认左右分割以外的排列方式，可以为每个工作区单独设置布局方向。

<video width="1024" height="566" autoplay muted loop>
  <source src="https://dl.hypr.land/wiki/demo_master.mp4" type="video/mp4">
</video>

<a id="config"></a>

## 配置

类别：`master`

| 名称 | 说明 | 类型 | 默认值 | 范围 |
| --- | --- | --- | --- | --- |
| allow_small_split | 允许以水平分割的方式添加更多主窗口 | bool | `false` |  |
| mfact | 主窗口所占的屏幕比例。例如，`mfact = 0.70` 表示主窗口占屏幕的 70%，从窗口占 30%。 | float | `0.55` | [0 - 1] |
| new_status | `"master"` 表示将新窗口设为主窗口，`"slave"` 表示将新窗口加入从窗口栈，`"inherit"` 表示新窗口继承当前焦点窗口的主从角色。 | string | `"slave"` |  |
| new_on_top | 是否将新打开的窗口放在栈顶 | bool | `false` |  |
| new_on_active | `"before"`、`"after"` 表示将新窗口分别放在当前焦点窗口之前或之后，`"none"` 表示根据 `new_on_top` 的值放置新窗口。 | string | `"none"` |  |
| orientation | 主区域的默认位置 | string | `"left"` | `"left"`, `"right"`, `"top"`, `"bottom"`, `"center"` |
| slave_count_for_center_master | 使用 orientation=center 时，只有当打开的从窗口数量达到此值时，才将主窗口居中。（设为 0 表示始终将主窗口居中。） | int | `2` | [0 - 10] |
| center_master_fallback | 设置主窗口采用居中布局时，从窗口数量少于 `slave_count_for_center_master` 时使用的后备布局方向 | string | `"left"` | `"left"`, `"right"`, `"top"`, `"bottom"` |
| smart_resizing | 启用后，调整窗口大小的方向取决于鼠标在窗口内的位置（离哪个角最近）。否则，该方向取决于窗口在平铺布局中的位置 | bool | `true` |  |
| drop_at_cursor | 启用后，拖放窗口会将其放在光标所在的位置。否则，将窗口拖放到窗口栈一侧时，窗口会根据 new_on_top 的值放在栈顶或栈底。 | bool | `true` |  |
| always_keep_position | 没有从窗口时，是否将主窗口保留在配置指定的位置 | bool | `false` |  |
| focus_master_on_close | 启用后，关闭窗口时焦点会移到主窗口。 | bool | `false` |  |

<a id="layout-messages"></a>

## 布局消息

调度器 `hl.dsp.layout()` 的参数：

| 命令 | 说明 | 参数 |
| --- | --- | --- |
| addmaster | 向主区域添加一个主窗口。如果活动窗口不是主窗口，则将其设为主窗口；否则，将第一个非主窗口设为主窗口。 | 无 |
| cyclenext | 按布局顺序将焦点移到下一个窗口 | 可选 `loop`（允许焦点从栈底循环回到主窗口）或 `noloop`（焦点移到栈底即停止，与 DWM 相同）。留空时默认为 `loop`。 |
| cycleprev | 按布局顺序将焦点移到上一个窗口 | 可选 `loop`（允许焦点从主窗口循环到栈底）或 `noloop`（焦点移到主窗口即停止，与 DWM 相同）。留空时默认为 `loop`。 |
| focusmaster | 将焦点移到主窗口 | 可选 `master`（焦点停留在主窗口）、`auto`（默认值；如果焦点已在主窗口，则移到第一个非主窗口）或 `previous`（将焦点移到主窗口时记住当前窗口；如果焦点已在主窗口，则返回之前的窗口，无法返回时按 `auto` 处理）。 |
| mfact | 更改主区域的分割比例 mfact | 新的分割比例，可用浮点增量表示（例如 `-0.2`、`+0.2`），也可用 `exact` 后接 0.0 到 1.0 之间的数值表示。 |
| orientationbottom | 将当前工作区的布局方向设为 bottom（主区域在下方，从窗口在上方横向排列） | 无 |
| orientationcenter | 将当前工作区的布局方向设为 center（主区域居中，从窗口交替放在左右两侧，每侧纵向排列） | 无 |
| orientationcycle | 在给定的方向列表中循环切换，将当前工作区设为列表中的下一个方向 | 可用值为 `left`、`top`、`right`、`bottom` 或 `center`。各值之间必须用空格分隔。留空时，行为与 `orientationnext` 相同。 |
| orientationleft | 将当前工作区的布局方向设为 left（主区域在左侧，从窗口在右侧纵向排列） | 无 |
| orientationnext | 按顺时针方向将当前工作区的布局循环切换到下一个方向 | 无 |
| orientationprev | 按逆时针方向将当前工作区的布局循环切换到上一个方向 | 无 |
| orientationright | 将当前工作区的布局方向设为 right（主区域在右侧，从窗口在左侧纵向排列） | 无 |
| orientationtop | 将当前工作区的布局方向设为 top（主区域在上方，从窗口在下方横向排列） | 无 |
| removemaster | 从主区域移出一个主窗口。如果活动窗口是主窗口，则移出该窗口；否则，移出最后一个主窗口。 | 无 |
| rollnext | 将栈中的下一个窗口轮换为主窗口，并让焦点保持在主窗口上 | 无 |
| rollprev | 将栈中的上一个窗口轮换为主窗口，并让焦点保持在主窗口上 | 无 |
| swapnext | 按布局顺序将当前焦点窗口与下一个窗口交换位置 | 可选 `loop`（允许栈底窗口与主窗口交换位置）或 `noloop`（禁止这种交换，与 DWM 相同）。留空时默认为 `loop`。 |
| swapprev | 按布局顺序将当前焦点窗口与上一个窗口交换位置 | 可选 `loop`（允许主窗口与栈底窗口交换位置）或 `noloop`（禁止这种交换，与 DWM 相同）。留空时默认为 `loop`。 |
| swapwithmaster | 将当前窗口与主窗口交换位置。如果当前窗口就是主窗口，则将其与第一个子窗口交换位置。 | 可选 `master`（焦点移到新的主窗口）、`child`（焦点移到新的子窗口）或 `auto`（默认值，焦点保持在交换前拥有焦点的窗口上）。加上 `ignoremaster` 后，如果主窗口已拥有焦点，则忽略此调度器。 |

命令的各个参数之间用一个空格分隔。

> [!NOTE]
> 用法示例：
>
> ```lua
> hl.bind(KEYS, hl.dsp.layout("cyclenext"))
> -- behaves like xmonads promote feature (https://hackage.haskell.org/package/xmonad-contrib-0.17.1/docs/XMonad-Actions-Promote.html)
> hl.bind(KEYS, hl.dsp.layout("swapwithmaster master"))
> ```

<a id="workspace-rules"></a>

## 工作区规则

`layout_opts` 规则：

| 规则 | 说明 | 类型 |
| --- | --- | --- |
| orientation = [o] | 设置工作区的布局方向。可用方向见[布局方向](#config)。 | string |

用法示例：

```lua
hl.workspace_rule({ workspace = "2", layout_opts =  { orientation = "top" } })
```
