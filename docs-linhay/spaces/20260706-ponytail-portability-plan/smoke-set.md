# Retrieval Quality Smoke Set

日期：2026-07-06

用途：固定 10 个 HarmonyOS NEXT 高频问题，检查 agent 是否先命中文档路径，再给答案和验证路径。这里只做路径和期望输出约束，不做 LLM 自动评分。

## 评分规则

- 必须先说明使用 `harmony-next/SKILL.md` 的检索路径。
- 必须打开每题列出的 1-3 个目标文档。
- 答案必须包含验证命令；没有稳定命令时返回明确的 `blocked` / 前置条件。
- 不得只凭模型记忆补 API 签名。

## 题目

### 1. ArkUI Button

- 问题：ArkUI `Button` 的常用写法和可点击验证怎么查？
- 目标文档：`harmony-next/references/TASK_MAP.md`、`harmony-next/references/JsEtsAPIReference/topics/components/Button.md`
- 必含验证：有运行页面和 HDC target 时执行 `hdc -t <target> shell uitest dumpLayout -p <remote.json> -a`；需要点击时从 bounds 算中心点再 `hdc -t <target> shell uitest uiInput click <x> <y>`；缺 target 或运行页面则 blocked。

### 2. UIAbility / Want

- 问题：Stage 模型里如何确认 `UIAbility` 生命周期和 `Want` 参数传递？
- 目标文档：`harmony-next/references/KITS.md`、`harmony-next/references/JsEtsAPIReference/modules/ohos/@ohos.app.ability.UIAbility (带界面的应用组件).md`、`harmony-next/references/JsEtsAPIReference/guides/启动应用内的UIAbility组件.md`
- 必含验证：明确 bundle/ability 后才执行 `hdc -t <target> shell aa start -b <bundle> -a <ability>`；参数传递用应用内日志或 `hilog` 验证；缺目标应用则 blocked。

### 3. Network HTTP / Socket

- 问题：HTTP 请求和 socket 连接应从哪些 Network 文档确认？
- 目标文档：`harmony-next/references/TASK_MAP.md`、`harmony-next/references/JsEtsAPIReference/modules/ohos/@ohos.net.http (数据请求).md`、`harmony-next/references/JsEtsAPIReference/modules/ohos/@ohos.net.socket (Socket连接).md`
- 必含验证：需要声明网络权限、给出可访问测试 URL 或 socket endpoint；缺网络目标或权限配置时 blocked。

### 4. Data RDB / Preferences

- 问题：关系型数据库和用户首选项应该查哪些模块？
- 目标文档：`harmony-next/references/KITS.md`、`harmony-next/references/JsEtsAPIReference/modules/ohos/@ohos.data.rdb (关系型数据库).md`、`harmony-next/references/JsEtsAPIReference/topics/misc/Preferences.md`
- 必含验证：说明 ArkTS API 与 C API 分开确认签名；有工程时用单元测试或最小页面读写后验证结果；无工程则 blocked。

### 5. Command Line Tools

- 问题：如何下载、安装并验证 HarmonyOS Command Line Tools？
- 目标文档：`harmony-next/SKILL.md`、`harmony-next/references/ideGuides/独立命令行工具配置手册.md`、`harmony-next/references/ideGuides/命令行工具指南.md`
- 必含验证：先跑 `python3 harmony-next/scripts/commandline_tools_manager.py doctor --tools-root <dir> --json`；下载中心页面 URL 必须返回 blocked，不能假装解析直链。

### 6. NDK Node-API

- 问题：ArkTS 调 C++ 插件时 Node-API/NAPI 文档和头文件怎么定位？
- 目标文档：`harmony-next/references/ndkGuides/NDK开发与Node-API指南.md`、`harmony-next/references/JsEtsAPIReference/topics/misc/Node-API.md`、`harmony-next/references/JsEtsAPIReference/topics/misc/native_node_napi.h.md`
- 必含验证：检查 `CMakeLists.txt` 是否链接 `libace_napi.z.so`，检查 `build-profile.json5` 的 `externalNativeBuild`；已有 native 工程时跑 `hvigorw --mode module -p module=entry@default assembleHap`，否则 blocked。

### 7. Testing / Publishing / Security

- 问题：测试、签名发布和权限声明怎么走文档而不是猜？
- 目标文档：`harmony-next/references/testing/应用测试与Hypium指南.md`、`harmony-next/references/ideGuides/应用签名指南.md`、`harmony-next/references/JsEtsAPIReference/guides/声明权限.md`
- 必含验证：测试题给出 Hypium/单元测试或 UI 测试命令；签名发布题检查证书/Profile/`module.json5` 权限声明；缺测试工程或签名材料则 blocked。

### 8. HVD / Emulator

- 问题：无 IDE 启动 HarmonyOS Emulator 前要检查什么？
- 目标文档：`harmony-next/SKILL.md`、`harmony-next/references/ideGuides/DevEco模拟器私有接口与AI自动化.md`
- 必含验证：先跑 `python3 harmony-next/scripts/hvd_manager.py doctor --json`；缺 HVD root、image root 或 trace 前置时返回 blocked。

### 9. Offline UI/UX Audit

- 问题：如何对运行中的页面做离线 UI/UX 体检？
- 目标文档：`harmony-next/SKILL.md`、`harmony-next/references/ideGuides/DevEco Studio IDE私有接口与AI自动化.md`
- 必含验证：先跑 `python3 harmony-next/scripts/ux_audit_pipeline.py doctor --deveco-app <DevEco-Studio.app> --python <python> --json`；有 target 时跑 `capture-audit --target <target> --artifact-dir <dir> --json`；已有证据时跑 `audit --evidence-summary <summary.json> --json`；缺 target/证据则 blocked。

### 10. Profiler Trace

- 问题：已有 `.htrace` / bytrace 文件时如何做离线性能审计？
- 目标文档：`harmony-next/SKILL.md`、`harmony-next/references/performanceAndStandards/性能调优与Profiler指南.md`
- 必含验证：先跑 `python3 harmony-next/scripts/profiler_trace_audit.py doctor --deveco-app <DevEco-Studio.app> --json`；已有输入 trace 时跑 `python3 harmony-next/scripts/profiler_trace_audit.py audit --input <trace> --output-dir <dir> --json`；缺 trace 或 `trace_streamer` 则 blocked。
