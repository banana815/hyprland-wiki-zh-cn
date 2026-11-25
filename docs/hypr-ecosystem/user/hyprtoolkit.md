# hyprtoolkit（用户文档）

[hyprtoolkit](https://github.com/hyprwm/hyprtoolkit) 是一个图形界面工具包，用于开发可在 Wayland 上原生运行的应用程序。
它专为 Hyprland 的需求而设计，但通常也能在任何支持现代标准的 Wayland 合成器上运行。

开发者文档请参阅 [hyprtoolkit 开发者文档](../dev/hyprtoolkit.md)。

<a id="configuration"></a>

## 配置

工具包的通用配置文件位于 `~/.config/hypr/hyprtoolkit.conf`。
此文件可用于设置主题和微调部分选项，支持与 Hyprland 相同的颜色选项。

| 变量 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| `background` | 背景色。 | color | `0xFF181818` |
| `base` | 基础色。 | color | `0xFF202020` |
| `text` | 文本颜色。 | color | `0xFFDADADA` |
| `alternate_base` | 备用基础色。 | color | `0xFF272727` |
| `bright_text` | 亮色文本的颜色。 | color | `0xFFFFDEDE` |
| `accent` | 强调色。 | color | `0xFF00FFCC` |
| `accent_secondary` | 辅助强调色。 | color | `0xFF0099F0` |
| `h1_size` | 一级标题的字号。 | int | `19` |
| `h2_size` | 二级标题的字号。 | int | `15` |
| `h3_size` | 三级标题的字号。 | int | `13` |
| `font_size` | 常规文本元素的字号。 | int | `11` |
| `small_font_size` | 小号文本元素的字号。 | int | `10` |
| `icon_theme` | 要使用的图标主题名称。留空时使用找到的第一个图标主题。 | string | [[Empty]] |
| `font_family` | 要使用的字体族名称。 | string | `Sans Serif` |
| `font_family_monospace` | 要使用的等宽字体族名称。 | string | `monospace` |
| `rounding_large` | 大圆角的半径，单位为逻辑像素 | int | `10` |
| `rounding_small` | 小圆角的半径，单位为逻辑像素 | int | `5` |
