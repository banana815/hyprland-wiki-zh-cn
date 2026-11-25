# 命名约定

<a id="syntax"></a>

## 语法

> [!TIP]
> 为便于理解，本 wiki 对部分元素采用了特殊记法。

<a id="parameters"></a>

### 参数

Hyprland 的许多 Lua 函数接受 Lua 表作为输入。将键值对放在花括号中即可创建表，例如 `{ key1 = value1, key2 = value2 }`。表中键值对的顺序无关紧要，访问不存在的键时会得到 `nil`。

参数名后带问号（`?`）表示该参数可选，可以省略。此处的问号不属于 Lua 语法，不能写入实际配置。

参数后带 `= data_type` 表示该参数仅接受指定的数据类型。可选参数后可以带 `= value`，表示未设置该参数时使用的默认值。

有关 Lua 表的更多信息，请参阅[此处](https://www.lua.org/pil/2.5.html)。


<details><summary>参数示例</summary>


下面以这段代码中的调度器为例，说明不同参数类型之间的区别：

```lua
hl.bind("SUPER + SHIFT + S", hl.dsp.window.move({ workspace = "special:magic" }))
hl.bind("SUPER + S", hl.dsp.workspace.toggle_special("magic"))
```

在第一个按键绑定中，`hl.dsp.window.move` 接受一个表作为参数。调度器参数记法 `move({ window?, workspace, follow? })` 用花括号（`{}`）表示表，其中列出了 `window?, workspace, follow?`。这里，`workspace` 为必填项，`window` 和 `follow` 为可选项，默认值分别为 `"activewindow"` 和 `true`。

在第二个按键绑定中，调度器接受一个普通的位置参数，而非表。调度器参数记法 `toggle_special( special_name )` 中没有花括号（`{}`），即表示这种用法。



</details>

<a id="value-ranges"></a>

### 取值范围

`[value1 - value2]` 表示在相应数据类型中从 `value1` 到 `value2` 的取值范围。若未指定上限或下限，则在相应位置使用 `...`。


<details><summary>示例</summary>


`[0.25 - 5.0]` 表示允许取 0.25 到 5.0 之间的所有浮点数。
`[0 - ...]` 表示允许取从 0 到当前机器的 int 类型上限之间的所有整数。



</details>

<a id="coordinates"></a>

### 坐标

坐标采用 Y 轴朝下的笛卡尔坐标系，向右为 X 轴正方向（+x），向下为 Y 轴正方向（+y）。

<a id="data-types"></a>

## 数据类型

| 类型 | 说明 |
| --- | --- |
| int | 整数 |
| float | 浮点数 |
| bool | 布尔值，取 `true` 或 `false` |
| string | Lua 字符串。用 `""`、`''` 或 `[[]]` 将字符括起来（例如 `"dwindle"`、`'master'`、`[[scrolling]]`）。使用 Lua 的长括号字符串字面量（`[[]]`）时，无需转义 `"` 和 `'`。 |
| table | Lua 表，写作 `{ }` |
| vec2 | 由两个浮点数构成的向量，写作 `{x, y}`（例如 `{20, 20}`） |
| css_gaps | 一个浮点数，或 `{ top?, left?, right?, bottom? }` |
| color | 颜色。有关颜色的说明，请参阅下方提示。 |
| gradient | 渐变。可传入单个颜色，也可使用 `{ colors = { color, color }, angle? = float }` 结构。部分选项可能提供额外的渐变参数。 |
| font_weight | 100 到 1000 之间的整数，或以下预设值之一：`thin`（100）、`ultralight`（200）、`light`（300）、`semilight`（350）、`book`（380）、`normal`（400）、`medium`（500）、`semibold`（600）、`bold`（700）、`ultrabold`（800）、`heavy`（900）、`ultraheavy`（1000） |

某些类型之间可以隐式转换，但这可能导致后续出现未定义行为。配合 Lua 存根使用 LSP，可在类型使用错误时收到警告。详情请参阅[此处](core/_index.md#editor-autocompletion)。

<a id="colors"></a>

### 颜色


颜色有以下四种写法：
- Web 风格的 RGB 或 RGBA 十六进制写法，以 # 开头：<code style="background-color:#FAFC21;color:#000000">"#FAFC32"</code>、<code style="background-color:#DDD;color:#000000">"#DDD"</code> 或 <code style="background-color:#FA3D7BFF;color:#000000">"#FA3D7BFF"</code>
- rgba()：<code style="background-color:#57BBFFEE;color:#000000">\"rgba(57BBFFEE)"</code>，或等价的十进制写法 <code style="background-color:#57BBFFEE;color:#000000">\"rgba(87,187,255,0.933)"</code>
- rgb()：<code style="background-color:#FF4410;color:#000000">\"rgb(FF4410)"</code>，或等价的十进制写法 <code style="background-color:#FF4410;color:#000000">\"rgb(255,68,16)"</code>
- 旧版 ARGB 格式：<code style="background-color:#B3FF1A;color:#000000">\"0xeeb3ff1a"</code>

请注意，`rgb()`/`rgba()` 中的十进制参数之间不能有空格。
