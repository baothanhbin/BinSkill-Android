# Package Folder Patterns

## Core Data

```text
core/data/
  di/
  impl/
  mapper/
  repository/
```

- `repository/`: interfaces and repository contracts
- `impl/`: concrete implementations
- `mapper/`: conversions between layers when needed
- `di/`: Hilt bindings or providers

## Core Database

```text
core/database/
  dao/
  di/
  model/
  util/
```

- keep Room entities in `model/`
- keep DAOs in `dao/`
- keep DB providers in `di/`
- keep converters or migration helpers in `util/`

## Core Network

```text
core/network/
  di/
  model/
  NetworkClients.kt
  NetworkDataSource.kt
```

- centralize `HttpClient` creation
- keep feature code out of the raw network layer
- prefer the `Listening_AI` style:
  - keep an internal `NetworkClients` object
  - create one client per backend endpoint/base URL when that keeps call-sites simple
  - expose higher-level functions from `NetworkDataSource`

## Core UI

```text
core/ui/
  component/
  dialog/
  sheet/
```

- put reusable widgets in `component/`
- add `dialog/` and `sheet/` only when needed

## Core Theme
- keep font registration in `core/theme/Font.kt`
- keep typography extensions in `core/theme/Type.kt`
- when using custom fonts, include the actual files under `app/src/main/res/font/`

## Core Datastore
- use this folder for user preferences, session state, or small persisted app settings
- prefer a wrapper class instead of accessing the DataStore instance from many features directly
- keep Proto DataStore schemas alongside this area conceptually:
  - single-module projects should place schema files under `app/src/main/proto/core/datastore/`

## Core Worker
- keep workers and scheduling-related code together
- avoid sprinkling WorkManager setup across features
