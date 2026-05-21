# DevEco 模拟器抓包与代理诊断沉淀

## 背景

使用者在 DevEco HarmonyOS Emulator 中调试网络请求时，可能会发现 Charles、mitmproxy、Proxyman 或其他抓包工具看不到模拟器流量。此次沉淀的目标不是记录某台机器的排查流水账，也不绑定某个抓包软件，而是把可复用的判断路径写入 `harmony-next` skill，供后续 Agent 面向外部使用者回答同类问题。

## 验收场景

1. 当使用者询问“模拟器为什么抓不到包”时，Agent 能先说明模拟器 NAT、宿主机可达地址和应用是否走代理这三个检查点。
2. 当使用者提出“起一个 Mac 中转脚本是否能透明转发所有流量”时，Agent 能明确区分显式 HTTP 代理和原始 TCP/TLS 流量，避免把端口转发描述成通用透明抓包方案。
3. 当使用者需要可落地方案时，Agent 优先建议调试目标应用使用 `setAppHttpProxy` 和 `usingProxy: true`，并提醒 HTTPS CA 与 certificate pinning 边界。
4. 当使用者追问系统级或全局方案时，Agent 能指出企业全局代理、PAC 和 `VpnExtension` 的权限、实现成本与适用边界。

## 实现范围

- `harmony-next/SKILL.md`：在 DevEco Emulator Automation 路由中加入 simulator traffic capture、HTTP proxy tools、NetworkKit proxy routing、transparent interception 触发词和处理边界。
- `harmony-next/references/ideGuides/DevEco模拟器私有接口与AI自动化.md`：新增“模拟器抓包与代理诊断”章节，使用面向外部使用者的措辞描述 NAT、显式 HTTP 代理、应用级代理、Mac 侧中转、透明接管和 VPN/TUN 边界。
- `README.md` / `README_en.md`：在 DevEco 模拟器私有接口说明中补充抓包与代理诊断入口。
- `harmony-next/tests/test_skill_metadata.py`：新增元数据测试，固定关键短语和外部使用者视角，防止后续把该能力写成内部排查记录。

## 边界结论

- Mac 系统代理不会天然变成模拟器内系统代理；模拟器访问 `127.0.0.1` 指向模拟器自身。
- 常见可达入口是宿主机网关地址，例如 `10.0.2.2:9090`，但应用必须显式使用代理。
- Mac 侧中转脚本只能服务主动连接中转端口的流量，不能透明接管全部模拟器连接。
- 显式 HTTP 代理端口期望 HTTP 请求或 `CONNECT host:443`；原始 HTTPS 直连流量直接转发过去会出现协议不匹配。
- 透明接管全流量需要设备侧 VPN/TUN、系统/全局代理或 PAC 这类能力，权限和实现成本都高于应用级调试代理。

## 验证

- 先新增失败测试：`test_emulator_proxy_capture_guidance_is_external_user_facing`。
- 更新 skill 与 README 后运行：`python3 -m unittest harmony-next/tests/test_skill_metadata.py`，10 项通过。
