# Package / app identifier

How to find applicationId, bundle ID, and display identity — safely.

## Android (source)

1. **Modern Gradle (Kotlin DSL)** — `android/app/build.gradle.kts`:

```kotlin
android {
    namespace = "com.example.app"
    defaultConfig {
        applicationId = "com.example.app"
        versionCode = 1
        versionName = "1.0"
    }
}
```

2. **Groovy** — `android/app/build.gradle`:

```gradle
android {
    namespace 'com.example.app'
    defaultConfig {
        applicationId "com.example.app"
        versionCode 1
        versionName "1.0"
    }
}
```

3. Flutter: `android/app/build.gradle` `applicationId`, or `ios/Runner.xcodeproj` bundle id.
4. React Native: same Gradle path under `android/`.

## Android (APK only, user-owned)

```bash
aapt dump badging app.apk | grep -E "package:|application-label"
# or
apkanalyzer manifest application-id app.apk
apkanalyzer manifest version-name app.apk
```

## iOS

- Xcode → target → **Bundle Identifier**
- Or `ios/*/Info.plist` → `CFBundleIdentifier`
- Or `project.pbxproj` → `PRODUCT_BUNDLE_IDENTIFIER`

## Web / Node

- `package.json` → `"name"` (npm name, not always public brand)
- `public/manifest.json` → `name`, `short_name`
- HTML: `<title>`, `<meta name="application-name">`

## Renaming package (when user asks)

1. Change `applicationId` (affects Play Store identity — old users won’t upgrade).
2. Refactor Java/Kotlin namespace carefully; use IDE refactor, not blind find-replace.
3. Update deep links, ContentProviders, file paths, CI scripts.
4. Rebuild and retest; document that Play identity change is high-risk.

## Never

- Rebrand someone else’s APK or strip their package identity for impersonation
- Publish a clone under a confusingly similar applicationId
