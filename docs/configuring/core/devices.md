# 设备

有关全局设备配置，请参阅[配置选项页面](config-options.md)。本页主要介绍如何为单个设备配置选项。

使用 `hl.device()` 函数可以为单个设备设置基本配置：

```lua
hl.device({
    name = "my-epic-keyboard",
    sensitivity = -0.5
})
```

查看 `hyprctl devices` 的输出即可找到 `name`。

在此表中指定所需的配置选项。除以下选项外，均可设置任意 [`input` 选项](config-options.md#input)。**例外如下**：
- `force_no_accel`
- 用于配置窗口管理的选项，例如 `follow_mouse`、`follow_mouse_threshold`、`float_switch_override_focus`、`mouse_refocus`、`special_fallthrough` 等。

对于数位板，还可以使用 `output` 设置将其绑定到指定的输出。请使用 `Tablet` 的名称，不要使用 `Tablet Pad` 或 `Tablet Tool` 的名称。

以下附加属性只能在单个设备的配置中指定：
- `enabled`（仅适用于鼠标、触控板、触摸设备、键盘和数位板）
  - 启用或禁用设备（将设备连接到屏幕光标或断开连接）
  - 默认值：`true`
- `keybinds`（仅适用于发送按键事件的设备）
  - 启用或禁用该设备的按键绑定
  - 默认值：`true`
- `tags`（仅适用于键盘和指针设备）
  - 以逗号分隔的标签列表，可用于在[针对单个设备的按键绑定](binds/devices/per-device.md)中对设备进行分组或为设备指定别名
  - 默认值：`""`

> [!NOTE]
> 默认情况下，单个设备的键盘布局不会改变按键绑定使用的键位映射。例如，如果全局键位映射为 `us`，而某个设备使用 `fr`，按键绑定仍会按 `us` 布局响应。
>
> 你可以通过设置 `resolve_binds_by_sym = 1` 来改变这一行为。这样，你就需要输入按键绑定中指定的符号才能触发该绑定。
