# 性能

如果你遇到性能问题，或者不在意动画效果，可以参考本页列出的已知性能优化技巧和问题解决方法。

<a id="fractional-scaling"></a>

## 分数缩放

Wayland 的分数缩放比以前好了很多，但仍不完善。有些应用程序尚不支持分数缩放，或者最多只提供实验性支持。如果显卡占用率很高，或者 Hyprland 用起来有卡顿感，可以尝试将缩放倍数设为 `1` 或 `2` 等整数，例如使用 `hl.monitor({ output = "", mode = "preferred", position = "auto", scale = 2 })`。

<a id="low-fpsstutterfps-drops-on-intel-igpu-with-tlp-mainly-laptops"></a>

## 使用 TLP 时 Intel 集成 GPU 帧率低、出现卡顿或掉帧（主要出现在笔记本电脑上）

TLP 的默认设置较为激进。在 `/etc/tlp.conf` 中，将 `INTEL_GPU_MIN_FREQ_ON_AC` 和 `INTEL_GPU_MIN_FREQ_ON_BAT` 中的一项或两项略微调高（例如从 300 调至 500），就能显著减少卡顿，理想情况下甚至可以完全消除卡顿。

<a id="how-do-i-make-hyprland-draw-as-little-power-as-possible-on-my-laptop"></a>

## 如何尽可能降低 Hyprland 在笔记本电脑上的耗电量？

使用 `hl.config({ ["decoration.blur.enabled"] = false })`  来禁用华丽但耗电的特效。



<a id="my-games-work-poorly-especially-proton-ones"></a>

## 我的游戏运行不流畅，尤其是通过 Proton 运行的游戏

使用 `gamescope` 通常可以解决 Wayland/Hyprland 相关的各种游戏问题。
