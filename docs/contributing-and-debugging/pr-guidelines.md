# PR 指南

<a id="pr-requirements"></a>

## PR 要求

- 代码简洁清晰，避免取巧的写法
- 说明改了什么，以及_为什么_这样改
- 遵循下文的代码风格

<a id="ai-policy"></a>

## AI 政策

你**必须**遵守我们的 [AI 政策](https://github.com/hyprwm/.github/blob/main/policies/AI_USAGE.md)。
违反政策可能会导致你今后被禁止提交任何 PR！

<a id="code-style"></a>

## 代码风格

提交 PR 前请阅读本节，以免维护者在审查时反复指出风格上的小问题，节省他们的时间。

<a id="before-you-submit"></a>

### 提交前

请确保已运行 clang-format：`make format-fix`

检查你的改动是否违反了 `clang-tidy` 规则。
通常可以直接在 IDE 中进行这项检查。

<a id="clang-format"></a>

### Clang-format

这项要求没有商量的余地。
你的代码**必须**经过格式化。

<a id="clang-tidy"></a>

### Clang-tidy

项目不强制要求解决所有 Clang-tidy 报告的问题，但请尽量减少这类问题，_只有_在确实必要时才忽略。

我们已调整过规则，99% 的情况下，你都应该修复它报告的问题。

<a id="testing"></a>

### 测试

有关 Hyprland 及相关项目的测试，请参阅[测试](tests.md)页面。

_必须_保证原本通过的测试继续通过。如果改动可以测试，就_必须_添加新测试（例如，图形界面方面的改动无法测试）。

<a id="other"></a>

### 其他

以下是 clang-tidy 和 clang-format 检查不到的一些问题：

- _基本类型_（int、float、double、size_t 等）的变量必须初始化。
- 如果 if/else 分支体只有一_行_（按行数算，不按语句数算），就不要用 `{}` 把它括起来。
  - 上一条规则不适用于循环等结构。
- 空函数体内可以考虑加一个 `;`。
- 初始化包含大量元素的 vector、数组或 map 时，在最后一个元素后加上 `,`，让排版更整齐。
- 在头文件中，能用前向声明代替包含头文件时，可以考虑使用前向声明，以缩短编译时间。
- 禁止使用 `using namespace std;`。`using namespace (anything else)` 只允许出现在源文件中，不能出现在头文件中。
- 优先使用提前返回来减少嵌套。`if(!valid) return;` 比 `if (valid) { /* a billion things */ }` 好得多。

<a id="naming-conventions"></a>

### 命名约定

代码应使用 `camelCase` 命名。如果变量是类的成员，还应加上 `m_` 前缀（结构体成员不加）。

另有以下约定：

- 类名以 `C` 开头，例如 `CMyClass`
- 结构体名以 `S` 开头，例如 `SMyStruct`
- 接口名以 `I` 开头，例如 `IMyInterface`
- 指向单例的全局指针以 `g_` 开头，例如 `g_someManager`
- 常量名全部大写，例如 `const auto MYVARIABLE = ...`

<a id="general-code-requirements"></a>

## 通用代码要求

<a id="no-raw-pointers"></a>

### 不使用裸指针

规则很简单：除非_确有必要_，否则不要使用裸指针（例如 `CMyClass*`）。
你可以使用 `UP`、`SP` 和 `WP`。
它们分别是独占指针、共享指针和弱指针。

<a id="no-malloc"></a>

### 不使用 malloc

除非确有必要，否则不要使用 `malloc`/`free`。
你_一定会_忘记释放内存。

<a id="avoid-dubious-cleanups"></a>

### 避免不可靠的资源清理方式

如果某个函数以 C 风格分配资源（例如 `some_c_call_make_new()`），通常就需要调用配套的 `some_c_call_free()` 来释放资源。
这种情况下，可以采用以下任一做法：

- 用 C++ 类封装该资源。
- 如果资源只在一个函数内使用，就用 `CScopeGuard` 确保函数退出时总会释放它。

<a id="use-the-stl"></a>

### 使用 STL

通常应使用 STL，避免重复实现已有功能。

<a id="use-hyprutils"></a>

### 使用 hyprutils

Hyprutils 提供了许多特别适合 Hyprland 和其他 hypr\* 项目的实用工具。
请使用它们。

<a id="no-absolute-includes-from-src"></a>

### 包含头文件时不要使用以 /src 为起点的绝对路径

假设目录结构如下：

```
src/
   a/
      a.hpp
   b/
      b.hpp
```

如果要在 `a.hpp` 中包含 `b.hpp`，就_必须_使用 `../b/b.hpp`，_不能_使用 `b/b.hpp`。
后一种写法会导致插件无法正常工作。

你可能会在代码中看到一个例外：允许使用从项目根目录算起的绝对路径（例如 `protocols/some-protocol.hpp`）。
