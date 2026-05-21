# Issue 12: Empty Ability 路由页与组件解耦

## 背景

GitHub issue #12 标题为“路由不对”，正文为“现在entry不能解耦，可以更新成组件吗”。问题指向 `empty-ability-app` 模板把 smoke UI、状态和点击逻辑直接写在 `pages/Index.ets` 中，复制到业务仓库后不利于替换路由页、接入导航结构或复用 smoke 组件。

## BDD 验收

### 场景 1：路由页只负责挂载组件

Given agent 复制 `harmony-next/references/templates/empty-ability-app`
When 打开 `entry/src/main/ets/pages/Index.ets`
Then `Index.ets` 保留 `@Entry` 页面入口
And 只挂载 `SmokeCounter()`
And 不再持有 smoke 状态字段

### 场景 2：smoke UI 可以独立复用

Given 目标项目需要复用模板的 smoke UI
When 打开 `entry/src/main/ets/components/SmokeCounter.ets`
Then 组件承载 `Harmony Smoke Ready`、`tapCount`、`smoke-title`、`smoke-counter`、`smoke-increment`
And 点击 `smoke-increment` 后仍更新为 `Harmony Smoke Tapped` / `tapCount=1`

### 场景 3：文档和测试同步描述结构

Given 后续维护者查看模板说明
When 阅读 README、skill 或 scaffold 文档
Then 能看到 `pages/Index.ets` 与 `components/SmokeCounter.ets` 的职责拆分
And 静态测试覆盖组件文件存在、入口页挂载和 smoke 节点 ID。

## 修改范围

- `harmony-next/references/templates/empty-ability-app/entry/src/main/ets/components/SmokeCounter.ets`：新增 smoke 组件。
- `harmony-next/references/templates/empty-ability-app/entry/src/main/ets/pages/Index.ets`：改为只导入并挂载 `SmokeCounter()`。
- `harmony-next/references/templates/empty-ability-app/README.md`：补充结构说明。
- `harmony-next/references/quickStart/ets/minimal-project-scaffold.md`：补充组件文件树、解耦说明和 smoke 节点来源。
- `harmony-next/SKILL.md`、`README.md`、`README_en.md`：同步最小工程入口说明。
- `harmony-next/tests/test_skill_metadata.py`：补充组件文件、入口页无 `@State`、组件保留 smoke 节点的回归测试。

## 验证

已执行：

```bash
python3 -m unittest harmony-next/tests/test_skill_metadata.py
python3 -m unittest discover -s harmony-next/tests -p 'test_*.py' -v
```

结果：

- 先补测试时，`test_empty_ability_template_is_copyable_for_smoke_tests` 因缺少 `components/SmokeCounter.ets` 失败，完成红灯确认。
- 实现后 targeted metadata 测试 9 项通过。
- 全量 unittest 32 项通过。

本次未做真实 DevEco / Hvigor 构建，因为改动是 ArkTS 模板静态结构拆分，当前仓库测试门禁覆盖模板文件、路由挂载、文档入口和敏感信息扫描。真实构建仍沿用 issue #11 已记录的 Empty Ability smoke 流程。
