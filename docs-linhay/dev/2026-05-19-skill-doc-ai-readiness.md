# Skill 文档 AI 可用性核对

## 背景

近期新增的 DevEco Studio / Emulator 私有接口资料包含大量本地验证结论。核对后确认：这类内容如果直接以调研报告或团队过程记录呈现，agent 读取后不容易判断触发场景、默认动作、确认边界和输出要求。

## 验收场景

- 当用户询问 HarmonyOS NEXT API 或 DevEco 自动化时，`harmony-next/SKILL.md` 能先引导 agent 做路由，而不是全量读取参考目录。
- 当用户要求 DevEco Emulator 自动化时，参考页能给出 agent 可执行的只读探测、确认动作、禁止动作、超时和脱敏规则。
- 当用户要求 DevEco Studio IDE 私有接口分析时，参考页能给出静态分析优先、用户数据保护、CodeGenie/MCP/LanceDB 风险边界和输出格式。

## 调整结论

- `harmony-next/SKILL.md` 改为 agent guide：收紧 description，强调请求分类、最小索引、目标文件读取和私有接口 playbook。
- `references/ideGuides/DevEco模拟器私有接口与AI自动化.md` 改为 Emulator automation playbook：按触发场景、风险分级、启动模板、UI 自动化、诊断、超时和脱敏组织。
- `references/ideGuides/DevEco Studio IDE私有接口与AI自动化.md` 改为 IDE private-interface playbook：按触发场景、风险分级、命令入口、私有协议、CodeGenie/MCP/LanceDB、插件入口和隐私输出组织。

## 后续准则

新增或修改 skill 文档时，优先回答四个问题：

1. 什么时候触发这个 skill？
2. agent 首先读什么、运行什么、避免读什么？
3. 哪些动作默认允许、需要确认、默认禁止？
4. 最终应该向用户输出什么，哪些敏感内容不能输出？

## 版本与安装信息补充

### 验收场景

- 当用户或 Agent 打开 `harmony-next/SKILL.md` 时，可以直接看到当前技能包版本，而不是只能从 README 或隐藏注释推断。
- 当用户询问“本地文档和在线文档是否有差距”时，Agent 能判断该技能包是离线快照，并知道需要对比 GitHub Releases、nightly 包或华为在线文档。
- 当用户需要更新技能包时，Agent 能在 `SKILL.md` 中找到 Gemini CLI、Claude/Claude Code、Codex 的安装或更新入口。

### 设计结论

- 版本、快照边界和安装信息属于 Agent 触发后的核心判断信息，应放入 `harmony-next/SKILL.md` 主体，不拆成额外安装文档。
- README 继续作为面向人的完整说明；`SKILL.md` 只保留执行时必需的最小信息。
- 新增测试约束 `SKILL.md` 必须包含显式版本、离线快照边界、在线 freshness 检查入口和三类 Agent 安装方式。
- 为符合渐进式披露，版本同时写入 frontmatter `metadata.version`，正文只保留最小的版本、快照边界、freshness 判断和安装入口，不复制 README 的完整安装说明。

### CI 版本同步

- 新增 `harmony-next/scripts/sync_release_version.py` 作为版本同步单一执行入口。
- GitHub Actions 发布流程在打包前解析 tag 或 `workflow_dispatch.inputs.version`，自动同步 `SKILL.md` 的 `metadata.version`、正文版本、隐藏版本，以及中英文 README 的 release badge/link。
- 发布前固定运行 `python3 -m unittest discover -s harmony-next/tests -p 'test_*.py' -v`，避免版本元信息不同步时继续生成 `.skill` 产物。
- `master` 每次 push 默认读取最新 `vX.Y.Z` tag 并自动递增 patch 版本发稳定 release；tag 发布和手动指定版本发布会按目标版本重写打包工作区内的元信息。

## Subagent 体验反馈修正

使用三个 subagent 分别体验 `SKILL.md`、Emulator playbook 和 IDE playbook 后，保留以下修正：

- `SKILL.md` 增加路径上下文说明：`references/...` 相对 `harmony-next/`，从仓库根目录执行时需加前缀或先 `cd harmony-next`。
- `SKILL.md` 增加排他路由：普通 API/组件/错误码查询不读取 DevEco playbook；只有命中 IDE/Emulator/hdc 等意图时才进入对应 playbook。
- Emulator playbook 增加最小只读探测流程、`trace-name` 处理规则、失败分流、坐标来源优先级和确认请求模板。
- IDE playbook 收紧隐私边界：`strings/rg` 命中敏感字段不得原样回传，用户侧目录默认只报告存在性/数量/类型分布，读取 MCP/model provider 配置正文需确认。
- IDE playbook 扩展输出格式，要求列出已执行/已跳过动作、确认需求、脱敏方式和证据等级。
