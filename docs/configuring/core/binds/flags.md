# 标志位

<a id="bind-flags"></a>

## 按键绑定标志

`hl.bind()` 支持按以下格式指定标志：

```lua
hl.bind(keys, dispatcher, { flag1 = true, flag2 = true })
```

例如：

```lua
hl.bind(keys, hl.dsp.exec_cmd("amongus"), { release = true, locked = true })
```

可用标志如下：

| 标志 | 说明 |
|------|-------------|
| `allow_input_capture` | 即使客户端捕获了输入，仍会处理此按键绑定 |
| `auto_consuming` | 如果调度器执行失败，则将键盘或鼠标事件传递给活动窗口 |
| `device` | 允许按设备设置按键绑定。参见[按设备设置按键绑定](devices/per-device.md) |
| `description` | 允许为按键绑定添加描述 |
| `dont_inhibit` | 忽略应用程序要求禁用按键绑定的请求 |
| `drag` | 如果鼠标指针的移动距离超过 `binds:drag_threshold`，则在松开按键或鼠标按钮时触发 |
| `click` | 如果鼠标指针的移动距离始终未超过 `binds:drag_threshold`，则在松开按键或鼠标按钮时触发 |
| `ignore_mods` | 忽略修饰键 |
| `locked` | 即使输入抑制器（如锁屏程序）已启用也能生效 |
| `long_press` | 长按按键时触发 |
| `mouse` | 参见专门介绍[鼠标按键绑定](devices/mouse.md)的章节 |
| `non_consuming` | 触发调度器的同时，也将键盘或鼠标事件传递给活动窗口 |
| `release` | 松开按键时触发 |
| `repeating` | 按住时重复触发 |
| `submap_universal` | 在任何子映射中都生效 |
| `transparent` | 其他按键绑定无法覆盖此绑定 |


<details><summary>示例</summary>


```lua
-- 如果 wofi 已打开，就将其关闭；否则将其打开
hl.bind("Super_L", hl.dsp.exec_cmd("pkill wofi || wofi"), {release = true})
```

以下按键绑定可使常见键盘上的音量控制键按预期工作，锁屏时也同样有效：

```lua
hl.bind("XF86AudioRaiseVolume", hl.dsp.exec_cmd("wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%+"), { repeating = true })
-- 音量键绑定示例，即使输入抑制器处于活动状态也能触发
hl.bind("XF86AudioLowerVolume", hl.dsp.exec_cmd("wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%-"), { repeating = true, locked = true })
hl.bind("XF86AudioMute",        hl.dsp.exec_cmd("wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle"), { locked = true })

-- 需要 playerctl
hl.bind("XF86AudioPlay", hl.dsp.exec_cmd("playerctl play-pause"), { locked = true })
hl.bind("XF86AudioPrev", hl.dsp.exec_cmd("playerctl previous"),   { locked = true })
hl.bind("XF86AudioNext", hl.dsp.exec_cmd("playerctl next"),       { locked = true })

-- 长按跳到下一曲，短按仅快进 5 秒
hl.bind("SUPER + XF86AudioNext", hl.dsp.exec_cmd("playerctl next"), { long_press = true })
hl.bind("SUPER + XF86AudioNext", hl.dsp.exec_cmd("playerctl position +5"))
```



</details>

<a id="description"></a>

### 描述

可以使用 `description` 标志为按键绑定添加描述。描述始终写在标志部分。

```lua
hl.bind(keys, dispatcher, { description = "Your description here"})
```

例如：

```lua
hl.bind("SUPER + Q", hl.dsp.exec_cmd("kitty"), { description = "Open my favourite terminal" })
```

要查看按键绑定的描述，可以读取返回的按键绑定对象的 `description` 字段，也可以使用 `hyprctl binds`。更多信息请参见[使用 hyprctl](../advanced-configuration/using-hyprctl.md)。
