---
name: skill-gen-app-compose-single-module
description: "Scaffold a brand-new Android project from zero so it uses a single `:app` module, while organizing `app`, `core`, and `feature` by package folders inside `app/src/main/java`, inspired by `D:\\Data\\Android\\BigQ\\Listening_AI`. Use when Codex should create a Compose-first Android starter that keeps architecture boundaries through folders instead of Gradle modules."
---

# Skill Gen App Compose Single Module

## Overview
Use this skill when the user wants a fresh Android project that keeps only one Android module, `:app`, while still separating responsibilities through package folders such as:
- `app`
- `core/*`
- `feature/*`

This skill is intentionally opinionated toward the organization style of `D:\Data\Android\BigQ\Listening_AI`, where the real app architecture lives inside the `app` module instead of being split into many Gradle modules.

## Required Inputs
Collect or infer these before scaffolding:
- project name
- base package, for example `com.example.listeningai`
- starter features to create now, for example `home,settings`
- whether the user wants only a minimal shell or an initial starter flow

If the user does not specify all of them, make reasonable defaults and state them while scaffolding.

## Workflow
1. Read `references/architecture.md` first.
2. Read `references/scaffold-spec.md` before creating files.
3. Read `references/app-shell-patterns.md` before generating or changing files in the `app` package.
4. Read `references/package-folder-patterns.md` before generating or changing any `core/*` package.
5. Read `references/feature-patterns.md` and `references/code-patterns.md` before generating feature code, navigation, or repository wiring.
6. Read `references/golden-file-examples.md` before refining app shell or feature file shapes.
7. Create the project skeleton by running `scripts/scaffold_project.py`.
8. Inspect the generated tree and fill any project-specific gaps the user requested.
9. If the user asked for starter features, wire one end-to-end first and then repeat the pattern.
10. Validate the scaffold by reading `references/validation-checklist.md`.

## Execution Rules
- Prefer creating the real project files instead of only describing what to do.
- Keep `settings.gradle.kts` limited to `include(":app")` unless the user explicitly asks for more modules.
- Keep architecture boundaries inside `app/src/main/java/<base-package>/`.
- Keep package roots in the form:
  - `<base-package>.app`
  - `<base-package>.core.<area>`
  - `<base-package>.feature.<name>`
- Keep `Route` responsible for `ViewModel`, state collection, and side effects by default.
- Keep `Screen` focused on UI-ready state and callbacks.
- Keep reusable UI pieces in `core/ui/component`, with `dialog/` and `sheet/` only when needed.
- Keep repository contracts in `core/data/repository`, implementations in `core/data/impl`, and DI in `core/data/di`.
- Keep Room classes under `core/database`, DataStore wrappers under `core/datastore`, network access under `core/network`, and background work under `core/worker`.
- Avoid `feature -> feature` dependencies in fresh scaffolds unless the requested flow clearly benefits from it.
- Default new code to `collectAsStateWithLifecycle()`, `StateFlow` for durable state, and `SharedFlow` only for one-off events.
- Avoid carrying over legacy quirks from old projects when a cleaner baseline is possible.

## Scaffolding Order
1. Create root Gradle files and `settings.gradle.kts`.
2. Create `gradle/libs.versions.toml`.
3. Create the `app` module Gradle file.
4. Create package folders inside the `app` module:
   - `app`
   - `core/model`
   - `core/theme`
   - `core/ui`
   - `core/network`
   - `core/data`
   - `core/database`
   - `core/datastore`
   - `core/worker`
   - `feature/<name>`
5. Create the app shell:
   - `MainApplication.kt`
   - `MainActivity.kt`
   - `MainViewModel.kt`
   - `navigation/AppState.kt`
   - `navigation/MainNavHost.kt`
   - `navigation/TopLevelDestination.kt`
   - `ui/AppUiProviders.kt`
   - `ui/MainApp.kt`
6. Create starter features if requested.
7. Wire the initial navigation graph and shared resource strings.

## Script Usage
Run the scaffold script like this:

```powershell
python scripts/scaffold_project.py ^
  --project-name "ListeningStarter" ^
  --package "com.example.listeningstarter" ^
  --features "home,settings"
```

Optional flags:
- `--output "D:\work\ListeningStarter"`: scaffold into another folder; if omitted, scaffold into the current working directory
- `--minimal`: create only the baseline shell and core folders without starter feature files
- `--features "home,library,settings"`: create custom starter features

## References
- Read `references/architecture.md` for the target single-module architecture and responsibility map.
- Read `references/scaffold-spec.md` for the generated folder map and file expectations.
- Read `references/app-shell-patterns.md` for the required `app` package shape.
- Read `references/package-folder-patterns.md` for `core/*` folder boundaries and naming rules.
- Read `references/feature-patterns.md` for feature folder layout, route/screen/viewmodel split, and navigation defaults.
- Read `references/code-patterns.md` for the default implementation shape of navigation, Hilt modules, repositories, Room, DataStore, and workers.
- Read `references/golden-file-examples.md` for the closest reference file shapes inspired by `Listening_AI`.
- Read `references/validation-checklist.md` before declaring the scaffold complete.

## Output Expectations
- Produce a real scaffolded project, not just prose.
- Keep generated names internally consistent across package names, namespaces, routes, and resources.
- State the assumptions you made if the user left parts unspecified.
- If the user later wants more features, extend the existing single-module scaffold instead of rebuilding it.
