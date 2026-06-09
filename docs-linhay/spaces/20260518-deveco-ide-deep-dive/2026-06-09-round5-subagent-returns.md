# 2026-06-09 第五轮子代理回收记录

## 总控约束

- 固定研究根：`/Users/linhey/Desktop/linhay-open-sources/harmony-next.skills/inputs/DevEco-Studio.app/Contents`
- 禁止访问：`/Applications/DevEco-Studio.app`
- 禁止动作：启动 IDE、启动模拟器、启动服务、登录、联网调用、写入 `.app`、改签名、执行会写缓存或项目的命令。
- 允许动作：`find`、`rg`、`zipinfo`、`unzip -p`、`strings`、`sed`、`head`、`file` 等只读静态读取。

## 子代理清单

| Agent | 方向 | 状态 | 归档位置 |
| --- | --- | --- | --- |
| Curie `019eac10-d203-7853-b87b-e30a33ce3d33` | 构建、包管理、校验规则 | 已完成并关闭 | 本文“构建/包管理线” |
| Volta `019eac10-d891-7b53-aa9c-8253c3b895e8` | SDK d.ts/native headers/HMS API | 已完成并关闭 | 本文“SDK/HMS 线” |
| Kuhn `019eac10-d956-7752-8be9-b3f7416932c6` | IDE 插件 actions/tool windows/services | 已完成并关闭 | 本文“IDE 入口线” |
| Leibniz `019eac10-daac-71d1-8e72-a45db4c0d041` | AI/Agent/CodeGenie/Application-Agent/CloudToolkit | 已完成并关闭 | 本文“AI/Agent 线” |
| Erdos `019eac10-dc87-7300-950c-48c22ad9076a` | 离线格式、协议、解析器、native 库 | 已完成并关闭 | 本文“格式/协议/native 线” |

## 构建/包管理线

1. `ohpm dependency-check` 可输出 installed/wanted/latest、推荐替代包、安全更新、漏洞/恶意包信息。  
   证据：`tools/ohpm/lib/commands/dependency-check.js`、`tools/ohpm/lib/core/dependency-check/dependencyCheck.js`、`PackageInfoResponse.recommend/security`。

2. OHPM lockfile 支持统一锁文件、稳定排序、target 专属 lock 名、依赖环检测。  
   证据：`tools/ohpm/lib/core/locker/PackageLocker.js`、`PackageLockerManager.shouldUseUnifiedLockfile`、`getLockFileName.js`。

3. 项目级依赖改写支持 `overrides`、`overrideDependencyMap`、`exclusions`，并检测同一依赖重复修改。  
   证据：`tools/ohpm/resources/schemas/oh-package-json5-schema-project.json`、`OverrideDepMapManager.js`、`ExclusionsManager.js`。

4. OHPM 支持 `@param:` 依赖版本参数化矩阵。  
   证据：`tools/ohpm/lib/core/parameter/types.js`、`ParameterizationConfigFile.js`。

5. OHPM cache 是内容寻址并做 SRI 校验，默认 `sha512`。  
   证据：`tools/ohpm/lib/core/cache/index.js`、`tools/ohpm/lib/tools/ssri/SsriOption.js`、`Integrity.js`。

6. 安装包解压前有防御规则：最大 500MB、拒绝路径穿越、忽略 `.CodeSignature`。  
   证据：`tools/ohpm/lib/core/dependency/dep-install/installRegistryArtifactDep.js`、`common/Constants.js`。

7. HSP tgz 结构识别要求刚好包含 `.har` 与 `.hsp`，安装时分离接口 HAR 与 HSP。  
   证据：`tools/ohpm/lib/core/dependency/util/hspDetect.js`、`installLocalArtifactDep.js`、`installRegistryArtifactDep.js`。

8. OHPM 脚本执行有安全语法：脚本中的 `ohpm` 只能 `ohpm run`，禁止 `--prefix`，alias 防环。  
   证据：`tools/ohpm/lib/core/scripts/compiler.js`、`ScriptRunner.js`、`DirectedGraph.js`。

9. `app_check_tool.jar` 是 HAP/HSP/APP 包体扫描器。  
   证据：`sdk/default/openharmony/toolchains/lib/app_check_tool.jar`，`ScanEntrance`、`ScanStatDuplicate`、`ScanStatFileSize`、`ScanStatSuffix`。

10. Hvigor 有 task/file/buildInfo 三类增量快照缓存，并按 Hvigor 版本变更清理旧缓存。  
    证据：`tools/hvigor/hvigor/src/base/internal/cache/project-cache-service.js`。

11. Hvigor 构建分析/优化旋钮包括 `analyze=ultrafine`、`optimizationStrategy`、worker/内存、rollup cache、single file emit、byteCodeHar、autoLazyImport。  
    证据：`tools/hvigor/hvigor/res/hvigor-config-schema.json`。

12. Hvigor 可对 `hvigorfile.ts` 做 TypeScript 诊断型 type check。  
    证据：`tools/hvigor/hvigor/src/base/internal/util/ts_check.js`、`execution.typeCheck`。

13. modulecheck schema 发现：`appStartupInner.json`、`routerMap.json`、`insightIntent.json`、`crossAppSharedConfig.json`、`forms.json`、`configSchema_lite.json`。

## SDK/HMS 线

1. HMS 本地 RAG/LLM 会话能力：`RagSession.streamRun()`、`createRagSession()`、`feedback()`。  
   证据：`sdk/default/hms/ets/api/@hms.data.rag.d.ts`。

2. HMS RDB 检索、向量召回、重排序能力。  
   证据：`@hms.data.retrieval.d.ts`，`getRetriever()`、`Retriever.retrieveRdb()`、`VectorRecallCondition`、`RerankMethod`。

3. HMS 知识库加工/向量化能力。  
   证据：`@hms.data.knowledgeProcessor.d.ts`，`getKnowledgeProcessor()`、`KnowledgeProcessor.startProcess()`。

4. HMS 本地聊天模型能力。  
   证据：`@hms.data.localChatModel.d.ts`，`init()`、`chat(info, config, callback)`。

5. NearLink 近距连接完整栈。  
   证据：`@hms.nearlink.manager.d.ts`、`advertising.d.ts`、`scan.d.ts`、`ssap.d.ts`、`dataTransfer.d.ts`。

6. NetworkBoost 多路径、弱信号预测、QoE 上报。  
   证据：`@hms.networkboost.handover.d.ts`、`@hms.networkboost.netquality.d.ts`。

7. 企业安全审计/进程与代码签名查询。  
   证据：`@hms.security.securityAudit.d.ts`。

8. 反欺诈、模拟点击、URL 威胁与系统完整性检测。  
   证据：`@hms.security.businessRiskIntelligentDetection.d.ts`、`@hms.security.safetyDetect.d.ts`、`@hms.security.antifraudPicker.d.ts`。

9. FIDO2、可信认证、设备证明/安全位置。  
   证据：`@hms.security.fido2.d.ts`、`trustedAuthentication.d.ts`、`trustedAppService.d.ts`、`deviceCertificate.d.ts`。

10. OpenHarmony DLP 文档权限与敏感内容扫描。  
    证据：`@ohos.security.identifySensitiveContent.d.ts`、`@ohos.dlpPermission.d.ts`。

11. HMS ScreenTimeGuard、LiveView、HealthStore、WearEngine、AR/空间渲染、AI 视觉/语音/NLP。  
    证据：`@hms.utilityApplication.screenTimeGuard.*.d.ts`、`@hms.core.liveview.*.d.ts`、`@hms.health.*.d.ts`、`@hms.core.ar.arengine.d.ts`、`@hms.graphics.spatialRender.d.ts`、`@hms.ai.*.d.ts`。

12. OpenHarmony 子进程、kiosk、DriverExtension、HID、USB Serial、SCSI、GameController、Display Capture、PiP。  
    证据：`@ohos.app.ability.childProcessManager.d.ts`、`kioskManager.d.ts`、native sysroot headers。

## IDE 入口线

1. `Device File Browser`：`plugins/openharmony/lib/device-file-explorer-6.1.1.280.jar!META-INF/device-file-explorer.xml`。
2. `Database Inspector`：`plugins/openharmony/lib/database-plugin-6.1.1.280.jar!META-INF/database-plugin.xml`。
3. `ArkUI-Inspector` / `ArkUIInspector`：`layout-inspector-server-6.1.1.280.jar!META-INF/layout-inspector-server.xml`。
4. `Previewer` / `PreviewerLog` / `PreviewerDebug`：`ohos-preview-plugin-6.1.1.280.jar!META-INF/ohos-previewer.xml`。
5. `Log` tool window + HiLog/FaultLog：`ohos_hilog-6.1.1.280.jar!META-INF/ohos-hilog.xml`。
6. C++ DAP 内存查看和 data breakpoint actions：`ohos-cpp-dap-client-6.1.1.280.jar!META-INF/cpp_dap_plugin.xml`。
7. C/C++ LSP/Clangd performance trace：`cpp-lsp-devecostudio-6.1.1.280.jar!META-INF/extended.xml`。
8. Project generator actions：`Ohos.NewImageAsset`、`Ohos.NewStaticWidgetAction`、`Ohos.InsightIntent`、多类 Extension Ability。
9. Project/module export and cross-platform conversion：`Ohos.ExportAppScope`、`Ohos.ExportModule`、`Ohos.ConvertCrossPlatformModule`。
10. `AppAnalyzer`、`CloudDev`、`Cloud Functions Requestor`、`LocalTestRunConfigurationType`、`API Change Assistant`、`Cangjie(Experiment)`。
11. `Application Agent`、`Operation Analyzer`、`CodeGenie` tool windows/actions、`UI Generation`、`Build Analyzer`、`Coverage`。

## AI/Agent 线

1. CodeGenie 自定义 Agent 配置与执行路由。  
   证据：`AgentHandler.class`；路由含 `agentConfig.addCustomAgent`、`agentConfig.modifyAgent`、`agentChat.invokeTool`、`agentChat.uploadImage`、`agentChat.acceptAllDiff`、`agentChat.confirmMaxSteps`。

2. CodeGenie MCP 本地服务管理与环境选择。  
   证据：`McpHandler.class`；路由含 `mcp.addServer`、`mcp.modifyServer`、`mcp.chooseEnv`、`mcp.serverEnvCheck`、`mcp.delServerEnv`。

3. CodeGenie MCP Market 配置模板与外跳入口。  
   证据：`McpMarketHandler.class`。

4. CodeGenie Rules 项目/全局规则文件能力。  
   证据：`RuleHandler.class`、`RuleFilePersistentState`。

5. CodeGenie Skills 导入/启用/编辑能力。  
   证据：`SkillHandler.class`。

6. CodeGenie 长期记忆开关与记忆管理。  
   证据：`MemoryHandler.class`、`MemoryConfigStore`、`MemorySystemManager`、`MemoryType.LONG_TERM`。

7. CodeGenie 本地 LanceDB/向量记忆服务。  
   证据：`plugins/codegenie-plugin/lancedb_server/main.js`、`LocalMemoryStore.class`、`LanceDbMemoryRepository`、`DatabaseWebSocketClient`。

8. Codebase feature ask 本地 WebSocket 模型入口。  
   证据：`plugins/codegenie-plugin/codebase_feature_ask/config/websocket.json`，`port: 9588`、`supportsFunctionCalling: true`、`contextWindow: 131072`。

9. Codebase feature ask 工具/提示模块配置。  
   证据：`config/tools.json`，`maxAgenticTurns: 100`、`fileContext.maxFiles: 10`、`promptModules.availableSubAgents`、`promptModules.availableSkills`。

10. Harmony 页面生成与预览服务。  
    证据：`PageHandler.class`、`instrumented-codegenie-page-generation.jar!/META-INF/harmony-page.xml`。

11. Application Agent 本地 web 资源协议与外部浏览器跳转白名单。  
    证据：`URLConstants.class`、`JumpToBrowserHandler.class`。

12. Cloud Toolkit CEF 本地消息分发、Cloud Console 前端资源、Cloud Function 本地/远程触发 UI、run/debug/生成调用接口命令入口。  
    证据：`deveco-cloud-toolkit-16.4.1.204.jar`、`cloud-console-view/asset-manifest.json`。

## 格式/协议/native 线

1. APP/HAP/HAR/HSP/HQF/TGZ/ZIP 离线包解析与嵌套 archive tree。  
   证据：`plugins/openharmony/lib/build-system-6.1.1.280.jar`。

2. OpenHarmony 工程 JSON5/JSON 模型解析。  
   证据：`plugins/openharmony/lib/ohos-project-model-6.1.1.280.jar`。

3. Stage/FA 资源、module/app/package JSON schema 与资源仓库解析。  
   证据：`plugins/openharmony/lib/ohos-resource-6.1.1.280.jar`。

4. config-json 可视化 JSON schema/data 协议对象。  
   证据：`plugins/openharmony/lib/resource-common-6.1.1.280.jar`。

5. DAP/Debug Adapter Protocol 消息适配与扩展请求模型。  
   证据：`plugins/openharmony/lib/dap4j-6.1.1.280.jar`。

6. LSP/Language Server Protocol 客户端封装。  
   证据：`plugins/openharmony/lib/lsp4intellij-6.1.1.280.jar`。

7. HDC 本地/远端命令协议封装。  
   证据：`plugins/openharmony/lib/ohos-hdclib-6.1.1.280.jar`。

8. RDB/JDBC/Vector DB 表数据与 SQL 结果解析。  
   证据：`plugins/openharmony/lib/database-plugin-6.1.1.280.jar`。

9. UI Generator 的 DEX/模板/资源插入解析。  
   证据：`plugins/ui-generator/lib/instrumented-ui-generator-6.1.0.660.jar`。

10. Obfuscation Helper、CodeLinter 的 Excel/CSV 导出与结果解析。  
    证据：`instrumented-obfuscation-helper-6.1.1.280.jar`、`instrumented-codelinter-6.1.1.280.jar`。

11. CodeGenie MCP schema、Markdown rule/skill 解析、LanceDB/Arrow/FlatBuffers、ONNX runtime。  
    证据：`instrumented-codegenie-infrastructure-6.1.1.280.jar`、`lancedb.darwin-arm64.node`、`model_fp16.onnx`、`onnxruntime-1.20.0.jar`。

12. WebP ImageIO、OpenCV、FFmpeg、ASTC/texture transcoding native 库。  
    证据：`plugins/webp/lib/webp.jar`、`plugins/harmony/lib/opencv-*.jar`、`ffmpeg-*.jar`、`sdk/default/hms/toolchains/lib/*.dylib`。

## 总控审核结论

- 第五轮所有子代理均声明只读、workspace 副本、未访问 `/Applications`、未启动/未写入。
- 已从聊天报告转为 space 内台账，后续公开文档只能引用本 space 的已审条目。
- 第五轮结果与第四轮有部分重叠，重复项在 `2026-06-09-static-research-ledger.md` 中按高级/中级/入口/AI 细项重新归并。

