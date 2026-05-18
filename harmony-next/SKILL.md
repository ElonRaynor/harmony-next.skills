---
name: harmony-next
description: HarmonyOS NEXT（以 API 12-23 为主）离线参考库导航：按 Kit/任务/索引渐进式定位文档（ArkTS/ArkUI/NDK）；触发 DevEco Studio / HarmonyOS Emulator / HVD / hdc / uitest / aa / bm / hilog / hidumper / 免 IDE 启动 / 私有未公开接口自动化任务。
---

# HarmonyOS NEXT（离线文档导航）

目标：在不盲读 `references/` 的前提下，快速定位到 1 个或少量目标 Markdown，然后只打开这些文件。

## 渐进式披露（按顺序走）

1. **先缩小范围（选 Kit 或任务）**
   - Kit 导航：`references/KITS.md`
   - 任务导向：`references/TASK_MAP.md`

2. **再精确命中文件（搜路径清单）**
   - 全库路径清单：`references/INDEX.md`
   - JS/ETS API 分桶清单：`references/JsEtsAPIReference/INDEX.md`

3. **仅在必要时浏览目录**
   `references/JsEtsAPIReference/` 目前以 `modules/`、`topics/`、`types/`、`errors/`、`guides/` 为主。
   - `guides/` 下同时包含一部分从官方在线 guide 整理出的离线入口页，用于承接仓库内原本只指向官网的高频说明文档。

## 常用检索（直接复制用）

- 先按关键词命中路径：`rg -n "UIAbility|AbilityStage|Want" references/INDEX.md | head`
- 查某个 `@ohos.*` 模块：`rg -n "@ohos\\.app\\.ability\\.|@ohos\\.ability\\." references/INDEX.md | rg "JsEtsAPIReference/" | head`
- 查 NDK/C API 头文件：`rg -n "JsEtsAPIReference/topics/.*/.*\\.h\\.md$" references/INDEX.md | rg "(napi|arkui|window|ability)" | head`

## 私有未公开接口：DevEco 模拟器自动化

这一章只适用于“免 IDE 启动 DevEco Studio 模拟器、用 AI/命令行操作 HarmonyOS Emulator、排查 hdc/uitest/aa/bm/hilog/hidumper 自动化链路”等任务。

先读 `references/ideGuides/DevEco模拟器私有接口与AI自动化.md`。该页来自本地验证结论，不属于稳定公开 API；任何命令、参数、路径和输出字段都可能随 DevEco Studio / Emulator 版本变化。执行前必须先验证当前机器版本与能力，不要把旧结论当作长期契约。

默认边界：

- 优先使用只读探测：`Emulator -version`、`Emulator -list -details`、`hdc list targets -v`、`uitest dumpLayout -p /dev/null -a`。
- UI 操作优先走 `hdc -t <target> shell uitest uiInput`，不要默认使用桌面坐标点击。
- 真实截图、layout、日志包、`file recv`、安装/卸载、创建/删除 HVD、端口转发、底层 `uinput`、`hitrace` 都需要用户确认和脱敏策略。
- 多 target 时必须显式选择 `127.0.0.1:<port>`；只选择 `Connected`，忽略 `Offline`。
- 不能分类的命令按 `require_confirm` 处理；刷写、格式化、清数据、root/daemon 模式等系统级命令默认禁止。

## 生成约束（避免踩坑）

- **不要全量读取**：先在 `INDEX.md` 命中路径，再打开对应 `.md`。
- **不确定就查文档**：API 签名、入参、返回值以 `references/` 内文本为准，不凭经验补全。
- **ArkUI 优先声明式**：示例优先使用 `@Entry` / `@Component` / `build()`（除非文档明确是 NDK 或系统服务）。
- **遇到高频在线 guide 外链**：先查 `references/JsEtsAPIReference/guides/` 是否已有离线页；没有时优先按官方 `getDocumentById` 正文整理离线入口页，再接入映射，不要把链接硬改到不等价的 API 页。

<!-- version: 1.3.4 -->
