# 显示器

<a id="fields"></a>

## 字段

除 `output` 外，所有字段均为可选项，省略时会使用合理的默认值。

| 字段 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| output | 输出名称，或带有 `desc:...` 前缀的描述 | string | [[Required]] |
| disabled | 将显示器从布局中移除 | bool | `false` |
| mode | 分辨率和刷新率（例如 `"1920x1080@144"`）。有关预定义模式，请参阅[说明](modes.md#modes)。可选值：`mode`/`"preferred"`/`"highres"`/`"highrr"`/`"maxwidth"` | string | `"preferred"` |
| scale | 缩放比例（例如 `1.5`）。`"auto"` 表示根据显示器的 PPI（每英寸像素数）确定缩放比例。可选值：`scale`/`"auto"` | float/string | `"auto"` |
| transform | 旋转或翻转变换（0–7） | int | 0 |
| position | 在虚拟布局中的位置（例如 `"1920x0"`）。有关预定义位置，请参阅[说明](positioning.md#positions) | string | `"auto"` |
| mirror | 要镜像的源输出名称 | string | [[Empty]] |
| bitdepth | 位深。可选值：`8`/`10` | int | `8` |
| cm | 色彩管理预设 | string | `"srgb"` |
| sdr_eotf | SDR 传递函数。可选值：`"default"`/`"gamma22"`/`"srgb"` | string | `"default"` |
| vrr | 可变刷新率（VRR）模式 | int | `0` |
| icc | ICC 配置文件的绝对路径 | string | [[Empty]] |
| reserved_area | 预留区域：使用一个 `int` 值统一设置四边，或使用表分别设置各边 | css_gaps | `0` |
| supports_wide_color | 强制启用广色域（-1 = 关闭，0 = 自动，1 = 开启） | int | `0` |
| supports_hdr | 强制启用 HDR 支持。-1 = 关闭，0 = 自动，1 = 开启。取值范围：[-1 - 1] | int | `0` |
| sdrbrightness | HDR 模式下的 SDR 亮度 | float | `1.0` |
| sdrsaturation | HDR 模式下的 SDR 饱和度 | float | `1.0` |
| sdr_min_luminance | SDR→HDR 映射所用的 SDR 最低亮度 | float | `0.2` |
| sdr_max_luminance | SDR 最高亮度 | int | `80` |
| min_luminance | 显示器最低亮度 | float | `-1` |
| max_luminance | 显示器可达到的最高亮度 | int | `-1` |
| max_avg_luminance | 显示器可达到的最高平均亮度 | int | `-1` |

将 `output` 留空即可定义一条后备规则，在其他规则均不匹配时使用。

```lua
hl.monitor({ output = "", mode = "preferred", position = "auto", scale = 1 })
```

这样，任何没有显式指定规则的显示器都会自动放置在其他显示器的右侧，并使用自身的首选分辨率。

<a id="general"></a>

## 概述

要列出所有可用的显示器（包括已启用和未启用的显示器），请使用：

```bash
hyprctl monitors all
```




<details><summary>输出示例</summary>


```
Monitor DP-3 (ID 0):
    2560x1440@165.00000 at 0x0
    description: AOC Q27G2G3R3B RTEN1HA009998
    make: AOC
    model: Q27G2G3R3B
    physical size (mm): 600x340
    serial: RTEN1HA009998
    active workspace: 5 (5)
    special workspace: 0 ()
    reserved: 0 34 0 0
    scale: 1
    transform: 0
    focused: yes
    dpmsStatus: 1
    vrr: false
    solitary: 0
    solitaryBlockedBy: windowed mode,missing candidate
    activelyTearing: false
    tearingBlockedBy: next frame is not torn,user settings,missing candidate
    directScanoutTo: 0
    directScanoutBlockedBy: windowed mode,missing candidate
    disabled: false
    currentFormat: XRGB2101010
    mirrorOf: none
    availableModes: 2560x1440@59.95Hz 2560x1440@165.00Hz 2560x1440@143.91Hz 2560x1440@120.00Hz 1920x1080@120.00Hz 1920x1080@119.88Hz 1920x1080@60.00Hz 1920x1080@60.00Hz 1920x1080@59.94Hz 1920x1080@50.00Hz 1280x1440@59.91Hz 1280x1024@75.03Hz 1280x1024@60.02Hz 1280x720@60.00Hz 1280x720@59.94Hz 1280x720@50.00Hz 1024x768@119.93Hz 1024x768@99.99Hz 1024x768@75.03Hz 1024x768@70.07Hz 1024x768@60.00Hz 832x624@74.55Hz 800x600@119.93Hz 800x600@99.86Hz 800x600@75.00Hz 800x600@72.19Hz 800x600@60.32Hz 800x600@56.25Hz 720x576@50.00Hz 720x576@50.00Hz 720x480@60.00Hz 720x480@60.00Hz 720x480@59.94Hz 720x480@59.94Hz 640x480@119.80Hz 640x480@99.83Hz 640x480@75.00Hz 640x480@72.81Hz 640x480@66.67Hz 640x480@60.00Hz 640x480@59.94Hz 640x480@59.94Hz 720x400@70.08Hz
    colorManagementPreset: srgb
    sdrBrightness: 1
    sdrSaturation: 1
    sdrMinLuminance: 0.2
    sdrMaxLuminance: 80
    hardwareCursorsInUse: true
 ```



</details>

<a id="disabling-a-monitor"></a>

### 禁用显示器

> [!WARNING]
> 禁用显示器会将其从显示器布局中移除，并将其上的所有窗口和工作区移至其余可用的显示器。如果你希望像屏幕保护程序那样仅关闭显示器，请使用 `dpms` [调度器](../dispatchers.md)。

要禁用显示器，请设置 `disabled = true`：

```lua
hl.monitor({ output = "name", disabled = true })
```

<a id="custom-reserved-area"></a>

## 自定义预留区域

预留区域是平铺窗口不会占用的区域。如果你的工作流程需要自定义预留区域，可以通过 `reserved_area` 字段添加。该字段接受单个整数（统一应用于四边），也接受分别指定各边数值的表：

```lua
-- 统一设置所有边
hl.monitor({ output = "name", reserved_area = 10 })

-- 分别设置各边
hl.monitor({ output = "name", reserved_area = { top = 10, bottom = 10, left = 0, right = 0 } })
```

自定义预留区域会叠加到计算得出的预留区域（例如状态栏占用的区域）上，但配置中每台显示器最多只能使用一条这样的规则。

<a id="default-workspace"></a>

## 默认工作区

请参阅[工作区规则](../rules/workspace-rules.md)。

<a id="binding-workspaces-to-a-monitor"></a>

### 将工作区绑定到显示器

请参阅[工作区规则](../rules/workspace-rules.md)。
