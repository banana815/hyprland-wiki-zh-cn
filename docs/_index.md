# Hyprland 中文文档

> [!IMPORTANT]
> ***本维基按版本提供文档！***
> 默认情况下，你看到的是 _Hyprland 最新 Git 提交_ 对应的文档。
> 如果你使用的是带版本标签的发行版（很可能是，可以用 `hyprctl version` 查看），请打开[版本选择页](version-selector.md)，选择你使用的版本。

你好，亲爱的旅行者！
欢迎来到 Hyprland 维基！

初次使用 Hyprland，可以从[安装指南](getting-started/installation.md)和[入门教程](getting-started/master-tutorial.md)开始。已有可用的桌面时，可以查阅[配置指南](configuring/_index.md)或[实用工具](useful-utilities/_index.md)。

<a id="having-issues"></a>

## 遇到问题？

遇到问题时，请先阅读[常见问题](faq/_index.md)和[配置](configuring/_index.md)章节，你很可能会在那里找到相关说明。
如果找不到，可以搜索 [GitHub 讨论区](https://github.com/hyprwm/Hyprland/discussions)，或向 [Hyprland 社区](community/_index.md#spaces)求助。

<a id="wayland-info"></a>

## 关于 Wayland

Wayland 合成器本身就是一个完全独立的显示服务器，与 Xorg 一样。
你**无法**像在 Xorg 上自由搭配窗口管理器和合成器那样，自由组合 Wayland 合成器。
在 Wayland 上运行所有 Xorg 应用程序也不完全可行，我们也不建议这样做。
推荐的 Wayland 原生或兼容程序见[此页](useful-utilities/_index.md)。
