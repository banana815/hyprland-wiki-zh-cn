# 权限

如果已安装 `hyprland-guiutils`，就可以使用 Hyprland 内置的权限系统。目前只有少数几项权限，今后可能会增加。

> [!TIP]
> 如果你在意这套权限系统，可能也希望阻止应用访问 Hyprland 的 [IPC 套接字](../../../ipc/_index.md)。Hyprland 本身无法强制实施这项限制，请查阅你所选用的应用沙箱的文档。

<a id="permissions"></a>

## 权限

这套权限系统的运作方式有点像 Android 的权限系统。如果应用尝试通过合成器（Hyprland）执行敏感操作，Hyprland 会弹出通知，询问你是否允许。

> [!NOTE]
> 权限系统默认关闭。配置权限前，请先设置 `hl.config({ ecosystem = { enforce_permissions = true } })` 将其启用。

<a id="configuring-permissions"></a>

### 配置权限

> [!IMPORTANT]
> 出于安全考虑，配置文件中的权限设置**不会**实时重载，必须重启 Hyprland 才能生效。

权限的配置方法很简单：

```lua
hl.permission({ binary, type, mode })
```

例如：

```lua
hl.permission({ binary = "/usr/bin/grim", type = "screencopy", mode = "allow" })
```

这条规则允许 `/usr/bin/grim` 始终无需询问即可捕获屏幕，而

```lua
hl.permission({ binary = "/usr/bin/appsuite-.*", type = "screencopy", mode = "allow" })
```
这条规则允许所有路径以 `/usr/bin/appsuite-` 开头的应用无需询问即可捕获屏幕。

<a id="permission-modes"></a>

### 权限模式

共有 3 种模式：
- `allow`：不询问，直接允许应用继续操作。
- `ask`：每当应用尝试执行敏感操作时，都弹出通知。你可以在弹窗中选择**拒绝**、**允许直到应用退出**或**允许直到 Hyprland 退出**。
- `deny`：不询问，始终拒绝应用访问。

<a id="permission-list"></a>

### 权限列表

<a id="screencopy"></a>

#### screencopy
- 默认值：**ASK**
- 允许应用在 _不经过_ xdg-desktop-portal-hyprland 的情况下访问屏幕。例如 `grim`、`wl-screenrec` 和 `wf-recorder`。
- 如果拒绝此权限，捕获的画面将是黑屏，并显示“权限被拒绝”字样。
- 为什么要拒绝？某些应用或脚本可能会直接使用 Wayland 协议，试图在你不知情的情况下恶意捕获屏幕。

<a id="plugin"></a>

#### plugin
- 默认值：**ASK**
- 允许加载插件。可以用正则表达式匹配应用的可执行文件，也可以匹配插件路径。
- _不要_ 默认允许 `hyprctl` 加载插件（攻击者可能会执行 `hyprctl plugin load /tmp/my-malicious-plugin.so`）。使用 `deny` 可禁止加载，使用 `ask` 则会在加载前询问。

<a id="keyboard"></a>

#### keyboard
- 默认值：**ALLOW**
- 允许连接新键盘。使用正则表达式匹配设备名称。
- 如果要禁用所有不匹配某个正则表达式的键盘，请添加一条将 `.*` 设为 `DENY` 的规则，并将其 _放在所有键盘权限规则的最后_。
- 为什么要拒绝？为了防范 Rubber Ducky 等按键注入设备，以及恶意虚拟键盘或 USB 键盘。

<a id="cursorpos"></a>

#### cursorpos
- 默认值：**ASK**
- 允许直接通过 Wayland 协议获取光标位置和光标图像。
- 为什么要拒绝？可以防止应用绕过 xdg-desktop-portal，悄悄跟踪你的光标位置。

<a id="input-capture"></a>

#### input-capture
- 默认值：**ASK**
- 允许捕获合成器的所有输入事件（键盘、指针和触摸事件）。
- 为什么要拒绝？可以防止应用未经你同意，恶意捕获你的所有输入。

<a id="notes"></a>

## 注意事项

<a id="portals"></a>

### 桌面门户

**xdg-desktop-portal** 的各种实现（包括 XDPH）都是普通应用，也会接受权限检查。你可以考虑添加如下规则：

```lua
hl.permission({ binary = "/usr/(lib|libexec|lib64)/xdg-desktop-portal-hyprland", type = "screencopy", mode = "allow" })
```
这适用于你没有向所有应用开放 screencopy 权限的情况。

<a id="nixos"></a>

### NixOS

在 NixOS 上，可执行文件的路径不固定，因此必须使用正则表达式。以下示例规则允许 `grim` 和 `xdg-desktop-portal-hyprland` 捕获屏幕画面：
```lua
hl.permission({ binary = "/nix/store/[a-z0-9]{32}-grim-[0-9.]*/bin/grim", type = "screencopy", mode = "allow" })
hl.permission({ binary = "/nix/store/[a-z0-9]{32}-xdg-desktop-portal-hyprland-[0-9.]*/libexec/.xdg-desktop-portal-hyprland-wrapped", type = "screencopy", mode = "allow" })
```

如果使用 Nix 本身生成配置，也可以使用字符串插值。请注意，如果路径中包含正则表达式的特殊字符（如 `+`），就需要对其进行转义：

```lua
hl.permission({ binary = "${lib.getExe pkgs.grim}", type = "screencopy", mode = "allow" })
hl.permission({ binary = [[${lib.escapeRegex (lib.getExe config.programs.hyprlock.package)}]], type = "screencopy", mode = "allow" })
hl.permission({ binary = [[${pkgs.xdg-desktop-portal-hyprland}/libexec/\.xdg-desktop-portal-hyprland-wrapped]], type = "screencopy", mode = "allow" })
```

<a id="bsd"></a>

### BSD

在某些 **BSD** 系统上，路径可能不起作用。遇到这种情况，可以考虑通过以下设置完全禁用权限系统：

```lua
hl.config({
  ecosystem = {
    enforce_permissions = false
  }
})
```

否则，你将无法通过 _配置文件_ 控制权限（弹窗仍可使用，但不会显示路径，也无法使用“记住”选项）。
