---
name: android-suffix-renamer
description: Append a caller-provided suffix to project-owned names in an existing Android Kotlin/Java project, including source files, types, Room declarations, functions, variables, and Android XML resources, while preserving runtime behavior and external contracts. Use for broad suffix-only refactors; do not use for package/application ID changes or feature rewrites.
---

# Android Suffix Renamer

Perform this as a behavior-preserving semantic refactor, not as blind text replacement.

## Required inputs

Obtain these before editing:

- `project_root`: the exact Android project root.
- `suffix`: the text to append. Never infer it from a previous run or from the project path.

Use the default scope unless the user narrows it: project-owned Kotlin/Java source files and declarations, Room types and DAO/repository methods, Android resource files and entries, XML IDs, and all project references to those names. Package names, namespace, application ID, module names, and directory names are outside the default scope.

Normalize the suffix into naming-style variants without changing its words:

- Type/file and camelCase symbol suffix: PascalCase, e.g. `Binbao`.
- `snake_case` resource suffix: lower snake with a leading underscore, e.g. `_binbao`.
- `UPPER_SNAKE_CASE` suffix: upper snake with a leading underscore, e.g. `_BINBAO`.

Reject an empty suffix or one that cannot be normalized to letters/digits. Do not add the same normalized suffix twice.

Before planning or editing, read [references/rename-rules.md](references/rename-rules.md) completely.

## Safety gate

1. Resolve and display the absolute project root. Verify it contains Gradle settings and at least one Android module before any move or edit.
2. Inspect repository status and preserve all pre-existing user changes. Never reset, clean, stash, or overwrite them. If planned edits overlap dirty files, continue only when the edits can be separated safely; otherwise ask the user how to proceed.
3. Discover the project's actual wrapper, modules, variants, and existing verification commands. Run a representative baseline build/test such as the app's debug assemble plus unit tests. Run lint/static checks separately when practical so existing lint failures are distinguishable from refactor regressions. If the baseline build/test fails, record the exact failure and stop unless the user explicitly accepts proceeding from that baseline.
4. Snapshot immutable identities before mutation: package declarations and their source-directory mapping, namespace/application ID, module/source-set names, external callback names, contract strings, and JNI/reflection registrations. These are verification inputs, never rename candidates.
5. Build a complete old-to-new mapping before mutation. Key source mappings by declaration identity or fully qualified symbol, never by bare spelling alone. Include declaration kind, defining file, new name, reference locations, and contract-risk classification. Detect duplicate targets, case-only collisions, generated names, and filesystem collisions. Resolve every collision before editing.

Do not create a commit unless the user asks.

## Refactor procedure

Prefer a language-aware Android Studio/IntelliJ rename or an available Kotlin/Java semantic refactoring facility. If none is available, use declaration-scoped mappings and compiler-guided edits; never apply a repository-wide regex replacement or a global token map keyed only by identifier text. Package/import path segments and external receiver members must not be changed merely because they share a spelling with a project declaration.

Work in small dependency-aware batches and verify after each batch:

1. Rename project-owned types and their matching Kotlin/Java file stems. Update imports, constructors, generics, manifests, DI registrations, reflection/keep rules when the reference is unquestionably to that project type, and test sources.
2. Rename Room-owned Kotlin/Java declarations and methods while preserving database schema strings and migration behavior. Update DAO callers, repository interfaces/implementations, abstract database accessors, and generated-type usages in source. Never edit generated Room output.
3. Rename Android resource entries and resource file basenames consistently across all qualifier directories. Update XML references, `R` references, Data Binding expressions, Navigation/Safe Args references, manifest references, tests, generated View Binding/Data Binding class names, and generated binding fields derived from renamed IDs. Handle custom `app:` attributes, direct style parents, and `<item>` declarations regardless of XML attribute order.
4. Rename remaining project-owned functions, properties, fields, parameters, and local variables semantically. Rename each interface/abstract contract and every project-owned implementation/call site as one unit. Preserve overload resolution, named arguments, accessor behavior, and Java interop.
5. Compile Kotlin and Java after each batch. Treat an unresolved suffixed member on an Android/library receiver as a collision signal: revert or skip only that declaration/reference unit, not every same-spelled identifier globally. Search all source sets and build logic for each old mapped name. Any remaining hit must be classified as an intentional contract/string occurrence or fixed. Do not alter comments and prose merely to make the search empty.

When a symbol is part of an Android, Kotlin, Java, library, serialization, JNI, reflection, database, IPC, deep-link, or server contract, preserve the contract-facing spelling. If the project-owned code name can safely change while an annotation or explicit string keeps the wire/storage name stable, rename only the code name and retain the explicit contract value. If safety is ambiguous, leave that symbol unchanged and report it instead of guessing.

Use `git mv` for tracked files when available. Otherwise move exact verified paths with the current shell. Never recursively move or rename a computed broad directory.

If `git mv` stages changes and the user did not ask for staging, perform verification with the staged diff as needed, then leave the final changes unstaged without discarding working-tree content.

## Verification

Run the same successful baseline commands after the refactor, then run the strongest relevant checks available:

- Gradle assemble/compile for every affected module and relevant variant.
- Unit and instrumentation-test compilation; run local tests when practical.
- Android lint or the project's configured static checks.
- Room schema/export validation and migration tests if present.
- A final search for old mapped identifiers and duplicate suffixes.
- Package declarations still match their source directories, imports use the original package paths, and namespace/application ID/module names are unchanged.
- Every renamed layout/ID has matching generated binding class/field references; every renamed custom attr and style parent resolves.
- `git diff --check`, repository status, and a focused diff review proving changes are renames/reference updates rather than logic edits.

Treat build success as necessary but not sufficient. Review for changed string literals, SQL, manifest wiring, resource qualifiers, Data/View Binding names, ProGuard/R8 keep rules, reflection, and serialized/storage keys.

## Completion report

Report:

- project root and suffix variants used;
- counts by renamed category;
- verification commands and outcomes;
- intentionally preserved contract names and any skipped ambiguous symbols;
- any pre-existing build failures or user changes that limited verification.

Do not claim full completion if old project-owned declarations remain in scope or any required verification is failing.
