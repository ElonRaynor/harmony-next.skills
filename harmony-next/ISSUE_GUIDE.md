# Issue Guide

Use this guide when a HarmonyOS NEXT user reports a requirement, bug, missing capability, confusing behavior, documentation gap, or local DevEco/HVD automation problem that should become a GitHub issue for this repository.

Repository: `linhay/harmony-next.skills`

## Workflow

1. Clarify only the minimum missing detail needed to avoid filing a wrong issue.
2. Reproduce or inspect locally when possible. Prefer machine-readable checks from this skill:
   - `python3 harmony-next/scripts/hvd_manager.py doctor --json`
   - `python3 harmony-next/scripts/hvd_manager.py list --json`
   - `python3 harmony-next/scripts/hvd_manager.py launch-preflight ... --json`
   - `python3 harmony-next/scripts/hvd_manager.py launch ... --json`
   - `python3 harmony-next/scripts/commandline_tools_manager.py doctor --tools-root <dir> --json`
   - `python3 harmony-next/scripts/reference_compat.py check`
   - `python3 -m unittest discover -s harmony-next/tests`
3. Preserve structured fields in the issue instead of flattening them into prose:
   - `decision`
   - `operation`
   - `missingConfig`
   - `issues`
   - `recommendations`
   - `hvdRoot`
   - `emulator`
   - `sdkRoot`
   - `imageRoot`
   - `imageSubPath`
   - `hdc`
   - `hdcWait`
   - `bootWait`
   - `stabilityWait`
   - `processExitCode`
   - `logPath`
4. Redact private data before filing:
   - Replace local usernames, absolute private repo paths, app names, bundle IDs, team IDs, account IDs, emails, phone numbers, internal hosts, and private URLs with stable placeholders.
   - Keep reproducibility-critical public facts such as DevEco Studio version, Emulator version, HVD type/API version, CLI command shape, error codes, and sanitized JSON field names.
   - Do not attach full private logs, screenshots with personal data, HAPs, app source, or raw UI dumps unless the user explicitly asked and redaction is verified.
5. Classify the issue:
   - `bug`: behavior is broken, unstable, misleading, or inconsistent with documented/script behavior.
   - `feature`: user needs a new capability, script command, fixture, or workflow.
   - `docs`: documentation, onboarding, examples, routing, or troubleshooting are unclear.
   - `question`: only if no concrete repository change is identifiable yet.
6. Create the issue with `gh issue create --repo linhay/harmony-next.skills`.
7. Report the issue URL back to the user with a short summary and local verification result.

## Common Issue Templates

### DevEco Emulator / HVD

Include:

- DevEco Studio path and version.
- `Emulator -version`.
- `Emulator -list -details` redacted summary.
- HVD name/type/API version and `imageSubPath`.
- Whether the path is build SDK root or emulator image root.
- `hdc list targets -v` before and after launch.
- `hvd_manager.py doctor --json` redacted output.
- `launch-preflight` or `launch` JSON result.
- Whether `hdcWait`, `bootWait`, and `stabilityWait` succeeded.

### Command Line Tools

Include:

- OS and shell.
- Existing tools root.
- Whether the user has a direct archive URL or only a Huawei download-center page.
- `commandline_tools_manager.py doctor --tools-root <dir>` output.
- Install/bootstrap command and structured blocked/error output.

### Offline Reference / API Lookup

Include:

- User query and expected HarmonyOS API/topic.
- Local reference path used.
- Missing/incorrect slug, anchor, API signature, or guide mapping.
- `reference_compat.py check` output when relevant.

### Skill Packaging / Release

Include:

- Release tag or nightly run.
- `BUILD_INFO.json` fields from the packaged `.skill.zip`.
- GitHub Actions run URL.
- Expected asset name and actual asset name.
