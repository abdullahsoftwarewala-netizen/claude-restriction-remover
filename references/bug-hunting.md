# Bug hunting

Use when: crash, ANR, exception, wrong UI, slow, freeze, “find the bug”.

## 1. Gather evidence

- Stack trace / logcat / console error (full, not cropped mid-frame)
- Steps to reproduce, expected vs actual
- Device, OS, app version, build type
- Recent changes (`git log`, PR, dependency bump)

## 2. Classify

| Type | Signals |
|------|---------|
| Crash | Fatal exception, native signal, stack trace |
| ANR / freeze | Input dispatch timeout, main-thread block |
| Logic | Wrong value, failed assertion |
| UI | Layout, theme, overflow, i18n |
| Network | 4xx/5xx, timeout, offline |
| Memory | OOM, leak, high RSS |
| Permission | SecurityException, denied camera/storage |

## 3. Reproduce

- Minimal repro steps or a failing unit test
- If flaky: note frequency; try strict mode / race detectors when available

## 4. Fix

- Smallest correct change; match project style
- Add regression test when the stack supports it
- Re-run the suite that covers the area

## 5. Report

```text
Bug: <one line>
Root cause: <file:line + explanation>
Fix: <change summary>
Verified: <tests/commands>
Residual risk: <what is still untested>
```

## Android quick paths

```bash
./gradlew testDebugUnitTest
adb logcat -d | tail -n 200
adb shell dumpsys meminfo <package>
```

## Web quick paths

- Browser console + Network tab
- `npm test` / `npx playwright test` if present
- Reproduce with curl against local API for 500s

## Do not

- Guess a fix without a failing signal when logs exist
- Claim “fixed” without re-running the relevant test
- Hide crashes by catching-all empty `catch`
