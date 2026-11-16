# Android string-resource rule

All text displayed to the user must be declared as an Android string resource, normally in `res/values/strings.xml`, and referenced from code or XML. Do not add hard-coded user-visible literals to layouts, menus, Compose UI, dialogs, Toasts, accessibility descriptions, or Kotlin/Java UI code.

- Reuse an existing resource when its wording and meaning match; otherwise add a clearly named key following the project's naming convention.
- Add locale-specific values in the existing `values-*` resource files when the project maintains translations. Keep placeholder types and order consistent across locales; use formatted string resources instead of interpolation in UI code.
- Use `plurals` for count-dependent text and `string-array` only when the project needs an actual resource-backed list.
- Text that is not user-visible, such as log tags, analytics event names, API values, database keys, and protocol constants, is not a string-resource candidate unless the project explicitly requires it.
