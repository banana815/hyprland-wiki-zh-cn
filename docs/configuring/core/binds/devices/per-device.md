# 按设备设置按键绑定

<a id="per-device-binds"></a>

## 按设备设置按键绑定

可以使用 `device` 标志为特定设备设置按键绑定。该标志是一个表，其中包含 `inclusive` 标志和设备列表。

如果将 `inclusive` 设为 true，则只有列表中指定的设备能触发该按键绑定。设为 false 时，除列表中指定的设备外，其他所有设备都能触发该按键绑定。省略 `inclusive` 时，其默认值为 true。

在 `list` 字段中以逗号分隔的字符串列表指定设备。也可以用设备标签代替设备名称，标签可通过[按设备配置](../../devices.md)设置。

<a id="examples"></a>

### 示例

```lua
hl.bind(keys, dispatcher(params), { device = { inclusive = true, list = { "device1", "device2" } } })
```

```lua
-- 只有 example-keyboard-1 可以使用此绑定
hl.bind("SUPER + Q", hl.dsp.exec_cmd("kitty"), { device = { inclusive = true, list = { "example-keyboard-1" } } })

-- 除 razer-keyboard 和 asus-keyboard 外，所有键盘都可以使用此绑定
hl.bind("SUPER + Q", hl.dsp.exec_cmd("kitty"), { device = { inclusive = false, list = { "razer-keyboard", "asus-keyboard" } } })
```

可以使用 `hyprctl devices` 查看设备名称。
