# Ponytail 借鉴方案 Space

日期：2026-07-06

## 目标

研究 `DietrichGebert/ponytail` 的 agent 技能产品化方式，并规划哪些做法适合迁移到 `harmony-next.skills`。重点不是复刻 Ponytail 的“懒人模式”，而是借鉴它把一套规则稳定分发到多类 agent 的工程方法。

## 边界

- 不引入常驻模式、状态栏、生命周期 hook，除非后续确认 HarmonyOS skill 需要跨回合强制注入。
- 不把 `harmony-next/SKILL.md` 拆成多个 skill，除非先证明大 skill 的上下文成本或误触发已经影响使用。
- 不新增 Node/npm 发布链路；当前仓库已有 Python 脚本和 `npx skills` 安装路径，优先复用。
- 不用宣传性 benchmark；只做能复现的 agent 正确率、文档命中率和验证命令覆盖率评估。

## Ponytail 可借鉴点

| 做法 | Ponytail 形态 | 本项目对应方案 | 优先级 |
| --- | --- | --- | --- |
| 单一权威规则源 | `skills/ponytail/SKILL.md` + `AGENTS.md` | 明确 `harmony-next/SKILL.md` 是权威源，README 只做入口说明 | P0 |
| 多平台薄适配器 | Codex/Claude/OpenCode/Gemini/Copilot adapter | 增加 `docs/agent-portability.md`，列出现有安装/读取路径 | P0 |
| 防副本漂移 | `scripts/check-rule-copies.js` | 增加轻量校验：README、README_en、SKILL 版本和安装命令一致 | P0 |
| 小技能/小命令 | `ponytail-review/audit/debt/help/gain` | 先用文档入口分区，不急拆 skill；必要时再拆 API/Emulator/UX/Trace | P1 |
| 可反驳 benchmark | agentic benchmark + 安全 scorer | 建 10 个 HarmonyOS 高频问题 smoke set，测文档命中与答案可验证性 | P1 |
| Before/After 叙事 | 原生 input 替代自定义组件 | README 增加“无 skill 猜 API / 有 skill 命中本地文档”短例 | P2 |

## 方案分期

状态：Phase 1-4 已落地为文档、校验脚本和 smoke set；后续只在 smoke 结果证明需要时再拆 skill。

### Phase 1：入口一致性

目标：让安装、版本、入口说明不漂移。

产物：

- 已完成：`docs/agent-portability.md` 列出 Gemini CLI、Claude Code、Codex、skills.sh、手动安装、Claude.ai 上传包的当前支持形态。
- 已完成：`harmony-next/scripts/check_packaging_docs.py` 校验 `metadata.version`、README/README_en 命令片段、portability 文档和 smoke-set 路径。
- 已完成：`harmony-next/tests/test_packaging_docs.py` 接入 unittest。

验收：

```bash
python3 harmony-next/scripts/check_packaging_docs.py
python3 -m unittest discover -s harmony-next/tests -p 'test_*.py' -v
```

### Phase 2：检索质量 smoke set

目标：证明 skill 的价值是“先命中文档，再回答”，不是模型记忆。

产物：

- 已完成：`docs-linhay/spaces/20260706-ponytail-portability-plan/smoke-set.md` 记录 10 个固定问题，覆盖 ArkUI、Ability/Want、Network、Data、NDK、测试/发布安全、HVD、UxTestService、Profiler trace、Command Line Tools。
- 每题记录：期望命中的索引路径、必须打开的目标文档、答案必须包含的验证命令。
- 已完成：`check_packaging_docs.py` 逐题检查标题、目标 Markdown 路径和关键验证片段，不做 LLM 自动评分。

验收：

- 每题能在 `references/INDEX.md` 或专题文档中定位到 1-3 个目标文件。
- 每题有可执行或明确 blocked 的验证路径。

### Phase 3：README 产品化

目标：降低新用户理解成本。

产物：

- 已完成：README/README_en 增加短 Before/After。
- 已完成：README/README_en 增加 `docs/agent-portability.md` 入口，并把漂移检查加入维护命令。
- 把高风险私有接口说明保留，但压缩到入口摘要，细节仍指向 playbook。

验收：

- README 首屏能回答：这是什么、解决什么、怎么装、从哪里查。
- 私有接口边界没有弱化。

### Phase 4：是否拆 skill 的决策

目标：只在有证据时拆分。

触发条件：

- agent 经常因为普通 API 查询误读 DevEco 私有接口章节。
- `SKILL.md` 继续增长，导致一次任务需要加载大量无关边界。
- 用户明确希望只安装某个子能力，例如 UX audit 或 Emulator automation。

候选拆法：

- `harmony-next-api-lookup`
- `harmony-next-emulator`
- `harmony-next-deveco-ide`
- `harmony-next-ux-audit`
- `harmony-next-trace-audit`

当前结论：先不拆。决策记录见 `split-decision.md`；用 smoke set 找证据。

## 不做清单

- 不搬 Ponytail 的 `ponytail-activate.js`、mode tracker、statusline。
- 不为每个平台复制一份大段规则文本。
- 不新增 npm package，仅为了“看起来像插件”。
- 不做无法复现的 star/效率宣传图。

## 已落地产物

- `docs/agent-portability.md`
- `harmony-next/scripts/check_packaging_docs.py`
- `harmony-next/tests/test_packaging_docs.py`
- `docs-linhay/spaces/20260706-ponytail-portability-plan/smoke-set.md`
- `docs-linhay/spaces/20260706-ponytail-portability-plan/split-decision.md`

## 后续触发

只有 smoke set 显示普通 API 查询误触发私有接口、上下文成本明显升高，或用户明确需要单独安装子能力时，才进入拆 skill 实施。
