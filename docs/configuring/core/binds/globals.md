# 全局快捷键与绑定

<a id="global-keybinds"></a>

## 全局按键绑定

<a id="classic"></a>

### 传统方式

没错，Hyprland 确实支持为 _所有_ 应用设置全局按键绑定，包括 OBS、Discord、Firefox 等。有关按键绑定的用法，请参阅 [`pass`](../dispatchers.md) 和 [`send_shortcut`](../dispatchers.md) 调度器的说明。

以 OBS 为例，假设“开始/停止录制”的按键绑定为 SUPER + F10，要使其全局生效，只需添加以下配置：

```lua
hl.bind("SUPER + F10", hl.dsp.pass({ window = [[class:com\.obsproject\.Studio]] }))
```

`pass` 会自动传递 `PRESS` 和 `RELEASE` 事件，无需设置 `release` 标志。因此，只需一个 `pass` 就能让按住说话功能正常工作，例如：

```lua
-- 将 MOUSE5 传递给 TeamSpeak 3
hl.bind("mouse:276", hl.dsp.pass({ window = "class:TeamSpeak 3" }))
```

你还可以添加快捷键，将其他按键传递给窗口。

```lua
-- 按下 SUPER + F10 时，向 OBS 发送 SUPER + F4。
hl.bind("SUPER + F10", hl.dsp.send_shortcut({ mods = "SUPER", key = "F4", window = "class:(TeamSpeak 3)" }))
```

> [!WARNING]
> 这种方式对所有原生 Wayland 应用都能正常生效。Xwayland 的表现则不太稳定。请确保传递的是“Xorg 全局按键绑定”，否则从另一个 Xwayland 应用传递按键时可能无法生效。

<a id="d-bus-global-shortcuts"></a>

### D-Bus 全局快捷键

> [!NOTE]
> 此功能 _仅_ 在使用 [XDPH](../../../hypr-ecosystem/user/xdg-desktop-portal-hyprland.md) 时可用。

有些应用可能已经支持 xdg-desktop-portal 的 GlobalShortcuts 门户接口。如果你的应用支持，建议用以下方法代替 `pass`：

打开目标应用，然后在终端中运行 `hyprctl globalshortcuts`。该命令会列出当前已注册的快捷键及其说明。

选中所需的快捷键，例如 `coolApp:myToggle`，然后使用 `global` 调度器将其绑定到任意按键组合：

```lua
hl.bind("SUPER + SHIFT + A", hl.dsp.global("coolApp:myToggle"))
```

全局快捷键协议可以发送“activated”（激活）和“deactivated”（停用）两种事件。默认情况下，`global` 调度器会根据触发它的按键输入发送相应事件。例如，如果在松开按键时触发的按键绑定中使用它，它只会发送“deactivated”事件，而应用可能不会响应该事件。要覆盖这一行为并发送指定事件，可向 `global` 传入一个布尔值作为第二个参数（`true` 表示激活事件，`false` 表示停用事件）。
