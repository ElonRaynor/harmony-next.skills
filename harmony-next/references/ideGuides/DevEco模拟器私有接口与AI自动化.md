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
3. 需要真实 UI 内容、设备文件、端口转发、安装卸载、启动/停止模拟器或写文件时，先请求用户确认并说明会采集什么。
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

### 需要用户确认

- 启动或停止 Emulator。
- 安装、卸载、清数据、启动应用。
- 创建、复制、删除、清理 HVD。
- `hdc file send` / `hdc file recv`。
- 保存真实 layout、截图、录屏、日志包或沙箱内容。
- 新增或删除 `fport/rport` 端口转发。
- `hitrace`、`uinput`、大范围 `hilog -x`。
- 电源、显示、折叠、窗口策略切换。

### 默认禁止

除非用户明确要求系统级调试并接受风险，不执行：

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

无法分类的命令按“需要用户确认”处理。

## 启动模拟器

当前版本线索显示：直接启动 Emulator 通常需要 `-hvd`、`-path`、`-imageRoot`，并可能需要 `-t <trace-name>` 对应的本地占位通道。占位通道是启动期依赖，不要把它当稳定控制协议。

确认后使用模板：

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

停止指定 HVD 需要确认：

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

## UI 自动化

优先使用设备侧 `uitest`，不要盲点桌面坐标。

只读探测：

```bash
"$HDC" -t "$TARGET" shell uitest dumpLayout -p /dev/null -a
"$HDC" -t "$TARGET" shell uitest screenCap -p /dev/null
```

真实内容采集需要确认：

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

- 坐标必须来自当前 layout 或截图。
- 每步输入后重新探测状态。
- 用户输入文本必须转义，不能拼接原文 shell。
- `uinput` 只作为确认后的兜底。

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
