# 测试

Hyprland 和 hypr\* 旗下的部分其他项目都设有_测试_，以便在代码合并前发现缺陷和回归问题。

使用 Debug 配置构建时，默认也会构建测试。

<a id="running-tests"></a>

## 运行测试

Hyprland 的 Makefile 提供了 `test` 目标，运行以下命令即可执行整套测试：

```sh
make test
```

也可以分别运行单元测试和集成测试，详见本节后续内容。

<a id="gtests"></a>

### GTests

GTests 是使用 GoogleTest 编写的_单元测试_。
这些测试用于检查各个组件独立运行时的行为。

对于 Hyprland，运行：

```sh
make gtest
```

在其他项目中，手动调用 ctest：

```sh
ctest -j$(nproc) -C Debug --test-dir=build
```

请确认你的测试均已通过。

<a id="hyprlands-hyprtester"></a>

### Hyprland 的 hyprtester

Hyprland 的许多代码无法通过单元测试来验证，因此我们开发了 Hyprtester。这个可执行程序会启动 Hyprland，向它发送命令，并检查结果是否符合预期。

<a id="run-all-tests"></a>

#### 运行全部测试

要运行 Hyprtester，请在调试构建中执行以下命令：

```sh
./build/hyprtester/hyprtester -c hyprtester/test.lua -b ./build/Hyprland -p hyprtester/plugin/hyprtestplugin.so
```

也可以调用对应的 Makefile 目标：

```sh
make hyprtest
```

*运行需要一些时间！*
最后，程序会输出汇总结果，列出通过和失败的测试数量。

失败的测试数应为 **0**。

<a id="run-selected-tests"></a>

#### 运行指定测试

如果只想运行特定测试，在命令行中列出测试名称即可（不含组名或文件名），例如：

```sh
./build/hyprtester/hyprtester dwindleSplit focusMasterPrevious processSpawning -c hyprtester/test.lua -b ./build/Hyprland -p hyprtester/plugin/hyprtestplugin.so
```

也可以在调用 Makefile 目标时额外设置 `HYPRTESTS` 变量：

```sh
make HYPRTESTS="dwindleSplit focusMasterPrevious processSpawning" hyprtest
```

<a id="submitting-new-tests"></a>

## 提交新测试

如果被测功能可以进行单元测试，就必须将新测试写成 GTest；否则应将其加入 hyprtester。

这两类测试都可以在项目的测试目录中找到。
GTests 位于 `tests/`，hyprtester 测试位于 `hyprtester/`。

<a id="what-to-test"></a>

### 测试哪些内容

如果你提交的是新功能，自然应该测试该功能。
如果你修复了缺陷，请尽量编写一个在修复前会失败的测试用例。

编写新测试时，可以查看测试覆盖率报告。

首先，_两者都要运行_：ctest 和 hyprtester。
然后，在仓库根目录运行：

```sh
gcovr -r . build --html --html-details -o build/coverage.html --gcov-ignore-parse-errors="negative_hits.warn" && xdg-open ./build/coverage.html
```

命令会运行一段时间，然后在浏览器中打开报告。
你可以查看哪些文件已被测试，以及各文件的测试覆盖率。点击文件即可逐行查看覆盖情况。

如果发现尚未覆盖的代码路径，我们很欢迎你为它们补充测试。
