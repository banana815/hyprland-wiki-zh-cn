# Lua 事件

<a id="events"></a>

## 事件

使用 `hl.on` 可以为事件定义回调函数。可以按需注册任意多个回调函数。

```lua
hl.on("window.active", function(w)
  hl.notification.create({ text = "Window focused: " .. w.title, timeout = 5000, icon = "ok" })
end)
```

如果要处理的事件有多个参数，也可以这样写：

```lua
hl.on("workspace.move_to_monitor", function(ws, m)
  hl.notification.create({
    text = "Workspace: " .. ws.name .. " moved to a monitor at x: " .. m.position.x,
    timeout = 4000,
    icon = "ok"
  })
end)
```

事件列表：

| 事件 | 说明 | 参数 |
| --- | --- | --- |
| config.props_refreshed | 执行属性刷新事件时触发 | bool：如果[属性刷新](lua-utilities.md#prop-refresh)事件按计划执行，则为 `true`；如果通过 Lua 函数提前执行，则为 `false` |
| config.reloaded | 重新加载配置**并应用配置**后触发 | 无 |
| config.unload | 重新加载配置或关闭 Hyprland 时，在即将卸载配置并销毁 Lua 状态之前触发，以便及时关闭或保存相关资源，避免丢失 | 无 |
| hyprland.shutdown | Hyprland 退出前触发一次 | 无 |
| hyprland.start | 启动时触发一次 | 无 |
| input.keyboard.key | 按下或松开按键时触发 | integer：XKB 键码；integer：事件发生时的 Unix 时间戳；integer：松开（0）、按下（1）或重复按键（2） |
| keybinds.submap | 当前按键绑定子映射发生变化时触发。空字符串表示已恢复默认子映射 | string：子映射名称 |
| layer.closed | 图层表面关闭时触发 | LayerSurface |
| layer.opened | 图层表面打开时触发 | LayerSurface |
| monitor.added | 显示器已连接并就绪时触发 | Monitor |
| monitor.focused | 当前活动显示器发生变化时触发 | Monitor |
| monitor.layout_changed | 显示器布局发生变化时触发。添加或移除显示器、更改显示器分辨率或刷新率，或重新加载采用不同规则的配置，都会触发此事件 | 无 |
| monitor.removed | 显示器断开连接并被移除时触发 | Monitor |
| screenshare.state | 屏幕共享会话开始或停止时触发 | Bool：是否正在共享；Integer：类型；String：名称 |
| window.active | 当前活动窗口发生变化时触发 | Window；int（焦点变化的原因） |
| window.bell | 窗口触发系统响铃时触发，即使响铃已静音也会触发 | Window |
| window.class | 窗口的类发生变化时触发 | Window |
| window.close | 窗口关闭时触发。关闭动画播放期间，窗口可能仍然可见 | Window |
| window.destroy | 窗口从合成器中移除时触发。如果窗口有关闭动画，则在动画结束后触发 | Window |
| window.fullscreen | 窗口的全屏状态发生变化时触发 | Window |
| window.kill | 通过 hyprctl kill 强制终止窗口时触发 | Window |
| window.minimize | 窗口请求更改自身的最小化状态时触发 | Window；bool：请求最小化时为 `true`，请求取消最小化时为 `false` |
| window.move_to_workspace | 窗口移至其他工作区时触发 | Window; Workspace |
| window.open | 窗口完成初始化且窗口规则已应用时触发 | Window |
| window.open_early | 窗口已创建并映射时触发，此时仍在应用窗口规则**之前** | Window |
| window.pin | 固定窗口或取消固定窗口时触发 | Window |
| window.title | 窗口标题发生变化时触发 | Window |
| window.update_rules | 重新评估窗口规则时触发，例如窗口标题或窗口类发生变化时 | Window |
| window.urgent | 窗口请求进入 `urgent` 状态时触发 | Window |
| window.update_state | 窗口的桌面状态发生变化时触发。状态表包含各项标志（例如 `pinned` 或 `floating`）。值为 nil 表示相应状态未变。 | Window，状态表 |
| workspace.active | 显示器上的当前活动工作区发生变化时触发 | Workspace |
| workspace.created | 工作区创建时触发。如果该工作区需要激活，则在激活后触发 | Workspace |
| workspace.created_early | 在工作区创建后、激活**之前**触发 | Workspace |
| workspace.move_to_monitor | 工作区移至其他显示器时触发 | Workspace; Monitor |
| workspace.removed | 工作区被移除时触发 | Workspace |
| workspace.special_active | 显示器上打开的特殊工作区发生变化时触发。Workspace 为 nil 表示没有打开任何特殊工作区 | Workspace; Monitor |
