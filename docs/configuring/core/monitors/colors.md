# 颜色与色彩空间

<a id="color-management-presets"></a>

## 色彩管理预设

使用 `cm` 字段可以更改默认的 sRGB 输出预设：

```lua
hl.monitor({ output = "eDP-1", cm = "wide" })
```

支持以下预设：

```plain
auto    - srgb for 8bpc, wide for 10bpc if supported (recommended)
srgb    - sRGB primaries (default)
dcip3   - DCI P3 primaries
dp3     - Apple P3 primaries
adobe   - Adobe RGB primaries
wide    - wide color gamut, BT2020 primaries
edid    - primaries from edid (known to be inaccurate)
hdr     - wide color gamut and HDR PQ transfer function (experimental)
hdredid - same as hdr with edid primaries (experimental)
```

启用 `render:cm_auto_hdr` 后，即使未将 cm 设为 `hdr`，也可以在全屏时使用 HDR。

使用 `sdrbrightness` 和 `sdrsaturation` 可分别控制 HDR 模式下的 SDR 亮度和饱和度。两者的默认值均为 `1.0`。亮度通常应设在 `1.0 - 2.0` 范围内。

```lua
hl.monitor({
  output = "eDP-1",
  cm = "hdr",
  sdrbrightness = 1.2,
  sdrsaturation = 0.98,
})
```

`sdr_eotf` 定义了默认情况下假定 SDR 显示器在显示 sRGB 内容时使用的传递函数。默认值（`"default"`）遵循 `render:cm_sdr_eotf` 的设置。设为 `"srgb"` 可使用分段式 sRGB 传递函数，设为 `"gamma22"` 可使用 Gamma 2.2。

如果显示器支持，建议设置 `bitdepth = 10`，以改善色彩空间的处理效果。

<a id="10-bit-support"></a>

## 10 位色深支持

> [!WARNING]
> 有些显示器标称支持 10 位色深，实际却使用 8 位色深加[帧率控制（FRC）](https://wikipedia.org/wiki/Frame_rate_control)来模拟。这可能会导致严重的视觉疲劳。

Hyprland 中注册的颜色（例如边框颜色）_不支持_ 10 位色深。启用 10 位色深后，某些应用程序 _不支持_ 屏幕捕获。

要为显示器启用 10 位色深支持，请设置 `bitdepth = 10`：

```lua
hl.monitor({ output = "DP-1", bitdepth = 10 })
```

<a id="icc-profiles"></a>

## ICC 配置文件

可以通过 `icc` 字段加载 ICC 配置文件（必须使用绝对路径）：

```lua
hl.monitor({ output = "DP-1", icc = "/path/to/icc.icm" })
```

请注意：
- 路径必须是绝对路径。
- 应用 ICC 配置文件后，系统会自动将该显示器的 `sdr_eotf` 强制设为 `sRGB`，以保证色彩准确性。
- 应用 ICC 配置文件会覆盖色彩管理预设。
- ICC 配置文件与 HDR 游戏从根本上不兼容，同时使用可能会出现异常。
