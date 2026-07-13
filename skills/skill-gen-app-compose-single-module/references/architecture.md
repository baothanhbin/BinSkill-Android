# Architecture

## Goal
Create a new Android project that keeps only one Android module, `:app`, while still separating responsibilities clearly through package folders inside that module.

## Project Map
Use this project split by default:

```text
app/
gradle/
```

Inside the `app` module, use this package layout:

```text
app/src/main/java/<base-package>/
  app/
  core/
    data/
      di/
      impl/
      mapper/
      repository/
    database/
      dao/
      di/
      model/
      util/
    datastore/
    model/
    network/
      di/
      model/
    theme/
    ui/
      component/
      dialog/
      sheet/
    worker/
  feature/
    <name>/
      component/
      navigation/
```

## Responsibilities
- `app`: application shell, `Application`, `MainActivity`, app-level navigation, app state, top-level UI wiring
- `core/model`: shared models, enums, value objects that do not belong to one feature
- `core/theme`: colors, typography, theme entrypoint, font registration
- `core/theme`: keep `Color.kt`, `Font.kt`, `Type.kt`, and `Theme.kt` together
- `core/ui`: reusable UI components, dialogs, sheets, loading states, generic UI helpers
- `core/network`: grouped Ktor clients, datasource layer, network DTOs, network DI
- `core/data`: repository contracts, implementations, mappers, DI bindings
- `core/database`: Room database, entities, DAOs, converters, DB DI
- `core/datastore`: DataStore wrappers and preference/session persistence
- `core/worker`: WorkManager workers and job wiring
- `feature/<name>`: route, screen, viewmodel, feature-local components, navigation registration

## Naming
- only Android module include by default: `:app`
- app namespace: `<base-package>`
- app shell package: `<base-package>.app`
- feature package: `<base-package>.feature.<name>`
- core package: `<base-package>.core.<area>`
- screen file: `<Feature>Screen.kt`
- viewmodel file: `<Feature>ViewModel.kt`
- navigation file: `<Feature>Navigation.kt`
- route wrapper: `<Feature>Route`
- navigation extension: `navigateTo<Feature>`

## Compose Rules
- use Compose for all new UI
- let `Route` own `ViewModel`, state collection, and side effects
- let `Screen` receive plain state and callbacks
- keep shared UI primitives in `core/ui`
- keep feature-specific UI pieces inside that feature folder

## Architecture Intent
This is not a "flat app module" style. It is a single-module build with internal architecture boundaries. The app should still feel layered and scalable even though Gradle only sees `:app`.
