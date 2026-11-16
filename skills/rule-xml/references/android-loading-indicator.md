# Android loading-indicator rule

For an indeterminate loading animation in an Android XML/View screen, use `com.google.android.material.progressindicator.CircularProgressIndicator` with this exact visual baseline:

```xml
<com.google.android.material.progressindicator.CircularProgressIndicator
    android:layout_width="36dp"
    android:layout_height="36dp"
    android:layout_gravity="center"
    android:indeterminate="true"
    app:indicatorColor="#B3FFFFFF"
    app:indicatorSize="36dp"
    app:trackColor="@android:color/transparent"
    app:trackThickness="3dp" />
```

- Ensure the root layout declares the `app` namespace: `xmlns:app="http://schemas.android.com/apk/res-auto"`.
- Place the indicator in a parent that supports `layout_gravity` (such as `FrameLayout`) when it needs to be centered. Do not replace the component with `ProgressBar` or a custom spinner.
- Toggle the indicator's visibility from the screen's loading state; do not create, start, or stop it from a ViewModel.
- This rule is for indeterminate loading only. Keep an existing progress-bar pattern when the UI must display measurable progress.
