# hyprqt6engine

[hyprqt6engine](https://github.com/hyprwm/hyprqt6engine) 为 Qt 6 应用提供主题。
它可替代 qt6ct，兼容 KDE 应用和 KColorScheme。

<a id="usage"></a>

## 用法

安装后，设置 `QT_QPA_PLATFORMTHEME=hyprqt6engine`。
你可以在 Hyprland 配置中通过 `env=` 设置这个环境变量，也可以在 `/etc/environment` 中设置，使其对整个系统生效。

<a id="configuration"></a>

## 配置

配置文件位于 `~/.config/hypr/hyprqt6engine.conf`。

<a id="theme"></a>

### 主题

类别 `theme:`

| 变量 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| `color_scheme` | 配色方案的完整路径。可以使用 qt6ct 主题或 KColorScheme 配色方案。留空则使用默认配色 | string | [[Empty]] |
| `icon_theme` | 要使用的图标主题名称 | string | [[Empty]] |
| `style` | 要使用的控件样式，例如 Fusion 或 kvantum-dark | string | `Fusion` |
| `font_fixed` | 等宽字体的字体族 | string | `monospace` |
| `font_fixed_size` | 等宽字体的字号 | int | `11` |
| `font` | 常规字体的字体族 | string | `Sans Serif` |
| `font_size` | 常规字体的字号 | int | `11` |

<a id="misc"></a>

### 杂项

类别 `misc:`

| 变量 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| `single_click_activate` | 是否单击即可激活或打开项目 | bool | `true` |
| `menus_have_icons` | 上下文菜单是否显示图标 | bool | `true` |
| `shortcuts_for_context_menus` | 上下文菜单项是否显示对应的键盘快捷键 | bool | `true` |
