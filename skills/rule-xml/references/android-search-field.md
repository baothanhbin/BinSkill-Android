# Android search-field rule

For a View/XML search field, use this `ConstraintLayout` baseline. It assumes the enclosing header exposes a `backButton`; retain that constraint only when the back button is present.

```xml
<androidx.constraintlayout.widget.ConstraintLayout
    android:id="@+id/searchField"
    android:layout_width="0dp"
    android:layout_height="56dp"
    android:layout_marginStart="8dp"
    android:background="@drawable/bg_search_field"
    app:layout_constraintBottom_toBottomOf="parent"
    app:layout_constraintEnd_toEndOf="parent"
    app:layout_constraintStart_toEndOf="@id/backButton"
    app:layout_constraintTop_toTopOf="parent">

    <EditText
        android:id="@+id/searchEditText"
        style="@style/body_large"
        android:layout_width="0dp"
        android:layout_height="match_parent"
        android:background="@null"
        android:hint="@string/search"
        android:imeOptions="actionSearch"
        android:inputType="text"
        android:maxLength="30"
        android:paddingStart="20dp"
        android:paddingEnd="4dp"
        android:singleLine="true"
        android:textColor="@color/white"
        android:textColorHint="#5CFFFFFF"
        android:textCursorDrawable="@drawable/search_cursor"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toStartOf="@id/searchButton"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

    <ImageView
        android:id="@+id/searchButton"
        android:layout_width="44dp"
        android:layout_height="44dp"
        android:layout_marginEnd="4dp"
        android:contentDescription="@string/search"
        android:src="@drawable/ic_search"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintTop_toTopOf="parent" />
</androidx.constraintlayout.widget.ConstraintLayout>
```

When adding this layout, also add these two XML drawables under `res/drawable/` if they are not already present.

`bg_search_field.xml`:

```xml
<?xml version="1.0" encoding="utf-8"?>
<layer-list xmlns:android="http://schemas.android.com/apk/res/android">
    <item>
        <shape android:shape="rectangle">
            <gradient
                android:angle="270"
                android:endColor="#3D3937"
                android:startColor="#0C0707" />
            <corners android:radius="100dp" />
        </shape>
    </item>
    <item
        android:bottom="1dp"
        android:left="1dp"
        android:right="1dp"
        android:top="1dp">
        <shape android:shape="rectangle">
            <solid android:color="#1D1717" />
            <corners android:radius="99dp" />
        </shape>
    </item>
</layer-list>
```

`search_cursor.xml`:

```xml
<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android"
    android:shape="rectangle">
    <size android:width="2dp" />
    <solid android:color="#FFFFFFFF" />
</shape>
```

The outer layout must declare `xmlns:app="http://schemas.android.com/apk/res-auto"`. Keep `@string/search`, `@style/body_large`, `@color/white`, and `@drawable/ic_search` resource-backed; add a missing resource following the project convention rather than hard-coding text.
