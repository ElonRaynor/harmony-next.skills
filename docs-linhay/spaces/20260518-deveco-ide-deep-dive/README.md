# DevEco Studio IDE 深度挖掘 Space

日期：2026-05-18

## 目标

独立记录 DevEco Studio IDE 本体、插件、内置工具、私有入口和自动化能力的深度探查结果。该 space 用于承接“我们还不知道 IDE 有什么能力”的持续研究，避免把未验证结论直接写入 `harmony-next/SKILL.md` 或公开参考页。

## 边界

- 默认只读：只做文件枚举、manifest 解析、help/version 查询、静态字符串与插件目录分析。
- 不默认启动 IDE，不默认打开 GUI，不默认修改 DevEco 配置、项目配置、SDK、模拟器、HVD 或设备状态。
- 不默认执行安装、卸载、清数据、端口转发、抓取真实 UI/日志/截图等动作。
- 发现私有未公开接口时，只记录入口、证据、风险等级和验证方法；实现细节进入确认档后再补。
- 所有结论必须标注来源：本机文件路径、命令输出、qmd 结果、截图或手工验证步骤。

## 当前环境

- DevEco Studio：`/Applications/DevEco-Studio.app`
- Bundle ID：`com.huawei.devecostudio.ds`
- 版本：`6.0.2`
- Build：`DS-243.24978.46.36.602642`
- URL Scheme：`devecostudio`

## 初始发现

### 可执行与工具入口

- `Contents/MacOS/devecostudio`
- `Contents/bin/inspect.sh`
- `Contents/bin/format.sh`
- `Contents/bin/ltedit.sh`
- `Contents/bin/fsnotifier`
- `Contents/tools/emulator/Emulator`
- `Contents/tools/emulator/emulator-crash-service`
- `Contents/tools/UxTestService/ux_detect.py`
- `Contents/tools/UxTestService/CheckMethods.py`
- `Contents/tools/ohpm/package.json`

### 插件能力线索

- `codegenie-plugin`：AI 辅助、embedding model、lancedb server、preview project/template。
- `codelinter`：Ark 性能检查、eslint agent、performance agent。
- `diagnostic-plugin`：诊断能力入口。
- `harmony`：preview server、jerry debug server、API scan、lib。
- `openharmony`：ace server、arktsdoc、arkui inspector、faultlog UI、doctor view、info center、debug view、preview server、project management。
- `ohos-profiler` / `ohos-trace`：性能与 trace 能力。
- `operation-analyzer-plugin` / `performanceTesting`：操作分析与性能测试线索。
- `ui-generator`：UI 生成能力线索。
- `Application-Agent-Plugin`：应用代理能力线索。
- `obfuscation-helper`：混淆辅助与 agent。

## 汇总发现

### 1. IDE 私有协议

- `devecostudio://` 已注册到 `com.huawei.devecostudio.ds`。
- 当前静态确认的业务 handler 只有 `sample/v1/import/git` 与 `sample/v1/import/fs`。
- 参数形态为 `?param={...}` JSON，入口正则提取后分发到 `com.huawei.devecoProtocolHandler`。
- URL 校验静态线索不是 allowlist，而是 `new java.net.URL(value)`。
- 结论：它是“示例工程导入协议”，不是通用 openFile/openProject 协议；动态验证必须隔离。

### 2. CodeGenie / AI / RAG / MCP

- CodeGenie 包含本地 VESO RoBERTa ONNX embedding 模型、LanceDB 本地向量索引、localhost WebSocket/Socket.IO 数据库服务、OpenAI 风格 HTTP forwarding、MCP stdio/HTTP/SSE、OpenAI/Anthropic/Gemini/custom provider 线索。
- RAG 本地索引字段包含 `file_path`、`chunk_text`、`chunk_metadata`、`chunk_embedding` 等敏感信息。
- 结论：本地 embedding 与索引链路可以静态研究；任何 localhost 端口调用、MCP 配置、外部 provider、聊天历史读取都需要确认。

### 3. Preview / Inspector / Profiler / Doctor / FaultLog

- Previewer、ArkUI Inspector、Profiler、Trace、Doctor、Diagnostic、FaultLog/HiLog、Debug/PandaDAP 均有明确插件入口。
- 可默认进入的是静态识别和离线文件分析：`.htrace`、profiler snapshot、faultlog、stacktrace、appFreeze/cppCrash、`.arkli`、`.preview`。
- 实时 Preview Server、Inspector live mode、Profiler 采集、Debug attach/run、HDC forward、在线 HiLog/FaultLog 都必须确认。

### 4. 调试协议

- Jerry DAP 支持 `--server=<port>` 并绑定 `127.0.0.1`，设备侧连接线索为 `ws://127.0.0.1:<port>/jerry-debugger`。
- OpenHarmony debug view 使用 `ws://localhost:<port>?plugin=<pluginName>&sid=<sid>`。
- ACE / ArkTS LSP、C/C++ LSP/DAP、native debug 都存在，但端口、session、payload 和 forward 服务名带 DevEco 私有约定。
- 端口线索：connect server `15037..15137`，DAP server `25037..25137`，fallback/default `20000`。

### 5. 项目模板与构建系统

- 发现 `44` 个 `template.json`，覆盖 New Project、Module、Ability、Page、Widget、Worker、Extension、Library、Insight Intent、AVSession、CloudDev、RemoteNotification、Map、Payment、Iap 等。
- 模板引擎基于 Freemarker 与 `command.xml.ftl`，会执行 `copy`、`merge`、`instantiate`、`mkdir`、`open`。
- Hvigor 版本线索：`@ohos/hvigor 6.22.3`，`@ohos/hvigor-ohos-plugin 6.22.3`；ohpm 版本线索：`6.0.1`。
- 结论：模板和构建系统可静态索引；渲染模板、构建、同步 SDK、安装依赖都会写工程或联网，需确认。

### 6. 用户侧数据与隐私

- 关键目录：`~/Library/Application Support/Huawei/DevEcoStudio6.0`、`~/Library/Caches/Huawei/DevEcoStudio6.0`、`~/Library/Logs/Huawei/DevEcoStudio6.0`、`~/Library/Preferences/com.huawei.devecostudio.ds.plist`。
- 高风险：CodeGenie chat history、JCEF Cookies/Trust Tokens/LocalStorage/Session Storage、recentProjects、workspace、LocalHistory、IDE index、idea.log、CodeGenie.log、DAP/LSP logs。
- 公开 skill 只保留目录模式、风险分类和只读命令模板，不记录真实路径、项目名、日志正文、cookie/token、workspace hash、URL 查询参数。

### 7. 登录、云端与运维能力

- 登录模块处理浏览器登录、回调 receiver、token 存取/刷新/过期与登录扩展点。
- Cloud Toolkit 覆盖 Cloud Function、Cloud DB、部署、运行、调试、触发器、Cloud Console、服务端/客户端模型生成。
- Application Agent 与 Operation Analyzer 都属于 O&M / 监控面，涉及 JCEF 页面、登录态同步、团队/项目/App、APM metric、Crash 跳转。
- CodeGenie 同时具备本地 RAG/MCP 和远端补全/问答/Inline Chat/UT/编译修复/自定义模型能力。
- 公开文档不记录内部测试域名、完整 API path、OAuth client id、token/cookie 桥接、模型内部协议、prompt、MCP schema 或真实项目参数。

## 已整合产物

- `harmony-next/references/ideGuides/DevEco Studio IDE私有接口与AI自动化.md`
- `harmony-next/SKILL.md`
- `harmony-next/references/TASK_MAP.md`
- `README.md`
- `README_en.md`

## 待验证问题

1. `devecostudio://` URL scheme 支持哪些 action、参数和文件定位能力。
2. `inspect.sh`、`format.sh`、`ltedit.sh` 是否能作为无 GUI 的代码检查、格式化或打开文件入口。
3. `codegenie-plugin` 是否暴露本地服务、索引、embedding 或项目预览入口。
4. `openharmony/arkui-inspector` 与设备侧 `uitest`、ArkUI Inspector 的关系。
5. `harmony-preview-server` / `openharmony-preview-server` 是否可无 IDE 启动，并服务 ArkUI preview。
6. `ohos-doctor-view` 背后是否有可直接调用的 doctor/诊断命令。
7. `faultlog-ui`、`ohos-profiler`、`ohos-trace` 是否能复用为 CLI 诊断采集。
8. `UxTestService` 的检测规则、输入输出格式和与 UI 自动化的关系。
9. 插件 descriptor 中是否有 action id、toolWindow id、service、extension point、hidden command。
10. IDE 配置目录中是否有最近使用的工具状态、端口、server pid、缓存索引等可读诊断信息。

## 下一步方向

1. 用只读方式继续汇总所有 `META-INF/*.xml` 的 action/service/extension point 矩阵。
2. 在隔离用户或 VM 中设计 `devecostudio://` test harness，先调用 handler，不直接 `open` URL。
3. 静态精查 CodeGenie 的 `HttpForwardingServer`、`McpServerConnector`、`ModelConfigStore`、`McpConfigStore`、RAG prompt builder。
4. 对 UxTestService 继续拆规则 schema、输入输出文件和离线 UX 审核边界。
5. 若进入动态阶段，先限定测试项目、测试账号、测试设备、端口观察方式和可写目录。

## 记录格式

每个发现使用以下结构：

```text
## <能力名称>

- 状态：候选 / 已验证 / 不稳定 / 废弃 / 禁用
- 风险：allow / require_confirm / deny
- 来源：<文件路径或命令>
- 入口：<命令、URL scheme、插件 action 或服务>
- 证据：<摘要，不贴敏感原文>
- 适用场景：<AI 自动化、诊断、预览、调试等>
- 限制：<版本、状态、权限、超时、隐私>
- 下一步：<只读验证或确认档验证>
```

## 验证命令

当前只允许默认只读命令：

```bash
find /Applications/DevEco-Studio.app/Contents -maxdepth 3 -type f
plutil -p /Applications/DevEco-Studio.app/Contents/Info.plist
find /Applications/DevEco-Studio.app/Contents/plugins -maxdepth 2 -type d
rg -n "<keyword>" /Applications/DevEco-Studio.app/Contents/plugins
```

执行任何可能启动服务、连接设备、写缓存、写项目、打开 GUI 或采集真实数据的命令前，需要先升级到用户确认档。
