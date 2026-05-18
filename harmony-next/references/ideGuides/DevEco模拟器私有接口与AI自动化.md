# DevEco Studio 模拟器私有接口与 AI 自动化

验证日期：2026-05-18

适用范围：macOS 上的 DevEco Studio 本地 HarmonyOS Emulator，目标是免启动 IDE，直接启动模拟器，并通过 `hdc`、`uitest`、`aa`、`bm`、`hilog`、`hidumper` 等命令完成 AI 自动化观察、输入和诊断。

重要声明：本页记录的是本地验证成果，包含私有未公开接口和经验性边界，不是稳定公开 API。DevEco Studio、Emulator、SDK 镜像、HVD 元数据、设备侧命令输出都可能随版本变化。每次执行前先做能力探测；脚本只能把这里的结论当作当前版本的候选路径，不能当长期契约。

## 已验证环境

- DevEco Studio 路径：`/Applications/DevEco-Studio.app`
- Emulator 路径：`/Applications/DevEco-Studio.app/Contents/tools/emulator/Emulator`
- hdc 路径：`/Applications/DevEco-Studio.app/Contents/sdk/default/openharmony/toolchains/hdc`
- 已验证 Emulator 版本：`HarmonyOS Emulator :6.0.2.200`

## 核心结论

1. 可以不启动 DevEco Studio IDE，直接启动 DevEco Studio 包内的 HarmonyOS Emulator。
2. 当前环境启动 Emulator 不能只传 `-hvd`，还需要 `-t <trace-name>`，并在启动阶段准备并持有同名本地占位通道。
3. `-path` 传虚拟设备父目录：`$HOME/.Huawei/Emulator/deployed`，不要传具体实例目录。
4. `-imageRoot` 使用 SDK 镜像根目录：`$HOME/Library/Huawei/Sdk`。
5. 设备上线后，`hdc list targets -v` 会出现 `127.0.0.1:<hdc-port>` 且状态为 `TCP Connected`。
6. AI UI 自动化优先使用 `hdc + uitest`，比桌面坐标点击稳定。
7. 创建、删除、复制 HVD 属于高风险私有流程；当前只保留能力边界，不沉淀内部文件和字段编辑细节。

## 启动流程

先由受控 helper 准备并持有 `-t <trace-name>` 对应的本地占位通道。占位通道只用于满足启动期依赖，不作为稳定控制通道使用；helper 必须绑定本轮 `run_id`，并由创建者清理。

```bash
EMU_ROOT="/Applications/DevEco-Studio.app/Contents/tools/emulator"
HVD_NAME="<hvd-name>"
HVD_ROOT="$HOME/.Huawei/Emulator/deployed"
IMAGE_ROOT="$HOME/Library/Huawei/Sdk"
TRACE_NAME="<trace-name>"

cd "$EMU_ROOT"

./Emulator \
  -hvd "$HVD_NAME" \
  -path "$HVD_ROOT" \
  -t "$TRACE_NAME" \
  -imageRoot "$IMAGE_ROOT"
```

多实例时显式指定独立 HDC 端口，建议从 `10100` 起递增：

```bash
./Emulator \
  -hvd "$HVD_NAME" \
  -path "$HVD_ROOT" \
  -t "$TRACE_NAME" \
  -imageRoot "$IMAGE_ROOT" \
  -hdcport 10100
```

停止指定 HVD：

```bash
/Applications/DevEco-Studio.app/Contents/tools/emulator/Emulator \
  -stop "<hvd-name>" \
  -path "$HOME/.Huawei/Emulator/deployed"
```

## 能力探测

只读探测优先执行：

```bash
EMULATOR="/Applications/DevEco-Studio.app/Contents/tools/emulator/Emulator"
HDC="/Applications/DevEco-Studio.app/Contents/sdk/default/openharmony/toolchains/hdc"

"$EMULATOR" -version
"$EMULATOR" -list
"$EMULATOR" -list -details
"$HDC" list targets -v
```

`Emulator -list -details` 当前会输出 JSON，包含 HVD 名称、运行状态、实例位置、镜像位置、端口、屏幕、内存、CPU、系统版本等摘要信息。字段名以当前版本输出为准，解析器只应读取必要摘要，不固定完整内部字段。

`hdc list targets -v` 只选择 `Connected` 目标：

```text
127.0.0.1:<port-a>    TCP    Offline      localhost
127.0.0.1:<port-b>    TCP    Connected    localhost
```

多 target 且用户未指定目标时停止，不默认选第一个。

## 启动完成判断

先等 HDC target `Connected`，再等系统启动完成：

```bash
TARGET="127.0.0.1:<hdc-port>"
"$HDC" -t "$TARGET" shell param get bootevent.boot.completed
```

期望返回 `true`。如果该参数不可用，回退查 Emulator 日志摘要中的：

```text
Guest OS Boot Completed!!
```

任一阶段超时后只采集连接状态、boot 状态和最近日志摘要，不进入 UI 输入。

## UI 自动化链路

能力探测不保存真实 UI 内容：

```bash
"$HDC" -t "$TARGET" shell uitest dumpLayout -p /dev/null -a
"$HDC" -t "$TARGET" shell uitest screenCap -p /dev/null
```

真实采集需要用户确认，因为会包含 UI 文本或屏幕内容：

```bash
"$HDC" -t "$TARGET" shell uitest dumpLayout -p /data/local/tmp/ai-layout.json -a
"$HDC" -t "$TARGET" shell cat /data/local/tmp/ai-layout.json
"$HDC" -t "$TARGET" shell uitest screenCap -p /data/local/tmp/ai-screen.png
"$HDC" -t "$TARGET" file recv /data/local/tmp/ai-screen.png ./ai-screen.png
```

输入优先使用 `uitest uiInput`：

```bash
"$HDC" -t "$TARGET" shell uitest uiInput click <x> <y>
"$HDC" -t "$TARGET" shell uitest uiInput swipe <x1> <y1> <x2> <y2>
"$HDC" -t "$TARGET" shell uitest uiInput drag <x1> <y1> <x2> <y2>
"$HDC" -t "$TARGET" shell uitest uiInput keyEvent Home
"$HDC" -t "$TARGET" shell uitest uiInput keyEvent Back
"$HDC" -t "$TARGET" shell uitest uiInput text "<text>"
```

约束：

- 坐标必须来自当前 layout 或截图，不做盲点。
- 每步输入后重新 dump layout 或截图确认状态变化。
- 输入文本必须做 shell 参数转义，禁止拼接未经处理的用户文本。
- `uinput` 是底层兜底入口，默认不用；只有 `uitest` 不覆盖且用户确认后才使用。

## 应用与诊断命令

常用只读或低风险命令：

```bash
"$HDC" -t "$TARGET" shell bm dump -n "<bundleName>"
"$HDC" -t "$TARGET" shell bm dump -g
"$HDC" -t "$TARGET" shell aa dump -l
"$HDC" -t "$TARGET" shell aa dump -r
"$HDC" -t "$TARGET" shell hidumper -ls
"$HDC" -t "$TARGET" shell hilog -z 100
"$HDC" -t "$TARGET" shell hidumper --cpuusage <pid>
"$HDC" -t "$TARGET" shell hidumper --mem <pid> --prune
"$HDC" -t "$TARGET" shell hidumper --net <pid>
"$HDC" -t "$TARGET" shell hidumper --storage <pid>
```

启动目标应用：

```bash
"$HDC" -t "$TARGET" shell bm dump -n "$BUNDLE"
"$HDC" -t "$TARGET" shell aa start -b "$BUNDLE" -a "$ABILITY"
```

如果不知道 Ability，先从 `bm dump -n` 的裁剪输出中提取 `mainAbility`、`mainElementName` 或 `abilityInfos[].name`。

## 风险分级

默认允许：

- `Emulator -version`
- `Emulator -list`
- `Emulator -list -details`
- `hdc list targets -v`
- `param get <white-listed-key>`
- `hilog -z <n>`
- `aa dump -l`
- `aa dump -r`
- `bm dump -g`
- `bm dump -n <bundleName>` 的裁剪摘要
- `hidumper --cpuusage <pid>`
- `hidumper --mem <pid> --prune`
- `uitest dumpLayout -p /dev/null -a`
- `uitest screenCap -p /dev/null`
- `uitest uiInput click/swipe/drag/text/keyEvent Back/Home`
- `power-shell wakeup`

需要用户确认：

- 启停模拟器。
- 安装、卸载、清数据。
- 创建、复制、删除、清理 HVD。
- `hdc file send` 写设备文件。
- `hdc file recv` 拉取真实 layout、截图、日志或沙箱内容。
- `Emulator -logZip`、`hilog -x` 或大范围日志打包。
- 真实 `dumpLayout`、`screenCap`、`snapshot_display`。
- 新增或删除 `fport/rport` 端口转发。
- `hitrace` 采样。
- `uinput` 底层输入。
- `aa force-stop`、`power-shell suspend/timeout/setmode`、显示/折叠/电源策略切换。

默认禁止，除非用户明确进入系统级调试：

- `hdc target mount`
- `hdc smode`
- `hdc flash`
- `hdc erase`
- `hdc format`
- `hdc sideload`
- `param set`
- `bm clean`
- `wukong exec/special/focus`

无法分类的命令按 `require_confirm` 处理。

## 参数白名单

默认健康检查只读取低风险参数：

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

不默认读取或落文档：

- `*udid*`、`*uuid*`、`*serial*`、`*sn*`
- `*account*`、`*user*`、`*token*`、`*auth*`
- `*wifi*`、`*wlan*`、`*mac*`、`*ip*`
- 全量 `param get` 输出

## 超时建议

所有自动化命令必须由上层 runner 设置超时。

| 场景 | 建议 timeout | 超时处理 |
| --- | ---: | --- |
| `hdc list targets -v` | 5s | 终止本轮自动化 |
| `param get bootevent.boot.completed` | 3s，轮询总时长 60-120s | 超时终止 UI 操作 |
| `uitest dumpLayout -p /dev/null -a` | 10s | 降级到截图/日志 |
| `uitest screenCap -p /dev/null` | 10s | 跳过截图 |
| `aa dump -l` / `aa dump -r` | 8s | 跳过输入动作 |
| `bm dump -g` / `bm dump -n <bundle>` | 8s | 裁剪输出；超时跳过 |
| `hidumper --cpuusage <pid>` / `--mem <pid>` | 8s | 跳过该指标 |
| `hilog -z 100 -P <pid>` | 5s | 保留已收集内容 |
| `track-jpid` 短监听 | 3s | 超时视为采样结束 |

禁止无超时运行无限流或后台任务，例如不带 `-z` / `-x` 的 `hilog`、无超时的 `track-jpid`、`hitrace --record`、`wukong exec`、`uitest uiRecord record`、`uitest start-daemon`。

## Runner 状态模型

建议每次自动化抽象为一个 `run_id`，格式如 `YYYYMMDD-HHMMSS-<short-random>`。`run_id` 贯穿命令日志、临时文件名、trace name、失败包和 artifact manifest。

状态机：

1. 生成唯一 `run_id` 和 `trace_name`。
2. 启动并记录 trace pipe helper；helper 异常退出时终止本轮 run。
3. 启动 Emulator。
4. 显式选择 target；多 target 且未指定时停止。
5. 等待 HDC connected 与 boot completed。
6. 执行应用启动、UI 探测、输入和验收。
7. 按失败类型采集诊断摘要。
8. 清理本轮临时文件和 trace pipe helper。

命令记录保存 argv 数组，不保存拼接后的 shell 字符串。默认只保存摘要，原始输出只有在用户确认档中保留。

## 脱敏规则

默认只保存能力、状态、错误摘要、资源数值和可复现命令模板，不保存完整原始输出。

可保留摘要：

```text
target: 127.0.0.1:<port>
boot: true
foreground: <bundle>/<ability>, pid=<pid>
window: focus=<winId>, bounds=<x,y,w,h>
display: <w>x<h>, density=<n>, rotation=<n>
resources: cpu=<percent>, memPss=<kb>, netRx=<bytes>, netTx=<bytes>
logs: errors=<n>, warnings=<n>, topError=<summary>
ui: layoutNodes=<n>, clickableNodes=<n>, screenshotCaptured=<true|false>, rawContentStored=false
```

必须删除或裁剪：

- token、cookie、session、authorization。
- 手机号、邮箱、用户 ID、设备唯一标识。
- URL query、请求体、响应体、业务 payload。
- 签名、证书、fingerprint、appId。
- 沙箱路径、安装路径、真实文件路径。
- 完整窗口树、完整 layout JSON、真实截图，除非用户明确确认保存附件。
- 外部 IP、域名、端口明细、socket 路径。

脱敏失败时禁止归档原文。

## 失败诊断包

默认档只读、无真实截图或布局附件：

```bash
"$HDC" list targets -v
"$HDC" -t "$TARGET" shell param get bootevent.boot.completed
"$HDC" -t "$TARGET" shell uitest dumpLayout -p /dev/null -a
"$HDC" -t "$TARGET" shell uitest screenCap -p /dev/null
"$HDC" -t "$TARGET" shell aa dump -l
"$HDC" -t "$TARGET" shell aa dump -r
"$HDC" -t "$TARGET" shell bm dump -g
```

增强档仍只读，但信息更多：

```bash
"$HDC" -t "$TARGET" shell hilog -z 50
"$HDC" -t "$TARGET" shell hidumper --cpuusage
"$HDC" -t "$TARGET" shell hidumper --mem --prune
"$HDC" -t "$TARGET" shell hidumper -e --list -n 5
"$HDC" -t "$TARGET" shell hidumper -ls
```

用户确认档：

```bash
Emulator -logZip <name> -logPath <path>
"$HDC" -t "$TARGET" shell hilog -x
"$HDC" -t "$TARGET" shell uitest dumpLayout -p /data/local/tmp/layout.json -a
"$HDC" -t "$TARGET" shell uitest screenCap -p /data/local/tmp/screen.png
"$HDC" -t "$TARGET" file recv /data/local/tmp/layout.json <local>
"$HDC" -t "$TARGET" file recv /data/local/tmp/screen.png <local>
```

## 已知限制

1. trace pipe 占位通道必须在启动阶段保持运行；退出后 Emulator 后续行为可能不稳定。
2. 当前只是验证最小可启动链路，没有实现完整 trace 协议。
3. HDC target 上线后仍需等待系统 boot completed，再执行 UI 操作。
4. 模拟器窗口可能不在主屏；桌面窗口移动可用 `osascript` 辅助，但 AI 自动化仍优先走 `hdc + uitest`。
5. 多实例必须使用不同 trace name 与 HDC 端口，避免连接冲突。
6. 本页不记录 HVD 创建/删除的内部文件、字段和编辑步骤；相关动作必须由受控工具备份、验证、可回滚，并经用户确认。
