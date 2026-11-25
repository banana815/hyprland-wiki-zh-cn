# 显示模式

<a id="mode"></a>

## 模式

显示器模式由分辨率和刷新率共同决定。要查看可用模式，请运行 `hyprctl monitors` 并查找 `availableModes` 字段。各模式按分辨率从高到低排列。某些模式可能会重复出现，或显示的刷新率可能有偏差。

<a id="modes"></a>

### 模式

**预定义模式不能组合使用**，只能选择一种。

- `preferred` - 使用显示器的首选分辨率和刷新率。
- `highres` - 使用显示器支持的最高分辨率。
- `highrr` - 使用显示器支持的最高刷新率。
- `maxwidth` - 使用显示器支持的水平像素数最多的分辨率。

<a id="custom-modelines"></a>

## 自定义显示时序（modeline）

将 modeline 字符串传给 `mode` 字段即可设置自定义显示时序：

```lua
hl.monitor({
  output = "DP-1",
  mode = "modeline 1071.101 3840 3848 3880 3920 2160 2263 2271 2277 +hsync -vsync",
})
```

有关显示时序的更多信息，请参阅 [XFree86 显示时序](https://wikipedia.org/wiki/XFree86_Modeline)和[协调视频时序](https://wikipedia.org/wiki/Coordinated_Video_Timings)。

<a id="mirrored-displays"></a>

## 显示器镜像

要镜像某台显示器的画面，请使用 `mirror` 字段：

```lua
hl.monitor({ output = "DP-3", mode = "1920x1080@60", position = "0x0", scale = 1, mirror = "DP-2" })
hl.monitor({ output = "", mode = "preferred", position = "auto", scale = 1, mirror = "DP-1" })
```

镜像显示不会为第二台显示器“重新渲染”所有内容。因此，将 1080p 屏幕镜像到 4K 显示器时，4K 显示器上呈现的画面仍为 1080p。如果两台显示器的宽高比不同（例如 16:9 和 16:10），画面也会被压缩或拉伸。

<a id="vrr"></a>

## VRR

可以全局启用 VRR，也可以为单台显示器启用。

可以在调用 `hl.monitor()` 时通过 `vrr` 字段为单台显示器配置 VRR。全局配置见[配置选项](../config-options.md)。

可用值：
- `-1` - 遵循全局开关设置
- `0` - 关闭
- `1` - 开启
- `2` - 仅在全屏时开启
- `3` - 仅在全屏且内容类型为 `video` 或 `game` 时开启

```lua
hl.monitor({ output = "DP-1", vrr = 3 })
```
