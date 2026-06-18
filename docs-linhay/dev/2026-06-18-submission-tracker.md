# 2026-06-18 投稿追踪

本文件记录 `linhay/harmony-next.skills` 对外自荐、awesome 列表 PR 和周报投稿状态，便于后续追踪。

状态更新时间：2026-06-18 23:18 Asia/Shanghai。

## 已收录 / 已处理

| 渠道 | 类型 | 链接 | 当前状态 | 备注 |
| --- | --- | --- | --- | --- |
| SwiftOldDriver/iOS-Weekly | issue | https://github.com/SwiftOldDriver/iOS-Weekly/issues/5356 | CLOSED | 用户确认已收录到下一期；GitHub issue 无评论，2026-06-11 关闭。 |
| milisp/awesome-codex-cli | PR | https://github.com/milisp/awesome-codex-cli/pull/50 | MERGED | 2026-06-18 21:44 Asia/Shanghai 合并；已进入 awesome-codex-cli。 |

## 待处理：中文推荐 / 周刊 issue

| 渠道 | 类型 | 链接 | 当前状态 | 评论 | 备注 |
| --- | --- | --- | --- | --- | --- |
| HelloGitHub | issue | https://github.com/521xueweihan/HelloGitHub/issues/3289 | OPEN | 0 | 2026-05-22 提交，标题：`[开源推荐] HarmonyOS NEXT 开发者 AI 技能包`。 |
| GitHubDaily | issue | https://github.com/GitHubDaily/GitHubDaily/issues/885 | OPEN | 0 | 2026-06-18 提交，标题：`【开源自荐】harmony-next.skills：给 AI 编程助手用的 HarmonyOS NEXT 开发者技能包`。 |
| ruanyf/weekly | issue | https://github.com/ruanyf/weekly/issues/10377 | OPEN | 0 | 2026-06-18 提交，标题同 GitHubDaily。 |
| OpenGithubs/weekly | issue | https://github.com/OpenGithubs/weekly/issues/116 | OPEN | 1 | 2026-06-18 提交，维护者回复“你的邮箱已收到，谢谢！”。 |
| OpenGithubs/monthly | issue | https://github.com/OpenGithubs/monthly/issues/24 | OPEN | 0 | 2026-06-18 提交，按开源项目精选月刊文案推荐。 |

## 待处理：移动开发 / Android AI 渠道

| 渠道 | 类型 | 链接 | 当前状态 | Merge 状态 | Review | 评论 | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Gracker/awesome-android-ai-dev-sources | PR | https://github.com/Gracker/awesome-android-ai-dev-sources/pull/39 | OPEN | CLEAN | - | 0 | 添加到开发工具分类；已更新 `data/entries.json` 与 README。 |
| Android Weekly | form | https://androidweekly.net/ | SUBMITTED | - | - | - | 2026-06-18 通过官网 Submit 表单提交项目链接；该渠道无公开追踪链接。 |

## 待处理：Codex / Claude / DevTools awesome PR

| 渠道 | 类型 | 链接 | 当前状态 | Merge 状态 | Review | 评论 | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ComposioHQ/awesome-codex-skills | PR | https://github.com/ComposioHQ/awesome-codex-skills/pull/117 | OPEN | CLEAN | - | 0 | 添加到 Development & Code Tools。 |
| RoggeOhta/awesome-codex-cli | PR | https://github.com/RoggeOhta/awesome-codex-cli/pull/101 | OPEN | CLEAN | - | 0 | 添加到 Domain-Specific Skills。 |
| LangGPT/awesome-claude-code | PR | https://github.com/LangGPT/awesome-claude-code/pull/100 | OPEN | CLEAN | - | 0 | 中英文 README 均添加到 Framework Extensions。 |
| harmonyos-dev/awesome-harmonyos-next | PR | https://github.com/harmonyos-dev/awesome-harmonyos-next/pull/2 | OPEN | CLEAN | - | 0 | 新增“AI 开发辅助”分类。 |
| helloianneo/awesome-claude-code-skills | PR | https://github.com/helloianneo/awesome-claude-code-skills/pull/42 | OPEN | CLEAN | - | 0 | 新增“移动端 / 客户端开发”分类，推荐等级“好用”。 |
| devtoolsd/awesome-devtools | PR | https://github.com/devtoolsd/awesome-devtools/pull/272 | OPEN | CLEAN | - | 0 | 添加到 AI Coding Tools。 |

## 未自动提交

| 渠道 | 原因 | 后续动作 |
| --- | --- | --- |
| hesreallyhim/awesome-claude-code | 投稿模板明确禁止使用 `gh` CLI 或程序化方式提交资源，要求人工通过 GitHub Web UI 填表。 | 如需投递，手动填写 `Recommend New Resource` 表单；分类建议选 `Agent Skills` 或 `Workflows & Knowledge Guides`。 |
| hashgraph-online/awesome-codex-plugins | 目标仓库偏 Codex plugin。本仓库当前还不是 Codex plugin。 | 等完成 `.codex-plugin/plugin.json` 和 plugin 包装后再投。 |
| Kotlin Weekly / KMP Weekly | 只维护 Kotlin/KMP 垂直技术主题，本项目不是 Kotlin/KMP 资源。 | 本轮跳过。 |
| JStumpp/awesome-android / wasabeef/awesome-android-libraries / binaryshrey/Awesome-Android-Open-Source-Projects | 主要收 Android library、Android app 或纯 Android 项目，本项目是 HarmonyOS NEXT + AI Agent 工具包。 | 本轮跳过，避免低匹配投稿。 |
| android-arsenal.com | 当前访问异常，GitHub 源码仓库多年未活跃。 | 暂不投递。 |

## 后续追踪建议

1. 每 3-5 天用 `gh issue view` / `gh pr view` 批量检查一次状态。
2. PR 若 7 天无反馈，优先只跟进高匹配渠道：ComposioHQ、RoggeOhta、milisp、helloianneo。
3. 不建议继续批量投低匹配周刊；后续新增渠道优先选择 Codex / Claude skills、AI developer tools、HarmonyOS/OpenHarmony 资源索引。
4. 若任一 PR 要求调整文案，保持定位为“HarmonyOS NEXT developer skill / workflow toolkit for AI coding agents”，避免写成普通文档镜像。
