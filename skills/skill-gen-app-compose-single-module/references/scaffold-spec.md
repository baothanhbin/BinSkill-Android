# Scaffold Spec

## Required Output
Generate a real Android project skeleton with:
- root Gradle files
- `gradle/libs.versions.toml`
- exactly one Android module: `:app`
- package-folder architecture inside `app/src/main/java/<base-package>/`

## Root Files
Create:
- `settings.gradle.kts`
- `build.gradle.kts`
- `gradle.properties`
- `.gitignore`
- `gradle/libs.versions.toml`

## App Module Files
Create:
- `app/build.gradle.kts`
- `app/src/main/AndroidManifest.xml`
- `app/src/main/proto/core/datastore/app_settings.proto`
- `app/src/main/res/font/bevietnampro_semibold.ttf`
- `app/src/main/res/font/bevietnampro_medium.ttf`
- `app/src/main/res/font/bevietnampro_regular.ttf`
- `app/src/main/res/drawable/ic_top_level_selected.xml`
- `app/src/main/res/drawable/ic_top_level_unselected.xml`
- `app/src/main/res/values/strings.xml`
- `app/src/main/res/values/themes.xml`

## App Shell Files
Create:
- `app/MainApplication.kt`
- `app/MainActivity.kt`
- `app/MainViewModel.kt`
- `app/navigation/AppState.kt`
- `app/navigation/MainNavHost.kt`
- `app/navigation/TopLevelDestination.kt`
- `app/ui/AppUiProviders.kt`
- `app/ui/MainApp.kt`

## Core Files
Create a small but real baseline for:
- `core/theme`
- `core/ui`
- `core/network`
- `core/data`
- `core/database`
- `core/datastore`
- `core/worker`

These files should compile as a starter baseline, even if some business logic is placeholder-shaped.

For `core/network`, include at least:
- an internal `NetworkClients` object
- one datasource/facade file over those clients
- one DI file that provides the datasource in the `Listening_AI` style

For `core/theme`, include at least:
- `Font.kt` for custom font families
- `Type.kt` for typography extensions
- starter font assets under `app/src/main/res/font/`

## Feature Files
For each requested starter feature, create:

```text
feature/<name>/
  <Feature>Screen.kt
  <Feature>ViewModel.kt
  component/
    <Feature>Content.kt
  navigation/
    <Feature>Navigation.kt
```

## Feature Defaults
- the first feature is the start destination
- later features should be reachable from the start feature
- keep routes string-based and simple
- use shared strings for feature titles and descriptions

## Non-Goals
- do not create extra Android library modules unless the user explicitly asks
- do not invent a domain layer unless the user explicitly wants one
- do not flatten everything into one package
