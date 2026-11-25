# 工作区规则

可以通过工作区规则为特定工作区设置专属行为。例如，可以定义一个工作区，让其中所有窗口都以无边框、无间隙的方式显示。

某些布局有专用规则，可在相应的布局页面中查阅。参见[布局](../../layouts/_index.md)。

<a id="syntax"></a>

## 语法

```lua
hl.workspace_rule({
    workspace = workspace_selector,
    rule1 = some_value,
    rule2 = other_value,
})
```

<a id="rules"></a>

## 规则


| 规则 | 说明 | 类型 | 范围 |
| --- | --- | --- | --- |
| animation | 此工作区使用的动画样式 | string |  |
| border_size | 设置窗口边框的宽度 | int |  |
| decorate | 是否绘制窗口装饰 | bool |  |
| default_name | 工作区的默认名称 | string |  |
| float_gaps | 设置浮动窗口的间距 | css_gaps |  |
| gaps_in | 设置窗口之间的间距 | css_gaps |  |
| gaps_out | 设置窗口与显示器边缘之间的间距 | css_gaps |  |
| layout | 此工作区使用的布局 | string |  |
| layout_opts | 此工作区的布局专属选项表。键和值取决于所用的布局 | table |  |
| monitor | 将工作区绑定到显示器。请参阅[语法](#syntax)和[显示器](../monitors/_index.md) | string |  |
| default | 是否将此工作区设为指定显示器的默认工作区 | bool |  |
| no_border | 是否禁用边框 | bool |  |
| no_rounding | 是否禁用窗口圆角 | bool |  |
| no_shadow | 是否禁用阴影 | bool |  |
| persistent | 即使此工作区为空且未处于活动状态，也保留它 | bool |  |


<details><summary>示例</summary>


```lua
hl.workspace_rule({ workspace = "3", no_rounding = true, decorate = false })
hl.workspace_rule({ workspace = "name:coding", no_rounding = true, decorate = false, gaps_in = 0, gaps_out = 0, no_border = true, monitor = "DP-1" })
hl.workspace_rule({ workspace = "8", border_size = 8 })
hl.workspace_rule({ workspace = "name:Hello", monitor = "DP-1", default = true })
hl.workspace_rule({ workspace = "name:gaming", monitor = "desc:Chimei Innolux Corporation 0x150C", default = true })
hl.workspace_rule({ workspace = "15", animation = "slidevert", default_name = "slider" })
```



</details>

<a id="per-workspace-layouts"></a>

### 为各工作区单独设置布局

使用工作区规则为各工作区单独设置布局：

```lua
hl.workspace_rule({ workspace = "2", layout = "scrolling" })
hl.workspace_rule({ workspace = "3", layout = "dwindle" })
```
