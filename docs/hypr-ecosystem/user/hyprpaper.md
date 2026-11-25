# hyprpaper

[hyprpaper](https://github.com/hyprwm/hyprpaper) 是一款适用于 Hyprland 的快速壁纸工具，可通过 IPC 控制。

<a id="configuration"></a>

## 配置

配置文件位于 `~/.config/hypr/hyprpaper.conf`。
该文件是可选的。

<a id="setting-wallpapers"></a>

### 设置壁纸

壁纸通过匿名特殊配置块设置。
将显示器留空即可指定后备壁纸。

| 变量 | 说明 | 值 |
| --- | --- | --- |
| `monitor` | 显示此壁纸的显示器。留空时，此壁纸将作为后备壁纸 | 显示器 ID |
| `path` | 图像文件或包含图像文件的目录的路径。相对路径以启动 hyprpaper 时的工作目录为基准 | 路径 |
| `fit_mode` | 指定图像的显示方式。可选，默认为 `cover` | `contain`\|`cover`\|`tile`\|`fill` |
| `timeout` | `path` 为目录时，切换壁纸的间隔，单位为秒。可选，默认为 30 秒 | int |
| `order`    | `path` 选项指定目录时，决定图像的显示顺序。可选，目前仅支持 `random` | `random` |
| `recursive` | `path` 为目录时，是否递归扫描子目录。可选，默认为 `false` | bool |


<details><summary>示例</summary>


```ini
wallpaper {
    monitor = DP-3
    path = ~/myFile.jxl
    fit_mode = cover
}

wallpaper {
    monitor = DP-2
    path = ~/myFile2.jxl
    fit_mode = cover
}

wallpaper {
    monitor = 
    path = ~/fallback.jxl
    fit_mode = cover
}
```



</details>

<a id="run-at-startup"></a>

### 开机自启

要让 hyprpaper 随 Hyprland 启动，请编辑 `hyprland.lua`，将 `hyprpaper` 添加到自动启动命令中。


<a id="misc-options"></a>

### 其他选项

以下选项应在 `wallpaper{...}` 配置块之外设置。

| 变量 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| `splash` | 是否在壁纸上显示 Hyprland 启动画面 | bool | `true` |
| `splash_offset` | 启动画面向上偏移的距离 | float | `20` |
| `splash_opacity` | 启动画面的不透明度 | float | `0.8` |
| `ipc` | 是否启用 IPC | bool | `true` |

<a id="sourcing"></a>

### 引入配置文件

使用 `source` 关键字引入其他文件。
支持通配符匹配、波浪号展开和相对路径。

```ini
source = ~/.config/hypr/hyprpaper.d/*.conf
```

请注意，配置按顺序解析。
先解析 `source =` 上方的行，再解析 `~/.config/hypr/hyprpaper.d/*.conf` 匹配的文件中的行，最后解析 `source =` 下方的行。

<a id="ipc"></a>

## IPC

hyprpaper 支持通过 `hyprctl` 进行 IPC 通信。

支持的请求如下：

```sh
hyprctl hyprpaper wallpaper '[mon], [path], [fit_mode]'
hyprctl hyprpaper listactive
```

使用 `wallpaper` 设置壁纸的方式如下：

```sh
hyprctl hyprpaper wallpaper '[mon], [path], [fit_mode]'
```

与配置文件一样，`fit_mode` 是可选的，`mon` 留空表示设置后备壁纸。
后备壁纸仅适用于从未被单独指定过壁纸的显示器。

`listactive` 会输出每个显示器当前使用的壁纸，例如：

```sh
hyprctl hyprpaper listactive
HDMI-A-1: /home/user/wallpapers/wp1.jpg
eDP-1: /home/user/wallpapers/wp2.jpg
```
