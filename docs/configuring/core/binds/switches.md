# 硬件开关

<a id="switches"></a>

## 硬件开关

> [!WARNING]
> systemd-logind 在 `logind.conf` 中的 `HandleLidSwitch` 设置可能与 Hyprland 的笔记本电脑上盖开关配置冲突。

> [!TIP]
> 如果你希望硬件开关平时照常工作，仅在 Hyprland 运行时覆盖其行为，可以使用 `systemd-inhibit`。例如，通过 `systemd-inhibit --what=handle-lid-switch Hyprland` 启动 Hyprland，systemd-logind 就会在 Hyprland 运行期间忽略上盖开关。

硬件开关可用于绑定笔记本电脑合盖、开盖等事件。要查看可用的硬件开关，请运行 `hyprctl devices`。

<a id="examples"></a>

### 示例
```lua
-- 开关状态切换时触发。
hl.bind("switch:[switch name]", hl.dsp.exec_cmd("swaylock"), { locked = true })
-- 开关切换到开启状态时触发。
hl.bind("switch:on:[switch name]", hl.dsp.exec_cmd("notify-send 'yooo'"), { locked = true })
-- 开关切换到关闭状态时触发。
hl.bind("switch:off:[switch name]", hl.dsp.exec_cmd("notify-send 'among us'"), { locked = true })
```
