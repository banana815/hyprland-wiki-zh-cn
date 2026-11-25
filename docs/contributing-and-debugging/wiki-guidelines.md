# Wiki 写作指南

<a id="wiki-engine-notes"></a>

## Wiki 引擎说明

Markdown 会自动合并相邻的两行，Hugo 也遵循这一规则，除非前一行以换行符或两个空格结尾。

可以通过 <code>\{\{< shortcode >\}\}</code> 或 <code>\{\{% shortcode %\}\}</code> 调用模板。
每个短代码文件的注释中都说明了正确用法。

Hextra 主题的短代码见[这里](https://github.com/imfing/hextra/tree/main/layouts/_shortcodes)。
本 Wiki 的短代码见[这里](https://github.com/hyprwm/hyprland-wiki/tree/main/layouts/_shortcodes)。

版本选择器由一个短代码生成，它从 Hugo 的 `config.toml` 中读取版本列表。

<a id="general-styling-notes"></a>

## 通用格式规范

凡是格式允许的地方，都必须遵守本节的所有规范（例如，Markdown 不允许将表格单元格中的多个句子分行书写）。

页面内容应遵循 [xkcd 1285](https://xkcd.com/1285) 的排版方式，即每写完一句就换行。
渲染页面时会忽略这些换行，但它们能缩小差异对比的范围，也让文档作者更容易阅读源文件。

想了解漫画之外的详细说明，请参阅[这篇文章](https://writingslowly.com/2025/01/13/semantic-line-breaks-are-a.html)和[语义换行规范](https://sembr.org)。

此外：

- 代码块应使用 4 个空格缩进，不要使用制表符或其他缩进方式。
- 警告必须放在所在小节的开头。
- 所有缩写都必须使用大写字母。
- 拼写必须遵循标准美式英语规范。
- 句末标点必须放在引号外。

添加新的调度器时，应按以下问题的顺序排列参数：

- 操作的对象是什么？
- 要执行什么操作？
- 如何执行该操作？

HTML 注释（``）不会显示在渲染后的页面上，但有助于维护文档。
适当时，请在注释首行使用标准标签（`WARNING: `、`NOTE: `、`TODO: `、`SORT: `）。
标签与注释正文之间留一个空格（`TODO: body here`）。

<a id="sorting-config-options"></a>

## 配置项排序

表格中的配置项按以下规则排序：




<a id="global-toggle"></a>

### 是否有全局开关？

如果有 `enabled` 选项，必须始终将其列在首位。

<a id="display-or-display-like"></a>

### 是否有显示或类似选项？

如果表中包含 `output`、`position`、`scale`、`transform` 或 `rotation`，必须按此处列出的顺序将它们排在接下来几位。

<a id="other"></a>

### 其他选项

其余选项必须按字母顺序排列，除非这样会让含义变得不清楚（见下文）。

<a id="special-order"></a>

### 特殊顺序

有些选项的功能相互关联，排在一起更有助于理解。
如果对排序做了额外调整，请在表格前添加一条以 `SORT: ` 开头的注释，说明排序方式。
说明的格式不限，只要其他人能看懂即可。
还要在 PR 中说明这项排序调整。




<a id="option-descriptions"></a>

## 选项说明

说明必须以大写字母开头，结尾_不加_句号。

说明应简明扼要。
如果需要进一步解释，请在下方新建小节，并在表格中添加指向该小节的链接。

如果某个选项只支持一组预定义值，请在说明中列出这些值。
如果预定义值超过四个，请新建小节，并在表格中添加指向该小节的链接。

如果配置管理器对某个选项强制设有限制，请根据该选项的类型，在 `Limits` 字段中写明这些限制。
