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
