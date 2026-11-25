# 选择显示输出

选择输出时，可以使用端口名或描述，两者只能选其一。

`hyprctl monitors` 的输出如下所示：

```
Monitor `portname` (ID `ID`)
        `mode` at `position`
        description: `description`
        [...]
```

`portname` 和 `description` 均可用来选择输出：

```lua
hl.monitor({
    output = "portname",
    mode = "preferred", position = "auto"
})

hl.monitor({
    output = "desc:description",
    mode = "preferred", position = "auto"
})
```


<details><summary>示例</summary>


```
Monitor eDP-1 (ID 0):
        1920x1080@60.00100 at 0x0
        description: Chimei Innolux Corporation 0x150C
        [...]
```

在此示例中，端口名为 `eDP-1`，描述为 `Chimei Innolux Corporation 0x150C`，因此可以分别按以下方式使用：

```lua
hl.monitor({
    output = "eDP-1",
    mode = "preferred", position = "auto"
})

hl.monitor({
    output = "desc:Chimei Innolux Corporation 0x150C",
    mode = "preferred", position = "auto"
})
```



</details>
