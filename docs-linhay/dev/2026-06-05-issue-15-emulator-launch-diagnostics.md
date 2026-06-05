# Issue 15: DevEco Emulator launch diagnostics

GitHub issue #15 反馈：在 DevEco Studio `/Applications/DevEco-Studio.app`、HarmonyOS Emulator `6.0.2.200` 环境中，直接执行带 `-t <trace-name>` 的 `Emulator -hvd ... -path ... -imageRoot ... -hdcport ...` 命令后，Emulator 进程可短暂出现但随后静默退出，stdout/stderr 为空，`hdc list targets -v` 始终为空，`Emulator -list -details` 仍显示 HVD `isRunning=false`。

同一链路还暴露了 issue #14 的 image root 混淆：`/Applications/DevEco-Studio.app/Contents/sdk` 是 build SDK root，不一定包含模拟器系统镜像；HVD `config.ini` 中的 `imageSubPath=system-image/...` 应拼到 emulator image root 下验证。macOS 常见 emulator image root 是 `$HOME/Library/Huawei/Sdk`。

验收标准：

- `launch-preflight` 和 `launch` 都按 HVD `imageSubPath` 校验 `<image-root>/<imageSubPath>`，错误目录在启动前返回 `missingConfig=["imageRootSystemImage"]`。
- `launch` 不再丢弃 Emulator stdout/stderr，而是写入 `artifactDir/emulator-launch.log` 并在 JSON 中返回 `logPath` 和 `logTail`。
- trace socket 超时或 Emulator 静默退出时，JSON 返回 `processExitCode`、`hvdRuntime`、`hdcSnapshot`，帮助区分启动慢、trace 前置条件缺失、CLI 参数变化和本机环境异常。
- 等待 HDC target 后继续检查 `bootevent.boot.completed`，返回 `hdcWait` 和 `bootWait`。
- 当前 `launch` 将 Emulator 进程和 trace holder 都放入独立 session，避免调用方命令结束时被进程组清理；trace holder 默认持有 1800 秒。后续生命周期调整应补充 attached 终端托管模式，前台 runner 结束时通过 `Emulator -stop` 回收模拟器，同时保留 detached 兼容模式。
- 默认稳定性窗口为 60 秒；在窗口内持续校验 Emulator 进程和 HDC target，失败时返回 `stabilityWait.stable=false`。

实现：

- `harmony-next/scripts/hvd_manager.py` 新增 emulator image root 候选、HDC 候选、HVD `imageSubPath` 暴露、`--image-root` preflight 参数、`--hdc`、`--artifact-dir`、`--trace-hold-seconds` 和 `--stability-seconds`。
- `doctor` 同时输出 build SDK root、emulator image root 和 HDC 探测结果。
- `launch` 失败路径采集 Emulator runtime 快照和 HDC target 快照。

生命周期后续核查表：

1. attached 模式应由父 runner 保持前台，不在启动成功后退出。
2. attached 模式应在同一进程生命周期内持有 trace socket，而不是依赖 detached trace holder。
3. runner 捕获 `SIGINT`、`SIGTERM`、`SIGHUP` 和正常退出后，应统一调用 `Emulator -stop "<hvd-name>" -path "<hvd-root>"`。
4. cleanup 只删除当前 `trace-name` / `run_id` 绑定的 trace path，不做固定路径通配清理。
5. cleanup 后应返回 `hdc list targets -v` 和 `Emulator -list -details` 的裁剪摘要；target 未消失时标记 `cleanup_failed`。
6. detached 模式仍可保留，但必须显式声明由调用方负责停止模拟器和控制 trace holder 时长。

验证：

```bash
python3 -m unittest harmony-next/tests/test_hvd_manager.py
```

结果：`hvd_manager` 专项 18 个测试通过。

前台终端托管原型验证：

- 使用临时 foreground runner 在 macOS Terminal 中启动 `Codex Test Phone`，trace name 为 `codex-foreground-20260605184919`，HDC port 为 `10106`。
- runner 在前台进程内创建并持有 `/tmp/<trace-name>` trace socket，不启动 detached trace holder。
- HDC 验证通过：`hdc list targets -v` 出现 `127.0.0.1:10106 TCP Connected localhost`，`param get bootevent.boot.completed` 返回 `true`。
- `ps` 验证 Emulator 进程处于前台终端会话下：`Emulator ... -t codex-foreground-20260605184919 ... -hdcport 10106` 状态为 `S+`。
- runner 退出后执行 `Emulator -stop "Codex Test Phone" -path "$HOME/.Huawei/Emulator/deployed"`，最终 `hdc list targets -v` 中 `10106` 回到 `Offline`，未留下活的 Emulator 进程。
- 该验证只证明 attached 生命周期模型可行；仓库脚本 `hvd_manager.py launch` 当前仍是 detached 实现，尚未提供 `--lifecycle attached` 参数。

本机真实验证：

- `launch-preflight` 使用 `/Applications/DevEco-Studio.app/Contents/sdk` 作为 `--image-root` 时返回 `missingConfig=["imageRootSystemImage"]`。
- `launch-preflight` 使用 `$HOME/Library/Huawei/Sdk` 作为 `--image-root` 时返回 `decision=allowed`。
- `launch --name "Codex Test Phone" --image-root "$HOME/Library/Huawei/Sdk" --hdc-port 10106 --stability-seconds 90 --json` 返回 `decision=allowed`，`socketConnected=true`，`traceBytesRead=282`，`hdcWait.connected=true`，`bootWait.completed=true`，`stabilityWait.stable=true`。
- 脚本返回后，外部命令继续可用：`hdc list targets -v` 显示 `127.0.0.1:10106 TCP Connected localhost`，`param get bootevent.boot.completed` 返回 `true`，`uitest dumpLayout` 成功保存 layout。
- 验证结束后执行 `Emulator -stop "Codex Test Phone" -path "$HOME/.Huawei/Emulator/deployed"`，并重启 HDC server，最终 `hdc list targets -v` 回到 `[Empty]`。
