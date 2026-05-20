# 给 AI 编程助手补一套 HarmonyOS NEXT 本地知识库

如果你最近让 AI 帮你写 HarmonyOS NEXT 代码，大概率遇到过同一个问题：模型很自信，但答案不一定落得回真实文档。

它可能会记错 `@ohos.*` 模块路径，混用旧版本 API，给出不存在的 ArkUI 参数，或者在 NDK、DevEco Studio、模拟器调试这些边界场景里凭经验补全。尤其是 DevEco 模拟器接口和 DevEco Studio IDE 接口，很多能力不在常规 API 手册里，只靠模型记忆很容易把路径、版本、私有协议和风险边界混在一起。

所以我整理了一个给 AI 编程助手使用的技能库：`harmony-next.skills`。

它不是给人从头翻的文档合集，而是给 Gemini CLI、Claude Code、Codex 这类 Agent 使用的 HarmonyOS NEXT 本地检索层。目标很直接：让 Agent 在回答之前先找到真实文档路径，再读取对应内容，最后基于可追溯的资料写代码、解释 API 或执行本地诊断。

项目地址：

<https://github.com/linhay/harmony-next.skills>

## 为什么需要这个库

HarmonyOS NEXT 开发里，很多问题看起来只是“查一下 API”，实际会牵出一串上下文：

- 这个能力属于哪个 Kit？
- 当前文档快照是否覆盖 API 23？
- `@ohos.*` 模块、ArkUI 组件、NDK 头文件是否真实存在？
- 旧文档链接是否已经迁移到新的 Markdown 页面？
- DevEco Studio、HarmonyOS Emulator、`hdc`、`uitest` 能不能在本机自动化验证？
- DevEco 模拟器的 HVD、target、截图、layout、日志链路该怎么被 Agent 安全调用？
- DevEco Studio IDE 里的 CodeGenie、MCP、Inspector、Profiler、Doctor 等能力该怎么先静态识别，再决定是否进入真实执行？
- AI 生成的代码到底是基于真实文档，还是基于模型记忆猜出来的？

`harmony-next.skills` 想解决的不是“把文档再复制一份”，而是把这些问题变成 Agent 能执行的检索流程。

它把 HarmonyOS NEXT API 12-23 的离线参考资料、Kit 导航、任务导航、全库索引、工具链说明和自动化边界组织在一起。Agent 不需要一上来全量读文档，也不需要凭关键词乱搜，而是按固定路径逐步缩小范围：

```text
SKILL.md
  -> KITS.md / TASK_MAP.md
  -> INDEX.md
  -> 目标 Markdown 正文
```

这套流程的核心只有一句话：先找路径，再读内容。

## 它和普通文档镜像有什么不同

普通文档镜像解决的是“离线能不能看”。`harmony-next.skills` 更关心另一个问题：AI Agent 能不能稳定使用。

所以它不只包含文档正文，还补了几层面向 Agent 的结构：

第一层是 `SKILL.md`。它告诉 Agent 什么时候应该使用这个技能，遇到 ArkTS、ArkUI、NDK、DevEco Studio、模拟器、`hdc`、`uitest` 等问题时该怎么路由。

第二层是 `KITS.md` 和 `TASK_MAP.md`。一个按 Kit 缩小范围，一个按开发任务反查关键词。比如你问生命周期、媒体、网络、UI、发布、NDK，不需要从几千个文件里盲搜。

第三层是全库索引。当前参考库包含 3,693 份 Markdown，其中 3,666 份在 `JsEtsAPIReference/` 下。Agent 会先命中路径，再打开少量目标文件读取细节。

第四层是验证与维护脚本。参考资料发生迁移或批量改写后，可以用脚本重建索引、检查旧路径残留、审计内部链接是否被误改成纯文本。

这让它更像一套 Agent 用的 HarmonyOS NEXT 知识基础设施，而不是静态资料包。

## 适合哪些场景

如果你主要用 AI 做 HarmonyOS NEXT 开发，这个库会在这些场景里很有用。

写 ArkTS / ArkUI 时，可以让 Agent 先确认组件、装饰器、状态管理、导航、UIAbility、Want 等 API 的真实位置和版本差异，再生成代码。

做 NDK / Node-API / C API 时，可以通过索引把头文件映射到真实的 `topics/**/<header>.h.md` 页面，避免旧路径、旧头文件和新文档结构混在一起。

排查工具链问题时，可以查签名、调试、发布、性能、模拟器、真机、`hdc`、`aa`、`bm`、`hilog`、`hidumper` 等本地链路，而不是让模型凭其他平台经验套答案。

DevEco 模拟器接口是这个库里很值得看的部分。它把免 IDE 启动 HarmonyOS Emulator、HVD 枚举、多实例、HDC target 选择、启动等待、`uitest dumpLayout`、截图、日志采集、应用安装启动这些动作整理成 Agent playbook。重点不只是列命令，而是把每个动作放进可审计的执行模式里：什么时候只做只读探测，什么时候可以保存截图和 layout，什么时候进入 UI 自动化，什么时候需要 diagnostic 或 break-glass 标记。

DevEco Studio IDE 接口也是一个单独亮点。库里整理了 CodeGenie、本地 RAG、MCP、LanceDB、`devecostudio://`、Previewer、ArkUI Inspector、Profiler、Doctor、Diagnostic、FaultLog、UxTestService 等入口线索。这里的处理方式比较克制：先确认版本和安装路径，默认做静态只读分析，不把私有接口包装成稳定公共 API；涉及 GUI、本地服务、设备连接、用户缓存、聊天历史、模型配置或外部 provider 时，必须明确目标、读取范围、产物目录和脱敏边界。

做自动化 smoke 时，可以复制内置的 Empty Ability 最小工程模板，用 `ohpm install`、`hvigorw --mode module`、HDC 安装启动、`uitest dumpLayout`、截图和点击事件完成最小验证。

如果你在研究 DevEco Studio 或 HarmonyOS Emulator 的本地能力，这两份 playbook 会比单纯搜索命令更有用。它们把“能不能做”“怎么做”“做完留下什么证据”“哪些内容不能泄露”放在一起，适合 Agent 长时间跑本地自动化时使用。

## 最近版本重点

当前本地版本是 `v1.3.7`。

这一版新增了可复制的 HarmonyOS NEXT Empty Ability 最小测试工程模板，和前面两份 DevEco playbook 正好能接起来。默认配置是：

- bundleName：`com.example.emptyability`
- module：`entry`
- ability：`EntryAbility`
- compatible SDK：`5.0.0(12)`
- target SDK：`5.0.0(12)`

它的价值不是“又多了一个 demo”，而是给 Agent 一个可以复制、构建、安装、启动、dump layout、点击验证的最小闭环。需要适配 API 22 等目标环境时，可以在复制出的 fixture 中覆盖 SDK 版本，例如 `6.0.2(22)`，并通过 `DEVECO_SDK_HOME=/Applications/DevEco-Studio.app/Contents/sdk` 指向本机 SDK 根目录。

也就是说，Agent 不只是会回答“应该怎么做”，还能在有设备或模拟器的环境里做一轮可回归的 smoke 验证。

## 怎么接入

Gemini CLI 可以直接安装：

```bash
gemini skills install https://github.com/linhay/harmony-next.skills --path harmony-next --scope user
```

Claude Code 可以下载仓库里的 `harmony-next/` 技能目录，放到对应技能目录里使用。也可以把它作为项目上下文附加：

```bash
git clone https://github.com/linhay/harmony-next.skills.git
claude --add-dir /path/to/harmony-next.skills/harmony-next
```

Codex 目前可以把 `harmony-next/` 放到官方 skill 扫描路径，例如：

```bash
git clone https://github.com/linhay/harmony-next.skills.git
mkdir -p "$HOME/.agents/skills"
ln -s "$(pwd)/harmony-next.skills/harmony-next" "$HOME/.agents/skills/harmony-next"
```

团队项目也可以把 `harmony-next/` 复制或软链到目标仓库的 `.agents/skills/harmony-next`，让项目内的 Agent 自动发现。

## 我希望它带来的变化

AI 编程助手真正有价值的地方，不是“更会编”，而是能进入一个可验证的工程流程。

在 HarmonyOS NEXT 这种快速演进的生态里，Agent 如果没有本地知识源，很容易把旧经验、旧 API、其他平台的模式和当前项目混在一起。短期看像是节省时间，长期看会增加排查成本。

`harmony-next.skills` 想把这件事往前推一步：让 Agent 先检索、再引用、再实现、最后验证。

如果你正在用 AI 写 HarmonyOS NEXT 应用，或者正在搭自己的 Agent 开发工作流，可以把这个库接进去试试。它不替代官方文档，也不替代工程判断，但它能让 AI 的回答更少凭空补全，更容易追溯，也更适合放进长期维护的开发链路里。

项目地址：

<https://github.com/linhay/harmony-next.skills>
