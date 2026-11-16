# Android Hilt ViewModel baseline

Use this baseline only for an Android project that already uses Dagger Hilt, and only when no closer project rule conflicts with it. It is based on the established Hilt/ViewModel pattern in `D:\Android\ASD117_ShortDrama25`.

## Hilt graph and ownership

- Retain the single application class annotated with `@HiltAndroidApp`.
- Annotate the Activity or Fragment that owns a Hilt ViewModel with `@AndroidEntryPoint`.
- Declare a ViewModel as `@HiltViewModel class XxxViewModel @Inject constructor(...) : ViewModel()`.
- Obtain an Activity- or Fragment-scoped ViewModel with `private val viewModel: XxxViewModel by viewModels()`. Do not manually instantiate that ViewModel, create a custom factory, or inject the ViewModel directly.
- For Compose, use the project's established Hilt ViewModel acquisition pattern; do not introduce Compose APIs into a View-based screen solely for ViewModel acquisition.

## Dependencies and state

- Constructor-inject repositories and collaborators. Reuse project-provided injectable types; add a Hilt binding only when a dependency is not constructor-injectable.
- Qualify application context with `@ApplicationContext`, and scope shared process-wide repositories only when their lifetime requires it.
- Keep mutable UI state private, expose read-only `StateFlow` via `asStateFlow()`, and update it from ViewModel actions.
- Launch asynchronous work from `viewModelScope`. Keep UI rendering, `View`, binding, `Context` tied to a screen, and lifecycle callbacks out of the ViewModel.
- In Fragments, collect ViewModel flows via `viewLifecycleOwner.lifecycleScope` and `repeatOnLifecycle(Lifecycle.State.STARTED)` so collection follows the view lifecycle.

Use `SavedStateHandle` only when the screen needs restored navigation or process-death state and the target project supports that pattern. Do not add it preemptively.
