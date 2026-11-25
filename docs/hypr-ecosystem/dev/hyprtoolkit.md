# hyprtoolkit（开发者文档）

Hyprtoolkit 是一个纯 C++ 工具包。
它采用 Hyprland 风格的现代 C++，并使用 hyprutils 等库。

建议先熟悉 C++，再用 hyprtoolkit 开发应用程序。

用户文档请参阅 [hyprtoolkit 用户文档](../user/hyprtoolkit.md)。

<a id="getting-started"></a>

## 入门

_如果你喜欢通过示例学习，可以查看 hyprtoolkit 仓库中的 `tests/` 目录。_

先从创建后端和打开窗口入手：

```cpp
// 本例中这样做是为了跳过 Hyprtoolkit::
using namespace Hyprtoolkit;

auto backend = CBackend::create();
auto window = CWindowBuilder::begin()->appTitle("Hello")->appClass("hyprtoolkit")->commence();
```

这段代码会创建窗口句柄，此时窗口尚未打开。

Hyprtoolkit 是保留模式工具包，用 C++ 定义一次布局后，就可以交给工具包管理。

首先需要一个矩形作为背景，可以这样创建：

```cpp
window->m_rootElement->addChild(CRectangleBuilder::begin()->color([] { return backend->getPalette()->m_colors.background; })->commence());
```

> [!NOTE]
> 请尽量使用调色板，让应用程序遵循用户的主题。

所有元素都在 `hyprtoolkit/elements/` 目录下，可在其中查看。
下面添加一个包含按钮的简单布局：

```cpp
auto layout = CColumnLayoutBuilder::begin()->size({CDynamicSize::HT_SIZE_PERCENT, CDynamicSize::HT_SIZE_PERCENT, {1.F, 1.F}})->commence();
layout->setMargin(3);

window->m_rootElement->addChild(layout);

layout->addChild(CButtonBuilder::begin()
                       ->label("Do something")
                       ->onMainClick([](SP<CButtonElement> el) { std::println("Did something!"); })
                       ->size({CDynamicSize::HT_SIZE_AUTO, CDynamicSize::HT_SIZE_AUTO, {1, 1}})
                       ->commence()
                );
layout->addChild(CButtonBuilder::begin()
                       ->label("Do something else")
                       ->onMainClick([](SP<CButtonElement> el) { std::println("Did something else!"); })
                       ->size({CDynamicSize::HT_SIZE_AUTO, CDynamicSize::HT_SIZE_AUTO, {1, 1}})
                       ->commence()
                );
```

这段代码会添加一个包含两个按钮的列布局，其中的元素从上到下排列。
按钮会根据各自的内容自动调整大小。

完成后，添加关闭回调，打开窗口并进入主循环：

```cpp
window->m_events.closeRequest.listenStatic([w = WP<IWindow>{window}] {
    w->close();
    backend->destroy();
});

window->open();

backend->enterLoop();
```

<a id="layout-system"></a>

## 布局系统

布局系统使用绝对定位和布局定位两种模式。下面分别介绍。

<a id="absolute-mode"></a>

### 绝对定位模式

当元素的父元素既不是 `ColumnLayout` 也不是 `RowLayout` 时，会使用此模式。
子元素根据自身的定位模式，在父元素内部定位。
可以用 `setPositionMode` 设置定位模式，用 `setAbsolutePosition` 添加偏移量。

例如：

- 用 `setPositionMode` 将定位模式设为 `CENTER`，子元素就会在父元素中居中。
- 用 `setPositionMode` 将定位模式设为 `ABSOLUTE`，子元素就会位于父元素的左上角。
- 在上一种设置的基础上，用 `setAbsolutePosition` 将偏移量设为 `{200, 200}`，子元素就会从父元素左上角向右、向下各移动 200 个布局像素。

<a id="layout-mode"></a>

### 布局定位模式

当元素的父元素是布局时，会使用此模式。
布局会尝试为子元素定位。
其工作方式类似于 CSS 的 `flex` 和 Qt 的 `RowLayout`、`ColumnLayout`，但不会换行。
如果元素溢出且无法收缩，就会消失。

RowLayout 将元素水平并排放置，ColumnLayout 则将元素从上到下排列。

<a id="size"></a>

### 尺寸

每个元素都有一个 `SizeType`。
布局系统据此确定元素的大小。

- `ABSOLUTE` 以布局像素指定大小，使元素的尺寸固定。
- `PERCENT` 用 `(0, 0) - (1, 1)` 范围内的比例分别指定宽和高。元素的宽和高等于父元素的相应尺寸乘以对应比例。
- `AUTO` 会忽略传入的向量（留空即可），并始终尝试调整大小以容纳子元素\*。

> [!NOTE]
> 有些元素（例如 `Text`）会强制使用自身确定的尺寸。
> 请将这些元素保留为 `AUTO`，以免混淆。

<a id="elements"></a>

## 元素

大多数元素的用途从名称就能看出来。
查看各元素的构建器函数，可以了解它们支持哪些样式和行为选项。

每个元素都通过 `Builder` 创建，以保持 ABI 稳定。
调用 `->commence()` 后，会得到一个指向新建对象的 `SP`。

随时可以调用 `->rebuild()` 重新构建对象，此时会再次得到一个构建器。
**修改完成后，记得调用 `commence()` 使更改生效！**

使用 `addChild` 将元素添加到树中后，无需再保留 `SP`。

<a id="other"></a>

## 其他

本节介绍其他杂项功能。

<a id="system-icons"></a>

### 系统图标

使用 `CBackend::systemIcons()` 函数可以获取对 `ISystemIconFactory` 的引用，并通过它按名称查询系统图标。
检查返回的结果对象即可判断是否找到了图标。
然后将该对象传给 `ImageElement`，就能把图标添加到布局中。

<a id="additional-fds"></a>

### 附加文件描述符

如果应用程序依赖其他事件循环（例如 PipeWire 或 D-Bus 的事件循环），请记住，hyprtoolkit 的布局和渲染严格在单个线程中进行。
不能从其他线程修改布局。

要接入其他事件循环，可以使用 `CBackend::addFd()` 将文件描述符及其回调函数添加到主循环中。文件描述符可读时，就会调用该函数。
回调函数在主线程中执行，因此可以在其中执行所需的任何操作。
