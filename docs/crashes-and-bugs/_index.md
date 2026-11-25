# 崩溃与缺陷

<a id="getting-the-log"></a>

## 获取日志

首先，将 `debug.disable_logs` [设为](../configuring/core/config-options.md#syntax) `false`，确保已启用日志记录。
如果还需要 OpenGL 消息，请将 `debug.gl_debugging` 设为 `true`。

日志记录完毕后，记得撤销这些设置，因为它们会降低性能。

> [!TIP]
> 可以在运行时使用 `hyprctl eval` 更改选项，随时开关调试日志。
> 如果不需要查看启动日志，可以考虑用这种方式设置调试选项，无需写入配置文件。这样一来，调试结束后只需重新加载配置即可关闭日志记录。

如果你在 TTY 中，且崩溃的是最近一次启动的 Hyprland 会话，可以用以下命令输出日志：

```sh
cat $XDG_RUNTIME_DIR/hypr/$(ls -t $XDG_RUNTIME_DIR/hypr/ | head -n 1)/hyprland.log
```

如果你正在使用 Hyprland，想查看上一次会话的日志，请使用：

```sh
cat $XDG_RUNTIME_DIR/hypr/$(ls -t $XDG_RUNTIME_DIR/hypr/ | head -n 2 | tail -n 1)/hyprland.log
```

<a id="obtaining-the-hyprland-crash-report"></a>

## 获取 Hyprland 崩溃报告

如果设置了 `$XDG_CACHE_HOME`，崩溃报告目录就是 `$XDG_CACHE_HOME/hyprland`。
否则，目录为 `$HOME/.cache/hyprland`。

进入崩溃报告目录，应该能找到一个名为 `hyprlandCrashReport[XXXX].txt` 的文件，其中 `[XXXX]` 是崩溃进程的 PID。

请将该文件作为附件添加到你的问题报告中。

<a id="crashes-at-launch"></a>

## 启动时崩溃

根据日志内容诊断问题：

- `backend failed to start`：在 TTY 中启动 Hyprland，查看红色的日志消息。
- `Monitor X has NO PREFERRED MODE, and an INVALID one was requested`：你的显示器出了故障。
- 其他情况：查看核心转储。运行 `coredumpctl`，找到最近一次核心转储对应的 PID，再运行 `coredumpctl info PID`。
- 如果在驱动程序（如 `radeon`）中出错，请提交问题报告。
- 如果在 `Hyprland` 中出错，请提交问题报告。

<a id="crashes-not-at-launch"></a>

## 启动后崩溃

请在 GitHub 或 Discord 服务器上报告问题。

<a id="obtaining-a-debug-stacktrace"></a>

## 获取调试堆栈跟踪

> 仅适用于 systemd。

1. 以调试模式构建 Hyprland（`make debug`）。
1. 启动 Hyprland 并复现崩溃。
1. 在 TTY 或终端中运行 `coredumpctl debug Hyprland`。
   - 如果 GDB 询问是否获取调试符号，输入 `y`。
   - 如果询问是否分页显示，输入 `c`。
1. 看到 `(gdb)` 提示符后，使用 `set logging enabled` 开始将日志写入文件。
   - 如需指定文件，请使用 `set logging file output.log`。
1. 运行 `bt -full`，完成后运行 `exit`，并将输出作为附件提交。

<a id="obtaining-a-trace-log"></a>

## 获取跟踪日志

设置环境变量 `HYPRLAND_TRACE=1 AQ_TRACE=1` 后启动 Hyprland。

这些变量会启用_极为_详细的日志记录，可能导致运行变慢，并产生_非常大_的日志文件，因此建议仅在调试时启用。

请尽快复现问题，这样我们就不用在上百万行日志中查找原因。

<a id="bugs"></a>

## 缺陷

首先，**_请阅读[常见问题页面](../faq/_index.md)_**。

如果其中没有列出你遇到的缺陷，可以在 Discord 服务器上提问，或在 [GitHub 上发起讨论](https://github.com/hyprwm/Hyprland/discussions)。

<a id="bisecting-an-issue"></a>

## 使用二分法定位问题

“二分查找”是指通过每次将搜索范围减半，找出最早引入某个缺陷或导致功能退化的那次 _git_ 提交。
在 `git` 中，可以使用 `git bisect` 命令完成这项操作。

如果还没有克隆 Hyprland 仓库，请先克隆：

```sh
git clone --recursive https://github.com/hyprwm/Hyprland
cd Hyprland
```

开始二分查找：

```sh
git bisect start
```

输入第一个已知没有该问题的正常提交的哈希值：

```sh
git bisect good [good commit]
```

然后输入已知存在该问题的提交的哈希值。这里可以直接使用 HEAD：

```sh
git bisect bad HEAD
```

此时，`git` 会检出指定范围中间的一次提交。
接下来，重置并构建 Hyprland：

```sh
git reset --hard --recurse-submodules
make all
```

……然后在 TTY 中运行构建生成的可执行文件 `./build/Hyprland`。

尝试复现问题。
如果无法复现（即该版本没有这个缺陷），请回到 Hyprland 仓库目录并运行 `git bisect good`。
如果可以复现，请运行 `git bisect bad`。
随后 `git` 会检出另一次提交，继续二分查找。
如果构建出错，请运行 `git bisect skip`。

再次重置、构建并安装 Hyprland，重复上述步骤，直到 `git` 找出引入缺陷的那次提交：

```
[commit hash] is the first bad commit
```

<a id="building-the-wayland-stack-with-asan"></a>

## 使用 ASan 构建 Wayland 软件栈

如果有人请你这样做，这种方法可以对内存问题进行最深入的调试。

_请在 TTY 中执行以下操作，并确保没有 Hyprland 实例正在运行。_

克隆 Hyprland：`git clone --recursive https://github.com/hyprwm/Hyprland`

`make asan`

复现崩溃。
Hyprland 会退出，你将回到 TTY。

接下来，在 `cwd`、`~` 或 `./build` 中查找名为 `asan.log.XXXXX` 的文件，其中 XXXXX 是一个数字。

将找到的所有文件打包成 ZIP 压缩包，作为附件添加到问题报告中。

<a id="debugging-drm-issues"></a>

## 调试 DRM 问题

DRM（直接渲染管理器）是内核中的底层架构，负责通过 GPU 将 GPU 缓冲区（可用作渲染目标）中的内容直接显示在屏幕上，而非显示在窗口中。

如果 Hyprland 与 DRM、驱动程序或内核之间的通信出现问题，可能会导致画面卡死、显示异常等现象。
遇到这些情况时，DRM 日志有助于排查问题。

> [!WARNING]
> 请注意，这些日志极为详尽。
> 请尽快复现缺陷，以免生成达 1 GB 的日志文件。

```sh
echo 0x19F | sudo tee /sys/module/drm/parameters/debug  # 启用详细的 DRM 日志记录
sudo dmesg -C                                           # 清空内核调试日志
dmesg -w > ~/dmesg.log &                                # 在后台将内核日志写入 ~/dmesg.log
Hyprland

# ... repro the issue, then quit Hyprland

fg # 完成后，按 CTRL+C 停止写入日志
echo 0 | sudo tee /sys/module/drm/parameters/debug # 禁用 DRM 日志记录，记得执行此步，以免系统变慢
```

完成后，请将 `dmesg.log` 文件_作为附件提交_。
