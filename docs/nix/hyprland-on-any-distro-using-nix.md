# 使用 Nix 在任意发行版上运行 Hyprland

在 NixOS 以外的发行版上，通过 Nix 软件包管理器使用 Hyprland 很简单。

<a id="installing-nix"></a>

## 安装 Nix

首先安装 Nix 本身。
安装 Nix 软件包管理器主要有两种方式：





<details><summary>从上游安装</summary>


Nix 上游推荐使用多用户安装程序，详见[官方文档](https://nixos.org/manual/nix/stable/installation/index.html)。
该安装程序不受发行版的软件包管理器管理，会直接修改你的 shell 配置文件。
通过这种方式安装的 Nix 较难卸载。
安装脚本要求发行版使用 systemd。



</details>


<details><summary>从发行版安装</summary>


使用发行版的软件包管理器安装 Nix，例如 `apt`、`pacman` 或 `dnf`。
软件包几乎都叫作 `nix`。
这种方式能与操作系统良好集成，卸载起来也和其他软件包一样简单。
不过，由于 Nix 依赖动态链接库，不兼容的系统更新可能导致 Nix 无法使用。
此外，Nix 更新也需要等待发行版维护者打包和推送，无法直接从上游获取。

例如，使用 pacman 安装：

```sh
sudo pacman -S nix
```

安装后，你必须手动启用守护进程。
如果你的发行版使用 systemd，请运行以下命令：

```sh
sudo systemctl enable --now nix-daemon
```



</details>




<a id="installing-hyprland"></a>

## 安装 Hyprland
开始之前，请先在 `/etc/nix/nix.conf` 或 `~/.config/nix/nix.conf` 中添加以下内容，以[启用 flakes](https://nixos.wiki/wiki/Flakes#Enable_flakes)：

```nix
experimental-features = nix-command flakes
```

然后通过 `nix profile` 安装 Hyprland：





<details><summary>从 hyprnix 安装（推荐）</summary>


可以用以下方式安装 Hyprland 及其他 hypr\* 工具：

```sh
sudo nix profile add --profile /nix/var/nix/profiles/default github:hyprwm/hyprnix#hyprland
```

要安装该 flake 中的其他应用，请将 `#hyprland` 替换为相应的应用名（例如 `#hyprpaper`）。



</details>


<details><summary>从 Nixpkgs 安装</summary>


你可以直接从 Nixpkgs 安装 Hyprland：

```sh
sudo nix profile install --profile /nix/var/nix/profiles/default nixpkgs#hyprland
```



</details>


<details><summary>从 flake 安装</summary>


> [!NOTE]
> 请务必先启用 [Cachix](cachix.md)。

> [!WARNING]
> 此方式会从最新的不稳定 Git 分支构建 Hyprland。

```sh
sudo nix profile add --profile /nix/var/nix/profiles/default github:hyprwm/Hyprland
```



</details>




由于你在 NixOS 以外的系统上使用 Hyprland，它会找不到图形驱动。
可以使用 [nixGL](https://github.com/guibou/nixGL) 解决这个问题。

按以下方式安装即可：

```sh
sudo nix profile add --profile /nix/var/nix/profiles/default github:guibou/nixGL --impure
```

由于 `nixGL` 依赖硬件信息，安装时需要使用 `--impure`。

从 0.53.2 版起，`start-hyprland` 会在需要时自动使用 `nixGL`。
更早的版本必须使用 `nixGL start-hyprland` 启动。

最后，如果你使用 SDDM 或 GDM 等登录管理器，需要按以下方式为 `.desktop` 文件创建符号链接：

```sh
sudo mkdir -p /usr/share/wayland-sessions
sudo ln -sf /nix/var/nix/profiles/default/share/wayland-sessions/hyprland.desktop /usr/share/wayland-sessions/hyprland.desktop
```

这样登录管理器就能找到 Hyprland。

<a id="upgrading--updating"></a>

## 升级与更新

要升级所有软件包，可以运行：

```sh
sudo nix profile upgrade --profile /nix/var/nix/profiles/default '.*'
```

如需了解其他升级选项，请参阅 [Nix profile 命令文档](https://nixos.org/manual/nix/stable/command-ref/new-cli/nix3-profile.html)。
