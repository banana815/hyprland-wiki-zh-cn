# hyprshutdown

[hyprshutdown](https://github.com/hyprwm/hyprshutdown) 是一个用于正常结束会话的工具。
它会打开图形界面，请求各应用正常退出，然后退出 Hyprland。
推荐使用这种方式退出 Hyprland，因为通过其他方式退出（例如 `dispatch exit`）会导致应用被强制终止，无法正常退出。

<a id="command-line-options"></a>

## 命令行选项

| 选项 | 说明 |
|--------|-------------|
| `--vt N` | 退出后切换到第 N 个虚拟终端（可解决同时使用 NVIDIA 和 SDDM 时的黑屏问题） |
| `--dry-run` | 仅显示界面，不实际关闭应用或退出 Hyprland |
| `--no-exit` | 关闭应用，但不退出 Hyprland |
| `--top-label`, `-t` | 自定义关机对话框的文本 |
| `--post-cmd`, `-p` | Hyprland 退出后要运行的命令 |
| `--no-fork` | 在前台运行（不转为守护进程） |
| `--verbose` | 启用调试日志 |
| `--help`, `-h` | 显示帮助信息 |

<a id="tips-and-tricks"></a>

## 使用技巧

如果你想关机或重启，而不只是注销，可以参考以下示例：

```sh
hyprshutdown -t 'Shutting down...' --post-cmd 'shutdown -P 0'

hyprshutdown -t 'Restarting...' --post-cmd 'reboot'
```

<a id="troubleshooting"></a>

## 故障排查

<a id="nvidia--sddm-users"></a>

### 使用 NVIDIA 和 SDDM 的用户

如果你使用 NVIDIA 显卡和 SDDM 显示管理器，注销时遇到黑屏或卡死，请使用 `--vt` 选项：

```bash
hyprshutdown --vt 2
```

**原因：**
在使用 SDDM 的 NVIDIA 系统上，Hyprland 退出时，显示器不会自动切回 SDDM 的虚拟终端（通常是 VT2）。
`--vt` 选项会在注销后强制切换虚拟终端。

**设置方法：**
要切换虚拟终端，需要允许通过 sudo 免密码运行 `chvt`：

```bash
echo "$USER ALL=(ALL) NOPASSWD: /usr/bin/chvt" | sudo tee /etc/sudoers.d/chvt
sudo chmod 440 /etc/sudoers.d/chvt
```

这样做是安全的，因为 `chvt` 只能切换虚拟终端，无法被用来提升权限。
