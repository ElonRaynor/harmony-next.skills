# Issue 11: Empty Ability 最小测试工程模板

## 背景

GitHub issue #11 要求提供一个无需打开 DevEco Studio 向导即可复制的 HarmonyOS NEXT 最小测试工程模板，用于 HDC、Emulator、`uitest dumpLayout`、截图和日志 smoke。

本次模板以本机 DevEco Studio 官方 `New Project` 与 `Empty Ability` 模板为结构来源，保留 Stage 模型、`EntryAbility`、`pages/Index`、`main_pages.json` 和基本资源文件，删除本机签名材料、IDE 缓存、绝对路径和 Freemarker 向导占位符。

## BDD 验收

### 场景 1：agent 复制最小工程

Given agent 需要在任意仓库生成 HarmonyOS NEXT smoke fixture
When 复制 `harmony-next/references/templates/empty-ability-app`
Then 目标目录包含可构建的 app/module/build/resource 基础结构
And 默认 `bundleName` 为 `com.example.emptyability`
And 默认 module 为 `entry`、ability 为 `EntryAbility`

### 场景 2：自动化 smoke 可定位 UI

Given 工程安装并启动到 Emulator
When agent 执行 `uitest dumpLayout` 或截图采集
Then 页面暴露 `Harmony Smoke Ready` 文本
And 暴露稳定节点 ID：`smoke-title`、`smoke-counter`、`smoke-increment`

### 场景 3：模板不携带本机敏感材料

Given 模板被提交到 skill 仓库
When 扫描模板文件
Then 不包含 `/Users/` 绝对路径、`${...}` 向导占位符、`certpath`、`storePassword` 或 `keyPassword`

## 修改范围

- `harmony-next/references/templates/empty-ability-app/`：新增可复制 Empty Ability 最小工程模板。
- `harmony-next/references/quickStart/ets/minimal-project-scaffold.md`：新增复制、构建、HDC 启动和 `uitest` smoke 指南。
- `harmony-next/SKILL.md`：新增 minimal scaffold 路由和使用入口。
- `README.md` / `README_en.md`：新增模板入口与 `v1.3.7` 变更说明。
- `harmony-next/tests/test_skill_metadata.py`：新增模板结构、默认参数、文档入口和敏感材料回归测试。

## 验证

已执行：

```bash
python3 harmony-next/scripts/reference_compat.py check
python3 harmony-next/scripts/reference_compat.py audit
python3 -m unittest discover -s harmony-next/tests -p 'test_*.py' -v
python3 -m unittest harmony-next/tests/test_skill_metadata.py -v
git diff --check
/Applications/DevEco-Studio.app/Contents/tools/ohpm/bin/ohpm install
```

结果：

- reference check/audit 通过。
- 全量 unittest 15 个测试通过。
- targeted metadata unittest 8 个测试通过。
- `git diff --check` 无输出。
- 模板副本 `ohpm install` 通过。

Hvigor 构建验证在本机被环境阻塞：当前 DevEco Studio SDK 为 HarmonyOS 6.0.2 / API 22，模板默认 `5.0.0(12)`，运行 `hvigorw --mode module -p module=entry@default assembleHap` 报 `SDK component missing`。这说明本机缺少 API 12 SDK 组件，未发现模板文件结构或 JSON 解析问题。
