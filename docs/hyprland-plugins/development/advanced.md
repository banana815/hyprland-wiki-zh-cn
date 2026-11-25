# 进阶

本页介绍 Hyprland 插件 API 的几种进阶用法。

<a id="accessing-private-members"></a>

## 访问私有成员

如果需要访问 Hyprland 某个类的私有成员，可以在包含相应头文件之前定义宏，将成员的访问权限改为公有，并在包含头文件后取消宏定义。
请注意，某些 Hyprland 文件会包含 STL 头文件，这种做法可能会导致 STL 代码编译失败。
如果遇到这个问题，请在包含 Hyprland 文件的代码段之前，先包含引发问题的 STL 头文件。

```cpp
#define private public
#include <hyprland/src/plugins/PluginAPI.hpp>
#include <hyprland/src/render/OpenGL.hpp>
#include <hyprland/src/desktop/Window.hpp>
#include <hyprland/src/layout/IHyprLayout.hpp>
#undef private
```

<a id="using-function-hooks"></a>

## 使用函数钩子

> [!WARNING]
> 函数钩子仅适用于 `AMD64`（`x86_64`）。
> 在其他架构上，Hyprland 会直接忽略设置钩子的尝试。

函数钩子初看可能令人望而生畏，但只要使用得当，功能就会_极其_强大。

函数钩子可以拦截对目标函数的每一次调用。

来看一个简单的例子：

```cpp
void Events::listener_monitorFrame(void* owner, void* data)
```

这就是我们要设置钩子的函数。
`Events::` 是命名空间，不是类，因此这是一个普通函数。

```cpp
// 为此钩子创建一个钩子类的全局实例
inline CFunctionHook* g_pMonitorFrameHook = nullptr;
// 使用 typedef 为要挂钩的函数定义函数指针类型。
typedef void (*origMonitorFrame)(void*, void*);

// 我们的钩子
void hkMonitorFrame(void* owner, void* data) {
    (*(origMonitorFrame)g_pMonitorFrameHook->m_pOriginal)(owner, data);
}

APICALL EXPORT PLUGIN_DESCRIPTION_INFO PLUGIN_INIT(HANDLE handle) {
    // 执行一些操作……

    // 创建钩子
    static const auto METHODS = HyprlandAPI::findFunctionsByName(PHANDLE, "listener_monitorFrame");
    g_pMonitorFrameHook = HyprlandAPI::createFunctionHook(handle, METHODS[0].address, (void*)&hkMonitorFrame);

    // 初始化钩子
    g_pMonitorFrameHook->hook();

    // 执行后续操作……
}
```

这样就创建好了钩子。
现在，每当 Hyprland 调用 `Events::listener_monitorFrame` 时，实际调用的都会是我们的钩子！

这样，你就可以在原函数执行前后运行代码，修改输入参数或返回结果，甚至阻止原函数执行。

你可以随时调用 `unhook()` 来解除 `CFunctionHook` 的挂钩。
之后再次调用 `hook()` 即可重新挂钩。

<a id="member-functions"></a>

### 成员函数

对于成员函数（例如 `CCompositor::focusWindow(CWindow*, wlr_surface*)`），还需要给钩子添加 thisptr 参数：

```cpp
typedef void (*origFocusWindow)(void*, CWindow*, wlr_surface*);

void hkFocusWindow(void* thisptr, CWindow* pWindow, wlr_surface* pSurface) {
    // 执行一些操作……

    // 如果还要调用原函数……
    (*(origFocusWindow)g_pFocusWindowHook->m_pOriginal)(thisptr, pWindow, pSurface);
}

APICALL EXPORT PLUGIN_DESCRIPTION_INFO PLUGIN_INIT(HANDLE handle) {
    // 执行一些操作……

    static const auto METHODS = HyprlandAPI::findFunctionsByName(PHANDLE, "focusWindow");
    g_pFocusWindowHook = HyprlandAPI::createFunctionHook(handle, METHODS[0].address, (void*)&hkFocusWindow);
    g_pFocusWindowHook->hook();

    // 执行后续操作……
}
```

> [!WARNING]
> 查找方法的速度较慢，应避免频繁查找。
> 这些条目在运行期间_不会_改变，因此建议用 `static` 保存查找结果。

<a id="why-use-findfunctionsbyname"></a>

### 为什么使用 findFunctionsByName？

为什么要用它，而不直接使用 `&CCompositor::focusWindow` 之类的表达式？有两个原因：

1. 更新后更不容易失效。
   每次更新 Hyprland，原来的地址都可能失效。
   findFunctionsByName 更能适应这种变化。
   只要函数仍然存在，就能找到它。
1. 便于处理错误。
   方法数组除了包含地址，还包含函数签名。
   你可以核对签名，完全确认找到的就是目标函数，也可以在未找到函数时抛出错误。

<a id="using-the-config"></a>

## 使用配置

你可以在 `PLUGIN_INIT` 函数中注册配置项：

```cpp
APICALL EXPORT PLUGIN_DESCRIPTION_INFO PLUGIN_INIT(HANDLE handle) {
    // 执行一些操作……

    HyprlandAPI::addConfigValue(PHANDLE, "plugin:example:exampleInt", SConfigValue{.intValue = 1});

    // 执行后续操作……
}
```

插件变量_**必须**_放在 `plugins:` 类别下。
子类别由你自行决定。
通常建议以插件名创建子类别，把该插件的所有变量都放在其中（例如 `plugins:myPlugin:variable1`）。

要获取配置值，请调用 `HyprlandAPI::getConfigValue`。

请记住，`PLUGIN_INIT` 执行完毕后，指向配置值的指针就不会再改变，因此将该指针声明为静态变量可以大幅提升性能：

```cpp
static auto* const MYVAR = &HyprlandAPI::getConfigValue(PHANDLE, "plugin:myPlugin:variable1")->intValue;
```

<a id="further"></a>

## 延伸阅读

可以阅读 `src/plugins/PluginAPI.hpp` 中的 API，也可以看看[官方插件](https://github.com/hyprwm/hyprland-plugins)。

最重要的是，玩得开心！
