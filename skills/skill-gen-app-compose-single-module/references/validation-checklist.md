# Validation Checklist

Before declaring the scaffold complete, verify:
- `settings.gradle.kts` includes only `:app` unless the user asked otherwise
- the namespace and application id match the requested base package
- the package tree exists under `app/src/main/java/<base-package>/`
- the app shell lives under the `app` package
- starter features live under the `feature` package
- shared technical layers live under the `core` package
- route constants, navigation helpers, and nav host registrations are internally consistent
- strings referenced from Compose files exist in `strings.xml`
- Room schema export is enabled if Room is included
- Hilt annotations are present where required
- network files follow the intended `Listening_AI`-style split between `NetworkClients`, `NetworkDataSource`, and `NetworkModule`
- no leftover naming from `AgriDoctorAI` or unrelated example apps remains
