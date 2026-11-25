# 触摸板

<a id="touchpad"></a>

## 触摸板

在触摸板上按下鼠标按钮的同时移动指针不太顺手，因此也可以用键盘按键代替鼠标点击。

```lua
hl.bind("SUPER + mouse:272", hl.dsp.window.drag(), { mouse = true })
hl.bind("SUPER + CTRL_L", hl.dsp.window.drag(), { mouse = true })

hl.bind("SUPER + mouse:273", hl.dsp.window.resize(), { mouse = true })
hl.bind("SUPER + ALT_L", hl.dsp.window.resize(), { mouse = true })
```
