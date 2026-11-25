# 多显卡

<a id="general"></a>

## 概述

如果你的主机配有多个 GPU，你可能希望用一个 GPU 渲染 Hyprland 的所有元素，包括窗口和动画等，再用另一个 GPU 为特定应用程序提供硬件加速等。

这种配置在游戏笔记本电脑、支持 GPU 直通（无需 VFIO）的主机以及其他配有多个 GPU 的系统上都很常见。

<a id="detecting-gpus"></a>

## 检测 GPU

这里以作者自己的笔记本电脑为例。

运行 `lspci -d ::03xx` 可列出所有可用的 PCI 显示控制器：

```plain
01:00.0 VGA compatible controller: NVIDIA Corporation TU117M [GeForce GTX 1650 Mobile / Max-Q] (rev a1)
06:00.0 VGA compatible controller: Advanced Micro Devices, Inc. [AMD/ATI] Cezanne [Radeon Vega Series / Radeon Vega Mobile Series] (rev c6)
```

从这里可以清楚地看到，有两个可用的 GPU：独立的 NVIDIA GTX 1650 Mobile 和集成的 AMD Cezanne Radeon Vega Series GPU。

接下来，运行 `ls -l /dev/dri/by-path`。

```plain
 total 0
lrwxrwxrwx 1 root root  8 Jul 14 15:45 pci-0000:01:00.0-card -> ../card0
lrwxrwxrwx 1 root root 13 Jul 14 15:45 pci-0000:01:00.0-render -> ../renderD128
lrwxrwxrwx 1 root root  8 Jul 14 15:45 pci-0000:06:00.0-card -> ../card1
lrwxrwxrwx 1 root root 13 Jul 14 15:45 pci-0000:06:00.0-render -> ../renderD129
```

从以上输出可以看出，AMD 显卡的路径是 `pci-0000:06:00.0-card`，因为其中的 `06:00.0` 与第一条命令的输出相符。不要使用这里显示的 `card1` 符号链接。它在启动时动态分配，经常会变，不适合作为选择 GPU 的标识。

<a id="telling-hyprland-which-gpu-to-use"></a>

## 指定 Hyprland 使用的 GPU

确定每个“card”对应哪个 GPU 后，就可以通过设置 `AQ_DRM_DEVICES` 环境变量来指定 Hyprland 使用哪些 GPU。

> [!NOTE]
> 对于笔记本电脑，通常建议使用集成 GPU 作为主渲染器，这样可以延长电池续航时间，而且在现代系统上，大多数情况下与使用独立 GPU 几乎感觉不到差别。Hyprland 完全可以在集成 GPU 上流畅运行。同样的原则也适用于同时配有低功耗和高功耗 GPU 的台式机。

如果你想使用另一个 GPU，或者默认选错了 GPU，请将 `AQ_DRM_DEVICES` 设为用 `:` 分隔的显卡设备路径列表，例如：

```lua
hl.env("AQ_DRM_DEVICES", "/dev/dri/card0:/dev/dri/card1")
```

这里按优先级列出了 Hyprland 可以使用的 GPU。例如，`card0` 会作为主渲染器，如果它因任何原因不可用，就由 `card1` 作为主渲染器。

请注意，如果外接显示器连接到某块显卡，例如 `card1`，则必须在 `AQ_DRM_DEVICES` 中列出该显卡，显示器才能工作，但该显卡不必是主渲染器。

现在，你应该可以使用集成 GPU 处理运行 Hyprland 等较轻的图形负载，也可以按自己的偏好默认使用独立 GPU。

<a id="creating-consistent-device-paths-for-specific-cards"></a>

## 为特定显卡创建稳定的设备路径

如上所述，不建议使用 `/dev/dri/card*` 设备路径，因为这些符号链接指向的设备会时有变化。此外，实际显卡设备路径中含有冒号，无法直接用在 `AQ_DRM_DEVICES` 环境变量中，因为冒号 `:` 用于分隔多个路径。

你可以使用 udev 规则为特定显卡设备创建稳定的符号链接。例如，要在 `/dev/dri/amd-igpu` 创建一个指向 AMD 显卡的符号链接，可以运行以下命令，在 `/etc/udev/rules.d/amd-igpu-dev-path.rules` 创建一条 udev 规则：

```sh
SYMLINK_NAME="amd-igpu"
RULE_PATH="/etc/udev/rules.d/amd-igpu-dev-path.rules"
AMD_IGPU_ID=$(lspci -d ::03xx | grep 'AMD' | cut -f1 -d' ')

cat <<EOF | sudo tee "$RULE_PATH"
KERNEL=="card*", \
KERNELS=="0000:$AMD_IGPU_ID", \
SUBSYSTEM=="drm", \
SUBSYSTEMS=="pci", \
SYMLINK+="dri/$SYMLINK_NAME"
EOF
```

然后，使用以下命令重新加载 udev 规则：

```sh
sudo udevadm control --reload
sudo udevadm trigger
```

现在，`/dev/dri/amd-igpu` 处应该有一个符号链接，指向对应的显卡设备文件：
```console
$ ls -l /dev/dri/amd-igpu
lrwxrwxrwx 1 root root 5 /dev/dri/amd-igpu -> card1
```

如果显卡设备文件发生变化，此符号链接会自动更新，指向正确的文件。

现在可以在 `AQ_DRM_DEVICES` 环境变量中使用新的符号链接：

```lua
hl.env("AQ_DRM_DEVICES", "/dev/dri/amd-igpu")
```
