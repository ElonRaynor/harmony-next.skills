# DevEco Studio IDE 私有接口与 AI 自动化

> 本页记录 DevEco Studio IDE 本体、插件、内置工具、本地服务、私有协议和缓存目录的静态验证结论。这里的内容属于私有未公开接口，不是稳定公开 API；路径、类名、端口、协议、参数和行为都可能随 DevEco Studio 版本变化。

## 适用范围

触发词包括：`DevEco Studio IDE`、`CodeGenie`、`MCP`、`LanceDB`、`devecostudio://`、`inspect.sh`、`format.sh`、`ltedit.sh`、`ArkUI Inspector`、`Previewer`、`Profiler`、`ohos-trace`、`Doctor`、`Diagnostic`、`FaultLog`、`HiLog`、`UxTestService`、`Application Agent`、`Operation Analyzer`、`Cloud Toolkit`、`UI Generator`。

当前静态验证环境：

- DevEco Studio：`/Applications/DevEco-Studio.app`
- Bundle ID：`com.huawei.devecostudio.ds`
- 版本：`6.0.2`
- Build：`DS-243.24978.46.36.602642`
- IntelliJ Platform：`243.24978.46`
- 数据目录名：`DevEcoStudio6.0`
- URL Scheme：`devecostudio`

## 默认安全边界

默认只允许：

- 枚举 DevEco Studio 包内文件、插件目录、`plugin.xml`、`package.json` 和小型配置文件。
- 使用 `plutil`、`find`、`rg`、`jar tf`、`unzip -p`、`strings` 做静态分析。
- 查询短生命周期 `--help`、`-h`、`-v`、`version`，前提是确认不会启动 GUI、服务、守护进程或连接设备。
- 分析离线文件：`.htrace`、profiler snapshot、faultlog、stacktrace、appFreeze/cppCrash 文本、`.arkli`、`.preview` 产物。

必须先让用户确认：

- 启动 DevEco Studio、Preview Server、ArkUI Inspector、Profiler、Debug session、JCEF toolWindow 或任何 GUI。
- 连接设备或模拟器、执行 `hdc fport/rport`、`file recv`、`hilog` 在线抓取、截图、录屏、layout dump。
- 运行 `format.sh` 修改源文件，运行 `inspect.sh` 写 inspection 输出。
- 调用 CodeGenie localhost HTTP/WebSocket 服务、创建 MCP 配置、触发外部 LLM provider 或云端能力。
- 读取用户侧聊天历史、recent projects、workspace、JCEF cache、LocalHistory、日志正文或内部数据库。

默认禁止：

- 自动登录、上传、发布、部署、卸载、清缓存、删除 HVD、清 IDE 状态。
- 在未隔离环境中验证未知 `devecostudio://` URL。
- 公开记录 token、securityId、API key、项目源码片段、日志正文或用户路径细节。

## IDE 命令入口

DevEco Studio 包内存在三个 JetBrains 风格命令封装：

| 入口 | 证据路径 | 能力 | 默认风险 |
| --- | --- | --- | --- |
| `inspect.sh` | `Contents/bin/inspect.sh` | 调用 `devecostudio inspect "$@"`，可做离线 inspection | `require_confirm`，可能启动 IDE 后端并写输出 |
| `format.sh` | `Contents/bin/format.sh` | 调用 `devecostudio format "$@"` | `require_confirm`，会修改源文件 |
| `ltedit.sh` | `Contents/bin/ltedit.sh` | 调用 `devecostudio nosplash -e "$@"` LightEdit | `require_confirm`，会启动 GUI/IDE 进程 |

命令行处理器还暴露 `--line`、`--column`、`--wait`、`--temp-project`、`--project` 等文件/项目打开参数线索。默认只记录能力，不自动执行。

## devecostudio:// 私有协议

DevEco Studio 注册了 macOS URL Scheme：`devecostudio`。

静态证据：

- `Contents/Info.plist`
- `plugins/openharmony/lib/project-mgmt-6.0.2.642.jar`
- `com.huawei.deveco.projectmgmt.ohos.actions.protocol.IdeProtocolHandler`
- 扩展点：`com.huawei.devecoProtocolHandler`

协议解析线索：

```text
scheme: devecostudio
pattern: ^(.*?)\?param=(\{.*\})$
```

入口处理线索：

- 先用 UTF-8 `URLDecoder.decode`。
- 再用正则提取 `uri/action` 与 JSON 字符串。
- 直接 `JSON.parseObject`；静态检查未看到入口层 JSON parse 异常兜底。
- 遍历 `com.huawei.devecoProtocolHandler` 扩展点，通过 `handler.getUri().equals(uri)` 分发。
- 当前只确认 `GitProtocolHandler` 与 `ZipProtocolHandler` 两个业务 handler。

已发现候选 action：

| action | 用途 | 必需字段 | 风险 |
| --- | --- | --- | --- |
| `sample/v1/import/git` | 导入 Git 示例工程 | `repoUrl`、`branch`、`projectName`、`relativePath` | `require_confirm`，会打开导入向导并访问远端仓库 |
| `sample/v1/import/fs` | 导入下载文件/Zip 示例工程 | `downloadUrl`、`checksum`、`projectName` | `require_confirm`，会下载并导入工程 |

候选格式：

```text
devecostudio://sample/v1/import/git?param={...}
devecostudio://sample/v1/import/fs?param={...}
```

未静态确认 `devecostudio://openFile` 或 `devecostudio://openProject`。文件/项目打开更可能走命令行参数或 macOS 文档关联。实际打开 URL 前必须在隔离用户或临时 VM 中验证。

`ValidatorUtil.checkUrl(String)` 静态线索显示只做 `new java.net.URL(value)`，未看到 http/https allowlist。Git handler 后续会把 `repoUrl` 交给 Git remote；Zip handler 后续会下载 `downloadUrl` 并校验 checksum。Git `relativePath`、绝对路径、`..`、sparse pattern、Zip 符号链接 entry 和 Zip Slip 等边界必须在隔离目录中验证。

## CodeGenie 本地 AI 能力

`codegenie-plugin` 是当前最重要的高风险能力面。

静态证据：

- `Contents/plugins/codegenie-plugin/embedding_model/VESO-model/VESO-25M/`
- `Contents/plugins/codegenie-plugin/lancedb_server/main.js`
- `Contents/plugins/codegenie-plugin/lib/rag-core-6.0.2.642.jar`
- `Contents/plugins/codegenie-plugin/lib/instrumented-CodeChat.jar`
- `Contents/plugins/codegenie-plugin/lib/instrumented-codegenie-infrastructure.jar`

已确认能力线索：

- 本地 VESO RoBERTa ONNX embedding 模型：`model_fp16.onnx`，输出维度 `768`。
- LanceDB 本地向量库：默认表名 `knowledge_base`，字段包含 `file_path`、`chunk_text`、`chunk_metadata`、`chunk_embedding`。
- 本地 LanceDB WebSocket/Socket.IO 服务：命令形态为 `node main.js <port> <securityId>`，客户端线索 `ws://localhost:%d?id=%s`，Node 侧绑定 `127.0.0.1`。
- OpenAI 风格本地 HTTP 转发服务：`POST /chat/completions`、`GET /models`，支持 streaming，静态线索包含 `Access-Control-Allow-Origin: *` 和 `Chat-Id` header。
- MCP：支持 stdio、HTTP/SSE、Streamable HTTP；stdio 由 `command + args + env` 构造。
- LLM provider：存在 OpenAI、Anthropic、Gemini、custom model config、proxy、SSE 相关依赖。

默认策略：

- 允许静态识别模型、jar、类名、配置路径、插件 action 和离线索引风险。
- 不默认启动 IDE、Node 服务、HTTP forwarding server、LanceDB server。
- 不默认调用 `/models`、`/chat/completions`、WebSocket 或 MCP server。
- 不默认读取用户本地 `.lancedb`、聊天历史、模型配置数据库、API key、headers 或 token。

核心风险：

- 本地 RAG 索引包含项目原文片段和路径。
- MCP stdio 本质可由配置启动本地命令。
- 外部 LLM provider 可能把 RAG chunk、prompt、源码片段外发。
- 若端口和 `securityId` 泄露，LanceDB 本地索引存在被操作风险。
- HTTP forwarding server 的 CORS 行为需要动态确认，不能凭静态线索认定安全。

## Preview / Inspector / Profiler / Debug

这些能力都有清晰插件入口，但大多跨过 IDE 进程、设备连接、本地服务或端口转发边界。

| 能力 | 证据路径 | 静态能力 | 默认策略 |
| --- | --- | --- | --- |
| Preview Server | `plugins/harmony/harmony-preview-server`、`plugins/openharmony/openharmony-preview-server`、`ohos-preview-plugin-6.0.2.642.jar` | `Previewer`、`PreviewerLog`、`PreviewerDebug`、`.preview/cache`、`buildPreviewerResource` | 静态识别可默认；启动 server、访问端口、Debug Preview 需确认 |
| ArkUI Inspector | `plugins/openharmony/arkui-inspector`、`layout-inspector-server-6.0.2.642.jar` | ToolWindow `ArkUI-Inspector`、端口范围 `30400-30500`、`.arkli` 导入导出、`get3DLayoutData`、`getImageBase64` | 离线 `.arkli` 分析可默认；实时组件树、截图、live mode 需确认 |
| Profiler / Trace | `ohos-profiler`、`ohos-trace` | `.htrace`、snapshot、gRPC、设备端口 `50051`、本地端口范围 `10001-11001`、`Profiler.Import` | 离线文件导入分析可默认；实时采集、`hdc fport`、hiprofiler 需确认 |
| Doctor / Diagnostic | `ohos-doctor-view`、`diagnostic-plugin` | OS/RAM/network/ohpm/git 检查项、log provider、crash/freeze watcher | 检查项建模可默认；执行 IDE action、收集/上传诊断包需确认 |
| FaultLog / HiLog | `faultlog-ui`、`ohos_hilog-6.0.2.642.jar` | faultlog、stacktrace、appFreeze、cppCrash 离线分析 | 离线日志分析可默认；在线 HiLog、截图/录屏、设备侧抓取需确认 |
| Debug / PandaDAP | `ohos-debug-common`、`ace-debugger`、`ohos-debugger` | WebSocket、`ws://127.0.0.1:<port>`、`PandaDAPServer`、port forward 线索 | 静态协议分析可默认；run/debug/attach/ConnectServer 需确认 |

调试协议补充线索：

- Jerry DAP：`plugins/harmony/jerry-debug-server/out/debugAdapter.js` 支持 `--log-home`、`--debug-port`、`--debug-log`、`--server=<port>`，DAP server 绑定 `127.0.0.1`，设备侧连接线索为 `ws://127.0.0.1:<port>/jerry-debugger`。
- OpenHarmony debug view：`plugins/openharmony/openharmony-debug-view/index.html` 通过 `ws://localhost:<port>?plugin=<pluginName>&sid=<sid>` 连接 IDE 内部 WebSocket，`pluginName` 涉及 `ipconnect`、`attach`、`configuration` 等模式。
- ACE / ArkTS LSP：`plugins/openharmony/ace-server/out/index.js` 使用 TypeScript fork `4.9.5-h1.AllScenario.devecostudio.20251205.r14`，支持 hover、definition、rename、completion、formatting、code action、call/type hierarchy 等能力。
- C/C++ LSP/DAP：`ohos-cpp-lsp-client`、`cpp-lsp-devecostudio`、`ohos-cpp-dap-client`、`dap4intellij`、`panda-debug-adapter` 提供补全、诊断、clang-tidy、断点和 native debug 线索。
- 端口范围：connect server `15037..15137`，DAP server `25037..25137`，fallback/default `20000`，端口可用性检查绑定 `127.0.0.1`。
- Native debug 静态线索涉及向设备推送 `lldb-server`、`start_lldb_server.sh`，并通过 shell、abstract socket、`/data/local/tmp` 建立会话。

这些接口虽然呈现 DAP/LSP/WebSocket 外形，但注册点、扩展通知、端口分配和 forward 服务名都带 DevEco 私有约定。不要把 `sid`、内部 WebSocket payload、hidden action 或测试 action 当长期稳定能力依赖。

## IDE 插件入口索引

高价值插件和入口：

- `openharmony`：项目/模块/页面创建、Build HAP/App、Previewer、HiLog/FaultLog、ArkUI Inspector、Device File Explorer、Database、SDK 管理、Debug/Attach/Hot reload 扩展点。
- `harmony`：Harmony 项目能力、登录、Cloud Toolkit、AppAnalyzer、Simulator/HVD、Cangjie 实验配置。
- `diagnostic-plugin`：Collect Logs and Diagnostic Data、UI freeze、low memory、crash、HDC 异常监听、metric log 扩展点。
- `ohos-profiler`：Profiler、Graphics Profiler、SmartProfiler、gRPC/WebSocket/JCEF 数据通道。
- `ohos-trace`：trace/lemon、metric/log upload 扩展点、内存报告线索。
- `ui-generator`：`Generate Project from...`、Android 到 ArkUI 转换、JCEF 文件选择与转换 handler。
- `Application-Agent-Plugin`：Application Agent、JCEF、OAuth、TokenManager、登录/登出事件监听。
- `operation-analyzer-plugin`：Operation Analyzer，含登录态/账号/可能云端依赖。

默认策略：插件 action、toolWindow、service、extension point 可静态索引；触发 action、打开 toolWindow、登录、部署、上传、监控、云函数调试都需用户确认。

## 登录、云端与运维能力

这组能力涉及账号、token、云端项目、运维监控和模型服务。公开沉淀只记录能力类别和风险，不记录内部测试域名、完整 API path、client id、token/cookie 桥接细节或模型内部协议。

| 能力 | 静态线索 | 风险边界 |
| --- | --- | --- |
| 登录/账号中心 | `Huawei.devecoLogin`、浏览器登录、回调 receiver、token 刷新、登录/退出扩展点 | 处理 access/refresh/JWT/OAuth token，默认不读取配置、日志或本地缓存内容 |
| Cloud Toolkit / AGC | Cloud Function、Cloud DB、部署、运行、调试、触发器、Cloud Console、模型生成 | 可能上传函数代码、schema、项目/App/team 信息和 credential 配置；任何同步/部署/上传都需确认 |
| Application Agent | O&M monitoring tool、JCEF 内嵌页、平台跳转、登录态同步、request handler | 可能把访问令牌注入 JCEF 请求或平台 cookie；不默认打开 toolWindow 或读取 JCEF 存储 |
| Operation Analyzer | O&M monitoring tool、项目/App/团队信息、APM metric、Crash 跳转 | 属于运维/监控数据面；查询指标、读取团队项目、跳转 crash 页面需确认 |
| CodeGenie 远端能力 | 补全、问答、Inline Chat、UT、编译错误修复、RAG、MCP、自定义 Agent/模型、JCEF Chat | 可能上传代码片段、prompt、RAG chunk、会话 ID 和模型配置；调用网络或模型前必须确认 |

不要公开或写入日志：

- 真实 token、cookie、Authorization header、refresh token、JWT、OAuth code。
- 内部测试/镜像域名、完整云端 API path、credential 相关接口、部署/上传流程细节。
- CodeGenie 内部 WSS endpoint、模型 ID、agent/MCP schema、系统 prompt、工具调用协议。
- Operation Analyzer 的 APM/Crash 查询参数、项目/团队/App 标识。
- Application Agent 的 client id、cookie bind path、authorization-code 到平台 cookie 的桥接细节。

## CLI 与 SDK 工具链

包内可脚本化工具：

| 工具 | 证据路径 | 能力 | 风险边界 |
| --- | --- | --- | --- |
| `ohpm` | `Contents/tools/ohpm/bin/ohpm` | 包管理，版本 `6.0.1`，默认 registry `https://ohpm.openharmony.cn/ohpm/` | `info/list/root/config list` 可低风险；install/update/clean/publish/unpublish 需确认 |
| `hvigor` | `Contents/tools/hvigor/bin/hvigorw.js` | 构建系统，`@ohos/hvigor 6.22.3` | help/tasks 可低风险；assemble/prune/daemon/watch 需确认 |
| `hdc` | `Contents/sdk/default/openharmony/toolchains/hdc` | 设备连接、安装、日志、shell、端口转发 | version/help 可低风险；连接设备、shell、install、file、fport 需确认 |
| `restool` | SDK toolchains | 资源编译/资源 dump | help 可低风险；写输出或 `--forceWrite` 需确认 |
| `idl` | SDK toolchains | 生成 C/C++/TS/Rust/Java | help 可低风险；生成代码需确认 |
| `syscap_tool` | SDK toolchains | syscap 编解码/比较 | help/version 可低风险；写输出需确认 |
| `ark_disasm` | SDK toolchains | Ark 字节码反汇编 | 写反汇编文件需确认 |
| `hnpcli` | SDK toolchains | native package 打包 | 打包写 `.hnp` 需确认 |
| `rawheap_translator` | SDK toolchains | rawheap 转 heapsnapshot | 生成文件需确认 |
| `hilogtool` | SDK toolchains | hilog 解析 | 写输出需确认 |

## 项目模板、工程向导与 SDK 管理

静态发现 `44` 个 `template.json`，主要位于：

- `Contents/plugins/openharmony/lib/templates`
- `Contents/plugins/harmony/lib/templates`

能力线索：

- OpenHarmony 模板：New Project、New Cross Project、New Hvigor Package、New Module、Empty Ability、Native C++、Flexible Layout Ability、Worker、New Page、Widget、BackupAbility、DriverExtensionAbility、EmbeddedUIExtensionAbility、WorkScheduler、Shared/Static Library、Insight Intent、AVSession。
- Harmony/HMS 模板：`[CloudDev]Empty Ability`、RemoteNotification、Map、Payment、Iap、Project/Module Append CTK Project。
- 模板引擎：Freemarker `.ftl`、`command.xml.ftl`，命令包含 `copy`、`merge`、`instantiate`、`mkdir`、`open`。
- 工程向导 JCEF 前端：`plugins/openharmony/project-mgmt-view`，路由线索包含 `CreateProject`、`CreateModule`、`CreateAbility`、`CreateExtAbility`、`CreatePagePackage`、`CreateWorker`、`UploadProduct`、`CreateKit`、`ShowProjectStructure`、`ImportPCID`、`CreateImageAsset`、`CreateInsightIntent`、`AssociateCloudDev`、`ApichangeAssistant`。
- Hvigor IDE 集成：`com.huawei.deveco.hvigor`、Build Analyzer、终端 PATH 注入、daemon、parallel、incremental、typeCheck、analyze、Java/Node 参数配置。
- SDK 管理：OpenHarmony SDK、HarmonyOS SDK、ArkUI-X SDK，含 update checker、compatibility checker、install/uninstall/location change listener。

风险边界：模板命令会写工程文件并可能合并 `build-profile.json5`、`hvigorfile.ts`、`oh-package.json5`、`module.json5`、`local.properties`。模板渲染、工程向导 JCEF handler、SDK 安装/卸载、AGC/上传/签名端点都必须在隔离临时工程和确认档中验证。

## UxTestService

证据路径：

- `Contents/tools/UxTestService/ux_detect.py`
- `Contents/tools/UxTestService/CheckMethods.py`
- `Contents/tools/UxTestService/util/param_builder.py`
- `Contents/tools/UxTestService/config/config.py`
- `Contents/tools/UxTestService/buildInfo.properties`

版本线索：`buildVersion=15.8.1.202512271854`。

入口参数：

```text
--task_id
--task_type UxTest|GlobalReview
--check_param <检测参数文件路径>
```

能力线索：离线 UX 审核，输入截图、布局 JSON、ArkUI JSON、HAP 路径、record 信息等。规则覆盖返回键、布局遮挡/截断/模糊、手势冲突、热区、对比度、字体、图标、动效、导航栏、深色模式、状态栏、元服务、横竖屏、大屏、悬浮、文本选择、全键盘、窗口内容保持等。

默认策略：可以静态解析规则、参数 schema 和输入输出格式；真实运行检测会读取 UI/截图/layout/HAP 并可能写日志或结果，需用户确认。

## 用户侧配置、缓存与隐私

主要目录：

- 配置：`~/Library/Application Support/Huawei/DevEcoStudio6.0`
- 旧版配置：`~/Library/Application Support/Huawei/DevEcoStudio5.0`
- 偏好：`~/Library/Preferences/com.huawei.devecostudio.ds.plist`
- 日志：`~/Library/Logs/Huawei/DevEcoStudio6.0`
- 缓存：`~/Library/Caches/Huawei/DevEcoStudio6.0`

高风险文件/目录：

- `options/recentProjects.xml`：最近项目路径、窗口标题、打开状态。
- `workspace/*.xml`：最近打开文件、光标行列、窗口布局、项目上下文。
- `options/CodeGenieChatHistoryPersistentState.xml`：可能包含 AI 对话历史状态。
- `idea.log`、`lsp-server/*.log`、`dap_server_*.log`：可能含项目路径、设备信息、命令参数、错误栈。
- `indexing-diagnostic/`：可能含项目结构、文件名、索引性能信息。
- `jcef_cache/`：可能含网页缓存、本地存储、会话痕迹。
- `LocalHistory`、`fileHistory`、`editor/`、`vcs-log/`：可能保留源码片段、历史和 VCS 信息。
- `app-internal-state.db`：IDE 内部状态数据库。

默认策略：只允许列目录、文件名、大小、mtime、路径模式。读取正文、导出、清理或归档前必须确认并说明脱敏策略。

## 推荐工作流

1. 先确认 DevEco Studio 版本和路径，不复用旧版本结论。
2. 只读静态定位入口：`Info.plist`、`product-info.json`、插件 `plugin.xml`、jar 类名、包内脚本。
3. 对能力按风险分类：
   - `allow`：静态索引、help/version、离线文件分析。
   - `require_confirm`：启动 GUI/服务、写文件、连接设备、读取用户数据、调用网络或 localhost 接口。
   - `deny`：破坏性清理、自动登录/上传/部署、未隔离验证未知私有 URL。
4. 记录证据路径、版本、命令、风险和下一步，不把私有接口当稳定契约。
5. 动态验证必须使用隔离用户/临时 VM/测试项目，验证后再决定是否提升到可复用脚本或 skill 默认流程。

## 只读复现命令

```bash
plutil -p /Applications/DevEco-Studio.app/Contents/Info.plist
cat /Applications/DevEco-Studio.app/Contents/Resources/product-info.json
cat /Applications/DevEco-Studio.app/Contents/Resources/build.txt
find /Applications/DevEco-Studio.app/Contents/plugins -maxdepth 2 -type d
find /Applications/DevEco-Studio.app/Contents/tools -maxdepth 3 -type f
jar tf <plugin.jar> | rg 'META-INF/.*\\.xml$'
unzip -p <plugin.jar> META-INF/plugin.xml
strings <plugin.jar> | rg -i 'localhost|127\\.0\\.0\\.1|websocket|grpc|token|mcp|port'
```
