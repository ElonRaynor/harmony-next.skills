# Issue 13: Emulator CLI trace preflight

日期：2026-05-28

## 背景

GitHub issue #13 反馈：Agent 直接执行 `Emulator -hvd ... -path ... -imageRoot ...` 时，DevEco Emulator 可能弹出登录/设备管理模态框：

```text
模拟器启动失败
请在DevEco Studio中登录华为账号，并从设备管理中启动模拟器
```

该现象容易被误判为用户必须先登录 DevEco Studio。结合 2026-05-18 的免 IDE 启动验证，根因边界应归类为 CLI 启动路径缺少 `-t <trace-name>` 和已准备好的 trace pipe。

## 验收场景

Given Agent 需要从 CLI 启动 HarmonyOS Emulator
When 没有已验证 trace pipe helper 或 helper readiness 信号
Then `harmony-next` skill 不应建议或执行只有 `-hvd` / `-path` / `-imageRoot` 的启动命令，并应返回 machine-readable `blocked`

Given trace pipe helper 已准备并输出 readiness 文件
When 运行 `hvd_manager.py launch-preflight`
Then 输出包含 `-t <trace-name>` 的 Emulator 启动命令计划，但不直接启动 Emulator

Given Agent 需要由仓库脚本直接启动 Emulator
When 运行 `hvd_manager.py launch --name <hvd> --image-root <dir> --trace-name <name>`
Then 脚本创建有界 trace socket，启动带 `-t <trace-name>` 的 Emulator 命令，并输出 `operation=emulator.launch`、`socketConnected` 和 `traceBytesRead`

## 实现

- `harmony-next/scripts/hvd_manager.py` 新增 `launch-preflight` 子命令，并补充直接启动用的 `launch` 子命令。
- preflight 校验 HVD、Emulator 可执行文件、SDK root、`traceName` 和 `tracePipeHelper` readiness 文件。
- 缺少 trace helper 时返回 `decision=blocked`、`operation=emulator.launch.preflight`，并输出已知 modal 症状，帮助未来 Agent 快速分类。
- preflight 通过时只输出 `emulatorCommand`，不直接执行 Emulator。
- `launch` 校验 HVD、Emulator、image root 和 trace name，创建 `/tmp/<trace-name>` trace socket，启动 Emulator，并可按 `--no-wait-target` 跳过 HDC target 等待。

## 验证

```bash
python3 -m unittest harmony-next/tests/test_hvd_manager.py
```

结果：`hvd_manager` 专项 13 个测试通过，全量 `harmony-next/tests` 37 个测试通过。
