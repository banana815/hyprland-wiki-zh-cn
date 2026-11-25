# 贡献与调试

> [!IMPORTANT]
> 所有交流请使用英语！
> 这样开发者和其他社区成员都能看懂并参与交流。
> 使用其他语言发布的内容可能会被关闭或忽略！
>
> 感谢理解。

有关拉取请求（PR）、代码风格和代码方面的常见问题，请见[此处](pr-guidelines.md)。

有关议题（issue），请参阅[议题指南](https://github.com/hyprwm/Hyprland/blob/main/docs/ISSUE_GUIDELINES.md)。

<a id="getting-vouched"></a>

## 获得担保

提交 PR 前，你需要先获得担保，否则你的 PR 会被自动关闭。

如需担保，请在[这里](https://github.com/hyprwm/.github/discussions)提交申请。

<a id="exemptions"></a>

### 豁免情形

以 i18n（本地化）为目的的 PR 无需担保。
提交这类 PR 时，请阅读 PR 正文顶部的注释，了解具体提交方式。

<a id="build-in-debug-mode"></a>

## 以调试模式构建

<a id="required-packages"></a>

### 所需软件包

所需依赖见[手动构建](../getting-started/installation.md#manual-build)。

<a id="clone-the-repository"></a>

### 克隆仓库

克隆仓库时必须包含子模块：`git clone --recurse-submodules https://github.com/hyprwm/Hyprland.git`

<a id="building"></a>

### 构建

<a id="vscode"></a>

#### VSCode

安装并使用 C/C++ 和 CMake Tools 扩展。

Hyprland 仓库中有一个 [launch.json](https://github.com/hyprwm/Hyprland/blob/main/example/launch.json) 文件，你可以将它复制到仓库根目录下的 `.vscode/` 目录中。

配置好后，以调试模式构建，再打开调试选项卡，点击 `(gdb) Launch`。

<a id="generic"></a>

#### 通用方法

运行 `make debug` 构建，再运行 `gdb build/Hyprland` 启动 Hyprland 并附加调试器。

<a id="nix"></a>

### Nix

请参阅 [Nix 贡献与调试页面](../nix/contributing-and-debugging.md)。

<a id="development-environment"></a>

## 开发环境

<a id="setup"></a>

### 设置

在 `~/.config/hypr` 中创建一份配置文件副本，命名为 `hyprlandd.lua`。
`Debug` 构建会自动使用默认搜索路径下的 `hyprlandd.lua`，也可以传入 `--config ~/path/to/conf.lua` 来指定其他配置文件位置。

<a id="recommended-debug-config-changes"></a>

#### 建议对调试配置做的修改

- 删除配置中的 _所有_ autoexec 指令。
- 更改键位绑定的默认修饰键（例如 `SUPER` → `ALT`）。

<a id="launch-the-dev-env"></a>

#### 启动开发环境

_登录 Hyprland 会话后_，运行 `./build/` 目录中构建生成的 `Hyprland` 可执行文件。
此时应该会打开一个新窗口，Hyprland 就运行在其中。
现在你可以在这个嵌套会话中进行测试，无需担心破坏正在使用的会话。

我也建议用 `gdb` 之类的调试器启动 Hyprland。
如果你使用 IDE，它很可能支持这种启动方式，否则运行 `gdb ./build/Hyprland` 通常就够了。
这样，当 Hyprland 崩溃时，GDB 会暂停执行，你可以用 `bt`、`frame`、`print` 等命令检查当前状态。
使用 IDE 还可以在图形界面中检查这些信息。

<a id="lsp-and-formatting"></a>

## LSP 与代码格式化

如果你的编辑器不会自动配置 LSP，可以使用 clangd 来获得完整的 LSP 支持。
由于还没有生成编译命令，你可能会看到许多警告。运行以下命令即可生成编译命令：

```sh
cmake -S . -B build/ -G Ninja -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
```

另外，提交 PR 前，请用 clang-format 格式化代码。
如果只想格式化你修改的部分，请在项目根目录运行 `git-clang-format`。

<a id="logs-dumps-etc"></a>

## 日志、转储等

你可以查看日志并使用 GDB 调试器。对于偶发的缺陷，把调试模式构建的 Hyprland 作为日常环境用上一段时间，可能会发现更多线索。

Hyprland 崩溃后，先运行 `coredumpctl`，再运行 `coredumpctl info PID` 查看转储信息。有关 `coredumpctl` 的更多说明，请见下文。

你还可以用下面这条很方便的命令

```sh
watch -n 0.1 "grep -v \"arranged\" $XDG_RUNTIME_DIR/hypr/$HYPRLAND_INSTANCE_SIGNATURE/hyprland.log | tail -n 40"
```

实时查看日志。
（对于调试构建，请将 `hyprland` 替换为 `hyprlandd`。）

<a id="how-do-i-get-a-coredump"></a>

### 如何获取核心转储？

请参阅 [`ISSUE_GUIDELINES.md`](https://github.com/hyprwm/Hyprland/blob/main/docs/ISSUE_GUIDELINES.md)。
