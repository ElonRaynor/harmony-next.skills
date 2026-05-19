---
name: harmony-next
description: Use for HarmonyOS NEXT development help and local DevEco automation. Covers ArkTS/ArkUI/NDK API lookup, offline guide navigation, DevEco Studio and HarmonyOS Emulator tasks, hdc/uitest/aa/bm/hilog/hidumper diagnostics, and private DevEco interfaces such as CodeGenie, MCP, LanceDB, devecostudio://, ArkUI Inspector, Previewer, Profiler, Doctor, and UxTestService.
---

# HarmonyOS NEXT Agent Guide

Use this skill to answer HarmonyOS NEXT questions with the bundled offline references. Keep context small: route the request first, then open only the specific Markdown files needed for the answer or action.

## Routing

1. **Classify the user request**
   - API, component, error, or code example: use the offline API indexes.
   - DevEco Studio or emulator automation: use the private-interface playbooks below.
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

- 先按关键词命中路径：`rg -n "UIAbility|AbilityStage|Want" references/INDEX.md | head`
- 查某个 `@ohos.*` 模块：`rg -n "@ohos\\.app\\.ability\\.|@ohos\\.ability\\." references/INDEX.md | rg "JsEtsAPIReference/" | head`
- 查 NDK/C API 头文件：`rg -n "JsEtsAPIReference/topics/.*/.*\\.h\\.md$" references/INDEX.md | rg "(napi|arkui|window|ability)" | head`

## DevEco Emulator Automation

Use when the user asks to start or inspect HarmonyOS Emulator without the IDE, operate the emulator from command line, or diagnose hdc/uitest/aa/bm/hilog/hidumper automation.

Read `references/ideGuides/DevEco模拟器私有接口与AI自动化.md` before acting. Treat it as an agent playbook for private, version-sensitive behavior; verify the local DevEco/Emulator version before relying on paths, flags, output fields, or ports.

Default boundary:

- 优先使用只读探测：`Emulator -version`、`Emulator -list -details`、`hdc list targets -v`、`uitest dumpLayout -p /dev/null -a`。
- UI 操作优先走 `hdc -t <target> shell uitest uiInput`；do not use blind desktop-coordinate clicks.
- 真实截图、layout、日志包、`file recv`、安装/卸载、创建/删除 HVD、端口转发、底层 `uinput`、`hitrace` 都需要用户确认和脱敏策略。
- 多 target 时必须显式选择 `127.0.0.1:<port>`；只选择 `Connected`，忽略 `Offline`。
- 不能分类的命令按 `require_confirm` 处理；刷写、格式化、清数据、root/daemon 模式等系统级命令默认禁止。

## DevEco Studio Private Interfaces

Use when the user asks about DevEco Studio internals or automation for CodeGenie, local AI/RAG/MCP, `devecostudio://`, Previewer, ArkUI Inspector, Profiler, Doctor, Diagnostic, FaultLog, UxTestService, plugin actions, tool windows, or services.

Read `references/ideGuides/DevEco Studio IDE私有接口与AI自动化.md` before acting. Treat it as a safety-first playbook, not as a stable public API reference. Reconfirm the installed DevEco version and local paths before using any plugin ID, class name, URL scheme, port range, handler, cache path, or local service.

Default boundary:

- 只读允许：枚举 DevEco 包内文件、解析 `Info.plist` / `product-info.json` / 插件 XML、扫描 jar 类名和字符串、分析离线 `.htrace` / faultlog / stacktrace / `.arkli` / `.preview` 产物。
- 需要确认：启动 IDE/GUI/JCEF/Preview Server/Inspector/Profiler/Debug，连接设备，抓截图/日志/layout，读取用户侧缓存或聊天历史，调用 CodeGenie localhost HTTP/WebSocket，创建 MCP 配置，触发外部 LLM provider。
- 默认禁止：自动登录、上传、部署、清缓存、删除状态、公开 token/securityId/API key/项目片段/日志正文、未隔离验证未知 `devecostudio://` URL。

CodeGenie、MCP、LanceDB、HTTP forwarding、Application Agent、Operation Analyzer、Cloud Toolkit 这类能力必须先做隐私和账号边界判断，再决定是否进入确认档验证。

## Answering Constraints

- **不要全量读取**：先在 `INDEX.md` 命中路径，再打开对应 `.md`。
- **不确定就查文档**：API 签名、入参、返回值以 `references/` 内文本为准，不凭经验补全。
- **ArkUI 优先声明式**：示例优先使用 `@Entry` / `@Component` / `build()`（除非文档明确是 NDK 或系统服务）。
- **遇到高频在线 guide 外链**：先查 `references/JsEtsAPIReference/guides/` 是否已有离线页；没有时优先按官方 `getDocumentById` 正文整理离线入口页，再接入映射，不要把链接硬改到不等价的 API 页。

<!-- version: 1.3.5 -->
