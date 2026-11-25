# 图层规则

<a id="syntax"></a>

## 语法

```lua
hl.layer_rule({
    name? = string,
    match = {
        prop = some_prop_value,
    },
    effect = some_effect_value,
})
```

<a id="layer-rules"></a>

## 图层规则

在 Wayland 中，应用启动器、状态栏、壁纸等属于图层，而非窗口。图层有独立的规则，通过 `hl.layer_rule()` 设置，其语法与 `hl.window_rule()` 相同。

<a id="props"></a>

### 匹配属性

| 属性 | 说明 | 类型 |
| --- | --- | --- |
| namespace | 图层的命名空间。可通过 `hyprctl layers` 查看 | [RegEx] |

<a id="effects"></a>

### 效果

> [!NOTE]
> 如果启用模糊后某些图层仍未显示模糊效果，可能是因为该效果由客户端设置控制。请参阅[常见问题](../../../faq/_index.md#blur)。

| 效果 | 说明 | 类型 | 范围 |
| ---- | --- | --- | --- |
| above_lock | 值非零时，将图层绘制在锁屏界面之上。设为 `2` 时，可在锁屏界面上与该图层交互 | int |  |
| animation | 为此图层设置特定的动画样式 | string |  |
| blur | 为图层启用模糊效果 | bool |  |
| blur_popups | 为弹出窗口启用模糊效果 | bool |  |
| dim_around | 调暗图层后方的所有内容 | bool |  |
| ignore_alpha | 应用模糊效果时，忽略不透明度小于或等于此值的像素 | float | [0.0 - 1.0] |
| no_anim | 禁用动画 | bool |  |
| no_screen_share | 在屏幕共享中隐藏图层 | bool |  |
| order | 设置此图层相对于其他图层预留空间的优先级。多个图层尝试预留空间时，数值较大的图层优先。该值可以为负数 | int |  |
| xray | 设置图层模糊效果的 xray 模式 | bool |  |


<details><summary>示例</summary>


```lua
-- 为 Waybar 启用模糊效果
hl.layer_rule({ match = { namespace = "waybar" }, blur = true })

-- 命名图层规则
local selectionRule = hl.layer_rule({
  name    = "no-anim-for-selection",
  match   = { namespace = "selection" },
  no_anim = true,
})

-- 为 Rofi 启用模糊效果和 ignore_alpha
hl.layer_rule({
  match        = { namespace = "rofi" },
  blur         = true,
  ignore_alpha = 0.5,
})
```



</details>

图层规则也会返回一个句柄，支持 `set_enabled()`/`is_enabled()`：

```lua
local myLayerRule = hl.layer_rule({
  name  = "my-layer-rule",
  match = { namespace = "waybar" },
  blur  = true,
})
myLayerRule:set_enabled(false)
```
