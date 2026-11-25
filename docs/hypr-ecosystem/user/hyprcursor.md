# hyprcursor

[hyprcursor](https://github.com/hyprwm/hyprcursor) 是一种新的光标主题格式，相比广泛使用的 XCursor 有许多优势。

<a id="hyprcursor-themes"></a>

## hyprcursor 主题

你需要自行获取这些主题。
如果你已加入 Discord 服务器，可以查看 `#hyprcursor-themes` 频道。

将主题放在 `~/.local/share/icons` 或 `~/.icons` 中。

> [!WARNING]
> 由于可能遇到权限问题，不建议将光标主题放在系统目录 `/usr/share/icons` 中。

你可以通过环境变量或 `hyprctl setcursor` 设置主题。

环境变量：
- `HYPRCURSOR_THEME` 设置光标主题。
- `HYPRCURSOR_SIZE` 设置光标大小。

`hyprland.lua` 配置片段示例：

```lua
hl.env("HYPRCURSOR_THEME", "MyCursor")
hl.env("HYPRCURSOR_SIZE", "24")
```

<a id="creating--porting-themes"></a>

## 创建或移植主题

前往 [hyprcursor 仓库](https://github.com/hyprwm/hyprcursor)。

具体说明见 `docs/` 和 `hyprcursor-util/` 目录。

<a id="important-notes"></a>

## 注意事项

许多应用都支持服务端光标，例如使用 Qt、Chromium 或 Electron 的应用以及 Hypr 生态系统中的应用，但仍有一些应用不支持，例如 GTK 应用。

既不支持服务端光标也不支持 hyprcursor 的应用仍会回退到 XCursor。

对于这些应用，你需要设置并导出 `XCURSOR_THEME` 和 `XCURSOR_SIZE`，分别指定有效的 XCursor 主题和光标大小。对于 GTK，还需运行以下命令：

```sh
gsettings set org.gnome.desktop.interface cursor-theme 'THEME_NAME'
```

如果 GSettings 模式定义不可用（例如，在 NixOS 上你会看到 `No schemas installed`），可以改为运行：

```sh
dconf write /org/gnome/desktop/interface/cursor-theme "'THEME_NAME'"
```

如果是 Flatpak 应用，请运行：

```sh
flatpak override --filesystem=~/.themes:ro --filesystem=~/.icons:ro --user
```

然后将主题同时放在 `/usr/share/themes` 和 `~/.themes` 中。
图标和 XCursor 光标也要同时放在 `/usr/share/icons` 和 `~/.icons` 中。

<a id="i-dont-want-to-use-hyprcursor"></a>

## 我不想使用 hyprcursor

如果你没有安装任何 hyprcursor 主题，Hyprland 会回退到 XCursor，并使用你通过 `XCURSOR_THEME` 和 `XCURSOR_SIZE` 设置的主题和光标大小。

<a id="my-cursor-is-a-hyprland-icon"></a>

## 为什么我的光标是 Hyprland 图标？

参见[常见问题](../../faq/_index.md)。
