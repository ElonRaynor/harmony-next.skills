# Skill Split Decision

日期：2026-07-06

结论：当前不拆分 `harmony-next` skill。

## 理由

- `harmony-next/SKILL.md` 已经有路由规则：普通 API 查询走 `KITS.md` / `TASK_MAP.md` / `INDEX.md`，DevEco 私有接口只在触发词出现时读取。
- 自动化脚本已经是独立入口，用户不需要安装多个 skill 才能使用 HVD、UX audit 或 trace audit。
- 现有风险不是“子能力不够独立”，而是 README、安装路径、版本和 smoke 验证容易漂移。Phase 1-3 先解决这个。

## 拆分触发条件

只有出现以下证据时再拆：

- 普通 API 问题反复误加载 DevEco 私有接口章节。
- `SKILL.md` 继续增长，导致一次任务需要读大量无关边界。
- 用户明确只想安装单一能力，例如 UX audit、Emulator automation 或 trace audit。

## 候选拆法

- `harmony-next-api-lookup`
- `harmony-next-emulator`
- `harmony-next-deveco-ide`
- `harmony-next-ux-audit`
- `harmony-next-trace-audit`

下一步：用 `smoke-set.md` 的 10 题观察误触发和上下文成本，再决定是否拆。
