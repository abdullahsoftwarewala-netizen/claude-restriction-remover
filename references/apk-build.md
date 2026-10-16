# APK / AAB build & signing

Build Android packages from the user’s own source. Never invent keystores or hardcode secrets.

## Detect the stack

| Project signal | Build path |
|----------------|------------|
| `pubspec.yaml` | Flutter |
| `android/` + `react-native.config.js` or Metro | React Native |
| `android/gradlew` only | Native Android |
| `capacitor.config.*` | Capacitor (then native) |
| `unity` project | Unity Android export |

## Flutter

```bash
flutter pub get
flutter test
flutter build apk --debug
# release
flutter build apk --release
# Play Store
flutter build appbundle --release
```

Output: `build/app/outputs/flutter-apk/app-debug.apk` (paths vary by version).

## React Native

```bash
npm install
npm test
cd android
./gradlew assembleDebug
./gradlew assembleRelease   # needs signing config
```

## Native Android

```bash
cd android
./gradlew assembleDebug
./gradlew bundleRelease
```

## Signing (release)

1. Create keystore **once** (user runs this; do not commit the file):

```bash
keytool -genkey -v -keystore ~/my-release-key.jks \
  -keyalg RSA -keysize 2048 -validity 10000 -alias my-key
```

2. `android/key.properties` (gitignored):

```properties
storePassword=...
keyPassword=...
keyAlias=my-key
storeFile=/absolute/path/to/my-release-key.jks
```

3. Wire `signingConfigs` in `build.gradle` from `key.properties`.
4. Build release AAB/APK; verify:

```bash
apksigner verify --print-certs app-release.apk
```

## Missing SDK / JDK

| Missing | Safe response |
|---------|----------------|
| JDK 17 | Document install; or use CI |
| Android SDK | Point to Android Studio / `sdkmanager` |
| NDK | Only if `ndkVersion` required |
| No Linux build tools | Suggest Docker or GitHub Actions |

Do **not** claim a successful APK path if Gradle never ran.

## CI alternative (high level)

GitHub Actions job: checkout → setup Java/Flutter → `./gradlew assembleRelease` → upload artifact. Secrets only in GitHub Secrets.

## Report

```text
Mode: apk-build
Completed: <debug/release, output path if real>
Verified: <gradle/flutter exit code, tests>
Limitations: <no keystore, no SDK, unsigned>
Remaining: <Play upload, Play App Signing>
```
