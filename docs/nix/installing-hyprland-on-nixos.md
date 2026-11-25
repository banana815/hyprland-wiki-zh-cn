# NixOS 上的 Hyprland

<a id="installing-hyprland-on-nixos"></a>

## 在 NixOS 上安装 Hyprland

你可以通过以下方式安装 Hyprland：

- 如果想使用当前最新的 Git 提交，可以从 Hyprland flake 安装；
- 如果想使用 Hyprland flake，但不想在 NixOS 系统上启用 flakes，可以通过 flake-compat 安装；
- 从 Nixpkgs 软件仓库安装。





<details><summary>Hyprland flake</summary>


> [!NOTE]
> 如果不想自行编译 Hyprland，请务必启用 [Cachix](cachix.md)。

如果想使用 Hyprland 的_开发版_，可以按以下方式将其添加到配置中：

```nix {filename="flake.nix"}
{
  inputs.hyprland.url = "github:hyprwm/Hyprland";
  # ...

  outputs = {nixpkgs, ...} @ inputs: {
    nixosConfigurations.HOSTNAME = nixpkgs.lib.nixosSystem {
      specialArgs = { inherit inputs; }; # 这是关键步骤
      modules = [
        ./configuration.nix
      ];
    };
  };
}
```

记得把 `HOSTNAME` 替换为你的实际主机名！

```nix {filename="configuration.nix"}
{inputs, pkgs, ...}: {
  programs.hyprland = {
    enable = true;
    # 设置 flake 软件包
    package = inputs.hyprland.packages.${pkgs.stdenv.hostPlatform.system}.hyprland;
    # 务必同时设置 portal 软件包，以保持两者版本同步
    portalPackage = inputs.hyprland.packages.${pkgs.stdenv.hostPlatform.system}.xdg-desktop-portal-hyprland;
  };
}
```

如果你在**稳定版** NixOS 上使用 Hyprland flake 时，发现游戏或 Blender 等程序开始卡顿、掉帧，很可能是因为系统和 Hyprland 使用的 `mesa` 版本不一致。

要解决这个问题，可以使用 Hyprland 的 `nixpkgs` 输入所提供的 `mesa`：

```nix {filename="configuration.nix"}
{pkgs, inputs, ...}: let
  pkgs-unstable = inputs.hyprland.inputs.nixpkgs.legacyPackages.${pkgs.stdenv.hostPlatform.system};
in {
  hardware.graphics = {
    package = pkgs-unstable.mesa;

    # 如果还需要 32 位支持（例如用于 Steam）
    enable32Bit = true;
    package32 = pkgs-unstable.pkgsi686Linux.mesa;
  };
}
```

详情请参阅 [issue #5148](https://github.com/hyprwm/Hyprland/issues/5148)。



</details>


<details><summary>flake-compat</summary>


本节介绍如何在不支持 Nix flakes 的 NixOS 系统中使用 Hyprland flake。

> [!NOTE]
> 如果不想自行编译 Hyprland，请务必启用 [Cachix](cachix.md)。

```nix {filename="configuration.nix"}
{pkgs, ...}: let
  flake-compat = builtins.fetchTarball "https://github.com/edolstra/flake-compat/archive/master.tar.gz";

  hyprland = (import flake-compat {
    src = builtins.fetchTarball "https://github.com/hyprwm/Hyprland/archive/main.tar.gz";
  }).defaultNix;
in {
  programs.hyprland = {
    enable = true;
    # 设置 flake 软件包
    package = hyprland.packages.${pkgs.stdenv.hostPlatform.system}.hyprland;
    # 务必同时设置 portal 软件包，以保持两者版本同步
    portalPackage = hyprland.packages.${pkgs.stdenv.hostPlatform.system}.xdg-desktop-portal-hyprland;
  };
}
```



</details>


<details><summary>Nixpkgs 软件仓库</summary>


```nix {filename="configuration.nix"}
{
  programs.hyprland.enable = true;
}
```

这种方式会安装当前 Nixpkgs 发行版本所包含的 Hyprland 版本。



</details>




<a id="configuring-hyprland-on-nixos"></a>

## 在 NixOS 上配置 Hyprland

使用 Nix 以声明式方式配置 Hyprland 有两种方法。
你也可以采用命令式配置，只需将 `hyprland.lua` 放在 `~/.config/hypr/` 中即可。
虽然不推荐这样做，但如果采用这种方式，就无需使用下面的两种方法。

<a id="hjem"></a>

### Hjem

Hjem 是一款简单轻量的主目录管理工具，可以将文件链接到主目录，并在用户级别配置 systemd 单元和环境变量。
[使用 Hjem 配置 Hyprland](configuring-hyprland-with-hjem.md)。

<a id="home-manager"></a>

### Home Manager

Home Manager 是一款流行的 Nix 主目录管理工具，功能丰富。
如果你希望完全使用 Nix 代码配置多种应用，Home Manager 就能做到。
[使用 Home Manager 配置 Hyprland](configuring-hyprland-with-home-manager.md)。

如果你喜欢尝试新方案，[@spikespaz](https://github.com/spikespaz) 开发了一个可在 Home Manager 和 NixOS 中使用的 Hyprland 模块。
你可以在[这里](https://github.com/hyprland-community/hyprnix)找到它。
