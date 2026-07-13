# Feature Patterns

## Default Layout

```text
feature/<name>/
  <Feature>Screen.kt
  <Feature>ViewModel.kt
  component/
    <Feature>Content.kt
  navigation/
    <Feature>Navigation.kt
```

## Route vs Screen
- `Route`:
  - gets the `ViewModel`
  - collects state with `collectAsStateWithLifecycle()`
  - performs side effects or event collection
- `Screen`:
  - receives plain state and callbacks
  - focuses on rendering
  - starter scaffolds should default to visually blank screens unless the user asked for seeded placeholder content

## Navigation File
Each feature should expose:
- a route constant
- a `navigateTo<Feature>()` extension for `NavController`
- a `<featureName>Screen()` registration function for `NavGraphBuilder`

## Component Folder
- use `component/` for feature-local UI pieces worth separating from the main screen file
- do not move generic shared widgets here; those belong in `core/ui`
- for blank starter scaffolds, the component file can be a minimal empty content container that fills available space

## ViewModel Defaults
- use `StateFlow` for durable screen state
- use constructor injection with Hilt
- avoid feature-to-feature coupling inside `ViewModel`
