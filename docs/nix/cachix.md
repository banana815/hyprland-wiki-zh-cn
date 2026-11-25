# Cachix

> [!WARNING]
> 除非清楚这样做的后果，否则**不要**覆盖 Hyprland 的 `nixpkgs` 输入。
> 这样做会使构建使用另一个 Nixpkgs 提交，导致缓存无法使用。

> [!NOTE]
> 本页仅适用于 flake 提供的软件包。
> 如果使用 Nixpkgs 提供的软件包，可以直接跳过本页。

Hydra 不构建 Hyprland flake，因此它不像 Nixpkgs 中的其他软件包那样缓存在 [cache.nixos.org] 中。

为了让你无需自行构建 Hyprland 及其依赖（可能包括 `mesa`、`ffmpeg` 等），我们提供了一个 Cachix 缓存，你可以将其添加到 Nix 配置中。

[Hyprland Cachix](https://app.cachix.org/cache/hyprland) 用于缓存 `hyprland` 软件包，以及 [cache.nixos.org] 中没有的依赖。

> [!WARNING]
> 要让 Nix 使用这个缓存，必须在使用 Hyprland flake 软件包**之前**启用缓存。

```nix {filename="configuration.nix"}
{
  nix.settings = {
    substituters = ["https://hyprland.cachix.org"];
    trusted-substituters = ["https://hyprland.cachix.org"];
    trusted-public-keys = ["hyprland.cachix.org-1:a7pgxzMz7+chwVL3/pzj6jIBMioiJM7ypFP8PwtkuGc="];
    # 必须这样设置，非 root 用户才能使用上述替代源和密钥。
    # 使用 @wheel 指定所有 sudo 用户，也可以显式列出你的用户名。
    trusted-users = ["root" "@wheel"];
  };
}
```

> [!NOTE]
> 如果看到 `ignoring the client-specified setting 'trusted-public-keys', because it is a restricted setting and you are not a trusted user`，说明你的用户不在 `trusted-users` 中。
> 请按上例将该用户加入 `trusted-users`，然后重新构建。

[cache.nixos.org]: https://cache.nixos.org
