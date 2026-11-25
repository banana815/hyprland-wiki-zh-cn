# hyprsunset

[hyprsunset](https://github.com/hyprwm/hyprsunset) 是一款为系统提供蓝光过滤功能的小工具。

与屏幕着色器相比，更推荐这种方式，因为它的滤镜效果_不会_出现在录屏或截图中。

hyprsunset 还提供伽马滤镜，可用来调节不支持软件亮度控制的显示器的感知亮度，也可以将感知亮度降至显示器的最低亮度以下。

<a id="configuration"></a>

## 配置

可通过配置文件 `~/.config/hypr/hyprsunset.conf` 配置 hyprsunset。
没有此文件也能运行 hyprsunset，但建议使用。

hyprsunset 使用配置方案来确定何时更改色温和伽马值。
你可以按需定义任意数量的配置方案。
每个方案都会在其指定的时间生效，并重置其他方案设置的所有选项。

启动时，hyprsunset 会应用当前时段对应的配置方案。
例如，使用下方的示例配置在 20:00 启动 hyprsunset 时，第一个方案会生效，屏幕显示基本没有变化。
到了 21:00，hyprsunset 会自动应用新方案。

| 变量 | 说明 | 类型 | 默认值 |
| -- | -- | -- | -- |
| `max-gamma` | 伽马值允许达到的最大百分比，最高为 `200`%。主要用于通过 IPC 控制 hyprsunset 的场景 | int | `100` |

<a id="profile"></a>

### 配置方案

| 变量 | 说明 | 类型 | 默认值 |
| -- | -- | -- | -- |
| `time` | 方案生效的时间。必须使用 `<hours>:<minutes>` 格式 | string | `00:00` |
| `temperature` | 屏幕色温。值越低，色调越暖 | int | `6000` |
| `gamma` | 屏幕的感知亮度。可将感知亮度降至屏幕的最低亮度以下 | float | `1.0` |
| `identity` | 启用后，hyprsunset 会忽略 temperature 的值，仅通过 gamma 调节感知亮度 | bool | `false` |
| `on-switch` | 方案生效时执行的命令 | string | [[Empty]] |


<details><summary>示例</summary>


```ini
max-gamma = 150

profile {
    time = 7:30
    identity = true
}

profile {
    time = 21:00
    temperature = 5500
    gamma = 0.8
}
```



</details>

<a id="usage"></a>

## 用法

要让 hyprsunset 自动启动，请将 `hyprsunset` 添加到 `hyprland.lua` 的自动启动部分。


也可以通过命令行参数控制 hyprsunset。
运行 `hyprsunset --temperature 5000` 会覆盖当前方案的色温设置。
新方案生效时，其色温设置会覆盖命令行指定的值。

有关命令行参数的更多信息，请运行 `hyprsunset --help`。

<a id="ipc"></a>

## IPC

`hyprsunset` 支持通过 hyprctl 进行 IPC 通信。
色温和伽马滤镜均可调节：

```sh
# 启用蓝光过滤
hyprctl hyprsunset temperature 2500
# 禁用蓝光过滤
hyprctl hyprsunset identity

# 将伽马值设为 50%
hyprctl hyprsunset gamma 50
# 将伽马值提高 10%
hyprctl hyprsunset gamma +10

# 按当前配置方案重置配置
hyprctl hyprsunset reset
# 将该值重置为当前配置方案中的值
hyprctl hyprsunset reset temperature
hyprctl hyprsunset reset gamma
hyprctl hyprsunset reset identity

# 打印当前配置方案
hyprctl hyprsunset profile
```

其他软件可以通过此接口在一天中的不同时段调整色温，也可以调节显示器的感知亮度，例如使用以下 Hyprland 键位绑定：
```lua
hl.bind("XF86MonBrightnessUp", hl.dsp.exec_cmd("hyprctl hyprsunset gamma +10"), { repeating = true, locked = true, })
hl.bind("XF86MonBrightnessDown", hl.dsp.exec_cmd("hyprctl hyprsunset gamma -10"), { repeating = true, locked = true, })
```

> [!WARNING]
> 调节伽马会降低色彩准确度。
> 如果显示器支持通过软件控制亮度，强烈建议优先使用该功能。

<a id="on-switch-command"></a>

## 切换方案时执行的命令

以下示例展示了 `on-switch` 命令的用法。
在此示例中，每个方案都会运行一条设置 GTK 主题的命令，以实现浅色和深色模式切换。
方案生效时，会执行该方案指定的 `on-switch` 命令：

```ini
# 浅色模式
profile {
	time = 8:00
	temperature = 6000
	on-switch = gsettings set org.gnome.desktop.interface color-scheme "prefer-light"
}

# 深色模式
profile {
	time = 20:00
	temperature = 1500
	on-switch = gsettings set org.gnome.desktop.interface color-scheme "prefer-dark"
}
```

此功能还可用于更新 Omarchy 的夜灯状态指示器，只需将 `on-switch` 命令设为 `omarchy-shell -q nightlight refresh`。
