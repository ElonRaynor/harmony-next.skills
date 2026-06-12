# HarmonyOS NEXT Reference Skill

An offline HarmonyOS NEXT reference skill for coding agents such as Gemini CLI, Claude Code, and Codex.

Language: English | [中文](./README.md)

[![release](https://img.shields.io/badge/release-v1.3.23-1f6feb?style=flat-square)](https://github.com/linhay/harmony-next.skills/releases/tag/v1.3.23)
[![readme](https://img.shields.io/badge/readme-%E4%B8%AD%E6%96%87-0f766e?style=flat-square)](./README.md)
![docs](https://img.shields.io/badge/docs-3,693%20markdown%20files-7c3aed?style=flat-square)
![js-ets](https://img.shields.io/badge/JsEtsAPIReference-3,666%20files-b45309?style=flat-square)

> A local knowledge source for API 12-23, covering ArkTS, ArkUI, NDK, toolchains, debugging, release workflows, and multi-device adaptation.

## What Problem It Solves

`harmony-next.skills` is not just a document mirror. It is a HarmonyOS NEXT retrieval layer designed for coding agents.

It is meant to answer questions like:

- Which file contains a specific `@ohos.*` module
- Whether an ArkUI component, interface, or NDK header actually exists
- Whether API 23 additions are already included in the current knowledge base
- Whether a legacy internal link has been migrated and still resolves correctly
- How to safely verify local DevEco Studio emulator automation with `hdc`, `uitest`, and related tooling
- How to isolate and verify private DevEco Studio IDE capabilities such as CodeGenie, MCP, Inspector, and Profiler before using them

The goal is to turn those questions into local file lookups that are traceable, linkable, and verifiable.

## Core Features

| Capability | Description |
| --- | --- |
| Offline retrieval | Resolve document paths first, then read the source instead of guessing from model memory |
| Agent-oriented workflow | Organized as `SKILL.md -> KITS/TASK_MAP -> INDEX`, which fits progressive retrieval |
| More than API docs | Includes IDE setup, signing, debugging, release, performance, multi-device, and NDK guidance |
| Private-interface isolation | DevEco emulator and IDE private capabilities each live in separate chapters with version checks and risk gates |
| Non-interactive automation policy | DevEco emulator automation supports `HARMONY_NEXT_AUTOMATION_POLICY`; policy is an execution mode, not an authorization gate |
| Offline UI/UX audit | Uses real emulator screenshots + `uitest dumpLayout` with DevEco `UxTestService` to produce JSON, issue coordinates, and marked images |
| Copyable minimal project | Provides `references/templates/empty-ability-app` for HDC / `uitest dumpLayout` / screenshot smoke tests |

## Repository Overview

| Module | Description | Entry |
| --- | --- | --- |
| Skill rules | Tells the agent how to search, answer, and what to trust | [`harmony-next/SKILL.md`](./harmony-next/SKILL.md) |
| Kit navigation | Narrow scope by AbilityKit, ArkUI, ArkData, MediaKit, Security, and more | [`references/KITS.md`](./harmony-next/references/KITS.md) |
| Task navigation | Map UI, lifecycle, network, media, NDK, release, and other tasks to keywords | [`references/TASK_MAP.md`](./harmony-next/references/TASK_MAP.md) |
| Global index | Full Markdown path index for the reference corpus | [`references/INDEX.md`](./harmony-next/references/INDEX.md) |
| Bucketed API index | Focused index for `JsEtsAPIReference/`, covering modules, topics, types, errors, and guides | [`JsEtsAPIReference/INDEX.md`](./harmony-next/references/JsEtsAPIReference/INDEX.md) |
| Empty Ability minimal project | Copyable HarmonyOS NEXT smoke fixture with defaults `com.example.emptyability` / `EntryAbility` / `5.0.0(12)` | [`references/templates/empty-ability-app`](./harmony-next/references/templates/empty-ability-app/) |
| Minimal project scaffold guide | Explains copy, the decoupled route page and `SmokeCounter` component, `ohpm install`, `hvigorw --mode module`, SDK override validation, HDC launch, `uitest dumpLayout`, and click smoke validation | [`minimal-project-scaffold.md`](./harmony-next/references/quickStart/ets/minimal-project-scaffold.md) |
| DevEco emulator private interfaces | Local validation boundaries for starting Emulator without the IDE, `hdc + uitest`, HVD, logs, and diagnostics | [`DevEco模拟器私有接口与AI自动化.md`](./harmony-next/references/ideGuides/DevEco模拟器私有接口与AI自动化.md) |
| DevEco IDE private interfaces | Validation boundaries for CodeGenie, local RAG/MCP, `devecostudio://`, Previewer, ArkUI Inspector, Profiler, Doctor, UxTestService, and offline UI/UX audits | [`DevEco Studio IDE私有接口与AI自动化.md`](./harmony-next/references/ideGuides/DevEco%20Studio%20IDE私有接口与AI自动化.md) |
| Command Line Tools setup | Direct archive download, local archive install, PATH profile setup, and `codelinter -v` validation | [`commandline_tools_manager.py`](./harmony-next/scripts/commandline_tools_manager.py) |
| Device debug evidence bundle | Uses `hdc` to collect bounded boot state, `bm/aa` summaries, short logs, layout, screenshot, and a command ledger | [`device_evidence_bundle.py`](./harmony-next/scripts/device_evidence_bundle.py) |
| One-shot offline UI/UX audit | Chains `hdc` evidence capture with DevEco `UxTestService`, producing `summary.json`, `report.md`, rule results, and marked images | [`ux_audit_pipeline.py`](./harmony-next/scripts/ux_audit_pipeline.py) |
| Offline trace performance evidence audit | Runs DevEco `trace_streamer` to convert `.ftrace/.htrace` traces to SQLite and export long-span, threshold-hit, and metadata JSON | [`profiler_trace_audit.py`](./harmony-next/scripts/profiler_trace_audit.py) |
| Reference corpus | `3,693` Markdown files total, with `3,666` under `JsEtsAPIReference/` | [`harmony-next/references/`](./harmony-next/references/) |

## Recommended Retrieval Path

```text
SKILL.md
  -> KITS.md / TASK_MAP.md
  -> INDEX.md
  -> target Markdown file
```

Why this layout works:

1. Start with rules so the agent does not blind-read the entire corpus.
2. Narrow the scope by kit or task to reduce false hits.
3. Resolve real file paths from indexes instead of relying on name guesses.
4. Open only 1-3 target files for API-level detail.

The core principle is simple: find the path first, then read the content.

## Typical Use Cases

### ArkTS / ArkUI Development

- Components, decorators, state management, navigation, UIAbility, and Want
- API version differences, parameter signatures, and return values
- Restoring working links inside component documentation

### NDK / Node-API / C API

- Mapping headers to real `topics/**/<header>.h.md` pages
- ArkTS/C++ interoperability, CMake, and native capability access
- Index and link validation after legacy path migration

### IDE / Toolchain / Debugging

- Signing, emulators, real devices, and breakpoints
- Standalone CLI setup and CI/CD integration
- Command Line Tools can be installed with `python3 harmony-next/scripts/commandline_tools_manager.py install --archive <zip> --dest ~/.harmony/command-line-tools --profile auto`; for download, pass a direct archive URL copied from Huawei's download center to `bootstrap --url <archive-url>`, preferably with `--sha256`
- Performance analysis and release workflows
- Device debug evidence bundle: run `python3 harmony-next/scripts/device_evidence_bundle.py capture --deveco-app <DevEco-Studio.app> --target <target> --artifact-dir .hvigor/outputs/<run> --json` to collect real layout, screenshot, short `hilog`, `bm/aa` summaries, and a command ledger for UI/UX audits, log triage, or reproduction reports
- One-shot offline UI/UX audit: first run `python3 harmony-next/scripts/ux_audit_pipeline.py doctor --deveco-app <DevEco-Studio.app> --python <python-with-ux-deps> --json` to check `hdc`, `UxTestService`, and Python image dependencies, then run `python3 harmony-next/scripts/ux_audit_pipeline.py capture-audit --deveco-app <DevEco-Studio.app> --python <python-with-ux-deps> --target <target> --artifact-dir .hvigor/outputs/<run> --json` to generate the report
- Offline trace performance evidence audit: when an existing `.ftrace/.htrace` / bytrace / rawtrace file is available, run `python3 harmony-next/scripts/profiler_trace_audit.py audit --deveco-app <DevEco-Studio.app> --input <trace> --output-dir .hvigor/outputs/<run> --json` to generate SQLite, `summary.json`, top callstack, and `16.67ms / 33.34ms` threshold-hit reports
- DevEco Studio / HarmonyOS Emulator automation: launching without the IDE, HVD, multi-instance runs, `hdc`, `uitest`, `aa`, `bm`, `hilog`, and `hidumper`
- Offline UI/UX audit: capture a running page screenshot and layout with `hdc` / `uitest`, then run the available static-rule subset in DevEco `UxTestService` to generate JSON reports and marked images; verified rules include hotspot size, icon size, icon clarity, status bar, navigation bar, occlusion, blur, hole adaptation, and page margin
- Copy `references/templates/empty-ability-app` to generate a minimal Empty Ability fixture; the page exposes `smoke-increment` for `uitest dumpLayout`, screenshots, and log smoke checks
- The route page and smoke component are decoupled: `pages/Index.ets` only mounts `SmokeCounter()`, while `components/SmokeCounter.ets` owns the smoke UI and state
- Supports SDK override validation: for example, HarmonyOS 6.0.2 / API 22 builds with `6.0.2(22)`, `DEVECO_SDK_HOME=/Applications/DevEco-Studio.app/Contents/sdk`, and the app `icon`, Ability `icon`, and `startWindowIcon`
- Interactive smoke uses `uitest uiInput click` on `smoke-increment`, then re-dumps layout and verifies `Harmony Smoke Tapped` / `tapCount=1`

### DevEco Emulator Private Interfaces

This section covers private, undocumented interfaces. Trigger terms include: `DevEco Studio`, `HarmonyOS Emulator`, `Emulator -list -details`, `launch without IDE`, `HVD`, `hdc`, `uitest`, `uiInput`, `aa`, `bm`, `hilog`, `hidumper`, `snapshot_display`, `uinput`, `hitrace`, `multi-instance`, and `trace pipe`.

Usage rules:

- Read the private-interface chapter in [`harmony-next/SKILL.md`](./harmony-next/SKILL.md) first, then open [`DevEco模拟器私有接口与AI自动化.md`](./harmony-next/references/ideGuides/DevEco模拟器私有接口与AI自动化.md).
- Re-verify the current DevEco / Emulator / SDK version and command capabilities before each run.
- Users are assumed to have full execution authority; long-running automation can use `HARMONY_NEXT_AUTOMATION_POLICY`, `--policy`, or `.harmony-next-policy.json` to describe execution mode, artifact directories, and redaction contracts.
- Real screenshots, layouts, log bundles, installs/uninstalls, port forwarding, and HVD create/delete flows run non-interactively; missing target, artifact directory, redaction policy, or timeout returns a machine-readable blocked result.
- `device_evidence_bundle.py` is a verified evidence-capture entrypoint: it does not start DevEco Studio and does not install, uninstall, start, or stop apps; artifacts may contain real UI, bundle, ability, and log content, so review or redact them before sharing.
- `ux_audit_pipeline.py` is a verified one-shot audit entrypoint: run `doctor` to check Python dependencies first, and during execution it copies `tools/UxTestService` into an artifact-local runtime to avoid writing `uxlog` inside the DevEco `.app`.
- If these wrappers return `blocked`, agents should try the official CLI evidence path first: `hdc list targets -v`, `uitest dumpLayout`, `screenCap`, `file recv`, `bm dump`, `aa dump`, and bounded `hilog`, then re-run the offline audit with the captured layout/screenshot.
- If a wrapper is blocked, output is misleading, a DevEco/device version is unsupported, or a workflow is missing, agents should ask users to choose the matching scenario template from the script's `feedback` field and [`ISSUE_GUIDE.md`](./harmony-next/ISSUE_GUIDE.md), redact sensitive data, then report it to GitHub Issues.
- This repo provides `python3 harmony-next/scripts/hvd_manager.py`: `doctor` environment probing, `list`, `create`, `delete`, `launch-preflight`, and `launch` are supported.
- HVD launch adaptation: use `--root` / `HARMONY_HVD_ROOT` for the HVD root, `--emulator` / `HARMONY_EMULATOR` for Emulator, `--image-root` / `HARMONY_EMULATOR_IMAGE_ROOT` for the emulator image root, and `--hdc` / `HARMONY_HDC` for HDC. `--sdk-root` / `DEVECO_SDK_HOME` means the DevEco build SDK root, not necessarily the emulator image root.
- On macOS the emulator image root is commonly `~/Library/Huawei/Sdk`; the script validates it against the HVD `imageSubPath`. The current `launch` command detaches Emulator and the trace holder, then waits for HDC, boot, and stability checks. A first-run Huawei Emulator license/agreement prompt returns `result=license-agreement-required` / `missingConfig=["emulatorLicenseAgreement"]`; the script only writes `y` to Emulator stdin when `--accept-license` is passed explicitly. The next lifecycle model should add an attached terminal-scoped mode that runs cleanup through `Emulator -stop` when the terminal session ends, while keeping detached mode for compatibility. `download-image` currently returns blocked because image downloads have only been verified through the IDE SDK Manager UI.
- For emulator traffic capture and proxy diagnostics, HTTP proxy capture tools such as Charles, mitmproxy, and Proxyman require checking the emulator NAT, a host address reachable from the emulator, and app-level proxy settings. The usual debugging path is to make the target app explicitly use `10.0.2.2:9090`, for example `setAppHttpProxy` plus `usingProxy: true`; a macOS forwarding script should not be documented as a general transparent interception solution.

### DevEco Studio IDE Private Interfaces

This section covers private, undocumented interfaces. Trigger terms include: `DevEco Studio IDE`, `CodeGenie`, `MCP`, `LanceDB`, `devecostudio://`, `inspect.sh`, `format.sh`, `ltedit.sh`, `ArkUI Inspector`, `Previewer`, `Profiler`, `Doctor`, `Diagnostic`, `FaultLog`, `UxTestService`, `Application Agent`, `Operation Analyzer`, and `Cloud Toolkit`.

Usage rules:

- Read the IDE private-interface chapter in [`harmony-next/SKILL.md`](./harmony-next/SKILL.md) first, then open [`DevEco Studio IDE私有接口与AI自动化.md`](./harmony-next/references/ideGuides/DevEco%20Studio%20IDE私有接口与AI自动化.md).
- Default to static read-only analysis: plugin XML, jar class names, strings, config paths, and offline `.htrace` / faultlog / stacktrace / `.arkli` / `.preview` artifacts.
- Starting the IDE/GUI/JCEF, local services, device connections, CodeGenie localhost endpoints, MCP config, external model calls, or reading user caches/chat history requires target, input, artifact-directory, and redaction-boundary records.
- `profiler_trace_audit.py` covers only the verified offline trace conversion and SQLite/JSON summary path; do not describe it as headless DevEco Profiler GUI import, and do not claim verified device capture.
- The `UxTestService` offline UI/UX audit is a verified implementable subset: prefer `ux_audit_pipeline.py capture-audit`; use the real foreground `bundle_name`, `extend_infos.language="zh"`, and an external artifact directory. Do not promise rules that are listed in config but missing from the current package, and do not describe text-heavy rules returning `UTS.0306` under plain `uitest dumpLayout` capture as full coverage.

### Agent Engineering Integration

- Gemini CLI, Claude Code, and Codex
- Local knowledge base retrieval layer
- Lower hallucination risk with higher traceability

## Quick Start

### Gemini CLI

```bash
gemini skills install https://github.com/linhay/harmony-next.skills --path harmony-next --scope user
```

### Claude Code

1. Download the skill directory from this repository.
2. Zip it if needed.
3. Upload it in Claude.ai via `Settings > Capabilities > Skills`.
4. Or place it in your Claude Code skills directory.

If you only want to attach it as project context:

```bash
git clone https://github.com/linhay/harmony-next.skills.git
claude --add-dir /path/to/harmony-next.skills/harmony-next
```

### Codex

The official Codex Agent Skills docs define skills as the authoring format for reusable workflows. Direct skill folders are for local authoring and discovery; plugins are the installable distribution unit.

Official docs: <https://developers.openai.com/codex/skills>

This repository is not currently packaged as a Codex plugin, so the official Codex setup path is to place it in an official skill scan location.

Official scan locations:

| Scope | Path |
| --- | --- |
| Repo | `$CWD/.agents/skills/harmony-next` |
| Repo | `$CWD/../.agents/skills/harmony-next` |
| Repo | `$REPO_ROOT/.agents/skills/harmony-next` |
| User | `$HOME/.agents/skills/harmony-next` |
| Admin | `/etc/codex/skills/harmony-next` |

Example: install into the current user's official skill directory:

```bash
git clone https://github.com/linhay/harmony-next.skills.git
mkdir -p "$HOME/.agents/skills"
ln -s "$(pwd)/harmony-next.skills/harmony-next" "$HOME/.agents/skills/harmony-next"
```

For team-level repo discovery, copy or symlink `harmony-next/` to the target repository's `$REPO_ROOT/.agents/skills/harmony-next`. Codex scans `.agents/skills` from the current working directory up to the repository root.

Entry files:

- [`harmony-next/SKILL.md`](https://github.com/linhay/harmony-next.skills/blob/master/harmony-next/SKILL.md)
- [`harmony-next/references/INDEX.md`](https://github.com/linhay/harmony-next.skills/blob/master/harmony-next/references/INDEX.md)

## Version Highlights

| Version | Highlights |
| --- | --- |
| `v1.3.7` | Added a copyable HarmonyOS NEXT Empty Ability minimal test project template: `references/templates/empty-ability-app`; defaults to `com.example.emptyability` / `EntryAbility` / `5.0.0(12)` and documents SDK override validation including `6.0.2(22)` / `DEVECO_SDK_HOME=/Applications/DevEco-Studio.app/Contents/sdk`, `ohpm install`, `hvigorw --mode module`, HDC launch, `uitest dumpLayout`, and `uitest uiInput click` smoke capabilities |
| `Unreleased` | Added `ux_audit_pipeline.py` for one-shot offline UI/UX audits: `doctor` checks `hdc`, `UxTestService`, and Python image dependencies, while `capture-audit` collects layout/screenshot/log evidence, infers the real foreground bundle, runs DevEco `UxTestService`, and writes `summary.json`, `ux_summary.json`, and `report.md`; a real emulator smoke produced a report with 7 pass, 1 issue, and 3 ignored results |
| `Unreleased` | Added `device_evidence_bundle.py` for device debug evidence bundles: it locates `hdc`, handles single/multiple targets, and collects boot state, debug bundles, `aa` runtime state, short `hilog`, `uitest dumpLayout`, screenshots, and a command ledger; a real emulator smoke collected layout/screenshot/log evidence and wrote `summary.json` |
| `Unreleased` | Added a local audit feedback mechanism: `device_evidence_bundle.py` and `ux_audit_pipeline.py` JSON outputs include a `feedback` field, `report.md` includes feedback guidance, and scenario-specific GitHub Issue forms now guide redacted reports for blocked runs, false positives, unsupported versions, and missing workflows |
| `Unreleased` | Added `profiler_trace_audit.py` for offline trace performance evidence audits: it locates DevEco `trace_streamer`, converts existing `.ftrace/.htrace` / bytrace / rawtrace artifacts to SQLite, and writes `summary.json`, top callstack, trace metadata, frame-slice summaries, and long-span threshold hits; the script refuses to write artifacts inside `.app` bundles |
| `Unreleased` | Added guarded DevEco Emulator CLI launch entries: `hvd_manager.py launch-preflight` only prints a command plan with `-t <trace-name>`, while `hvd_manager.py launch` creates the trace socket, detaches Emulator and the trace holder, then starts the runtime; launch now validates the emulator image root against the HVD `imageSubPath`, distinguishes the build SDK root from `~/Library/Huawei/Sdk`, and returns machine-readable diagnostics such as process exit code, log path, HDC snapshot, HVD runtime state, and stability checks on failures/timeouts; first-run license prompts are classified as `license-agreement-required` with an explicit `--accept-license` opt-in; docs now include an attached terminal-scoped lifecycle checklist for binding terminal exit to `Emulator -stop` cleanup |
| `Unreleased` | Release assets now use `harmony-next.skill.zip`; the package includes `BUILD_INFO.json` with version, release tag, and git commit metadata, plus `ISSUE_GUIDE.md` for agent-led reproduction, redaction, classification, and issue filing |
| `v1.3.6` | Added a non-interactive automation policy for the DevEco emulator playbook: users are assumed to have full authority and `policy` only means execution mode; supports `readonly/evidence/automation/diagnostic/break-glass`, artifact directories, redaction metadata, and machine-readable blocked output |
| `v1.3.5` | Added a private, undocumented DevEco Studio IDE capability reference covering CodeGenie local RAG/MCP/LanceDB, `devecostudio://`, Previewer, ArkUI Inspector, Profiler, Doctor, UxTestService, plugin entry indexes, and privacy risk gates; updated README and trigger terms |
| `v1.3.4` | Added a private, undocumented DevEco Studio emulator automation reference covering launch without the IDE, `hdc + uitest`, HVD, multi-instance runs, risk gates, timeouts, and redaction boundaries; updated `SKILL.md` trigger terms and task navigation |
| `v1.2.0` | API 23 content is included; `references/INDEX.md` and `JsEtsAPIReference/INDEX.md` were rebuilt; legacy `capi/headers/*.md` pages were removed and replaced with direct links to real targets; `reference_compat.py` and link-audit tooling were added; both Chinese and English README files were synchronized |

## Reference Maintenance

After syncing, migrating, or bulk-rewriting `references/JsEtsAPIReference/`, run the following in order:

```bash
python3 harmony-next/scripts/reference_compat.py generate
python3 harmony-next/scripts/reference_compat.py check
python3 harmony-next/scripts/reference_compat.py audit
python3 -m unittest discover -s harmony-next/tests -p 'test_*.py' -v
```

Command roles:

- `generate`
  - Rewrite legacy `../../capi/headers/*.md` links to real `topics/**/<header>.h.md` targets
  - Rebuild `references/INDEX.md` and `references/JsEtsAPIReference/INDEX.md`
- `check`
  - Verify legacy `capi/headers/` pages are gone
  - Verify indexes match the filesystem
  - Verify body content no longer points at old header paths
- `audit`
  - Scan current uncommitted changes
  - Detect internal Markdown links that used to exist but were flattened into plain text
- `unittest`
  - Verify the migration and audit tooling itself has not regressed

## Why It Is Worth Integrating

| Value | Description |
| --- | --- |
| Fewer hallucinations | Answers come from real document paths instead of memory completion |
| Better traceability | Every answer can point back to a concrete Markdown file |
| Better automation fit | Indexes, rules, and validation make it suitable for long-term agent workflows |

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=linhay/harmony-next.skills&type=Date)](https://www.star-history.com/#linhay/harmony-next.skills&Date)

## Acknowledgements

Thanks to [LINUX DO](https://linux.do/).

## Source and License

- Source: Huawei HarmonyOS official documentation
- This repository repackages those materials for AI-assisted development workflows

Chinese documentation is available in [README.md](./README.md).
