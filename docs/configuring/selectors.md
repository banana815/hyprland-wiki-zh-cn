# 选择器

可以使用以下两种选择器中的任意一种来选择 ID：
- 通过 `+` 或 `-` 进行相对选择
- 通过 ID 本身进行绝对选择

<a id="regex-selector"></a>

## 正则表达式选择器

Hyprland 使用 [Google 的 RE2](https://github.com/google/re2) 解析正则表达式。这意味着任何需要多项式时间才能完成的运算都无法使用。有关支持的扩展语法，请参阅 [RE2 的 wiki](https://github.com/google/re2/wiki/Syntax)。

要进一步了解支持的正则表达式语法结构，请[参阅这份速查表](https://github.com/ziishaned/learn-regex/blob/master/README.md)。

如果要对正则表达式_取反_，即仅在正则表达式_匹配失败_时才通过，可以在表达式前加上 `negative:`（例如 `"negative:kitty"`）。

> [!TIP]
> Lua 的长括号字符串字面量语法 `[[]]` 有助于避免反复转义反斜杠。例如，可以将 `"\\b\\w*apple\\b"` 写成 `[[\b\w*apple\b]]`。

<a id="window-selector"></a>

## 窗口选择器

可以通过以下方式选择窗口：
- 窗口对象
- 精确匹配选择器：
  - `pid:...`
  - `stableid:...`
  - `address:0x...`
- 正则表达式：
  - `class:...`
  - `initialclass:...`
  - `title:...`
  - `initialtitle:...`
  - `tag:...`
- `activewindow`
- `floating`
- `tiled`

如果未指定窗口，则使用活动窗口。

<a id="workspaces"></a>

## 工作区

可以通过以下方式引用工作区：

- 名称：例如 `1`、`42`、`Web`、`Anime`、`Better anime`
- 上一个工作区：`previous` 或 `previous_per_monitor`
- 特殊工作区：使用 `special`，对于命名的特殊工作区则使用 `special:name`。
- 工作区对象
- [工作区过滤器](#workspace-filters)
- [工作区查询](#workspace-query)

> [!NOTE]
> 在仅接受特殊工作区的场合（例如 `hl.dsp.toggle_special()` 的参数），不要包含 `special:` 工作区前缀。只有在普通工作区也有效的场合才需要此前缀。例如，`hl.dsp.toggle_special("foo")` 指向通常写作 `special:foo` 的工作区。

<a id="workspace-filters"></a>

### 工作区过滤器



可以使用工作区过滤器（例如 `r[2-4] w[t1]`）选取已创建的工作区。

过滤器由一系列以空格分隔的过滤表达式组成。表达式内部不允许出现空格。

- `r[A-B]` - ID 范围从 A 到 B，包含两端。
- `s[bool]` - 工作区是否为特殊工作区。
- `n[bool]`、`n[s:string]`、`n[e:string]` - 按名称筛选。`n[bool]` 判断工作区是否为命名工作区。`s` 和 `e` 分别表示名称以指定字符串开头或结尾。
- `m[monitor]` - 显示器选择器
- `w[(flags)A-B]`、`w[(flags)X]` - 按工作区中的窗口数量筛选。`A-B` 表示包含两端的范围，`X` 表示确切数量。标志可以省略。可用标志如下：
  - `t` 仅统计平铺窗口
  - `f` 仅统计浮动窗口
  - `g` 按组数而非窗口数统计
  - `v` 仅统计可见窗口
  - `p` 仅统计固定窗口
- `f[-1]`、`f[0]`、`f[1]`、`f[2]` - 工作区的全屏状态。`-1`：无全屏窗口，`0`：全屏，`1`：最大化，`2`：全屏，但不向窗口发送全屏状态。仅匹配有全屏窗口覆盖的工作区。

> [!NOTE]
> 过滤器*只能*选取已存在的工作区。尝试将规则（例如 `persistent`）应用到尚不存在的工作区会失败。

<a id="workspace-query"></a>

### 工作区查询

在查询选择器后附加带符号的偏移量 `+n` 或 `-n`，即可相对于当前活动工作区查找匹配的工作区。要改用从 1 开始编号的绝对 ID，可在选择器与 ID 之间插入 `~`（例如，`m~3` 表示当前显示器上的第三个工作区）。

| 选择器 | 说明 | 范围 |
| --- | --- | --- |
| e | 在所有显示器上查找 | 如果查找范围超出该方向上的工作区数量，则从另一端继续查找 |
| m | 在当前显示器上查找 | 如果查找范围超出该方向上的工作区数量，则从另一端继续查找 |
| r | 在当前显示器上查找，包括空工作区和尚不存在的工作区 | [1 - ...] |
| empty | 查找第一个空工作区。可添加后缀 `m` 将查找范围限定在当前显示器，也可添加后缀 `n` 查找 _下一个_ 可用的空工作区，还可同时使用两者（例如 `emptynm`） | 如果计算出的编号超过最后一个数字工作区的编号 2147483647，则回绕到开头 |

> [!WARNING]
> 对于接受 ID 的查询选择器，必须使用正负号或 `~`。`m3` 会被解释为工作区名称，而非查询选择器。只有存在名为“m3”的工作区时，它才会生效。

<a id="direction"></a>

## 方向

指定一个方向。
- `l`/`left` - 向左
- `r`/`right` - 向右
- `u`/`up` - 向上
- `d`/`down` - 向下

<a id="monitor"></a>

## Monitor

可以通过以下方式选择显示器：
- 显示器对象
- 显示器 ID
- [输出选择器](core/monitors/output-selection.md)
- [方向](#direction)
- `current`
