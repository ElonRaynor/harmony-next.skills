# Command Line Tools 下载与配置脚本

## 背景

用户提供官方文档 `https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/ide-commandline-get`，要求补齐命令行下载和配置能力。

官方页面结论：

- Command Line Tools 从华为下载中心获取。
- 下载中心页面提供工具完整性校验。
- HarmonyOS SDK 已嵌入命令行工具包，无需额外下载配置。
- 解压后将 `${Command Line Tools解压路径}/command-line-tools/bin` 加入 `PATH`。
- 可用 `codelinter -v` 验证配置是否成功。

## 实现

新增脚本：

```bash
python3 harmony-next/scripts/commandline_tools_manager.py
```

子命令：

- `download --url <direct-archive-url> --output-dir <dir> [--sha256 <digest>]`
- `install --archive <zip|tar> --dest <dir> [--profile auto|path] [--sha256 <digest>]`
- `bootstrap --url <direct-archive-url> --dest <dir> [--profile auto|path] [--sha256 <digest>]`
- `configure --tools-root <dir> --profile auto|path`
- `doctor --tools-root <dir>`

## 边界

- `--url` 必须是下载中心复制出的压缩包直链，不是下载中心页面 URL。
- 下载中心需要浏览器登录态选择包版本；脚本不绕过登录，传下载中心页面 URL 时返回 machine-readable `blocked`，提示用户登录下载中心复制 archive link，或手动下载后使用 `install --archive`。
- 解压 zip/tar 时校验成员路径，拒绝 path traversal 和 tar link entries。
- `--force` 替换非空目录前拒绝 `/`、当前工作目录和用户 Home，避免误删过宽目录。
- zip 解压后按 archive mode 恢复可执行位，避免 `codelinter` 等工具不可执行。
- profile 写入使用 `harmony-next command-line-tools` 标记块，重复执行时替换旧块，不重复追加。
- 默认只配置 `PATH`；传 `--include-sdk-env` 且工具包存在 `sdk/` 时，额外导出 `HOS_SDK_HOME`、`OHOS_BASE_SDK_HOME`、`DEVECO_SDK_HOME`。

## 验证

新增测试：

```bash
python3 -m unittest harmony-next/tests/test_commandline_tools_manager.py
```

覆盖：

- 本地 archive 安装和 profile 写入。
- profile 标记块可重复替换。
- `doctor` 调用 `codelinter -v`。
- SHA256 mismatch blocked。
- 下载中心页面 URL blocked。
- zip path traversal blocked。
- broad destination force blocked。
