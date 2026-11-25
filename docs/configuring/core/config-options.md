# 配置选项

本页介绍 Hyprland 的所有配置选项，特定布局专用的选项除外。这些选项在各自的[布局页面](../layouts/_index.md)中介绍。

有关[按键绑定](binds/_index.md)、[显示器](monitors/_index.md)、[动画](animations.md)等内容，请参阅[核心配置](_index.md)中的其他页面。

<a id="syntax"></a>

## 语法

要一次更新多个选项，可以这样写：

```lua
hl.config({
  category1 = {
    option = value,
  },
  category2 = {
    option1 = value1,
    option2 = value2,
  },
})
```

如果只需更新少数几个选项，也可以这样写：

```lua
hl.config({ ["category.option"] = value })
```

你可以多次调用 `hl.config()` 来设置选项，因为每次调用只会更新该次传入的选项。

请注意，**如果多次设置同一个配置选项，最后一行的设置始终会覆盖此前对该选项的所有设置！**

因此，你也可以使用 [`hyprctl eval 'hl.config(...)'`](advanced-configuration/using-hyprctl.md#eval) 在运行时更新选项，无需将这些设置写入配置文件。这样设置的选项会在下次重新加载（或重新启动）Hyprland 时恢复为默认值。

> [!TIP]
> 继续之前，请确保你已阅读并理解[本 wiki 使用的命名约定](../naming-conventions.md)。

各选项以表格形式说明：

| 名称 | 说明 | 类型 | 默认值 | 范围 |
| --- | --- | --- | --- | --- |
| string | 字符串 | [数据类型](../naming-conventions.md#data-types) | `Default` | `Limit` |

`Default` 可以是以下之一：
- 与类型相符的值
- ``[[Empty]]``
- ``[[Auto]]``

`Limit` 可以是以下之一：
- 取值范围
- `None`

如果限制字段填写的是字面值 `None`，表示该选项没有限制。如果某个选项的值超出允许范围，Hyprland 会报配置错误。

<a id="sections"></a>

## 配置分节

<a id="general"></a>

### 常规

类别：`general`

| 名称 | 说明 | 类型 | 默认值 | 范围 |
| --- | --- | --- | --- | --- |
| allow_tearing | 控制是否允许画面撕裂的总开关。参见[画面撕裂](../extra/tearing.md)。 | bool | `false` |  |
| border_size | 窗口四周的边框宽度 | int | `1` | [0 - 20] |
| extend_border_grab_area | 扩大边框周围可点击并拖动的区域，仅在启用 `general.resize_on_border` 时生效 | int | `15` | [0 - 100] |
| float_gaps | 浮动窗口与显示器边缘之间的间距。`-1` 表示使用默认值。 | css_gaps | `0` |  |
| gaps_in | 窗口之间的间距 | css_gaps | `5` |  |
| gaps_out | 窗口与显示器边缘之间的间距 | css_gaps | `20` |  |
| gaps_workspaces | 工作区之间的间距。与 gaps_out 叠加 | int | `0` | [0 - 100] |
| hover_icon_on_border | 光标悬停在边框上时显示调整大小的光标图标，仅在启用 `general.resize_on_border` 时生效 | bool | `true` |  |
| layout | 要使用的布局。可选值：`"dwindle"`/`"master"`/`"scrolling"`/`"monocle"` | string | `"dwindle"` |  |
| locale | 覆盖系统的区域设置，例如 `"en_US"`、`"es"` | string | [[Empty]] |  |
| modal_parent_blocking | 是否允许与模态窗口的父窗口交互 | bool | `true` |  |
| no_focus_fallback | 如果设为 true，沿某个方向移动焦点时，若该方向没有窗口，就不会将焦点移到下一个可用窗口 | bool | `false` |  |
| resize_corner | 调整浮动窗口大小时，强制使用指定的角（从左上角起按顺时针方向编号为 1-4，设为 0 可禁用） | int | `0` | [0 - 4] |
| resize_on_border | 允许通过点击并拖动边框或窗口间的空隙来调整窗口大小 | bool | `false` |  |

<a id="general-colors"></a>

#### 常规配色

类别：`general.col`

| 名称 | 说明 | 类型 | 默认值 | 范围 |
| --- | --- | --- | --- | --- |
| active_border | 活动窗口的边框颜色 | gradient | `0xffffffff` |  |
| inactive_border | 非活动窗口的边框颜色 | gradient | `0xff444444` |  |
| nogroup_border | 无法加入窗口组的非活动窗口的边框颜色 | gradient | `0xffffaaff` |  |
| nogroup_border_active | 无法加入窗口组的活动窗口的边框颜色 | gradient | `0xffff00ff` |  |

<a id="snap"></a>

#### 吸附

类别：`general.snap`

| 名称 | 说明 | 类型 | 默认值 | 范围 |
| --- | --- | --- | --- | --- |
| enabled | 启用浮动窗口吸附 | bool | `false` |  |
| border_overlap | 启用后，相互吸附的窗口之间只留出一个边框宽度的间距 | bool | `false` |  |
| respect_gaps | 启用后，吸附时会保留 general:gaps_in 设置的窗口间距 | bool | `false` |  |
| monitor_gap | 触发吸附前，窗口边缘与显示器边缘之间的最小间距（像素） | int | `10` | [0 - 100] |
| window_gap | 触发吸附前，窗口之间的最小间距（像素） | int | `10` | [0 - 100] |

<a id="decoration"></a>

### 窗口装饰

类别：`decoration`

| 名称 | 说明 | 类型 | 默认值 | 范围 |
| --- | --- | --- | --- | --- |
| active_opacity | 活动窗口的不透明度 | float | `1.0` | [0.0 - 1.0] |
| border_part_of_window | 是否将窗口边框视为窗口的一部分 | bool | `true` |  |
| dim_around | `dim_around` 窗口规则使窗口周围区域变暗的程度 | float | `0.4` | [0.0 - 1.0] |
| dim_inactive | 启用非活动窗口变暗效果 | bool | `false` |  |
| dim_modal | 启用模态窗口的父窗口变暗效果 | bool | `true` |  |
| dim_special | 打开特殊工作区时，屏幕其余部分变暗的程度。[0.0 - 1.0] | float | `0.2 ` |  |
| dim_strength | 非活动窗口变暗的程度 | float | `0.5` | [0.0 - 1.0] |
| fullscreen_opacity | 全屏窗口的不透明度 | float | `1.0` | [0.0 - 1.0] |
| inactive_opacity | 非活动窗口的不透明度 | float | `1.0` | [0.0 - 1.0] |
| rounding | 圆角半径（以布局像素为单位） | int / `{ top_left?, top_right?, bottom_left?, bottom_right?}` | `0` | [0 - 100] |
| rounding_power | 调整圆角的曲线形状。值越大，曲线越平滑。1.0 对应三角形切角，2.0 对应圆弧，4.0 对应方圆形曲线 | float | `2.0` | [1.0 - 10.0] |
| screen_shader | 自定义着色器的路径。该着色器在渲染结束时应用。示例见 `examples/screenShader.frag` | string | [[Empty]] |  |

<a id="opacity"></a>

#### 不透明度

最终不透明度是所有不透明度值的**乘积**。在不透明度值后添加 `"override"`，即可将其用作固定值，而非乘数。

例如，将 `active_opacity` 设为 `0.5`，并将窗口规则 `opacity` 设为 `0.5`，最终不透明度为 `0.25`。

> [!IMPORTANT]
> 单个不透明度值可以超过 `1.0`，但只要乘积超过 `1.0`，就会导致画面显示异常。


<details><summary>示例</summary>


```lua
-- 无论其他规则如何设置，不透明度在活动时为 0.8，非活动时为 0.8，全屏时为 1.0：
hl.window_rule({
  match   = { class = "kitty" },
  opacity = "0.8 override 0.8 override 1.0 override",
})
```



</details>

<a id="blur"></a>

#### 模糊

类别：`decoration.blur`

| 名称 | 说明 | 类型 | 默认值 | 范围 |
| --- | --- | --- | --- | --- |
| enabled | 启用 kawase 窗口背景模糊效果 | bool | `true` |  |
| brightness | 调节模糊效果的亮度 | float | `1` | [0.0 - 2.0] |
| contrast | 调节模糊效果的对比度 | float | `0.8916` | [0.0 - 2.0] |
| ignore_opacity | 让模糊层忽略窗口的不透明度 | bool | `true` |  |
| input_methods | 是否对输入法窗口应用模糊效果，例如 `fcitx5` 的窗口 | bool | `false` |  |
| input_methods_ignorealpha | 作用与图层规则中的 ignore_alpha 相同。如果像素的不透明度低于设定值，就不对该像素应用模糊效果 | float | `0.2` | [0.0 - 1.0] |
| new_optimizations | 是否进一步优化模糊处理。建议保持启用，可大幅提升性能 | bool | `true` |  |
| noise | 添加的噪声量 | float | `0.0117` | [0.0 - 1.0] |
| passes | 执行模糊处理的遍数 | int | `1` | [0 - 10] |
| popups | 是否对弹出窗口应用模糊效果，例如 `right-click menus`（右键菜单） | bool | `false` |  |
| popups_ignorealpha | 作用与图层规则中的 ignore_alpha 相同。如果像素的不透明度低于设定值，就不对该像素应用模糊效果 | float | `0.2` | [0.0 - 1.0] |
| proportional | 启用后，模糊强度与像素的不透明度成正比。需要启用 `render:use_shader_blur_blend` | bool | `false` |  |
| size | 模糊范围（距离） | int | `8` |  |
| special | 是否模糊特殊工作区后方的内容（注意：性能开销较大） | bool | `false` |  |
| variant | 模糊效果的样式。可能会显著提高 GPU 和 CPU 的使用率 | string | `kawase` | [见下文](#blur-variants) |
| vibrancy | 提高模糊区域的色彩饱和度 | float | `0.1696` | [0.0 - 1.0] |
| vibrancy_darkness | `vibrancy` 对暗部的影响强度 | float | `0.0` | [0.0 - 1.0] |
| xray | 启用后，浮动窗口的背景模糊处理会忽略平铺窗口，从而显著降低浮动窗口的模糊处理开销。设置 `new_optimizations = false` 时，此项禁用 | bool | `false` |  |

> [!NOTE]
> `blur.size` 和 `blur.passes` 都必须至少为 1，模糊效果才会生效。
>
> 当 `blur.size` 的值较大时，需要增大 `blur.passes` 才能避免模糊效果出现异常，但请记住，`blur.passes` 越大，GPU 的负担就越重。
>
> 如果启用模糊后，某些窗口仍没有模糊效果，可能是因为该效果由客户端设置控制。请参阅[常见问题](../../faq/_index.md#blur)。

<a id="blur-variants"></a>

##### 模糊样式

不同的模糊方法可能共用某些选项。

可用样式：

- `kawase` - 默认样式
- `acrylic` - 类似液态玻璃的效果
- `aurora` - 类似极光的光带
- `drops` - 雨滴落在窗玻璃上的效果
- `fluid_jar` - 二维流体模拟
- `frost` - 冰面开裂效果
- `haze` - 另一种光线漫射效果
- `heat_shimmer` - 带有像差的轻微热浪抖动效果
- `prism` - 三角形折射遮罩
- `ripple` - 点击时产生涟漪
- `water` - 使用高度图生成的涟漪

<a id="acrylic"></a>

###### 亚克力

适用样式：`acrylic`
类别：`decoration.blur.acrylic`

| 名称 | 说明 | 类型 | 默认值 | 范围 |
| --- | --- | --- | --- | --- |
| aberration | 亚克力透镜中各色光的相对分离程度 | float | `0.025` | [0.0 - 0.25] |
| bulb | 亚克力弯曲边缘的宽度（像素） | float | `48.0` | [4.0 - 256.0] |
| clarity | 透过亚克力表面仍清晰可见的背景比例 | float | `0.82` | [0.0 - 1.0] |
| refraction | 亚克力透镜的最大位移（像素） | float | `24.0` | [0.0 - 48.0] |
| tint | 亚克力的着色颜色。Alpha 通道控制光的吸收程度 | color | `0x14EEF5FF` |  |

<a id="aurora"></a>

###### 极光

适用样式：`aurora`
类别：`decoration.blur.aurora`

| 名称 | 说明 | 类型 | 默认值 | 范围 |
| --- | --- | --- | --- | --- |
| color1 | 第一层极光光幕的颜色。Alpha 值控制该颜色在最终效果中的权重 | color | `0x29F0A0FF` |  |
| color2 | 第二层极光光幕的颜色。Alpha 值控制该颜色在最终效果中的权重 | color | `0x7A4DFFFF` |  |
| intensity | 极光颜色对最终效果的影响强度 | float | `0.35` | [0.0 - 1.0] |
| speed | 动画速度。设为 0 可冻结动画 | float | `1.0` | [0.0 - 10.0] |

<a id="drops"></a>

###### 水滴

适用于：`drops`
类别：`decoration.blur.drops`

| 名称 | 说明 | 类型 | 默认值 | 范围 |
| --- | --- | --- | --- | --- |
| speed | 动画速度。设为 0 可禁用动画 | float | `3.0` | [0.0 - 10.0] |

<a id="fluid-jar"></a>

###### 液体罐

适用于：`fluid_jar`
类别：`decoration.blur.fluid_jar`

| 名称 | 说明 | 类型 | 默认值 | 范围 |
| --- | --- | --- | --- | --- |
| color | 液体颜色 | color | `0xCC3399FF` |  |
| distortion | 液体折射畸变的倍率 | float | `8.0` | [0.0 - 10.0] |
| fill_amount | 罐内液体的填充高度 | float | `0.5` | [0.0 - 1.0] |
| mass | 液体的惯性质量 | float | `1.4` | [0.1 - 10.0] |
| precision | 液体模拟精度的倍率。2x 能较好地兼顾精度与性能，4x 的计算开销较大，8x 则过高且没有必要 | float | `2.0` | [0.5 - 8.0] |
| speed | 动画速度 | float | `3.7` | [0.0 - 10.0] |
| turbulence | 液体内部湍流强度的倍率 | float | `1.2` | [0.0 - 5.0] |

<a id="glass"></a>

###### 玻璃

适用于：`aurora`、`drops`、`heat_shimmer`、`prism`
类别：`decoration.blur.glass`

| 名称 | 说明 | 类型 | 默认值 | 范围 |
| --- | --- | --- | --- | --- |
| refraction | 玻璃类模糊效果的最大折射位移，单位为像素 | float | `20.0` | [0.0 - 20.0] |
| roughness | 玻璃浮雕效果的明暗强度 | float | `1.0` | [0.0 - 1.0] |
| size | 玻璃类模糊效果的图案大小，单位为像素 | float | `40.0` | [4.0 - 512.0] |

<a id="haze"></a>

###### 薄雾

适用于：`haze`
类别：`decoration.blur.haze`

| 名称 | 说明 | 类型 | 默认值 | 范围 |
| --- | --- | --- | --- | --- |
| intensity | 薄雾的珠光光泽强度 | float | `0.35` | [0.0 - 1.0] |
| iridescence | 薄雾珠光效果的色彩偏移强度 | float | `0.7` | [0.0 - 1.0] |

<a id="heat-shimmer"></a>

###### 热浪扭曲

适用于：`heat_shimmer`
类别：`decoration.blur.heat_shimmer`

| 名称 | 说明 | 类型 | 默认值 | 范围 |
| --- | --- | --- | --- | --- |
| speed | 动画速度。设为 0 可禁用动画 | float | `1.0` | [0.0 - 10.0] |

<a id="ripple"></a>

###### 涟漪

适用于：`ripple`
类别：`decoration.blur.ripple`

| 名称 | 说明 | 类型 | 默认值 | 范围 |
| --- | --- | --- | --- | --- |
| duration | 持续时间，单位为秒 | float | `0.45` | [0.05 - 5.0] |
| radius | 最大半径，单位为像素 | float | `400.0` | [1.0 - 1000.0] |
| strength | 最大折射位移，单位为像素 | float | `30.0` | [0.0 - 32.0] |
| width | 波纹宽度，单位为像素 | float | `32.0` | [1.0 - 200.0] |

<a id="water"></a>

###### 水面

适用于：`water`
类别：`decoration.blur.water`

| 名称 | 说明 | 类型 | 默认值 | 范围 |
| --- | --- | --- | --- | --- |
| damping | 波动衰减的阻尼 | float | `0.95` | [0.0 - 1.0] |
| duration | 最长持续时间，单位为秒 | float | `12.0` | [0.5 - 60.0] |
| radius | 指针作用半径，单位为像素 | float | `20.0` | [1.0 - 1000.0] |
| speed | 传播速度 | float | `0.76` | [0.0 - 10.0] |
| strength | 最大折射位移和扰动注入强度，单位均为像素 | float | `32.0` | [0.0 - 32.0] |

<a id="shadow"></a>

#### 阴影

类别：`decoration.shadow`

| 名称 | 说明 | 类型 | 默认值 | 范围 |
| --- | --- | --- | --- | --- |
| enabled | 启用窗口投影 | bool | `true` |  |
| color | 活动窗口的阴影颜色。Alpha 值决定不透明度 | color/gradient | `0xee1a1a1a` |  |
| color_inactive | 非活动窗口的阴影颜色。未设置时使用 `color` 的值 | color/gradient | [[Empty]] |  |
| offset | 阴影的渲染偏移量 | vec2 | `{0, 0}` |  |
| range | 阴影范围（大小），单位为像素 | int | `4` | [0 - 100] |
| render_power | 渲染阴影衰减时使用的指数。指数越大，衰减越快 | int | `3` | [1 - 4] |
| scale | 阴影的缩放比例 | float | `1.0` | [0.05 - 2.0] |
| sharp | 启用后，阴影边缘会变得锐利，效果类似于将渲染指数设为无穷大 | bool | `false` |  |

<a id="glow"></a>

#### 辉光

类别：`decoration.glow`

| 名称 | 说明 | 类型 | 默认值 | 范围 |
| --- | --- | --- | --- | --- |
| enabled | 启用窗口内辉光 | bool | `false` |  |
| color | 活动窗口的辉光颜色。Alpha 值决定不透明度 | gradient | `0xee1a1a1a` |  |
| color_inactive | 非活动窗口的辉光颜色。未设置时使用 `color` 的值 | gradient | [[Empty]] |  |
| range | 辉光范围（大小），单位为像素 | int | `10` | [0 - 100] |
| render_power | 渲染阴影衰减时使用的指数。指数越大，衰减越快 | int | `3` | [1 - 4] |

<a id="motion-blur"></a>

#### 运动模糊

类别：`decoration.motion_blur`

| 名称 | 说明 | 类型 | 默认值 | 范围 |
| --- | --- | --- | --- | --- |
| enabled | 在移动窗口或调整窗口大小时启用运动模糊 | bool | `false` |  |
| samples | 渲染时的采样数。采样越多，模糊效果越清晰，计算开销也越大 | int | `7` | [1 - 64] |

<a id="wobble"></a>

#### 晃动

类别：`decoration.wobble`

| 名称 | 说明 | 类型 | 默认值 | 范围 |
| --- | --- | --- | --- | --- |
| enabled | 在移动窗口或调整窗口大小时启用晃动效果 | bool | `false` |  |
| mesh | 晃动网格每条边上的顶点数 | int | `12` | [2 - 32] |
| stiffness | 晃动形变的弹簧刚度 | float | `200` | [0.0001 - 1000] |
| damping | 晃动形变的弹簧阻尼 | float | `12` | [0 - 1000] |
| mass | 晃动形变的弹簧质量 | float | `1` | [0.0001 - 1000] |
| intensity | 晃动形变的冲量倍率 | float | `0.2` | [0 - 2] |
| value_epsilon | 位置偏差阈值，低于该值时视为晃动已稳定 | float | `0.25` | [0 - 100] |
| velocity_epsilon | 速度阈值，低于该值时视为晃动已稳定 | float | `2` | [0 - 1000] |

<a id="animations"></a>

### 动画

类别：`animations`

| 名称 | 说明 | 类型 | 默认值 | 范围 |
| --- | --- | --- | --- | --- |
| enabled | 启用动画 | bool | `true` |  |
| workspace_wraparound | 启用工作区首尾循环，使有方向的工作区切换动画将第一个和最后一个工作区视为相邻 | bool | `false` |  |

有关动画的更多信息，请参阅[此处](animations.md)。

<a id="input"></a>

### 输入

类别：`input`

| 名称 | 说明 | 类型 | 默认值 | 范围 |
| --- | --- | --- | --- | --- |
| accel_profile | 设置光标加速模式。请参阅[下方](#accel-profile)的说明。留空时使用 `libinput` 为当前输入设备提供的默认模式。另请参阅 [libinput 的指针加速说明](https://wayland.freedesktop.org/libinput/doc/latest/pointer-acceleration.html#pointer-acceleration)。可选值：`"adaptive"`/`"flat"`/`"custom"` | string | [[Empty]] |  |
| emulate_discrete_scroll | 根据高分辨率滚动事件模拟离散滚动。`0` 表示禁用，`1` 表示仅处理非标准事件，`2` 表示强制处理所有滚轮事件 | int | `1` | [0 - 2] |
| float_switch_override_focus | 设为 `1` 或 `2` 时，在平铺窗口与浮动窗口之间双向切换时，焦点会转移到光标下的窗口。设为 `2` 时，在浮动窗口之间切换时，焦点也会跟随鼠标。`0` 表示禁用 | int | `1` | [0 - 2] |
| focus_on_close | 控制关闭窗口后的焦点行为。设为 `0` 时，焦点转移到下一个候选窗口。设为 `1` 时，焦点转移到光标下的窗口。设为 `2` 时，焦点转移到最近使用或激活的窗口 | int | `0` | [0 - 2] |
| follow_mouse | 指定光标移动是否影响窗口焦点，以及如何影响。请参阅[下方](#follow-mouse)的说明 | int | `1` | [0 - 3] |
| follow_mouse_shrink | 将非活动窗口用于焦点检测的判定区域向内缩小指定的像素数。这样会在窗口间隙中形成死区，光标在死区内移动时不会改变焦点。仅在 `follow_mouse` 设为 `1` 时生效 | int | `0` | [0 - 300] |
| follow_mouse_threshold | 要使光标下的窗口获得焦点，鼠标至少需要移动的距离，单位为逻辑像素。仅在 `follow_mouse` 设为 `1` 时生效 | float | `0.0` |  |
| force_no_accel | 强制禁用光标加速。此设置会绕过大部分指针设置，以获取尽可能接近原始输入的信号。**不建议启用此项，因为它可能导致光标不同步。** | bool | `false` |  |
| kb_file | 也可以按需指定自定义 .xkb 文件的路径 | string | [[Empty]] |  |
| kb_layout | 相应的 XKB 键盘映射参数 | string | `"us"` |  |
| kb_model | 对应的 XKB 键位映射参数。参见[下方说明](#xkb-keymap-params) | string | [[Empty]] |  |
| kb_options | 相应的 XKB 键盘映射参数 | string | [[Empty]] |  |
| kb_rules | 相应的 XKB 键盘映射参数 | string | [[Empty]] |  |
| kb_variant | 相应的 XKB 键盘映射参数 | string | [[Empty]] |  |
| left_handed | 互换鼠标左右键 | bool | `false` |  |
| mouse_refocus | 启用后，当指针越过窗口边界时，鼠标焦点会切换到指针悬停的窗口。仅当 `follow_mouse` 设为 `1` 时生效 | bool | `true` |  |
| natural_scroll | 反转滚动方向。启用后，滚动操作会直接移动内容，而不是操纵滚动条 | bool | `false` |  |
| numlock_by_default | 默认启用数字锁定键（Num Lock） | bool | `false` |  |
| off_window_axis_events | 指定如何处理焦点窗口周围的滚动轴事件（平铺窗口的间隙或边框，浮动窗口的拖动区域或边框）。`0` 忽略事件；`1` 发送窗口边界外的坐标；`2` 将发送的指针坐标模拟为窗口内距离指针最近的点；`3` 将光标移至窗口内距离光标最近的点 | int | `1` | [0 - 3] |
| repeat_delay | 按住按键后开始连发前的延迟，单位为毫秒 | int | `600` | [0 - 2000] |
| repeat_rate | 按住按键时的连发速率，单位为次/秒 | int | `25` | [0 - 200] |
| resolve_binds_by_sym | 决定使用多种键盘布局时按键绑定的行为。设为 false 时，按键绑定始终按指定的第一个布局生效。设为 true 时，使用当前布局输入相应符号即可触发以该符号指定的按键绑定 | bool | `false` |  |
| rotation | 设置设备相对于逻辑中立位置顺时针旋转的角度，单位为度 | int | `0` | [0 - 359] |
| scroll_button | 设置用于滚动的按键。可用 `wev` 查看按键 ID。`0` 表示使用默认值 | int | `0` | [0 - 300] |
| scroll_button_lock | 启用滚动按键锁定后，无需一直按住该键。每按下并松开一次，就会切换锁定状态，使该键在逻辑上保持按下或松开。该键在逻辑上保持按下时，移动事件会转换为滚动事件 | bool | `false` |  |
| scroll_points | 当 `accel_profile` 设为 `"custom"` 时，设置滚动加速曲线。格式必须为 `"<step> <points>"`。留空则使用平坦的滚动曲线 | string | [[Empty]] |  |
| scroll_method | 设置滚动方式。更多信息见 [libinput 滚动文档](https://wayland.freedesktop.org/libinput/doc/latest/scrolling.html)。可选值为 `"2fg"`/`"edge"`/`"on_button_down"`/`"no_scroll"`（2fg 表示双指滚动） | string | [[Empty]] |  |
| scroll_factor | 外接鼠标滚动距离的倍率。[触控板的 scroll_factor](#touchpad) 需单独设置 | float | `1.0` | [0 - 100] |
| sensitivity | 设置鼠标输入灵敏度。更多信息见 [libinput 指针加速文档](https://wayland.freedesktop.org/libinput/doc/latest/pointer-acceleration.html#pointer-acceleration) | float | `0.0` | [-1.0 - 1.0] |
| special_fallthrough | 启用后，如果特殊工作区中只有浮动窗口，常规工作区中的窗口仍可获得焦点 | bool | `false` |  |
| swallow_focus_click | 启用后，首次点击未获得焦点的窗口时，只会将焦点移至该窗口，不会将此次点击传递给它。仅在鼠标焦点与键盘焦点分离时生效，例如 `input.follow_mouse` 设为 `0` 或 `2` 时 | bool | `false` |  |

<a id="xkb-keymap-params"></a>

##### XKB 键位映射参数

可在 [`/usr/share/X11/xkb/rules/evdev.lst`](file:///usr/share/X11/xkb/rules/evdev.lst) 中查看键盘型号、布局、变体和选项列表。也可使用 `localectl` 命令查看系统上有哪些可用配置。

有关可切换的键盘配置，请参阅[按键绑定页面的键盘布局条目](binds/keyboard-layouts.md)。

<a id="follow-mouse"></a>

##### 焦点跟随鼠标

- `0` - 移动光标不会改变焦点。
- `1` - 移动光标时，焦点始终跟随光标，切换到光标所在的窗口。
- `2` - 光标焦点与键盘焦点分离。点击窗口会将键盘焦点移至该窗口。
- `3` - 光标焦点与键盘焦点完全独立。点击窗口不会改变键盘焦点。

<a id="accel-profile"></a>

##### 加速曲线

`custom <step> <points...>`

示例：`custom 200 0.0 0.5`

<a id="scroll-points"></a>

##### 滚动曲线控制点

`<step> <points...>`

示例：`0.2 0.0 0.5 1 1.2 1.5`

有关其工作原理的详细说明，请参阅 [libinput 文档](https://wayland.freedesktop.org/libinput/doc/latest/pointer-acceleration.html)。

要模拟 Windows 的加速曲线，请参阅[此脚本](https://gist.github.com/fufexan/de2099bc3086f3a6c83d61fc1fcc06c9)。

<a id="touchpad"></a>

#### 触摸板

类别：`input.touchpad`

| 名称 | 说明 | 类型 | 默认值 | 范围 |
| --- | --- | --- | --- | --- |
| clickfinger_behavior | 用一指、双指或三指按下触控板时，分别映射为鼠标左键、右键或中键。启用后，点击位置不再决定触发哪个按键。更多信息见 [libinput 按手指数判定按键的说明](https://wayland.freedesktop.org/libinput/doc/latest/clickpad-softbuttons.html#clickfinger-behavior) | bool | `false` |  |
| disable_while_typing | 打字时禁用触控板 | bool | `true` |  |
| drag_3fg | 启用三指拖动。更多信息见 [libinput 三指拖动文档](https://wayland.freedesktop.org/libinput/doc/latest/drag-3fg.html) | int | `0` | [0 - 2] |
| drag_lock | 启用后，拖动过程中抬起手指不会立即放下所拖动的项目。0 表示禁用，1 表示启用并在超时后解除拖动锁定，2 表示启用粘滞拖动锁定。更多信息见 [libinput 轻点拖动文档](https://wayland.freedesktop.org/libinput/doc/latest/tapping.html#tap-and-drag) | int | `0` | [0 - 2] |
| flip_x | 反转触控板的水平移动方向 | bool | `false` |  |
| flip_y | 反转触控板的垂直移动方向 | bool | `false` |  |
| middle_button_emulation | 同时触发鼠标左键和右键将被视为一次中键点击。启用后，触控板上原本按点击位置触发中键的区域将不再具有该功能。更多信息见 [libinput 中键模拟文档](https://wayland.freedesktop.org/libinput/doc/latest/middle-button-emulation.html) | bool | `false` |  |
| natural_scroll | 反转滚动方向。启用后，滚动操作会直接移动内容，而不是操纵滚动条 | bool | `false` |  |
| scroll_factor | 滚动距离的倍率 | float | `1.0` | [0.0 - 100] |
| tap_and_drag | 设置触控板的轻点拖动模式 | bool | `true` |  |
| tap_button_map | 设置触控板通过轻点模拟鼠标按键时的映射。留空时默认为 `"lrm"`。L 表示左键，M 表示中键，R 表示右键 | string | [[Empty]] | "lrm"/"lmr" |
| tap_to_click | 用一指、双指或三指轻点触控板，分别触发鼠标左键、右键或中键 | bool | `true` |  |

<a id="touchdevice"></a>

#### 触摸设备

类别：`input.touchdevice`

| 名称 | 说明 | 类型 | 默认值 | 范围 |
| --- | --- | --- | --- | --- |
| enabled | 是否启用触摸设备输入 | bool | `true` |  |
| output | 触摸设备绑定的显示器。默认自动检测。设为空字符串可关闭自动检测 | string | [[Auto]] |  |
| transform | 对触摸设备的输入应用变换。可用的变换与[显示器支持的变换](monitors/positioning.md#rotation)相同 | int | `0` | [0 - 6] |

<a id="virtualkeyboard"></a>

#### 虚拟键盘

类别：`input.virtualkeyboard`

| 名称 | 说明 | 类型 | 默认值 | 范围 |
| --- | --- | --- | --- | --- |
| release_pressed_on_close | 关闭虚拟键盘时，释放该键盘按下的所有按键 | bool | `false` |  |
| share_states | 是否与其他键盘共用按键按下状态和修饰键状态。0 表示否，1 表示是，2 表示除输入法客户端外均共用 | int | `2` | [0 - 2] |

<a id="tablet"></a>

#### 数位板

类别：`input.tablet`

| 名称 | 说明 | 类型 | 默认值 | 范围 |
| --- | --- | --- | --- | --- |
| enabled | 是否启用数位板输入 | bool | `true` |  |
| output | 数位板绑定的显示器。可设为 `"current"` 或显示器名称。留空则映射到所有显示器组成的区域 | string | [[Empty]] |  |
| transform | 对数位板的输入应用变换。可用的变换与[显示器支持的变换](monitors/positioning.md#rotation)相同 | int | `0` | [0 - 6] |
| absolute_region_position | 是否将 `region_position` 视为显示器布局中的绝对位置。仅在 `output` 为空时生效 | bool | `false` |  |
| active_area_position | 有效区域的位置，单位为毫米 | vec2 | `{0, 0}` | [0 - 5000] |
| active_area_size | 数位板有效区域的尺寸，单位为毫米 | vec2 | `{0, 0}` | [0 - 5000] |
| left_handed | 启用后，数位板的输入方向将旋转 180 度 | bool | `false` |  |
| region_position | 映射区域在显示器布局中的位置，以所绑定显示器的左上角或所有显示器组成的区域的左上角为基准 | vec2 | `{0, 0}` | [-100000 - 100000] |
| region_size | 映射区域的尺寸。设置此变量后，数位板输入将映射到该区域。`{0, 0}` 或无效尺寸表示未设置 | vec2 | `{0, 0}` | [1 - 100000] |
| relative_input | 是否使用相对坐标输入 | bool | `false` |  |

<a id="tablettool"></a>

#### 数位板工具

类别：`input.tablettool`

| 名称 | 说明 | 类型 | 默认值 | 范围 |
| --- | --- | --- | --- | --- |
| eraser_button_mode | 更改数位板工具上橡皮擦按键的行为。设为 `0` 时，使用工具默认的硬件行为。设为 `1` 时，橡皮擦按键改为发送按键事件 | int | 0 | [0 - 6] |
| eraser_button_override | 指定 eraser_button_mode 设为 `1` 时按键事件对应的按钮。必须使用有效的按钮代码（如 BTN_STYLUS），不能使用伪按钮代码（如 BTN_TOOL_\*）或键盘按键代码（KEY_\*）。可用 `wev` 查看 ID。`0` 表示使用默认值 | int | 0 | [0 - ...] |
| pressure_range_min | 设置工具压力范围的下限。负值表示使用设备默认值。该值通常为 `0.0` | float | -1.0 | [-1.0 - 1.0] |
| pressure_range_max | 设置工具压力范围的上限。负值表示使用设备默认值。该值通常为 `1.0` | float | -1.0 | [-1.0 - 1.0] |
<a id="per-device-input-config"></a>

### 按设备配置输入

详见[各设备的输入配置说明](devices.md)。

<a id="gestures"></a>

### 手势

类别：`gestures`

| 名称 | 说明 | 类型 | 默认值 | 范围 |
| --- | --- | --- | --- | --- |
| close_max_timeout | 使用 1:1 手势关闭窗口时的超时时间，单位为毫秒 | int | `1000` | [10 - 2000] |
| workspace_swipe_cancel_ratio | 滑动距离达到总距离的多大比例才会触发切换。例如，设为 `0.7` 时，如果滑动距离超过总距离的 70%，则切换工作区，否则取消手势 | float | `0.5` | [0.0 - 1.0] |
| workspace_swipe_create_new | 在最后一个工作区向右滑动时，是否创建新的工作区 | bool | `true` |  |
| workspace_swipe_direction_lock | 启用后，滑动距离超过 `direction_lock_threshold` 时，工作区切换方向将被锁定（仅适用于触控板） | bool | `true` |  |
| workspace_swipe_direction_lock_threshold | 触发方向锁定所需的滑动距离，单位为像素（仅适用于触控板） | int | `10` | [0 - 200] |
| workspace_swipe_distance | 触控板手势的滑动距离，单位为像素 | int | `300` | [0 - 2000] |
| workspace_swipe_forever | 启用后，可继续滑动到更远的工作区，不受相邻工作区的限制 | bool | `false` |  |
| workspace_swipe_invert | 反转滑动方向（仅适用于触控板） | bool | `true` |  |
| workspace_swipe_min_speed_to_force | 忽略 `cancel_ratio` 并强制切换工作区所需的最低滑动速度，以每个采样时间点的像素数计。`0` 表示禁用 | int | `30` | [0 - 200] |
| workspace_swipe_touch | 启用从触摸屏边缘滑动切换工作区的功能 | bool | `false` |  |
| workspace_swipe_touch_invert | 反转滑动方向（仅适用于触摸屏） | bool | `false` |  |
| workspace_swipe_use_r | 启用后，滑动时将使用 `r` 前缀代替 `m` 前缀来查找工作区 | bool | `false` |  |

<a id="scrolling"></a>

#### 滚动

类别：`gestures.scrolling`

| 名称 | 说明 | 类型 | 默认值 | 范围 |
| --- | --- | --- | --- | --- |
| move_snap_to_grid | 结束滚动移动手势时，是否尝试对齐到网格 | bool | `true` |  |
| move_snap_cursor | 结束滚动移动手势时，是否将光标移至刚获得焦点的窗口 | bool | `true` |  |

<a id="group"></a>

### 窗口组

类别：`group`

| 名称 | 说明 | 类型 | 默认值 | 范围 |
| --- | --- | --- | --- | --- |
| auto_group | 是否将新窗口自动加入当前获得焦点且未锁定的窗口组。*注意：如果只想对特定窗口禁用 auto_group，请改用[“group barred”窗口规则](rules/window-rules.md#group-window-rule-options)。* | bool | `true` |  |
| drag_into_group | 将窗口拖入未锁定的窗口组时，是否将其并入该组。`0` - 禁用，`1` - 启用，`2` - 仅在拖入组栏时合并 | int | `1` | [0 - 2] |
| focus_removed_window | 是否让刚移出窗口组的窗口获得焦点 | bool | `true` |  |
| group_on_movetoworkspace | 使用 hl.dsp.window.move({ workspace }) 时，是否将窗口并入目标工作区中唯一的未锁定窗口组 | bool | `false` |  |
| insert_after_current | 组内新窗口是插在当前窗口之后，还是追加到组末尾 | bool | `true` |  |
| merge_floated_into_tiled_on_groupbar | 将浮动窗口拖入平铺窗口的组栏时，是否将其并入该组 | bool | `false` |  |
| merge_groups_on_drag | 是否允许将窗口组拖入其他组 | bool | `true` |  |
| merge_groups_on_groupbar | 将一个窗口组拖入另一个组的组栏时，是否合并这两个组。*注意：只有同时设置了 `drag_into_group = 2` 和 `merge_groups_on_drag = true`，启用此选项才会生效。* | bool | `true` |  |

<a id="group-colors"></a>

#### 窗口组颜色

类别：`group.col`

| 名称 | 说明 | 类型 | 默认值 | 范围 |
| --- | --- | --- | --- | --- |
| border_active | 活动窗口组的边框颜色。渐变支持额外参数 `whole_monitor? = bool` | gradient | `0x66ffff00` |  |
| border_inactive | 非活动窗口组的边框颜色。渐变支持额外参数 `whole_monitor? = bool` | gradient | `0x66777700` |  |
| border_locked_active | 已锁定的活动窗口组的边框颜色。渐变支持额外参数 `whole_monitor? = bool` | gradient | `0x66ff5500` |  |
| border_locked_inactive | 已锁定的非活动窗口组的边框颜色。渐变支持额外参数 `whole_monitor? = bool` | gradient | `0x66775500` |  |

<a id="groupbar"></a>

#### 组栏

类别：`group.groupbar`

| 名称 | 说明 | 类型 | 默认值 | 范围 |
| --- | --- | --- | --- | --- |
| enabled | 启用组栏 | bool | `true` |  |
| blur | 对组栏中的指示条和渐变区域应用模糊效果 | bool | `false` |  |
| disable_when_only | 组内只有一个窗口时禁用组栏 | bool | `false` |  |
| font_family | 显示组栏标题所用的字体。未指定时使用 `misc.font_family` | string | [[Empty]] |  |
| font_size | 组栏标题的字号 | int | `8` | [2 - 64] |
| font_weight_active | 组栏中活动窗口标题的字重 | font_weight | `"normal"` |  |
| font_weight_inactive | 组栏中非活动窗口标题的字重 | font_weight | `"normal"` |  |
| gaps_in | 各渐变区域之间的间距 | int | `2` | [0 - 20] |
| gaps_out | 渐变区域与窗口之间的间距 | int | `2` | [0 - 20] |
| gradients | 启用渐变 | bool | `false` |  |
| gradient_round_only_edges | 仅对整个组栏最外侧的渐变边缘应用圆角 | bool | `true` |  |
| gradient_rounding | 渐变区域的圆角大小 | int | `2` | [0 - 100] |
| gradient_rounding_power | 调整渐变区域的圆角曲线。值越大，曲线越平滑。1.0 对应三角形切角，2.0 对应圆弧，4.0 对应方圆形曲线 | float | `2.0` | [1.0 - 10.0] |
| height | 组栏高度 | int | `14` | [0 - 64] |
| indicator_gap | 组栏指示条与标题之间的垂直间距 | int | `0` | [0 - 64] |
| indicator_height | 组栏指示条的高度 | int | `3` | [0 - 64] |
| keep_upper_gap | 添加或移除上方间距 | bool | `true` |  |
| middle_click_close | 用鼠标中键点击组栏时，是否关闭所点击的窗口 | bool | `true` |  |
| priority | 设置组栏的窗口装饰优先级 | int | `3` | [0 - 6] |
| render_titles | 是否在组栏装饰中显示窗口标题 | bool | `true` |  |
| round_only_edges | 仅对整个组栏最外侧的指示条边缘应用圆角 | bool | `true` |  |
| rounding | 指示条的圆角大小 | int | `1` | [0 - 40] |
| rounding_power | 调整组栏的圆角曲线。值越大，曲线越平滑。1.0 对应三角形切角，2.0 对应圆弧，4.0 对应方圆形曲线 | float | `2.0` | [1.0 - 10.0] |
| scrolling | 在组栏上滚动时，是否切换组内的活动窗口 | bool | `true` |  |
| stacked | 将组栏中的条目纵向堆叠显示 | bool | `false` |  |
| text_color | 组栏中窗口标题的颜色 | color | `0xffffffff` |  |
| text_color_inactive | 组栏中非活动窗口标题的颜色。未设置时使用 text_color | color | [[Empty]] |  |
| text_color_locked_active | 已锁定窗口组中活动窗口标题的颜色。未设置时使用 text_color | color | [[Empty]] |  |
| text_color_locked_inactive | 已锁定窗口组中非活动窗口标题的颜色。未设置时使用 text_color_inactive | color | [[Empty]] |  |
| text_offset | 调整标题的垂直位置 | int | `0` | [-20 - 20] |
| text_padding | 设置标题的水平内边距 | int | `0` | [0 - 22] |

<a id="groupbar-colors"></a>

##### 组栏颜色

类别：`group.groupbar.col`

| 名称 | 说明 | 类型 | 默认值 | 范围 |
| --- | --- | --- | --- | --- |
| active | 活动窗口组的组栏背景色 | gradient | `0x66ffff00` |  |
| inactive | 非活动（失去焦点）窗口组的组栏背景色 | gradient | `0x66777700` |  |
| locked_active | 已锁定的活动窗口组的组栏背景色 | gradient | `0x66ff5500` |  |
| locked_inactive | 已锁定的非活动窗口组的组栏背景色 | gradient | `0x66775500` |  |

<a id="misc"></a>

### 其他

类别：`misc`

| 名称 | 说明 | 类型 | 默认值 | 范围 |
| --- | --- | --- | --- | --- |
| allow_session_lock_restore | 设为 true 时，允许在锁屏应用崩溃后重新启动它 | bool | `false` |  |
| always_follow_on_dnd | 让鼠标焦点在拖放过程中跟随鼠标指针。建议保持启用，尤其是当“焦点跟随鼠标”设为 0 时 | bool | `true` |  |
| animate_manual_resizes | 设为 true 时，手动调整窗口大小或移动窗口时会显示动画 | bool | `false` |  |
| animate_mouse_windowdragging | 设为 true 时，用鼠标拖动窗口会显示动画。请注意，使用某些动画曲线时，窗口可能会出现异常行为 | bool | `false` |  |
| anr_missed_pings | 显示 ANR（应用无响应）对话框前，允许应用未响应的探测次数 | int | `5` | [1 - 20] |
| background_color | 更改背景颜色（需要启用 `disable_hyprland_logo`） | color | `0x111111` |  |
| bell_sound | 自定义系统提示音的 wav/ogg 文件路径。设为 "none" 或空字符串可静音，设为 "default" 则使用系统当前的提示音 | string | `"default"` |  |
| close_special_on_empty | 移除特殊工作区中的最后一个窗口时，关闭该工作区 | bool | `true` |  |
| disable_autoreload | 设为 true 时，保存配置后不会自动重新加载，需要执行 `hyprctl reload` 才能重新加载。这可能有助于节省电量 | bool | `false` |  |
| disable_hyprland_guiutils_check | 未安装 hyprland-guiutils 时不显示警告 | bool | `false` |  |
| disable_hyprland_logo | 禁用随机显示的 Hyprland 徽标或动漫少女背景。:( | bool | `false` |  |
| disable_scale_notification | 显示器无法设置合适的缩放比例时，不弹出通知 | bool | `false` |  |
| disable_splash_rendering | 禁用 Hyprland 背景上的随机短句。需要重新加载显示器配置才能生效。请注意，hyprpaper 有单独的设置可禁用这段文字 | bool | `false` |  |
| disable_watchdog_warning | 禁用关于未使用 start-hyprland 的警告 | bool | `false` |  |
| disable_xdg_env_checks | XDG 环境由外部管理时不显示警告 | bool | `false` |  |
| enable_anr_dialog | 是否在应用卡住时显示 ANR（应用无响应）对话框 | bool | `true` |  |
| enable_swallow | 启用窗口吞并 | bool | `false` |  |
| exit_window_retains_fullscreen | 关闭全屏窗口时，是否让下一个获得焦点的窗口进入全屏。0 - 禁用，1 - 启用，2 - 仅在关闭组内窗口时启用，3 - 仅在关闭未分组窗口时启用 | int | `0` | [0 - 3] |
| float_force_onscreen | 是否以及如何限制已有浮动窗口的位置，使其保持在屏幕范围内。0 - 不限制，1 - 至少一部分必须在屏幕内，2 - 必须完全在屏幕内 | int | `0` | [0 - 2] |
| new_float_force_onscreen | 与 `float_force_onscreen` 相同，但仅适用于新建的浮动窗口 | int | `2` | [0 - 2] |
| focus_on_activate | 应用请求获得焦点（即发出 `activate` 请求）时，Hyprland 是否将焦点交给该应用 | bool | `false` |  |
| font_family | 设置渲染文本所用的全局默认字体 | string | `"Sans"` |  |
| force_default_wallpaper | 强制使用三张默认壁纸中的一张。0 - 禁用动漫背景，1 - 禁用动漫背景，2 - 启用动漫背景，-1 - 随机选择 | int | `-1` | [-1 - 2] |
| initial_workspace_token_timeout | 窗口跟踪令牌的有效时间，以秒为单位。窗口须在令牌过期前于发起启动请求的工作区中打开。 | int | `10` | [1 - 3600] |
| initial_workspace_tracking | 启用后，窗口会在发起启动请求的工作区中打开。0 - 禁用，1 - 仅生效一次，2 - 持续生效（也适用于所有子进程） | int | `1` |  |
| key_press_enables_dpms | 如果 DPMS 处于 off 状态，按下任意键即可唤醒显示器 | bool | `false` |  |
| lockdead_screen_delay | 锁屏应用未能覆盖所有显示输出时，显示“lockdead”画面前的延迟时间，单位为毫秒 | int | `1000` | [0 - 5000] |
| middle_click_paste | 是否启用鼠标中键粘贴（也称为主选区粘贴） | bool | `true` |  |
| mouse_move_enables_dpms | 如果 DPMS 处于 off 状态，移动鼠标即可唤醒显示器 | bool | `false` |  |
| mouse_move_focuses_monitor | 鼠标指针移入另一台显示器时，是否将焦点切换到该显示器 | bool | `true` |  |
| name_vk_after_proc | 根据创建虚拟键盘的进程为其命名。例如，`/usr/bin/fcitx5` 创建的虚拟键盘名为 hl-virtual-keyboard-fcitx5 | bool | `true` |  |
| on_focus_under_fullscreen | 已有全屏或最大化窗口时，决定请求获得焦点的平铺窗口是取代该窗口、留在其后方，还是让该窗口退出全屏或最大化状态。0 - 忽略焦点请求（焦点保留在全屏窗口上），1 - 由平铺窗口取代原窗口，2 - 退出全屏或取消最大化 | int | `2` | [0 - 2] |
| render_unfocused_fps | 启用 render_unfocused 的窗口在后台运行时的帧率上限（FPS）（另见[窗口规则](rules/window-rules.md#dynamic-effects)，例如 `render_unfocused`） | int | `15` | [1 - 120] |
| screencopy_force_8b | 强制使用 8 位屏幕复制 | bool | `true` |  |
| session_lock_blur | 启用锁屏模糊效果。必须启用 `session_lock_xray` | bool | `false` |  |
| session_lock_xray | 设为 true 时，在锁屏界面下方继续渲染工作区 | bool | `false` |  |
| size_limits_tiled | 是否将 min_size 和 max_size 规则应用于平铺窗口 | bool | `false` |  |
| splash_font_family | 从系统字体中选择用于渲染背景短句的字体（需要重新加载显示器配置才能生效） | string | [[Empty]] |  |
| swallow_exception_regex | 用于匹配窗口 _标题_ 的正则表达式，例如 `wev`。匹配的窗口 _不应_ 被 swallow_regex 指定的窗口吞并。此正则表达式匹配父窗口（例如 Kitty 窗口）的标题，前提是该标题会随其中运行的进程而变化 | string | [[Empty]] |  |
| swallow_regex | 用于匹配应被吞并的窗口（通常是终端）的 _类名_ 的正则表达式 | string | [[Empty]] |  |
| vrr | 控制显示器的 VRR（可变刷新率，即自适应同步）。0 - 关闭，1 - 开启，2 - 仅在全屏时开启，3 - 仅在全屏且内容类型为 `video` 或 `game` 时开启 | int | `0` | [0 - 3] |

类别：`misc.col`

| 名称 | 说明 | 类型 | 默认值 | 范围 |
| --- | --- | --- | --- | --- |
| splash | 更改背景随机短句的颜色（需重新加载显示器配置才会生效） | color | `0x55ffffff` |  |


<a id="layers"></a>

### 图层

类别：`layers`

| 名称 | 说明 | 类型 | 默认值 | 范围 |
| --- | --- | --- | --- | --- |
| allow_new_top_layers_over_existing_fullscreen | 设为 false 时，新映射的图层不能绘制在已覆盖该区域的全屏窗口之上。无论此项如何设置，进入全屏都会隐藏此前已存在的所有顶层图层 | bool | `true` |  |
| layers_hog_keyboard_focus | 设为 true 时，支持键盘交互的图层（如 `wofi`、`bemenu`）会在鼠标移动时保持焦点 | bool | `true` |  |

<a id="layout"></a>

### 布局

类别：`layout`

| 名称 | 说明 | 类型 | 默认值 | 范围 |
| --- | --- | --- | --- | --- |
| single_window_aspect_ratio | 当屏幕上只显示一个窗口时，通过留白使窗口符合指定的宽高比。例如，在 16:9 的屏幕上设为 `4 3`，会使窗口以 4:3 的比例居中显示，两侧留白 | vec2 | `{0, 0}` |  |
| single_window_aspect_ratio_tolerance | 设置 `single_window_aspect_ratio` 的容差。如果所需留白小于屏幕高度或宽度的指定比例，就不会尝试调整窗口大小 | float | `0.1` | [0.0 - 1.0] |

<a id="binds"></a>

### 按键绑定

类别：`binds`

| 名称 | 说明 | 类型 | 默认值 | 范围 |
| --- | --- | --- | --- | --- |
| allow_pin_fullscreen | 启用后，允许已固定到所有工作区的窗口进入全屏，并在退出全屏后恢复固定状态 | bool | `false` |  |
| client_requested_fs_uses_layout_handler | 设为 false 时，客户端发起的全屏请求由默认全屏处理程序处理 | bool | `true` |  |
| allow_workspace_cycles | 启用后，每个工作区都会记住上一个工作区。这样，切换到一组工作区中的第一个工作区后，就可以反复切换到上一个工作区，在这组工作区之间循环 | bool | `false` |  |
| disable_keybind_grabbing | 启用后，应用（如 `VMs`）将无法通过请求禁用按键绑定 | bool | `false` |  |
| drag_threshold | 拖动窗口以及使用 `click`/`drag` 按键绑定标志时的移动距离阈值，单位为像素。`0` 表示禁用阈值 | int | `0` | [0 - ...] |
| drag_center_window | 拖动时，是将窗口中心对准指针，还是保持最初抓取的位置 | bool | true |  |
| focus_preferred_method | 设置使用 `hl.dsp.focus({ direction })`、`hl.dsp.window.move({ direction })` 等时查找焦点目标的首选方式。`0` 表示优先选择最近活动的窗口，`1` 表示优先选择与当前窗口共边更长的窗口 | int | `0` | [0 - 1] |
| hide_special_on_workspace_change | 启用后，切换活动工作区（包括切换到其自身）会隐藏新活动工作区所在显示器上的特殊工作区 | bool | `false` |  |
| ignore_group_lock | 启用后，`hl.dsp.window.move({ into_group })` 和 `hl.dsp.window.move({ out_of_group })` 等调度器会忽略各窗口组单独设置的锁定状态 | bool | `false` |  |
| movefocus_cycles_fullscreen | 启用后，当焦点位于全屏窗口时，`hl.dsp.focus({ direction })` 可以查找窗口。禁用时，它只会查找显示器。 | bool | `false` |  |
| movefocus_cycles_groupfirst | 启用后，当焦点位于组内窗口时，`hl.dsp.focus({ direction })` 会先在组内依次切换窗口，到达标签栏任一端后，再移至其他窗口或窗口组 | bool | `false` |  |
| pass_mouse_when_bound | 启用后，即使已触发按键绑定，鼠标事件仍可传给应用或用于拖动窗口 | bool | `false` |  |
| scroll_event_delay | 设置两次传给按键绑定的滚动事件之间的最短等待时间，单位为毫秒 | int | `300` | [0 - 2000] |
| window_direction_monitor_fallback | 启用后，沿指定方向移动窗口或焦点并越过显示器边缘时，会将其移至该方向上的下一台显示器 | bool | `true` |  |
| workspace_back_and_forth | 尝试切换到当前具有焦点的工作区时，会转而切换到上一个工作区，类似于 i3 的 `_auto_back_and_forth_`。`0` 表示禁用，`1` 表示启用，`2` 表示按显示器分别处理 | int | `0` | [0 - 2] |
| workspace_center_on | 切换工作区时，将光标移至工作区中心（0），或移至该工作区上次活动窗口的中心（1） | int | `1` | [0 - 1] |

<a id="xwayland"></a>

### Xwayland

类别：`xwayland`

| 名称 | 说明 | 类型 | 默认值 | 范围 |
| --- | --- | --- | --- | --- |
| enabled | 允许运行使用 X11 的应用 | bool | `true` |  |
| create_abstract_socket | 为 Xwayland 连接创建[抽象 Unix 域套接字](../extra/xwayland.md#abstract-unix-domain-socket)。更改后需重启 Xwayland 才会生效。仅适用于 Linux | bool | `false` |  |
| force_zero_scaling | 在启用了缩放的显示器上，强制将 Xwayland 窗口的缩放比例设为 1 | bool | `false` |  |
| use_nearest_neighbor | 对 Xwayland 应用使用最近邻过滤，使画面呈现清晰的像素块，避免模糊 | bool | `true` |  |

<a id="opengl"></a>

### OpenGL

类别：`opengl`

| 名称 | 说明 | 类型 | 默认值 | 范围 |
| --- | --- | --- | --- | --- |
| nvidia_anti_flicker | 减少 NVIDIA GPU 上的画面闪烁，但在低端 GPU 上可能会掉帧。非 NVIDIA GPU 会忽略此项设置 | bool | `true` |  |

<a id="render"></a>

### 渲染

类别：`render`

| 名称 | 说明 | 类型 | 默认值 | 范围 |
| --- | --- | --- | --- | --- |
| async_commit | 在可能的情况下异步发送 DRM 提交，以降低硬件光标的延迟 | bool | `false` |  |
| cm_auto_hdr | 全屏时根据需要自动切换到 HDR。`0` 表示禁用，`1` 表示切换到 `hdr`，`2` 表示切换到 `hdredid` | int | `1` | [0 - 2] |
| cm_enabled | 是否启用色彩管理管线。更改后需重启 | bool | `true` |  |
| cm_sdr_eotf | 显示 SDR 应用时使用的默认传递函数。`default` 表示使用默认值（sRGB），`gamma22` 表示将未指定的传递函数视为 Gamma 2.2，`gamma22force` 表示将未指定的传递函数和 sRGB 均视为 Gamma 2.2，`srgb` 表示将未指定的传递函数视为 sRGB。可选值：`"default"`/`"gamma22"`/`"gamma22force"`/`"srgb"` | string | `"default"` |  |
| ctm_animation | 是否在色彩变换矩阵（CTM）发生变化时启用渐变动画（用于 hyprsunset）。2 表示 "auto"，在 NVIDIA GPU 上会禁用此动画 | int | `2` | [0 - 2] |
| commit_timing_enabled | 启用提交时序协议。更改后需重启 | bool | `true` |  |
| direct_scanout | 启用直接扫描输出。当屏幕上只有一个全屏应用（如游戏）时，直接扫描输出会尝试降低延迟。如果全屏应用出现画面异常，也建议将此项设为 false。`0` 表示禁用，`1` 表示启用，`2` 表示自动（内容类型为 'game' 时启用） | int | `0` | [0 - 2] |
| expand_undersized_textures | 当纹理尺寸不足时，是延展纹理边缘，还是拉伸整个纹理 | bool | `true` |  |
| fp16_sdr_tf | SDR 模式下 fp16 内部工作缓冲区的传递函数。0 表示使用显示器的传递函数，1 表示使用线性传递函数 | int | `0` | [0 - 1] |
| icc_vcgt_enabled | 使用 ICC 配置文件时，启用向 KMS 发送 VCGT 校正曲线的功能 | bool | `true` |  |
| keep_unmodified_copy | 保留未经修改的 SDR 帧副本，供屏幕共享使用。`0` 表示禁用，`1` 表示启用，`2` 表示自动（在 HDR 模式下使用 SDR 修饰符时启用）。如果截图呈透明状，请设为 1 | int | `2` | [0 - 2] |
| new_render_scheduling | 需要时自动使用三重缓冲，以提高性能较弱设备上的帧率 | bool | `false` |  |
| not_shown_fifo_lock | 控制未显示表面的 fifo 锁定行为。always 表示对所有表面使用 fifo 锁，ignore_unfocused 表示忽略 render_unfocused 窗口，never 表示跳过对不可见表面的锁定 | int | `0` | [0 - 2] |
| non_shader_cm | 启用无需着色器的色彩管理（CM）。`0` 表示禁用，`1` 表示尽可能启用，`2` 表示仅在直接扫描输出（DS）和直通模式下启用，`3` 表示禁用并忽略色彩管理问题。可选值：[0 - 3] | int | `2` | [0 - 3] |
| non_shader_cm_interop | `0` 表示全屏时禁用外部色彩变换矩阵（CTM，如 hyprsunset 等工具使用的矩阵），`1` 表示全屏时启用外部 CTM，`2` 表示全屏显示照片、视频或游戏类型的内容时禁用外部 CTM | int | `2` | [0 - 2] |
| send_content_type | 报告内容类型，以便自动切换显示器配置文件（切换期间可能会出现黑屏） | bool | `true` |  |
| use_fp16 | 在内部使用 FP16 缓冲区。`0` 表示禁用，`1` 表示启用，`2` 表示在 HDR 模式下启用 | int | `2` | [0 - 2] |
| use_shader_blur_blend | 使用实验性的模糊背景混合方式（在旋转后的屏幕上会出现画面异常）。如果使用 fp16 或 `keep_unmodified_copy` 时缺少模糊效果，请设为 `true` | bool | `false` |  |
| xp_mode | 禁用后缓冲区和底层图层的渲染 | bool | `false` |  |

在高于 v0.40.0 的 mpv 版本中，必须设置 mpv 选项 `--target-colorspace-hint-mode=source`，`cm_auto_hdr` 才能生效。

<a id="cursor"></a>

### 光标

类别：`cursor`

| 名称 | 说明 | 类型 | 默认值 | 范围 |
| --- | --- | --- | --- | --- |
| default_monitor | 启动时放置光标的默认显示器名称（可通过 `hyprctl monitors` 查看显示器名称） | string | `[[Empty]]` |  |
| enable_hyprcursor | 是否启用 hyprcursor 支持 | bool | `true` |  |
| hide_on_key_press | 按下任意键时隐藏光标，直到鼠标移动 | bool | `false` |  |
| hide_on_tablet | 如果最近一次输入来自数位板，则隐藏光标，直到收到鼠标输入 | bool | `false` |  |
| hide_on_touch | 如果最近一次输入为触摸输入，则隐藏光标，直到收到鼠标输入 | bool | `true` |  |
| hotspot_padding | 屏幕边缘与光标之间的间距，单位为逻辑像素 | int | `0` | [0 - 20] |
| inactive_timeout | 光标停止活动多少秒后将其隐藏。设为 `0` 表示永不因闲置而隐藏 | float | `0` | [0 - 20] |
| invisible | 不渲染光标 | bool | `false` |  |
| min_refresh_rate | `no_break_fs_vrr` 生效时，光标移动所用的最低刷新率。请设为显示器支持的最低刷新率或更高的值 | int | `24` | [10 - 500] |
| no_break_fs_vrr | 对于启用了可变刷新率（VRR）的全屏应用，禁止因光标移动而调度新帧，以避免帧率突增（可能需要将 `no_hardware_cursors` 设为 `1`）。`0` 表示禁用，`1` 表示启用，`2` 表示自动（内容类型为 'game' 时启用） | int | `2` | [0 - 2] |
| no_hardware_cursors | 禁用硬件光标。`0` 表示尽可能使用硬件光标，`1` 表示不使用硬件光标，`2` 表示自动（使用画面撕裂时禁用硬件光标） | int | `2` | [0 - 2] |
| no_warps | 设为 true 时，在许多情况下（如切换焦点、触发按键绑定等）都不会自动移动光标 | bool | `false` |  |
| persistent_warps | 当窗口重新获得焦点时，光标会回到上次在该窗口中的相对位置，而非窗口中心 | bool | `false` |  |
| sync_gsettings_theme | 将 XCursor 主题与 GSettings 同步。加载主题时，会将 cursor-theme 和 cursor-size 写入 GSettings，使大多数采用客户端装饰（CSD）的 GTK 客户端使用相同的 XCursor 主题和光标大小 | bool | `true` |  |
| use_cpu_buffer | 使硬件光标使用 CPU 缓冲区。在 NVIDIA GPU 上使用硬件光标需要此设置。`0` 表示禁用，`1` 表示启用，`2` 表示自动（使用 NVIDIA GPU 时启用） | int | `2` | [0 - 2] |
| warp_back_after_non_mouse_input | 使用非鼠标输入移动光标后，重新使用鼠标时，将光标移回原先的位置 | bool | `false` |  |
| warp_on_change_workspace | 切换工作区后，将光标移至该工作区上次获得焦点的窗口。`0` 表示禁用，`1` 表示启用，`2` 表示强制执行（忽略 cursor:no_warps 选项） | int | `0` | [0 - 2] |
| warp_on_monitor_change | 将焦点切换到另一台显示器时，将光标移至该显示器上次获得焦点的窗口。`-1` 表示沿用 `cursor:warp_on_change_workspace` 的值，`0` 表示禁用，`1` 表示启用，`2` 表示强制执行，即使启用了 `cursor:no_warps` 也会移动光标 | int | `-1` | [-1 - 2] |
| warp_on_toggle_special | 切换特殊工作区的显示状态时，将光标移至上次获得焦点的窗口。`0` 表示禁用，`1` 表示启用，`2` 表示强制执行（忽略 cursor:no_warps 选项） | int | `0` | [0 - 2] |
| zoom_detached_camera | 放大时，视野不再跟随鼠标移动。只有当鼠标越过屏幕边缘时，才移动视野以保持鼠标可见 | bool | `true` |  |
| zoom_disable_aa | 缩放时禁用抗锯齿，使画面呈现清晰的像素块，避免模糊 | bool | `false` |  |
| zoom_factor | 以光标为中心的放大倍数，效果类似放大镜。最小值为 1.0（表示不缩放） | float | `1.0` | [1 - 10] |
| zoom_rigid | 缩放视图是严格跟随光标（只要条件允许，光标就始终居中），还是宽松地跟随光标 | bool | `false` |  |

<a id="ecosystem"></a>

### 生态系统

类别：`ecosystem`

| 名称 | 说明 | 类型 | 默认值 | 范围 |
| --- | --- | --- | --- | --- |
| enforce_permissions | 是否启用[权限控制](advanced-configuration/permissions.md) | bool | `false` |  |
| no_donation_nag | 禁用每年出现两次的捐赠提示弹窗 | bool | `false` |  |
| no_update_news | 禁用将 Hyprland 更新到新版本时出现的弹窗 | bool | `false` |  |

<a id="quirks"></a>

### 兼容性调整

类别：`quirks`

| 名称 | 说明 | 类型 | 默认值 | 范围 |
| --- | --- | --- | --- | --- |
| prefer_hdr | 将 HDR 模式报告为首选模式。`0` - 禁用，`1` - 始终报告，`2` - 仅对 gamescope 报告 | int | `0` | [0 - 1] |
| skip_non_kms_dmabuf_formats | 不报告无法导入 KMS 的 dmabuf 格式 | bool | `false` |  |

某些客户端要求显示器在客户端启动前就已进入 HDR 模式。这会导致 HDR 无法自动启用，并可能引起白屏和闪烁。使用 `prefer_hdr` 可解决此问题。

<a id="input-capture"></a>

### 输入捕获

类别：`input-capture`

| 名称 | 说明 | 类型 | 默认值 | 范围 |
| --- | --- | --- | --- | --- |
| capture_modifiers | 启用后，修饰键也会被捕获并发送给程序 | bool | `false` |  |
| enforce_barriers | 启用后，收到无效的输入屏障时会抛出 Wayland 错误 | bool | `true` |  |

<a id="debug"></a>

### 调试

> [!WARNING]
> 这些设置仅供开发和测试使用。请勿在日常配置中更改它们。

类别：`debug`

| 名称 | 说明 | 类型 | 默认值 | 范围 |
| --- | --- | --- | --- | --- |
| colored_stdout_logs | 在输出到 stdout 的日志中启用彩色显示 | bool | `true` |  |
| damage_blink | （警告：闪烁可能诱发癫痫！）让损伤跟踪检测到的更新区域闪烁 | bool | `false` |  |
| damage_tracking | 仅重绘画面中需要更新的部分。请**勿**更改。None - 0，monitor - 1，full - 2 | int | `2` | [0 - 2] |
| disable_logs | 禁用日志文件写入 | bool | `true` |  |
| disable_scale_checks | 禁用对缩放因子的校验。这会导致像素对齐错误和舍入误差 | bool | `false` |  |
| disable_time | 禁用日志中的时间记录 | bool | `true` |  |
| ds_handle_same_buffer | 对缓冲区未修改时的直接扫描输出进行特殊处理 | bool | `true` |  |
| ds_handle_same_buffer_fifo | 对缓冲区未修改时的直接扫描输出进行特殊处理，解除 fifo 锁定 | bool | `true` |  |
| enable_stdout_logs | 启用向 stdout 输出日志 | bool | `false` |  |
| error_limit | 限制显示的配置文件解析错误数量 | int | `5` | [0 - 20] |
| error_position | 设置错误提示栏的位置。`0` - 顶部，`1` - 底部 | int | `0` | [0 - 1] |
| fifo_pending_workaround | 待处理列表为空时使用的 fifo 变通方案 | bool | `false` |  |
| full_cm_proto | 声明支持颜色管理协议的所有功能（需要重启） | bool | `false` |  |
| gl_debugging | 使用 glGetError 和 EGL_KHR_debug 启用 OpenGL 调试，更改后需要重启 | bool | `false` |  |
| invalidate_buffers | 允许将缓冲区标记为无效（此举可提高性能，但在某些系统上会导致画面异常）。0 - 不允许，1 - 允许 | int | `1` | [0 - 1] |
| log_damage | 启用损伤区域日志记录 | bool | `false` |  |
| manual_crash | 先设为 1，再改回 0，即可使 Hyprland 崩溃 | int | `0` | [0 - 1] |
| overlay | 显示调试用的性能叠加层。请禁用 VFR 以获得准确结果 | bool | `false` |  |
| pass | 启用渲染通道调试 | bool | `false` |  |
| render_solitary_wo_damage | 即使损伤区域为空，也渲染唯一的窗口 | bool | `false` |  |
| suppress_errors | 启用后，Hyprland 将不再显示配置文件解析错误 | bool | `false` |  |
| vfr | 控制 Hyprland 是否启用 VFR。强烈建议保持启用以节省资源 | bool | `true` |  |

<a id="experimental"></a>

### 实验性功能

类别：`experimental`

| 名称 | 说明 | 类型 | 默认值 | 范围 |
| --- | --- | --- | --- | --- |
| wp_cm_1_2 | 允许使用 wp-cm-v1 的第 2 版 | bool | `false` |  |

<a id="more"></a>

### 更多选项

其他页面还介绍了适用于特定布局或场景的配置选项。可通过侧边栏查看更多页面，尤其是各布局的页面。
