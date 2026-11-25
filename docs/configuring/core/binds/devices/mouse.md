# 鼠标

> [!NOTE]
> 鼠标按键绑定虽然名称中有“鼠标”，但用法与普通按键绑定相同。你可以任意选择按键和修饰键。按住选定的按键组合即可激活鼠标功能，此时再按相应的鼠标按钮即可。

<a id="mouse-buttons"></a>

## 鼠标按钮

在键码前加上 `mouse:` 即可绑定鼠标按钮。常见鼠标按钮的键码如下（其他按钮的键码可用 `wev` 查看）：

- 鼠标左键：272
- 鼠标右键：273
- 鼠标中键：274

```lua
-- 将 SUPER + LMB 绑定为启动 kitty 终端。
hl.bind("SUPER + mouse:272", hl.dsp.exec_cmd("kitty"))
```

<a id="movement"></a>

## 鼠标移动

某些调度器依赖鼠标移动，需要将 `mouse` 标志设为 `true`。



| 名称 | 说明 |
| ---- | ----------- |
| `window.drag()` | 移动活动窗口 |
| `window.resize()` | 调整活动窗口的大小 |
| `window.resize({ keep_aspect_ratio })` | 调整活动窗口的大小，暂时覆盖窗口的 keep_aspect_ratio 属性 |

可以使用 `binds.drag_threshold` 配置选项区分同一按钮的点击和拖动操作：

```lua
hl.config({
    binds {
        -- 仅当拖动距离超过 10px 时才触发拖动事件
        drag_threshold = 10
    }
})

-- ALT + LMB：拖动超过 10px 即可移动窗口。
hl.bind("ALT + mouse:272", hl.dsp.window.drag(), { mouse = true })
-- ALT + LMB（单击）：单击即可将窗口设为浮动
hl.bind("ALT + mouse:272", hl.dsp.window.float(), { click = true })
-- ALT + LMB：拖动即可调整窗口大小
hl.bind("ALT + mouse:273", hl.dsp.window.resize(), { mouse = true })
```

还可以使用 `mouse_up` 和 `mouse_down` 绑定鼠标滚轮事件（如果鼠标支持水平滚动，也可以使用 `mouse_left` 和 `mouse_right`）：

```lua
hl.bind("SUPER + mouse_down", hl.dsp.focus({ workspace = "e-1" }))
```

> [!NOTE]
> 连续的滚动事件之间有一个最短间隔。可以通过 `binds.scroll_event_delay` 配置值调整此间隔。
