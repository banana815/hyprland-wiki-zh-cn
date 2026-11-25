# aquamarine

[aquamarine](https://github.com/hyprwm/aquamarine) 是一个非常轻量的 Linux 渲染后端库。

它无意取代其他 Wayland 合成器库（如 wlroots、libweston），也不与它们竞争。
它只实现了 KMS、DRM 等底层渲染后端。

<a id="configuration"></a>

## 配置

通过以 `AQ_` 开头的环境变量，可以将配置选项传递给使用 aquamarine 的应用（如 Hyprland）。

<a id="variables"></a>

### 变量

用于配置 Aquamarine 的环境变量列在[环境变量页面](../../configuring/core/environment-variables.md)中。
