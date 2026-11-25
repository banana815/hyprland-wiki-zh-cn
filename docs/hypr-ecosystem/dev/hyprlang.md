# hyprlang

[hyprlang](https://github.com/hyprwm/hyprlang) 是用于解析 hypr 配置语言的库。

<a id="syntax"></a>

## 语法

<a id="line-style"></a>

### 行格式

每行配置由一条命令及其后的值组成。

```ini
COMMAND = VALUE
```

命令可以是变量，也可以是特殊关键字（由你使用的应用程序定义）。

变量类似于“选项”，关键字则类似于“命令”。
每个选项只能有一个有效值（重复设置会覆盖之前的值），而命令每出现一次，都会触发相应的行为。

单词前后的空格可以省略，写出来只是为了方便阅读。

<a id="categories"></a>

### 类别

类别分为普通类别和“特殊”类别。

两者的写法相同：

```ini
category {
    variable = value
}
```

特殊类别还可以有其他属性，例如包含一个键：

```ini
special {
    key = A
    variable = value
}
special {
    key = B
    variable = value
}
```

这相当于定义了两个“组”，一个的键是 A，另一个的键是 B。
例如，Hyprland 就用这种方式为各个设备单独配置。

<a id="defining-variables"></a>

### 定义变量

可以这样定义变量：

```ini
$VAR = myData
```

之后可以这样使用这些变量：

```ini
$SUFFIX = -san
$NAME = Jeremy
greeting = Hello, $NAME$SUFFIX.
```

> [!NOTE]
> 值前后以及各个值之间的空格都可以省略。

<a id="comments"></a>

### 注释

注释以 `#` 字符开头。

如果要写入字面字符 `#`，可以用 `##` 对其转义，以免开始一段注释。
`##` 会被转换为单个 `#`，这个字符_会_保留在当前行中。

<a id="escaping-errors"></a>

### 忽略错误

如果使用插件，你可能希望忽略因缺少选项或关键字而产生的错误，以免在插件加载前看到错误提示栏。
可以这样写：

```ini
# hyprlang noerror true

bind = MOD, KEY, something, amogus
someoption = blah

# hyprlang noerror false
```

<a id="inline-options"></a>

### 行内选项

要在一行内指定选项，省去类别块的起止标记，可以使用 `:` 分隔符：

```ini
category:variable = value
```

如果是需要键的特殊类别，可以这样写：

```ini
category[keyvalue]:variable = value
```

例如，`hyprctl keyword` 就使用这种语法。

<a id="arithmetic-operations"></a>

### 算术运算

从 0.6.3 版开始，hyprlang 支持使用 `{{}}` 对变量进行_非常_基础的算术运算。

可以使用 `+`、`-`、`*` 或 `/`，每次只能对_两个_变量（或常量）进行运算。
运算_不能_嵌套，但可以用中间变量保存结果。

示例：
```ini
$VAR1 = 2
$VAR2 = {{VAR1 + 3}}
$VAR3 = {{VAR2 * 2}}

someVariable = {{VAR3 / 2}}
someVariable2 = VAR3
```

写法有误时可能会报错。
请确保满足以下条件：

- 运算符两侧各有一个操作数（**不能**写成 `{{a + b + c}}`，这里有三个操作数）
- 两侧的操作数都是已定义的数值变量或数值常量
- 运算符两侧都有空格（**不能**写成 `{{a+b}}`）

<a id="arithmetic-escaping"></a>

### 转义算术表达式

从 0.6.4 版开始，hyprlang 允许在 `{{a + b}}` 这样的算术表达式前加上 `\` 进行转义。
可以在表达式开头的任意一个左花括号前加上转义符。

示例：
```ini
$VAR = \{{10 + 10}}
bind = MOD, KEY, exec, COMMAND "{\{10 + 10}}"
someVariable = \{\{10 + 10}}
```

这样会跳过表达式求值，直接按原文赋值。
值中所有用于转义的 `\` 都会被移除。
因此，`\{{hello world}}` 会变成 `{{hello world}}`，hyprlang 不会尝试将其解析为表达式。

<a id="escaping-escapes"></a>

### 转义转义符

从 0.6.4 版开始，任何原本用于转义其他字符的 `\` 本身也可以被转义。

例如，要在需要求值的表达式前保留一个 `\`，可以这样写：

```ini
someVariable = \\{{VAR1 + 10}}
```

要在任意可转义字符前保留一个 `\`，可以这样写：

```ini
someOtherVariable = \\{ hello \\}
```

<a id="conditionals"></a>

### 条件判断

从 0.6.4 版开始，可以在配置中加入条件判断。
使用 `# hyprlang if` 指令可以让配置块按条件生效。

示例：

```ini
# hyprlang if MY_VAR

test = 24

# hyprlang endif

# hyprlang if !MY_VAR

test = 12

# hyprlang endif
```

> [!NOTE] 重要说明
> - 当且仅当变量存在且其值不是空字符串时，条件才为 `true`。
> - 支持环境变量。
> - 动态设置关键字（使用 `hyprctl keyword`）**不会**让这些配置块重新生效或失效。
>   必须直接修改配置文件或环境变量。如果修改的是环境变量，或者使用的 hypr\* 应用程序不会自动重新加载配置，就需要重启应用程序（对于 Hyprland，运行 `hyprctl reload`）。

<a id="developer-documentation"></a>

## 开发者文档

请参阅 [standards.hyprland.org/hyprlang](https://standards.hyprland.org/hyprlang/) 上的文档。
