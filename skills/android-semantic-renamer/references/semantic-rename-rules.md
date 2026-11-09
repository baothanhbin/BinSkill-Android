# Android semantic rename rules

Use these rules to generate alternative identifiers without changing what the application does or how it looks.

## Allowed change matrix

| Category | Rename when safe | Example | Required invariant |
|---|---|---|---|
| Kotlin/Java type | Yes | `MovieRepository` -> `FilmRepository` | Responsibility, modifiers, supertypes, annotations, members, and behavior remain identical. |
| Matching source file | Yes | `MovieRepository.kt` -> `FilmRepository.kt` | Rename only the file stem associated with the renamed declaration. |
| Function/method | Yes | `displayMovie` -> `showFilm` | Parameters, return type, modifiers, body, dispatch, and call order remain identical. |
| Property/field/local/parameter | Yes | `movieItems` -> `filmEntries` | Type, value, initializer, accessor, delegation, default, and named-argument behavior remain identical. |
| Constant identifier | Yes | `MOVIE_LIMIT` -> `FILM_LIMIT` | Constant value and every behavioral use remain identical. |
| Layout/resource basename | Yes | `screen_movie_detail` -> `screen_film_detail` | All qualifier copies and references move together; XML content and rendered UI remain identical. |
| XML ID/non-string resource name | Yes | `btn_play_movie` -> `btn_start_film` | Only definition/reference names change; values, styles, geometry, interaction, and accessibility remain identical. |
| Room code declaration | Conditional | `MovieDao` -> `FilmDao` | SQL and persisted schema identities are explicit and unchanged. Skip implicit table/column identities that would drift. |
| Test declaration/file | Yes | `MovieRepositoryTest` -> `FilmRepositoryTest` | Test logic and assertions remain identical. |
| String resource | No | `R.string.title_movie` stays unchanged | Keys, references, values, translations, formatting, and `strings*.xml` basenames are immutable. |
| Package/application identity | No | `com.example.movie` stays unchanged | Packages, directories, namespace, application ID, modules, and variants are immutable. |

Examples illustrate naming shape, not mandatory word substitutions. Choose replacements from actual project context.

## Semantic-family mapping

Treat a recurring concept as a family rather than independently renaming matching text:

```text
MovieRepository     -> FilmRepository
MovieDao            -> FilmDao
MovieDetailScreen   -> FilmDetailScreen
movieItems          -> filmEntries
displayMovie        -> showFilm
screen_movie_detail -> screen_film_detail
```

Before accepting a family:

- prove each occurrence represents the same domain concept;
- preserve technical-role tokens and exact responsibilities;
- reject alternatives that imply a different data source, timing, side effect, ownership, nullability, lifecycle, or UI behavior;
- avoid translating established API/domain terminology when doing so would reduce accuracy;
- do not force every occurrence of the same word into one mapping when symbols resolve to unrelated concepts.

For example, changing `load` to `fetch` is unsafe when `fetch` would imply a network operation that the code does not perform. Prefer an alternative that remains accurate, or skip the name.

## Code-flow freeze

Only identifier tokens and mechanically required imports/references may change. Preserve byte-for-byte whenever possible:

- operators, expressions, conditions, branches, loops, returns, throws, and exception handling;
- statement and argument order;
- coroutine builders, dispatchers, scopes, Flow operators, collection order, and synchronization;
- function types, parameter order, receiver types, defaults, visibility, modifiers, and annotations other than renamed project-owned class references;
- initializers, delegated properties, getters/setters, lazy behavior, and side effects;
- lifecycle callbacks, listener wiring, dependency injection behavior, and reflection registrations;
- tests' inputs, expected values, timing, assertions, and fixtures.

A reference token inside a function body may change only because its declaration is in the approved mapping. Do not refactor, simplify, format, reorder, or clean up surrounding code.

## UI freeze

Renaming a UI declaration or resource must produce the same rendered pixels, semantics, navigation, and interaction.

For XML, preserve:

- element tree and order;
- dimensions, constraints, margins, padding, visibility, colors, styles, themes, fonts, drawables, text, content descriptions, focus, enabled/clickable state, animation, and tools/runtime attributes;
- listener and navigation wiring, except the exact resource/class reference token required by an approved rename.

For Compose, preserve:

- composable call tree and order;
- modifiers and modifier order;
- state reads/writes, remembered values, effects, keys, semantics, focus, gestures, animation, and navigation calls;
- arguments, defaults, literals, resources, previews, and test tags.

Do not alter assets, images, fonts, icons, raw resources, string contents, or resource values to make the renamed version appear different. Existing screenshot/golden output must remain identical.

## Contract and persistence boundaries

Preserve:

- Android/Kotlin/Java/library overrides and callbacks;
- Room table names, column names, database filenames, SQL, schema versions, exported schemas, and migrations;
- JSON/wire names, serialization annotations, API paths/parameters, GraphQL fields, remote keys, analytics names, and ad identifiers;
- SharedPreferences/DataStore keys and filenames, Bundle/Intent/SavedState keys, WorkManager unique names/tags, notification channel IDs, routes, deep links, actions, permissions, authorities, and IPC/AIDL names;
- JNI/native names, loaded-library values, reflection strings, class names loaded by string, ServiceLoader registrations, and externally consumed public APIs;
- ProGuard/R8 semantics, manifest behavior, Gradle dependencies, plugins, flags, and build configuration.

If Room derives a table or column identity implicitly from a code identifier, do not rename that declaration. This skill does not add annotations or migration code to compensate because its scope is rename-only.

## Resource boundaries

- Exclude `<string>` and `<string-array>` declarations, `R.string.*`, `@string/...`, translations, formatted values, and `strings*.xml` basenames from the mapping.
- Preserve resource directory and qualifier names.
- Track resources by `(type, old name)` and update all qualifier copies atomically.
- Do not rename framework or dependency resources such as `@android:id/...` or `android.R...`.
- Derive View Binding/Data Binding class and field consequences explicitly when layouts or IDs change.
- Preserve all resource values. Renaming a color, dimen, style, attr, array, plural, drawable, menu, navigation graph, animation, XML config, raw item, or font is allowed only when references can change without modifying the value or behavior.

## Mapping and review invariants

- Every mapping is one-to-one, collision-free, valid, and semantically equivalent.
- Source mappings are keyed by resolved declaration identity; bare spelling is insufficient.
- A semantic family is consistent across all related project-owned declarations and eligible resources.
- Generated code and build outputs are never edited.
- Package portions of imports remain unchanged; only renamed project-owned declaration/member portions may differ.
- No random words, common suffixes, numeric disambiguators, or meaningless churn are allowed.
- Ambiguous, contract-sensitive, already clear, or non-equivalent candidates stay unchanged and are reported.
- The final diff contains only approved names, their references/imports, and exact file moves. Any other change invalidates the affected rename unit.
