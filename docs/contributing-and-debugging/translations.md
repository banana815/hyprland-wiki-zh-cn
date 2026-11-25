# 翻译

Hyprland 生态中的部分项目已实现本地化。
越来越多的项目也正陆续引入本地化框架。
本页简要介绍如何为 Hyprland 应用贡献翻译。

<a id="find-the-translation-file"></a>

## 查找翻译文件

以下 hyprapps 的翻译文件已可供翻译：

- [hyprland](https://github.com/hyprwm/Hyprland/blob/main/src/i18n/Engine.cpp)
- [hyprlauncher](https://github.com/hyprwm/hyprlauncher/blob/main/src/i18n/Engine.cpp)
- [hyprpwcenter](https://github.com/hyprwm/hyprpwcenter/blob/main/src/i18n/Engine.cpp)

_后续还会有更多应用支持翻译，届时会更新此列表。_

<a id="translate"></a>

## 编写翻译

翻译使用 C++ 编写，但写法简单，无需太多专业知识。
按常规流程在 GitHub 上提交合并请求（MR）即可贡献翻译。

<a id="basic-translations-unconditional"></a>

### 基本翻译（无条件）

为指定的键和语言代码注册一条译文。
例如，要为键 `TXT_KEY_HELLO` 注册 `pl_PL`（波兰语）译文，可以这样写：

```cpp
registerEntry("pl_PL", TXT_KEY_HELLO, "Siemka!");
```

有些译文包含变量，可以这样插入：

```cpp
registerEntry("pl_PL", TXT_KEY_HELLO, "Siemka, {name}!");
```

<a id="conditional-translations"></a>

### 条件翻译

在某些语言中，你可能需要根据数量等条件调整译文（例如英语中的 apple 和 apples）。
这种情况稍复杂一些，写法如下：

```cpp
registerEntry("pl_PL", TXT_KEY_HELLO, [](const Hyprutils::I18n::translationVarMap& vars) {
    int peopleAmount = std::stoi(vars.at("count"));
    if (peopleAmount == 1)
        return "Mam {count} dziewczynkę anime.";
    int last = peopleAmount % 10;
    int lastTwo = peopleAmount % 100;
    if (last >= 2 && last <= 4 && !(lastTwo >= 12 && lastTwo <= 14))
        return "Mam {count} dziewczynki anime.";
    return "Mam {count} dziewczynek anime.";
});
```

如上所示，可以根据变量的值返回不同的字符串。
请注意，所有变量都是字符串，因此要得到整数，需要调用 `std::stoi` 之类的标准库函数。

<a id="fallbacks"></a>

### 回退机制

如果目标语言有多个地区变体，而同一条译文在两个变体中完全相同，通常只需写一个条目。

回退顺序如下：

- `xy_ZT`
- `xy_XY`
- `xy_ANYTHING`
- 全局回退语言（通常为 `en_US`）

例如，如果你编写了 `de_DE` 译文，而用户的语言设置为 `de_AT`，在缺少 `de_AT` 译文时，就会使用 `de_DE` 译文。
