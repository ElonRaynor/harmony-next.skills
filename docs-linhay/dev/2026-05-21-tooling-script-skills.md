# 工具脚本型 skill 整理

## 背景

本轮新增了两类可复用命令行能力：

- HarmonyOS Command Line Tools 下载、安装、profile 配置和 doctor 校验。
- DevEco HVD 本地实例探测、克隆、删除和环境适配。

如果只把这些能力写在 README 或单个 playbook 中，Agent 在后续会话里容易遗漏脚本入口，继续手写不稳定路径或误判下载中心页面可以直接下载。因此将它们整理为 `harmony-next/SKILL.md` 中的工具脚本型 skill 入口。

## 验收场景

- 用户询问 Command Line Tools 下载、安装、配置、`codelinter -v` 校验时，Agent 能优先使用 `commandline_tools_manager.py`。
- 用户询问 HVD 列表、新建、删除、模拟器环境适配时，Agent 能优先使用 `hvd_manager.py doctor --json` 做跨机器探测。
- 用户提供华为下载中心页面 URL 时，Agent 不尝试绕过登录态，而是返回 blocked 边界并要求用户登录后复制压缩包直链或提供本地 archive。
- 用户要求下载 HVD 镜像时，Agent 能明确 `download-image` 当前只返回 blocked，稳定非 UI 下载入口尚未验证。

## 调整

- `harmony-next/SKILL.md` 新增 `Tooling Script Skills`，把 `commandline_tools_manager.py` 和 `hvd_manager.py` 作为两个脚本型 skill 入口整理。
- `DevEco模拟器私有接口与AI自动化.md` 的 HVD CLI 段落补充跨机器分发规则：先运行 `doctor --json`，再根据 `issues` / `recommendations` 补路径参数或环境变量。
- `命令行工具指南.md` 更新模拟器段落：官方 `Emulator` 命令未验证到稳定创建入口，仓库 `hvd_manager.py create` 是基于已有同版本实例的受控克隆。
- `test_skill_metadata.py` 新增回归测试，约束 skill 文档必须保留两个工具脚本入口、首选命令和 blocked 边界。

## 验证

```bash
python3 -m unittest harmony-next/tests/test_skill_metadata.py
```

结果：9 个测试通过。
