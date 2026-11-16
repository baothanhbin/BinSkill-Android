---
name: code-standards-enforcer
description: Implement or review code against the target project's documented standards and enforced tooling. Use when a user asks to follow, enforce, or check project coding rules; do not use merely for general coding help with no project-specific rules.
---

# Code Standards Enforcer

Make every code change conform to the target project's authoritative rules. Treat the rules as constraints on the implementation, not as optional style suggestions.

## Discover the rules first

Before editing, inspect the repository root and the relevant parent directories for project instructions and tooling. Give precedence to rules in this order:

1. Direct instructions from the user for the current task.
2. Repository and directory-scoped agent instructions (for example `AGENTS.md`, `CONTRIBUTING.md`, or a documented development guide). The closest applicable directory rule wins when scopes conflict.
3. Enforced configuration and CI definitions, such as formatter, linter, type checker, test, build, dependency, and IDE settings.
4. Established conventions in the adjacent code, where they do not conflict with the sources above.

Use fast file discovery (for example `rg --files`) and inspect only files relevant to the requested change. Common signals include `.editorconfig`, formatter and linter configuration, build files, package manifests, test configuration, and CI workflows.

If no project-specific rule exists, do not invent an arbitrary house style. Follow the language's idiomatic conventions and keep the change consistent with nearby code. Offer to add an explicit project rule only if the user asks to establish one.

## Android projects using Hilt

When the target Android project already uses Dagger Hilt (for example, it applies the Hilt Gradle plugin or has an `@HiltAndroidApp` application), read [references/android-hilt-viewmodel.md](references/android-hilt-viewmodel.md) before adding or changing a ViewModel. These are a fallback baseline derived from `ASD117_ShortDrama25`; explicit project rules and established local patterns still take precedence.

## Android user-visible text

For Android projects, read [references/android-string-resources.md](references/android-string-resources.md) before adding or changing user-visible text. Follow the project's existing resource naming and localization conventions when they differ.

## Android loading UI

For Android View/XML screens, read [references/android-loading-indicator.md](references/android-loading-indicator.md) before adding or changing an indeterminate loading indicator. Use the specified component and visual properties unless the user explicitly requests an exception.

## Android text views

For Android View/XML screens, read [references/android-textview.md](references/android-textview.md) before adding or changing a direct `TextView`-based UI label.

## Android search fields

For Android View/XML screens, read [references/android-search-field.md](references/android-search-field.md) before adding or changing a search input. Use the specified layout and paired drawable resources unless the user requests a different search design.

## Android Activity layouts

For Android Activity XML layouts, read [references/android-activity-layouts.md](references/android-activity-layouts.md) before adding or restructuring a screen.

## Implement under the rules

- Preserve the project's architecture, naming, imports, error handling, nullability, logging, documentation, and testing conventions.
- Prefer existing project utilities and patterns over introducing a competing abstraction or dependency.
- Do not disable, weaken, or bypass a formatter, linter, type checker, test, or CI check simply to make a change pass. If a rule conflicts with the user's requested behavior, explain the conflict and request direction before making an exception.
- Keep changes scoped to the task. Do not reformat or refactor unrelated files unless it is required by an enforced tool or explicitly requested.
- When a written rule and an executable check differ, satisfy the executable check and report the discrepancy succinctly.

## Verify before handoff

Run the narrowest relevant validation available in the project (format, lint, type check, focused tests, then build when appropriate). Apply automatic formatting only to files changed for the task unless the project tool necessarily touches a broader generated output.

Report what you changed, which rule sources were applied, and the validations run. State any validation you could not run and why; never claim compliance without evidence.
