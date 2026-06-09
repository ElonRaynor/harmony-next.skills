# DevEco Emulator 流量转发深度研究

## 背景

用户追问“能不能转发模拟器流量”，并提供本机 `/Applications/DevEco-Studio.app/`。本轮目标是区分以下几类能力：

1. `hdc fport/rport` 端口转发。
2. Emulator 自带 `-http_proxy` 与 UI 代理面板。
3. HarmonyOS 应用级 HTTP/WebView/WebSocket/RCP 代理。
4. 设备侧 VPN/TUN 透明接管。

## 本机环境

- DevEco Studio：`6.1.1.280`，`CFBundleVersion=DS-243.24978.46.36.611280`。
- HarmonyOS Emulator：`6.1.1.200`。
- 已完成的运行态实验来自 `Codex Test Phone`，HarmonyOS `6.0.2(22)`。
- 实验时 HDC target：`127.0.0.1:5555 TCP Connected localhost`。
- 实验时设备网络：`eth0=10.0.2.15/24`，默认网关 `10.0.2.2`。
- 实验时端口转发：`hdc -t 127.0.0.1:5555 fport ls` 返回 `[Empty]`。
- 2026-06-09 继续实验时，HDC 旧目标先显示 `127.0.0.1:5555 TCP Offline localhost`；执行 `hdc kill && hdc start` 后 target 列表变为 `[Empty]`。`hvd_manager.py launch` 因 trace socket 超时未能重新拉起模拟器，`Emulator -list -details` 也会挂起，需要从 DevEco Studio Device Manager 侧恢复 HVD 后再做 UI 实验。
- 2026-06-09 直接测试：原生命令 `Emulator -hvd "Codex Test Phone" -path ~/.Huawei/Emulator/deployed -imageRoot ~/Library/Huawei/Sdk` 启动后进程很快退出，90 秒轮询 `hdc list targets -v` 始终为 `[Empty]`。`open -a /Applications/DevEco-Studio.app` 只留下一个很小的 `devecostudio` launcher 进程，未拉起完整 IDE/Java 主进程，也未产生 HDC target。
- 同轮直接测试里，`scutil --proxy` 显示 macOS 系统 `HTTPEnable=0`、`HTTPSEnable=0`、`SOCKSEnable=0`，`lsof` 未发现 Proxyman/Charles/mitmproxy/Shadowrocket 常见代理端口监听。此状态下无法做新的 guest -> Mac 代理连通性验证。

## 关键发现

### 0. 可以把“显式代理流量”打到 Mac 侧代理端口

当前 DevEco Emulator guest 网络是 QEMU NAT：

```text
guest eth0 = 10.0.2.15/24
default gw = 10.0.2.2
```

实测 guest 能访问 `10.0.2.2`：

```text
hdc shell ping -c 2 -W 1 10.0.2.2
2 packets transmitted, 2 received, 0% packet loss
```

Mac 侧 Shadowrocket 当前只监听本机回环代理端口：

```text
scutil --proxy:
HTTPProxy=127.0.0.1 HTTPPort=1082
HTTPSProxy=127.0.0.1 HTTPSPort=1082

lsof -nP -iTCP:1082 -sTCP:LISTEN:
MacPacketTunnel ... TCP 127.0.0.1:1082 (LISTEN)
MacPacketTunnel ... TCP [::1]:1082 (LISTEN)
```

即便代理只监听 `127.0.0.1:1082`，guest 访问 `10.0.2.2:1082` 仍能打到该代理端口。由于当前镜像没有 `curl/nc/telnet`，用 `ftpget` 做 TCP 可达性探针：

```text
hdc shell 'timeout 15 ftpget -v -p 1082 10.0.2.2 /data/local/tmp/proxy-test.bin /'

guest netstat:
10.0.2.15:<ephemeral> -> 10.0.2.2:1082 TIME_WAIT

ftpget:
must 220 ... rc 0 ...
```

`ftpget` 期望 FTP 服务端先返回 `220` banner，但 HTTP 代理不会按 FTP 协议响应，所以最后报协议错误。这反而证明 TCP 连接没有被拒绝，确实到达了 Mac 侧 `1082` 代理入口。

因此，若应用或系统网络栈显式使用 HTTP 代理，代理地址应写成 guest 可达的 `10.0.2.2:1082`，不是 `127.0.0.1:1082`。`127.0.0.1` 在 guest 内代表模拟器自己。

### 1. `hdc fport/rport` 不是全流量转发

`hdc help` 显示：

```text
fport localnode remotenode - Forward local traffic to remote device
rport remotenode localnode - Reserve remote traffic to local host
```

仓库既有研究也确认 `fport/rport` 支持 TCP、Unix socket、`jdwp`、`ark:pid@tid@Debugger` 等节点。它适合调试端口映射，不会把 guest 里已经直连外部 IP 的 HTTP/TLS 请求自动改道到宿主抓包工具。

### 2. `Emulator -http_proxy` 是管理器/下载代理线索

`/Applications/DevEco-Studio.app/Contents/tools/emulator/Emulator -help` 暴露：

```text
-imageList ... [-http_proxy <url>]
-install ... [-http_proxy <url>]
-screenProfileList ... [-http_proxy <url>]
-config ... [-http_proxy <url>]
-http_proxy: Network proxy configuration
```

二进制字符串中同时出现：

```text
InputParametersParser::ApplyNetworkProxyEnvironment()
Please check your network or use -http_proxy to configure a proxy.
Emulator http_proxy updated successfully.
```

这说明 `-http_proxy` 至少用于宿主侧 Emulator 管理器访问镜像列表、下载镜像、更新屏幕 profile 等网络请求。当前没有证据显示它会在已启动 guest 内设置业务网络代理，也没有出现在当前 `Emulator -hvd ...` 进程参数里。

### 3. Emulator UI 有私有 Network Proxy 面板

`strings` 在 Emulator 二进制和翻译文件中发现：

```text
networkProxyPanel
WidgetNetworkProxy
WidgetNetworkProxy::SetNetworkProxyAndSendRequest()
SendProxySettingsToAgent()
ApplyProxySettings()
ApplyDnsSettings()
use.ide.proxy
manual.proxy.configuration
no.proxy
proxy.authentication
ide.proxy.method.socks
proxy-settings.ini
```

这说明 DevEco Emulator UI 确实有“把 IDE 代理或手动代理配置发给 guest agent”的能力线索。当前本机两个 HVD 的 `huawei-settings.cfg` 没有代理段，未见 `proxy-settings.ini` 落盘，说明本机尚未通过 UI 应用过该代理。

这条路径应继续按私有 UI/agent 能力看待：它可能设置系统 HTTP 代理或 DNS，但尚未证明能透明接管所有 TCP/TLS 流量，也没有稳定公开 CLI。

### 4. 当前 guest 仍在直接联网

运行态证据：

```text
hdc shell netstat -rn:
0.0.0.0 -> 10.0.2.2 dev eth0

hdc shell netstat -ant:
10.0.2.15:<ephemeral> -> 198.18.0.x:443
10.0.2.15:<ephemeral> -> 49.4.36.124:5223

lsof -p <Emulator pid> -i:
Emulator 198.18.0.1:<ephemeral> -> 198.18.0.x:443
Emulator 198.18.0.1:<ephemeral> -> 49.4.36.124:5223
```

`param get` 没有可见的 `proxy` 默认配置，只看到 `NetManager.Vpn` 等系统能力。启动日志里有 `persist.edc.proxy_ap_startup` watcher 和 `clouddevelopproxy` 服务，但当前 `param get persist.edc.proxy_ap_startup` 返回不存在；这更像内部服务观察点，不是可直接依赖的公开开关。

### 5. 证书能力存在，但不是“自动抓包”的全部条件

SDK 里存在证书管理能力：

```text
@ohos.security.certManagerDialog:
openCertificateManagerDialog(...)
openInstallCertificateDialog(context, CA_CERT, CURRENT_USER/GLOBAL_USER, cert)

@ohos.security.certManager:
installUserTrustedCertificateSync(cert, CURRENT_USER/GLOBAL_USER)
getAllUserTrustedCertificates(scope)
getCertificateStorePath({ certType: CA_CERT_USER, certScope })
```

这说明 HarmonyOS 有“安装用户信任 CA”的平台能力；但同步安装接口需要 `ohos.permission.ACCESS_ENTERPRISE_USER_TRUSTED_CERT` 或 `ohos.permission.ACCESS_USER_TRUSTED_CERT`，证书管理弹窗也需要 `ohos.permission.ACCESS_CERT_MANAGER`。普通调试应用不应默认能静默安装全局 CA。

NetworkKit 也提供应用内证书入口：

```text
HttpRequestOptions.caPath
HttpRequestOptions.caData
```

`caPath/caData` 会在单次 HTTP 请求里把调试 CA 与系统预置 CA 一起用于校验，适合测试包或调试构建；它不等于给整个系统安装 CA。RCP 也有 `security.certificate` 配置，可在会话级别指定证书材料。

因此，“装证书后能解 HTTPS”必须和“流量是否走代理”分开判断：

- 若应用没有走 `10.0.2.2:<proxy-port>` 这样的显式代理，装 CA 也不会让直连流量自动进入抓包工具。
- 若应用走了显式代理，但 TLS 栈不信任抓包 CA，会看到连接失败或证书错误。
- 若应用启用了 certificate pinning，即使用户 CA 已安装，也仍可能无法解密，需要调试构建关闭或替换 pin。
- WebView、NetworkKit HTTP、RCP、Socket/TLSSocket 可能使用不同代理和证书配置入口，不能按一个开关覆盖全部。

## 结论

- 能转发端口：用 `hdc fport/rport`。
- 能把模拟器内“显式代理流量”转到 Mac 侧代理：使用 guest 可达的 `10.0.2.2:<proxy-port>`。本机 Shadowrocket `127.0.0.1:1082` 通过 `10.0.2.2:1082` 可达。
- 能让目标应用流量进代理：应用内显式使用 `setAppHttpProxy`、`usingProxy: true`，或 WebView/WebSocket/RCP 各自的代理配置。NetworkKit 文档明确说明 `setAppHttpProxy` 只配置代理规则，HTTP 请求还需要 `HttpRequestOptions.usingProxy=true` 才启用代理转发。
- 能让调试 HTTP 请求信任抓包 CA：应用内使用 `caPath` / `caData`，或走证书管理能力安装用户 CA；但权限、设备安全策略、网络栈差异和 pinning 都会影响结果。
- Emulator 自带 UI 可能能设置 guest 代理：已有静态证据，但属于私有 agent 通道，需 UI 前后对比验证，不应写成稳定 CLI。
- 不能仅靠 Mac 脚本透明转发全部模拟器流量：HTTP 代理端口需要 HTTP 请求或 `CONNECT`，原始 TLS 直连不会自动变成代理协议。
- 暂无证据支持“像 iOS 模拟器一样，只安装一次 CA 就自动抓到所有模拟器 HTTPS 流量”。当前更可靠的路径是：显式代理到 `10.0.2.2:<proxy-port>`，再按目标网络栈配 CA。
- 真正全流量路径应是设备侧 VPN/TUN：使用 `VpnExtension` 创建虚拟网卡、配置 routes/DNS/trustedApplications/blockedApplications，然后在设备侧转发包。

## 后续实验建议

1. 先从 DevEco Studio Device Manager 恢复 HVD，直到 `hdc list targets -v` 显示 `Connected`。
2. 打开 Emulator UI 的 Network Proxy 面板，分别应用 No Proxy、Use IDE Proxy、Manual HTTP Proxy。
3. 每次应用后采集 `huawei-settings.cfg`、`proxy-settings.ini`、`param get`、`netstat -ant`、`lsof -p <Emulator pid> -i` 差异，并在测试 App 内调用 `connection.getDefaultHttpProxy()`。
4. 用一个本地 HTTP proxy 监听 `10.0.2.2:<port>`，在 guest 内用系统浏览器、NetworkKit 测试包、WebView 测试包分别发请求。
5. 对证书路径单独做测试：证书管理 UI 安装用户 CA、NetworkKit `caData`、RCP `security.certificate` 三条路径分别验证。
6. 若 UI 代理只影响系统/应用 HTTP 栈，继续保持应用级代理建议；若能影响系统默认代理，把它标为 DevEco UI 私有方案，不包装成通用 CLI。
7. 若要全流量抓包，做最小 `VpnExtension` proof of concept，而不是扩展 Mac 侧端口转发脚本。

## 待补实测矩阵

### A. Emulator UI Network Proxy

目标：确认 Emulator UI 里的 Network Proxy 面板到底能否设置 guest 的系统 HTTP 代理。

步骤：

1. Mac 侧启动一个明确监听的 HTTP 代理或临时探针端口，记录监听地址和端口。
2. 在 Emulator UI 中设置 Manual Proxy 到 `10.0.2.2:<proxy-port>`。
3. 在 guest 内采集：
   - `param get | grep -i proxy`
   - `netstat -ant`
   - 测试 App 调用 `connection.getDefaultHttpProxy()`
4. 在宿主侧采集：
   - `lsof -Pan -p <emulator-pid> -i`
   - `huawei-settings.cfg`
   - 是否生成 `proxy-settings.ini`
5. 分别验证 No Proxy、Use IDE Proxy、Manual HTTP Proxy 三种状态。

判定标准：

- 若 `getDefaultHttpProxy()` 返回 UI 配置，且系统浏览器或默认 HTTP 请求开始连接 `10.0.2.2:<proxy-port>`，可标记为“Emulator UI 私有系统 HTTP 代理”。
- 若只有 Emulator 管理器请求走代理，guest App 不走代理，则继续归类为“管理器/agent 配置，不可作为业务抓包入口”。
- 即使 UI 代理生效，也不能自动推出“透明接管全部 TCP/TLS 流量”。

### B. 证书安装与 TLS 信任

目标：确认 HarmonyOS Emulator 是否能像 iOS 一样把抓包 CA 加入用户信任，并确认哪些网络栈实际信任它。

步骤：

1. 导出抓包工具 CA，准备 `.cer`、`.pem` 两种格式。
2. 通过系统证书管理 UI 尝试安装用户 CA。
3. 通过测试 App 调用 `certificateManagerDialog.openInstallCertificateDialog(...)` 尝试安装。
4. 通过测试 App 调用 `NetworkKit`：
   - `usingProxy: true`
   - `usingProxy: { host: '10.0.2.2', port: <proxy-port> }`
   - `caPath`
   - `caData`
5. 用 WebView、RCP、Socket/TLSSocket 分别验证 HTTPS 抓包结果。

判定标准：

- 若系统 UI 安装 CA 后，默认 NetworkKit/WebView/RCP 都能通过代理 MITM HTTPS，才接近 iOS 式体验。
- 若只有 `caPath` / `caData` 生效，则结论应保持为“调试 App 内配置 CA”，不是系统全局证书方案。
- 若遇到 certificate pinning，需在调试构建关闭 pin；这不能算代理或 CA 方案失败。

### C. 最小测试 App

目标：用一个可重复运行的 Harmony 测试 App 做最终裁判。

页面只需要几个按钮：

1. 默认 `http.request('https://example.com')`。
2. `connection.setAppHttpProxy({ host: '10.0.2.2', port })` 后 `usingProxy: true`。
3. `usingProxy` 直接传 `HttpProxy`。
4. `usingProxy + caPath`。
5. `usingProxy + caData`。
6. `connection.getDefaultHttpProxy()` 并显示结果。
7. WebView 打开一个 HTTPS 页面。
8. RCP session 使用 `proxy: 'system'`、自定义 `WebProxy`、`security.certificate`。

每个按钮输出：

- 是否请求成功。
- HTTP 状态码。
- 错误码和错误信息。
- 当前请求是否被 Mac 侧抓包工具捕获。

### D. 私有协议与隐藏 CLI 继续反查

目标：判断 Emulator UI 的代理设置能否被自动化复现。

研究方向：

1. 继续反查 `WidgetNetworkProxy::SendProxySettingsToAgent()`，找它给 guest agent 发送的字段、socket、端口或 RPC 名称。
2. 在 Emulator/镜像字符串里搜索 `ApplyProxySettings`、`ApplyDnsSettings`、`clouddevelopproxy`、`persist.edc.proxy_ap_startup` 的接收端。
3. 对比应用 UI 设置代理前后的文件和参数变化：
   - `huawei-settings.cfg`
   - `proxy-settings.ini`
   - guest `param get`
   - guest 网络服务日志
4. 查找是否存在隐藏 CLI 或本地 IPC，可以设置 guest 默认代理；不要把 `Emulator -http_proxy` 当成业务流量代理，除非运行态证明确实影响 guest。

当前优先级：先做 A 和 C，因为它们直接回答“能不能转发到 Mac 侧代理”；再做 B，因为它回答“能不能解 HTTPS”；最后做 D，把 UI 操作变成可脚本化能力。
