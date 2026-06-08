# Issue 16: trace-timeout actionable diagnostics

GitHub issue #16 反馈：升级到 release `v1.3.20` 后，`hvd_manager.py launch` 使用 DevEco Studio Emulator、有效 HVD root 和有效 emulator image root 启动本地 HVD 时，Emulator 没有连接 `-t <trace-name>` 对应的 trace socket，最终返回：

- `socketConnected=false`
- `result=trace-timeout`
- `missingConfig=["tracePipeConnection"]`
- `hdc list targets -v` 仅显示 `Offline localhost`
- `Emulator -list -details` 也可能长时间无输出

本轮不把该现象伪装成已绕过 DevEco 私有启动限制，而是强化失败 payload，让 agent 和用户能继续定位是 Emulator runtime 卡住、HDC stale target、进程提前退出，还是 trace 启动契约变化。

实现：

- `harmony-next/scripts/hvd_manager.py` 新增 `traceTimeoutDiagnostics` 字段。
- trace socket 超时时继续保留既有 `result=trace-timeout` 和 `missingConfig=["tracePipeConnection"]`，兼容旧消费方。
- `traceTimeoutDiagnostics` 包含 `socketPath`、`timeoutSeconds`、`likelyCauses`、`nextDiagnosticCommands` 和 `manualChecks`。
- 根据 `processExitCode`、`Emulator -list -details` 结果、`hdcSnapshot` 中的 Offline target 做轻量归因。

验证：

```bash
python3 -m unittest harmony-next/tests/test_hvd_manager.py
python3 -m unittest discover -s harmony-next/tests
```

结果：

- `hvd_manager` 专项 19 个测试通过。
- 全仓库 unittest 45 个测试通过。

