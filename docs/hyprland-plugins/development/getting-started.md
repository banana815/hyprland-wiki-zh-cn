# 插件开发入门

本页介绍从零开始编写 Hyprland 插件的基础知识。

<a id="how-do-plugins-work"></a>

## 插件如何工作？

插件本质上是由 Hyprland 动态加载的共享对象。
插件几乎可以完全访问 Hyprland 进程内部的各个部分，因此能修改的内容比脚本多得多。

<a id="prerequisites"></a>

## 前提条件

编写 Hyprland 插件需要：

- 掌握 C++
- 具备阅读能力
- 大致了解 Hyprland 的内部机制（_可以_ 边开发边学）

<a id="making-your-first-plugin"></a>

## 编写你的第一个插件

打开你喜欢的代码编辑器。

新建一个目录，本例使用 `MyPlugin`。

_**→ 如果你已经有 Hyprland 的头文件**_

如果你是通过 `make install` 安装的 Hyprland，头文件应该已经安装好了。
这种情况下，无需额外操作。

_**→ 如果你尚未克隆 Hyprland 源码**_

将 Hyprland 源码克隆到一个子目录，本例使用 `MyPlugin/Hyprland`。
运行 `cd Hyprland && make debug && sudo make installheaders && cd ..`。

准备好 Hyprland 源码后，如果你知道该怎么做，就可以从头编写插件；也可以先看看[官方插件仓库](https://github.com/hyprwm/hyprland-plugins)中的一些简单插件，例如 `csgo-vulkan-fix` 或 `hyprwinwrap`。

<a id="the-basic-parts-of-the-plugin"></a>

### 插件的基本组成部分

先在文件开头引入插件 API：

```cpp
#include <hyprland/src/plugins/PluginAPI.hpp>
```

可以看看这个头文件。
里面有不少有用的注释。

我们还要创建一个全局指针，用来保存插件句柄：

```cpp
inline HANDLE PHANDLE = nullptr;
```

稍后我们会在插件的初始化函数中初始化这个指针。
它充当插件的内部标识。

接下来是返回 API 版本的方法：

```cpp
// 切勿修改此函数。
APICALL EXPORT std::string PLUGIN_API_VERSION() {
    return HYPRLAND_API_VERSION;
}
```

这个方法告诉 Hyprland 编译插件时使用的是哪个 API 版本。
切勿修改它。
编译时会自动填入正确的值。

跳过几个示例处理函数，接下来是两个重要的函数：

```cpp
APICALL EXPORT PLUGIN_DESCRIPTION_INFO PLUGIN_INIT(HANDLE handle) {
    PHANDLE = handle;

    const std::string COMPOSITOR_HASH = __hyprland_api_get_hash();
    const std::string CLIENT_HASH = __hyprland_api_get_client_hash();

    // 务必在插件中加入这段代码，以防止因
    // 头文件版本不匹配而导致的随机崩溃。
    if (COMPOSITOR_HASH != CLIENT_HASH) {
        HyprlandAPI::addNotification(PHANDLE, "[MyPlugin] Mismatched headers! Can't proceed.",
                                     CHyprColor{1.0, 0.2, 0.2, 1.0}, 5000);
        throw std::runtime_error("[MyPlugin] Version mismatch");
    }

    // ...

    return {"MyPlugin", "An amazing plugin that is going to change the world!", "Me", "1.0"};
}

APICALL EXPORT void PLUGIN_EXIT() {
    // ...
}
```

Hyprland 会在初始化（加载）插件时调用第一个函数，因此它是 _必需的_。
你可以在这里初始化插件可能用到的一切，通常也应该这样做。
务必保存 `HANDLE`，调用 API 时需要用到它。

请注意，_只有_ 在这个函数中才能添加配置变量。

返回值应为 `PLUGIN_DESCRIPTION_INFO` 结构体，Hyprland 通过它获取插件的名称、描述、作者和版本。

第二个函数是可选的，用户卸载插件时，Hyprland 会调用它。

如果插件因自身发生故障而被卸载，Hyprland _不会_ 调用这个函数。

你无需在退出函数中卸载布局、移除配置项、分发器或窗口装饰，也无需注销钩子。
Hyprland 会为你完成这些工作。

<a id="setting-up-a-development-environment"></a>

### 搭建开发环境

为了方便开发，建议在嵌套的 Hyprland 调试会话中工作。
除非要测试依赖真实硬件的功能（例如触控板手势），否则强烈建议使用嵌套会话。

有关搭建开发环境的步骤，请参阅[贡献指南](../../contributing-and-debugging/_index.md#development-environment)。

<a id="loading--reloading-plugins"></a>

### 加载与重新加载插件

构建插件后，可以在嵌套会话中用以下命令加载它：

```sh
hyprctl plugin load /absolute/path/to/plugin.so
```

卸载插件则使用：

```sh
hyprctl plugin unload /absolute/path/to/plugin.so
```

通常的开发流程是先加载插件，检查改动的效果，再修改代码并重新构建插件，然后卸载并再次加载插件，如此反复。

可以将这些操作写成一行命令：

```sh
hyprctl plugin unload /absolute/path/to/plugin.so ; hyprctl plugin load /absolute/path/to/plugin.so
```

这样就能“重新加载”插件。

<a id="more-advanced-stuff"></a>

### 进阶内容

可以看看 `src/plugins/PluginAPI.hpp` 头文件。
其中每个方法都有注释说明其用途。

有关一些概念的进一步说明，请参阅[进阶内容](advanced.md)和[插件开发指南](plugin-guidelines.md)。
