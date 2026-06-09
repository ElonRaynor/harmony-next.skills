# DevEco Studio 能力索引

本索引用于快速定位当前 space 已沉淀的研究结果。所有条目默认来自 workspace 副本：

`/Users/linhey/Desktop/linhay-open-sources/harmony-next.skills/inputs/DevEco-Studio.app/Contents`

## 风险分层

- `allow-static`：只读枚举、jar/xml/schema/d.ts/header 读取，可继续默认探索。
- `confirm-local`：可能写用户配置、缓存、项目、日志、索引，执行前必须确认。
- `confirm-device`：可能连接设备、HDC、模拟器、端口转发、采集日志/截图/性能数据，执行前必须确认。
- `confirm-network`：可能登录、联网、访问云服务、模型服务、MCP market、上传日志或 telemetry，执行前必须确认。
- `deny-installed-app`：禁止对 `/Applications/DevEco-Studio.app` 做研究动作。

## AI / Agent / CodeGenie

| 能力 | 价值 | 风险 | 主要证据 |
| --- | --- | --- | --- |
| 本地 RAG、LanceDB、ONNX embedding | 代码库问答、离线索引、向量记忆 | `confirm-local` | `codegenie-plugin/lancedb_server/main.js`、`embedding_model/VESO-model/VESO-25M/model_fp16.onnx` |
| MCP server 管理 | 工具扩展、stdio/http/sse 连接 | `confirm-local` / `confirm-network` | `McpHandler.class`、`McpServerConnector.buildStdioClient(...)` |
| 自定义 Agent | Agent 配置、工具调用、diff 接受/拒绝 | `confirm-local` | `AgentHandler.class` |
| Rules / Skills | 项目/全局规则与技能导入、启用、编辑 | `confirm-local` | `RuleHandler.class`、`SkillHandler.class` |
| 长期记忆 | 记忆开关、编辑、删除 | `confirm-local` | `MemoryHandler.class`、`MemoryType.LONG_TERM` |
| 本地 WebSocket LLM provider | 代码库问答运行配置 | `confirm-local` | `codebase_feature_ask/config/websocket.json` |
| Harmony 页面生成 | 页面生成、预览转发、编译修复 | `confirm-local` | `PageHandler.class`、`harmony-page.xml` |
| Application Agent | O&M 助手 JCEF 页面与白名单外跳 | `confirm-network` | `Application-Agent-Plugin`、`URLConstants.class`、`JumpToBrowserHandler.class` |
| Operation Analyzer | O&M monitoring 面板 | `confirm-network` | `operation-analyzer-plugin` |

## Build / Package / Schema

| 能力 | 价值 | 风险 | 主要证据 |
| --- | --- | --- | --- |
| Hvigor 构建分析与优化 | 构建性能、cache、worker、type check | `allow-static`；执行构建为 `confirm-local` | `hvigor-config-schema.json`、`project-cache-service.js`、`ts_check.js` |
| OHPM dependency-check | 安全、推荐、版本差异 | `allow-static`；真实执行为 `confirm-network` | `dependency-check.js`、`PackageInfoResponse.recommend/security` |
| OHPM lockfile/overrides/exclusions | 依赖治理 | `allow-static`；安装为 `confirm-local`/`confirm-network` | `PackageLocker.js`、`OverrideDepMapManager.js`、`ExclusionsManager.js` |
| OHPM SRI cache / tgz 防御 | 供应链安全 | `allow-static` | `SsriOption.js`、`Integrity.js`、`installRegistryArtifactDep.js` |
| HSP tgz 识别 | HSP/HAR 安装结构 | `allow-static` | `hspDetect.js` |
| app_check_tool 包体扫描 | 重复文件、so、大小、后缀占比 | `confirm-local` | `app_check_tool.jar`、`ScanEntrance` |
| modulecheck schema | router、intent、forms、startup、cross-app shared | `allow-static` | `modulecheck/*.json` |
| configcheck rich/lite schema | module/app/config 规则 | `allow-static` | `configSchema_rich.json`、`configSchema_lite.json` |

## UI Migration / Templates

| 能力 | 价值 | 风险 | 主要证据 |
| --- | --- | --- | --- |
| APK/Dex component analyzer | Android 到 Harmony UI 迁移 | `allow-static`；执行转换为 `confirm-local` | `component_analyze.sh`、`DexParser.findSuper(...)` |
| UI IR 到 ArkTS/Harmony project | UI 生成工程链 | `confirm-local` | `coreability-1.0-SNAPSHOT.jar` |
| ConstraintLayout/RelativeLayout solver | 布局迁移求解 | `allow-static` | `ConstraintGraph`、`AnalyzerPipeline`、`GuideLine` |
| Drawable/resource migration | Android 资源迁移 | `allow-static` | `Vector2Svg`、`ShapeConvertor`、`SelectorConvertor` |
| Project templates | Ability、Page、Widget、CloudDev、Intent 等 | `allow-static`；渲染为 `confirm-local` | `template.json`、`command.xml.ftl` |

## Debug / Device / Runtime

| 能力 | 价值 | 风险 | 主要证据 |
| --- | --- | --- | --- |
| DAP/Jerry/Panda debug | ArkTS/JS/native 调试 | `confirm-device` | `dap4j-6.1.1.280.jar`、debug view |
| C++ DAP memory/data breakpoint | 内存查看、数据断点 | `confirm-device` | `ohos-cpp-dap-client-6.1.1.280.jar` |
| C/C++ LSP/Clangd | native 代码诊断 | `allow-static`；启动 clangd 为 `confirm-local` | `cpp-lsp-devecostudio-6.1.1.280.jar` |
| HDC command wrapper | 本地/远端设备命令 | `confirm-device` | `ohos-hdclib-6.1.1.280.jar` |
| Device File Browser | 设备文件浏览 | `confirm-device` | `device-file-explorer.xml` |
| Database Inspector | RDB/JDBC/Vector DB 查看 | `confirm-device` 或 `confirm-local` | `database-plugin.xml`、`DataParser` |
| LocalTest framework | JS/ETS 本地测试 run/debug | `confirm-local` | `hos-localtest-framework.xml` |

## Profiler / Trace / Diagnostic

| 能力 | 价值 | 风险 | 主要证据 |
| --- | --- | --- | --- |
| Profiler offline import matrix | 多格式离线导入 | `allow-static`；导入用户数据为 `confirm-local` | `file_importer_config.xml` |
| Profiler gRPC protocol | offline/online session | `confirm-device` | `profiler_service.proto` |
| HiPerf parser/symbolizer | `.perfdata/.data` 解析 | `confirm-local` | `ParsePerfData`、`ArkTSSymbolFile` |
| Heap/rawheap/jsleak parser | ArkTS 内存分析 | `confirm-local` | `HeapSnapshotParser`、`ArkVmProfilerMapper.xml` |
| NativeHook parser | native 内存事件与符号化 | `confirm-local` | `native_hook_result.proto` |
| Network profiler parser | HTTP/traffic 解析 | `confirm-local` | `network_profiler_event.proto`、`NetworkMapper.xml` |
| Frame/RS/VSync/jank/GPU | 帧与渲染关联 | `confirm-local` | `FrameMapper.xml`、`RsTreeReplayService` |
| Diagnostic HPROF/GC Root | Java/IDE 内存诊断 | `confirm-local` | `HProfEventBasedParser`、`GCRootPathsTree` |
| Freeze/thread dump attribution | 卡顿、线程 dump、模块归因 | `confirm-local` | `UIFreezeWatcher`、`ProblemModuleAnalyzerUtil` |
| Trace native pipe / WiseEye | telemetry、crash、上传链 | `confirm-network` | `trace-lemon-plugin`、`trace-ide-6.1.1.280.jar` |

## SDK / HMS API Surface

| 能力 | 价值 | 风险 | 主要证据 |
| --- | --- | --- | --- |
| HMS RAG / retrieval / knowledgeProcessor / localChatModel | App 内 AI 与知识库能力 | `allow-static`；真实调用为 `confirm-network` 或设备权限确认 | `sdk/default/hms/ets/api/@hms.data.*.d.ts` |
| NearLink | 近距连接 | `confirm-device` | `@hms.nearlink.*.d.ts` |
| NetworkBoost | 多路径与网络质量 | `confirm-device` | `@hms.networkboost.*.d.ts` |
| Security audit / antifraud / FIDO2 / attestation | 安全、风控、认证 | `confirm-device` / `confirm-network` | `@hms.security.*.d.ts` |
| DLP / sensitive content | 文档权限与敏感内容扫描 | `confirm-local` | `@ohos.dlpPermission.d.ts`、`identifySensitiveContent.d.ts` |
| Child process / kiosk | App 能力控制 | `confirm-device` | `childProcessManager.d.ts`、`kioskManager.d.ts` |
| DriverExtension/HID/USB/SCSI | 外设/驱动开发 | `confirm-device` | native sysroot headers |
| GameController/Display Capture/PiP | 游戏、屏幕、窗口能力 | `confirm-device` | native sysroot headers |

## Cloud / AGC / O&M

| 能力 | 价值 | 风险 | 主要证据 |
| --- | --- | --- | --- |
| Cloud Toolkit deployment | Cloud Function、Cloud DB、ArkData 部署/同步 | `confirm-network` | `deveco-cloud-toolkit-16.4.1.204.jar` |
| Cloud Console web assets | Cloud Function/DB/Storage/Auth 前端入口 | `confirm-network` | `plugins/openharmony/cloud-console-view/asset-manifest.json` |
| Cloud Functions Requestor | 本地/远程函数触发 UI | `confirm-network` | `FunctionTriggerForm.class` |
| Run/debug/generate invoke interface | 云函数运行、调试、接口生成 | `confirm-network` | `RunCloudFunction`、`DebugCloudFunction`、`GenerateInvokeInterfaceAction` |

## Native / Media / Asset Libraries

| 能力 | 价值 | 风险 | 主要证据 |
| --- | --- | --- | --- |
| WebP ImageIO | WebP 读写 | `allow-static`；处理用户文件为 `confirm-local` | `plugins/webp/lib/webp.jar`、`libwebp_jni.dylib` |
| OpenCV / FFmpeg | 图像、视频、二维码、媒体处理 | `allow-static`；处理用户文件为 `confirm-local` | `opencv-*.jar`、`ffmpeg-*.jar` |
| ASTC / texture transcoding | 纹理压缩与转码 | `allow-static`；处理用户文件为 `confirm-local` | `sdk/default/hms/toolchains/lib/*.dylib` |

## Public Promotion Rule

任何条目进入 `harmony-next/SKILL.md`、`README.md` 或公开 reference 前，必须满足：

1. 在本 space 中已有来源、能力、风险、边界。
2. 不包含 token、cookie、真实项目名、内部 URL、真实日志正文、用户路径散列等敏感数据。
3. 动态能力必须从 `allow-static` 升级到确认档，并记录测试账号、测试项目、可写目录、回滚方式。

