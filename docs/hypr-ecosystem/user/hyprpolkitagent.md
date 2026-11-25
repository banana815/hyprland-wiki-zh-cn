# hyprpolkitagent

[hyprpolkitagent](https://github.com/hyprwm/hyprpolkitagent) 是一个 polkit 认证守护进程。
图形应用需要认证代理才能请求提升权限。

如果你的发行版软件仓库中没有 hyprpolkitagent，可以[从源码构建](https://github.com/hyprwm/hyprpolkitagent)，也可以使用其他认证代理，例如 [KDE 的认证代理](https://github.com/KDE/polkit-kde-agent-1/)。

<a id="usage"></a>

## 用法

将 `systemctl --user start hyprpolkitagent` 添加到 Hyprland 配置的自启动项中，然后重启 Hyprland。
（如果使用其他认证代理，请改用该代理的启动命令。）



对于使用其他初始化系统的发行版（例如 Gentoo），可能需要改用 `/usr/lib64/libexec/hyprpolkitagent`。

其他可能的路径包括 `/usr/lib/hyprpolkitagent` 和 `/usr/libexec/hyprpolkitagent`。

<a id="configuration"></a>

## 配置

配置文件位于 `~/.config/hyprpolkitagent/hyprpolkitagent.conf`。
该文件是可选的。
更改会在代理下次启动时生效。

`general` 类别中的变量：

| 变量 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| `allow_empty_password` | 是否允许提交空密码。如果 PAM 在密码模块认证失败后会尝试其他方式（例如使用 howdy 进行人脸识别），此选项就很有用 | bool | `false` |
| `password_field_width` | 密码输入框的宽度，单位为像素 | int | `340` |
| `require_confirmation` | 如果无需输入即可通过认证（例如使用 howdy 进行人脸识别，或使用指纹认证），是否要等你确认后才允许执行操作 | bool | `false` |
| `show_details` | 是否允许显示或隐藏列出操作和命令的面板 | bool | `true` |
| `window_height` | 对话框的高度，单位为像素 | int | `440` |
| `window_width` | 对话框的宽度，单位为像素 | int | `520` |


<details><summary>示例</summary>


```ini { filename="~/.config/hyprpolkitagent/hyprpolkitagent.conf" }
general {
    show_details = true
}
```



</details>

<a id="theming"></a>

### 主题

颜色、圆角和字体沿用你的 [hyprtoolkit](hyprtoolkit.md) 主题。
