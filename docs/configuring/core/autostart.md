# 自动启动

可以使用 `hyprland.start` 事件自动启动应用：

```lua
hl.on("hyprland.start", function()
    hl.exec_cmd(terminal)
    hl.exec_cmd("nm-applet")
    hl.exec_cmd("waybar & hyprpaper & firefox") -- 运行 waybar、hyprpaper 和 firefox
end)
```

同样，可以监听 `hyprland.shutdown`，在 Hyprland 退出时启动进程。有关 `hl.on` 的更多信息，请参阅[事件](advanced-configuration/events.md)。

