# 按键绑定

> [!WARNING]
> **按键绑定处理函数不得阻塞。** Lua 回调在合成器的事件循环中运行。请避免在按键绑定函数中使用 `io.popen`、执行网络 I/O、调用剪贴板工具（`wl-paste`、`xclip`）、休眠或执行其他耗时操作。运行外部命令时，优先使用 `hl.dsp.exec_cmd(...)`，让命令在按键绑定回调之外执行。如果必须从 Lua 中查询系统状态，请限制等待时间（例如使用 `timeout`）。调用一旦卡住或执行缓慢，输入和整个桌面都会冻结，直到调用返回。

> [!TIP]
> 如果不确定某个键的名称、键符号（keysym）或键码（keycode），可以使用 [`wev`](https://github.com/jwrdegoede/wev) 查看。

<a id="basics"></a>

## 基础知识

基本语法如下：

```lua
hl.bind("keys", dispatcher or function(), { bind_flags })
```

调度器列表见[调度器](../dispatchers.md)。也可以为按键绑定传入 Lua 函数，触发绑定时就会调用该函数。

按键绑定标志的说明见[标志](flags.md)。


<details><summary>示例</summary>


```lua
-- 将 SUPER + SHIFT + Q 绑定为打开 Firefox
hl.bind("SUPER + SHIFT + Q", hl.dsp.exec_cmd("firefox"))

-- 将按键绑定到包含处理逻辑的匿名函数
hl.bind("SUPER + SHIFT + X", function()
    -- 更多处理逻辑……
    hl.dispatch(hl.dsp.window.float())
end)
```



</details>

<a id="uncommon-syms--binding-with-a-keycode"></a>

## 不常见的键符号与使用键码进行绑定

所有键符号均列在 [xkbcommon-keysyms.h 头文件](https://github.com/xkbcommon/libxkbcommon/blob/master/include/xkbcommon/xkbcommon-keysyms.h)中。绑定时应使用 `XKB_KEY_` 之后的部分作为名称。

要使用键码进行绑定，请在键码前加上 `code:` 前缀。例如：

```lua
hl.bind("SUPER + code:28", hl.dsp.exec_cmd("amongus"))
```

上例会绑定 `SUPER + T`，因为 `T` 的键码是 28。

<a id="binding-modkeys-only"></a>

## 仅绑定修饰键



要单独绑定一个修饰键，请使用对应的键符号名称。该名称通常由 `MOD` 键名加上 `_L` 或 `_R` 后缀构成。使用键符号时，这些键不再被当作修饰键处理，因此按键的先后顺序会影响绑定的触发。


<details><summary>示例</summary>


```lua
-- 将 `amongus` 绑定到左侧 alt 键
hl.bind("Alt_L", hl.dsp.exec_cmd("amongus"))

-- 将左侧 super 与左侧 ctrl 的组合键绑定为打开 kitty
hl.bind("Super_L + Alt_L", hl.dsp.exec_cmd("kitty"))

-- 绑定左侧 ctrl 与右侧 ctrl 的组合键
hl.bind("Ctrl_L + Ctrl_R", hl.dsp.exec_cmd("kitty"))

-- 绑定 super 键的释放事件，仅当该键未参与组合键时触发
hl.bind("Super_L", hl.dsp.exec_cmd("hyprlauncher -t"), { release = true })
```



</details>

<a id="multiple-binds-to-one-key"></a>

## 为同一个键设置多个绑定

> [!WARNING]
> 这些按键绑定会按编写顺序自上而下执行。

可以使用 Lua 匿名函数，让同一个按键绑定触发多个操作。该函数可以依次发起多次调度调用：

```lua
-- 要在浮动工作区中切换窗口：
hl.bind("SUPER + Tab", function()
    -- 将焦点移到另一个窗口
    hl.dispatch(hl.dsp.window.cycle_next())
    -- 将该窗口移至最上层
    hl.dispatch(hl.dsp.window.alter_zorder({ mode = "top" }))
end)
```

<a id="unbind"></a>

## 解除绑定

要解除按键绑定，可以使用 `hl.unbind("key")`，也可以将绑定保存到变量中，再调用其 `:unbind()` 或 `:remove()` 方法。`hl.unbind` 中的键名区分大小写，必须与要解除的 `hl.bind` 绑定中的键名大小写完全一致。解除绑定会移除此前为该键注册的所有绑定。


<details><summary>示例</summary>


```lua
hl.bind("SUPER + TAB", hl.focus.workspace("e+1"))
hl.unbind("SUPER + Tab") -- 这不会解除绑定
hl.unbind("SUPER + TAB") -- 这会解除绑定

-- 将绑定赋给 "lft"
local moveLeft = hl.bind("SUPER + L", hl.dsp.window.move({ direction = "left" }) )

-- 解除 "SUPER + L" 的绑定
moveLeft:unbind()
-- 或者
moveLeft:remove()
```



</details>

<a id="xkb-options"></a>

## XKB 选项



要更改某些按键的行为，请使用 `kb_options`。

要查看所有可用选项，请运行：

```sh
cat /usr/share/X11/xkb/rules/base.lst
```


<details><summary>示例</summary>


要将 Caps Lock 重新映射为 Ctrl：

```lua
hl.config({
    input = {
        kb_options = "ctrl:nocaps"
    }
})
```

要交换 Caps Lock 和 Escape 的功能：

```lua
hl.config({
    input =  {
        kb_options = "caps:swapescape"
    }
})
```



</details>

<a id="binding-quirks"></a>

## 按键绑定的注意事项



<a id="conditional-bind-resolution-at-bind-time"></a>

### 在创建绑定时求值的条件

创建包含条件判断的按键绑定时，几乎总是应该将判断逻辑放在函数中。例如，下面的绑定：

```lua
hl.bind("SUPER + L", hl.dsp.exec_cmd("foot", { float = not (hl.get_active_window().title == "foot") }) )
```

会被解析为：

```lua
hl.bind("SUPER + L", hl.dsp.exec_cmd("foot", { float = false }) )
-- 或者，取决于重新加载配置时焦点所在的位置
hl.bind("SUPER + L", hl.dsp.exec_cmd("foot", { float = true }) )
```

绑定会一直保持这个结果，直到下次重新加载配置。要让它按预期工作，必须将判断逻辑放在函数中：

```lua
hl.bind("SUPER + L", function()
    local is_foot = hl.get_active_window().title == "foot"
    hl.dispatch( hl.dsp.exec_cmd("foot", { float = not is_foot }) )
end)
```

这样，每次触发绑定时都会重新判断条件，而不会只在加载配置时判断一次。

<a id="auto-consuming-binds-and-return--ok--false-"></a>

### 自动消耗按键事件的绑定与 `return { ok = false }`

调度器执行完毕后，可以返回 `ok` 值来表示执行是否成功。设置 `auto_consuming` 标志后，`hl.bind` 会检查该值，以决定是消耗这次按键事件，还是将其继续传递下去。


<details><summary>示例</summary>


```lua
hl.bind("p", function()
    local window = hl.get_active_window()
    if window and window.title == "some cool app" then
        hl.dispatch(hl.dsp.exec_cmd("another_cool_app"))
    else
        return { ok = false }
    end
end, { auto_consuming = true })
```

如果当前活动窗口的标题为 `"some cool app"`，此绑定会启动 `another_cool_app`；否则会将 `p` 键事件传递给当前活动窗口。



</details>

<a id="binding-to-keys-handled-by-systemd-logind"></a>

### 为 systemd-logind 处理的按键设置按键绑定

通常，systemd-logind 会处理按下电源键、开合笔记本盖等硬件事件。可以通过编辑其配置文件在全局禁用这类处理，但更合适的做法是仅在 Hyprland 运行期间阻止它处理相应事件。

可以使用 `systemd-inhibit` 来实现。例如，可以通过 `systemd-inhibit --what=handle-power-key Hyprland` 启动 Hyprland，然后为相应的按键事件（本例中为 `XF86PowerOff`）创建按键绑定。
