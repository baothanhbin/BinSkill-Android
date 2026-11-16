# Android TextView rule

Use the project's `AlwaysMarqueeTextView` as the default XML component for every newly added direct text label. Do not use a plain `TextView` for those labels.

- Resolve the target project's existing fully qualified `AlwaysMarqueeTextView` class before writing XML. If it does not exist, add the reusable AppCompat-based marquee view before using it; it must be single-line, use marquee ellipsizing, repeat indefinitely, and remain selected so marquee animation works.
- Retain specialized widgets when their behavior is required, such as `EditText`, `TextInputEditText`, `Button`, `MaterialButton`, or a third-party text component. Do not replace existing widgets outside the requested change merely to apply this baseline.
- A text label acting as a button must include `android:paddingHorizontal="10dp"`. Apply this to an `AlwaysMarqueeTextView` used as the interactive button surface; do not add it to a parent when the TextView itself is not the click target.
- Apply a text style declared in the project's `res/values/style.xml` or `styles.xml`, choosing the semantic typography that fits the label (for example, `style="@style/body_medium"`). Do not duplicate a matching style with inline `textSize`, `fontFamily`, `textStyle`, or line-height attributes.
- Continue to source all user-visible text from string resources as required by `android-string-resources.md`.

Example, replacing `com.example.app.view` with the target project's package:

```xml
<com.example.app.view.AlwaysMarqueeTextView
    style="@style/body_medium"
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:paddingHorizontal="10dp"
    android:text="@string/action_continue" />
```
