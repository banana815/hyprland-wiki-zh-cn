# 使用插件

本页介绍如何使用插件。

<a id="disclaimers"></a>

## 免责声明

> [!WARNING]
> 插件用 C++ 编写，会作为 Hyprland 的一部分运行。
> _每次_使用新插件前，务必阅读其源代码，并确认来源可信。
> 编写一个能清空你电脑上所有数据的插件并不难。
>
> _**绝不要**_相信别人随手发给你的 `.so` 文件。

<a id="getting-plugins"></a>

## 获取插件

插件以_共享对象_的形式提供，也就是 `.so` 文件。

Hyprland 没有“默认”插件，想用什么插件都得自己找。

<a id="installing--using-plugins"></a>

## 安装和使用插件

_强烈_建议使用 Hyprland 插件管理器 `hyprpm`。
手动操作步骤请见[此处](#manual)。

<a id="hyprpm"></a>

### hyprpm

> [!NOTE]
> 如果你启用了[权限管理](../configuring/core/advanced-configuration/permissions.md)，请在配置中加入以下内容，允许 hyprpm 加载插件：
>
> ```lua
> hl.permission("/usr/(bin|local/bin)/hyprpm", "plugin", "allow")
> ```
>
> 否则，每次 hyprpm 尝试加载插件时，都会弹窗请求授权。

如果 `hyprpm` 与 Hyprland 分开打包，请确认已安装 `hyprpm`。还要确认已安装所需的依赖：
`cpio`、`cmake`、`git`、`meson` 和 `gcc`。
如果你的发行版将二进制文件和头文件分开打包（如 Fedora 或 Debian），可能还需要安装 Hyprland 各依赖项对应的 `-dev` 软件包。

找到包含你想安装的插件的仓库。下面以 [hyprland-plugins](https://github.com/hyprwm/hyprland-plugins) 为例。

```sh
hyprpm add https://github.com/hyprwm/hyprland-plugins
```

完成后，可以用以下命令列出已安装的插件：

```sh
hyprpm list
```

然后，用 `hyprpm enable name` 启用插件，用 `hyprpm disable name` 禁用插件。

要将插件加载到 Hyprland 中，请运行 `hyprpm reload`。

可以把 `hyprpm reload` 加入 Hyprland 配置的自动启动项，让 Hyprland 在启动时加载插件。
如果喜欢，也可以加上 `-n` 标志，让插件加载成功时显示一条通知（纯粹为了好看）。
请注意，无论是否加上 `-n`，`reload` 命令遇到警告或错误时都会发出通知。

要更新插件，请运行 `hyprpm update`。

要查看 `hyprpm` 的所有选项，请运行 `hyprpm -h`。

<a id="manual"></a>

### 手动操作

不同插件的构建方法可能不同，请参阅各插件的说明。

如果尚未安装 Hyprland 头文件，请克隆 Hyprland 仓库，切换到与你当前使用的版本相对应的代码，构建 Hyprland，然后运行 `sudo make installheaders`。
接着构建你要使用的插件。

要手动加载插件，请使用 `hyprctl plugin load path`。

可以用 `hyprctl plugin unload path` 卸载已加载的插件。

也可以在 Lua 中用 `hl.plugin.load(path)` 加载插件。

> [!WARNING]
> 所有路径都必须是绝对路径！

<a id="faq-about-plugins"></a>

## 插件常见问题

<a id="how-do-i-use-them-in-my-config"></a>

### 如何在配置中使用插件？

示例：

```lua
hl.on("hyprland.start", function()
    hl.exec_cmd("hyprpm reload")
end)

function M.setup_vkfix()
    if hl.plugin.csgo_vulkan_fix ~= nil then
        hl.plugin.csgo_vulkan_fix.vkfix_app({ app = "cs2", w = 2304, h = 1440 })
        hl.config({
            plugin = {
                csgo_vulkan_fix = {
                    fix_mouse = false
                }
            }
        })
    end
end
```

这里的 `if` 可以避免插件尚未加载时报错。有些插件无法用这种方式检测。下面的示例用 Lua 尝试加载一个手动构建的插件，加载成功后再对其进行配置：

```lua
function is_plugin_loaded(name)
    for _,v in pairs(hl.get_loaded_plugins()) do
        if v.name == name then return true end
    end
    return false
end

hl.plugin.load("/absolute/path/to/example.so")

if is_plugin_loaded("example") then
    hl.config({
        plugin = {
            example = {
                ...
            }
        }
    })
end
```

<a id="my-hyprland-crashes"></a>

### 我的 Hyprland 崩溃了！

糟糕。
哎呀。
这通常说明某个插件出了问题。
用 `hyprpm disable` 禁用它。

<a id="how-do-i-list-my-loaded-plugins"></a>

### 如何列出已加载的插件？

`hyprctl plugin list`

<a id="how-do-i-make-my-own-plugin"></a>

### 如何编写自己的插件？

请见[此处](development/getting-started.md)。

<a id="where-do-i-find-plugins"></a>

### 去哪里找插件？

可以在 [hypr.land/plugins](https://hypr.land/plugins/) 找到我们精选的插件。
[awesome-hyprland](https://github.com/hyprland-community/awesome-hyprland#plugins) 上也有一份插件列表。
请注意，这份列表可能并不完整。
最后，还可以试着在 GitHub 上搜索关键词 `"hyprland plugin"`。

<a id="are-plugins-safe"></a>

### 插件安全吗？

只要你读过插件的源代码，并能确认其中没有恶意行为，就可以安全使用。

<a id="do-plugins-decrease-hyprlands-stability"></a>

### 插件会降低 Hyprland 的稳定性吗？

Hyprland 会通过几种机制尝试卸载发生崩溃的插件。
不过，这些机制并非总能奏效。
一般来说，只要插件设计得当，就不会影响 Hyprland 的稳定性。
