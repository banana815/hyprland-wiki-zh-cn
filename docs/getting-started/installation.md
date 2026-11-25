# 安装

> [!WARNING]
> Hyprland 的设计目标并非提供一套完整易用的桌面环境。
> 简单来说，它是一组工具，供你搭建自己的桌面环境。
>
> 应用、集成组件、shell 等都由**你自己**选择、安装和配置。
>
> 本 wiki 的内容_非常_详尽。
> 在认定某项功能无法正常工作或不可用之前，强烈建议先仔细查阅本 wiki。

> [!NOTE]
> NVIDIA GPU 往往无法开箱即用。
> 如果你打算使用 NVIDIA GPU，请在安装 Hyprland 后按照 [NVIDIA 页面](../nvidia/_index.md)上的说明操作。
> 这得怪 NVIDIA。

<a id="distros"></a>

## 发行版

我们在 Arch 和 NixOS 上运行并测试 Hyprland，并保证 Hyprland 能在这两个发行版上正常工作。
在其他发行版（不基于 Arch 或 Nix 的发行版）上，运行效果可能各不相同。
不过，Hyprland 采用的技术非常前沿，因此在 Pop!\_OS、Fedora、Ubuntu 等定期发布新版本的发行版上运行时，会遇到**严重**问题。
openSUSE、Solus 等滚动发行版通常可以正常运行 Hyprland。

<a id="installation"></a>

## 安装

安装 Hyprland 很简单。
用你的包管理器安装即可。

**强烈**建议使用**发行版为你打包的版本**，**不要**手动编译或使用 `-git` 包。
Hyprland 的生态庞大，依赖关系错综复杂，手动编译可能会让你遇到依赖版本过旧或不兼容的问题。

如果你因此遇到 `.so` 文件不匹配或缺失的错误，_这完全是你自己造成的_！
请参阅[这条常见问题解答](../faq/_index.md#symbol-lookup-errors)。

当然，如果你经验丰富，想参与新功能的测试，我们非常欢迎你运行最新的 Git 提交版本。
不过，遇到“.so 文件缺失”错误就别来问我们了！

[Nix](../nix/hyprland-on-any-distro-using-nix.md) 可以解决这个问题。
这种方法适合熟悉脚本运行的进阶用户。
如果你使用的发行版对 Hyprland 支持欠佳，可以考虑安装 Nix 包管理器。
它可以解决 `.so` 文件不匹配以及其他库冲突问题，并确保软件包保持最新。
所有使用 systemd 的发行版都支持 Nix，它不会干扰或取代你现用的包管理器。

<a id="packages"></a>

### 软件包

> [!WARNING]
> Hypr\* 团队不维护任何软件包。
> 如果软件包有问题，请先尝试从源码构建。

标有 `*` 的发行版不受官方支持。
这些发行版的安装说明由社区维护，无法保证其准确性。





<details><summary>Arch</summary>


从 Arch 软件仓库安装带版本标签的正式发行版：

```shell
sudo pacman -S hyprland
```

<a id="compile-from-source-automatically"></a>

##### 自动从源码编译

> [!WARNING]
> 请先阅读[安装](#installation)一节中关于使用 `-git` 包或从源码编译的警告！

从 AUR 安装时会编译最新源码：

```shell
yay -S hyprland-git
```

你也可以安装 `hyprland-meta-git` 包，自动获取并编译 hypr\* 生态中所有组件的最新 Git 版本。

```shell
yay -S hyprland-meta-git
```

> [!WARNING]
> 使用 `-git` 版本时，每当 `hyprutils` 等直接依赖项的更新破坏 ABI 兼容性，你都需要重新编译 Hyprland 和所有其他依赖该组件的工具。
> 否则就会出现“.so not found”错误。

如果你决定使用 AUR 中的 `git` 版本，可以从 [Chaotic AUR](https://aur.chaotic.cx/) 获取预编译的二进制包。
请注意，更新 `hyprutils` 等依赖项后，你可能仍需自行重新编译所有组件，因为 Chaotic AUR 不会自动完成这一步。

> [!NOTE]
> 你可以使用 [downgrade](https://github.com/archlinux-downgrade/downgrade) 轻松回退到先前的 -git 版本。



</details>


<details><summary>Nix</summary>


请参阅 [Nix 页面](../nix/_index.md)，了解如何安装 Hyprland。



</details>


<details><summary>openSUSE*</summary>


从快照 20230411 起，Factory 已收录 Hyprland。
使用 zypper 即可安装：

```sh
sudo zypper in hyprland
```

也可以通过 YaST2 Software 安装“hyprland”包。

要让 `hyprpm` 识别其依赖项，还需要安装 `hyprland-devel`：

```sh
sudo zypper in hyprland-devel
```

你也可以按照[手动构建](#manual-build)一节的说明自行构建 Hyprland。

> [!NOTE]
> Leap 不提供 Hyprland，因为它所提供的编译器以及 Hyprland 需要的大多数库都太旧了。



</details>


<details><summary>Fedora*</summary>


使用 [lionheartp/Hyprland](https://copr.fedorainfracloud.org/coprs/lionheartp/Hyprland) Copr 仓库。

你也可以按照[这里的说明](https://github.com/hyprwm/Hyprland/discussions/284)自行编译。



</details>


<details><summary>Debian*</summary>


从 Debian 14（Forky）起，软件仓库已提供 Hyprland：

```bash
sudo apt install hyprland
```

Debian 13（Trixie）的 backports 仓库也提供 Hyprland：

```bash
sudo apt install -t trixie-backports hyprland
```



</details>


<details><summary>Gentoo*</summary>


[hyproverlay](https://codeberg.org/hyproverlay/hyproverlay) 提供 hypr 系列软件包。
使用以下命令启用这个 overlay：

```sh
sudo eselect repository enable hyproverlay
sudo emaint sync -r hyproverlay
```

然后即可安装 Hyprland：

```sh
sudo emerge --ask gui-wm/hyprland
```

这个 overlay 还提供 hyprlock、hypridle、xdg-desktop-portal-hyprland、hyprland-plugins、hyprpaper 和 hyprpicker 等软件包。
[hyprwm/contrib](https://github.com/hyprwm/contrib) 中的部分社区贡献脚本也有各自独立的软件包（如 app-misc/grimblast、app-misc/hdrop 等）。

```sh
emerge --ask gui-apps/hyprlock
emerge --ask gui-apps/hypridle
emerge --ask gui-libs/xdg-desktop-portal-hyprland
emerge --ask gui-apps/hyprpaper
emerge --ask gui-apps/hyprpicker
```

有关 USE 标志和更多细节，请参阅 [Gentoo wiki 的 Hyprland 页面](https://wiki.gentoo.org/wiki/Hyprland)。



</details>


<details><summary>FreeBSD*</summary>


默认仓库提供 Hyprland 及相关软件包：

- [hyprland](https://www.freshports.org/x11-wm/hyprland)
- [hyprpaper](https://www.freshports.org/x11/hyprpaper)
- [hyprpicker](https://www.freshports.org/x11/hyprpicker)
- [xdg-desktop-portal-hyprland](https://www.freshports.org/x11/xdg-desktop-portal-hyprland)
- [其他 Wayland 相关软件](https://www.freshports.org/wayland/)



</details>


<details><summary>Ubuntu*</summary>


<a id="ubuntu-2610-stonking-stingray-universe-repository"></a>

#### Ubuntu 26.10（Stonking Stingray）的 universe 仓库

Ubuntu 26.10 提供 `hyprland` `0.56.2`，建议使用 `apt` 安装。

```bash
sudo add-apt-repository universe && sudo apt update && sudo apt install hyprland
```

> [!WARNING]
> Ubuntu 26.04 及更早版本提供的 `hyprland` 包**极其**陈旧。
> 强烈建议避免使用这些版本的软件包。
> 请[手动构建](#manual-build)整个软件栈。

<a id="ubuntu-2604-lts-resolute-raccoon-universe-repository"></a>

#### Ubuntu 26.04 LTS（Resolute Raccoon）的 universe 仓库

```bash
sudo add-apt-repository universe && sudo apt update && sudo apt install hyprland
```

<a id="ubuntu-2410-oracular-oriole-universe-repository"></a>

#### Ubuntu 24.10（Oracular Oriole）的 universe 仓库

```bash
sudo add-apt-repository universe && sudo apt update && sudo apt install hyprland
```



</details>


<details><summary>Alpine*</summary>


Alpine 的 [community 仓库](https://wiki.alpinelinux.org/wiki/Repositories#Community)目前提供 Hyprland，由社区维护。

以下命令会安装 Hyprland 及其依赖项。

```sh
apk add hyprland
```



</details>


<details><summary>Void Linux*</summary>


[由于打包理念存在分歧](https://github.com/void-linux/void-packages/issues/37544)，Void Linux 的官方仓库不提供 Hyprland。
不过，有一个[第三方仓库](https://github.com/Event-Horizon-VL/blackhole-vl)提供通过 GitHub Actions 在持续集成流程中构建的[二进制包](https://mirror.black-hole.dev/x86_64/)。

运行以下命令即可添加该仓库：

```sh
sudo cp /usr/share/xbps.d/00-repository-main.conf /etc/xbps.d/
sudo sed -i "1i repository=https://mirror.black-hole.dev/$(xbps-uhelper arch)" /etc/xbps.d/00-repository-main.conf
```

然后就可以像安装其他软件包一样安装这些包：

```sh
sudo xbps-install -S hyprland
sudo xbps-install -S hyprland-devel # 如果要使用插件
sudo xbps-install -S xdg-desktop-portal-hyprland

xbps-query -Rs hypr # 执行此步前，需要先使用 xbps-install -S 接受软件仓库的指纹
```

更多信息请参阅 [hyprland-void README](https://github.com/Event-Horizon-VL/blackhole-vl/blob/master/README.md)，其中也说明了如何使用提供的模板为 Void Linux [手动构建](https://github.com/Event-Horizon-VL/blackhole-vl?tab=readme-ov-file#installation) Hyprland。



</details>


<details><summary>Ximper*</summary>


从 Sisyphus 安装：

```bash
epmi hyprland
epmi hyprland-devel # 如果要使用插件
```

安装生态系统中的相关组件：

```bash
epmi xdg-desktop-portal-hyprland
epmi hypridle
epmi hyprpaper
epmi hyprpicker
```



</details>


<details><summary>Solus*</summary>


在 Solus 上运行：

```bash
sudo eopkg install hyprland
```



</details>




---


> [!NOTE]
> 如果你打算使用插件，请注意，某些发行版可能会将 `hyprpm` 单独打包。

<a id="manual-build"></a>

### 手动构建

<a id="dependencies"></a>

#### 依赖项

> [!WARNING]
> ***在任何情况下都绝对不要***用符号链接把不同版本的 .so 文件连在一起，这会导致内存错误和程序崩溃。
> 不管网上哪个陌生人怎么说，都一样。
> _千万别_这么做。

> [!IMPORTANT]
> Hyprland 使用 C++26 标准，因此编译器和 C++ 标准库都必须支持该标准（`gcc >= 16` 或 `clang >= 19`）。

如果列表中遗漏了软件包，请到 wiki 仓库提交拉取请求或创建 issue。





<details><summary>Arch</summary>


```plain
yay -S ninja gcc cmake meson libxcb xcb-proto xcb-util xcb-util-keysyms libxfixes libx11 libxcomposite libxrender libxcursor pixman wayland-protocols cairo pango libxkbcommon xcb-util-wm xorg-xwayland libinput libliftoff libdisplay-info cpio tomlplusplus hyprlang-git hyprcursor-git hyprwayland-scanner-git hyprwire-git xcb-util-errors hyprutils-git glaze hyprgraphics-git aquamarine-git re2 hyprland-qtutils-git muparser
```



</details>


<details><summary>openSUSE</summary>


```sh
zypper in gcc-c++ git meson cmake "pkgconfig(cairo)" "pkgconfig(egl)" "pkgconfig(gbm)" "pkgconfig(gl)" "pkgconfig(glesv2)" "pkgconfig(libdrm)" "pkgconfig(libinput)" "pkgconfig(libseat)" "pkgconfig(libudev)" "pkgconfig(pango)" "pkgconfig(pangocairo)" "pkgconfig(pixman-1)" "pkgconfig(vulkan)" "pkgconfig(wayland-client)" "pkgconfig(wayland-protocols)" "pkgconfig(wayland-scanner)" "pkgconfig(wayland-server)" "pkgconfig(xcb)" "pkgconfig(xcb-icccm)" "pkgconfig(xcb-renderutil)" "pkgconfig(xkbcommon)" "pkgconfig(xwayland)" "pkgconfig(xcb-errors)" glslang-devel Mesa-libGLESv3-devel tomlplusplus-devel
```

（去掉 `Mesa-libGLESv3-devel` 和 `pkgconfig(xcb-errors)` 后，这个方法应该也适用于 RHEL/Fedora。）



</details>


<details><summary>FreeBSD</summary>


```sh
pkg install git pkgconf gmake gcc evdev-proto cmake wayland-protocols wayland libglvnd libxkbcommon libinput cairo pango pixman libxcb meson jq hwdata libdisplay-info libliftoff
export CC=gcc CXX=g++ LDFLAGS="-static-libstdc++ -static-libgcc"
```



</details>


<details><summary>Ubuntu</summary>


<a id="ubuntu-2604-lts-resolute-raccoon"></a>

#### Ubuntu 26.04 LTS（Resolute Raccoon）

构建脚本见 [gitlab.com/kralos/hyprbuntu](https://gitlab.com/kralos/hyprbuntu)。

<a id="ubuntu-2410-oracular-oriole"></a>

#### Ubuntu 24.10（Oracular Oriole）

要从源码安装 Hyprland，需要先安装以下依赖：

```bash
sudo apt install -y meson wget build-essential ninja-build cmake-extras cmake gettext gettext-base fontconfig libfontconfig-dev libffi-dev libxml2-dev libdrm-dev libxkbcommon-x11-dev libxkbregistry-dev libxkbcommon-dev libpixman-1-dev libudev-dev libseat-dev seatd libxcb-dri3-dev libegl-dev libgles2 libegl1-mesa-dev glslang-tools libinput-bin libinput-dev libxcb-composite0-dev libavutil-dev libavcodec-dev libavformat-dev libxcb-ewmh2 libxcb-ewmh-dev libxcb-present-dev libxcb-icccm4-dev libxcb-render-util0-dev libxcb-res0-dev libxcb-xinput-dev libtomlplusplus3 libre2-dev
```

还需要从源码构建 wayland、wayland-protocols 和 libdisplay-info，各自选用带有版本标签的最新发行版。

如需共享屏幕，还可以安装 `xdg-desktop-portal-wlr` 或 `xdg-desktop-portal-hyprland`：

```bash
sudo apt install -y xdg-desktop-portal-wlr
```

请参阅 [XDPH GitHub 仓库的 README](https://github.com/hyprwm/xdg-desktop-portal-hyprland)。
更多信息见 [XDPH](../hypr-ecosystem/user/xdg-desktop-portal-hyprland.md) 和 [Ubuntu 上安装和构建 Hyprland 的 Gist 指南](https://gist.github.com/Vertecedoc4545/3b077301299c20c5b9b4db00f4ca6000)。

> [!WARNING]
> Ubuntu 提供的依赖版本通常较旧，因此无法保证构建成功。
> 即使现在能成功构建，以后也很可能会失败。

> [!WARNING]
> 请始终使用最新版本的 Ubuntu，以获取最新的依赖。
>
> 注意：GDM 与 Hyprland 配合使用时存在一些问题，实际体验可能因环境而异。
> 更多信息见[入门教程](master-tutorial.md)。
>
> 如果遇到问题，请参阅上面的 Gist 指南。



</details>




**必须**按以下顺序构建：

```
lua
hyprland-protocols
hyprwayland-scanner
hyprutils
hyprgraphics
hyprlang
hyprcursor
aquamarine
xdg-desktop-portal-hyprland
hyprwire
hyprtoolkit
hyprland
```

构建好 Hyprland 后，hypr\* 系列的其他软件包（如 hyprlock、hyprsunset 等）可以按任意顺序构建。

<a id="building-with-cmake"></a>

#### 使用 CMake 构建

```sh
git clone --recursive https://github.com/hyprwm/Hyprland
cd Hyprland
make all && sudo make install
```

<a id="crash-on-launch"></a>

## 启动时崩溃

请参阅[崩溃与缺陷](../crashes-and-bugs/_index.md)。

<a id="custom-installation-debug-build-etc"></a>

## 自定义安装（调试构建等）

1. 用 `cd` 进入 Hyprland 仓库目录。
1. 如需构建调试版本：
   ```bash
   make debug
   sudo make install
   ```
1. 如需使用其他构建配置，请将 `<PRESET>` 替换为所选预设（`release` 或 `debug`）：
   ```bash
   make <PRESET> && sudo cp ./build/Hyprland /usr/bin && sudo cp ./example/hyprland.desktop /usr/share/wayland-sessions
   ```

<a id="custom-build-flags"></a>

## 自定义构建标志

要使用自定义构建标志，需要跳过 make，直接使用 CMake。

CMake 支持以下自定义构建标志：

```bash
NO_XWAYLAND - Removes Xwayland support
NO_SYSTEMD - Removes systemd dependencies
NO_UWSM - Does not install the hyprland-uwsm.desktop file
NO_HYPRPM - Does not build and install hyprpm
```

可以这样向 CMake 传递标志：

```bash
cmake --no-warn-unused-cli -DCMAKE_BUILD_TYPE:STRING=Release -D<FLAG>:STRING=true -B build
```

将 `<FLAG>` 替换为其中一个自定义构建标志。
要同时使用多个标志，可以继续添加 `-D<FLAG_2>:STRING=true`。

也可以将 `BUILD_TYPE` 改为 `Debug`。

运行以下命令进行构建：

```bash
cmake --build ./build --config Release --target all -j`nproc 2>/dev/null || getconf NPROCESSORS_CONF`
```

如果配置时选择了 `Debug`，也要将 `--config` 的值改为 `Debug`。

运行以下命令进行安装：

```bash
sudo cmake --install ./build
```

<a id="running-in-a-vm"></a>

## 在虚拟机中运行

_实际效果可能因环境而异，官方不支持这种运行方式。_

通读 [ArchWiki 的 libvirt 页面](https://wiki.archlinux.org/title/Libvirt)，安装并配置好 `libvirt`、`virsh` 和 `virt-viewer`。

```bash
# 安装 libvirt 和 qemu 相关软件包。
sudo pacman -S libvirt virt-viewer qemu-common
# 将自己的用户账户加入 libvirt 组。
sudo usermod -a -G libvirt USER # 将 'USER' 替换为你的用户名。
# 启用并启动 libvirtd。
systemctl enable --now libvirtd
```

前往 [GitLab 上的 arch-boxes 仓库](https://gitlab.archlinux.org/archlinux/arch-boxes/-/packages)，下载最新的 Arch QEMU 基础镜像。
也可以从任意 Arch 镜像站下载。

```bash
curl https://geo.mirror.pkgbuild.com/images/latest/Arch-Linux-x86_64-basic.qcow2 \
  -o ~/Downloads/arch-qemu.qcow2 # 也可以将其下载到任意位置。
```

使用 virsh 创建虚拟机。

```bash
# 使用 virt-install（随 libvirt 提供）从镜像安装虚拟机。
virt-install \
  --graphics spice,listen=none,gl.enable=yes,rendernode=/dev/dri/renderD128 \
  --name hypr-vm \
  --os-variant archlinux \
  --memory 2048 \
  --disk ~/Downloads/arch-qemu.qcow2 \
  --import
```

使用 `virt-viewer` 连接，它会在 TTY 上打开图形会话。
默认用户名和密码都是 `arch`。

> [!WARNING]
> 务必使用 `--attach` 标志，因为启用 virgl 后必须禁用监听。
> 因此，无法通过 TCP 或 UNIX 套接字直接连接到远程显示。
> `--attach` 会请求 libvirt 提供一个已连接到远程显示的套接字。\*

```sh
virt-viewer --attach hypr-vm
```

最后，在虚拟机内按照上文的说明[从 AUR 安装 hyprland-git](#installation) 或[手动构建](#manual-build)。

> [!WARNING]
> 务必安装 `mesa` 作为 OpenGL 驱动。
> `mesa` 包含 virgl 驱动。
