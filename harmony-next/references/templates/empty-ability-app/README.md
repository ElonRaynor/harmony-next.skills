# Empty Ability 最小测试工程模板

该目录是可直接复制的 HarmonyOS NEXT Stage 模型 `Empty Ability` 最小工程，用于 agent 在不打开 DevEco Studio 向导的情况下创建测试 fixture。

来源边界：

- 工程结构参考本机 DevEco Studio 模板：
  `/Applications/DevEco-Studio.app/Contents/plugins/openharmony/lib/templates/project/New Project`
- Ability 与页面结构参考本机 DevEco Studio 模板：
  `/Applications/DevEco-Studio.app/Contents/plugins/openharmony/lib/templates/ability/Empty Ability`
- 模板已去除本机签名材料、绝对路径、IDE 缓存和向导占位符。

默认参数：

| 字段 | 值 |
| --- | --- |
| bundleName | `com.example.emptyability` |
| moduleName | `entry` |
| abilityName | `EntryAbility` |
| Compatible SDK | `5.0.0(12)` |
| targetSdkVersion | `5.0.0(12)` |
| modelVersion | `5.0.0` |
| runtimeOS | `HarmonyOS` |
| deviceTypes | `phone`, `tablet`, `2in1` |

复制后至少修改：

1. `AppScope/app.json5` 的 `bundleName`。
2. `AppScope/resources/base/element/string.json` 的 `app_name`。
3. 如需真机构建签名，在目标工程内用 DevEco Studio 或本地签名配置生成 `signingConfigs`，不要把个人签名材料提交到模板。
4. 如需替换应用图标，覆盖 `AppScope/resources/base/media/app_icon.png` 即可。
5. `entry/src/main/module.json5` 的 Ability `icon` 和 `startWindowIcon` 默认复用同一资源。

基本校验：

```bash
cd <copied-project>
/Applications/DevEco-Studio.app/Contents/tools/ohpm/bin/ohpm install
/Applications/DevEco-Studio.app/Contents/tools/hvigor/bin/hvigorw --mode module -p module=entry@default assembleHap
```

HDC / Emulator smoke：

```bash
HDC="/Applications/DevEco-Studio.app/Contents/sdk/default/openharmony/toolchains/hdc"
TARGET="127.0.0.1:10100"
BUNDLE="com.example.emptyability"
ABILITY="EntryAbility"
HAP="$(find entry/build -name '*.hap' | head -1)"

"$HDC" -t "$TARGET" install "$HAP"
"$HDC" -t "$TARGET" shell aa start -b "$BUNDLE" -a "$ABILITY"
"$HDC" -t "$TARGET" shell uitest dumpLayout -p /dev/null -a
"$HDC" -t "$TARGET" shell uitest screenCap -p /dev/null
```

不同 DevEco/Hvigor 版本的输出路径可能不同。若找不到 HAP，先执行：

```bash
find entry/build -name '*.hap' -print
```
