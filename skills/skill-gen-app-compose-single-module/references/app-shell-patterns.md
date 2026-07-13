# App Shell Patterns

## Package Shape
Keep the app shell under:

```text
<base-package>.app
  MainApplication.kt
  MainActivity.kt
  MainViewModel.kt
  navigation/
  ui/
```

## MainApplication
- annotate with `@HiltAndroidApp`
- if a worker is scaffolded, wire `HiltWorkerFactory` through `Configuration.Provider`

## MainActivity
- keep it small
- it should primarily call `setContent`
- wrap app content with a single UI provider entrypoint

## MainApp
- own the remembered navigation state
- set the app-level `Scaffold`
- host `MainNavHost`
- keep long business logic out of this file

## AppState
- keep a thin wrapper around `NavHostController`
- put app-level navigation helpers here only if they are broadly useful

## TopLevelDestination
- use it to map routes to top-level UI metadata
- prefer the `Listening_AI` shape:
  - `route`
  - `selectedIconId`
  - `unselectedIconId`
  - `labelId`
- keep enum entries in uppercase style such as `HOME` or `ADD_CONTENT`
- keep it close to app navigation, not inside features

## MainViewModel
- reserve it for app-wide state, startup orchestration, or shell-level flags
- do not dump feature logic here
