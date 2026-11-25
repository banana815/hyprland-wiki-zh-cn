# 动画

<a id="general"></a>

## 概述

使用 `hl.animation()` 方法声明动画。

语法：
```
hl.animation({ leaf = string, enabled = bool, speed = float, curve = string, style? = string })
```
- `leaf` 指定动画的作用范围。请参阅[动画树](#animation-tree)。
- `enabled` 可设为 `true` 以启用动画，或设为 `false` 以禁用动画。_注意：_ 如果设为 `false`，可省略后续参数。
- `speed` 表示动画持续多少个*十分之一秒*（每个单位为 100 毫秒）。例如，`speed = 1` 表示动画持续 100 毫秒。
- `bezier`/`spring` 指定曲线名称，详见[曲线](#curves)。
- `style` 指定动画样式。请参阅[动画树](#animation-tree)。

<a id="examples"></a>

### 示例

```lua
hl.animation({ leaf = "workspaces", enabled = true, speed = 8, bezier = "my_epic_bezier" })
hl.animation({ leaf = "windows", enabled = true, speed = 10, spring = "my_epic_spring", style = "slide"})
hl.animation({ leaf = "fade", enabled = 0 })
```

<a id="animation-tree"></a>

### 动画树

动画按树状结构组织。未设置的动画会继承父节点的值。

```plain
global
  ↳ windows - styles: slide, popin, gnomed
    ↳ windowsIn - window open - styles: same as windows
    ↳ windowsOut - window close - styles: same as windows
    ↳ windowsMove - everything in between, moving, dragging, resizing.
  ↳ layers - styles: slide, popin, fade
    ↳ layersIn - layer open
    ↳ layersOut - layer close
  ↳ fade
    ↳ fadeIn - fade in for window open
    ↳ fadeOut - fade out for window close
    ↳ fadeSwitch - fade on changing activewindow and its opacity
    ↳ fadeShadow - fade on changing activewindow for shadows
    ↳ fadeGlow - fade on changing activewindow for glow
    ↳ fadeDim - the easing of the dimming of inactive windows
    ↳ fadeLayers - for controlling fade on layers
      ↳ fadeLayersIn - fade in for layer open
      ↳ fadeLayersOut - fade out for layer close
    ↳ fadePopups - for controlling fade on Wayland popups
      ↳ fadePopupsIn - fade in for Wayland popup open
      ↳ fadePopupsOut - fade out for Wayland popup close
    ↳ fadeDpms - for controlling fade when dpms is toggled
  ↳ border - for animating the border's color switch speed
  ↳ borderangle - for animating the border's gradient angle - styles: once (default), loop
  ↳ shadowangle - for animating the shadow's gradient angle - styles: once (default), loop
  ↳ glowangle - for animating the glow's gradient angle - styles: once (default), loop
  ↳ workspaces - styles: slide, slidevert, fade, slidefade, slidefadevert
    ↳ workspacesIn - styles: same as workspaces
    ↳ workspacesOut - styles: same as workspaces
    ↳ specialWorkspace - styles: same as workspaces
      ↳ specialWorkspaceIn - styles: same as workspaces
      ↳ specialWorkspaceOut - styles: same as workspaces
  ↳ zoomFactor - animates the screen zoom
  ↳ monitorAdded - monitor added zoom animation
```

> [!WARNING]
> 为 `*angle` 动画使用 `loop` 样式时，Hyprland 必须按屏幕刷新率 _持续_ 渲染新帧（例如，60 Hz 显示器每秒渲染 60 帧）。这可能会加重 CPU/GPU 的负载，并会影响电池续航。即使动画已禁用或相应的装饰效果不可见，Hyprland 仍会持续渲染。

<a id="curves"></a>

## 曲线

<a id="bezier"></a>

### 贝塞尔曲线

三次[贝塞尔曲线](https://en.wikipedia.org/wiki/B%C3%A9zier_curve)是由 4 个点定义的简单样条曲线，其中中间的两个点可以配置。

```lua
hl.curve( NAME, { type = "bezier", points = { {X0, Y0}, {X1, Y1} } })
```

你可以使用 [cssportal.com](https://www.cssportal.com/css-cubic-bezier-generator/) 设计自己的贝塞尔曲线。如果想选用现成的贝塞尔曲线，可以浏览 [easings.net](https://easings.net)。

<a id="spring"></a>

### 弹簧曲线

弹簧曲线常见于苹果的操作系统中，由质量、刚度和阻尼三个参数定义。通常建议将质量保持为 1，只调整刚度和阻尼。

```lua
hl.curve(NAME, { type = "spring", mass = float, stiffness = float, damping = float })
```

“刚度”越大，运动越快；“阻尼”越大，回弹越弱。

<a id="damping"></a>

#### 阻尼

<a id="critical-damping"></a>

##### 临界阻尼

当弹簧处于临界阻尼状态时，它会迅速稳定在平衡位置，不会越过该位置（即不会回弹）。

当 $\zeta = 1$ 时，弹簧处于临界阻尼状态，其中：

$$
\zeta = \frac{c}{c_c} = \frac{c}{2\sqrt{k\,m}}, \quad
\begin{cases}
c   & \text{阻尼系数*} \\
c_c & \text{临界阻尼系数} \\
k   & \text{刚度} \\
m   & \text{质量}
\end{cases}
$$

> \* 这就是你为曲线指定的阻尼值。

若想让动画响应灵敏、过渡平滑，阻尼值可取 `0.6` 到 `0.8` 左右。

<a id="overdamped"></a>

##### 过阻尼

当 $\zeta > 1$ 时，弹簧处于过阻尼状态。

弹簧缓慢回到平衡位置，不会振荡（即不会回弹）。

<a id="underdamped"></a>

##### 欠阻尼

当 $\zeta < 1$ 时，弹簧处于欠阻尼状态。

弹簧会振荡（回弹），振幅按指数规律衰减\*。

> \* 回弹的幅度随时间呈指数减小。

<a id="examples-1"></a>

### 示例

```lua
hl.curve( "overshoot", { type = "bezier", points = { {0.5, 0.9}, {0.1, 1.1} } } )
hl.curve( "rubber", { type = "spring", mass = 1, stiffness = 70, damping = 10 } )
```

<a id="extras"></a>

### 补充说明

为 `windows` 使用 `popin` 动画样式时，可以指定起始大小的最小百分比。例如，以下设置会让窗口从其大小的 80% 逐渐放大到 100%：

```lua
hl.animation({ leaf = "windows", enabled = true, speed = 8, curve = "default", style = "popin 80%" })
```

为 `workspaces` 使用 `slide`、`slidevert`、`slidefade` 或 `slidefadevert` 动画样式时，可以用百分比指定移动距离。例如，以下设置会让窗口移动屏幕宽度的 20%：

```lua
hl.animation({ leaf = "workspaces", enabled = true, speed = 8, curve = "default", style = "slidefade 20%" })
```

为 `windows` 和 `layers` 使用 `slide` 动画样式时，可以强制指定滑动所用的屏幕边缘，可选值为 `top`、`bottom`、`left` 或 `right`。

```lua
hl.animation({ leaf = "windows", enabled = true, speed = 8, curve = "default", style = "slide left" })
```
