# 画面撕裂

允许画面撕裂可以减少游戏中的延迟、抖动，或同时减少两者。

<a id="enabling-tearing"></a>

## 启用画面撕裂

> [!WARNING]
> 如果你遇到画面异常，可能暂时没有解决办法。对画面撕裂的支持仍处于实验阶段。下文列出了一些可能的原因。

要启用画面撕裂，请按以下步骤操作：

- 将 `general.allow_tearing` 设为 `true`。这是画面撕裂的“总开关”。
- 为你选定的游戏添加 `immediate` 窗口规则效果。这样可以确保 Hyprland 对该游戏启用画面撕裂。

> [!NOTE]
> 只有当游戏处于全屏模式且屏幕上只显示游戏画面时，画面撕裂才会生效。有关详细信息，请查看 `hyprctl monitors` 输出中的 `tearingBlockedBy` 字段。

配置片段示例：

```lua
hl.config({
  general = {
    allow_tearing = true
  }
})

hl.window_rule({
  match = { class = "cs2" }, immediate = true
})
```

<a id="common-issues"></a>

## 常见问题

<a id="no-tearing-at-all"></a>

### 完全没有画面撕裂

请确认窗口规则能匹配游戏窗口，并且已开启总开关。

还要确保这台显示器上只显示游戏画面，没有通知、叠加层、锁屏界面、面板栏、其他窗口等。（这些元素显示在另一台显示器上没有问题。）

<a id="apps-that-should-tear-freeze"></a>

### 应启用画面撕裂的应用程序卡死

这几乎可以确定是因为你的 GPU 驱动不支持画面撕裂。

如果确认是这个原因，请_不要_提交问题报告。

<a id="graphical-artifacts-random-colorful-pixels-etc"></a>

### 显示异常（随机出现彩色像素等）

很可能是显卡驱动有问题。

如果确认是这个原因，请_不要_提交问题报告。遗憾的是，这种情况很可能是你的 GPU 驱动造成的。
