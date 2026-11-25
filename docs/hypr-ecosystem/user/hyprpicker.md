# hyprpicker

[hyprpicker](https://github.com/hyprwm/hyprpicker) 是一款方便的小工具，可在 Hyprland 中从屏幕上取色。

<a id="configuration"></a>

## 配置

无需配置，通过启动参数即可调整其行为：

| 选项 | 说明 | 参数 |
| --- | --- | --- |
| `-a`/`--autocopy` | 自动将输出复制到剪贴板（需要 wl-clipboard） | [[Empty]] |
| `-f`/`--format=` | 指定输出格式 | `cmyk` \| `hex` \| `rgb` \| `hsl` \| `hsv` |
| `-o`/`--output-format=` | 指定输出颜色时使用的格式字符串 | 格式字符串，例如 "rgb({0}, {1}, {2})" |
| `-n`/`--notify` | 取色后发送桌面通知（需要 notify-send 和 dunst 等通知守护进程） | [[Empty]] |
| `-b`/`--no-fancy` | 禁用“花式”输出（即彩色输出） | [[Empty]] |
| `-h`/`--help` | 显示帮助信息 | [[Empty]] |
| `-r`/`--render-inactive` | 渲染非活动显示器的画面，使其保持静止 | [[Empty]] |
| `-z`/`--no-zoom` | 禁用放大镜 | [[Empty]] |
| `-q`/`--quiet` | 禁用大部分日志，保留错误信息 | [[Empty]] |
| `-v`/`--verbose` | 输出更详细的日志 | [[Empty]] |
| `-t`/`--no-fractional` | 禁用分数缩放支持 | [[Empty]] |
| `-d`/`--disable-hex-preview` | 禁用十六进制颜色值的实时预览 | [[Empty]] |
| `-l`/`--lowercase-hex` | 以小写字母输出十六进制颜色值 | [[Empty]] |
| `-s`/`--scale=scale` | 设置放大倍数 | 1.0 到 10.0 之间的浮点数 |
| `-u`/`--radius=radius` | 设置圆的半径 | 1 到 1000 之间的整数 |
| `-N`/`--name` | 如果所选颜色有对应的标准名称，则复制该名称，取代指定格式的颜色值（需要 -a） | [[Empty]] |
| `-V`/`--version` | 输出版本信息 | [[Empty]] |
