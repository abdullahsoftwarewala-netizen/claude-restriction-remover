# App / APK testing

Use for Android apps, Flutter/RN projects, and standalone APK/AAB files the user owns.

## Prefer source when available

| Stack | Good first commands |
|-------|---------------------|
| Flutter | `flutter analyze`, `flutter test`, `flutter build apk --debug` |
| React Native | `npm test`, `npx tsc --noEmit`, `cd android && ./gradlew test` |
| Native Android | `./gradlew test`, `./gradlew lint`, `./gradlew connectedDebugAndroidTest` (device needed) |
| Capacitor | project unit tests + `npx cap sync` then platform build |

## APK-only testing (no source)

Only if the user owns the APK and asks for testing:

1. Confirm ownership/authorization in one short line.
2. If tools exist, use them; if not, say so — do not invent output.

Useful tools (install only if user agrees):

```bash
# Package id / version (Android SDK build-tools)
aapt dump badging app.apk | head
# or
apkanalyzer manifest print app.apk

# Signature info
apksigner verify --print-certs app.apk
# or
jarsigner -verify -verbose -certs app.apk
```

3. Install on a device/emulator the user controls:

```bash
adb install -r app.apk
adb logcat | grep -iE "AndroidRuntime|FATAL|ANR"
```

4. Smoke: launch, login (test account), main flows, rotation, background/foreground, permission dialogs.
5. Never redistribute the APK or strip signatures without authorization.

## What to report

- Build type (debug/release), device/API level if tested
- Automated results (exact command + pass/fail counts)
- Manual smoke checklist
- Crashes with log excerpts
- What was **not** tested

## Common blockers and safe paths

| Blocker | Safe path |
|---------|-----------|
| No Android SDK | Document install or use CI (GitHub Actions) |
| No signing keystore | Use debug keystore; guide user to create release keystore |
| No device | Emulator, or unit tests only — say clearly |
| Play App Signing | Build AAB; upload via user’s Play Console |
| Gradle OOM | Increase `org.gradle.jvmargs`, fix memory |
