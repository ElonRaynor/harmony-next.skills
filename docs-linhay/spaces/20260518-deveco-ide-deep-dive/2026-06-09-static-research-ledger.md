# 2026-06-09 DevEco Studio 静态研究台账

## 执行约束

- 固定研究根：`/Users/linhey/Desktop/linhay-open-sources/harmony-next.skills/inputs/DevEco-Studio.app/Contents`
- 禁止对象：`/Applications/DevEco-Studio.app`
- 执行边界：只读静态审计，不启动 DevEco Studio、模拟器、预览器、HDC、Profiler、Cloud Toolkit、CodeGenie 服务或任何会写缓存/改签名/联网的命令。
- 允许方法：`find`、`rg`、`zipinfo`、`unzip -p`、`strings`、`sed`、`head`、`file` 等静态读取。
- 产出位置：本 space 内部，先沉淀研究结论，再决定是否进入公开 skill 或 reference。

## 子代理编排记录

第五轮共拆 5 条只读探索线，均已回收并关闭：

1. 构建/包管理/校验规则：`tools/hvigor`、`tools/ohpm`、`toolchains/configcheck/modulecheck/syscapcheck`。
2. SDK d.ts/native headers/HMS API：`sdk/default/openharmony`、`sdk/default/hms`。
3. IDE 插件隐藏 actions/tool windows/services：`plugins/*/lib/*.jar`、`lib/modules/*.jar`。
4. AI/Agent/CodeGenie/Celia/Application-Agent/CloudToolkit：本地协议、路由、缓存、模板、前端资源。
5. 性能/诊断以外的离线格式、协议、解析器、native 库。

## 前几轮已确认高价值线索

这些项目来自前序静态轮次，当前仍以 workspace 副本作为后续唯一证据源：

1. Ark/Panda `ark_disasm` 反汇编入口。
2. `rawheap_translator` 与 ArkTS/rawheap 离线分析链。
3. Previewer native Ark runtime 与预览服务能力。
4. HAP/HSP/APP/ELF 签名、验签、profile、provision 工具体系。
5. CodeGenie 本地 DB schema、inline completion、RAG、LanceDB 与 embedding model。
6. Hvigor native build、pack/sign/profile merge、构建分析与优化。
7. Native sanitizer、coverage、LLDB、C/C++ DAP/LSP 调试能力。
8. HDC 本地/远端命令协议封装。
9. `trace_streamer`、DAP sidecar、Profiler/Trace 离线格式解析。
10. Project/Module/Ability/Page/Widget/CloudDev/Insight Intent 等模板矩阵。
11. OHPM 发布、预发布、资产泄露、兼容性、包大小与 schema 校验。
12. IDE hidden actions、tool windows、inspection、local history、coverage、terminal block UI。

## 第四轮清单回填

### 高级

1. UI Generator Android APK/Dex component analyzer：`plugins/ui-generator/lib/instrumented-ui-generator-6.1.0.660.jar!/sim-sdk/component_analyze.sh`。
2. UI Generator IR 到 ArkTS/Harmony project generation：`plugins/ui-generator/lib/coreability-1.0-SNAPSHOT.jar`。
3. ConstraintLayout/RelativeLayout migration solver：`ConstraintGraph`、`AnalyzerPipeline`、`GuideLine`。
4. Android drawable/resource migration：`Vector2Svg`、`ShapeConvertor`、`SelectorConvertor`、`ResourceManager`。
5. Profiler offline import matrix：`plugins/ohos-profiler/lib/instrumented-ohos-profiler-6.1.1.280.jar!/config/import/file_importer_config.xml`，覆盖 `heapsnapshot/rawheap/htrace/ftrace/sys/perfdata/data/nas/acm/insight/jsleaklist/sourceMap/nameCache`。
6. Profiler gRPC session protocol：`profiler_service.proto`、`profiler_service_types.proto`，含 `GetCapabilities`、`CreateSession`、`FetchData`、`SubscribeProfilerEvt`、`OFFLINE/ONLINE`。
7. HiPerf `.perfdata/.data` Java parser and symbolizer：`ParsePerfData`、`PerfRecordSampleHandler`、`ElfFileSymbolFile`、`ArkTSSymbolFile`、`CangjieSymbolFile`、`KernelSymbolFile`。
8. ArkTS heap/rawheap/jsleak offline parser：`HeapSnapshotParser`、`JsHeapSnapshot`、`ArkVmProfilerMapper.xml`。
9. SourceMap/nameCache/NAPI symbol restoration：`SrcMapDecoder`、`ObfuscationDecoder`、`NapiSymManager`、`importOfflineSymbols`。
10. NativeHook offline IP symbolization and memory event model：`native_hook_result.proto`、`NativeHookOfflineSceneExtensionParser`。
11. Network profiler HTTP/traffic parser：`network_profiler_event.proto`、`NetworkMapper.xml`。
12. Frame/RS/VSync/jank/GPU correlation：`FrameMapper.xml`、`RsTreeReplayService`、`RsNodeService`、`FrameLayoutService`。
13. Diagnostic HPROF/GC root analysis engine：`plugins/diagnostic-plugin/lib/instrumented-diagnostic-plugin-6.1.1.280.jar`，`HProfEventBasedParser`、`HistogramVisitor`、`GCRootPathsTree`、`AnalyzeGraph`、`HProfAnalysis`。
14. Diagnostic freeze/thread dump module attribution：`UIFreezeWatcher`、`IdeFreezeReporter`、`ProblemModuleAnalyzerUtil`、`problemAnalyze/package_white_list`。
15. SDK signing/profile/provision chain：`sdk/default/openharmony/toolchains/lib/hap-sign-tool.jar`、`binary-sign-tool.jar`、profile PEM/templates、HMS `sdk-sign-tool-full.jar`、`Provisionsigntool.jar`、`defaultSignConfigs.json`、`defaultVerifyConfig.json`。

### 中级

1. Application Agent local JCEF bridge：`Application-Agent-Plugin`、`MessageRouterHandler`、`OpenAgentPlatformHandler`、`LoginHandler`、webview assets。
2. Celia/Agent OAuth and permission gate：`env_common.properties`、`TokenManager`、`EnvPropertiesKey`。
3. ohos-trace native pipe telemetry/crash upload：`trace-lemon-plugin`、`LocalReadAndWriteByNativeService`、`PipeNameRunnable`、`TraceCrashFileUtils`、`libide_pipe_jni*.dylib`。
4. trace-ide WiseEye local/write/upload chain：`trace-ide-6.1.1.280.jar`、`BatchUploadTraceDataWorker`、`WriteLocalTraceDataWorker`、`Signer`、`AkSkUtil`。
5. Obfuscation Helper keep-surface analyzer：`plugins/obfuscation-helper/agent/task/ObfuscationAnalyzer.d.ts`，`JSONTask`、`SoLibApiTask`、`HarExportApiTask`、`DynamicLoadingTask`、`NapiTask`、`NavigationTask`、`DataBaseTask`。
6. OHPM publish/prepublish compliance：`PublishCore.js`、`checkAndAlarmAssetLeakage.js`、`validateCompability.js`、`validateHmPackage.js`、`validatePkgSize.js`。
7. OHPM schema/custom validation：`tools/ohpm/resources/schemas/oh-package-json5-schema*.json`、`OhPkgValidationConfig.json`。
8. Manifest/config rich schema：`sdk/default/openharmony/toolchains/configcheck/configSchema_rich.json`。
9. Hvigor build-profile hardening：`tools/hvigor/hvigor-ohos-plugin/res/schemas/ohos-module-build-profile-schema.json`、`ohos-project-build-profile-schema.json`。
10. Syscap/ArkData schema：`toolchains/syscapcheck/sysCapSchema.json`、`toolchains/modulecheck/arkDataSchema.json`。
11. AGC/Cloud Toolkit deployment/permission/schema：`deveco-cloud-toolkit-16.4.1.204.jar`、`DeployService`、`PackageCloudFunction`、`CloudDbSyncService`、`CheckPermissionResp`、`cloud-config-schema.json`、`function-config-schema.json`。
12. SDK modulecheck protocols：`crossAppSharedConfig.json`、`customUtds.json`、`insightIntent.json`、`appStartup.json`、`routerMap.json`、`startWindow.json`。
13. Web Native Messaging + ArkWeb scheme handler：`@ohos.web.WebNativeMessagingExtensionAbility.d.ts`、`native/sysroot/usr/include/web/arkweb_scheme_handler.h`。
14. Native ContentEmbed/ObjectEditor C API：`ContentEmbedKit/content_embed/*.h`。
15. HMS DeviceCloudGateway cloud resource/storage/database：`@hms.core.deviceCloudGateway.cloudResPrefetch.d.ts`、`cloudStorage.d.ts`、`cloudDatabase.d.ts`。

### 基础/平台

1. Dev PSI Viewer + debugger PSI：`plugins/dev/lib/dev.jar`、`intellij.dev.psiViewer.xml`、`intellij.java.dev.xml`。
2. FUS/Statistics Event Log DevKit：`intellij.platform.statistics.devkit.xml`、`schemas/events-test-scheme.schema.json`。
3. Performance Testing local playback：`performanceTesting.jar`、`commandProvider`、`LocalPlaybackRunner`、`SimulateFreeze`。
4. Terminal Block UI/OSC command block protocol：`plugins/terminal`、`terminal.new.ui.*`、`command-block-support.zsh`、OSC `1341`。
5. JSON Schema/JSON hidden actions：`plugins/json/lib/json.jar`、`JsonCopyPointer`、`ConsoleView.ShowAsJsonAction`、`JsonJacksonReformatAction`。
6. YAML schema/search everywhere：`plugins/yaml/lib/yaml.jar`、`YAMLKeysSearchEverywhereContributor`。
7. EditorConfig export/generation：`plugins/editorconfig/lib/editorconfig.jar`。
8. Properties/ResourceBundle tools：`plugins/properties/lib/properties.jar`。
9. Shell Script runner/ShellCheck/shfmt/templates：`plugins/sh/lib/sh.jar`。
10. Platform modules：coverage、local history、smart update、freeze、inline completion，证据在 `Contents/lib/modules/*.jar`。
11. CLI headless entries：`Contents/bin/format.sh`、`inspect.sh`、`ltedit.sh`，当前只记录不运行。

## 第五轮高级发现

1. **HMS 本地 RAG/LLM 会话能力**  
   证据：`sdk/default/hms/ets/api/@hms.data.rag.d.ts`，`RagSession.streamRun()`、`createRagSession()`、`feedback()`。

2. **HMS 检索增强与向量召回链**  
   证据：`@hms.data.retrieval.d.ts`，`Retriever.retrieveRdb()`、`VectorRecallCondition`、`RerankMethod`。

3. **HMS 知识库加工/向量化能力**  
   证据：`@hms.data.knowledgeProcessor.d.ts`，`getKnowledgeProcessor()`、`KnowledgeProcessor.startProcess()`。

4. **CodeGenie 自定义 Agent 与 MCP 管理面**  
   证据：`plugins/codegenie-plugin/lib/instrumented-CodeChat.jar`，`AgentHandler`、`McpHandler`、`McpMarketHandler`。

5. **CodeGenie Rules/Skills/Memory 本地治理能力**  
   证据：`RuleHandler`、`SkillHandler`、`MemoryHandler`、`RuleFilePersistentState`、`MemoryType.LONG_TERM`。

6. **CodeGenie 本地 LanceDB/ONNX/RAG 运行时**  
   证据：`codegenie-plugin/lancedb_server/main.js`、`embedding_model/VESO-model/VESO-25M/model_fp16.onnx`、`rag-core-6.1.1.280.jar`、`onnxruntime-1.20.0.jar`。

7. **APP/HAP/HAR/HSP/HQF/TGZ/ZIP 离线包解析器**  
   证据：`plugins/openharmony/lib/build-system-6.1.1.280.jar`，`AppFileParser`、`HapFileParser`、`HarFileParser`、`ArchiveService.openInnerArchive(...)`。

8. **OpenHarmony 工程 JSON5/JSON 模型解析器**  
   证据：`plugins/openharmony/lib/ohos-project-model-6.1.1.280.jar`，`ProjectBuildProfileJson5ParserV2`、`ModuleJson5Parser`、`ConfigJsonParser`、`LockJson5Parser`。

9. **DAP/LSP 协议客户端封装**  
   证据：`dap4j-6.1.1.280.jar`、`lsp4intellij-6.1.1.280.jar`，`GenericIDebugProtocolClient`、`LanguageServerWrapper`。

10. **HMS 安全审计、反欺诈、FIDO2 与设备证明**  
    证据：`@hms.security.securityAudit.d.ts`、`businessRiskIntelligentDetection.d.ts`、`safetyDetect.d.ts`、`fido2.d.ts`、`trustedAppService.d.ts`。

## 第五轮中级发现

1. **NearLink 近距连接完整栈**  
   证据：`@hms.nearlink.manager.d.ts`、`advertising.d.ts`、`scan.d.ts`、`ssap.d.ts`、`dataTransfer.d.ts`。

2. **NetworkBoost 多路径、弱信号预测、QoE 上报**  
   证据：`@hms.networkboost.handover.d.ts`、`@hms.networkboost.netquality.d.ts`。

3. **OpenHarmony DLP 文档权限与敏感内容扫描**  
   证据：`@ohos.security.identifySensitiveContent.d.ts`、`@ohos.dlpPermission.d.ts`。

4. **OpenHarmony 子进程与 kiosk 模式**  
   证据：`@ohos.app.ability.childProcessManager.d.ts`、`@ohos.app.ability.kioskManager.d.ts`。

5. **外设/驱动开发：HID、USB Serial、SCSI**  
   证据：`DriverExtensionAbility.d.ts`、`hid_ddk_api.h`、`usb_serial_api.h`、`scsi_peripheral_api.h`。

6. **原生游戏手柄、屏幕捕获、PiP**  
   证据：`GameControllerKit/game_device.h`、`game_pad.h`、`window_manager/oh_display_capture.h`、`oh_window_pip.h`。

7. **RDB/JDBC/Vector DB 表数据与 SQL 结果解析**  
   证据：`database-plugin-6.1.1.280.jar`，`DataParser.parseResult(...)`、`parseVectorDbTableField(...)`、`RdbDatabaseService`、`JdbcDatabaseService`。

8. **Stage/FA 资源仓库与 JSON schema provider**  
   证据：`ohos-resource-6.1.1.280.jar`，`RepositoryLoader`、`ResourceFolderLoader`、`AppJson5SchemaProvider`、`ModuleJson5SchemaProvider`。

9. **config-json 可视化协议对象**  
   证据：`resource-common-6.1.1.280.jar`，`JsonSchemaRsp`、`JsonDataRsp`、`ResponsePacket`、`DynamicDataType`。

10. **OHPM dependency-check 安全/推荐/版本检查**  
    证据：`tools/ohpm/lib/commands/dependency-check.js`、`core/dependency-check/dependencyCheck.js`、`PackageInfoResponse.recommend/security`。

11. **OHPM unified lockfile 与依赖环检测**  
    证据：`PackageLocker.js`、`PackageLockerManager.shouldUseUnifiedLockfile`、`getLockFileName.js`。

12. **OHPM overrides/exclusions/参数化版本矩阵**  
    证据：`oh-package-json5-schema-project.json`、`OverrideDepMapManager.js`、`ExclusionsManager.js`、`core/parameter/types.js`。

13. **OHPM 内容寻址缓存与 SRI 校验**  
    证据：`core/cache/index.js`、`SsriOption.js`、`Integrity.js`。

14. **OHPM tgz 解压防御与 HSP 结构识别**  
    证据：`installRegistryArtifactDep.js`、`Constants.js`、`hspDetect.js`。

15. **Hvigor 增量快照缓存与 type check**  
    证据：`project-cache-service.js`、`ts_check.js`、`hvigor-config-schema.json`。

16. **`app_check_tool.jar` 包体扫描器**  
    证据：`sdk/default/openharmony/toolchains/lib/app_check_tool.jar`，`ScanEntrance`、`ScanStatDuplicate`、`ScanStatFileSize`、`ScanStatSuffix`。

17. **HAR/HSP 启动任务 DAG schema**  
    证据：`toolchains/modulecheck/appStartupInner.json`。

18. **RouterMap/Insight Intent/CrossAppShared/Forms rich schema**  
    证据：`routerMap.json`、`insightIntent.json`、`crossAppSharedConfig.json`、`forms.json`。

19. **Obfuscation Helper Excel/CSV 规则导出**  
    证据：`instrumented-obfuscation-helper-6.1.1.280.jar`，`EasyExcelUtil`、`AgentResultParseUtil`、`ExportScanData`。

20. **CodeLinter 结果 Excel 导出与 exclude 解析**  
    证据：`instrumented-codelinter-6.1.1.280.jar`，`ExcelUtil.writeDefectsToExcelEx(...)`、`ExportExcelHandler`、`ExcludeFoldersParser`。

## 第五轮 IDE 入口发现

1. `Device File Browser` tool window：`device-file-explorer-6.1.1.280.jar!META-INF/device-file-explorer.xml`。
2. `Database Inspector` tool window：`database-plugin-6.1.1.280.jar!META-INF/database-plugin.xml`。
3. `ArkUI-Inspector` / `ArkUIInspector`：`layout-inspector-server-6.1.1.280.jar!META-INF/layout-inspector-server.xml`。
4. `Previewer` / `PreviewerLog` / `PreviewerDebug`：`ohos-preview-plugin-6.1.1.280.jar!META-INF/ohos-previewer.xml`。
5. `Log` tool window + HiLog/FaultLog actions：`ohos_hilog-6.1.1.280.jar!META-INF/ohos-hilog.xml`。
6. C++ DAP 内存查看与 data breakpoint actions：`ohos-cpp-dap-client-6.1.1.280.jar!META-INF/cpp_dap_plugin.xml`。
7. C/C++ LSP/Clangd performance trace：`cpp-lsp-devecostudio-6.1.1.280.jar!META-INF/extended.xml`。
8. `Ohos.NewImageAsset`、`Ohos.NewStaticWidgetAction`、`Ohos.InsightIntent`：`project-mgmt-6.1.1.280.jar!META-INF/project-mgmt.xml`。
9. `EmbeddedUIExtensionAbilityAction`、`BackupAbilityExtAction`、`DriverExtAbilityAction`、`WorkSchedulerExtAbility`：`project-mgmt.xml`。
10. `Ohos.ExportAppScope`、`Ohos.ExportModule`、`Ohos.ConvertCrossPlatformModule`：`project-mgmt.xml`。
11. `AppAnalyzer` tool window/action：`hos-app-analyzer-6.1.1.280.jar!META-INF/hos-app-analyzer.xml`。
12. `LocalTestRunConfigurationType` / `LocalTestDebugProgramRunner`：`hos-localtest-framework-6.1.1.280.jar!META-INF/hos-localtest-framework.xml`。
13. `API Change Assistant`：`project-api-change-assistant-6.1.1.280.jar!META-INF/hos-project-api-change-assistant.xml`。
14. `Cangjie(Experiment)` settings/services：`cangjie-mgmt-plugin-6.1.1.280.jar!META-INF/cangjie-mgmt-plugin.xml`。
15. `Operation Analyzer` tool window：`operation-analyzer-plugin/lib/instrumented-operation-analyzer-plugin-6.1.1.280.jar!META-INF/plugin.xml`。
16. `Build Analyzer` action / Hvigor services：`hvigor-support/lib/instrumented-hvigor-support-6.1.1.280.jar!META-INF/plugin.xml`。
17. Coverage tool window/actions：`lib/modules/intellij.platform.coverage.jar!intellij.platform.coverage.xml`。
18. UI Generation tool window/wizard：`ui-generator/lib/instrumented-ui-generator-6.1.0.660.jar!META-INF/plugin.xml`。

## 第五轮 AI/Agent 与 CloudToolkit 细项

1. CodeGenie 自定义 Agent 路由：`agentConfig.addCustomAgent`、`agentConfig.modifyAgent`、`agentChat.invokeTool`、`agentChat.uploadImage`、`agentChat.acceptAllDiff`、`agentChat.confirmMaxSteps`。
2. CodeGenie MCP 路由：`mcp.addServer`、`mcp.modifyServer`、`mcp.chooseEnv`、`mcp.serverEnvCheck`、`mcp.delServerEnv`。
3. MCP Market 路由：`mcp.market.getServerList`、`mcp.market.getServerConfigTemplate`、`mcp.market.addServer`、`mcp.market.jump`。
4. Rules 路由：`createProjectRuleMDFile`、`importProjectRule`、`queryGlobalRuleList`、`setUseGlobalRuleFile`。
5. Skills 路由：`skill.importProjectSkill`、`skill.importGlobalSkill`、`skill.enableProjectSkill`、`skill.enableGlobalSkill`、`skill.editProjectSkill`。
6. Memory 路由：`memory.getMemoriesStatus`、`memory.setMemoryEnable`、`memory.deleteMemory`、`memory.editMemory`。
7. Codebase feature ask WebSocket 配置：`codegenie-plugin/codebase_feature_ask/config/websocket.json`，`port: 9588`、`supportsFunctionCalling: true`、`contextWindow: 131072`。
8. Codebase feature ask 工具配置：`config/tools.json`，`maxAgenticTurns: 100`、`fileContext.maxFiles: 10`、`promptModules.availableSubAgents`、`promptModules.availableSkills`。
9. Harmony 页面生成路由：`page.initHarmonyPage`、`page.forwardDataToPreViewTab`、`page.fileInfo`、`page.sendCompileFix`。
10. 页面生成客户端资源：`page_generation_client/component/module_v4.json`、`real_images/real_images.json`、`resource/template_resource.json`、`base64_icons_all_black.json`。
11. 自定义 prompt 菜单：`PromptHandler`、`PromptConfigStore`、`CustomPromptMenuManager`、`CustomPromptAction`。
12. 历史导出/检索/删除：`HistoryHandler`、`exportHistory`、`searchHistory`、`deleteHistory`、`HistoryHelper.saveMarkdown`。
13. 内置 Agent/任务目录：`promptGPTs/zh/defaultGPTsList.json`、`promptGPTs/en/defaultGPTsList.json`。
14. Application Agent 本地 web origin：`http://agent/index.html`，证据 `URLConstants.class`、`webview/index.html`。
15. Application Agent 外跳白名单：`JumpToBrowserHandler.class`，仅允许 `https` 且 host 后缀为 `huawei.com` 或 `cac.gov.cn`。
16. Cloud Toolkit CEF 消息分发：`WindowPanel$MyCefMessageRouterHandlerAdapter.class`，`key`、`data`、`cefQueryHandlerHashMap`。
17. Cloud Console 前端资源：`plugins/openharmony/cloud-console-view/asset-manifest.json`，`AgcConsoleLogin`、`AgcGetUserInfo`、`AgcGotoServerless`、`AgcOpenRequest`。
18. Cloud Functions Requestor：`deveco-cloud-toolkit.xml`，`id="Cloud Functions Requestor"`、`FunctionTriggerWindowFactory`。
19. Cloud Function 本地/远程触发 UI：`FunctionTriggerForm.class`，`LOCAL`、`REMOTE`、`EVENT`、`RESULT`、`LOGS`。
20. Cloud Toolkit run/debug/接口生成：`RunCloudFunction`、`DebugCloudFunction`、`GenerateInvokeInterfaceAction`。
21. CloudDev 工程/文件模板：`templates/ability/[CloudDev]Empty Ability/template.json`、`cloud_function_empty_handler.ts.ft`、`cloud_functions_run_env.json.ft`、`cloud_functions_run_wrapper.js.ft`。

## 资产/格式/native 库发现

1. UI Generator DEX/模板/资源插入：`DexParser.findSuper(...)`、`TemplateManager.getTemplate(...)`、`ResourceFileInsertStrategy`、`ETSFileInsertStrategy`。
2. CodeGenie MCP schema 与 Markdown rule/skill 解析：`McpConfigManager.parseConfigFile()`、`McpServerConnector.buildStdioClient(...)`、`MarkdownRuleFileVisitor`、`SkillParser.parseSkill(...)`。
3. LanceDB native binding 与 Arrow/FlatBuffers：`lancedb.darwin-arm64.node`、`apache-arrow/src/ipc/reader.ts`、`writer.ts`、`flatbuffers/js/byte-buffer.js`。
4. WebP ImageIO 与 libwebp JNI：`plugins/webp/lib/webp.jar`、`plugins/webp/lib/libwebp/mac/libwebp_jni.dylib`。
5. OpenCV/FFmpeg/纹理压缩 native 库：`opencv-4.10.0-1.5.11-macosx-arm64.jar`、`ffmpeg-7.1-1.5.11-macosx-arm64.jar`、`libastc_encoder_shared.dylib`、`libimage_transcoder_shared.dylib`、`libtextureSuperCompress.dylib`。

## 下一步只读沉淀任务

1. 继续把 jar 内 `META-INF/*.xml` 汇总成 action/toolWindow/service/extension point 矩阵。
2. 为 CodeGenie 单独建一份 route map，区分本地只读配置、可能写用户数据、可能联网、必须确认四类。
3. 为 OHPM/Hvigor/modulecheck 建一份 schema index，后续服务于 harmony-next skill 的“配置诊断”能力。
4. 为 SDK/HMS d.ts 建一份 API capability index，标注“只是声明”与“IDE 内置工具可直接复用”的差异。
5. 为 UxTestService 另开规则表，提取 checker、输入、输出、风险、离线可运行性。
