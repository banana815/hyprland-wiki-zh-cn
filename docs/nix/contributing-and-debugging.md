# 参与贡献与调试

构建和调试 Hyprland 及其他 hyprwm 程序所需的一切都已包含在提供的 `devShell` 中。

只需在克隆的仓库中运行 `nix develop`，即可进入开发环境。

<a id="build-in-debug-mode"></a>

## 以调试模式构建

<a id="through-nix-build"></a>

### 使用 `nix build`

Hyprland flake 已提供调试版本：`hyprland.packages.${pkgs.stdenv.hostPlatform.system}.hyprland-debug`。

大多数 hyprwm 应用也提供各自的 `-debug` 版本。
对于未提供调试版本的程序，可以在命令行中使用 [overrideAttrs](advanced.md#using-nix-repl) 构建调试版本。根据程序所用的构建系统，设置 `cmakeBuildType = "Debug";` 或 `mesonBuildType = "debug";`。

如果不想使用 Hyprland flake，可以在调试模式下构建 Nixpkgs 中的派生。
为此，请在 NixOS 或 Home Manager 模块的 `package` 属性中使用以下代码：

```nix
hyprland.override {
  debug = true;
};
```

<a id="through-cmake"></a>

### 使用 `cmake`

除了使用 `nix build`，也可以直接调用 `cmake` 构建 Hyprland。
这样做的好处是可以增量构建：只需重新构建受改动影响的部分，无需重新构建整个仓库。

1. 克隆 Hyprland 仓库及其子模块。
1. 进入仓库目录，在 shell 中执行 `nix develop`。
1. 运行 `make debug`（其他选项见 Makefile）。

<a id="bisecting-an-issue"></a>

## 使用二分法定位问题

请按[使用二分法定位问题](../crashes-and-bugs/_index.md#bisecting-an-issue)指南操作。
构建时，运行 `nix build`。

> [!WARNING]
> 要构建支持 Tracy 的版本，请修改 `nix/default.nix` 以启用相应选项，然后运行 `nix build '.?submodules=1'`。

要查看构建日志，请传入 `--print-build-logs`（`-L`）选项。
要保留构建失败时的构建目录，请传入 `--keep-failed` 选项。

<a id="using-cachix-to-bisect"></a>

### 借助 Cachix 进行二分查找

启用 [Cachix](cachix.md) 后，可以通过 `nix run github:hyprwm/Hyprland/commit_hash` 运行指定提交对应的版本，无需自行编译，因为 Cachix 保存了 Hyprland 每次提交对应的二进制文件。

<a id="building-the-wayland-stack-with-asan"></a>

## 使用 ASan 构建 Wayland 软件栈

先运行 `nix develop`，然后按[使用 ASan 构建](../crashes-and-bugs/_index.md#building-the-wayland-stack-with-asan)指南操作。

<a id="getting-a-debug-stacktrace"></a>

## 获取调试堆栈跟踪

调试堆栈跟踪有助于查明程序崩溃的原因。
要获取准确的 Hyprland 堆栈跟踪，请确保 Hyprland 是[以调试模式构建的](#build-in-debug-mode)。

程序崩溃后，请执行以下步骤：

```sh
nix shell nixpkgs#gdb   # 临时获取 GDB
coredumpctl             # 查看最近一次崩溃进程的 PID
coredumpctl debug <PID> # 使用上一步查到的 PID
```

其余步骤与[这份指南](../crashes-and-bugs/_index.md#obtaining-a-debug-stacktrace)相同，从第 3 步开始即可。
