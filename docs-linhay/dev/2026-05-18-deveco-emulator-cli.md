# DevEco Studio 模拟器免 IDE 启动验证

日期：2026-05-18

## 背景

目标是在不启动 DevEco Studio IDE 的前提下，直接启动 HarmonyOS 本地模拟器，并让 AI 可以通过命令行或桌面自动化操作模拟器。验证环境为 macOS，DevEco Studio 安装路径：

```bash
/Applications/DevEco-Studio.app
```

## 结论

方案成立：可以不启动 DevEco Studio，直接启动 DevEco Studio 包内的 HarmonyOS Emulator。

验证结果：

1. `Emulator` 独立进程成功启动。
2. 模拟器日志出现 `Guest OS Boot Completed!!`。
3. `hdc list targets -v` 返回 `127.0.0.1:<hdc-port>` 且状态为 `TCP Connected`。
4. `hdc -t <target> shell uitest dumpLayout` 可以导出 UI 树。
5. `hdc -t <target> shell uitest uiInput keyEvent Home` 返回 `No Error`。
6. 模拟器窗口可通过 macOS 辅助功能移动到主屏并截图确认。

## 并行探查覆盖矩阵

本轮使用多路子任务并行探查，文档只沉淀命令级结论、验证结果和风险边界。

| 方向 | 覆盖内容 | 结论 |
| --- | --- | --- |
| 宿主侧 Emulator / hdc | `Emulator -version/-list/-list -details`、`hdc help/list targets/fport/jpid` | 可发现实例、运行态和调试进程；`-list -details` 已验证可用 |
| UI 控制 | `uitest dumpLayout/screenCap/uiInput`、`uinput`、`snapshot_display` | AI 操作首选 `uitest`；复杂输入再考虑 `uinput` |
| 应用与诊断 | `aa`、`bm`、`hidumper`、`hilog`、`param` | 可覆盖启动、前台状态、包信息、资源、日志和系统参数 |
| 环境模拟 | Display / Battery / Sensor / Power / Thermal / hitrace | 多数适合观测；会改变状态的入口进入确认档 |
| 网络与端口 | `fport/rport`、`jpid`、`ifconfig`、`hidumper --net` | 默认只读查询；不默认创建转发或广播发现 |
| 调试与测试 | `aa appdebug/process/test`、`bm dump -g`、`shell -b` | 只读发现默认允许；真实调试/测试执行需要确认 |
| 多实例 / HVD | `-hdcport`、`-list -details`、配置字段 | 多实例端口建议从 `10100` 递增；创建/删除 HVD 需要确认 |
| 失败诊断 | 默认档、增强档、用户确认档 | 默认只读无附件；真实截图、layout、大日志需确认 |
| 风险策略 | risk gate、超时、防卡死、脱敏 | 默认只读 + 受控输入；无法分类按 `require_confirm` |

真实截图附件说明：本轮曾生成一张 `snapshot_display` 验证截图并存入 `docs-linhay/screenshots/20260518/emulator/20260518-emulator-snapshot-display-after-v01.png`。它属于用户确认档性质的诊断附件，不构成 UI 回归的 before/after 截图组；后续若要严格遵守“默认不保存真实截图”，应由用户确认保留、脱敏或删除。

## 关键发现

已验证启动模拟器时不能只执行 `Emulator -hvd ...`。当前环境还需要通过 `-t` 参数传入一个本地占位通道名称。

已验证启动命令形态：

```bash
/Applications/DevEco-Studio.app/Contents/tools/emulator/Emulator \
  -hvd '<hvd-name>' \
  -path '<hvd-root>' \
  -t '<trace-name>' \
  -imageRoot '<image-root>'
```

如果缺少该占位通道，Emulator 会在早期退出，不会完整写入实例日志。2026-05-28 追加线上 issue #13 结论：在 DevEco Studio `6.0.2` / HarmonyOS Emulator `6.0.2.200` 环境中，不完整命令还可能弹出登录/设备管理模态框：

```text
模拟器启动失败
请在DevEco Studio中登录华为账号，并从设备管理中启动模拟器
```

这不是“先让用户登录”的默认分流，而是 CLI 启动路径缺少 trace pipe 前置条件的已知症状。后续 Agent 在执行或建议启动命令前，必须先完成 trace pipe helper preflight；helper 不可用时返回 blocked，不继续尝试 `Emulator -hvd ... -path ... -imageRoot ...`。

### trace pipe 的公开可复现边界

出于合规和可维护性考虑，本文只记录命令级结论、运行现象和风险边界。

当前可复现事实：

1. Emulator 启动命令可传入 `-t <trace-name>`。
2. 当前环境中，免 IDE 启动需要先准备同名本地占位通道。
3. 如果占位通道不存在，Emulator 会早期退出。
4. 该占位通道只用于启动期依赖满足，不作为稳定控制通道使用。

## 可复现启动流程

### 1. 准备 trace pipe 占位通道

启动前先准备 `-t <trace-name>` 对应的本地占位通道，并保持该通道在 Emulator 启动阶段可用。占位通道的实现细节不写入公开文档；脚本化时应由受控 helper 负责创建、持有和清理，并确保不会覆盖非本流程创建的本地文件。

### 1.1 Runner 参数约定

第一步由受控 helper 准备并持有 trace pipe，占位通道准备完成后再启动 Emulator。受控 helper 需要提供 readiness 信号；没有 readiness 信号时，不执行 Emulator 启动。

```text
TRACE_NAME="<trace-name>"
EMU_ROOT="/Applications/DevEco-Studio.app/Contents/tools/emulator"
HVD_NAME="<hvd-name>"
HVD_ROOT="$HOME/.Huawei/Emulator/deployed"
IMAGE_ROOT="$HOME/Library/Huawei/Sdk"

<受控 helper 准备并持有 TRACE_NAME 对应的本地占位通道>
```

执行启动前先跑脚本层 preflight。该命令不会启动 Emulator，只验证路径、HVD 和 trace helper readiness，并在通过后输出带 `-t` 的命令计划：

```bash
python3 harmony-next/scripts/hvd_manager.py \
  --root "$HVD_ROOT" \
  --emulator "$EMU_ROOT/Emulator" \
  --sdk-root "$IMAGE_ROOT" \
  launch-preflight \
  --name "$HVD_NAME" \
  --trace-name "$TRACE_NAME" \
  --trace-helper-ready-file "<helper-ready-file>" \
  --json
```

保持占位通道 helper 运行，再开一个终端：

```bash
TRACE_NAME="<trace-name>"
EMU_ROOT="/Applications/DevEco-Studio.app/Contents/tools/emulator"
HVD_NAME="<hvd-name>"
HVD_ROOT="$HOME/.Huawei/Emulator/deployed"
IMAGE_ROOT="$HOME/Library/Huawei/Sdk"

cd "$EMU_ROOT"

./Emulator \
  -hvd "$HVD_NAME" \
  -path "$HVD_ROOT" \
  -t "$TRACE_NAME" \
  -imageRoot "$IMAGE_ROOT"
```

### 2. 启动 Emulator

在另一个终端执行：

```bash
cd /Applications/DevEco-Studio.app/Contents/tools/emulator

./Emulator \
  -hvd "<hvd-name>" \
  -path "$HOME/.Huawei/Emulator/deployed" \
  -t "<trace-name>" \
  -imageRoot "$HOME/Library/Huawei/Sdk"
```

注意：

- `-path` 必须传虚拟设备父目录：`$HOME/.Huawei/Emulator/deployed`。
- 不要传具体实例目录。传实例目录会导致 Emulator 按 `<hvd-root>/<hvd-name>/<hvd-name>` 形态查找并失败。
- `-imageRoot` 使用 SDK 镜像根目录：`$HOME/Library/Huawei/Sdk`。

### 3. 验证设备上线

```bash
HDC="/Applications/DevEco-Studio.app/Contents/sdk/default/openharmony/toolchains/hdc"

"$HDC" list targets -v
```

期望输出示例：

```bash
127.0.0.1:<hdc-port>
```

进一步确认系统启动完成：

```bash
tail -80 "<hvd-log-file>"
```

日志中出现以下内容即可认为系统已完成启动：

```text
Guest OS Boot Completed!!
```

## AI 自动化操作方式

优先使用 `hdc + uitest`，比桌面坐标点击更稳定。

常用命令：

```bash
HDC="/Applications/DevEco-Studio.app/Contents/sdk/default/openharmony/toolchains/hdc"
TARGET="127.0.0.1:<hdc-port>"

"$HDC" -t "$TARGET" shell uitest dumpLayout -p /dev/null -a
"$HDC" -t "$TARGET" shell uitest dumpLayout -p /data/local/tmp/layout.json -a
"$HDC" -t "$TARGET" shell uitest screenCap -p /data/local/tmp/screen.png
"$HDC" -t "$TARGET" file recv /data/local/tmp/screen.png ./screen.png
"$HDC" -t "$TARGET" shell uitest uiInput click 300 500
"$HDC" -t "$TARGET" shell uitest uiInput swipe 300 1200 300 400
"$HDC" -t "$TARGET" shell uitest uiInput keyEvent Home
"$HDC" -t "$TARGET" shell uitest uiInput keyEvent Back
"$HDC" -t "$TARGET" shell uitest uiInput inputText 300 500 "hello"
```

`dumpLayout -p /dev/null -a` 只用于能力探测。真实 `dumpLayout`、`screenCap` 和 `file recv` 会生成或拉取 UI 内容，默认不归档；保存真实 layout / screenshot 前需要用户确认或脱敏策略。

## 创建新本地模拟器实例

### 结论

当前没有确认到稳定公开的 `Emulator create` 子命令。本地 HVD 创建在技术上可行，但属于“复制同版本可启动实例并刷新必要元数据”的高风险操作；具体文件、字段和编辑步骤不写入公开沉淀。

2026-05-21 追加静态验证：DevEco Studio 6.0.2.642 的 IDE 包内存在 HVD Manager UI 实现，位置为 `Contents/plugins/harmony/lib/device-mgmt-6.0.2.642.jar`。其中可见 `RunHuaweiHvdManagerAction`、`DownloadImageAction`、`CreateHvdAction`、`DeleteHvdAction`、`ImageDownloadAction`、`ImageDeleteAction` 等类。这说明 IDE 内部确实有下载镜像、新建 HVD、删除 HVD 的 UI action，但这些不是 `Emulator` 可执行文件暴露的稳定 CLI。

静态反编译到的调用边界：

- 镜像下载 / 删除走 SDK Manager 弹窗：`HosIdeaDialogSdkInfoHandler.showInstallPackagesDialog(...)` / `showDeletePackagesDialog(...)`。
- 新建 HVD 走 `LocalDeviceConnection.createDevice(...)`，核心动作是生成实例目录、`config.ini` 和 `<name>.ini` 配置文件。
- 删除 HVD 走 `LocalDeviceConnection.deleteHvd(...)`，核心动作是删除 `<name>.ini`、实例目录内容和实例目录本身。
- `Emulator -help` 仍只列出 `-hvd`、`-path`、`-imageRoot`、`-logZip`、`-logPath`、`-stop`、`-version`、`-list`、`-hdcport`。

2026-05-21 已新增受控命令行封装：

```bash
python3 harmony-next/scripts/hvd_manager.py list --json
python3 harmony-next/scripts/hvd_manager.py doctor --json
python3 harmony-next/scripts/hvd_manager.py create --from "<source-hvd>" --name "<new-hvd>" --hdc-port 10100
python3 harmony-next/scripts/hvd_manager.py delete --name "<new-hvd>" --confirm-name "<new-hvd>"
python3 harmony-next/scripts/hvd_manager.py launch-preflight --name "<hvd-name>" --trace-name "<trace-name>" --trace-helper-ready-file "<helper-ready-file>" --json
python3 harmony-next/scripts/hvd_manager.py launch --name "<hvd-name>" --image-root "<emulator-image-root>" --trace-name "<trace-name>" --json
python3 harmony-next/scripts/hvd_manager.py download-image --device-type phone --api-version 22
```

实现边界：

- `list` 只读解析 HVD root 下的根 `.ini` 与实例 `config.ini`。
- `doctor` 探测本机平台、HVD root、Emulator 可执行文件、build SDK root、emulator image root、HDC、Emulator 版本和 HVD 列表；输出不包含 HVD UUID。
- `create` 以现有本地实例为源克隆目录，刷新名称、路径、UUID、`hardware-qemu.ini` 中的 HVD 名称以及可选 HDC 端口；默认不复制旧日志。
- `delete` 必须传入完全匹配的 `--confirm-name`，只删除 HVD root 内目标实例目录、根 `.ini` 和 `lists.json` 同名条目。
- `launch-preflight` 验证启动前置条件，不创建 trace pipe、不启动 Emulator；缺少 `traceName`、helper readiness 文件或 HVD `imageSubPath` 对应系统镜像时返回 `blocked`，满足时输出含 `-t <trace-name>` 的命令计划。
- `launch` 创建启动期 trace socket，detach Emulator 进程与 trace holder 后执行含 `-t <trace-name>` 的 Emulator 命令；缺少 HVD、Emulator、image root、trace name 或 HDC 时返回 machine-readable `blocked`。启动失败、trace 超时或 HDC/boot/稳定性检查超时时输出 `logPath`、`processExitCode`、`hvdRuntime`、`hdcSnapshot`、`hdcWait`、`bootWait` 和 `stabilityWait` 诊断。
- `download-image` 暂不执行下载，只返回 machine-readable `blocked`，用于明确区分“已有命令入口”和“仍需 SDK Manager bridge 的能力”。
- 环境适配：`--root` / `HARMONY_HVD_ROOT` 指定 HVD root；`--emulator` / `HARMONY_EMULATOR` 指定 Emulator；`--image-root` / `HARMONY_EMULATOR_IMAGE_ROOT` 指定模拟器镜像根；`--hdc` / `HARMONY_HDC` 指定 HDC；`--sdk-root` / `DEVECO_SDK_HOME` 只表示 DevEco build SDK root。macOS 常见拆分是 build SDK root 为 `/Applications/DevEco-Studio.app/Contents/sdk`，模拟器镜像根为 `$HOME/Library/Huawei/Sdk`。

真实环境 smoke（2026-05-21）：

- `list --json` 在本机 HVD root 下只读列出 `Codex Test Phone` 与 `Pura 90 Pro Max`，输出不包含 UUID。
- `doctor --json` 在本机 macOS arm64 上发现 HVD root、`/Applications/DevEco-Studio.app/Contents/tools/emulator/Emulator`、`/Applications/DevEco-Studio.app/Contents/sdk`，并读取 `HarmonyOS Emulator :6.0.2.200`。
- 从 `Codex Test Phone` 创建 `Codex CLI Smoke 20260521`，指定 `--hdc-port 10101`。
- 验证新实例 `config.ini` 中 `name`、`productModel`、`hw.hdc.port` 已刷新，`hardware-qemu.ini` 中 `hvd.id`、`hvd.name` 已刷新，`list --json` 可见新实例。
- 执行 `delete --name "Codex CLI Smoke 20260521" --confirm-name "Codex CLI Smoke 20260521"` 后，确认临时实例目录和根 `.ini` 均已删除，原有 HVD 保留。

风险门禁：

- 本节只记录能力结论、验收信号和风险边界。
- 创建、删除、清理 HVD 都必须由用户明确确认后执行。
- 只读审计阶段只允许 `Emulator -list`、`Emulator -list -details`、读取现有实例摘要。
- 删除测试实例属于破坏性动作，只允许用于确认过的测试实例名，禁止套用到原始实例。

本次已验证创建并启动成功的新实例，以下用 `<new-hvd-name>` 表示。

验证结果：

1. `Emulator -list` 能看到 `<new-hvd-name>`。
2. 使用独立 trace pipe 与独立 HDC 端口启动成功。
3. 新实例日志出现 `Guest OS Boot Completed!!`。
4. `hdc list targets` 能看到对应 `TCP Connected` 目标。
5. `hdc -t <target> shell uitest dumpLayout` 成功。
6. `hdc -t <target> shell uitest uiInput keyEvent Home` 返回 `No Error`。

### 创建能力边界

创建 HVD 的受控工具至少要满足以下约束：

- 源实例必须是同版本、当前可启动、可回滚的本地实例。
- 新实例名必须先做重名检查。
- 必须刷新名称、路径、唯一标识和实例注册信息。
- 必须先备份再修改，失败时能恢复到修改前状态。
- 必须使用独立 HDC 端口，避免和已有实例冲突。
- 必须把创建、启动验证、停止和清理放在同一个确认档 run 内记录。

验证注册结果：

```bash
/Applications/DevEco-Studio.app/Contents/tools/emulator/Emulator -list
```

期望能看到：

```text
<new-hvd-name>
<existing-hvd-name>
```

### 启动新实例验证

先准备 `-t <trace_name>` 对应的本地占位通道。再启动新实例，并指定独立 HDC 端口，避免与已有实例冲突：

```bash
cd /Applications/DevEco-Studio.app/Contents/tools/emulator

./Emulator \
  -hvd "<new-hvd-name>" \
  -path "$HOME/.Huawei/Emulator/deployed" \
  -t "<trace-name>" \
  -imageRoot "$HOME/Library/Huawei/Sdk" \
  -hdcport <port>
```

验证新实例自动化能力：

```bash
HDC="/Applications/DevEco-Studio.app/Contents/sdk/default/openharmony/toolchains/hdc"
TARGET="127.0.0.1:<port>"

"$HDC" list targets -v
"$HDC" -t "$TARGET" shell uitest dumpLayout -p /dev/null -a
"$HDC" -t "$TARGET" shell uitest uiInput keyEvent Home
```

### 停止新实例

```bash
/Applications/DevEco-Studio.app/Contents/tools/emulator/Emulator \
  -stop "<new-hvd-name>" \
  -path "$HOME/.Huawei/Emulator/deployed"
```

### 删除测试实例

如果不需要保留测试实例，先停止它，再通过受控清理工具删除实例数据和注册信息。该动作必须在用户确认后执行，并记录被删除的实例名、备份位置和恢复策略。下面是概念性调用形态，不代表仓库内已有 `hvd-delete` 命令：

```text
<受控清理工具> --name "<new-hvd-name>" --require-confirm
```

注意：删除命令会移除新实例数据，执行前确认 `NEW_NAME` 是测试实例，不要误删原实例。

### HVD 元数据边界

HVD 能否被列出、能否启动、能否通过 HDC 连接，依赖多份本地实例数据的一致性。公开文档只保留以下结论：

- 只创建声明信息不足以保证实例可启动。
- 复制同版本可启动实例并刷新必要元数据，是当前已验证的可行方向。
- 受控工具必须先备份、再修改、再验证 `Emulator -list -details`、启动日志和 HDC 连接状态。
- 删除或清理实例属于破坏性动作，脚本必须先确认目标是测试实例。

### 硬件与名称约束

以下约束经公开可操作界面验证，只作为手工创建 HVD 的保守建议：

- HVD 名称只能包含字母、空格、数字、下划线。
- HVD 名称长度为 1-60。
- RAM 最小值：2GB。
- ROM 最小值：2GB。
- ROM 最大值：1023GB。
- 手机 / 折叠屏屏幕尺寸：3.5-9 inch。
- 平板屏幕尺寸：8-15 inch。
- PC 屏幕尺寸：10-20 inch。
- 手机 / 折叠屏分辨率宽高：720-3500 px。
- PC 分辨率宽高：1000-4000 px。
- DPI 范围：240-640。

这些约束来自可操作界面校验；手工改配置可能绕过校验，但不代表 Emulator 一定能启动。

### 模板与能力边界

已确认 Emulator 具备预置设备模板、版本信息、传感器配置和排障入口；文档只记录能力结论，不记录文件定位信息。

当前命令级结论：

- Emulator 版本：`6.0.2.200`。
- 模板覆盖：API 12-16 的 `phone`、`foldable`、`tablet` 等设备类型。
- 传感器覆盖：phone 常见传感器包括计步、光照、加速度、霍尔、重力、旋转向量、方向、陀螺仪、磁场；foldable 还涉及姿态/扩展霍尔等能力。
- 排障方向覆盖：镜像无效、SDK 路径变化、设备不存在、GPU 驱动不支持、内存不足、bundle 安装错误等。

## 桌面窗口辅助操作

模拟器窗口可能出现在外接屏或不可见区域。可用 macOS 辅助功能移动窗口：

```bash
osascript -e 'tell application "System Events" to tell process "Emulator" to get {position of window 1, size of window 1, value of attribute "AXMinimized" of window 1}'

osascript -e 'tell application "System Events" to tell process "Emulator" to set position of window 1 to {120, 120}'

osascript -e 'tell application "System Events" to tell process "Emulator" to perform action "AXRaise" of window 1'
```

截图确认：

```bash
screencapture -x /tmp/harmony-emulator-visible.png
```

当前验证中，Computer Use 插件对 app 名称 `Emulator` 返回 `Invalid app`，但系统进程与窗口均存在。因此优先走 `hdc + uitest`，必要时再用 `osascript` 或截图辅助定位桌面窗口。

## 已确认的增强能力

### Emulator

可用命令包括：

```bash
/Applications/DevEco-Studio.app/Contents/tools/emulator/Emulator -list -details
```

该命令会输出 JSON，包含每个 HVD 的名称、运行状态、实例位置、镜像位置、端口、屏幕、内存、CPU、系统版本等摘要信息，比普通 `-list` 更适合脚本自动发现和选择模拟器。字段名以当前版本输出为准，文档不固定内部字段清单。

`Emulator -logZip <name> -logPath <path>` 可收集模拟器日志，适合 CI 失败后自动归档。

`Emulator -hdcport <port>` 可以让多个模拟器使用不同 hdc 端口，避免默认 `5555` 冲突。端口范围为 `10000~16555`。

`Emulator -version` 已验证：

```text
HarmonyOS Emulator :6.0.2.200
```

当前只把以下入口视为可沉淀、可脚本化的 Emulator 侧能力：启动、停止、版本、帮助、列表、详情列表、日志收集、HDC 端口。未发现公开稳定的 `create`、`edit`、`wipe` 等 CLI 子命令。

多实例建议：

```bash
/Applications/DevEco-Studio.app/Contents/tools/emulator/Emulator \
  -hvd "<实例名>" \
  -path "$HOME/.Huawei/Emulator/deployed" \
  -t "<trace-name>" \
  -imageRoot "$HOME/Library/Huawei/Sdk" \
  -hdcport <port>
```

- 单实例通常可使用默认 HDC 端口。
- 多实例必须显式传 `-hdcport`，建议从 `10100` 起递增，例如 `10100`、`10101`、`10102`。
- 连接目标固定为 `127.0.0.1:<hdcport>`。
- 启动前后都用 `hdc list targets -v` 确认目标状态，避免 AI 操作打到错误实例。
- 不建议直接修改实例配置内的端口字段；端口按启动参数管理更清晰。

`hdc list targets -v` 会暴露目标连接状态。目标状态示例：

```text
127.0.0.1:<port-a>    TCP    Offline      localhost
127.0.0.1:<port-b>    TCP    Connected    localhost
```

这说明停止过的多开实例可能留下 offline 记录，脚本应只选择 `Connected` 目标。

运行态端口结论：

当前版本可观察到本机 HDC 监听：

```text
TCP 127.0.0.1:<hdc-port> (LISTEN)
TCP 127.0.0.1:<hdc-port>->127.0.0.1:<hdc-client-port> (ESTABLISHED)
```

网络控制能力未纳入稳定自动化契约，第一版 runner 只依赖 HDC target。

若需要完全离线或可审计的 CI 环境，应额外用防火墙/网络隔离验证 Emulator 在离线模式下的行为。

### Emulator UI 能力线索

Emulator UI 覆盖的能力比第一版脚本需要的能力更多，但当前不把 UI 面板能力作为稳定自动化协议。本文只沉淀命令级结论和可验证风险边界。

可作为后续验证方向的能力：

- 电池：电量、充电/放电状态。
- GPS：经度、纬度、方向、海拔。
- 虚拟传感器：光照、温度、湿度、心率等。
- 车机数据：驱动、座舱、车身等车辆属性。
- 多屏/折叠：添加显示屏、折叠/展开/半折叠、主屏/副屏/协同屏。
- 网络代理：将宿主代理配置同步给模拟器。
- 截图/日志：截图、bugreport、日志打包。
- 拖拽安装/推送：HAP/HSP 安装、文件或目录推送。

当前判断：

- 这些能力适合作为后续探索线索，但不适合作为第一版脚本依赖。
- 第一版 AI 自动化仍应依赖 `hdc + uitest + aa/bm/hilog/hidumper`。
- 多屏/折叠、截图、日志、安装等部分能力可以通过设备侧命令稳定复现，优先走设备侧命令。

拖拽安装可以绕开 UI 复现为命令行。该块属于用户确认档，因为它会写设备文件并安装应用：

```bash
HDC="/Applications/DevEco-Studio.app/Contents/sdk/default/openharmony/toolchains/hdc"
TARGET="127.0.0.1:<hdc-port>"

"$HDC" -t "$TARGET" file send ./demo.hap /data/local/tmp/demo.hap
"$HDC" -t "$TARGET" shell bm install -p /data/local/tmp/demo.hap
```

拖拽安装有文件大小和格式限制。脚本化时建议先检查文件后缀、大小和 `bm install` 返回值。

### hdc

`hdc help verbose` 比普通 help 多出不少能力：

```bash
hdc discover
hdc list targets -v
hdc tconn <ip:port>
hdc -s [ip:]port
hdc -e <ip>
hdc fport localnode remotenode
hdc rport remotenode localnode
hdc bugreport [FILE]
hdc jpid
hdc track-jpid [-a|-p]
hdc shell -b <bundleName> <COMMAND>
```

用途：

- `discover`：局域网发现 TCP 设备。
- `list targets -v`：输出更详细设备状态。
- `tconn`：连接远程设备或 TCP 设备。
- `fport/rport`：正向/反向端口转发，可转发 `tcp`、Unix socket、`jdwp`、`ark:pid@tid@Debugger`。
- `bugreport`：抓完整设备诊断信息。
- `jpid/track-jpid`：发现可调试进程。
- `shell -b <bundleName>`：在指定调试应用 bundle 路径下执行非交互命令。

已验证：

```bash
hdc checkserver
hdc -t 127.0.0.1:<hdc-port> fport ls
hdc -t 127.0.0.1:<hdc-port> jpid
hdc -t 127.0.0.1:<hdc-port> shell -b <bundle-name> pwd
```

结果：

- `checkserver` 可确认 client/server 版本一致。
- `fport ls` 无端口转发时返回 `[Empty]`。
- `jpid` 可列出可调试进程 PID。
- `track-jpid` 可监听可调试进程变化，但必须配合超时，不能作为常驻阻塞命令。
- `shell -b <bundle-name> pwd` 适合在调试应用目录下执行只读排查命令；真实路径不写入文档。
- `shell -b <bundle>` 只建议先做 `pwd` 这种只读探测；后续若要 `ls/cat/file recv` 沙箱内容，需要单独确认范围。
- `checkdevice` 在当前 TCP 模拟器目标上返回 `CreateConnect failed`，不适合作为模拟器健康检查；优先使用 `hdc list targets -v` 和 `shell` 探活。

高风险命令：

```bash
hdc target mount
hdc smode
hdc flash
hdc erase
hdc format
hdc sideload
```

这些会影响系统分区、root/daemon 状态或刷写系统镜像，除非明确要做系统级调试，否则不要在日常 AI 自动化里使用。

网络与端口转发：

```bash
hdc fport ls
hdc -t 127.0.0.1:<hdc-port> fport ls
hdc -t 127.0.0.1:<hdc-port> jpid
hdc -t 127.0.0.1:<hdc-port> shell ifconfig
hdc -t 127.0.0.1:<hdc-port> shell netstat -an
hdc -t 127.0.0.1:<hdc-port> shell hidumper --net <pid>
```

结论：

- `fport ls` 可确认是否存在 forward/reverse 任务；当前无任务时返回 `[Empty]`。
- `fport` / `rport` 支持 TCP、Unix socket、`jdwp:<pid>`、`ark:pid@tid@Debugger` 等节点，但新增/删除转发会改变连接状态，默认不执行。
- `tconn <ip:port>`、`discover` 会改变连接列表或产生局域网广播，默认不执行。
- `ifconfig` 可看设备 NAT 网卡；`ip addr` 在当前设备侧不可用。
- `netstat -an` 可能包含外部 IP、内部 socket 路径；默认只做人工诊断，不写完整原文。
- `hidumper --net <pid>` 适合纳入单进程资源验收；不建议默认跑无 PID 的全局网络诊断。

### uitest

`uitest` 不只是点坐标，还能做 UI 树、截图、录制：

以下为设备侧子命令形态；runner 执行时必须统一加 `"$HDC" -t "$TARGET" shell`。

```bash
uitest dumpLayout -p /dev/null -a
uitest dumpLayout -p /data/local/tmp/layout.json
uitest dumpLayout -a
uitest dumpLayout -b <bundleName>
uitest dumpLayout -w <windowId>
uitest screenCap -p /data/local/tmp/screen.png
uitest uiRecord record -W true -l -c true
uitest uiRecord read
uitest uiInput click <x> <y>
uitest uiInput doubleClick <x> <y>
uitest uiInput longClick <x> <y>
uitest uiInput swipe <from_x> <from_y> <to_x> <to_y>
uitest uiInput drag <from_x> <from_y> <to_x> <to_y>
uitest uiInput keyEvent Home
uitest uiInput keyEvent Back
uitest uiInput inputText <x> <y> <text>
uitest uiInput text <text>
```

对 AI 最有价值的是：

- `dumpLayout -a`：连字体属性一起导出。
- `dumpLayout -b`：只看目标应用窗口。
- `dumpLayout -p /dev/null -a`：可作为能力探测，不拿真实布局内容。
- `screenCap -p /dev/null`：可作为截图能力探测，不生成可拉取截图。
- `uiRecord record -W true -l -c true`：录制人工操作，同时保存控件信息和每步布局。

注意：

- 真正给 AI 解析 UI 树时，仍建议写入 `/data/local/tmp/layout.json` 后用 `hdc file recv` 拉回。
- `dumpLayout -a` 不指定 `-p` 会在设备侧生成 `/data/local/tmp/layout_*.json`。
- `dumpLayout -i` 在当前环境有超时风险，不建议默认使用。
- 写入 `/data/local/tmp/*.json` 或 `/data/local/tmp/*.png` 属于真实采集，可能包含 UI 文本或屏幕内容；默认只用 `/dev/null` 探测，真实采集进入用户确认档。

### 设备侧诊断命令

模拟器内已确认存在：

```bash
aa
bm
hilog
hidumper
param
power-shell
snapshot_display
uinput
uitest
wukong
```

底层输入变体不作为稳定入口沉淀。普通 UI 自动化优先使用 `uitest uiInput`。

常用能力：

- `bm dump`：查看 bundle 信息。
- `bm dump -g`：列出 debug bundle。
- `aa start`：命令行启动 Ability。
- `aa test`：启动测试框架。
- `hidumper --mem`、`--cpuusage`、`--net`、`--storage`：抓性能/资源信息。
- `hidumper -ls`：列出 system abilities。
- `param get/ls/wait`：读取或等待系统参数。
- `hilog -z <n>`：读取最近 n 行日志。
- `hilog -w start`：启动日志落盘任务。
- `snapshot_display -f <file>`：系统级截图。
- `power-shell wakeup/suspend/timeout`：控制屏幕唤醒、休眠、熄屏时间。

注意：`param set`、`bm clean`、`aa force-stop`、`power-shell suspend`、`wukong exec` 都会改变设备状态，默认不执行。使用前应明确目标、用户确认和恢复动作。

应用与包诊断补充：

以下为设备侧子命令形态；runner 执行时必须统一加 `"$HDC" -t "$TARGET" shell`。

```bash
aa appdebug --help
aa process --help
aa test --help
aa dump -i <abilityRecordId>
aa dump -a
bm dump -n <bundleName>
bm dump-dependencies -n <bundleName> -m <moduleName>
bm dump-shared -n <bundleName>
bm get -u
```

说明：

- `aa dump -i` 可按 AbilityRecordId 精确查询单个 ability。
- `aa dump -a` 输出较多，只建议失败诊断使用。
- `aa appdebug`、`aa process`、`aa test` 的 help 可用于能力发现；真实执行会改变调试状态、目标进程或启动测试框架，默认不执行。
- `bm dump -n` 可能包含路径、签名、metadata、URI skill 等信息，写入日志或文档前应裁剪脱敏。
- `bm dump-dependencies` 和 `bm dump-shared` 可用于依赖/共享库诊断，真实输出同样需要裁剪脱敏。
- `bm get -u` 会输出设备 UDID，默认不应写入公开文档。

更细的 help 入口：

以下为设备侧子命令形态；runner 执行时必须统一加 `"$HDC" -t "$TARGET" shell`。

```bash
uitest help
uitest uiInput help
aa help
bm help
hidumper -h
hilog -h
wukong help
power-shell help
param
snapshot_display
```

建议的 AI 自动化分层：

- 发现设备：`Emulator -list -details`、`hdc list targets -v`。
- 启停模拟器：`Emulator -hvd ... -t ... -imageRoot ...`、`Emulator -stop <name> -path <root>`。
- UI 观察：`uitest dumpLayout -p /dev/null -a`、`uitest screenCap -p /dev/null` 做能力探测；真实采集走用户确认档。
- UI 操作：`uitest uiInput`。
- 应用生命周期：`aa start`、`aa dump`；`aa force-stop` 需要用户确认。
- 包管理：`bm install`、`bm uninstall`、`bm dump`。
- 日志：默认使用 `hilog -z <n>`；`hilog -x` 输出可能很大，进入用户确认档。
- 性能诊断：`hidumper --mem`、`--cpuusage`、`--net`、`--storage`。
- 压测：`wukong exec/special/focus` 默认禁止，仅在用户明确要求随机压力测试时使用。

## AI Runner 执行模型

未来封装 runner 时，建议把每次执行抽象为一个 `run_id`。格式建议为 `YYYYMMDD-HHMMSS-<short-random>`，贯穿命令日志、临时文件名、trace name、失败包和 artifact manifest。

`run_id` 生成后必须检查 `.ai-runs/<run_id>/` 不存在；若冲突，重新生成。`run.json` 至少记录：

```json
{
  "schema_version": "1",
  "run_id": "20260518-143012-a8f3c1",
  "runner_version": "<runner-version>",
  "created_at": "<iso8601>",
  "inputs": {
    "hvd_name": "<hvd-name>",
    "target": "127.0.0.1:<hdc-port>",
    "bundle": "<bundle-name>"
  },
  "budgets": {
    "total_timeout_ms": 300000,
    "boot_timeout_ms": 120000,
    "launch_timeout_ms": 30000,
    "ui_step_timeout_ms": 20000
  },
  "trace_pipe_helper": {
    "trace_name": "<trace-name>",
    "pid": "<pid>",
    "owned_by_run_id": true,
    "cleanup_status": "pending"
  },
  "final_status": "running",
  "failure_type": null,
  "commands_path": "commands.jsonl",
  "artifacts_path": "artifacts.json",
  "confirmations_path": "confirmations.jsonl"
}
```

每条命令写入 JSONL 记录，保存 argv 数组而不是单条 shell 字符串：

```json
{
  "schema_version": "1",
  "run_id": "20260518-143012-a8f3c1",
  "step_id": "dump-ui",
  "parent_step_id": null,
  "retry_index": 0,
  "command": ["hdc", "-t", "127.0.0.1:<hdc-port>", "shell", "uitest", "dumpLayout", "-p", "/dev/null", "-a"],
  "cwd": "<runner-cwd>",
  "env_allowlist": ["HDC", "TARGET"],
  "target": "127.0.0.1:<hdc-port>",
  "started_at": "<iso8601>",
  "ended_at": "<iso8601>",
  "duration_ms": 421,
  "timeout_ms": 10000,
  "status": "success",
  "exit_code": 0,
  "signal": null,
  "stdout_summary": "<redacted-summary>",
  "stderr_summary": "<redacted-summary>",
  "risk_level": "allow",
  "risk_gate_decision": "allow",
  "artifact_refs": [],
  "redaction_status": "summary-only",
  "raw_output_retention": "discarded"
}
```

Runner 状态机：

1. 生成 `run_id` 和唯一 `trace_name`。
2. 启动并记录 trace pipe helper；helper 异常退出时终止本轮 run。
3. 启动 Emulator。
4. 选择显式 target；多 target 且未指定时停止。
5. 等待 HDC connected 与 boot completed。
6. 执行应用启动、UI 探测、输入和验收。
7. 按失败类型采集诊断摘要。
8. 清理本轮临时文件和 trace pipe helper。

确认档升级流程：

- 命令执行前先跑 `risk-gate`，结果只能是 `allow`、`require_confirm`、`deny`。
- `require_confirm` 时暂停 runner，只展示目标、命令类别、预期写入位置、脱敏摘要和回滚策略。
- 用户确认只对当前 `run_id` 生效；用户拒绝后降级为只读诊断或直接停止。
- 无法识别目标、无法判断是否写设备/写宿主、包含通配删除、刷写、清数据、卸载、端口转发修改时，默认升级为 `require_confirm` 或 `deny`。

确认事件写入 `confirmations.jsonl`：

```json
{
  "schema_version": "1",
  "run_id": "20260518-143012-a8f3c1",
  "confirmation_id": "confirm-001",
  "requested_at": "<iso8601>",
  "resolved_at": "<iso8601>",
  "scope": "current-run",
  "requested_action": "capture-real-screenshot",
  "command_hash": "<sha256-of-argv>",
  "decision": "approved",
  "approved_by": "user",
  "expires_at": "<iso8601>",
  "denial_reason": null,
  "fallback_action": null
}
```

## AI 自动化标准链路

以下链路适合封装成脚本或 skill。变量：

```bash
HDC="/Applications/DevEco-Studio.app/Contents/sdk/default/openharmony/toolchains/hdc"
TARGET="127.0.0.1:<hdc-port>"
BUNDLE="<bundleName>"
```

### 1. 选择 Connected target

```bash
"$HDC" list targets -v
```

规则：

- 没有 `Connected`：停止，模拟器未就绪或 HDC 未连接。
- 多个 `Connected`：必须使用显式传入的 target；未指定 target 时停止并输出候选列表，不默认选择第一个目标。
- 忽略 `Offline` 目标。

### 2. 等待系统启动完成

```bash
"$HDC" -t "$TARGET" shell param get bootevent.boot.completed
```

期望返回 `true`。如果 key 不可用，回退到 Emulator 日志中的 `Guest OS Boot Completed!!` 摘要。轮询顺序为：先等待 `hdc list targets -v` 出现指定 `TCP Connected`，再轮询 boot 参数；任一阶段超过总超时后，只采集连接状态、boot 状态和最近日志摘要，不进入 UI 输入。

### 3. 启动目标应用

先查询 bundle：

```bash
"$HDC" -t "$TARGET" shell bm dump -n "$BUNDLE"
```

再启动：

```bash
ABILITY="<ability-name>"
"$HDC" -t "$TARGET" shell aa start -b "$BUNDLE" -a "$ABILITY"
```

如果不知道 Ability，先从 `bm dump -n` 的裁剪输出中提取 `mainAbility` / `mainElementName` / `abilityInfos[].name`。

### 4. 查前台窗口与 PID

```bash
"$HDC" -t "$TARGET" shell aa dump -l
"$HDC" -t "$TARGET" shell aa dump -r
"$HDC" -t "$TARGET" shell hidumper -ls
```

用于确认：

- bundle 是否为 `FOREGROUND`。
- PID 是否存在。
- 窗口诊断项是否能提供焦点窗口、窗口 bounds、display id 等摘要。具体 service 名称由 `hidumper -ls` 动态发现，不在文档中固定。

### 5. 获取 UI 树与截图

真实采集，需用户确认：

```bash
"$HDC" -t "$TARGET" shell uitest dumpLayout -p /data/local/tmp/ai-layout.json -a
"$HDC" -t "$TARGET" shell cat /data/local/tmp/ai-layout.json
"$HDC" -t "$TARGET" shell uitest screenCap -p /data/local/tmp/ai-screen.png
"$HDC" -t "$TARGET" file recv /data/local/tmp/ai-screen.png ./ai-screen.png
```

能力探测：

```bash
"$HDC" -t "$TARGET" shell uitest dumpLayout -p /dev/null -a
"$HDC" -t "$TARGET" shell uitest screenCap -p /dev/null
```

### 6. 执行输入

```bash
"$HDC" -t "$TARGET" shell uitest uiInput click <x> <y>
"$HDC" -t "$TARGET" shell uitest uiInput swipe <x1> <y1> <x2> <y2>
"$HDC" -t "$TARGET" shell uitest uiInput keyEvent Back
"$HDC" -t "$TARGET" shell uitest uiInput text "<text>"
```

约束：

- 坐标必须来自当前 UI 树或截图。
- 每步输入后重新 dump layout 或截图确认。
- 复杂多指/鼠标/手写笔场景再考虑 `uinput`，默认不用。
- 执行输入前必须校验坐标落在当前 display/window bounds 内，并记录来源节点；文本输入必须经过 shell 参数转义，禁止把未经处理的用户文本直接拼接进命令字符串。

### 7. 资源与日志验收

```bash
"$HDC" -t "$TARGET" shell hilog -z 100 -P <pid>
"$HDC" -t "$TARGET" shell hidumper --cpuusage <pid>
"$HDC" -t "$TARGET" shell hidumper --mem <pid> --prune
"$HDC" -t "$TARGET" shell hidumper --net <pid>
"$HDC" -t "$TARGET" shell hidumper --storage <pid>
```

默认按 PID 采集，避免全局输出过大。

## 失败诊断包

默认档：只读、无真实截图/布局附件、低泄露风险。

```bash
HDC="/Applications/DevEco-Studio.app/Contents/sdk/default/openharmony/toolchains/hdc"

"$HDC" list targets -v
"$HDC" -t "$TARGET" shell param get bootevent.boot.completed
"$HDC" -t "$TARGET" shell uitest dumpLayout -p /dev/null -a
"$HDC" -t "$TARGET" shell uitest screenCap -p /dev/null
"$HDC" -t "$TARGET" shell aa dump -l
"$HDC" -t "$TARGET" shell aa dump -r
"$HDC" -t "$TARGET" shell bm dump -g
```

增强档：仍只读，但信息更多。

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

脱敏建议：

- 日志只保留时间、level、tag、错误码、异常摘要；过滤 token、手机号、邮箱、URL query、cookie、业务 payload。
- 包信息保留 bundle、version、debug 状态、module、ability；裁剪签名、安装路径、metadata、业务 URI。
- 窗口/显示保留窗口名、PID、焦点窗口、尺寸、旋转；不记录完整 UI 文本。
- 截图/布局默认不采真实内容；用户确认后作为附件采集。

## 控件定位策略

推荐用窗口和无障碍状态给 `uitest` 限定范围，减少盲点风险：

```bash
"$HDC" -t "$TARGET" shell aa dump -l
"$HDC" -t "$TARGET" shell hidumper -ls
"$HDC" -t "$TARGET" shell uitest dumpLayout -p /data/local/tmp/layout.json -w <windowId>
"$HDC" -t "$TARGET" shell uitest uiInput click <centerX> <centerY>
```

定位步骤：

1. `aa dump -l` 确认前台 bundle / ability。
2. 通过窗口诊断项找到 focus window，记录 display、window id、bounds、Z 序等摘要。
3. 通过无障碍诊断项确认 active window 与 focus window 一致。
4. `uitest dumpLayout -w <windowId>` 获取目标窗口 UI 树。
5. 从目标 node bounds 计算中心点。
6. 点击后重新跑 `aa dump -l`、active window、dump layout，确认状态变化。

已验证：

- `dumpLayout -p /dev/null -b <bundle>` 可做能力探测。
- `dumpLayout -p /dev/null -w <windowId>` 可做窗口级能力探测。
- `dumpLayout -b/-w` 叠加 `-a` 在当前环境出现超时，不建议默认组合使用。

停止条件：

- `hdc list targets -v` 不是 `Connected`。
- `bootevent.boot.completed` 不是 `true`。
- `dumpLayout` 和 `screenCap` 都失败。
- `aa dump -r` 找不到目标进程。
- 任一命令持续输出或超过预期时间。
- 输出出现明显敏感业务数据。

### uinput 底层输入

`uinput` 是比 `uitest uiInput` 更底层的输入注入入口。它只作为用户确认档兜底能力，不进入默认自动化链路；内部变体不在文档沉淀。

```bash
"$HDC" -t "$TARGET" shell uinput
"$HDC" -t "$TARGET" shell uinput -T -c 20 20
"$HDC" -t "$TARGET" shell uinput -K -t "hello"
```

建议：

- 默认优先 `uitest uiInput`，因为命令简单、返回稳定。
- `uinput` 适合作为兜底能力，用于 `uitest` 不覆盖的底层输入场景。
- `uinput` 是纯坐标/设备事件注入，不理解控件语义；自动化前应先用 `dumpLayout` 或截图定位。

### screenshot / snapshot

截图有两条稳定路径。以下命令属于用户确认档，因为会生成真实屏幕内容：

```bash
"$HDC" -t "$TARGET" shell uitest screenCap -p /data/local/tmp/screen.png
"$HDC" -t "$TARGET" shell snapshot_display -i 0 -f /data/local/tmp/snapshot_display.jpeg -w 1308 -h 2880 -t jpeg
```

验证结果：

- `uitest screenCap` 会报告保存到设备侧路径，但不同版本上实际文件位置可能需要再确认。
- `snapshot_display` 可生成截图，并可通过 `hdc file recv` 拉回本地。
- `snapshot_display` 对后缀/类型较严格，JPEG 输出文件应使用 `.jpeg` 后缀。

### hidumper system abilities

`hidumper -ls` 能列出设备侧 system ability。具体 service 名称和参数以当前版本动态发现为准，文档不固定内部符号清单。

对模拟器控制和诊断最有价值的能力类别：

- 窗口诊断：窗口列表、窗口 id、display id、pid、bounds、焦点窗口。
- 显示诊断：屏幕、旋转、折叠/展开、亮度和显示电源状态。
- 电池/温度/传感器诊断：容量、充电状态、温度、常见传感器枚举。
- 无障碍/输入诊断：active window、输入设备、最近输入事件摘要。
- `hidumper -e --list -n 5` 可查近期异常退出摘要；可能包含系统历史故障信息，失败诊断时再采集。

### power-shell

`power-shell` 可以控制屏幕唤醒、休眠、熄屏时间和电源模式：

```bash
"$HDC" -t "$TARGET" shell power-shell help
"$HDC" -t "$TARGET" shell power-shell wakeup
```

已验证：

- `wakeup` 返回 `WakeupDevice is called`。

风险：

- `suspend` 会让屏幕休眠，自动化中可能导致后续 UI 命令不可见。
- `setmode` 会影响电源策略，常规 UI 自动化不建议修改。
- `timeout -o <ms>` 使用前应记录当前屏幕超时，执行后立即用 `timeout -r` 恢复。

### hitrace

`hitrace` 适合短时采集系统级性能 trace：

```bash
"$HDC" -t "$TARGET" shell hitrace --help
"$HDC" -t "$TARGET" shell hitrace -l
"$HDC" -t "$TARGET" shell hitrace -t 1 window multimodalinput app
```

已确认分类包括 `ability`、`app`、`ark`、`graphic`、`multimodalinput`、`sensors`、`window`、`power`、`net`、`sched`、`memory` 等。

建议：

- 只在性能诊断时短时启用。
- 不要在普通 AI UI 自动化里默认开启长时间 trace。
- 若写入文件，需要先验证输出路径是否实际可通过 `hdc file recv` 取回。

### 压测、录制、测试入口

这些能力存在，但不进入默认 AI 自动化链路：

```bash
"$HDC" -t "$TARGET" shell wukong help
"$HDC" -t "$TARGET" shell wukong --version
"$HDC" -t "$TARGET" shell wukong appinfo
"$HDC" -t "$TARGET" shell wukong exec <options>
"$HDC" -t "$TARGET" shell wukong special <options>
"$HDC" -t "$TARGET" shell wukong focus <options>
"$HDC" -t "$TARGET" shell uitest uiRecord read
"$HDC" -t "$TARGET" shell uitest uiRecord record -W true -l -c true
"$HDC" -t "$TARGET" shell uitest start-daemon <token>
"$HDC" -t "$TARGET" shell aa test -b <bundle> -m <module> -s unittest <test-runner> -s class <test-class> -w <seconds>
```

建议：

- `wukong appinfo` 可作为只读应用入口发现，输出需要裁剪。
- `wukong exec/special/focus` 会大量操作 UI，默认禁止。
- `uitest uiRecord record` 会写录制文件、可保存布局、可能持续采集，需要用户确认。
- `uitest start-daemon` 会启动后台测试进程，默认禁止。
- `aa test` 会启动测试框架，只有用户明确要求跑测试时执行。

### 命令风险分级

稳定推荐：

- `Emulator -list -details`
- `hdc list targets -v`
- `uitest dumpLayout -p /dev/null -a`
- `uitest uiInput`
- `snapshot_display` 能力探测
- `aa dump`
- `bm dump`
- `hilog -z <n>`
- `hidumper --cpuusage` / `--mem` / `--net` / `--storage`

可用但需谨慎：

- `aa start`

默认禁止，除非明确进入系统级调试：

- `hdc target mount`
- `hdc smode`
- `hdc flash`
- `hdc erase`
- `hdc format`
- `hdc sideload`
- `param set`
- `bm clean`
- `wukong exec/special/focus`

### AI 自动化 Guardrails

默认白名单：

```bash
Emulator -version
Emulator -list
Emulator -list -details
hdc list targets -v
hdc wait
param get <white-listed-key>
hilog -z <n>
aa dump -l
aa dump -r
bm dump -a
bm dump -g
hidumper --cpuusage
hidumper --mem --prune
uitest dumpLayout -p /dev/null -a
uitest screenCap -p /dev/null
uitest uiInput click/swipe/drag/text/keyEvent Back/Home
power-shell wakeup
```

每次输入前的检查顺序：

1. `hdc list targets -v` 必须有 `Connected`。
2. `param get bootevent.boot.completed` 应为完成态；若 key 不存在或为空，回退查 Emulator 日志中的 `Guest OS Boot Completed!!`。
3. `power-shell wakeup` 保证屏幕可见。
4. `uitest dumpLayout -p /dev/null -a` 或 `uitest screenCap -p /dev/null` 先确认能力；真实内容采集需要进入确认档。
5. 坐标必须来自当前布局或截图，不做盲点。

失败恢复顺序：

1. `hdc wait`
2. `power-shell wakeup`
3. `uitest uiInput keyEvent Home`
4. 重新 `dumpLayout` 或 `screenCap`
5. 仍失败时停止自动化，等待用户确认是否重启或重开模拟器。

需要用户确认：

- 启停模拟器。
- 安装、卸载、清数据。
- `hdc file send` 写设备文件。
- `Emulator -logZip` 或大范围日志打包。
- 真实 `dumpLayout` / `screenCap` 文件和 `file recv` 拉取。
- `bm install` / `bm uninstall`。
- `hilog -x`。
- `hitrace` 采样。
- `uinput` 底层输入。
- `aa force-stop`、`power-shell timeout/suspend/setmode`、DisplayManager 折叠/显示模式切换。

### 参数白名单

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

不建议默认读取或落文档：

- `*udid*`、`*uuid*`、`*serial*`、`*sn*`。
- `*account*`、`*user*`、`*token*`、`*auth*`。
- `*wifi*`、`*wlan*`、`*mac*`、`*ip*`。
- 全量 `param get` 输出。

### 超时与防卡死

所有自动化命令必须由上层 runner 设置超时。

| 场景 | 建议 timeout | 超时处理 |
| --- | ---: | --- |
| `hdc list targets -v` | 5s | 终止本轮自动化 |
| `param get bootevent.boot.completed` | 3s，轮询总时长 60-120s | 超时终止 UI 操作 |
| `uitest dumpLayout -p /dev/null -a` | 10s | 跳过结构化 UI，改用截图/日志 |
| `uitest screenCap -p /dev/null` | 10s | 跳过截图，保留日志诊断 |
| `aa dump -l` / `aa dump -r` | 8s | 跳过输入动作 |
| `bm dump -g` / `bm dump -n <bundle>` | 8s | 裁剪输出；超时跳过 |
| 窗口诊断项 | 8s | 降级只看 `aa dump` |
| `hidumper --cpuusage <pid>` / `--mem <pid>` | 8s | 跳过该指标 |
| `hilog -z 100 -P <pid>` | 5s | 保留已收集内容 |
| `track-jpid` 短监听 | 3s | 超时视为采样结束 |

默认禁止无限流或后台任务：

- `hilog` 不带 `-z` / `-x`。
- 无超时的 `track-jpid`。
- `hitrace --record`、`--trace_begin`、`--start_bgsrv`。
- `wukong exec/special/focus`。
- `uitest uiRecord record`。
- `uitest start-daemon`。

Runner 预算：

- 单次普通 UI run 总预算建议 5 分钟；包含启动模拟器的 run 建议 15 分钟。
- 阶段预算建议：boot 120s，app launch 30s，单个 UI step 20s，失败诊断 30s。
- 允许重试的只限只读探测和 `Back/Home/wakeup` 这类低风险恢复动作；每类最多 2 次，重试间隔递增。
- 超时状态统一记录为 `timeout`、`skipped`、`degraded` 或 `aborted`，不得静默继续。
- 子步骤预算从父阶段预算中扣减；重试、诊断和清理都必须扣总预算。
- 后台 helper 必须有健康检查预算；helper 超时或异常退出时，本轮状态转为 `aborted`。
- 清理阶段也必须设置超时；清理失败记录为 `cleanup_failed`，不得反复阻塞。

### 脱敏规则

默认文档只保存能力、状态、错误摘要、资源数值和可复现命令模板，不保存完整原始输出。

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

脱敏执行顺序：

1. 原始输出先进入本轮临时区。
2. 先生成摘要和 mask 后文本。
3. 默认只落摘要。
4. 原始文件仅在用户确认档保留。
5. 脱敏失败时禁止归档原文。

推荐 mask：`<redacted:phone>`、`<redacted:email>`、`<redacted:token>`、`<redacted:url-query>`、`<redacted:path>`、`<redacted:payload>`。

脱敏规则必须有版本号，并同时作用于 `stdout_summary`、`stderr_summary`、命令记录和 artifact 摘要。脱敏前后 artifact 要通过 `source_artifact_id` 关联；脱敏失败时删除原始 artifact 或标记为 `delete-pending`，禁止移动到 `docs-linhay/`。

### 解析规则

`hdc list targets -v`：

```text
^(\S+)\s+(USB|TCP)\s+(Connected|Offline|Unauthorized|Unknown)\s*(.*)$
```

选择 `state == Connected` 的目标；多实例时优先匹配显式 target。

`Emulator -list -details`：解析 JSON 数组，读取 HVD 名称、运行状态、实例位置、镜像位置和 HDC 端口等摘要字段。字段名以当前版本输出为准，运行状态为真值时视为运行中。

`aa dump -l`：提取 `Mission ID`、`AbilityRecord ID`、`app name`、`main name`、`bundle name`、`state`、`app state`。`state == FOREGROUND && app state == FOREGROUND` 视为前台。

`aa dump -r`：提取 `process name`、`pid`、`uid`、`state`。优先选择 `processName == bundle && state == FOREGROUND` 的 PID。

窗口诊断项：提取 focus window、display、pid、bounds 等摘要。

无障碍诊断项：提取 active window，与 focus window 一致才继续点击。

`hilog`：推荐 `hilog -z <n> -P <pid> -L E`，按 level `E/F` 聚合错误，写文档前先脱敏。

资源阈值建议：

- CPU `total >= 80%` 连续 3 次：`high_cpu`。
- CPU `total >= 50%` 连续 5 次：`suspicious_cpu`。
- PSS `>= 800000 KB`：`high_memory`。
- swap 持续增长：`memory_pressure`。

## Runner 文件落盘规范

默认不把 runner 产物写入 git。临时运行目录建议：

```text
.ai-runs/<run_id>/
  run.json
  commands.jsonl
  artifacts.json
  logs/
  ui/
  screenshots/
  failure-package/
```

如果产物需要沉淀到 `docs-linhay/`，必须先按用户确认档处理并脱敏；截图统一进入 `docs-linhay/screenshots/YYYYMMDD/<module>/`。

`artifacts.json` 建议使用 manifest 顶层结构：

```json
{
  "schema_version": "1",
  "run_id": "20260518-143012-a8f3c1",
  "created_at": "<iso8601>",
  "artifacts": [
    {
      "artifact_id": "art-001",
      "type": "screenshot",
      "path": ".ai-runs/<run_id>/screenshots/screen.png",
      "size_bytes": 12345,
      "sha256": "<sha256>",
      "sensitivity": "high",
      "requires_user_confirm": true,
      "redaction_status": "summary-only",
      "source_artifact_id": null,
      "source_command_step_id": "capture-screen",
      "confirmation_id": "confirm-001",
      "retention_policy": "delete-after-run-unless-confirmed",
      "retention_status": "delete-pending"
    }
  ]
}
```

失败类型与采集矩阵：

| 失败类型 | 默认采集 | 升级条件 |
| --- | --- | --- |
| `target_not_found` | `hdc list targets -v` 摘要 | 不升级 |
| `trace_pipe_failed` | helper 状态摘要 | 停止本轮 run |
| `emulator_start_failed` | 启动命令摘要、最近日志摘要 | 用户确认后采日志包 |
| `target_ambiguous` | target 候选列表 | 用户选择 target 后继续 |
| `hdc_disconnected` | HDC 状态摘要 | 可重试 `hdc wait` |
| `boot_timeout` | boot 参数、Emulator 日志摘要 | 用户确认后采日志包 |
| `app_launch_failed` | `bm dump -n` 裁剪摘要、`aa dump`、错误日志摘要 | 用户确认后采更大日志 |
| `ui_unavailable` | `dumpLayout/screenCap` 能力探测结果 | 用户确认后采真实 layout/screenshot |
| `input_failed` | 前后 UI 摘要、命令记录 | 用户确认后采真实截图 |
| `risk_denied` | risk-gate 决策摘要 | 不升级 |
| `confirmation_rejected` | 确认事件摘要 | 降级或停止 |
| `redaction_failed` | 脱敏错误摘要 | 删除原始产物 |
| `artifact_write_failed` | 文件写入错误摘要 | 跳过产物归档 |
| `command_timeout` | 命令记录摘要 | 按阶段策略降级 |
| `command_nonzero_exit` | 退出码和错误摘要 | 按命令类别处理 |
| `cleanup_failed` | 清理错误摘要 | 记录后结束，不循环重试 |

## 可封装脚本模板

### start-emulator

参数：`hvd_name`、`hvd_root`、`image_root`、必填 `trace_name`、可选 `hdc_port`。

`image_root` 是模拟器系统镜像根目录，不是 DevEco build SDK root。启动前读取 HVD `config.ini` 的 `imageSubPath`，校验 `<image_root>/<imageSubPath>` 存在；例如 macOS 上常见可用路径是 `$HOME/Library/Huawei/Sdk`，而 `/Applications/DevEco-Studio.app/Contents/sdk` 只用于 hvigor/build SDK。

```bash
EMULATOR="/Applications/DevEco-Studio.app/Contents/tools/emulator/Emulator"

"$EMULATOR" -hvd "$hvd_name" -path "$hvd_root" -imageRoot "$image_root" -t "$trace_name"
"$EMULATOR" -hvd "$hvd_name" -path "$hvd_root" -imageRoot "$image_root" -t "$trace_name" -hdcport "$hdc_port"
```

启动前必须由 runner 准备并持有同名 trace pipe helper。启动命令本身不代表 boot 完成，必须后接 `wait-target`、`bootevent.boot.completed` 和稳定性检查；若进程静默退出、调用进程退出后 HDC target 消失或 trace 超时，runner 必须返回 stdout/stderr 日志路径、进程退出码、`Emulator -list -details` 摘要和 `hdc list targets -v` 快照。仓库脚本的 `launch` 默认让 trace holder 保活 1800 秒，并做 60 秒稳定性检查。

### select-target

```bash
HDC="/Applications/DevEco-Studio.app/Contents/sdk/default/openharmony/toolchains/hdc"
"$HDC" list targets -v
```

解析：选择 `TCP Connected` 行。多实例时优先精确匹配显式 target，例如 `127.0.0.1:10100`。多个 `Connected` 且未指定 target 时应停止，让上层显式选择。

### wait-target

```bash
"$HDC" -t "$target" shell param get bootevent.boot.completed
```

期望输出 `true`。超时后只采集连接和 boot 状态，不继续 UI 输入。

### dump-ui

```bash
"$HDC" -t "$target" shell uitest dumpLayout -p /dev/null -a
"$HDC" -t "$target" shell uitest dumpLayout -p /data/local/tmp/ai-layout.json -a
"$HDC" -t "$target" shell cat /data/local/tmp/ai-layout.json
```

`/dev/null` 只做能力探测；真实 UI 树会写设备侧临时文件，内容可能包含 UI 文本。

### capture-screen

```bash
"$HDC" -t "$target" shell uitest screenCap -p /dev/null
"$HDC" -t "$target" shell uitest screenCap -p /data/local/tmp/ai-screen.png
"$HDC" -t "$target" file recv /data/local/tmp/ai-screen.png "$local_path"
```

真实截图含屏幕内容，归档前需要脱敏策略或用户确认。

### launch-bundle

```bash
"$HDC" -t "$target" shell bm dump -n "$bundle"
"$HDC" -t "$target" shell aa start -b "$bundle" -a "$ability"
"$HDC" -t "$target" shell aa start -b "$bundle" -a "$ability" -m "$module"
```

启动后必须用 `find-pid-window` 验证前台状态。

### find-pid-window

```bash
"$HDC" -t "$target" shell aa dump -l
"$HDC" -t "$target" shell aa dump -r
"$HDC" -t "$target" shell hidumper -ls
```

解析：`aa dump -r` 提取 process name、pid、foreground state；窗口诊断项提取 focus window、pid、window id、bounds。两者对上才认为启动完成。

### risk-gate

输出只允许三种：

```text
allow
require_confirm
deny
```

无法分类时按 `require_confirm` 处理。

## 停止与清理

停止指定 HVD：

```bash
/Applications/DevEco-Studio.app/Contents/tools/emulator/Emulator \
  -stop "<hvd-name>" \
  -path "$HOME/.Huawei/Emulator/deployed"
```

确认没有残留进程：

```bash
ps -axo pid,stat,command | rg "Contents/tools/emulator/Emulator|<emulator-related-process>|<trace-name>" || true
```

trace pipe helper 的清理必须由创建它的 runner 执行；清理前确认目标属于当前 `run_id`，不要用固定路径做无条件删除。

## 排障 checklist

1. `Emulator` 启动后立刻退出：
   - 检查 `<trace-name>` 对应的本地占位通道是否由当前 runner 持有。
   - 检查 `-t <trace-name>` 与 runner 记录是否一致。
   - 确认占位通道 helper 仍在运行。
2. 报设备不存在或路径错误：
   - 执行 `Emulator -list` 查看 HVD 名称。
   - 确认 `-path` 是 `$HOME/.Huawei/Emulator/deployed`，不是具体实例目录。
3. `hdc list targets` 为空：
   - 等待日志出现 `Guest OS Boot Completed!!`。
   - 检查是否有旧 hdc server 或旧模拟器实例占用连接。
4. 模拟器窗口不可见：
   - 用 `osascript` 查询窗口位置。
   - 将窗口移动到 `{120, 120}` 后再截图确认。
5. AI 桌面插件无法识别 `Emulator`：
   - 优先使用 `hdc -t <target> shell uitest dumpLayout` 与 `uiInput`。
   - 桌面插件只作为截图或窗口移动的补充方案。

## 已知限制

1. trace pipe 占位通道必须保持运行；退出后 Emulator 后续行为可能不稳定。
2. 当前只是验证“最小可启动”，没有实现完整 trace 协议。
3. `hdc list targets` 上线后仍可能需要等待系统完成启动，再执行 UI 操作。
4. GUI 窗口位置可能不在主屏，需要通过辅助功能移动。
5. 多模拟器实例时应使用不同的 trace pipe 名称与 HDC 端口，避免连接冲突。

## 后续建议

1. 在项目中沉淀一个 `scripts/start-harmony-emulator.sh`：
   - 自动准备 trace pipe 占位通道
   - 自动启动指定 HVD
   - 轮询 `hdc list targets`
   - 可选移动窗口到主屏
2. 再封装一个 AI 测试入口：
   - `dumpLayout`
   - `screenCap`
   - 坐标点击
   - 文本输入
   - Home/Back
3. 若要长期运行，trace pipe helper 应作为受控后台进程管理，具备 `run_id` 绑定、健康检查和清理能力。
