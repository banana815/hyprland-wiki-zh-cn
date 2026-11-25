# hypridle

[hypridle](https://github.com/hyprwm/hypridle) 是 Hyprland 的空闲管理守护进程。

<a id="configuration"></a>

## 配置

配置文件位于 `~/.config/hypr/hypridle.conf`。
此文件必不可少，没有它 hypridle 就无法运行。

要让 hypridle 随 Hyprland 启动，请将 `hypridle` 加入 Hyprland 配置的自启动命令中。



<a id="general"></a>

### 常规设置

`general` 类别中的变量：

| 变量 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| `lock_cmd` | 收到 D-Bus 锁定事件（例如由 `loginctl lock-session` 触发）时运行的命令 | string | [[Empty]] |
| `unlock_cmd` | 收到 D-Bus 解锁事件（例如由 `loginctl unlock-session` 触发）时运行的命令 | string | [[Empty]] |
| `on_lock_cmd` | 锁屏程序锁定会话时运行的命令 | string | [[Empty]] |
| `on_unlock_cmd` | 锁屏程序解锁会话时运行的命令 | string | [[Empty]] |
| `before_sleep_cmd` | 收到 D-Bus 的 prepare_sleep 事件时运行的命令 | string | [[Empty]] |
| `after_sleep_cmd` | 系统唤醒后收到 D-Bus 的 post prepare_sleep 事件时运行的命令 | string | [[Empty]] |
| `ignore_dbus_inhibit` | 是否忽略 D-Bus 空闲抑制事件（例如来自 Firefox 的事件） | bool | `false` |
| `ignore_systemd_inhibit` | 是否忽略 `systemd-inhibit --what=idle` 设置的空闲抑制锁 | bool | `false` |
| `ignore_wayland_inhibit` | 是否忽略通过 Wayland 协议设置的空闲抑制锁 | bool | `false` |
| `inhibit_sleep` | 睡眠抑制模式：<br> `0`：禁用 <br> `1`：常规 <br> `2`：自动 <br> `3`：等待锁定通知 | int | `2` |

> [!NOTE]
> `general:inhibit_sleep` 选项可确保 hypridle 在系统进入睡眠前执行指定任务。
>
> 可选值：
> - `0` 禁用睡眠抑制。
> - `1` 让系统等到 hypridle 启动 `general:before_sleep_cmd` 后再进入睡眠。
> - `2`（自动）会根据配置判断你是否希望在睡眠前启动 hyprlock，据此选择 `3` 或 `1`。
> - `3` 让系统等到锁屏程序锁定会话后再进入睡眠。
>   此模式适用于所有使用 Wayland 会话锁定协议的程序。

<a id="listeners"></a>

### 监听器

hypridle 通过监听器定义用户空闲时要执行的操作。

每个监听器都有一个 `timeout`，单位为秒。
用户持续空闲 `timeout` 秒后，就会触发 `on-timeout`。
用户在空闲后恢复活动时，就会触发 `on-resume`。

你可以按需定义任意数量的监听器。


<details><summary>监听器示例</summary>

```ini
listener {
    timeout = 500                            # 单位为秒。
    on-timeout = notify-send "You are idle!" # 超时后运行的命令。
    on-resume = notify-send "Welcome back!"  # 超时触发后，再次检测到活动时运行的命令。
}
```


</details>

`listener` 类别中的变量：

| 变量 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| `timeout` | 空闲时长，单位为秒 | int | 无，必须指定 |
| `on-timeout` | 达到超时时长时运行的命令 | string | [[Empty]] |
| `on-resume` | 超时触发后，再次检测到用户活动时运行的命令 | string | [[Empty]] |
| `ignore_inhibit` | 让此规则忽略所有类型的空闲抑制锁 | bool | `false` |
| `condition_cmd` | 达到超时时长时，在 `on-timeout` _之前_运行的命令。通过 `/bin/sh -c` 执行；退出码为 `0` 时触发 `on-timeout`，非零时推迟触发 | string | [[Empty]] |
| `condition_retry` | 若 `condition_cmd` 推迟了触发，只要用户仍处于空闲状态，就每隔 N 秒重新运行该命令，一旦成功便触发 `on-timeout`。设为 `0` 可禁用重试（本次空闲期间将跳过被推迟的 `on-timeout`） | int | `0` |

<a id="conditional-timeouts"></a>

#### 条件超时

监听器可以通过 `condition_cmd` 根据外部状态决定是否触发 `on-timeout`。
达到超时时长时，hypridle 会先运行 `condition_cmd`。只有该命令以 `0` 退出时，才会触发 `on-timeout`。
退出码非零时，`on-timeout` 将推迟触发。

设置 `condition_retry` 可让 hypridle 在用户持续空闲时反复检查：每隔 `condition_retry` 秒重新运行一次 `condition_cmd`，一旦成功便立即触发 `on-timeout`。
使用默认设置 `condition_retry = 0` 时，如果 `on-timeout` 被推迟，本次空闲期间就会跳过它，直到下次空闲时才重新计时。
任何用户活动都会重置监听器，并取消尚未执行的重试。

> [!NOTE]
> `condition_cmd` 在 hypridle 的事件循环中同步运行，应确保它能快速执行完毕。脚本一旦阻塞，空闲事件的处理也会停下来。
> hypridle 大约每 5 秒在事件循环中检查一次是否该重试，因此即使 `condition_retry` 设得很小，实际重试间隔也会向上取整到这一时间粒度。


<details><summary>示例</summary>


SSH 会话保持连接时不挂起系统：

```ini
listener {
    timeout = 900                                          # 15min.
    on-timeout = systemctl suspend                         # 挂起计算机。
    condition_cmd = ~/.config/hypr/scripts/can-suspend.sh  # 退出状态码为 0 时挂起，非零时保持唤醒。
    condition_retry = 30                                   # 如果仍处于空闲状态，每 30 秒重新检查一次。
}
```

```sh { filename="~/.config/hypr/scripts/can-suspend.sh" }
#!/bin/sh
ss -tn state established '( sport = :ssh )' | grep -q . && exit 1
exit 0
```

hypridle 配合 hyprlock 使用的完整示例：

```ini { filename="~/.config/hypr/hypridle.conf" }
general {
    lock_cmd = pidof hyprlock || hyprlock                                    # 避免启动多个 hyprlock 实例。
    before_sleep_cmd = loginctl lock-session                                 # 在挂起前锁屏。
    after_sleep_cmd = hyprctl dispatch 'hl.dsp.dpms({ action = "enable" })'  # 以免需要按两次键才能点亮显示器。
}

listener {
    timeout = 150                         # 2.5min.
    on-timeout = brightnessctl -s set 10  # 将显示器背光调至最低；OLED 显示器应避免设为 0。
    on-resume = brightnessctl -r          # 恢复显示器背光亮度。
}

# 关闭键盘背光。如果键盘没有背光，请注释掉此配置段。
listener {
    timeout = 150                                           # 2.5min.
    on-timeout = brightnessctl -sd rgb:kbd_backlight set 0  # 关闭键盘背光。
    on-resume = brightnessctl -rd rgb:kbd_backlight         # 开启键盘背光。
}

listener {
    timeout = 300                       # 5min
    on-timeout = loginctl lock-session  # 超时后锁屏
}

listener {
    timeout = 330                                                                          # 5.5min
    on-timeout = hyprctl dispatch 'hl.dsp.dpms({ action = "disable" })'                    # 超时后关闭屏幕
    on-resume = hyprctl dispatch 'hl.dsp.dpms({ action = "enable" })' && brightnessctl -r  # 超时触发后，再次检测到活动时点亮屏幕。
}

listener {
    timeout = 1800                  # 30min
    on-timeout = systemctl suspend  # 挂起计算机
}
```

<a id="fading-the-keyboard-backlight"></a>

#### 让键盘背光渐亮渐暗

`brightnessctl` 会立即设置亮度，因此仅用一对 `on-timeout`/`on-resume` 命令会让键盘背光骤然熄灭或亮起。
[hypr-kbd-backlight-fade](https://github.com/queueingqt/hypr-kbd-backlight-fade) 是一个小脚本，它通过逐级调整亮度，让背光快速渐亮、缓慢渐暗。
它还使用锁文件，避免渐亮和渐暗操作重叠时发生竞争（例如用户短暂触碰后很快又进入空闲状态时）。

请注意，视频播放器和浏览器通常会在播放视频时持有 Wayland 空闲抑制锁，即使没有全屏播放也是如此。这会暂停**所有**监听器，包括锁屏和挂起以外的监听器。
如果希望键盘背光在播放视频时仍能响应实际输入，请只在键盘背光监听器中设置 `ignore_inhibit = true`。启用 `general:ignore_wayland_inhibit` 会让所有监听器都忽略 Wayland 空闲抑制锁。



</details>

<a id="locking-on-suspend-and-hibernate"></a>

## 在挂起和休眠时锁定会话

会话在进入睡眠*之前*就会锁定，而非等到唤醒之后。
无论以何种方式进入睡眠，logind 都会发出 `PrepareForSleep` 信号：运行 `systemctl suspend`、`systemctl hibernate` 或 `systemctl suspend-then-hibernate`，由监听器执行 `on-timeout = systemctl suspend`，或合上笔记本电脑盖并由 logind 的 `HandleLidSwitch` 处理。
因此，上述情况都会触发 `general:before_sleep_cmd`，即使睡眠并非由 hypridle 自身发起。

```ini { filename="~/.config/hypr/hypridle.conf" }
general {
    lock_cmd = pidof hyprlock || hyprlock     # 会话收到锁定请求时运行。
    before_sleep_cmd = loginctl lock-session  # 进入睡眠前请求锁屏。
}
```

`before_sleep_cmd` 本身不会启动锁屏程序。
`loginctl lock-session` 只会让 logind 为当前会话发出 `Lock` 信号。hypridle 收到信号后会运行 `general:lock_cmd`。
将这两步分开，只需在一处指定锁屏程序。手动执行 `loginctl lock-session`（例如通过键位绑定）时，也会走与进入睡眠时相同的锁屏流程。

合盖事件由 logind 处理，不归 Hyprland 管理。请参阅[关于 `HandleLidSwitch` 的警告](../../configuring/core/binds/switches.md)。
合盖时锁屏无需额外配置键位绑定，因为合盖进入睡眠时 logind 同样会发出 `PrepareForSleep` 信号。

hypridle 只执行你指定的命令，挂起或休眠由该命令决定。
`systemctl hibernate` 需要可用的休眠恢复设备。`systemctl suspend-then-hibernate` 会先挂起系统，等到 `HibernateDelaySec` 指定的时间后再进入休眠。该选项在 `/etc/systemd/sleep.conf.d/` 中设置。

<a id="waiting-for-the-lock-to-be-drawn"></a>

### 等待锁屏界面绘制完成

`loginctl lock-session` 在信号发出后便立即返回，此时距离锁屏程序绘制出画面还有一段时间。
如果没有睡眠抑制锁，系统可能在这段间隙冻结。这样一来，唤醒时首先显示的是未锁定的桌面，直到锁屏界面绘制出来并将其覆盖。

[`general:inhibit_sleep`](#general) 用于解决这个问题：hypridle 向 logind 获取一把 `delay` 类型的睡眠抑制锁，并在睡眠前的处理完成后释放它。
不同模式对“完成”的判定不同：

- `1` 在 `before_sleep_cmd` 进程*刚启动*时就释放抑制锁。对于 `loginctl lock-session`，这不足以确保锁屏完成。
- `3` 只有在通过 `hyprland-lock-notify-v1` 协议收到会话已锁定的通知后，才释放抑制锁。
- `2`（默认值）仅在识别出 hyprlock 时选择 `3`。识别条件是 `before_sleep_cmd` 包含 `hyprlock`，或者 `lock_cmd` 包含 `hyprlock` 且 `before_sleep_cmd` 包含 `lock-session`。
  其他情况均回退到 `1`。

如果使用其他锁屏程序，请显式设置 `inhibit_sleep = 3`。
建议优先采用这种方式，而不是在 `before_sleep_cmd` 中用 `sleep` 延时：休眠抑制器会等待实际的锁屏事件，无需猜测要等多久。
启动时会输出所选模式，消息为 `Sleep inhibition enabled - inhibiting until the wayland session gets locked`。

> [!NOTE]
> 锁屏界面一旦显示，会话就视为已锁定，此时锁屏程序的淡入动画可能还未结束。
> 如果从休眠中恢复时仍能透过半透明的锁屏界面看到背后的内容，请同时禁用淡入动画（[hypridle#146](https://github.com/hyprwm/hypridle/issues/146)）。
> 如果使用 hyprlock，可以用 `hyprlock --no-fade-in` 启动，也可以完全关闭它的[动画](hyprlock.md#animations)。
