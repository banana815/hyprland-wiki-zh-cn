# Hyprland 中文文档

Hyprland Wiki 当前 Git 版本的非官方简体中文译本，共 121 页。正文、配置参考和示例说明均可在仓库中阅读。配置键、命令、快捷键名及程序输出保留原样，便于对照使用。

**[在线阅读](https://banana815.github.io/hyprland-wiki-zh-cn/)** · [在仓库阅读](docs/_index.md) · [上游 Wiki](https://wiki.hypr.land/)

| 章节 | 内容 |
| --- | --- |
| [入门指南](docs/getting-started/_index.md) | 安装 Hyprland、首次启动和预配置桌面 |
| [配置指南](docs/configuring/_index.md) | 显示器、输入设备、快捷键、窗口规则、布局、动画和 Lua 配置 |
| [Hypr 生态](docs/hypr-ecosystem/_index.md) | 锁屏、壁纸、空闲管理、桌面门户及开发工具库 |
| [插件](docs/hyprland-plugins/_index.md) | 安装和管理插件，编写自己的 Hyprland 插件 |
| [实用工具](docs/useful-utilities/_index.md) | 状态栏、启动器、剪贴板、截图录屏和屏幕共享 |
| [Nix](docs/nix/_index.md) | NixOS、Home Manager、Hjem 和软件包配置 |
| [NVIDIA](docs/nvidia/_index.md) | 显卡驱动、硬件加速和常见问题 |
| [进程间通信](docs/ipc/_index.md) | 通过套接字读取事件和控制 Hyprland |
| [崩溃与缺陷](docs/crashes-and-bugs/_index.md) · [常见问题](docs/faq/_index.md) | 收集日志、诊断故障和查找解决办法 |
| [社区](docs/community/_index.md) · [贡献与调试](docs/contributing-and-debugging/_index.md) | 交流渠道、提交问题、测试和参与开发 |

## 文档版本

译文对应 2026 年 11 月 25 日获取的[上游快照 `bd104c0`](https://github.com/hyprwm/hyprland-wiki/tree/bd104c02d476c726d665e4ee14e861b97c21b67d/content)。运行 `hyprctl version` 可查看本机版本。[版本选择页](docs/version-selector.md)列出官方保存的英文历史文档。

## 本地阅读与构建

直接在 GitHub 或 Markdown 阅读器中打开 [docs/_index.md](docs/_index.md) 即可阅读。要使用网页的全文搜索和导航，请在安装 Python 3 和 Pandoc 后（本次使用 Pandoc 3.14），从仓库根目录运行以下命令。

```sh
python3 scripts/build.py
python3 -m http.server 8000 --directory public
```

在浏览器中打开 [localhost:8000](http://localhost:8000/)。网页输出位于 `public/`，GitHub Pages 使用 `gh-pages` 分支发布。

原文及徽标来自 Hyprland Wiki，原项目版权归 vaxerski 等上游贡献者所有。项目保留[上游 BSD-3-Clause 许可证](LICENSE)。
