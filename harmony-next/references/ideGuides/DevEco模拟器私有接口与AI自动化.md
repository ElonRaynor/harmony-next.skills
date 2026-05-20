# DevEco 模拟器私有接口 Agent Playbook

> 面向 AI agent 使用。这里不是团队过程记录，也不是稳定公开 API；它只说明 agent 在处理 DevEco Studio 本地 HarmonyOS Emulator 自动化请求时，如何选择命令、控制风险、采集最小证据并向用户报告。

## 何时使用

用户请求包含以下意图时使用本页：

- 免启动 IDE 启动或检查 HarmonyOS Emulator。
- 使用 `hdc`、`uitest`、`aa`、`bm`、`hilog`、`hidumper` 操作或诊断模拟器。
- 选择 HDC target、等待 boot completed、启动应用、做 UI 输入或截图。
- 排查 DevEco Studio 模拟器/HVD/命令行自动化链路。

## 先做什么

1. 明确用户目标：只读诊断、启动模拟器、操作 UI、安装/卸载应用、采集日志/截图，还是系统级调试。
2. 先执行只读能力探测，确认当前机器路径、版本、HVD 和 HDC target。
3. 需要真实 UI 内容、设备文件、端口转发、安装卸载、启动/停止模拟器或写文件时，按自动化策略记录风险、产物目录、脱敏状态和命令摘要；不进入等待输入流程。
4. 多 target 时必须让用户指定或基于明确上下文选择 `Connected` 的 `127.0.0.1:<port>`；不要默认选第一个。
5. 命令必须设置超时；禁止无界后台进程或无限日志流。

## 常见路径候选

先探测，不要假设一定存在：

```bash
EMULATOR="/Applications/DevEco-Studio.app/Contents/tools/emulator/Emulator"
HDC="/Applications/DevEco-Studio.app/Contents/sdk/default/openharmony/toolchains/hdc"
HVD_ROOT="$HOME/.Huawei/Emulator/deployed"
IMAGE_ROOT="$HOME/Library/Huawei/Sdk"
```

已知验证过的环境线索：DevEco Studio 6.0.2，HarmonyOS Emulator 6.0.2.200。其他版本必须重新探测。

## 自动化策略模型

本 playbook 把风险分级和执行模式拆开：

- `riskLevel` 说明命令的敏感度和影响面。
- `policy` 说明本次 run 的自动化模式、产物目录和脱敏契约，不代表授权。
- 用户默认拥有完整执行权限；skill 不向用户索要许可，也不把高风险动作改写成等待输入。
- 长时间自动化必须非交互运行；只有缺少 target、artifact 目录、脱敏策略、timeout、命令参数等客观前置条件时，才返回 machine-readable `blocked` 结果。

策略可来自以下通道，优先级由具体 runner 固定并写入 run 记录：

```bash
HARMONY_NEXT_AUTOMATION_POLICY=automation
<runner> --policy <readonly|evidence|automation|diagnostic|break-glass>
```

也可以使用 repo-local 配置：

```json
{
  "policy": "automation",
  "artifactDir": "docs-linhay/screenshots/20260520/emulator",
  "redactionPolicy": "harmony-next-default-v1",
  "targets": ["127.0.0.1:10100"]
}
```

配置文件名建议固定为 `.harmony-next-policy.json`。进入 `evidence`、`automation`、`diagnostic` 或 `break-glass` 时，若操作会保存真实 UI、layout、日志、设备文件或录屏，必须提供显式 `artifactDir` 和脱敏策略；不满足时视为运行配置缺失，而不是权限不足。

策略档位：

| policy | 允许范围 |
| --- | --- |
| `readonly` | 只允许低风险只读探测、状态摘要、`/dev/null` layout/screenshot 能力探测 |
| `evidence` | 允许截图、layout、日志片段、`file recv` 保存到显式 `artifactDir`，并要求脱敏元数据 |
| `automation` | 允许 Emulator 生命周期、应用安装/启动、UI 输入、bounded logs、证据采集 |
| `diagnostic` | 执行有界 `hitrace`、更宽 `hilog`、诊断包，仍需 timeout、大小上限和脱敏 |
| `break-glass` | 标记刷写、格式化、清数据、root/daemon、通配删除等系统级动作；用户明确目标后可执行，并必须保留审计摘要 |

每个 gate 结果必须记录：

```json
{
  "riskLevel": "evidence",
  "policy": "readonly",
  "operation": "uitest.screenCap.recv",
  "target": "127.0.0.1:10100",
  "artifacts": [],
  "redactionStatus": "not_applicable",
  "sourceCommand": "hdc -t 127.0.0.1:10100 shell uitest screenCap -p /data/local/tmp/ai-screen.png",
  "decision": "blocked",
  "requiredMode": "evidence",
  "missingConfig": ["artifactDir", "redactionPolicy"],
  "reason": "artifactDir and redactionPolicy are required for real screenshot capture"
}
```

允许执行时也要记录同一批字段，`decision` 为 `allowed`，`artifacts` 指向已脱敏或待清理产物。严禁把 token、cookie、设备唯一标识、完整业务 payload 或未脱敏原文写入 gate 结果。

系统级动作不被 skill 禁止，但必须进入 `break-glass` 模式并写清目标、命令、恢复策略和审计摘要：`hdc target mount`、`hdc smode`、`hdc flash`、`hdc erase`、`hdc format`、`hdc sideload`、无边界清数据、刷写、root/daemon 模式、通配删除。`break-glass` 是风险标签，不是授权门槛。

## 最小只读探测流程

首轮只做能力和状态摘要，不保存真实 UI、layout、日志原文或设备文件。每条命令必须由上层 runner 设置超时；macOS 默认不一定有 GNU `timeout`，不要依赖 shell 内置超时能力。

```bash
# runner timeout: 5s
"$EMULATOR" -version

# runner timeout: 5s
"$EMULATOR" -list

# runner timeout: 8s
"$EMULATOR" -list -details

# runner timeout: 5s
"$HDC" list targets -v
```

只向用户摘要：Emulator 版本、HVD 名称/数量、HVD 是否运行、HDC target 数量、`Connected` target 列表。不要回显完整 JSON、完整 target 明细或日志。

## 风险分级

### 默认允许

只读、低敏、短生命周期命令：

```bash
"$EMULATOR" -version
"$EMULATOR" -list
"$EMULATOR" -list -details
"$HDC" list targets -v
"$HDC" -t "$TARGET" shell param get bootevent.boot.completed
"$HDC" -t "$TARGET" shell bm dump -g
"$HDC" -t "$TARGET" shell bm dump -n "<bundleName>"
"$HDC" -t "$TARGET" shell aa dump -l
"$HDC" -t "$TARGET" shell aa dump -r
"$HDC" -t "$TARGET" shell hidumper -ls
"$HDC" -t "$TARGET" shell hilog -z 100
"$HDC" -t "$TARGET" shell uitest dumpLayout -p /dev/null -a
"$HDC" -t "$TARGET" shell uitest screenCap -p /dev/null
```

`bm dump`、`aa dump`、`hilog` 输出可能包含应用名、路径或错误文本；报告时只保留必要摘要。

### 执行模式标注

- `automation`：启动或停止 Emulator。
- `automation`：安装、卸载、启动应用。
- `automation`：创建、复制、删除或清理 HVD，需限定实例名和恢复策略。
- `evidence`：`hdc file recv`、保存真实 layout、截图、录屏、日志包或沙箱内容，必须写入显式 `artifactDir`。
- `automation`：`hdc file send` 和新增或删除 `fport/rport` 端口转发，必须限定 target、端口和生命周期。
- `diagnostic`：有界 `hitrace`、底层 `uinput`、大范围 `hilog -x`。
- `diagnostic`：电源、显示、折叠、窗口策略切换，必须记录恢复动作。
- `break-glass`：清数据、刷写、格式化、root/daemon、通配删除等系统级动作。

### 系统级动作

用户明确目标时可以执行；执行前后必须记录 target、命令摘要、恢复策略、产物目录和脱敏状态：

```bash
hdc target mount
hdc smode
hdc flash
hdc erase
hdc format
hdc sideload
param set
bm clean
wukong exec
wukong special
wukong focus
```

无法分类的命令标记为 `riskLevel=unknown`，不请求确认；若缺少 target、timeout 或命令参数，返回 `blocked` 并给出 `missingConfig`。

## 启动模拟器

当前版本线索显示：直接启动 Emulator 通常需要 `-hvd`、`-path`、`-imageRoot`，并可能需要 `-t <trace-name>` 对应的本地占位通道。占位通道是启动期依赖，不要把它当稳定控制协议。

`<trace-name>` 处理规则：

- 优先沿用当前任务或已验证 helper 生成的唯一 trace name。
- 找不到已验证来源时，可以生成仅用于本轮的唯一名称，例如 `ai-emu-<YYYYMMDDHHMMSS>`，但必须说明这不是稳定协议。
- 若缺少占位通道导致启动失败，停止本轮启动尝试，只报告 Emulator 版本、HVD 名称、命令类型和裁剪后的错误摘要，不继续 UI 自动化。
- 不记录或沉淀 HVD 内部字段、trace pipe 私有协议或未验证 helper 细节。

使用模板：

```bash
cd "/Applications/DevEco-Studio.app/Contents/tools/emulator"

./Emulator \
  -hvd "<hvd-name>" \
  -path "$HOME/.Huawei/Emulator/deployed" \
  -t "<trace-name>" \
  -imageRoot "$HOME/Library/Huawei/Sdk"
```

多实例时显式指定不同 HDC 端口：

```bash
./Emulator \
  -hvd "<hvd-name>" \
  -path "$HOME/.Huawei/Emulator/deployed" \
  -t "<trace-name>" \
  -imageRoot "$HOME/Library/Huawei/Sdk" \
  -hdcport 10100
```

停止指定 HVD：

```bash
"/Applications/DevEco-Studio.app/Contents/tools/emulator/Emulator" \
  -stop "<hvd-name>" \
  -path "$HOME/.Huawei/Emulator/deployed"
```

## 等待可操作状态

1. 等待 `hdc list targets -v` 中目标为 `TCP Connected`。
2. 查询启动完成：

```bash
"$HDC" -t "$TARGET" shell param get bootevent.boot.completed
```

期望返回 `true`。如果不可用，只能把 Emulator 日志中的 `Guest OS Boot Completed!!` 当辅助线索。

超时后停止 UI 操作，只报告 target 状态、boot 状态和裁剪后的日志摘要。

## 失败分流

- 没有 HDC target：停止 UI 自动化，报告 Emulator/HVD 探测摘要；非交互 run 返回 `blocked`，`missingConfig` 为 `target`。
- 只有 `Offline` target：不执行 shell、uitest 或输入动作；报告 target 状态并建议重启/等待连接。
- 多个 `Connected` target 且用户未指定：停止，要求用户选择 `127.0.0.1:<port>`。
- boot completed 超时或不是 `true`：不点击、不输入，只保留 boot 参数和连接摘要。
- `uitest dumpLayout -p /dev/null -a` 不支持或返回权限错误：不默认改为真实路径采集；先降级到其他只读诊断，真实 layout/screenshot 需要 `artifactDir` 和脱敏配置。
- 脱敏失败：不归档、不回显原文。

## UI 自动化

优先使用设备侧 `uitest`，不要盲点桌面坐标。

只读探测：

```bash
"$HDC" -t "$TARGET" shell uitest dumpLayout -p /dev/null -a
"$HDC" -t "$TARGET" shell uitest screenCap -p /dev/null
```

真实内容采集需要显式 `artifactDir` 和脱敏配置：

```bash
"$HDC" -t "$TARGET" shell uitest dumpLayout -p /data/local/tmp/ai-layout.json -a
"$HDC" -t "$TARGET" shell cat /data/local/tmp/ai-layout.json
"$HDC" -t "$TARGET" shell uitest screenCap -p /data/local/tmp/ai-screen.png
"$HDC" -t "$TARGET" file recv /data/local/tmp/ai-screen.png ./ai-screen.png
```

输入模板：

```bash
"$HDC" -t "$TARGET" shell uitest uiInput click <x> <y>
"$HDC" -t "$TARGET" shell uitest uiInput swipe <x1> <y1> <x2> <y2>
"$HDC" -t "$TARGET" shell uitest uiInput drag <x1> <y1> <x2> <y2>
"$HDC" -t "$TARGET" shell uitest uiInput keyEvent Home
"$HDC" -t "$TARGET" shell uitest uiInput keyEvent Back
"$HDC" -t "$TARGET" shell uitest uiInput text "<escaped-text>"
```

规则：

- 坐标来源优先级：可解析的 dumpLayout 节点坐标 -> 截图辅助定位 -> 用户明确给出的坐标 -> `uinput` 或桌面坐标兜底。
- 每步输入后重新探测状态。
- 用户输入文本必须转义，不能拼接原文 shell。
- `uinput` 作为底层输入兜底，必须记录 `riskLevel=diagnostic`。

## 应用启动与诊断

启动前先定位 bundle 和 ability：

```bash
"$HDC" -t "$TARGET" shell bm dump -n "$BUNDLE"
"$HDC" -t "$TARGET" shell aa start -b "$BUNDLE" -a "$ABILITY"
```

不知道 ability 时，从 `bm dump -n` 的裁剪输出中查 `mainAbility`、`mainElementName` 或 `abilityInfos[].name`。

常用只读诊断：

```bash
"$HDC" -t "$TARGET" shell hidumper --cpuusage <pid>
"$HDC" -t "$TARGET" shell hidumper --mem <pid> --prune
"$HDC" -t "$TARGET" shell hidumper --net <pid>
"$HDC" -t "$TARGET" shell hidumper --storage <pid>
"$HDC" -t "$TARGET" shell hilog -z 100
```

## 参数白名单

默认健康检查只读取这些低风险参数：

```bash
param get bootevent.boot.completed
param get const.product.model
param get const.product.name
param get const.product.devicetype
param get const.product.os.dist.name
param get const.product.os.dist.version
param get const.product.os.dist.apiversion
param get const.ohos.fullname
param get const.ohos.apiversion
param get persist.sys.hilog.loggable.global
```

不默认读取或记录包含这些关键词的参数：`udid`、`uuid`、`serial`、`sn`、`account`、`user`、`token`、`auth`、`wifi`、`wlan`、`mac`、`ip`。

## 超时

| 场景 | 建议 timeout | 超时处理 |
| --- | ---: | --- |
| `hdc list targets -v` | 5s | 停止本轮自动化 |
| boot completed 轮询 | 单次 3s，总 60-120s | 超时不做 UI 输入 |
| `uitest dumpLayout` / `screenCap` | 10s | 降级到日志摘要 |
| `aa dump` / `bm dump` | 8s | 裁剪输出，失败则跳过 |
| `hidumper` | 8s | 跳过该指标 |
| `hilog -z 100` | 5s | 保留已返回内容 |

禁止无超时运行：不带 `-z` / `-x` 的 `hilog`、`track-jpid`、`hitrace --record`、`wukong exec`、`uitest uiRecord record`、`uitest start-daemon`。

## 执行记录模板

高风险或会写入产物的动作必须记录读取范围、写入位置、脱敏策略和停止条件：

```text
动作：<启动/停止/安装/采集/端口转发>。
范围：<HVD/target/bundle/path>。
读取：<target 状态/boot 参数/裁剪日志/截图/layout/设备文件>。
写入：<无/本地路径/设备路径>。
脱敏：<只保留摘要，不保存原文/保存附件前裁剪字段>。
停止条件：<无 Connected target/boot 超时/命令失败/脱敏失败>。
```

## 输出与脱敏

默认只向用户报告能力、状态、错误摘要、资源数值和可复现命令模板。不要保存或回显完整 layout、截图、日志、token、cookie、设备唯一标识、用户 ID、URL query、请求体、响应体、证书、fingerprint、真实沙箱路径、完整窗口树或完整业务 payload。

推荐摘要格式：

```text
target: 127.0.0.1:<port>
boot: true|false
foreground: <bundle>/<ability>, pid=<pid>
display: <w>x<h>, density=<n>, rotation=<n>
resources: cpu=<percent>, memPss=<kb>
logs: errors=<n>, warnings=<n>, topError=<summary>
ui: layoutProbe=true|false, screenshotProbe=true|false, rawContentStored=false
```

脱敏失败时，不归档原文。
