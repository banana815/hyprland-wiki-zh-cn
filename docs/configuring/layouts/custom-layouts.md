# 自定义布局

你可以直接在 Lua 配置中创建自定义布局。先用 `hl.layout.register(name, { recalculate, layout_msg? })` 定义布局，再通过 `lua:name` 使用它。

下面是一个简单的布局示例：

```lua
hl.layout.register("columns", {
    recalculate = function(ctx)
        local n = #ctx.targets
        if n == 0 then
            return
        end

        for i, target in ipairs(ctx.targets) do
            target:place(ctx:column(i, n))
        end
    end,
})
```

定义后，即可通过 `lua:columns` 使用此布局。

Hyprland 仓库中提供了一些[布局示例](https://github.com/hyprwm/Hyprland/tree/main/example/layouts)。

`ctx` 提供了一些便捷函数，例如 `grid_cell`、`column`、`row` 和 `split`。它还提供 `area` 和 `targets`，分别表示工作区域和目标列表。

你可以通过布局目标的 `.window` 字段获取窗口，但要注意，该字段不一定存在。有些布局目标（例如窗口组）可能包含多个窗口，此时该字段只提供其中的“主”窗口。

> [!NOTE]
> 请优先使用 `:place()`，仅在必要时使用 `:set_box()`。`:place()` 会自动处理间隙、伪平铺、预留空间等布局计算。只有确实需要完全手动定位时，才应使用 `:set_box()`。
