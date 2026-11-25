# 规则

可以通过规则为符合条件的窗口、工作区或图层强制应用特定选项。

规则可以命名，也可以匿名。

规则的参数分为两类：_匹配属性_和_效果_。匹配属性是 `match` 表中的字段，用于判断规则是否适用于某个窗口。效果是 `match` 表之外的其他字段，用于改变目标窗口的行为。

规则按从上到下的顺序求值，但会先处理所有命名规则，再处理所有匿名规则。

只有_所有_匹配属性都符合条件，规则才会生效。每条规则的匹配属性和效果数量不限，顺序任意。不过，`match` 表不能为空。

在 `hyprctl clients` 命令的输出中，`fullscreen` 指的是 `fullscreen_state_internal`，`fullscreenClient` 指的是 `fullscreen_state_client`。

有关规则的更多内容，请参阅以下页面：

- [窗口规则](window-rules.md)
- [工作区规则](workspace-rules.md)
- [图层规则](layer-rules.md)
