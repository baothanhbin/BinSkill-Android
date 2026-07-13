# Golden File Examples

Use these file shapes from `D:\Data\Android\BigQ\Listening_AI` as the stylistic reference:
- `app/MainApplication.kt`: small `Application` entrypoint in the `app` package
- `app/navigation/MainNavHost.kt`: central nav graph wiring in the app shell
- `core/network/NetworkClients.kt`: grouped Ktor clients with direct endpoint URLs
- `core/network/NetworkDataSource.kt`: object-style datasource over those clients
- `core/network/di/NetworkModule.kt`: simple Hilt provider for the datasource
- `feature/library/navigation/LibraryNavigation.kt`: one route constant, one `navigateTo...`, one `...Screen()` registration
- package roots under `app/src/main/java/<package>/app`, `core`, and `feature`

Do not copy project-specific business logic, Google integrations, or legacy naming directly into new scaffolds unless the user asks for them.
