# 插件开发指南

本页介绍编写稳定、整洁的插件时建议遵循的做法。

<a id="making-your-plugin-compatible-with-hyprpm"></a>

## 让插件兼容 hyprpm

要让用户能通过 `hyprpm` 安装你的插件，你需要提供一份清单文件。

`hyprpm` 可以正常解析 `hyprload` 清单，但建议使用功能更丰富的 hyprpm 清单。

在仓库根目录下创建一个名为 `hyprpm.toml` 的文件。

<a id="repository-metadata"></a>

### 仓库元数据

在文件开头填写插件的元数据：

```toml {filename="hyprpm.toml"}
[repository]
name = "MyPlugin"
authors = ["Me"]
commit_pins = [
    ["3bb9c7c5cf4f2ee30bf821501499f2308d616f94", "efee74a7404495dbda70205824d6e9fc923ccdae"],
    ["d74607e414dcd16911089a6d4b6aeb661c880923", "efee74a7404495dbda70205824d6e9fc923ccdae"]
]
```

`name` 和 `authors` 为必填项。
`commit_pins` 为可选项。
详情请参阅[固定提交版本](#commit-pins)。

<a id="plugins"></a>

### 插件

为每个插件添加一个如下所示的配置节：

```toml {filename="hyprpm.toml"}
[plugin-name]
description = "An epic plugin that will change the world!"
authors = ["Me"]
output = "plugin.so"
build = [
    "make all"
]
```

`description` 和 `authors` 为可选项。
`output` 和 `build` 为必填项。

`build` 列出 `hyprpm` 在仓库根目录下构建插件时要执行的命令。
执行每条命令前，当前工作目录都会重置为仓库根目录。

`output` 指定构建生成的 `.so` 文件相对于仓库根目录的路径。

<a id="commit-pins"></a>

### 固定提交版本

你可以通过固定提交来管理插件版本。
每条记录都是一对 `hash,hash`，第一个是 Hyprland 的提交哈希，第二个是与之对应的插件提交哈希。

例如，在上面的清单中，`d74607e414dcd16911089a6d4b6aeb661c880923` 对应 Hyprland 的 `0.33.1` 版本。
这意味着，如果用户运行的是 `0.33.1`，`hyprpm` 就会将插件重置到 `efee74a7404495dbda70205824d6e9fc923ccdae` 这一提交。

建议为 Hyprland 的每个发行版都固定一个对应的插件提交。
如果没有匹配的记录，就会使用插件 Git 仓库中的最新提交。

<a id="formatting"></a>

## 代码格式

Hyprland 插件并非 _必须_ 遵循 Hyprland 的代码格式、命名约定等规范，但建议让插件代码与 Hyprland 保持一致。
请参阅 Hyprland 仓库中的 [`.clang-format`](https://github.com/hyprwm/Hyprland/blob/main/.clang-format)。

<a id="usage-of-the-api"></a>

## 使用 API

建议尽可能使用 API 提供的接口，因为只要版本匹配，这些接口的稳定性就有保证。

当然，只要引入相应的头文件，也可以调用内部方法，但这不应成为常规做法。

Hyprland 的内部方法可能随时修改、移除或新增，恕不另行通知。不过，对于那些“看起来”很基础的方法（例如 `focusWindow` 和 `mouseMoveUnified`），其基本工作方式不太可能改变。

<a id="function-hooks"></a>

## 函数钩子

函数钩子可以让插件拦截对指定函数的所有调用。
版本更新时，函数钩子最容易失效，因此只应将其作为最后的手段。

始终优先使用事件钩子。

<a id="threads"></a>

## 线程

Wayland 事件循环严格采用单线程模型。
除非线程执行的工作完全独立于 Hyprland 进程（例如保存文件），否则不建议在插件代码中创建线程。
