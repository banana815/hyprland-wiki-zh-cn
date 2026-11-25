# 虚拟 GPU

<a id="general"></a>

## 概述

如果你的 GPU 属于以下类别之一：
- Intel Arc Pro 显卡
- Intel 笔记本电脑集成显卡
- NVIDIA 工作站或服务器显卡
- NVIDIA RTX 2000 系列显卡
- AMD Radeon Instinct 显卡

那么你的显卡很可能支持通过中介设备或 SR-IOV 进行虚拟分区。启用虚拟分区的方法因厂商而异，差别很大，超出了本 Wiki 的讨论范围。

例如，启用虚拟分区后，RTX A5000 显卡会创建以下设备：

```console
# lspci -d 10de:
01:00.0 3D controller: NVIDIA Corporation GA102GL [RTX A5000] (rev a1)
01:00.4 3D controller: NVIDIA Corporation GA102GL [RTX A5000] (rev a1)
01:00.5 3D controller: NVIDIA Corporation GA102GL [RTX A5000] (rev a1)
01:00.6 3D controller: NVIDIA Corporation GA102GL [RTX A5000] (rev a1)
01:00.7 3D controller: NVIDIA Corporation GA102GL [RTX A5000] (rev a1)
01:01.0 3D controller: NVIDIA Corporation GA102GL [RTX A5000] (rev a1)
01:01.1 3D controller: NVIDIA Corporation GA102GL [RTX A5000] (rev a1)
01:01.2 3D controller: NVIDIA Corporation GA102GL [RTX A5000] (rev a1)
01:01.3 3D controller: NVIDIA Corporation GA102GL [RTX A5000] (rev a1)
01:01.4 3D controller: NVIDIA Corporation GA102GL [RTX A5000] (rev a1)
01:01.5 3D controller: NVIDIA Corporation GA102GL [RTX A5000] (rev a1)
01:01.6 3D controller: NVIDIA Corporation GA102GL [RTX A5000] (rev a1)
01:01.7 3D controller: NVIDIA Corporation GA102GL [RTX A5000] (rev a1)
01:02.0 3D controller: NVIDIA Corporation GA102GL [RTX A5000] (rev a1)
01:02.1 3D controller: NVIDIA Corporation GA102GL [RTX A5000] (rev a1)
01:02.2 3D controller: NVIDIA Corporation GA102GL [RTX A5000] (rev a1)
01:02.3 3D controller: NVIDIA Corporation GA102GL [RTX A5000] (rev a1)
01:02.4 3D controller: NVIDIA Corporation GA102GL [RTX A5000] (rev a1)
01:02.5 3D controller: NVIDIA Corporation GA102GL [RTX A5000] (rev a1)
01:02.6 3D controller: NVIDIA Corporation GA102GL [RTX A5000] (rev a1)
01:02.7 3D controller: NVIDIA Corporation GA102GL [RTX A5000] (rev a1)
01:03.0 3D controller: NVIDIA Corporation GA102GL [RTX A5000] (rev a1)
01:03.1 3D controller: NVIDIA Corporation GA102GL [RTX A5000] (rev a1)
01:03.2 3D controller: NVIDIA Corporation GA102GL [RTX A5000] (rev a1)
01:03.3 3D controller: NVIDIA Corporation GA102GL [RTX A5000] (rev a1)
```

如果想在虚拟机中使用硬件加速运行 Hyprland，可以将其中一个虚拟 GPU 分区（也称为 vGPU）直通给虚拟机。

> [!NOTE]
> 以下步骤**不适用于 Virtio-GPU 等半虚拟化驱动程序**。
>
> Virtio-GPU 是完全由软件模拟的设备，会将图形处理工作转交给宿主机的 GPU。它不需要从物理 GPU 划出分区。Virtio-GPU 专为这种场景设计，自带模拟显示输出，因此你可以直接使用它正常运行 Hyprland。

<a id="running-hyprland-on-vgpu"></a>

## 在 vGPU 上运行 Hyprland

默认情况下，Hyprland 要求显卡**至少有一个显示输出**。

不过，各厂商的 vGPU 都是仅用于渲染的显卡，在 Linux 上没有模拟的显示输出。这是因为它们面向虚拟桌面基础设施（VDI）、3D 渲染、编码和计算等远程使用场景。从设备描述的前缀也能看出这一点：vGPU 的前缀是“3D controller”（3D 控制器），而不是“VGA compatible controller”（VGA 兼容控制器）。

**要让 Hyprland** 在**没有显示输出的显卡上运行，必须在启动 Hyprland 时启用** `AQ_NO_KMS_REQUIREMENT` 环境标志：

```lua
hl.env("AQ_NO_KMS_REQUIREMENT", "1")
```

<a id="usage-of-both-a-gpu-and-vgpu"></a>

### 同时使用 GPU 和 vGPU

> [!WARNING]
> 本节适用于在 QEMU 虚拟机中同时使用直通 vGPU 和 Virtio-GPU 设备的用户。

大多数硬件驱动程序和半虚拟化驱动程序都会在 `/dev/dri` 目录下为同一张显卡提供两个设备节点。一个节点可供所有用户访问，提供渲染功能；另一个节点需要特权才能访问，提供一个或多个显示输出。

```console
$ ls -lh /dev/dri/
total 0
drwxr-xr-x  2 root root         80 Apr 20 07:01 by-path/
crw-rw----+ 1 root video  226,   1 Apr 20 07:01 card1           # 带有显示输出的 KMS 显卡
crw-rw-rw-  1 root render 226, 128 Apr 20 07:01 renderD128      # 仅用于渲染的 DRM 显卡
```

默认情况下，Hyprland 只会选择系统中具有显示输出的节点，忽略 `render` 节点。启用 `AQ_NO_KMS_REQUIREMENT` 解除这一限制后，`render` 节点也可以被选中。

如果在同一台虚拟机中同时使用虚拟 GPU 和硬件 GPU，**必须设置 `AQ_DRM_DEVICES` 标志**。有关此标志的详细说明，请参阅[多 GPU](multi-gpu.md)：

```lua
hl.env("AQ_NO_KMS_REQUIREMENT", "1")
hl.env("AQ_DRM_DEVICES", "/dev/dri/card0:/dev/dri/card1")
```

实际使用中，虚拟机选择设备节点作为主渲染器的顺序并不固定，因此务必手动指定优先级。

> [!WARNING]
> 某些虚拟机监控程序提供的 PCI 拓扑在每次启动时可能会被解析为不同的设备顺序。为确保选中正确的节点，请参阅[多 GPU 文档中关于为特定显卡创建固定设备路径的章节](multi-gpu.md#creating-consistent-device-paths-for-specific-cards)，了解如何重命名节点，使配置在重启后保持一致。

<a id="accessing-the-virtual-display"></a>

## 访问虚拟显示器

如果启动 Hyprland 时没有任何显示输出，它会初始化一个名为 `HEADLESS-0` 的无头输出，其分辨率和帧率为 `1920x1080@60Hz`。你可以在平时使用的 `hyprland.lua` 配置文件中调整这些参数。

要访问该显示器并与 Hyprland 交互，必须使用支持 wlroots 屏幕捕获协议的远程桌面服务器。

已知支持以下服务器：
- [Sunshine/Moonlight](https://app.lizardbyte.dev/Sunshine/)
- [Apollo/Artemis(Moonlight Noir)](https://github.com/ClassicOldSong/Apollo)
- [Wayvnc](https://github.com/any1/wayvnc)

启动 Hyprland 后，即可在客户机上使用 `hyprctl` 远程启动服务器（参见[使用 hyprctl](../core/advanced-configuration/using-hyprctl.md)）。

```bash
hyprctl --instance 0 eval 'hl.exec_cmd("Sunshine")'
```

远程显示服务器应作为 Hyprland 的子进程或后代进程运行，以继承其所有环境变量，否则服务器将找不到无头显示器。

如果一切配置妥当且运行正常，可以在 `hyprland.lua` 文件中将服务器设为自动启动（参见[自动启动](../core/autostart.md)）。例如：

```lua
hl.on("hyprland.start", function()
    hl.exec_cmd("Sunshine")
end)
```

恭喜你拥有了自己的 Hyprland 虚拟桌面！
