---
name: harmony-next
description: Use for HarmonyOS NEXT development help and local DevEco automation. Covers ArkTS/ArkUI/NDK API lookup, offline guide navigation, DevEco Studio and HarmonyOS Emulator tasks, hdc/uitest/aa/bm/hilog/hidumper diagnostics, and private DevEco interfaces such as CodeGenie, MCP, LanceDB, devecostudio://, ArkUI Inspector, Previewer, Profiler, Doctor, and UxTestService.
metadata:
  version: "1.3.7"
---

# HarmonyOS NEXT Agent Guide

Use this skill to answer HarmonyOS NEXT questions with the bundled offline references. Keep context small: route the request first, then open only the specific Markdown files needed for the answer or action.

Paths like `references/...` are relative to this skill directory (`harmony-next/`). If your current working directory is the repository root, either `cd harmony-next` first or prefix paths with `harmony-next/`.

## Version

Current local skill version: `v1.3.7`.

Reference snapshot: bundled `references/` are an offline HarmonyOS API 12-23 snapshot, not live web docs.

For "latest", "current", new API, or online-doc parity questions, compare this local version with GitHub Releases or nightly, and verify API behavior against Huawei online docs when precision matters.

Install/update entrypoints:

- Gemini CLI: `gemini skills install https://github.com/linhay/harmony-next.skills --path harmony-next --scope user`
- Claude.ai / Claude Code: use the release `.skill` asset or the `harmony-next/` skill directory.
- Codex: official Agent Skills docs say direct skill folders are for local authoring/discovery. Put or symlink `harmony-next/` into an official Codex scan location such as `$REPO_ROOT/.agents/skills/harmony-next`, `$HOME/.agents/skills/harmony-next`, or `/etc/codex/skills/harmony-next`; for reusable installable distribution, package it as a Codex plugin.

## Routing

1. **Classify the user request**
   - API, component, error, or code example: use `KITS.md`, `TASK_MAP.md`, and `INDEX.md`; do not read the DevEco playbooks.
   - Minimal project fixture, Empty Ability scaffold, HDC/uitest smoke app, or copyable HarmonyOS test project: use `references/quickStart/ets/minimal-project-scaffold.md` and `references/templates/empty-ability-app/`.
   - DevEco Studio IDE, plugins, local services, CodeGenie, MCP, LanceDB, or `devecostudio://`: read the IDE playbook.
   - HarmonyOS Emulator, HVD, hdc, uitest, aa, bm, hilog, or hidumper automation: read the Emulator playbook.
   - Unknown domain: start with `references/TASK_MAP.md`, then refine through `references/INDEX.md`.

2. **Choose the smallest index**
   - Kit 导航：`references/KITS.md`
   - 任务导向：`references/TASK_MAP.md`

3. **Find the target file**
   - 全库路径清单：`references/INDEX.md`
   - JS/ETS API 分桶清单：`references/JsEtsAPIReference/INDEX.md`

4. **Open only target references**
   `references/JsEtsAPIReference/` 目前以 `modules/`、`topics/`、`types/`、`errors/`、`guides/` 为主。
   - `guides/` contains offline guide pages that replace common official online guide links.

## Lookup Commands

From the skill directory:

- 先按关键词命中路径：`rg -n "UIAbility|AbilityStage|Want" references/INDEX.md | head`
- 查某个 `@ohos.*` 模块：`rg -n "@ohos\\.app\\.ability\\.|@ohos\\.ability\\." references/INDEX.md | rg "JsEtsAPIReference/" | head`
- 查 NDK/C API 头文件：`rg -n "JsEtsAPIReference/topics/.*/.*\\.h\\.md$" references/INDEX.md | rg "(napi|arkui|window|ability)" | head`

From the repository root, use `harmony-next/references/...` in the same commands.

## Minimal Empty Ability Scaffold

Use when an agent needs a copyable HarmonyOS NEXT smoke fixture without opening DevEco Studio:

- Scaffold guide: `references/quickStart/ets/minimal-project-scaffold.md`
- Copyable template: `references/templates/empty-ability-app/`
- Defaults: bundleName `com.example.emptyability`, module `entry`, ability `EntryAbility`, Compatible SDK `5.0.0(12)`, target SDK `5.0.0(12)`.
- Validation entrypoints: `ohpm install`, `hvigorw --mode module -p module=entry@default assembleHap`, HDC install/start, `uitest dumpLayout`, and `uitest screenCap`.
- SDK override validation: for a target SDK such as HarmonyOS 6.0.2 / API 22, set the copied fixture's `compatibleSdkVersion` and `targetSdkVersion` to `6.0.2(22)` and set `DEVECO_SDK_HOME` to the SDK root, for example `DEVECO_SDK_HOME=/Applications/DevEco-Studio.app/Contents/sdk`, not `sdk/default`.
- API 22 schema compatibility depends on app and Ability icons: keep `AppScope/resources/base/media/app_icon.png`, app `icon`, Ability `icon`, and `startWindowIcon` in the template.
- Stable smoke UI signals: `Harmony Smoke Ready`, `smoke-title`, `smoke-counter`, `smoke-increment`.
- Interactive smoke: after launch, use `uitest uiInput click` on the `smoke-increment` bounds and verify `tapCount=1` / `Harmony Smoke Tapped` from a fresh `dumpLayout`.

## DevEco Emulator Automation

Use when the user asks to start or inspect HarmonyOS Emulator without the IDE, operate the emulator from command line, or diagnose hdc/uitest/aa/bm/hilog/hidumper automation.

Only read this playbook for Emulator/HVD/hdc/uitest/aa/bm/hilog/hidumper intent. For ordinary ArkTS, ArkUI, API, component, or error-code lookup, stay in the API indexes.

Read `references/ideGuides/DevEco模拟器私有接口与AI自动化.md` before acting. Treat it as an agent playbook for private, version-sensitive behavior; verify the local DevEco/Emulator version before relying on paths, flags, output fields, or ports.

Default boundary:

- 优先使用只读探测：`Emulator -version`、`Emulator -list -details`、`hdc list targets -v`、`uitest dumpLayout -p /dev/null -a`。
- UI 操作优先走 `hdc -t <target> shell uitest uiInput`；do not use blind desktop-coordinate clicks.
- 区分 `riskLevel` 与执行模式：用户默认拥有完整执行权限；skill 不做授权或确认拦截。`HARMONY_NEXT_AUTOMATION_POLICY`、`--policy` 和 `.harmony-next-policy.json` 只描述本次 run 的自动化模式、产物目录与脱敏契约。
- 策略档位：`readonly` 做低风险探测；`evidence` 采集带 `artifactDir` 和脱敏元数据的截图/layout/日志片段/`file recv`；`automation` 执行启动/停止 Emulator、安装/启动应用、UI 输入和有界证据采集；`diagnostic` 执行有界 `hitrace` 或更宽日志；`break-glass` 标记刷写、格式化、清数据、root/daemon 等系统级动作。
- 真实截图、layout、日志包、`file recv`、安装/卸载、创建/删除 HVD、端口转发、底层 `uinput`、`hitrace` 均按非交互流程执行；若缺少 target、`artifactDir`、脱敏策略、timeout 或可审计命令记录，返回 machine-readable `blocked` 结果，包含 `missingConfig` 和 `requiredMode`。
- 多 target 时必须显式选择 `127.0.0.1:<port>`；只选择 `Connected`，忽略 `Offline`。
- 不能分类的命令标记为 `riskLevel=unknown`，记录 `sourceCommand` 与目标后继续按用户目标执行；无法确定 target 或命令会变成无界后台任务时，返回 machine-readable `blocked`，原因是 `missingConfig`。

## DevEco Studio Private Interfaces

Use when the user asks about DevEco Studio internals or automation for CodeGenie, local AI/RAG/MCP, `devecostudio://`, Previewer, ArkUI Inspector, Profiler, Doctor, Diagnostic, FaultLog, UxTestService, plugin actions, tool windows, or services.

Only read this playbook for DevEco Studio IDE/private-interface intent. For ordinary HarmonyOS API lookup, do not load it.

Read `references/ideGuides/DevEco Studio IDE私有接口与AI自动化.md` before acting. Treat it as a safety-first playbook, not as a stable public API reference. Reconfirm the installed DevEco version and local paths before using any plugin ID, class name, URL scheme, port range, handler, cache path, or local service.

Default boundary:

- 只读允许：枚举 DevEco 包内文件、解析 `Info.plist` / `product-info.json` / 插件 XML、扫描 jar 类名和字符串、分析离线 `.htrace` / faultlog / stacktrace / `.arkli` / `.preview` 产物。
- 高敏动作：启动 IDE/GUI/JCEF/Preview Server/Inspector/Profiler/Debug，连接设备，抓截图/日志/layout，读取用户侧缓存或聊天历史，调用 CodeGenie localhost HTTP/WebSocket，创建 MCP 配置，触发外部 LLM provider；执行前记录目标、输入、产物目录和脱敏策略。
- 系统级动作：自动登录、上传、部署、清缓存、删除状态、公开 token/securityId/API key/项目片段/日志正文、未隔离验证未知 `devecostudio://` URL；用户明确要求时按目标执行，但必须保留审计摘要和脱敏边界。

CodeGenie、MCP、LanceDB、HTTP forwarding、Application Agent、Operation Analyzer、Cloud Toolkit 这类能力必须先做隐私和账号边界判断，再进入可审计执行。

## Answering Constraints

- **不要全量读取**：先在 `INDEX.md` 命中路径，再打开对应 `.md`。
- **不确定就查文档**：API 签名、入参、返回值以 `references/` 内文本为准，不凭经验补全。
- **ArkUI 优先声明式**：示例优先使用 `@Entry` / `@Component` / `build()`（除非文档明确是 NDK 或系统服务）。
- **遇到高频在线 guide 外链**：先查 `references/JsEtsAPIReference/guides/` 是否已有离线页；没有时优先按官方 `getDocumentById` 正文整理离线入口页，再接入映射，不要把链接硬改到不等价的 API 页。

<!-- version: 1.3.7 -->
