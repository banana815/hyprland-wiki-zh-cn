# hyprlauncher

[hyprlauncher](https://github.com/hyprwm/hyprlauncher) 是一款适用于 Hyprland 的多用途启动器和选择器。
它快速、简单，并提供多种模块。

<a id="usage"></a>

## 用法

hyprlauncher _始终_以守护进程方式运行。
启动时，它会创建一个守护进程来监听请求。
如果使用 `hyprlauncher -d` 启动，首次启动时不会打开窗口。

要打开 hyprlauncher，只需将 `hyprlauncher` 绑定到一个按键。

<a id="configuration"></a>

## 配置

<a id="theming"></a>

### 主题

hyprlauncher 会沿用你的 [hyprtoolkit](../dev/hyprtoolkit.md) 主题。

<a id="config"></a>

### 配置文件

`~/.config/hypr/hyprlauncher.conf`

各配置类别及其选项和取值如下：

<a id="general"></a>

#### 常规

| 选项 | 说明 | 类型 | 默认值 |
| -- | -- | -- | -- |
| `grab_focus` | 是否强制独占键盘焦点。 | bool | `true` |

<a id="cache"></a>

#### 缓存

| 选项 | 说明 | 类型 | 默认值 |
| -- | -- | -- | -- |
| enabled | 是否允许模块缓存常用条目。 <br> 这些历史记录以明文形式保存在磁盘上的 `~/.local/share/hyprlauncher` 中。 | bool | `true` |

<a id="finders"></a>

#### 查找器

可用的查找器有 `math`、`desktop` 和 `unicode`。

前缀最多只能有一个字符。

| 选项 | 说明 | 类型 | 默认值 |
| -- | -- | -- | -- |
| `default_finder` | 指定默认使用的查找器。 | string | `desktop` |
| `desktop_prefix` | 桌面应用查找器的前缀。 | string | [[Empty]] |
| `unicode_prefix` | Unicode 查找器的前缀。 | string | `.` |
| `math_prefix` | 数学查找器的前缀。 | string | `=` |
| `font_prefix` | 字体查找器的前缀。 | string | `'` |
| `desktop_launch_prefix` | 启动每个桌面应用时使用的命令前缀，例如 `uwsm app -- `。 | string | [[Empty]] |
| `desktop_icons` | 是否在结果中显示桌面应用图标。 | bool | `true` |

<a id="ui"></a>

#### 用户界面

| 选项 | 说明 | 类型 | 默认值 |
| -- | -- | -- | -- |
| window_size | 启动器窗口的大小。 | vec2 | `400 260` |
