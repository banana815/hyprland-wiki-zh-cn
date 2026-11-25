# 键盘布局

<a id="switchable-keyboard-layouts"></a>

## 可切换的键盘布局

> [!WARNING]
> 默认情况下，按键绑定使用 input 配置节中定义的第一个键盘布局。
>
> 例如，使用 `us,ua` 布局顺序时，可以在配置中将按键绑定写为 `"SUPER + A"`；如果顺序是 `ua,us`，同一按键绑定就要写为 `"SUPER + Cyrillic_ef"`。
>
> 你可以在全局或针对单个设备设置 `resolve_binds_by_sym = 1` 来改变这一行为。这样，当输入的符号与按键绑定中指定的符号匹配时，就会触发该按键绑定。
>
> 例如，如果你的布局是 `us,fr`，并且配置了 `"SUPER + A"` 按键绑定，那么在 `us` 布局下，需要按住 SUPER 并按下第二排的第一个字母键；在 `fr` 布局下，则需要按住 SUPER 并按下第一排的第一个字母键。

<a id="xkb"></a>

### XKB

切换布局的一种方法是设置 XKB 选项，例如：

```lua
hl.config({
    input =  {
        kb_layout = "us,cz",
        kb_variant = ",qwerty",
        kb_options = "grp:alt_shift_toggle"
    }
})
```

每个布局的变体都要单独设置，因此变体的数量和顺序必须与要应用这些变体的布局一一对应。

<a id="hyprctl"></a>

### Hyprctl

你也可以将某个按键绑定到 `hyprctl switchxkblayout` 命令，从而更灵活地设置布局切换快捷键。参阅[使用 hyprctl](../advanced-configuration/using-hyprctl.md)。

要查找可用的布局和 `kb_options` 取值，可以查看 `/usr/share/X11/xkb/rules/base.lst`。

例如，要查找某种语言的布局名称：

```sh
grep -i 'persian' /usr/share/X11/xkb/rules/base.lst
```

要列出可在 `kb_options` 中设置、用于切换键盘布局的快捷键：

```sh
grep 'grp:.*toggle' /usr/share/X11/xkb/rules/base.lst
```

<a id="misc"></a>

## 其他

<a id="workspace-bindings-on-non-qwerty-layouts"></a>

### 非 QWERTY 布局下的工作区按键绑定

在当前键盘布局下，用于按键绑定的键必须能在不按任何修饰键的情况下直接输入。

例如，[法语 AZERTY](https://en.wikipedia.org/wiki/AZERTY) 布局使用 SHIFT + _`unmodified key`_ 来输入 `0-9` 的数字。因此，这种布局的按键绑定必须使用 _未按修饰键时的键名_，使用 `0-9` 的数字不会生效。

> [!NOTE]
> 要确定 `unmodified_key` 的正确名称，请参阅[关于不常见键符号的小节](_index.md#uncommon-syms--binding-with-a-keycode)。

有几种方法可以解决这个问题：
1. 使用键码；
1. 使用通用键名。

<a id="keycodes"></a>

#### 键码

你可以使用 `code:int` 语法按键码绑定按键。从 1 到 0 的十个数字键依次对应键码 10 到 19。例如，`1` 对应 `code:10`。

<a id="generic-key-name"></a>

#### 通用键名

要查找通用键名，需要查看当前键盘布局的 XKB 文件。

例如，法语布局位于 `/usr/share/X11/xkb/symbols/fr` 文件中，其中列出了以下键名：

```plain
1 — ampersand
2 — eacute
3 — quotedbl
4 — apostrophe
5 — parenleft
6 — egrave
7 — minus
8 — underscore
9 — ccedilla
0 — agrave
```
