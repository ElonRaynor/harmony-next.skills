# Issue 17: Emulator first-run license agreement classification

GitHub issue #17 反馈：重装 DevEco Studio 后，`hvd_manager.py doctor --json` 可以报告环境健康，但首次执行 `hvd_manager.py launch` 时，HarmonyOS Emulator 会在 stdin 上要求确认华为许可协议。

原有实现会把该场景落到通用 `trace-timeout` / startup failure 诊断，agent 容易误判成 trace pipe、HDC 或镜像路径问题。

实现：

- `hvd_manager.py launch` 默认不自动同意协议。
- Emulator stdout/stderr 日志尾部包含协议确认提示时，返回：

```json
{
  "decision": "blocked",
  "result": "license-agreement-required",
  "missingConfig": ["emulatorLicenseAgreement"]
}
```

- 新增显式 opt-in 参数 `--accept-license`，只有传入该参数时才向 Emulator stdin 写入 `y\n`。
- `recommendations` 明确提示可以先交互式启动一次，或在阅读协议后显式传入 `--accept-license`。

验证：

```bash
python3 -m unittest harmony-next/tests/test_hvd_manager.py
```

结果：

- `hvd_manager` 专项 21 个测试通过。
- 新增 fake Emulator 覆盖默认分类和 `--accept-license` 显式确认两个分支。
