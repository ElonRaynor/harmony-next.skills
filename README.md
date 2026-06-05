# HarmonyOS NEXT 开发者专家技能包

给 Gemini CLI、Claude Code、Codex 等 AI 编程助手使用的 HarmonyOS NEXT 离线参考技能库。

语言：中文 | [English](./README_en.md)

[![release](https://img.shields.io/badge/release-v1.3.7-1f6feb?style=flat-square)](https://github.com/linhay/harmony-next.skills/releases/tag/v1.3.7)
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
| DevEco IDE 私有接口 | CodeGenie、本地 RAG/MCP、`devecostudio://`、Previewer、ArkUI Inspector、Profiler、Doctor、UxTestService 的静态验证边界 | [`DevEco Studio IDE私有接口与AI自动化.md`](./harmony-next/references/ideGuides/DevEco%20Studio%20IDE私有接口与AI自动化.md) |
| 命令行工具配置 | Command Line Tools 直链下载、本地压缩包安装、PATH 配置和 `codelinter -v` 校验 | [`commandline_tools_manager.py`](./harmony-next/scripts/commandline_tools_manager.py) |
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
- DevEco Studio / HarmonyOS Emulator 免 IDE 启动、HVD、多实例、`hdc`、`uitest`、`aa`、`bm`、`hilog`、`hidumper` 自动化诊断
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
- 本仓库提供 `python3 harmony-next/scripts/hvd_manager.py`：支持 `doctor` 环境探测、`list`、`create`、`delete`、`launch-preflight` 和 `launch`。
- HVD 启动适配：`--root` / `HARMONY_HVD_ROOT` 指定 HVD root，`--emulator` / `HARMONY_EMULATOR` 指定 Emulator，`--image-root` / `HARMONY_EMULATOR_IMAGE_ROOT` 指定模拟器镜像根，`--hdc` / `HARMONY_HDC` 指定 HDC。`--sdk-root` / `DEVECO_SDK_HOME` 只表示 DevEco build SDK root，不等同于模拟器镜像根。
- macOS 常见镜像根是 `~/Library/Huawei/Sdk`；脚本会用 HVD `imageSubPath` 校验系统镜像。`launch` 会 detach Emulator 与 trace holder，等待 HDC、boot 和稳定性检查；`download-image` 当前只返回 blocked，因为镜像下载仅确认到 IDE SDK Manager UI 入口。
- 模拟器抓包与代理诊断：Charles、mitmproxy、Proxyman 等抓包工具都需要确认模拟器 NAT、宿主机可达地址和应用级代理。常见调试入口是让目标应用显式走 `10.0.2.2:9090`，例如 `setAppHttpProxy` 配合 `usingProxy: true`；Mac 侧中转脚本不能被描述为通用透明抓包方案。

### DevEco Studio IDE 私有接口

这部分属于私有未公开接口，触发词包括：`DevEco Studio IDE`、`CodeGenie`、`MCP`、`LanceDB`、`devecostudio://`、`inspect.sh`、`format.sh`、`ltedit.sh`、`ArkUI Inspector`、`Previewer`、`Profiler`、`Doctor`、`Diagnostic`、`FaultLog`、`UxTestService`、`Application Agent`、`Operation Analyzer`、`Cloud Toolkit`。

使用规则：

- 先读 [`harmony-next/SKILL.md`](./harmony-next/SKILL.md) 的 IDE 私有接口章节，再读 [`DevEco Studio IDE私有接口与AI自动化.md`](./harmony-next/references/ideGuides/DevEco%20Studio%20IDE私有接口与AI自动化.md)。
- 默认只做静态只读分析：插件 XML、jar 类名、字符串、配置路径、离线 `.htrace` / faultlog / stacktrace / `.arkli` / `.preview` 产物。
- 启动 IDE/GUI/JCEF、本地服务、设备连接、CodeGenie localhost 接口、MCP 配置、外部模型请求、读取用户缓存或聊天历史时，记录目标、输入、产物目录和脱敏边界。

### Agent 工程化集成

- Gemini CLI、Claude Code、Codex
- 本地知识库检索层
- 避免幻觉、提升可追踪性与可复现性

## 快速接入

### Gemini CLI

```bash
gemini skills install https://github.com/linhay/harmony-next.skills --path harmony-next --scope user
```

### Claude Code

1. 下载本仓库中的技能目录。
2. 按需压缩技能文件夹。
3. 在 Claude.ai 的 `Settings > Capabilities > Skills` 中上传。
4. 或直接放进你的 Claude Code 技能目录。

如果你只是想把仓库作为项目上下文附加：

```bash
git clone https://github.com/linhay/harmony-next.skills.git
claude --add-dir /path/to/harmony-next.skills/harmony-next
```

### Codex

官方 Codex Agent Skills 文档说明：skill 是可复用工作流的创作格式；直接 skill 目录用于本地创作与发现；可安装分发单元是 Codex plugin。

官方文档：<https://developers.openai.com/codex/skills>

本仓库当前还没有打包成 Codex plugin，因此 Codex 的官方接入方式是放入官方 skill 扫描路径。

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
| `Unreleased` | DevEco Emulator CLI 启动补充 trace socket 守护入口：`hvd_manager.py launch-preflight` 只输出带 `-t <trace-name>` 的命令计划，`hvd_manager.py launch` 创建 trace socket、detach Emulator 与 trace holder 后启动；启动前按 HVD `imageSubPath` 校验 emulator image root，区分 build SDK root 与 `~/Library/Huawei/Sdk`；启动失败/超时时返回退出码、日志路径、HDC 快照、HVD 运行态和稳定性检查等 machine-readable 诊断 |
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

## 来源与许可

- 数据源：华为 HarmonyOS 官方文档
- 本仓库：为 AI 辅助开发工作流重新封装这些参考资料

英文说明见 [README_en.md](./README_en.md)。
