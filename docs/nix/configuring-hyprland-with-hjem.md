# 使用 Hjem 配置 Hyprland

Hjem（丹麦语意为“家”）是一个模块系统，可让你轻松管理 `$HOME` 中的文件，包括 `~/.config` 和其他目录下的文件。
Hjem 旨在提供一种易于理解的替代工具，让你以纯函数式的方式安全地管理 `$HOME`。

要了解如何安装和使用 Hjem，可以阅读这份出色的 [Hjem 文档](https://hjem.feel-co.org/)。

<a id="writing-your-hyprlandlua-directly-inside-your-nix-config"></a>

## 直接在 Nix 配置中编写 hyprland.lua

下面的示例展示了如何借助 Hjem 直接在 Nix 配置中编写 `hyprland.lua` 的内容，这样就可以使用 Nix 字符串插值。

```lua {filename="hyprland.nix"}
{
    hjem.users.youruser.xdg.config.files."hypr/hyprland.lua".text = /* lua */ ''
      # 在此填写 hyprland.lua 的内容。
      # 可以使用字符串插值，让 Nix 在构建时对变量求值。
      # 以下 hyprland.lua 配置片段使用字符串插值，让 Nix 对其中的部分变量求值：
          local monitor1 = "${config.custom.host.monitors."1"}"
          local monitor2 = "${config.custom.host.monitors."2"}"
          hl.monitor({
              output   = monitor2,
              ${lib.optionalString (hostName == "deck") "transform = 3"}
          })
    ''
}
```

<a id="sourcing-a-hyprlandlua-file-at-your-nix-config"></a>

## 在 Nix 配置中引用 hyprland.lua 文件

除了直接在 Nix 配置中编写 `hyprland.lua` 的内容，你还可以使用 Hjem 引用已有的 `hyprland.lua` 文件，将其链接到 `~/.config/hypr/` 下的相应位置。
如果使用版本控制，请确保这个 `hyprland.lua` 与 Nix 配置位于同一仓库。
不过，采用这种方式无法使用 Nix 字符串插值。

```nix {filename="hyprland.nix"}
{
    hjem.users.youruser.xdg.config.files."hypr/hyprland.lua".source = ./relative/path/to/file;
}
```

如果已经将 `hyprland.lua` 拆分为多个文件，也可以用同样的方式引用它们。

```nix {filename="hyprland.nix"}
{
    hjem.users.youruser.xdg.config.files = {
        "hypr/hyprland.lua".source = ./relative/path/to/hyprland.lua;
        "hypr/rules.lua".source = ./relative/path/to/rules.lua;
        "hypr/keybinds.lua".source = ./relative/path/to/keybinds.lua;
        "hypr/animations.lua".source = ./relative/path/to/animations.lua;
    };
}
```

对于上面这样的多文件配置，你可能更希望直接链接整个目录。
Hjem 支持这样做，但整个目录会变为只读。
这可能会带来问题，因为无法在该目录中创建新文件，某些应用也会因此无法正常工作。
如果只想递归地链接目录中的文件，可以看看 [FindFiles](#findfiles)。

<a id="hjem-impure"></a>

## Hjem-impure

你很可能会经常修改 `hyprland.lua` 文件。
如果想尝试修改 Hyprland 配置，又不想重新构建并切换到新的 NixOS 配置，该怎么办？
Hjem 部署 `hyprland.lua` 时，会在 `~/.config/hyprland.lua` 创建一个指向 Nix 存储中文件的符号链接。
这个文件默认只读，但借助 [`hjem-impure`](https://github.com/Rexcrazy804/hjem-impure) 工具，就可以轻松修改它。

运行 `hjem-impure` 会将 Hjem 创建的每个符号链接替换为可写的普通文件或目录。
之后就可以直接编辑 Hjem 部署的 `~/.config/hyprland.lua` 文件。
**这样就能试验不同的配置。**
重新构建并切换 NixOS 配置或重启系统后，你对 `~/.config/hyprland.lua` 所做的修改**都会丢失**。
因此，对修改满意后，请将其写入 Nix 配置以便永久保留。

<a id="findfiles"></a>

## FindFiles

[FindFiles](https://github.com/Michael-C-Buckley/findFiles.nix) 是一个小型 Nix 库，让你可以轻松地将配置中的整个目录逐文件链接到相应位置。
它与 Hjem 等主目录管理工具配合使用：FindFiles 负责递归查找目录中的文件，主目录管理工具负责创建链接。
这样只需一行代码，就能为目录中的每个文件分别创建链接，而无需链接目录本身。
Hjem 通常会链接整个目录，这意味着目录会变为只读。
如果需要热重载，FindFiles 可以与 Hjem-impure 配合使用。
例如，可以用 FindFiles 实现以下配置：

- 在仓库中维护一个配置目录，将其内容映射到整个 `~/.config` 目录树中。
- 在仓库中维护一个 Hyprland 目录，将其内容自动链接到 `~/.config/hypr/`。
