# Issue 10: DevEco Emulator 非交互自动化策略

## 背景

GitHub issue #10 要求 DevEco Emulator 自动化不要把高风险动作绑定到人工确认。用户明确补充：skill 不需要授权，用户拥有最大权限，想怎么使用就怎么使用。

因此本次调整采用以下边界：

1. `riskLevel` 只描述敏感度和影响面。
2. `policy` 只描述执行模式、产物目录和脱敏契约，不代表授权。
3. skill 不向用户索要许可，也不把高风险动作改写成等待输入。
4. machine-readable `blocked` 只用于缺少 target、artifactDir、redactionPolicy、timeout、命令参数等客观前置条件。
5. `break-glass` 是系统级动作风险标签，不是授权门槛。

## BDD 验收

### 场景 1：长时间自动化采集证据

Given run 配置提供 `policy=evidence`、`artifactDir`、`redactionPolicy` 和明确 target  
When agent 采集真实截图、layout、日志片段或 `file recv`  
Then playbook 不要求人工确认  
And gate 记录 `riskLevel`、`policy`、`operation`、`target`、`artifacts`、`redactionStatus`、`sourceCommand`

### 场景 2：缺少运行配置

Given run 缺少 target、artifactDir、redactionPolicy 或 timeout  
When agent 准备执行需要这些配置的动作  
Then 返回 machine-readable `blocked`  
And 结果包含 `missingConfig` 与 `requiredMode`  
And 原因不是权限不足

### 场景 3：系统级动作

Given 用户明确目标为刷写、格式化、清数据、root/daemon 或通配删除  
When agent 执行该类动作  
Then playbook 将其标记为 `break-glass`  
And 要求记录目标、命令摘要、恢复策略和审计摘要  
And 不把 `break-glass` 作为授权拦截

## 修改范围

- `harmony-next/SKILL.md`：更新 DevEco Emulator 默认边界，声明用户默认拥有完整执行权限。
- `harmony-next/references/ideGuides/DevEco模拟器私有接口与AI自动化.md`：新增自动化策略模型，移除人工确认语义。
- `README.md` / `README_en.md`：补充非交互自动化策略说明。
- `harmony-next/tests/test_skill_metadata.py`：增加文档契约测试，防止回退到授权 gate 语义。

## 验证

已执行：

```bash
python3 -m unittest discover -s harmony-next/tests -p 'test_*.py' -v
```

结果：14 个测试通过。
