# 单窗口布局

在 Monocle 布局中，每个窗口始终占满工作区内除预留区域以外的全部空间。

<video width="1024" height="566" autoplay muted loop>
  <source src="https://dl.hypr.land/wiki/demo_monocle.mp4" type="video/mp4">
</video>

<a id="quirks"></a>

## 兼容性调整

受布局工作方式的限制，`hl.dsp.window.cycle_next()` 在 Monocle 布局中不起作用。要循环切换此布局中的窗口，请使用 `hl.dsp.layout("cyclenext")` 或 `hl.dsp.window.cycle_next({ tiled = true })`。

<a id="layout-messages"></a>

## 布局消息

调度器 `hl.dsp.layout()` 的参数：

| 名称 | 说明 | 参数 |
| --- | --- | --- |
| cyclenext | 循环切换到下一个窗口 | 无 |
| cycleprev | 循环切换到上一个窗口 | 无 |
