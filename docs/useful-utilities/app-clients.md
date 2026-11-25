# 应用客户端

有些客户端在 Wayland 下用起来出了名地麻烦。
以下是一些不错的替代选择：

<a id="discord"></a>

## Discord

- [WebCord](https://github.com/SpacingBat3/WebCord)
  是一款基于最新版 Electron 的 Discord 客户端，支持 Wayland Ozone 平台，也能通过 PipeWire 共享屏幕。
  它功能丰富，并尽量遵守 Discord 的服务条款。
- [Vesktop](https://github.com/Vencord/Vesktop)
  与 WebCord 类似，是一款改进了性能和 Wayland 支持的第三方 Discord 客户端。
  它还内置了屏幕共享功能，并支持插件和自定义主题。
  使用 Vesktop 共享屏幕时，甚至还可以正常共享音频。
  请注意，Vesktop 依赖 Vencord，而 Vencord 是一款违反 Discord 服务条款的第三方客户端模组。
  使用风险由你自行承担。
- [Dissent](https://github.com/diamondburned/dissent)
  是一款使用 GTK4 编写的 Discord 客户端。
  虽然它违反了 Discord 的服务条款，但使用起来相对安全，而且不依赖任何 WebView 技术。

<a id="matrixelement"></a>

## Matrix/Element

[Fractal](https://gitlab.gnome.org/World/fractal) 是一款使用 GTK4 编写的 Matrix 客户端。
和 Discord 一样，Element 也因基于 Electron 而存在不少广为人知的问题。
Fractal 目前尚不支持 VoIP 通话，但支持其他所有功能，包括端到端加密（E2EE）和跨设备验证。
