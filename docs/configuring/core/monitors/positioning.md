# 显示器排列

> [!WARNING]
> 显示器的位置不能重叠。如果发生重叠，Hyprland 会发出警告，并且不会注册位置重叠的显示器。

<a id="position"></a>

## 位置

位置按缩放和变换后的分辨率计算。例如，要将缩放倍数为 2 的 4K 显示器放在 1080p 显示器左侧，应将第二台显示器的位置设为 `1920x0`（3840 / 2）。如果这台 4K 显示器还旋转了 90 度（竖屏），则应使用 `1080x0`。

如果按指定倍数缩放后得不到整数逻辑像素，就会出现“缩放倍数无效”（Invalid scale）警告。分辨率的宽和高分别除以缩放倍数后都必须是整数（不能有小数）。例如：
- 1920×1080 / 1.5 = 1280×720 → 有效
- 1920×1080 / 1.4 = 1371.4286×771.42857 → 无效。

<a id="positions"></a>

### 位置选项

- `auto` - 由 Hyprland 决定位置。默认情况下，每台新显示器都会放在已有显示器的右侧，定位时以显示器左上角为基准点。
- `auto-right/left/up/down` - 将显示器放在其他显示器的右侧、左侧、上方或下方，同样以各显示器的左上角为基准点。
- `auto-center-right/left/up/down` - 将显示器放在其他显示器的右侧、左侧、上方或下方，但计算位置时改用各显示器的中心点作为基准点，而非左上角。

如果为显示器布局中的第一个输出指定了带方向的特殊位置，方向会被忽略，该显示器会放在 (0,0)。

方向始终从中心向外延伸。例如，可以先指定 `auto-up`，再指定 `auto-left`，此时向左排列的显示器会位于原点左上方。也可以多次指定同一方向，后续显示器会沿该方向继续排列。


<details><summary>示例</summary>


```lua
hl.monitor({ output = "DP-1", mode = "1920x1080@120Hz", position = "0x0", scale = 1 })
hl.monitor({ output = "DP-2", mode = "1920x1080@120Hz", position = "1920x0", scale = 1 })
```

会让 Hyprland 将 DP-2 放在 DP-1 的_右侧_，而

```lua
hl.monitor({ output = "DP-1", mode = "1920x1080@120Hz", position = "1920x0", scale = 1 })
hl.monitor({ output = "DP-2", mode = "1920x1080@120Hz", position = "0x0", scale = 1 })
```

会让 Hyprland 将 DP-1 放在 DP-2 的_右侧_。

`position` 可以包含_负值_，因此上面的示例也可以写成：

```lua
hl.monitor({ output = "DP-1", mode = "1920x1080@120Hz", position = "0x0", scale = 1 })
hl.monitor({ output = "DP-2", mode = "1920x1080@120Hz", position = "-1920x0", scale = 1 })
```

再举一个例子，

```lua
hl.monitor({ output = "DP-1", mode = "1920x1080@120Hz", position = "0x0", scale = 1 })
hl.monitor({ output = "DP-2", mode = "1920x1080@120Hz", position = "0x-1080", scale = 1 })
```

会让 Hyprland 将 DP-2 放在 DP-1 的_上方_，而

```lua
hl.monitor({ output = "DP-1", mode = "1920x1080@120Hz", position = "0x0", scale = 1 })
hl.monitor({ output = "DP-2", mode = "1920x1080@120Hz", position = "0x1080", scale = 1 })
```

会让 Hyprland 将 DP-2 放在 DP-1 的_下方_。



</details>

<a id="rotation"></a>

## 旋转

要旋转显示器，请使用 `transform` 字段：

```lua
hl.monitor({ output = "eDP-1", mode = "2880x1800@90", position = "0x0", scale = 1, transform = 1 })
```

各变换值的含义如下：
- 0：正常（不做变换）
- 1：旋转 90 度
- 2：旋转 180 度
- 3：旋转 270 度
- 4：翻转
- 5：翻转并旋转 90 度
- 6：翻转并旋转 180 度
- 7：翻转并旋转 270 度
