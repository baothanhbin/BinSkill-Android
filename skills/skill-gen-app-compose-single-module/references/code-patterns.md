# Code Patterns

## State
- prefer immutable UI state data classes
- expose `StateFlow` from `ViewModel`
- use `MutableSharedFlow` only for one-off events when really needed

## Hilt
- annotate `MainActivity` with `@AndroidEntryPoint`
- annotate app `Application` with `@HiltAndroidApp`
- keep DI entry files close to their technical layer, for example:
  - `core/network/di/NetworkModule.kt`
  - `core/data/di/DataModule.kt`
  - `core/database/di/DatabaseModule.kt`

## Room
- keep schema export enabled
- start with one small example entity/DAO if the user did not specify real tables yet
- avoid destructive migration defaults unless the user explicitly accepts them

## DataStore
- default to a domain-specific wrapper class such as `AppSettingsDataStore`
- keep preference keys private to the wrapper

## Network
- mirror `Listening_AI`:
  - `NetworkClients` owns preconfigured Ktor clients
  - `NetworkDataSource` exposes suspend functions over those clients
  - `NetworkModule` can simply provide the datasource object
- avoid calling Ktor directly from repositories or features

## Workers
- if workers are scaffolded, keep them simple and injected
- prefer one placeholder worker that shows the pattern instead of many half-finished workers

## Resources
- keep feature titles and descriptions in `strings.xml`
- avoid hardcoding repeated user-facing text in Compose files
- keep custom fonts in `res/font`
- prefer a dedicated `Font.kt` plus typography extensions in `Type.kt` for app-wide text styles
