# IPC

Hyprland 提供两个 UNIX 套接字，可通过代码或 shell 工具控制 Hyprland 或获取其信息。

<a id="hyprland-instance-signature-his"></a>

## Hyprland 实例签名（HIS）

```sh
echo $HYPRLAND_INSTANCE_SIGNATURE
```

<a id="xdg_runtime_dirhyprhissocketsock"></a>

## `$XDG_RUNTIME_DIR/hypr/[HIS]/.socket.sock`

用于处理类似 hyprctl 的请求。
可用命令见 [Hyprctl 页面](../configuring/core/advanced-configuration/using-hyprctl.md)。

请求的基本写法是向套接字写入 `[flags]/command args`。

> [!NOTE]
> Hyprland 完全以同步方式处理此套接字上的连接。因此，任何未关闭的连接*都会导致 Hyprland 卡住*，直到 5 秒后超时。
> 每次都应在即将写入请求时才打开套接字，写完后就将其关闭。

<a id="xdg_runtime_dirhyprhissocket2sock"></a>

## `$XDG_RUNTIME_DIR/hypr/[HIS]/.socket2.sock`

用于接收事件。
Hyprland 会按以下格式向每个已连接的客户端实时发送事件：

`EVENT>>DATA\n`（`\n` 表示换行符）

例如：`workspace>>2`

<a id="events-list"></a>

## 事件列表

| 名称 | 说明 | 数据 |
| --- | --- | --- |
| workspace | 工作区切换时触发。仅在用户请求切换工作区时触发，移动鼠标不会触发（见 `focusedmon`）。 | `WORKSPACEADDRESS` |
| workspacev2 | 工作区切换时触发。仅在用户请求切换工作区时触发，移动鼠标不会触发（见 `focusedmon`）。 | `WORKSPACEADDRESS,WORKSPACENAME` |
| focusedmon | 活动显示器变更时触发。 | `MONNAME,WORKSPACEADDRESS` |
| focusedmonv2 | 活动显示器变更时触发。 | `MONNAME,WORKSPACEADDRESS` |
| activewindow | 活动窗口变更时触发。 | `WINDOWCLASS,WINDOWTITLE` |
| activewindowv2 | 活动窗口变更时触发。 | `WINDOWADDRESS` |
| fullscreen | 窗口的全屏状态改变时触发。 | `0/1`（退出全屏/进入全屏） |
| monitorremoved | 移除显示器（断开连接）时触发。 | `MONITORNAME` |
| monitorremovedv2 | 移除显示器（断开连接）时触发。 | `MONITORID,MONITORNAME,MONITORDESCRIPTION` |
| monitoradded | 添加显示器（建立连接）时触发。 | `MONITORNAME` |
| monitoraddedv2 | 添加显示器（建立连接）时触发。 | `MONITORID,MONITORNAME,MONITORDESCRIPTION` |
| createworkspace | 创建工作区时触发。 | `WORKSPACEADDRESS` |
| createworkspacev2 | 创建工作区时触发。 | `WORKSPACEADDRESS,WORKSPACENAME` |
| destroyworkspace | 销毁工作区时触发。 | `WORKSPACEADDRESS` |
| destroyworkspacev2 | 销毁工作区时触发。 | `WORKSPACEADDRESS,WORKSPACENAME` |
| moveworkspace | 将工作区移至另一台显示器时触发。 | `WORKSPACEADDRESS,MONNAME` |
| moveworkspacev2 | 将工作区移至另一台显示器时触发。 | `WORKSPACEADDRESS,WORKSPACENAME,MONNAME` |
| renameworkspace | 重命名工作区时触发。 | `WORKSPACEADDRESS,NEWNAME` |
| activespecial | 显示器上打开的特殊工作区发生变化时触发（关闭时 `WORKSPACEADDRESS` 为空）。 | `WORKSPACEADDRESS,MONNAME` |
| activespecialv2 | 显示器上打开的特殊工作区发生变化时触发（关闭时 `WORKSPACEADDRESS` 和 `WORKSPACENAME` 均为空）。 | `WORKSPACEADDRESS,WORKSPACENAME,MONNAME` |
| activelayout | 当前活动键盘的布局改变时触发。 | `KEYBOARDNAME,LAYOUTNAME` |
| openwindow | 打开窗口时触发。 | `WINDOWADDRESS,WORKSPACEADDRESS,WINDOWCLASS,WINDOWTITLE` |
| closewindow | 关闭窗口时触发。 | `WINDOWADDRESS` |
| kill | 通过 `hyprctl kill` 强制终止窗口时触发。 | `WINDOWADDRESS` |
| movewindow | 将窗口移至某个工作区时触发。 | `WINDOWADDRESS`,`WORKSPACEADDRESS` |
| movewindowv2 | 将窗口移至某个工作区时触发。 | `WINDOWADDRESS`,`WORKSPACEADDRESS`,`WORKSPACENAME` |
| openlayer | 映射 layerSurface 时触发。 | `NAMESPACE` |
| closelayer | 取消映射 layerSurface 时触发。 | `NAMESPACE` |
| submap | 键位绑定子映射改变时触发。空值表示默认映射。 |`SUBMAPNAME` |
| changefloatingmode | 窗口的浮动模式改变时触发。`FLOATING` 的值为 0 或 1。 | `WINDOWADDRESS`,`FLOATING` |
| urgent | 窗口请求进入 `urgent` 状态时触发。 | `WINDOWADDRESS` |
| screencast | 客户端的屏幕捕获状态改变时触发。可能同时存在多个独立客户端。状态值为 0 或 1，owner 的取值为 monitor（显示器）、window（窗口）或 region（区域）。 | `STATE,OWNER` |
| screencastv2 | 客户端的屏幕捕获状态改变时触发。可能同时存在多个独立客户端。状态值为 0 或 1，owner 的取值为 monitor（显示器）、window（窗口）或 region（区域），name 是共享目标的标识（显示器名称或窗口标题）。 | `STATE,OWNER,NAME` |
| windowtitle | 窗口标题改变时触发。 | `WINDOWADDRESS` |
| windowtitlev2 | 窗口标题改变时触发。 | `WINDOWADDRESS,WINDOWTITLE` |
| togglegroup | 使用 `togglegroup` 命令时触发。返回 `state,handle`，其中 `state` 表示切换后的状态，`handle` 是一个或多个以逗号分隔的窗口地址（例如，在 `0,64cea2525760,64cea2522380` 中，`0` 表示窗口组已解散，其余值是原组成员的窗口地址）。 | `0/1,WINDOWADDRESS(ES)` |
| moveintogroup | 窗口并入组时触发，返回该窗口的地址。 | `WINDOWADDRESS` |
| moveoutofgroup | 窗口移出组时触发，返回该窗口的地址。 | `WINDOWADDRESS` |
| ignoregrouplock | 切换 `ignoregrouplock` 时触发。 | `0/1` |
| lockgroups | 切换 `lockgroups` 时触发。 | `0/1` |
| configreloaded | 配置重新加载完毕时触发。 | [[Empty]] |
| pin | 固定窗口或取消固定时触发。 | `WINDOWADDRESS,PINSTATE` |
| minimized | 任务栏一类的外部应用请求最小化窗口时触发。 | `WINDOWADDRESS,0/1` |
| bell | 应用通过 `xdg-system-bell-v1` 请求响起系统铃声时触发。窗口地址参数可能为空。 | `WINDOWADDRESS` |

> [!WARNING]
> 进入和退出全屏的事件不一定会交替出现、每次各触发一次。
> 有些窗口可能多次请求进入全屏，从而触发多个全屏事件。

<a id="how-to-use-socket2-with-bash"></a>

## 如何在 bash 中使用 socket2

以下示例脚本使用 bash 和 `socat` 处理 socket2 事件：

```sh
#!/bin/sh

handle() {
  case $1 in
    monitoradded*) do_something ;;
    focusedmon*) do_something_else ;;
  esac
}

socat -U - UNIX-CONNECT:$XDG_RUNTIME_DIR/hypr/$HYPRLAND_INSTANCE_SIGNATURE/.socket2.sock | while read -r line; do handle "$line"; done
```
