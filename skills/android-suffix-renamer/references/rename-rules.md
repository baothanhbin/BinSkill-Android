# Android suffix rename rules

Apply suffixes to identifiers, not arbitrary text. The examples below use suffix `Binbao`.

## Rename matrix

| Category | Rename | Example | Notes |
|---|---|---|---|
| Kotlin/Java type | Yes | `MovieDao` -> `MovieDaoBinbao` | Includes classes, interfaces, objects, enums, annotations, type aliases, project-owned exceptions, and nested types. |
| Matching source file | Yes | `MovieDao.kt` -> `MovieDaoBinbao.kt` | Rename a file that represents a renamed declaration. For multi-declaration utility files, append to the file stem and rename each in-scope project declaration separately. Keep extensions unchanged. |
| Project function/method | Yes | `loadMovies` -> `loadMoviesBinbao` | Includes top-level functions, members, extensions, Room DAO methods, and project-owned callbacks. Rename the whole project-owned interface/implementation chain together. |
| Property/field/local/parameter | Yes | `movieDao` -> `movieDaoBinbao` | Update destructuring, named arguments, backing-field/accessor use, lambdas, and tests semantically. Do not rename implicit `it`, `this`, or `super`. |
| Constant | Yes | `MAX_COUNT` -> `MAX_COUNT_BINBAO` | Preserve upper-snake style. Enum entries may use this form when they are not serialized contracts. |
| Layout/resource file | Yes | `activity_main.xml` -> `activity_main_binbao.xml` | Apply the same basename mapping to every qualifier copy. Update generated binding class usage, e.g. `ActivityMainBinding` -> `ActivityMainBinbaoBinding`. |
| Resource entry | Yes | `title_home` -> `title_home_binbao` | Covers project-owned IDs, strings, colors, dimens, styles, attrs, arrays, plurals, menus, navigation graphs, drawables, mipmaps, anims, XML configs, raw/font names when safe. Preserve Android/library attribute names. |
| Manifest component type | Rename code type and references | `MainActivity` -> `MainActivityBinbao` | Update manifest/class references and keep rules. Do not change intent action/category strings unless explicitly requested. |
| Room code types | Yes | `AppDatabase` -> `AppDatabaseBinbao` | Entity/DAO/database/repository class names and project-owned accessors may be renamed. |
| Test declarations/files | Yes | `MovieDaoTest` -> `MovieDaoTestBinbao` | Update fixtures and references; keep framework test annotation names unchanged. |

## Preserve by default

These spellings are behavioral contracts, not ordinary code identifiers:

- Packages, source directories, Gradle module names, namespace, application ID, build types, product flavors, signing config names, dependency coordinates, and plugin IDs.
- Android/Kotlin/Java/library overrides and callbacks such as `onCreate`, `onStart`, `onClick`, `equals`, `hashCode`, `toString`, `compareTo`, `invoke`, `getItemCount`, and methods required by external interfaces. Also preserve required operator/component names.
- Annotation type names and XML attributes owned by Android or dependencies.
- Room `tableName`, `@ColumnInfo(name=...)`, database filename, SQL table/column spelling inside `@Query`/migrations, schema versions, exported schema history, and migration start/end versions. Rename a query method, not its SQL.
- JSON/wire field names, `@SerializedName`, `@SerialName`, Moshi/Jackson names, Retrofit paths/parameters, GraphQL fields, server keys, Remote Config keys, analytics event/parameter names, Firebase collection/document names, and ad-unit identifiers.
- SharedPreferences/DataStore keys and file names, Bundle/Intent extra keys, SavedState keys, WorkManager unique names/tags, notification channel IDs, deep links, intent actions/categories, permissions, authorities, URI paths, navigation route strings, and IPC/AIDL contract names.
- JNI/native method names, `System.loadLibrary` values, C/C++ exported symbols, reflection strings, class names loaded by string, ServiceLoader registrations, ProGuard/R8 rule syntax, and externally consumed public API names unless all consumers are in scope and verified.
- Assets and arbitrary raw data file names when accessed by string, generated code, build outputs, `.gradle`, IDE metadata, Git internals, vendored dependencies, binaries, keystores, and secrets.
- User-visible string values, comments, documentation, licenses, URLs, and ordinary string contents solely because they contain an old identifier.

Explicit contract annotations are a boundary: for `@SerializedName("movie_id") val movieId`, `movieId` may become `movieIdBinbao`, while `"movie_id"` remains unchanged.

## Special cases

### Android resources

- Resource file basenames, IDs, attrs, and ordinary value-entry names must remain valid lower snake case. Structured names that legitimately use another grammar, especially style/theme names with dots or existing capitalization, keep that grammar and append the corresponding style-preserving suffix. Rename definitions and references as one atomic mapping per resource type.
- Preserve directory names such as `layout`, `layout-land`, `values-night`, and `drawable-hdpi`; rename the resource basename inside them.
- A basename repeated across qualifiers is one logical resource and must receive the identical new name everywhere.
- Distinct resource types have distinct namespaces. Track `(type, oldName) -> newName`, not only the bare old name.
- Update `@type/name`, `@+id/name`, `?attr/name`, `R.type.name`, static imports, style/item references, `<include layout=...>`, menus, navigation XML, and manifest resource references.
- Parse resource declarations structurally rather than assuming XML attribute order. Both `<item type="id" name="x">` and `<item name="x" type="id">` define the same ID.
- Update custom-attribute usages such as `app:skeletonCornerRadius`, direct style parents such as `parent="AppTheme"`, and styleable composite fields such as `R.styleable.Widget_attr`.
- Layout rename changes View Binding/Data Binding generated type names. Derive the generated class using Android's underscore-to-PascalCase convention and update imports/usages. ID rename also changes generated binding field names; derive and map those fields explicitly (for example, `btn_cancel` -> `btnCancel`, then apply the resource suffix mapping).
- Do not rename framework resources such as `@android:id/...`, `android.R...`, or dependency resources.

### Kotlin and Java semantics

- A declaration and references may share text with unrelated declarations. Resolve symbols before replacing.
- Never infer ownership from spelling alone. A local `context`, a model property `id`, `R.id`, `View.id`, a package segment, and an imported symbol are different rename units even when their token text matches.
- Keep package declarations and package portions of imports byte-for-byte stable. Only the imported project-owned type/member portion may change. After editing, derive the expected package from each source directory and compare it to the declaration.
- Preserve override names when the root contract is external. A project-owned interface may be renamed only with every implementation and caller in scope.
- Check overloads, extension receivers, callable references (`::name`), property references, delegated properties, companion/static access, annotations using `KClass`, Java getters/setters, and `@JvmName`/`@JvmField`/`@JvmStatic` boundaries.
- Parameter renames require updating Kotlin named-argument call sites. Java callers are unaffected by parameter names but still need compile verification.
- Data-class constructor property changes alter generated component/property names at source level; update all Kotlin/Java callers while preserving serialized/storage names.
- For Compose, rename project-owned composable functions and state variables but preserve framework parameter/semantics keys and externally stable routes.

### Room

- Rename entity class names, DAO interface names, database class names, repository types, DAO methods, abstract DAO accessor methods, and their files/references.
- Preserve persisted schema identity. Do not change table or column names just to suffix code identifiers.
- If Room relied on implicit table or column names derived from code identifiers, add explicit `tableName` or `@ColumnInfo(name=...)` with the old persisted name before renaming the Kotlin/Java identifier. This prevents an accidental schema change.
- Apply `@ColumnInfo` to every persisted property, including a `@PrimaryKey` declared on the same line. Preserve `primaryKeys=[...]` strings.
- Preserve SQL table/column text. Rename only named bind placeholders (`:parameter`) when the corresponding DAO parameter is renamed, and keep the placeholder synchronized if a parameter is later skipped because of a collision. Regenerate by building; never modify Room-generated implementation sources.
- Confirm schema JSON and migration diffs do not show unintended table/column changes.

## Mapping and review invariants

- Mapping is one-to-one and idempotent: no two old names produce the same target, and already suffixed names remain unchanged.
- Source mappings are keyed by symbol identity; resource mappings are keyed by `(resource type, old name)`. A bare-token dictionary is insufficient for either source semantics or generated bindings.
- Only declarations owned by the target project are rename candidates. Usages in all source sets are updated, but external declarations are not.
- File extensions and resource qualifiers remain unchanged.
- The refactor must not change literals that define wire, storage, database, reflection, platform, or user-visible behavior.
- Diff review should show declaration/file/resource renames plus mechanically necessary reference updates. Any changed conditional, loop, coroutine flow, SQL logic, expression order, literal value, or dependency is out of scope and must be reverted or explained before completion.
