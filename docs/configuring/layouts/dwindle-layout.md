# Dwindle 布局

Dwindle 是一种类似 BSPWM 的布局，工作区中的每个窗口都是一棵二叉树中的节点。

<video width="1024" height="566" autoplay muted loop>
  <source src="https://dl.hypr.land/wiki/demo_dwindle.mp4" type="video/mp4">
</video>

<a id="quirks"></a>

## 兼容性调整

Dwindle 的分割方向并不固定，而是根据父节点的宽高比（W/H）动态决定。如果 W > H，则左右排列；如果 H > W，则上下排列。启用 `preserve_split` 可以固定分割方向。

<a id="config"></a>

## 配置

类别：`dwindle`

| 名称 | 说明 | 类型 | 默认值 | 范围 |
| --- | --- | --- | --- | --- |
| force_split | 0 - 根据鼠标位置决定分割方向；1 - 始终向左分割（新窗口位于左侧或上方）；2 - 始终向右分割（新窗口位于右侧或下方） | int | `0` | [0 - 2] |
| preserve_split | 启用后，无论容器如何变化，分割方向（左右排列或上下排列）都保持不变 | bool | `false` |  |
| smart_split | 启用后，可以根据光标位置更精确地控制窗口的分割方向。可将窗口想象成四个三角形，光标所在的三角形决定分割方向。此功能还会启用 `preserve_split` | bool | `false` |  |
| smart_resizing | 启用后，调整窗口大小的方向取决于鼠标在窗口内的位置（离哪个角最近）。否则，该方向取决于窗口在平铺布局中的位置 | bool | `true` |  |
| permanent_direction_override | 启用后，预选的分割方向会一直生效，直到关闭此模式、指定其他方向，或指定不表示方向的值（即 `l`、`r`、`u`/`t`、`d`/`b` 以外的任何值） | bool | `false` |  |
| split_width_multiplier | 指定自动分割时使用的宽度乘数。在宽屏显示器上，即使经过多次分割，窗口仍可能满足 W > H，此时用乘数调整参与计算的窗口宽度很有用 | float | `1.0` | [0.1 - 3.0] |
| use_active_for_splits | 分割时优先依据活动窗口还是鼠标位置 | bool | `true` |  |
| default_split_ratio | 打开窗口时使用的默认分割比例。1 表示按 50/50 等分 | float | `1.0` | [0.1 - 1.9] |
| split_bias | 指定分割比例应用于哪个窗口。0 - 按方向选择（上方或左侧的窗口）；1 - 当前窗口 | int | `0` | [0 - 1] |
| precise_mouse_move | 拖放窗口时，根据鼠标所在位置更精确地放置窗口 | bool | `false` |  |

<a id="dispatchers"></a>

## 调度器

| 调度器 | 说明 | 参数 |
| --- | --- | --- |
| window.pseudo | 切换指定窗口的伪平铺模式 | 留空或设为 `"active"` 表示当前窗口，设为 `"window"` 表示特定窗口 |  |

<a id="layout-messages"></a>

## 布局消息



调度器 `hl.dsp.layout()` 的参数：

| 参数 | 说明 | 参数 |
| --- | --- | --- |
| movetoroot | 将窗口移至工作区布局树的根节点。参见[下方说明](#movetoroot) | window?, "unstable"? |
| preselect | 一次性覆盖分割方向，仅对下一个打开的窗口生效，且只适用于平铺窗口 | direction |
| rotatesplit | 按指定角度旋转当前窗口的分割方向，角度参数可省略。角度必须是 90 的倍数，正值表示顺时针，负值表示逆时针 | int? = 90 |
| splitratio | 更改分割比例。参见[下方说明](#splitratio) | float |
| swapsplit | 交换当前窗口所在分割的两个部分 | 无 |
| togglesplit | 切换当前窗口的分割方向（上下或左右）。必须启用 `preserve_split` 才能切换。 | 无 |

<a id="movetoroot"></a>

### movetoroot

将指定窗口移到工作区中离它最近的根节点下，使其成为该节点的直接子节点。如果窗口已经是该根节点的直接子节点，则发出警告。

默认行为是“稳定的”，即拥有焦点的窗口会留在屏幕的同一侧。将 `unstable` 作为第二个参数传入，则会交换根节点的两个直接子节点的位置（即它们各自在屏幕上所占的一侧）。

请注意，`movetoroot unstable` *无效*，正确的写法是 `movetoroot active unstable`。

<a id="splitratio"></a>

### splitratio

`splitratio` 默认将数值作为增量使用。在数值后加上 `exact` 即可直接设置分割比例。增量默认为正。要指定调整方向，请在数值前加上正号（`+`）或负号（`-`）。

超出 [0.1 - 1.9] 范围的值会被限制为最近的边界值。


<details><summary>示例</summary>


```lua
-- 对窗口类为 "imcool" 的窗口使用 movetoroot
hl.bind("SUPER + A", hl.dsp.layout("movetoroot class:imcool"))

hl.bind("SUPER + A", hl.dsp.layout("togglesplit"))

-- 将分割比例设为 1.2
hl.bind("SUPER + A", hl.dsp.layout("splitratio 1.2 exact"))

-- 在上一次调度后将分割比例设为 0.8
hl.bind("SUPER + A", hl.dsp.layout("splitratio -0.4"))
```



</details>
