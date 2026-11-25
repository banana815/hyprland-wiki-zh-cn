# 使用 Home Manager 配置 Hyprland

可用选项的完整列表见 [Home Manager 选项](https://nix-community.github.io/home-manager/options.xhtml#opt-wayland.windowManager.hyprland.enable)。

> [!WARNING]
> **必需：**
> - **NixOS 模块：** 启用 Hyprland 正常运行所需的关键组件。
>   如果未启用此模块，显示管理器可能会因缺少会话文件而出现问题。
>
> **可选**：
> - **Home Manager 模块：** 让你可以通过 Home Manager 以声明式方式配置 Hyprland。
> - 该模块会配置 Hyprland 并将其加入当前用户的 `$PATH`，但不会执行某些系统级更改，例如为显示管理器添加桌面会话文件。
>   启用 NixOS 模块后，这些更改由它负责。

<a id="installation"></a>

## 安装





<details><summary>Home Manager</summary>


```nix {filename="home.nix"}
{
  wayland.windowManager.hyprland.enable = true;
}
```



</details>


<details><summary>Hyprland flake</summary>


以下代码演示如何从 flake 输入中引入 Hyprland flake，并在 Home Manager 中使用它提供的软件包。
你可以根据自己的环境调整代码。

记得将 `user@hostname` 替换为你自己的用户名和主机名！

```nix {filename="flake.nix"}
{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

    home-manager = {
      url = "github:nix-community/home-manager";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    hyprland.url = "github:hyprwm/Hyprland";
  };

  outputs = {nixpkgs, home-manager, hyprland, ...}: {
    homeConfigurations."user@hostname" = home-manager.lib.homeManagerConfiguration {
      pkgs = nixpkgs.legacyPackages.x86_64-linux;

      modules = [
        {
          wayland.windowManager.hyprland = {
            enable = true;
            # 设置 flake 软件包
            package = inputs.hyprland.packages.${pkgs.stdenv.hostPlatform.system}.hyprland;
            portalPackage = inputs.hyprland.packages.${pkgs.stdenv.hostPlatform.system}.xdg-desktop-portal-hyprland;
          };
        }
        # ...
      ];
    };
  };
}
```



</details>


<details><summary>flake-compat</summary>


本节介绍如何在不支持 Nix flakes 的 NixOS 系统上使用 Hyprland flake。

> [!WARNING]
> flake 模块只是对 Home Manager 下游模块的扩展。
> 它主要用于试用新选项，因此除非你是测试人员，否则应使用 Home Manager 下游模块。

以下代码演示如何从 flake 输入中引入 Hyprland flake，并在 Home Manager 的选项中使用它提供的软件包。
你可以根据自己的环境调整代码。

```nix {filename="home.nix"}
{pkgs, ...}: let
  flake-compat = builtins.fetchTarball "https://github.com/edolstra/flake-compat/archive/master.tar.gz";

  hyprland = (import flake-compat {
    src = builtins.fetchTarball "https://github.com/hyprwm/Hyprland/archive/main.tar.gz";
  }).defaultNix;
in {
  wayland.windowManager.hyprland = {
    enable = true;
    # 设置 flake 软件包
    package = hyprland.packages.${pkgs.stdenv.hostPlatform.system}.hyprland;
    portalPackage = hyprland.packages.${pkgs.stdenv.hostPlatform.system}.xdg-desktop-portal-hyprland;
  }
}
```



</details>




<a id="usage"></a>

## 用法

启用模块后，就可以用它以声明式方式配置 Hyprland。
配置示例如下：


```nix {filename="home.nix"}
{
  wayland.windowManager.hyprland.settings = {
    "$mod" = "SUPER";
    bind =
      [
        "$mod, F, exec, firefox"
        ", Print, exec, grimblast copy area"
      ]
      ++ (
        # 工作区
        # 将 $mod + [shift +] {1..9} 绑定为切换到工作区 {1..9}（按住 shift 时将窗口移至对应工作区）
        builtins.concatLists (builtins.genList (i:
            let ws = i + 1;
            in [
              "$mod, code:1${toString i}, workspace, ${toString ws}"
              "$mod SHIFT, code:1${toString i}, movetoworkspace, ${toString ws}"
            ]
          )
          9)
      );
  };
}
```

<a id="plugins"></a>

## 插件

在 Nix 上管理 Hyprland 插件的方式与其他发行版不同。
最明显的区别是 Nix 不支持 `hyprpm`，但我们提供了自己的插件构建和管理方式。

> [!WARNING]
> 要使用以下语法配置插件，你必须通过 [Home Manager 模块](configuring-hyprland-with-home-manager.md)或[上游 NixOS 模块](installing-hyprland-on-nixos.md)使用 Hyprland。

<a id="using-plugins-from-nixpkgs"></a>

## 使用 Nixpkgs 中的插件

Nixpkgs 提供了针对其所含 Hyprland 版本打包的插件。
用法如下：

```nix {filename="home.nix"}
{pkgs, ...}: {
  wayland.windowManager.hyprland.plugins = [
    pkgs.hyprlandPlugins.<plugin>
  ];
}
```

可以使用 `nix search nixpkgs#hyprlandPlugins ^` 查看 Nixpkgs 包含哪些插件。

<a id="hyprland-plugins"></a>

## hyprland-plugins

这些官方插件由 vaxry 开发和维护。

要使用这些插件，建议先采用 Hyprland flake，**不要**使用 Nixpkgs 中的 Hyprland 版本。

首先，将 hyprland-plugins flake 添加到你的 flake 输入中：

```nix {filename="flake.nix"}
{
  inputs = {
    hyprland.url = "github:hyprwm/Hyprland";

    hyprland-plugins = {
      url = "github:hyprwm/hyprland-plugins";
      inputs.hyprland.follows = "hyprland";
    };

    # ...
  }
}
```

`inputs.hyprland.follows` 这一行让 hyprland-plugins 使用你锁定的同一个 Hyprland 修订版本。
这样，只要同时更新这两个输入，就不会出现版本不匹配的问题。

接下来，将插件添加到 Hyprland：

```nix {filename="home.nix"}
{inputs, pkgs, ...}: {
  wayland.windowManager.hyprland = {
    enable = true;

    plugins = [
      inputs.hyprland-plugins.packages.${pkgs.stdenv.hostPlatform.system}.<plugin>
    ];
  };
}
```

<a id="faq"></a>

## 常见问题

<a id="fixing-problems-with-themes"></a>

### 解决主题问题

如果鼠标指针、图标或窗口的主题无法正确加载，可以尝试通过 `home.pointerCursor` 和 `gtk.theme` 设置主题。这些设置会启用多项兼容性选项，让主题在各种情况下都能正常加载。

配置示例：

```nix {filename="home.nix"}
{
  home.pointerCursor = {
    gtk.enable = true;
    # x11.enable = true;
    package = pkgs.bibata-cursors;
    name = "Bibata-Modern-Classic";
    size = 16;
  };

  gtk = {
    enable = true;

    theme = {
      package = pkgs.flat-remix-gtk;
      name = "Flat-Remix-GTK-Grey-Darkest";
    };

    iconTheme = {
      package = pkgs.adwaita-icon-theme;
      name = "Adwaita";
    };

    font = {
      name = "Sans";
      size = 11;
    };
  };
}
```

<a id="using-the-home-manager-module-with-nixos"></a>

### 在 NixOS 上使用 Home Manager 模块

如果你希望 Home Manager 模块使用你在 NixOS 模块中指定的 Hyprland 软件包，只要使用 [Home Manager `5dc1c2e40410f7dabef3ba8bf4fdb3145eae3ceb`](https://github.com/nix-community/home-manager/commit/5dc1c2e40410f7dabef3ba8bf4fdb3145eae3ceb) 或更高版本，就可以将 `package` 和 `portalPackage` 都设为 `null` 来实现。

```nix {filename="home.nix"}
{
  wayland.windowManager.hyprland = {
    enable = true;
    # 将 Hyprland 和 XDPH 的软件包设为 null，以使用 NixOS 模块提供的软件包
    package = null;
    portalPackage = null;
  };
}
```

**不要**混用版本不匹配的 Hyprland 和 XDPH。
如果你的 NixOS 配置使用 flake 提供的 Hyprland，也应使用同一 flake 提供的 XDPH。
如果你将 Home Manager 的 Hyprland 模块中的 Hyprland 软件包设为 `null`，也应将 XDPH 软件包设为 `null`。

<a id="programs-dont-work-in-systemd-services-but-do-on-the-terminal"></a>

### 程序在终端中可以运行，却无法在 systemd 服务中运行

出现这个问题是因为 systemd 默认不导入环境变量。
它无法获取 `PATH`，因此无法运行服务中的命令。
最常受影响的是用户自行配置的服务，例如 `hypridle` 或 `swayidle`。

要解决这个问题，请将以下内容添加到配置中：

```nix {filename="home.nix"}
{
  wayland.windowManager.hyprland.systemd.variables = ["--all"];
}
```

这项设置会在 Hyprland 配置中生成以下条目：

```lua {filename="hyprland.lua"}
hl.on("hyprland.start", function()
    hl.exec_cmd("dbus-update-activation-environment --systemd --all")
end)
```

如果你没有使用 Home Manager 模块，请务必在 Hyprland 配置中使用上述命令。
