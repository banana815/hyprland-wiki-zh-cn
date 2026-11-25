# UWSM

<a id="uwsm"></a>

## UWSM

[Universal Wayland Session Manager](https://github.com/Vladimir-csp/uwsm) 将独立运行的 Wayland 合成器封装成一组 systemd 单元，提供可靠的会话管理功能，包括管理会话环境、支持 XDG 自动启动、与登录会话双向绑定，以及有序关闭会话。

请注意，uwsm 面向高级用户，本身也有一些问题和使用时需要留意的特性。

<a id="installation"></a>

### 安装


<details><summary>Arch</summary>


Arch 官方软件仓库提供了 uwsm。

```sh
pacman -S uwsm libnewt
```



</details>


<details><summary>Nix/NixOS</summary>


```nix
{
  programs.hyprland.withUWSM = true;
}
```

上述选项会生成新的桌面条目 `hyprland-uwsm.desktop`，可在显示管理器中选择。

详情请参阅[该选项的说明](https://search.nixos.org/options?channel=unstable&show=programs.uwsm.enable&from=0&size=50&sort=relevance&type=packages&query=uwsm)。

> [!WARNING]
> 如果你使用 [Home Manager 模块](../nix/configuring-hyprland-with-home-manager.md)，请务必禁用该模块的 systemd 集成功能，因为它与 uwsm 冲突。
>
> ```nix
> {
>   wayland.windowManager.hyprland.systemd.enable = false;
> }
> ```



</details>

> [!NOTE]
> 如需了解其他发行版的安装方法或手动构建步骤，请参阅项目页面的[构建与安装](https://github.com/Vladimir-csp/uwsm?tab=readme-ov-file#installation)一节。

<a id="launching-hyprland-with-uwsm"></a>

### 使用 uwsm 启动 Hyprland

> [!NOTE]
> 请留意[环境变量](../configuring/core/environment-variables.md)、[多 GPU](../configuring/extra/multi-gpu.md) 和[调度器](../configuring/core/dispatchers.md)章节中的警告。

<a id="in-tty"></a>

#### 从 TTY 启动


<details><summary>为 GNOME Keyring 配置 PAM</summary>


从 TTY 启动时，某些通常由显示管理器处理的会话集成功能可能尚未配置。
[GNOME Keyring](https://wiki.gnome.org/Projects/GnomeKeyring) 就是一个常见例子。如果 PAM 登录配置中没有 `pam_gnome_keyring.so`，密钥环就不会自动解锁，应用程序可能会提示你手动解锁。

要启用自动解锁，请将包含 `pam_gnome_keyring.so` 的配置行添加到当前登录方式使用的 PAM 配置文件中（例如，`login(1)` 使用 `/etc/pam.d/login`）。
请查阅发行版文档，确认应使用的文件和语法。
以 Arch Linux 为例：

```plain {hl_lines=[5,8,10]}
#%PAM-1.0

auth       requisite    pam_nologin.so
auth       include      system-local-login
-auth      optional     pam_gnome_keyring.so
account    include      system-local-login
password   include      system-local-login
-password  optional     pam_gnome_keyring.so    use_authtok
session    include      system-local-login
-session   optional     pam_gnome_keyring.so    auto_start
```

显示管理器（如 GDM、SDDM）通常已包含这项 PAM 配置。
只有通过控制台（TTY）登录时才需要这一步。



</details>

要使用 uwsm 启动 Hyprland，请将以下代码添加到 shell 的登录配置文件中。

```
if uwsm check may-start && uwsm select; then
    exec uwsm start default
fi
```

这样，登录 tty1 后就会出现 uwsm 的合成器选择菜单。
选择 `Hyprland` 条目即可启动。

如果希望跳过合成器选择菜单，直接启动 Hyprland，请改用以下代码作为 shell 登录配置。

```
if uwsm check may-start; then
    exec uwsm start hyprland.desktop
fi
```

<a id="using-a-display-manager"></a>

#### 使用显示管理器

如果你使用显示管理器，请在其会话选择菜单中选择 `Hyprland (uwsm-managed)` 条目。

<a id="launching-applications-inside-session"></a>

### 在会话中启动应用程序

使用 systemd 管理会话时，应用程序也应作为单元运行。
uwsm 为此[提供了辅助工具](https://github.com/Vladimir-csp/uwsm#3-applications-and-slices)。
不建议在合成器的单元中将应用程序作为子进程运行。

请在应用程序的启动命令前加上 `uwsm app --`。
该命令也支持按 ID 或路径启动桌面条目。
详情请参阅 `man uwsm` 或 `uwsm app --help`。

以下工具启动更快：

- `uwsm-app`：与按需启动的守护进程配合使用的 shell 客户端，是 uwsm 的可选组件。
- [`app2unit`](https://github.com/Vladimir-csp/app2unit)：纯 shell 实现的替代工具，也可用于打开文件，通常会更早支持新功能。
- [`runapp`](https://github.com/c4rlo/runapp/)：用 C++ 实现的替代工具，速度更快，支持的功能可能有所不同。

<a id="autostart"></a>

## 自动启动

systemd 负责处理 XDG 自动启动。由 uwsm 管理的会话会自动激活相应的目标单元。
用户服务通常需要先激活 `graphical-session.target`，本页介绍的任一启动方式都可以激活它。

有些应用程序自带原生 systemd 用户单元，可借此自动启动。
你可能需要运行 `systemctl --user enable [some-app.service]` 显式启用这些单元。
如果单元缺少 `[Install]` 段，可以用更直接的方式启用它：`systemctl --user add-wants graphical-session.target [some-app.service]`。
还需确保单元设置了 `After=graphical-session.target` 启动顺序（可通过 drop-in 配置文件添加）。

例如，只需运行一次 `systemctl --user enable hyprpaper.service`，此后 systemd 就会自动启动 hyprpaper，无需在配置中写入 `hl.exec_cmd("hyprpaper")`。

更多自动启动示例和技巧请见[这里](https://github.com/Vladimir-csp/uwsm/tree/master/example-units)。

<a id="notes"></a>

## 注意事项

建议改在 `~/.config/uwsm/env-hyprland` 中导出 `AQ_DRM_DEVICES` 变量。
这样可确保将该变量正确导出到 systemd 环境中，同时避免与其他合成器或桌面环境冲突。

```plain
export AQ_DRM_DEVICES="/dev/dri/card0:/dev/dri/card1"
```

uwsm 会自动设置 XDG 环境变量，无需显式设置。

请避免在 `hyprland.lua` 文件中设置环境变量。
请将主题、XCursor、NVIDIA 和工具包相关变量放在 `~/.config/uwsm/env` 中，将 `HYPR*` 和 `AQ_*` 变量放在 `~/.config/uwsm/env-hyprland` 中。
格式为 `export KEY=VAL`。

```plain
export XCURSOR_SIZE=24
```

更多信息请参阅 [uwsm 的 README](https://github.com/Vladimir-csp/uwsm?tab=readme-ov-file#4-environments-and-shell-profile)。

请避免使用 Hyprland 的 `exit` 调度器或直接终止 Hyprland 进程。这会让仍在运行的客户端失去合成器，打乱正常的关闭顺序，导致会话被强制关闭。
请使用 `uwsm stop`（或[其他变体](https://github.com/Vladimir-csp/uwsm#how-to-stop)）有序关闭图形会话。如果图形会话绑定了登录会话，登录会话也会一并关闭。
如果单元进入不一致状态，影响后续会话，请改用 `loginctl terminate-user ""`（这会终止该用户的所有单元）。

<a id="nixos-uwsm"></a>

## 在 NixOS 上使用 UWSM

如果你在 NixOS 模块中启用了 UWSM（`programs.hyprland.withUWSM = true`），可以按以下方式[设置环境变量](https://github.com/Vladimir-csp/uwsm?tab=readme-ov-file#4-environments-and-shell-profile "UWSM 的环境和 shell 配置")：

```nix {filename="home.nix"}
{
  xdg.configFile."uwsm/env".source = "${config.home.sessionVariablesPackage}/etc/profile.d/hm-session-vars.sh";
}
```
