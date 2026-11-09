---
name: android-semantic-renamer
description: Rename project-owned identifiers in an existing Android Kotlin/Java project to context-aware alternative names with equivalent meaning. Perform rename-only refactoring while preserving code flow, runtime behavior, application state, UI appearance and interaction, external contracts, persisted data, package identities, and string resources. Use when identifiers should be reworded rather than suffixed.
---

# Android Semantic Renamer

Perform a rename-only semantic refactor. Generate context-aware alternative names that remain close in meaning to the originals, then update only the declarations, matching file/resource names, and references required by those renames.

Never append a common suffix merely to make a name different. Never rewrite application logic or UI.

## Required input

Obtain `project_root`, the exact Android project root, before editing. The user may optionally provide naming preferences or terms to preserve. Do not require a suffix or invent a hidden naming seed.

Use the default scope unless the user narrows it: project-owned Kotlin/Java types and files, functions, properties, fields, parameters, locals, safe Room code declarations, eligible non-string Android resource names, XML IDs, tests, and their project-owned references.

Before planning or editing, read [references/semantic-rename-rules.md](references/semantic-rename-rules.md) completely.

## Non-negotiable invariants

The refactor must not change:

- control flow, data flow, expression order, threading, coroutine/Flow behavior, lifecycle, callbacks, error handling, or state transitions;
- function bodies except identifier reference tokens required by approved mappings;
- type signatures except the names of project-owned declarations and parameters;
- runtime values, literals, constants' values, default arguments, annotations' contract values, dependencies, compiler settings, or build behavior;
- UI structure, component order, layout geometry, dimensions, colors, typography, icons, drawables, text, accessibility semantics, animation, focus, gestures, navigation behavior, or interaction;
- packages, source-directory mapping, namespace, application ID, module names, build variants, or resource qualifier directories;
- persisted, wire, platform, reflection, JNI, IPC, deep-link, database, analytics, or externally consumed contract spellings;
- string-resource keys, `R.string.*`/`@string/...` references, string values, translations, or `strings*.xml` basenames.

If a candidate cannot be renamed while all invariants remain true, exclude it from the mapping and report it. Do not compensate by changing logic, UI, data, or configuration.

## Safety gate

1. Resolve and display the absolute project root. Verify it contains Gradle settings and at least one Android module.
2. Inspect repository status and preserve all pre-existing user changes. Never reset, clean, stash, or overwrite them. If planned edits overlap dirty files and cannot be separated safely, ask the user how to proceed.
3. Discover the wrapper, modules, variants, source sets, and verification commands. Run a representative baseline assemble/compile and unit tests. Run lint/static checks separately when practical. If assemble, compilation, or tests fail, record the exact failure and stop unless the user explicitly accepts that baseline. A pre-existing lint/static-analysis failure does not block a rename-only refactor when assemble, compilation, and tests succeed: record the complete baseline issue identities and counts, then require the post-refactor run to introduce no new issue, no new affected location except mechanically renamed paths/symbols, and no increased count or severity.
4. Snapshot immutable identities and UI/behavior inputs: packages, namespace/application ID, module/source-set names, contract literals, Room schema/export history, navigation wiring, manifest wiring, XML non-name attributes, Compose structure, resources, assets, and available screenshot/golden baselines.
5. Build a complete old-to-new mapping before mutation. Key source mappings by declaration identity or fully qualified symbol and resource mappings by `(resource type, old name)`. Include the semantic family, rationale, defining file, references, collision analysis, and risk classification.

Do not create a commit unless the user asks.

## Name generation

Create conservative alternative names from project context:

- Preserve the declaration's exact responsibility and technical role.
- Keep role suffixes such as `Activity`, `Fragment`, `ViewModel`, `Repository`, `Dao`, `Entity`, `Worker`, `Adapter`, `Screen`, `State`, and `Event` when they remain accurate.
- Replace descriptive stems or verbs only with close contextual equivalents. Do not use random words, numeric disambiguators, decorative prefixes, or a shared suffix.
- Preserve naming grammar: PascalCase, camelCase, lower_snake_case, or UPPER_SNAKE_CASE.
- Apply one semantic-family decision consistently. If `Movie` becomes `Film`, related project-owned names must use the same concept mapping unless their context proves they are unrelated.
- Keep overload groups, interface/implementation families, tests, and generated binding consequences synchronized.
- Skip vague, already optimal, framework-owned, external, or meaning-sensitive names when no equally accurate alternative exists.

Names must be one-to-one, collision-free, valid for their language/resource type, and different from the original. A rename that only changes case, pluralization without reason, or abbreviation clarity is not automatically safe.

## Refactor procedure

Prefer Android Studio/IntelliJ or another language-aware semantic rename facility. Otherwise use declaration-scoped mappings and compiler-guided reference updates. Never apply repository-wide regex replacement or a token dictionary keyed only by bare spelling.

Work in small dependency-aware batches:

1. Rename safe project-owned types and matching Kotlin/Java file stems. Update imports, constructors, generics, manifests, DI registrations, keep rules, tests, and unambiguous project references.
2. Rename safe Room code-only types and methods. Rename an entity type or persisted property only when explicit stable table/column names already prove that schema identity will not change. Otherwise skip it. Never edit generated Room output, schema history, SQL, or migrations.
3. Rename eligible non-string resources and file basenames across every qualifier copy. Update references, Data Binding/View Binding derived names, Navigation/Safe Args references, manifests, and tests. Preserve XML structure and every visual/behavioral attribute value except the exact identifier/reference token required by the mapping.
4. Rename remaining safe functions, properties, fields, parameters, and locals semantically. Update named arguments and project-owned interface/implementation chains without changing types, modifiers, annotations, defaults, bodies, or call order.
5. Compile after each batch. Fix only missing or incorrect references caused by the approved mapping. If compilation would require a logic, UI, contract, or configuration change, revert or skip that rename unit.

Use `git mv` for tracked files when available. If it stages changes and the user did not ask for staging, leave final changes unstaged without discarding working-tree content. Never recursively move a computed broad directory.

## Verification

Run the successful baseline commands again, then perform the strongest relevant checks available:

- assemble/compile every affected module and relevant variant;
- compile instrumentation tests and run local tests where practical;
- run lint/static checks and Room schema/migration tests when present; when lint/static analysis already failed at baseline, compare issue identities, severity, counts, and affected source locations to prove the refactor introduced no regression;
- run existing screenshot, golden, Compose UI, XML layout, and navigation tests when available;
- compare string resources, runtime literals, contracts, assets, manifest wiring, navigation wiring, Room schemas, dependencies, and immutable identities against the baseline;
- inspect Kotlin/Java diffs to prove only declaration/reference tokens, imports, and matching file names changed;
- inspect XML diffs to prove only eligible resource definitions/references changed, with visual and interaction attributes untouched;
- search for remaining old mapped identifiers, accidental mixed semantic families, duplicate targets, and unintended suffix patterns;
- run `git diff --check`, inspect repository status, and review the focused diff.

Build success is necessary but not sufficient. Any changed branch, expression, literal, Compose component tree, modifier, XML visual attribute, resource value, navigation edge, callback wiring, or dependency is a failed invariant. Revert the affected rename unit instead of explaining the change away.

## Completion report

Report:

- project root and any user-provided naming preferences;
- old-to-new mappings grouped by semantic family and category;
- skipped names and the invariant or ambiguity that blocked each rename;
- verification commands and outcomes;
- proof that code flow, runtime behavior, UI, contracts, persisted data, and string resources remain unchanged;
- any pre-existing failures or user changes that limited verification, including unchanged baseline lint/static-analysis failures.

Do not claim full completion while an approved mapping is partially applied or any required verification fails.
