# systemd

<a id="preface"></a>

## 前言

按照 systemd 的设计，运行 Hyprland 等 Wayland 合成器时应启动 `graphical-session.target`。某些程序依赖 `graphical-session.target` 来启动其服务。最典型的例子是 `xdg-desktop-portal` 服务，屏幕共享、GTK 应用程序切换配色方案等功能都需要它。

<a id="hyprland-sessiontarget"></a>

## hyprland-session.target

以前需要手动配置这一步，现在 Hyprland 已集成此功能，会自动处理。如果你使用了本文旧版本中的自定义 `hyprland-session.target`，可以通过 `systemctl --user revert hyprland-session.target` 将其清理掉。还应从配置中*移除*所有遗留的 `systemctl` 命令，例如：

```lua
hl.on("hyprland.start", function()
    hl.exec_cmd("systemctl --user start hyprland-session.target")
end)

hl.on("hyprland.shutdown", function()
    os.execute("systemctl --user stop graphical-session.target")
end)
```

> [!NOTE]
> systemd 的设计假定同一用户不会同时运行多个图形会话（即多个合成器）。如果你确实这样做，请注意，退出一个 Hyprland 实例会停止 `graphical-session.target`，并可能影响仍在运行的其他会话。
>
> 设置 `HYPRLAND_NO_SD_TARGET` 可以避免这种情况，但也会使 `hyprland-session.target` 和 `graphical-session.target` 从一开始就无法*启动*。你可以根据上面的 Lua 事件监听示例调整配置，让会话按预期运行。

<a id="uwsm"></a>

## UWSM

UWSM 会自动启动 `graphical-session.target`。

如果你想使用 systemd 的高级功能，可以了解一下 [UWSM](../../useful-utilities/uwsm.md)。
