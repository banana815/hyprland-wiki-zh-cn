# 按键子映射

<a id="submaps"></a>

## 子映射

按键绑定子映射可以让你启用一组独立的按键绑定。

例如，如果你想进入一种可以用方向键调整窗口大小的“缩放模式”，可以这样设置：

```lua
-- 切换到名为 `resize` 的子映射。
hl.bind("ALT + R", hl.dsp.submap("resize"))

-- 开始定义名为 "resize" 的子映射。
hl.define_submap("resize", function()

    -- 设置可重复触发的按键绑定，用于调整活动窗口的大小。
    hl.bind("right", hl.dsp.window.resize({ x = 10, y = 0, relative = true}), { repeating = true })
    hl.bind("left", hl.dsp.window.resize({ x = -10, y = 0, relative = true}), { repeating = true })
    hl.bind("up", hl.dsp.window.resize({ x = 0, y = 10, relative = true}), { repeating = true })
    hl.bind("down", hl.dsp.window.resize({ x = 0, y = -10, relative = true}), { repeating = true })

    -- 使用 `reset` 返回全局子映射
    hl.bind("Escape", hl.dsp.submap("reset"))

end)

-- 后面定义的按键绑定将重新成为全局绑定……
```

> [!WARNING]
> 别忘了在子映射中设置一个用于重置按键映射的按键绑定（本例中为 `Escape`）！
>
> 如果你被困在某个按键映射中，可以使用 `hyprctl dispatch 'hl.dsp.submap("reset")'` 返回。如果没有打开终端，请打开一个新的 TTY，并使用 `--instance` 标志选择要操作的 Hyprland 实例（如果只有一个实例在运行，其编号为 0）。例如：`hyprctl dispatch --instance 0 'hl.dsp.submap("reset")'`。

你也可以让同一个按键绑定执行多个操作，例如调整窗口大小后关闭子映射，配置如下：

```lua
hl.bind("ALT + R", hl.dsp.submap("resize"))

hl.define_submap("resize", function()
    hl.bind("right", function()
        hl.dispatch(hl.dsp.window.resize({ x = 10, y = 0, relative = true }))
        hl.dispatch(hl.dsp.submap("reset"))
    end)
end)
```

这是因为同一个按键绑定可以关联多个操作，而这些绑定会按它们在配置中出现的顺序执行。

使用子映射的通用绑定标志，可以让某个按键绑定在任何子映射中都生效。

```lua
hl.bind(mainMod .. " + K", hl.dsp.exec_cmd("kitty"), { submap_universal = true })
```

<a id="nesting"></a>

### 嵌套

子映射可以嵌套，示例如下：

```lua
hl.bind(mainMod .. " + M", hl.dsp.submap("main"))
hl.define_submap("main", function()

    hl.bind("1", hl.dsp.submap("nested_one"))
    hl.define_submap("nested_one", function()

        hl.bind("SHIFT + Escape", hl.dsp.submap("reset"))
        hl.bind("Escape", hl.dsp.submap("main_submap"))

        hl.bind("2", hl.dsp.submap("nested_two"))
        hl.define_submap("nested_two", function()

            hl.bind("SHIFT + Escape", hl.dsp.submap("reset"))
            hl.bind("Escape", hl.dsp.submap("main_submap"))

        -- nested_two 子映射结束
        end)
    -- nested_one 子映射结束
    end)

    hl.bind("Escape", hl.dsp.submap("reset"))
-- main 子映射结束
end)
```

<a id="automatically-close-a-submap-on-dispatch"></a>

### 执行调度操作时自动关闭子映射

将子映射名称或 `"reset"` 作为第二个参数传给 `hl.define_submap()`，即可在执行调度操作时自动切换到指定子映射或关闭当前子映射。

```lua
hl.bind("SUPER + a", hl.dsp.submap("submapA"))

-- 按下 a 后切换到子映射 submapB。
hl.define_submap("submapA", "submapB", function()
    hl.bind("a", hl.dsp.exec_cmd("someCoolThing.sh"))
end)

-- 按下 a 后将子映射重置为默认值。
hl.dsp.submap("submapB", "reset", function()
    hl.bind("a", hl.dsp.exec_cmd("someOtherCoolThing.sh"))
end)
```

<a id="catch-all"></a>

### 匹配任意按键

你也可以使用特殊关键字 `catchall` 定义一个按键绑定，按下任意键都能触发它。这样可以在子映射中阻止任何按键传递给当前活动的应用，也可以在按下任何未定义的键时立即退出子映射：

```lua
hl.bind("catchall", hl.dsp.submap("reset"))
```

<a id="disabling-keybinds-with-one-master-keybind"></a>

### 使用一个总控按键绑定禁用所有按键绑定

如果你想用另一个按键绑定来禁用所有按键绑定，相当于为按键绑定设置一个总开关，只需创建一个子映射，其中仅保留用于退出该子映射的按键绑定即可。

```lua
hl.bind(KEYS, hl.dsp.submap("clean"))
hl.define_submap("clean", function()
    hl.bind(KEYS, hl.dsp.submap("reset"))
end)
```
