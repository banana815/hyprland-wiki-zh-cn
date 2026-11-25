# 高级用法

<a id="overlays"></a>

## 叠加层

<a id="default"></a>

### default

Hyprland 的 `default` 叠加层仅包含 Hyprland 软件包、xdg-desktop-portal-hyprland，以及 Hyprland 的内部依赖（udis86-hyprland 和 glaze-hyprland）。

如果希望 hypr\* 依赖保持最新，你需要自行导入这些依赖的所有叠加层。
否则，构建 Hyprland 时会使用 Nixpkgs 中提供的版本。

<a id="hyprland-packages"></a>

### hyprland-packages

如果希望通过叠加层引入所有依赖，请同时导入 `hyprland-packages` 和 `hyprland-extras` 叠加层。

> [!NOTE]
> 这些依赖有时会过时，影响其他 hypr\* 应用，例如 <https://github.com/hyprwm/Hyprland/discussions/13396>。
> 遇到这种情况，可以联系维护者更新锁文件，也可以使用 `default` 叠加层。

<a id="package-options"></a>

## 软件包选项

以下是构建 Hyprland 软件包时使用的默认选项。
将相应选项设为 `true` 或 `false` 即可更改设置。
更多选项请参阅[模块选项](https://search.nixos.org/options?channel=unstable&from=0&size=50&sort=relevance&type=packages&query=hyprland)。

<a id="package"></a>

### 软件包

可以通过 `.override` 或 `.overrideAttrs` 覆盖软件包的设置。

```nix
(pkgs.hyprland.override { # 或者使用 inputs.hyprland.packages.${pkgs.stdenv.hostPlatform.system}.hyprland
  enableXWayland = true;  # 是否启用 Xwayland
  withSystemd = true;     # 构建时是否启用 systemd 支持
})
```

<a id="nixos--hm-modules"></a>

### NixOS 和 Home Manager 模块

```nix
{
  programs.hyprland = { # 如果使用 Home Manager，则使用 wayland.windowManager.hyprland
    enable = true;
    xwayland.enable = true;
  };
}
```

<a id="using-nix-repl"></a>

## 使用 Nix REPL

如果你单独使用 Nix（未使用 NixOS 或 Home Manager），可以按以下方式覆盖软件包的设置：

```nix
$ nix repl
nix-repl> :lf github:hyprwm/Hyprland
nix-repl> :bl outputs.packages.x86_64-linux.hyprland.override { /* flag here */ }
```

然后就可以从构建产物所在的路径运行 Hyprland。
也可以使用 `overrideAttrs` 覆盖 `mkDerivation` 的参数，例如 `cmakeBuildType`：

```nix
$ nix repl
nix-repl> :lf github:hyprwm/Hyprland
nix-repl> :bl outputs.packages.x86_64-linux.hyprland.overrideAttrs (self: super: { cmakeBuildType = "Debug" })
```

<a id="building-plugins-with-nix"></a>

## 使用 Nix 构建插件

Nixpkgs 中的插件和 `hyprland-plugins` 中的插件都使用通用函数 `mkHyprlandPlugin` 构建。
任何插件都可以适配这个函数。
下面以 hy3 的派生式为例，说明该函数的基本用法：

```nix {filename="plugin.nix"}
{
  lib,
  fetchFromGitHub,
  cmake,
  hyprland,
  hyprlandPlugins,
}:
hyprlandPlugins.mkHyprlandPlugin (finalAttrs: {
  pluginName = "hy3";
  version = "0.39.1";

  src = fetchFromGitHub {
    owner = "outfoxxed";
    repo = "hy3";
    rev = "hl${finalAttrs.version}";
    hash = "sha256-PqVld+oFziSt7VZTNBomPyboaMEAIkerPQFwNJL/Wjw=";
  };

  # 插件所需的所有 nativeBuildInputs
  nativeBuildInputs = [cmake];

  # 设置 Hyprland 尚未包含的所有 buildInputs
  # 默认包含 Hyprland 及其依赖项
  buildInputs = [];

  meta = {
    homepage = "https://github.com/outfoxxed/hy3";
    description = "Hyprland plugin for an i3 / sway like manual tiling layout";
    license = lib.licenses.gpl3;
    platforms = lib.platforms.linux;
  };
})
```

```nix {filename="home.nix"}
{pkgs, ...}: {
  wayland.windowManager.hyprland.plugins = [
    (pkgs.callPackage ./plugin.nix {})
  ];
}
```

`mkHyprlandPlugin` 本质上是对 `stdenv.mkDerivation` 的封装，因此同样接受一个属性集，其中大多数选项与 `mkDerivation` 的选项相同。

<a id="fixing-problems-with-themes"></a>

## 解决主题问题

如果鼠标指针、图标或窗口主题无法正确加载，请参阅[通过 Home Manager 使用 Hyprland](configuring-hyprland-with-home-manager.md) 中的相关章节。

如果你不想使用 Home Manager，也可以按以下方式使用 dconf 解决 GTK 主题问题：

```nix {filename="configuration.nix"}
{
  programs.dconf.profiles.user.databases = [
    {
      settings."org/gnome/desktop/interface" = {
        gtk-theme = "Adwaita";
        icon-theme = "Flat-Remix-Red-Dark";
        font-name = "Noto Sans Medium 11";
        document-font-name = "Noto Sans Medium 11";
        monospace-font-name = "Noto Sans Mono Medium 11";
      };
    }
  ];
}
```
