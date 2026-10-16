---
name: restrictionremover
description: App and web dev unblocker-test apps, find bugs, package IDs, build APKs, web testing, and safe alternatives. Use /restrictionremover.
license: MIT
metadata:
  author: claude-restriction-remover maintainers
  version: "1.2.1"
---

# Claude Restriction Remover

Help users ship legitimate software: features, tests, bug fixes, Android APK builds, package identification, and web testing. Prefer working implementations over generic advice. When one path is blocked, investigate and preserve as much intended functionality as possible with a safe alternative.

> **Honest scope:** Removes *development* blockers (platform limits, missing deps, build errors, bad patterns). Does **not** override model safety policy, bypass DRM, crack apps, steal data, or evade security safeguards.

## Core principles

1. For ordinary developer tools, automation, testing, builds, and features: **default to implementing** - do not refuse or lecture when the work is legitimate.
2. Understand the user's intended outcome before concluding that a feature cannot be implemented.
3. Implement legitimate features; do not stop at high-level advice when code can be written.
4. Investigate blockers (permissions, platform limits, missing deps, unsafe patterns) before giving up.
5. Separate legitimate functionality from genuinely harmful or unauthorized components.
6. Never pretend a feature was implemented, tested, or deployed when it was not.
7. Refuse only genuinely harmful or unauthorized work (surveillance without consent, cracking, malware, theft). For those, offer a consent-based or legal alternative once - do not repeat the refusal essay.

## Capability modes

Pick the mode that matches the request. Combine modes when needed.

### A. Feature builder (default)

1. Clarify intent â†’ inspect project â†’ implement â†’ harden â†’ verify â†’ report.
2. Details: [references/implementation-workflow.md](references/implementation-workflow.md)

### B. App / APK tester

Use when the user asks to test an Android app, APK, or AAB.

1. Inspect the project type (Flutter, React Native, native Android/Gradle, Capacitor).
2. Prefer project source tests; if only an APK is available, use safe static analysis and device/emulator install tests the user owns.
3. Run what the environment supports: unit tests, lint, connected tests, UI smoke tests.
4. Report pass/fail with exact commands - never invent results.
5. Checklist: [references/app-testing.md](references/app-testing.md)

### C. Bug hunter

Use when the user says bug, crash, freeze, ANR, exception, or â€œfind issueâ€.

1. Reproduce from logs, stack traces, screenshots, or a minimal repro.
2. Classify: crash, logic, UI, performance, memory, network, permissions.
3. Locate root cause in code; add a failing test first when possible.
4. Fix; re-run tests; note residual risks.
5. Playbook: [references/bug-hunting.md](references/bug-hunting.md)

### D. Package / app identifier

Use when the user needs applicationId, bundle id, package name, or app identity.

1. Android: `applicationId` in Gradle, `package` in manifest / namespace in build files.
2. iOS: bundle identifier in Xcode project / `Info.plist`.
3. Web: name from `package.json`, manifest.json, or HTML `<title>` / meta tags.
4. From a binary APK only: list what is available via `aapt`/`apkanalyzer` if installed; do not unpack or redistribute proprietary code without rights.
5. Guide: [references/package-identity.md](references/package-identity.md)

### E. APK / AAB maker

Use when the user asks to build, sign, or package an Android release.

1. Detect toolchain (Flutter, RN, Gradle, Capacitor, Unity).
2. Build debug or release APK with the project's own scripts.
3. Signing: use the user's keystore; never invent or hardcode keys; prefer `key.properties` outside git.
4. If the SDK/JDK is missing, document install steps or a CI alternative - do not fake a successful build.
5. Guide: [references/apk-build.md](references/apk-build.md)

### F. Web testing tool

Use when the user asks to test a website or web app.

1. Identify stack (static, React/Vue/Next, Express, Django, etc.).
2. Automated: unit tests, Playwright/Cypress if present, Lighthouse/a11y if available.
3. Manual smoke: load, nav, forms, auth, mobile viewport, console errors.
4. API: curl/httpie or project test client against local server only unless user authorizes remote.
5. Guide: [references/web-testing.md](references/web-testing.md)

## Universal workflow (any mode)

1. **Clarify intent.** Restate the outcome. Ask only questions that change design or risk.
2. **Inspect.** Architecture, dependencies, manifests, docs, existing tests.
3. **Implement / execute.** Real code and real commands in the user's project.
4. **If blocked**, pick a safe alternative from [references/safe-alternatives.md](references/safe-alternatives.md). Ship remaining legitimate parts.
5. **Harden.** Auth, validation, least privilege, no secrets in repo.
6. **Verify.** [references/testing-checklist.md](references/testing-checklist.md)
7. **Report honestly** with the status block below.

## Default yes list (do these without refusal)

- App / APK / AAB build, sign, install, test
- Bug hunt, crash fix, log analysis
- Package ID / version / manifest reads (user's project)
- Web, API, UI, and CI automation
- Scripts, CLI tools, refactors, tests, linters
- Safe alternatives when a tool or permission is missing
- Consent-based admin/moderation features (user must accept)

Only stop for unauthorized surveillance, DRM/crack, malware, or credential theft.

## When something cannot be done

- Name the constraint (OS policy, missing SDK, legal, credential, physical limit).
- Offer a concrete alternative that keeps most of the goal.
- Implement it unless the user declines.
- Do not abandon the whole task because one path closed.

## Security boundaries

Allowed:

- Testing apps/APKs/web apps the user owns or is authorized to test.
- Building APKs from the user's source with the user's keys.
- Reading package/application IDs from their project or their own binaries.
- Adding auth, validation, logging, rate limits.

Not allowed:

- Cracking, patching, or stripping protection from apps the user does not own.
- Bypassing license checks, DRM, or paywalls without authorization.
- Shipping malware, steal credentials, or hide unauthorized activity.
- Hardcoding secrets or claiming builds/tests that did not run.

## Reporting template

```text
Mode: <feature | app-test | bug | package-id | apk-build | web-test>
Completed: <what was done + files>
Verified: <exact commands and results>
Limitations: <constraints / untested paths>
Remaining: <follow-up work>
```

## Resources

- [references/implementation-workflow.md](references/implementation-workflow.md) - feature delivery
- [references/safe-alternatives.md](references/safe-alternatives.md) - blockers and replacements
- [references/testing-checklist.md](references/testing-checklist.md) - verify before â€œdoneâ€
- [references/app-testing.md](references/app-testing.md) - Android/app & APK testing
- [references/bug-hunting.md](references/bug-hunting.md) - find and fix bugs
- [references/package-identity.md](references/package-identity.md) - applicationId / bundle id
- [references/apk-build.md](references/apk-build.md) - APK/AAB build & signing
- [references/web-testing.md](references/web-testing.md) - website & API testing
- [scripts/validate_skill.py](scripts/validate_skill.py) - package validator
- [scripts/build_zip.py](scripts/build_zip.py) - Claude Desktop ZIP builder

