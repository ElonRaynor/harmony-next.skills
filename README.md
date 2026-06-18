# HarmonyOS NEXT 开发者专家技能包

给 Gemini CLI、Claude Code、Codex 等 AI 编程助手使用的 HarmonyOS NEXT 离线参考技能库。

语言：中文 | [English](./README_en.md)

[![release](https://img.shields.io/badge/release-v1.3.23-1f6feb?style=flat-square)](https://github.com/linhay/harmony-next.skills/releases/tag/v1.3.23)
[![skills.sh](https://skills.sh/b/linhay/harmony-next.skills)](https://skills.sh/linhay/harmony-next.skills)
[![readme](https://img.shields.io/badge/readme-English-0f766e?style=flat-square)](./README_en.md)
![docs](https://img.shields.io/badge/docs-3,693%20markdown%20files-7c3aed?style=flat-square)
![js-ets](https://img.shields.io/badge/JsEtsAPIReference-3,666%20files-b45309?style=flat-square)

> 面向 API 12-23 的本地知识源，覆盖 ArkTS、ArkUI、NDK、工具链、调试、发布与多端适配。

## 它解决什么问题

`harmony-next.skills` 不是普通文档镜像，而是一套给 AI 编程助手使用的 HarmonyOS NEXT 检索层。

它主要解决这几类问题：

- `@ohos.*` 模块到底在哪个文件
- 某个 ArkUI 组件、接口或 NDK 头文件是否真的存在
- API 23 新增内容有没有纳入当前知识库
- 某个旧链接是否已经迁移、是否还能跳转
- DevEco Studio 模拟器、`hdc`、`uitest` 等本地自动化链路该如何安全验证
- DevEco Studio IDE、CodeGenie、MCP、Inspector、Profiler 等私有能力该如何先隔离验证再使用

这个仓库的目标，是把这些问题变成可定位、可跳转、可验证的本地文件查询。

## 核心特性

| 能力 | 说明 |
| --- | --- |
| 离线可检索 | 不依赖模型记忆猜 API，先命中文档路径再读取正文 |
| 面向 Agent 工作流 | 按 `SKILL.md -> KITS/TASK_MAP -> INDEX` 组织，适合渐进式检索 |
| 不只 API 手册 | 还包含 IDE、签名、调试、发布、性能、多端与 NDK 实战指引 |
| 私有接口隔离 | DevEco 模拟器与 IDE 本体私有未公开能力分别单独成章，默认先验证版本和风险门禁 |
| 非交互自动化策略 | DevEco 模拟器自动化支持 `HARMONY_NEXT_AUTOMATION_POLICY`；策略是执行模式，不是授权门槛 |
| 离线 UI/UX 体检 | 基于模拟器真实截图 + `uitest dumpLayout` 调用 DevEco `UxTestService`，输出 JSON、问题坐标和标注图 |
| 可复制最小工程 | 提供 `references/templates/empty-ability-app`，用于 HDC / `uitest dumpLayout` / screenshot smoke |

## 内容概览

| 模块 | 说明 | 入口 |
| --- | --- | --- |
| 技能规则 | 告诉 Agent 如何检索、如何回答、哪些内容要优先信文档 | [`harmony-next/SKILL.md`](./harmony-next/SKILL.md) |
| Kit 导航 | 按 AbilityKit、ArkUI、ArkData、MediaKit、Security 等缩小检索范围 | [`references/KITS.md`](./harmony-next/references/KITS.md) |
| 任务导航 | 按 UI、生命周期、网络、媒体、NDK、发布等任务反查关键词 | [`references/TASK_MAP.md`](./harmony-next/references/TASK_MAP.md) |
| 全库索引 | 收录整个参考库的 Markdown 路径，用于先命中路径再读正文 | [`references/INDEX.md`](./harmony-next/references/INDEX.md) |
| API 分桶索引 | 聚焦 `JsEtsAPIReference/`，覆盖 modules、topics、types、errors、guides | [`JsEtsAPIReference/INDEX.md`](./harmony-next/references/JsEtsAPIReference/INDEX.md) |
| Empty Ability 最小工程 | 可复制到任意仓库的 HarmonyOS NEXT smoke fixture，默认 `com.example.emptyability` / `EntryAbility` / `5.0.0(12)` | [`references/templates/empty-ability-app`](./harmony-next/references/templates/empty-ability-app/) |
| 最小工程脚手架指南 | 说明如何复制模板、路由页与 `SmokeCounter` 组件解耦、运行 `ohpm install`、`hvigorw --mode module`、SDK 版本适配验证、安装启动、`uitest dumpLayout` 和点击 smoke | [`minimal-project-scaffold.md`](./harmony-next/references/quickStart/ets/minimal-project-scaffold.md) |
| DevEco 模拟器私有接口 | 免 IDE 启动 Emulator、`hdc + uitest`、HVD、日志与诊断的本地验证边界 | [`DevEco模拟器私有接口与AI自动化.md`](./harmony-next/references/ideGuides/DevEco模拟器私有接口与AI自动化.md) |
| DevEco IDE 私有接口 | CodeGenie、本地 RAG/MCP、`devecostudio://`、Previewer、ArkUI Inspector、Profiler、Doctor、UxTestService 与离线 UI/UX 体检的验证边界 | [`DevEco Studio IDE私有接口与AI自动化.md`](./harmony-next/references/ideGuides/DevEco%20Studio%20IDE私有接口与AI自动化.md) |
| 命令行工具配置 | Command Line Tools 直链下载、本地压缩包安装、PATH 配置和 `codelinter -v` 校验 | [`commandline_tools_manager.py`](./harmony-next/scripts/commandline_tools_manager.py) |
| 设备调试证据包 | 用 `hdc` 有界采集 boot 状态、`bm/aa` 摘要、短日志、layout、截图和命令审计账本 | [`device_evidence_bundle.py`](./harmony-next/scripts/device_evidence_bundle.py) |
| 一键离线 UI/UX 体检 | 串联 `hdc` 证据采集与 DevEco `UxTestService`，输出 `summary.json`、`report.md`、规则结果和标注图 | [`ux_audit_pipeline.py`](./harmony-next/scripts/ux_audit_pipeline.py) |
| 离线 Trace 性能证据审计 | 调用 DevEco `trace_streamer` 将 `.ftrace/.htrace` 等 trace 转 SQLite，并导出耗时 span、阈值命中和元数据 JSON | [`profiler_trace_audit.py`](./harmony-next/scripts/profiler_trace_audit.py) |
| 参考正文 | 共 `3,693` 份 Markdown，其中 `3,666` 份在 `JsEtsAPIReference/` | [`harmony-next/references/`](./harmony-next/references/) |

## 推荐检索路径

```text
SKILL.md
  -> KITS.md / TASK_MAP.md
  -> INDEX.md
  -> 目标 Markdown 正文
```

为什么这样设计：

1. 先定规则，避免 Agent 一上来就盲读大库。
2. 再按 Kit 或任务缩小范围，减少误命中。
3. 用索引命中真实路径，而不是凭名称想当然。
4. 最后只打开 1-3 个目标文件读 API 细节。

这套结构的核心是：先找路径，再读内容。

## 适用场景

### ArkTS / ArkUI 开发

- 组件、装饰器、状态管理、导航、UIAbility、Want
- API 版本差异、参数签名、返回值确认
- 组件示例与文档跳转恢复

### NDK / Node-API / C API

- 头文件对应到真实 `topics/**/<header>.h.md`
- 跨语言互调、CMake、原生能力接入
- 旧路径迁移后的索引与链接校验

### IDE / 工具链 / 调试

- 签名、模拟器、真机、断点调试
- 独立命令行工具链与 CI/CD 集成
- Command Line Tools 可用 `python3 harmony-next/scripts/commandline_tools_manager.py install --archive <zip> --dest ~/.harmony/command-line-tools --profile auto` 解压并写入 shell profile；如需下载，传下载中心复制出的压缩包直链给 `bootstrap --url <archive-url>`，并建议附带 `--sha256`
- 性能分析与发布流程
- 设备调试证据包：用 `python3 harmony-next/scripts/device_evidence_bundle.py capture --deveco-app <DevEco-Studio.app> --target <target> --artifact-dir .hvigor/outputs/<run> --json` 采集真实 layout、截图、短 `hilog`、`bm/aa` 摘要和命令账本，可作为 UI/UX 体检、日志排查或复现报告输入
- 一键离线 UI/UX 体检：先用 `python3 harmony-next/scripts/ux_audit_pipeline.py doctor --deveco-app <DevEco-Studio.app> --python <python-with-ux-deps> --json` 检查 `hdc`、`UxTestService` 和 Python 图像依赖，再用 `python3 harmony-next/scripts/ux_audit_pipeline.py capture-audit --deveco-app <DevEco-Studio.app> --python <python-with-ux-deps> --target <target> --artifact-dir .hvigor/outputs/<run> --json` 生成报告
- 离线 Trace 性能证据审计：已有 `.ftrace/.htrace` / bytrace / rawtrace 文件时，使用 `python3 harmony-next/scripts/profiler_trace_audit.py audit --deveco-app <DevEco-Studio.app> --input <trace> --output-dir .hvigor/outputs/<run> --json` 生成 SQLite、`summary.json`、top callstack 和 `16.67ms / 33.34ms` 阈值命中报告
- DevEco Studio / HarmonyOS Emulator 免 IDE 启动、HVD、多实例、`hdc`、`uitest`、`aa`、`bm`、`hilog`、`hidumper` 自动化诊断
- 离线 UI/UX 体检：用 `hdc` / `uitest` 采集运行中页面截图与 layout，再调用 DevEco `UxTestService` 的可用静态规则子集生成 JSON 报告和标注图；已验证热区、图标尺寸、图标清晰度、状态栏、导航栏、遮挡、模糊、挖孔区和页面边距等规则
- 复制 `references/templates/empty-ability-app` 生成最小 Empty Ability 测试工程；页面含 `smoke-increment` 节点，适合 `uitest dumpLayout`、截图和日志 smoke
- 页面入口与 smoke 组件解耦：`pages/Index.ets` 只挂载 `SmokeCounter()`，测试 UI 与状态逻辑放在 `components/SmokeCounter.ets`
- 支持 SDK 版本适配验证：例如 HarmonyOS 6.0.2 / API 22 使用 `6.0.2(22)` 构建，配合 `DEVECO_SDK_HOME=/Applications/DevEco-Studio.app/Contents/sdk`，并保留 app `icon`、Ability `icon` 与 `startWindowIcon`
- 交互 smoke 使用 `uitest uiInput click` 点击 `smoke-increment`，重新 dump 后断言 `Harmony Smoke Tapped` / `tapCount=1`

### DevEco 模拟器私有接口

这部分属于私有未公开接口，触发词包括：`DevEco Studio`、`HarmonyOS Emulator`、`Emulator -list -details`、`免 IDE 启动`、`HVD`、`hdc`、`uitest`、`uiInput`、`aa`、`bm`、`hilog`、`hidumper`、`snapshot_display`、`uinput`、`hitrace`、`多实例`、`trace pipe`。

使用规则：

- 先读 [`harmony-next/SKILL.md`](./harmony-next/SKILL.md) 的私有接口章节，再读 [`DevEco模拟器私有接口与AI自动化.md`](./harmony-next/references/ideGuides/DevEco模拟器私有接口与AI自动化.md)。
- 每次执行前重新验证当前 DevEco / Emulator / SDK 版本和命令能力。
- 用户默认拥有完整执行权限；长时间自动化可用 `HARMONY_NEXT_AUTOMATION_POLICY`、`--policy` 或 `.harmony-next-policy.json` 描述执行模式、产物目录和脱敏契约。
- 真实截图、layout、日志包、安装卸载、端口转发、HVD 创建/删除等动作按非交互流程执行；缺少 target、artifact 目录、脱敏策略或 timeout 时才返回 machine-readable blocked 结果。
- `device_evidence_bundle.py` 已验证为可落地证据采集入口：不会启动 DevEco Studio，也不会安装、卸载、启动或停止应用；产物可能包含真实 UI、bundle、ability 和日志内容，分享前需要审阅或脱敏。
- `ux_audit_pipeline.py` 已验证为一键体检入口：运行前用 `doctor` 检查 Python 依赖，执行时把 `tools/UxTestService` 复制到 artifact-local runtime，避免向 DevEco `.app` 内写 `uxlog`。
- 如果上述 wrapper 返回 `blocked`，agent 应优先尝试官方 CLI 证据路径：`hdc list targets -v`、`uitest dumpLayout`、`screenCap`、`file recv`、`bm dump`、`aa dump` 和有界 `hilog`，再用采集到的 layout/screenshot 重跑离线 audit。
- 如果 wrapper 被阻塞、输出误导、DevEco/设备版本不兼容或缺少工作流，agent 应建议用户按脚本输出里的 `feedback` 字段和 [`ISSUE_GUIDE.md`](./harmony-next/ISSUE_GUIDE.md) 选择对应场景模板，脱敏后反馈到 GitHub Issues。
- 本仓库提供 `python3 harmony-next/scripts/hvd_manager.py`：支持 `doctor` 环境探测、`list`、`create`、`delete`、`launch-preflight` 和 `launch`。
- HVD 启动适配：`--root` / `HARMONY_HVD_ROOT` 指定 HVD root，`--emulator` / `HARMONY_EMULATOR` 指定 Emulator，`--image-root` / `HARMONY_EMULATOR_IMAGE_ROOT` 指定模拟器镜像根，`--hdc` / `HARMONY_HDC` 指定 HDC。`--sdk-root` / `DEVECO_SDK_HOME` 只表示 DevEco build SDK root，不等同于模拟器镜像根。
- macOS 常见镜像根是 `~/Library/Huawei/Sdk`；脚本会用 HVD `imageSubPath` 校验系统镜像。当前 `launch` 会 detach Emulator 与 trace holder，等待 HDC、boot 和稳定性检查；首次运行 Emulator 遇到华为许可协议确认时返回 `result=license-agreement-required` / `missingConfig=["emulatorLicenseAgreement"]`，只有显式传入 `--accept-license` 才会向 Emulator stdin 写入 `y`。后续生命周期模型应补齐 attached 终端托管模式，让终端结束时通过 `Emulator -stop` 回收模拟器，并保留 detached 兼容模式。`download-image` 当前只返回 blocked，因为镜像下载仅确认到 IDE SDK Manager UI 入口。
- 模拟器抓包与代理诊断：Charles、mitmproxy、Proxyman 等抓包工具都需要确认模拟器 NAT、宿主机可达地址和应用级代理。常见调试入口是让目标应用显式走 `10.0.2.2:9090`，例如 `setAppHttpProxy` 配合 `usingProxy: true`；Mac 侧中转脚本不能被描述为通用透明抓包方案。

### DevEco Studio IDE 私有接口

这部分属于私有未公开接口，触发词包括：`DevEco Studio IDE`、`CodeGenie`、`MCP`、`LanceDB`、`devecostudio://`、`inspect.sh`、`format.sh`、`ltedit.sh`、`ArkUI Inspector`、`Previewer`、`Profiler`、`Doctor`、`Diagnostic`、`FaultLog`、`UxTestService`、`Application Agent`、`Operation Analyzer`、`Cloud Toolkit`。

使用规则：

- 先读 [`harmony-next/SKILL.md`](./harmony-next/SKILL.md) 的 IDE 私有接口章节，再读 [`DevEco Studio IDE私有接口与AI自动化.md`](./harmony-next/references/ideGuides/DevEco%20Studio%20IDE私有接口与AI自动化.md)。
- 默认只做静态只读分析：插件 XML、jar 类名、字符串、配置路径、离线 `.htrace` / faultlog / stacktrace / `.arkli` / `.preview` 产物。
- 启动 IDE/GUI/JCEF、本地服务、设备连接、CodeGenie localhost 接口、MCP 配置、外部模型请求、读取用户缓存或聊天历史时，记录目标、输入、产物目录和脱敏边界。
- `profiler_trace_audit.py` 仅覆盖已验证的离线 trace 转换与 SQLite/JSON 摘要；不要把它描述成 DevEco Profiler GUI 的 headless 导入，也不要把设备采集能力写成已验证。
- `UxTestService` 离线 UI/UX 体检已验证为可落地子集：优先使用 `ux_audit_pipeline.py capture-audit`；必须使用真实前台 `bundle_name`、`extend_infos.language="zh"`，产物写到外部 artifact 目录；不要承诺配置文件中存在但当前包内缺实现文件的规则，也不要把仅 `uitest dumpLayout` 下返回 `UTS.0306` 的文本类规则写成完整覆盖。

### Agent 工程化集成

- Gemini CLI、Claude Code、Codex
- 本地知识库检索层
- 避免幻觉、提升可追踪性与可复现性

## 快速接入

### Vercel Labs skills CLI（推荐通用方式）

本仓库可被 [`vercel-labs/skills`](https://github.com/vercel-labs/skills) 直接发现并安装：

```bash
npx skills add linhay/harmony-next.skills --skill harmony-next
```

只查看可用技能：

```bash
npx skills add linhay/harmony-next.skills --list
```

安装到 Codex 的全局技能目录（非交互，复制文件而不是软链）：

```bash
npx skills add linhay/harmony-next.skills --skill harmony-next -a codex -g -y --copy
```

相关目录与官方示例仓库：

- [`skills.sh`](https://skills.sh/)：`vercel-labs/skills` 使用的公开目录与安全评分入口；本仓库页面是 [`skills.sh/linhay/harmony-next.skills`](https://skills.sh/linhay/harmony-next.skills)。
- [`vercel-labs/agent-skills`](https://github.com/vercel-labs/agent-skills)：Vercel 官方维护的 Agent Skills 集合。
- [`anthropics/skills`](https://github.com/anthropics/skills)：Anthropic 的公开 Agent Skills 仓库，包含 Claude skills 示例、规范与模板。

### Gemini CLI

```bash
gemini skills install https://github.com/linhay/harmony-next.skills --path harmony-next --scope user
```

### Claude Code

推荐使用 `vercel-labs/skills` CLI 安装到 Claude Code：

```bash
npx skills add linhay/harmony-next.skills --skill harmony-next -a claude-code -g -y --copy
```

这会把技能安装到 Claude Code 的全局技能目录（当前 CLI 行为是 `~/.claude/skills/harmony-next`）。

Claude.ai 网页端仍可使用 release 中的 `harmony-next.skill.zip`：在 `Settings > Capabilities > Skills` 中上传。

如果你只是想把仓库作为项目上下文附加：

```bash
git clone https://github.com/linhay/harmony-next.skills.git
claude --add-dir /path/to/harmony-next.skills/harmony-next
```

### Codex

推荐使用 `vercel-labs/skills` CLI 安装到 Codex：

```bash
npx skills add linhay/harmony-next.skills --skill harmony-next -a codex -g -y --copy
```

官方 Codex Agent Skills 文档说明：skill 是可复用工作流的创作格式；直接 skill 目录用于本地创作与发现；可安装分发单元是 Codex plugin。

官方文档：<https://developers.openai.com/codex/skills>

本仓库当前还没有打包成 Codex plugin。如果不使用 `npx skills`，可手动放入官方 skill 扫描路径。

可选官方路径：

| 范围 | 路径 |
| --- | --- |
| Repo | `$CWD/.agents/skills/harmony-next` |
| Repo | `$CWD/../.agents/skills/harmony-next` |
| Repo | `$REPO_ROOT/.agents/skills/harmony-next` |
| User | `$HOME/.agents/skills/harmony-next` |
| Admin | `/etc/codex/skills/harmony-next` |

示例：安装到当前用户的官方 skill 目录：

```bash
git clone https://github.com/linhay/harmony-next.skills.git
mkdir -p "$HOME/.agents/skills"
ln -s "$(pwd)/harmony-next.skills/harmony-next" "$HOME/.agents/skills/harmony-next"
```

如果要让团队在某个仓库里自动发现这个 skill，把 `harmony-next/` 复制或软链到目标仓库的 `$REPO_ROOT/.agents/skills/harmony-next`。Codex 会从当前工作目录向上扫描 `.agents/skills`。

入口文件：

- [`harmony-next/SKILL.md`](https://github.com/linhay/harmony-next.skills/blob/master/harmony-next/SKILL.md)
- [`harmony-next/references/INDEX.md`](https://github.com/linhay/harmony-next.skills/blob/master/harmony-next/references/INDEX.md)

## 版本重点

| 版本 | 重点变化 |
| --- | --- |
| `v1.3.7` | 新增可复制 HarmonyOS NEXT Empty Ability 最小测试工程模板：`references/templates/empty-ability-app`；默认 `com.example.emptyability` / `EntryAbility` / `5.0.0(12)`，补充 SDK 版本适配验证（含 `6.0.2(22)` / `DEVECO_SDK_HOME=/Applications/DevEco-Studio.app/Contents/sdk`）、`ohpm install`、`hvigorw --mode module`、HDC 启动、`uitest dumpLayout` 和 `uitest uiInput click` smoke 能力 |
| `Unreleased` | 新增 `ux_audit_pipeline.py` 一键离线 UI/UX 体检 CLI：先用 `doctor` 检查 `hdc`、`UxTestService` 和 Python 图像依赖，再执行 `capture-audit` 采集 layout/screenshot/log 证据、推断真实前台 bundle、运行 DevEco `UxTestService` 并输出 `summary.json`、`ux_summary.json`、`report.md`；真实模拟器 smoke 已产出 7 pass、1 issue、3 ignored 的报告 |
| `Unreleased` | 新增 `device_evidence_bundle.py` 设备调试证据包 CLI：定位 `hdc`、处理单/多 target、采集 boot 状态、debug bundle、`aa` 运行态、短 `hilog`、`uitest dumpLayout`、截图和 command ledger；真实模拟器 smoke 已采到 layout/screenshot/log 证据并输出 `summary.json` |
| `Unreleased` | 新增本地审计反馈机制：`device_evidence_bundle.py` 与 `ux_audit_pipeline.py` 的 JSON 输出包含 `feedback` 字段，`report.md` 追加反馈说明，并新增按场景拆分的 GitHub Issue 表单，指导用户脱敏提交 blocked、误判、版本不兼容和缺失工作流 |
| `Unreleased` | 新增 `profiler_trace_audit.py` 离线 Trace 性能证据审计脚本：定位 DevEco `trace_streamer`，将已有 `.ftrace/.htrace` / bytrace / rawtrace 转 SQLite，并输出 `summary.json`、top callstack、trace 元数据、frame slice 摘要和长 span 阈值命中；脚本拒绝把产物写入 `.app` 包内 |
| `Unreleased` | DevEco Emulator CLI 启动补充 trace socket 守护入口：`hvd_manager.py launch-preflight` 只输出带 `-t <trace-name>` 的命令计划，`hvd_manager.py launch` 创建 trace socket、detach Emulator 与 trace holder 后启动；启动前按 HVD `imageSubPath` 校验 emulator image root，区分 build SDK root 与 `~/Library/Huawei/Sdk`；启动失败/超时时返回退出码、日志路径、HDC 快照、HVD 运行态和稳定性检查等 machine-readable 诊断；首次运行许可协议提示会分类为 `license-agreement-required`，并提供显式 `--accept-license` opt-in；文档新增 attached 终端托管生命周期核查表，指导后续将终端结束与 `Emulator -stop` 清理绑定 |
| `Unreleased` | Release 产物改为 `harmony-next.skill.zip`，包内新增 `BUILD_INFO.json` 记录版本、release tag 与 git commit，并新增 `ISSUE_GUIDE.md` 指导 agent 复现、脱敏、分类和提交仓库 issue |
| `v1.3.6` | DevEco 模拟器 playbook 新增非交互自动化策略：用户默认拥有完整权限，`policy` 仅表示执行模式；支持 `readonly/evidence/automation/diagnostic/break-glass`、artifact 目录、脱敏元数据与 machine-readable blocked 输出 |
| `v1.3.5` | 新增 DevEco Studio IDE 私有未公开能力参考：CodeGenie 本地 RAG/MCP/LanceDB、`devecostudio://`、Previewer、ArkUI Inspector、Profiler、Doctor、UxTestService、插件入口索引与隐私风险门禁；更新 README 与触发词 |
| `v1.3.4` | 新增 DevEco Studio 模拟器私有未公开自动化参考：免 IDE 启动、`hdc + uitest`、HVD、多实例、风险门禁、超时与脱敏边界；更新 `SKILL.md` 触发词与任务索引 |
| `v1.2.0` | API 23 相关内容纳入当前更新；重建 `references/INDEX.md` 与 `JsEtsAPIReference/INDEX.md`；移除旧 `capi/headers/*.md` 页面并改为直链真实目标；新增 `reference_compat.py` 与链接回归审计能力；同步中英文 README 与维护说明 |

## 参考库维护

当 `references/JsEtsAPIReference/` 发生同步、迁移或批量改写后，建议按下面顺序执行：

```bash
python3 harmony-next/scripts/reference_compat.py generate
python3 harmony-next/scripts/reference_compat.py check
python3 harmony-next/scripts/reference_compat.py audit
python3 -m unittest discover -s harmony-next/tests -p 'test_*.py' -v
```

命令职责：

- `generate`
  - 把旧的 `../../capi/headers/*.md` 引用改写到真实 `topics/**/<header>.h.md`
  - 重建 `references/INDEX.md` 与 `references/JsEtsAPIReference/INDEX.md`
- `check`
  - 校验旧 `capi/headers/` 页面已删除
  - 校验索引与磁盘一致
  - 校验正文里没有残留旧路径引用
- `audit`
  - 扫描当前未提交改动
  - 找出“原本有内部 Markdown 链接、现在被改成纯文本”的残留问题
- `unittest`
  - 校验迁移脚本与审计逻辑没有回归

## 为什么值得接入

| 价值 | 说明 |
| --- | --- |
| 更少幻觉 | 回答基于真实文档路径，而不是模型记忆补全 |
| 更易追溯 | 每个答案都能落回具体 Markdown 文件 |
| 更适合自动化 | 有索引、有规则、有校验，适合长期接入 Agent 工作流 |

## Star 增长趋势

[![Star History Chart](https://api.star-history.com/svg?repos=linhay/harmony-next.skills&type=Date)](https://www.star-history.com/#linhay/harmony-next.skills&Date)

## 致谢

感谢 [LINUX DO](https://linux.do/)。

## 来源与许可

- 数据源：华为 HarmonyOS 官方文档
- 本仓库：为 AI 辅助开发工作流重新封装这些参考资料

英文说明见 [README_en.md](./README_en.md)。
