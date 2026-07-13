#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path
from textwrap import dedent

SKILL_ROOT = Path(__file__).resolve().parent.parent
FONT_ASSETS_DIR = SKILL_ROOT / "assets" / "fonts"


def package_to_path(package_name: str) -> Path:
    return Path(*package_name.split("."))


def pascal_case(value: str) -> str:
    parts = [part for part in re.split(r"[^a-zA-Z0-9]+", value) if part]
    return "".join(part[:1].upper() + part[1:] for part in parts) or "Feature"


def camel_case(value: str) -> str:
    pascal = pascal_case(value)
    return pascal[:1].lower() + pascal[1:] if pascal else value


def humanize(value: str) -> str:
    parts = [part for part in re.split(r"[^a-zA-Z0-9]+", value) if part]
    return " ".join(part[:1].upper() + part[1:] for part in parts) or value


def resource_name(value: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9]+", "_", value).strip("_").lower()
    if not normalized:
        return "value"
    if normalized[0].isdigit():
        return f"value_{normalized}"
    return normalized


def xml_escape(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "\\'")
    )


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    normalized = content.lstrip("\n").rstrip()
    path.write_text((normalized + "\n") if normalized else "", encoding="utf-8")


def remove_file_if_exists(path: Path) -> None:
    if path.exists():
        path.unlink()


def copy_file(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def strings_block(project_name: str, features: list[str]) -> str:
    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        "<resources>",
        f'    <string name="app_name">{xml_escape(project_name)}</string>',
        '    <string name="shell_title">App Shell</string>',
        '    <string name="shell_loading">Preparing app...</string>',
        '    <string name="generic_back">Back</string>',
        '    <string name="generic_open">Open</string>',
    ]
    for feature in features:
        key = resource_name(feature)
        label = xml_escape(humanize(feature))
        lines.append(f'    <string name="feature_{key}_title">{label}</string>')
        lines.append(
            f'    <string name="feature_{key}_description">'
            f'This starter screen belongs to the {label} feature inside the single app module.'
            "</string>"
        )
    lines.append("</resources>")
    return "\n".join(lines)


def create_root_files(root: Path, project_name: str) -> None:
    write_file(
        root / "settings.gradle.kts",
        dedent(
            f"""
            pluginManagement {{
                repositories {{
                    google {{
                        content {{
                            includeGroupByRegex("com\\\\.android.*")
                            includeGroupByRegex("com\\\\.google.*")
                            includeGroupByRegex("androidx.*")
                        }}
                    }}
                    mavenCentral()
                    gradlePluginPortal()
                }}
            }}
            dependencyResolutionManagement {{
                repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
                repositories {{
                    google()
                    mavenCentral()
                }}
            }}

            rootProject.name = "{project_name}"
            include(":app")
            """
        ),
    )

    write_file(
        root / "build.gradle.kts",
        dedent(
            """
            plugins {
                alias(libs.plugins.android.application) apply false
                alias(libs.plugins.jetbrains.kotlin.android) apply false
                alias(libs.plugins.jetbrains.kotlin.plugin.compose) apply false
                alias(libs.plugins.google.devtools.ksp) apply false
                alias(libs.plugins.google.dagger.hilt.android) apply false
                alias(libs.plugins.jetbrains.kotlin.plugin.serialization) apply false
                alias(libs.plugins.androidx.room) apply false
                alias(libs.plugins.google.protobuf) apply false
            }}
            """
        ),
    )

    write_file(
        root / "gradle.properties",
        dedent(
            """
            org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
            android.useAndroidX=true
            kotlin.code.style=official
            android.nonTransitiveRClass=true
            """
        ),
    )

    write_file(
        root / ".gitignore",
        dedent(
            """
            .gradle/
            .idea/
            build/
            */build/
            local.properties
            *.iml
            captures/
            .DS_Store
            """
        ),
    )

    write_file(
        root / "gradle" / "libs.versions.toml",
        dedent(
            """
            [versions]
            agp = "8.13.0"
            kotlin = "2.0.21"
            ksp = "2.0.21-1.0.25"
            googleProtobuf = "0.9.5"
            coreKtx = "1.16.0"
            lifecycle = "2.9.4"
            activityCompose = "1.10.0"
            composeBom = "2025.09.01"
            material3 = "1.4.0"
            material = "1.13.0"
            navigationCompose = "2.9.4"
            hilt = "2.52"
            hiltNavigationCompose = "1.3.0"
            room = "2.8.1"
            datastore = "1.1.7"
            work = "2.9.1"
            kotlinxSerialization = "1.7.3"
            ktor = "2.3.12"
            junit = "4.13.2"
            junitVersion = "1.3.0"
            espressoCore = "3.7.0"
            protobuf = "4.28.2"

            [libraries]
            androidx-core-ktx = { group = "androidx.core", name = "core-ktx", version.ref = "coreKtx" }
            androidx-lifecycle-runtime-ktx = { group = "androidx.lifecycle", name = "lifecycle-runtime-ktx", version.ref = "lifecycle" }
            androidx-lifecycle-runtime-compose = { group = "androidx.lifecycle", name = "lifecycle-runtime-compose", version.ref = "lifecycle" }
            androidx-lifecycle-viewmodel-compose = { group = "androidx.lifecycle", name = "lifecycle-viewmodel-compose", version.ref = "lifecycle" }
            androidx-activity-compose = { group = "androidx.activity", name = "activity-compose", version.ref = "activityCompose" }
            androidx-compose-bom = { group = "androidx.compose", name = "compose-bom", version.ref = "composeBom" }
            androidx-ui = { group = "androidx.compose.ui", name = "ui" }
            androidx-ui-graphics = { group = "androidx.compose.ui", name = "ui-graphics" }
            androidx-ui-tooling = { group = "androidx.compose.ui", name = "ui-tooling" }
            androidx-ui-tooling-preview = { group = "androidx.compose.ui", name = "ui-tooling-preview" }
            androidx-ui-test-manifest = { group = "androidx.compose.ui", name = "ui-test-manifest" }
            androidx-ui-test-junit4 = { group = "androidx.compose.ui", name = "ui-test-junit4" }
            androidx-material3 = { group = "androidx.compose.material3", name = "material3", version.ref = "material3" }
            material = { group = "com.google.android.material", name = "material", version.ref = "material" }
            androidx-navigation-compose = { module = "androidx.navigation:navigation-compose", version.ref = "navigationCompose" }
            hilt-android = { group = "com.google.dagger", name = "hilt-android", version.ref = "hilt" }
            dagger-hilt-compiler = { group = "com.google.dagger", name = "hilt-compiler", version.ref = "hilt" }
            androidx-hilt-navigation-compose = { group = "androidx.hilt", name = "hilt-navigation-compose", version.ref = "hiltNavigationCompose" }
            androidx-hilt-work = { group = "androidx.hilt", name = "hilt-work", version.ref = "hiltNavigationCompose" }
            androidx-hilt-compiler = { group = "androidx.hilt", name = "hilt-compiler", version.ref = "hiltNavigationCompose" }
            androidx-room-runtime = { module = "androidx.room:room-runtime", version.ref = "room" }
            androidx-room-compiler = { module = "androidx.room:room-compiler", version.ref = "room" }
            androidx-room-ktx = { module = "androidx.room:room-ktx", version.ref = "room" }
            androidx-datastore = { group = "androidx.datastore", name = "datastore", version.ref = "datastore" }
            protobuf-kotlin-lite = { group = "com.google.protobuf", name = "protobuf-kotlin-lite", version.ref = "protobuf" }
            protobuf-protoc = { group = "com.google.protobuf", name = "protoc", version.ref = "protobuf" }
            androidx-work-runtime-ktx = { group = "androidx.work", name = "work-runtime-ktx", version.ref = "work" }
            kotlinx-serialization-json = { group = "org.jetbrains.kotlinx", name = "kotlinx-serialization-json", version.ref = "kotlinxSerialization" }
            ktor-client-core = { module = "io.ktor:ktor-client-core", version.ref = "ktor" }
            ktor-client-android = { module = "io.ktor:ktor-client-android", version.ref = "ktor" }
            ktor-client-logging = { module = "io.ktor:ktor-client-logging", version.ref = "ktor" }
            ktor-client-content-negotiation = { module = "io.ktor:ktor-client-content-negotiation", version.ref = "ktor" }
            ktor-serialization-kotlinx-json = { module = "io.ktor:ktor-serialization-kotlinx-json", version.ref = "ktor" }
            junit = { group = "junit", name = "junit", version.ref = "junit" }
            androidx-junit = { group = "androidx.test.ext", name = "junit", version.ref = "junitVersion" }
            androidx-espresso-core = { group = "androidx.test.espresso", name = "espresso-core", version.ref = "espressoCore" }

            [plugins]
            android-application = { id = "com.android.application", version.ref = "agp" }
            jetbrains-kotlin-android = { id = "org.jetbrains.kotlin.android", version.ref = "kotlin" }
            jetbrains-kotlin-plugin-compose = { id = "org.jetbrains.kotlin.plugin.compose", version.ref = "kotlin" }
            jetbrains-kotlin-plugin-serialization = { id = "org.jetbrains.kotlin.plugin.serialization", version.ref = "kotlin" }
            google-devtools-ksp = { id = "com.google.devtools.ksp", version.ref = "ksp" }
            google-dagger-hilt-android = { id = "com.google.dagger.hilt.android", version.ref = "hilt" }
            androidx-room = { id = "androidx.room", version.ref = "room" }
            google-protobuf = { id = "com.google.protobuf", version.ref = "googleProtobuf" }
            """
        ),
    )


def create_app_build_file(root: Path, base_package: str) -> None:
    write_file(
        root / "app" / "build.gradle.kts",
        dedent(
            f"""
            plugins {{
                alias(libs.plugins.android.application)
                alias(libs.plugins.jetbrains.kotlin.android)
                alias(libs.plugins.jetbrains.kotlin.plugin.compose)
                alias(libs.plugins.google.devtools.ksp)
                alias(libs.plugins.google.dagger.hilt.android)
                alias(libs.plugins.jetbrains.kotlin.plugin.serialization)
                alias(libs.plugins.androidx.room)
                alias(libs.plugins.google.protobuf)
            }}

            android {{
                namespace = "{base_package}"
                compileSdk = 36

                defaultConfig {{
                    applicationId = "{base_package}"
                    minSdk = 26
                    targetSdk = 36
                    versionCode = 1
                    versionName = "1.0"
                    testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
                }}

                buildTypes {{
                    release {{
                        isMinifyEnabled = false
                        proguardFiles(
                            getDefaultProguardFile("proguard-android-optimize.txt"),
                            "proguard-rules.pro",
                        )
                    }}
                }}

                compileOptions {{
                    sourceCompatibility = JavaVersion.VERSION_17
                    targetCompatibility = JavaVersion.VERSION_17
                }}

                kotlinOptions {{
                    jvmTarget = "17"
                }}

                buildFeatures {{
                    compose = true
                }}

                packaging {{
                    resources {{
                        excludes += "/META-INF/{{AL2.0,LGPL2.1}}"
                    }}
                }}

                room {{
                    schemaDirectory("$projectDir/schemas")
                }}
            }}

            protobuf {{
                protoc {{
                    artifact = libs.protobuf.protoc.get().toString()
                }}
                generateProtoTasks {{
                    all().forEach {{ task ->
                        task.builtins {{
                            register("java") {{
                                option("lite")
                            }}
                            register("kotlin") {{
                                option("lite")
                            }}
                        }}
                    }}
                }}
            }}

            dependencies {{
                implementation(libs.androidx.core.ktx)
                implementation(libs.androidx.lifecycle.runtime.ktx)
                implementation(libs.androidx.lifecycle.runtime.compose)
                implementation(libs.androidx.lifecycle.viewmodel.compose)
                implementation(libs.androidx.activity.compose)
                implementation(platform(libs.androidx.compose.bom))
                implementation(libs.androidx.ui)
                implementation(libs.androidx.ui.graphics)
                implementation(libs.androidx.ui.tooling.preview)
                implementation(libs.androidx.material3)
                implementation(libs.material)
                implementation(libs.androidx.navigation.compose)

                implementation(libs.hilt.android)
                implementation(libs.androidx.hilt.navigation.compose)
                implementation(libs.androidx.hilt.work)
                ksp(libs.dagger.hilt.compiler)
                ksp(libs.androidx.hilt.compiler)

                implementation(libs.androidx.room.runtime)
                implementation(libs.androidx.room.ktx)
                ksp(libs.androidx.room.compiler)

                implementation(libs.androidx.datastore)
                implementation(libs.protobuf.kotlin.lite)
                implementation(libs.androidx.work.runtime.ktx)

                implementation(libs.ktor.client.core)
                implementation(libs.ktor.client.android)
                implementation(libs.ktor.client.logging)
                implementation(libs.ktor.client.content.negotiation)
                implementation(libs.ktor.serialization.kotlinx.json)
                implementation(libs.kotlinx.serialization.json)

                testImplementation(libs.junit)
                androidTestImplementation(libs.androidx.junit)
                androidTestImplementation(libs.androidx.espresso.core)
                androidTestImplementation(platform(libs.androidx.compose.bom))
                androidTestImplementation(libs.androidx.ui.test.junit4)
                debugImplementation(libs.androidx.ui.tooling)
                debugImplementation(libs.androidx.ui.test.manifest)
            }}
            """
        ),
    )

    write_file(root / "app" / "proguard-rules.pro", "")


def create_android_resources(root: Path, project_name: str, base_package: str, features: list[str]) -> None:
    write_file(
        root / "app" / "src" / "main" / "AndroidManifest.xml",
        dedent(
            f"""
            <?xml version="1.0" encoding="utf-8"?>
            <manifest xmlns:android="http://schemas.android.com/apk/res/android">

                <application
                    android:name="{base_package}.app.MainApplication"
                    android:allowBackup="true"
                    android:label="@string/app_name"
                    android:supportsRtl="true"
                    android:theme="@style/Theme.SingleModuleStarter">
                    <activity
                        android:name="{base_package}.app.MainActivity"
                        android:exported="true">
                        <intent-filter>
                            <action android:name="android.intent.action.MAIN" />

                            <category android:name="android.intent.category.LAUNCHER" />
                        </intent-filter>
                    </activity>
                </application>

            </manifest>
            """
        ),
    )

    write_file(root / "app" / "src" / "main" / "res" / "values" / "strings.xml", strings_block(project_name, features))
    write_file(
        root / "app" / "src" / "main" / "res" / "values" / "themes.xml",
        dedent(
            """
            <?xml version="1.0" encoding="utf-8"?>
            <resources>
                <style name="Theme.SingleModuleStarter" parent="Theme.Material3.DayNight.NoActionBar" />
            </resources>
            """
        ),
    )
    write_file(
        root / "app" / "src" / "main" / "res" / "drawable" / "ic_top_level_selected.xml",
        dedent(
            """
            <?xml version="1.0" encoding="utf-8"?>
            <vector xmlns:android="http://schemas.android.com/apk/res/android"
                android:width="24dp"
                android:height="24dp"
                android:viewportWidth="24"
                android:viewportHeight="24">
                <path
                    android:fillColor="#2C6E49"
                    android:pathData="M12,3C7.03,3 3,7.03 3,12s4.03,9 9,9 9,-4.03 9,-9 -4.03,-9 -9,-9z" />
            </vector>
            """
        ),
    )
    write_file(
        root / "app" / "src" / "main" / "res" / "drawable" / "ic_top_level_unselected.xml",
        dedent(
            """
            <?xml version="1.0" encoding="utf-8"?>
            <vector xmlns:android="http://schemas.android.com/apk/res/android"
                android:width="24dp"
                android:height="24dp"
                android:viewportWidth="24"
                android:viewportHeight="24">
                <path
                    android:fillColor="#7A8B80"
                    android:pathData="M12,5C8.13,5 5,8.13 5,12s3.13,7 7,7 7,-3.13 7,-7 -3.13,-7 -7,-7z" />
            </vector>
            """
        ),
    )


def create_app_shell(root: Path, base_package: str, features: list[str]) -> None:
    base = root / "app" / "src" / "main" / "java" / package_to_path(base_package)
    first_feature = features[0]
    first_route_const = f"{resource_name(first_feature).upper()}_ROUTE"

    feature_imports = "\n".join(
        [
            f"import {base_package}.feature.{resource_name(feature)}.navigation.{resource_name(feature).upper()}_ROUTE"
            for feature in features
        ]
    )
    top_level_entries = ",\n".join(
        [
            f"    {resource_name(feature).upper()}(\n"
            f"        route = {resource_name(feature).upper()}_ROUTE,\n"
            "        selectedIconId = R.drawable.ic_top_level_selected,\n"
            "        unselectedIconId = R.drawable.ic_top_level_unselected,\n"
            f"        labelId = R.string.feature_{resource_name(feature)}_title,\n"
            "    )"
            for feature in features
        ]
    )

    feature_nav_imports = "\n".join(
        [
            f"import {base_package}.feature.{resource_name(feature)}.navigation.{camel_case(feature)}Screen"
            for feature in features
        ]
        + [
            f"import {base_package}.feature.{resource_name(feature)}.navigation.{resource_name(feature).upper()}_ROUTE"
            for feature in features
        ]
    )
    feature_screen_blocks = "\n".join(
        [
            feature_nav_host_block(feature, features)
            for feature in features
        ]
    )

    write_file(
        base / "app" / "MainApplication.kt",
        dedent(
            f"""
            package {base_package}.app

            import android.app.Application
            import androidx.hilt.work.HiltWorkerFactory
            import androidx.work.Configuration
            import dagger.hilt.android.HiltAndroidApp
            import javax.inject.Inject

            @HiltAndroidApp
            class MainApplication : Application(), Configuration.Provider {{
                @Inject
                lateinit var workerFactory: HiltWorkerFactory

                override val workManagerConfiguration: Configuration
                    get() = Configuration.Builder()
                        .setWorkerFactory(workerFactory)
                        .build()
            }}
            """
        ),
    )

    write_file(
        base / "app" / "MainActivity.kt",
        dedent(
            f"""
            package {base_package}.app

            import android.os.Bundle
            import androidx.activity.ComponentActivity
            import androidx.activity.compose.setContent
            import androidx.activity.enableEdgeToEdge
            import dagger.hilt.android.AndroidEntryPoint
            import {base_package}.app.ui.AppUiProviders
            import {base_package}.app.ui.MainApp

            @AndroidEntryPoint
            class MainActivity : ComponentActivity() {{
                override fun onCreate(savedInstanceState: Bundle?) {{
                    super.onCreate(savedInstanceState)
                    enableEdgeToEdge()

                    setContent {{
                        AppUiProviders {{
                            MainApp()
                        }}
                    }}
                }}
            }}
            """
        ),
    )

    write_file(
        base / "app" / "MainViewModel.kt",
        dedent(
            f"""
            package {base_package}.app

            import androidx.lifecycle.ViewModel
            import dagger.hilt.android.lifecycle.HiltViewModel
            import javax.inject.Inject
            import kotlinx.coroutines.flow.MutableStateFlow
            import kotlinx.coroutines.flow.StateFlow
            import kotlinx.coroutines.flow.asStateFlow

            data class MainUiState(
                val isReady: Boolean = true,
            )

            @HiltViewModel
            class MainViewModel @Inject constructor() : ViewModel() {{
                private val _uiState = MutableStateFlow(MainUiState())
                val uiState: StateFlow<MainUiState> = _uiState.asStateFlow()
            }}
            """
        ),
    )

    write_file(
        base / "app" / "navigation" / "AppState.kt",
        dedent(
            f"""
            package {base_package}.app.navigation

            import androidx.compose.runtime.Composable
            import androidx.compose.runtime.Stable
            import androidx.compose.runtime.getValue
            import androidx.compose.runtime.remember
            import androidx.navigation.NavDestination
            import androidx.navigation.NavDestination.Companion.hierarchy
            import androidx.navigation.NavGraph.Companion.findStartDestination
            import androidx.navigation.NavHostController
            import androidx.navigation.compose.currentBackStackEntryAsState
            import androidx.navigation.compose.rememberNavController

            @Stable
            class AppState(
                val navController: NavHostController,
            ) {{
                @Composable
                fun currentDestination(): NavDestination? {{
                    val backStackEntry by navController.currentBackStackEntryAsState()
                    return backStackEntry?.destination
                }}

                fun navigateToTopLevelDestination(destination: TopLevelDestination) {{
                    navController.navigate(destination.route) {{
                        popUpTo(navController.graph.findStartDestination().id) {{
                            saveState = true
                        }}
                        launchSingleTop = true
                        restoreState = true
                    }}
                }}

                fun isTopLevelDestinationInHierarchy(destination: TopLevelDestination): Boolean {{
                    return navController.currentDestination
                        ?.hierarchy
                        ?.any {{ it.route == destination.route }} == true
                }}
            }}

            @Composable
            fun rememberAppState(
                navController: NavHostController = rememberNavController(),
            ): AppState = remember(navController) {{
                AppState(navController = navController)
            }}
            """
        ),
    )

    write_file(
        base / "app" / "navigation" / "TopLevelDestination.kt",
        "\n".join(
            [
                f"package {base_package}.app.navigation",
                "",
                "import androidx.annotation.DrawableRes",
                "import androidx.annotation.StringRes",
                f"import {base_package}.R",
                feature_imports,
                "",
                "enum class TopLevelDestination(",
                "    val route: String,",
                "    @DrawableRes val selectedIconId: Int,",
                "    @DrawableRes val unselectedIconId: Int,",
                "    @StringRes val labelId: Int,",
                ") {",
                top_level_entries,
                "}",
            ]
        ),
    )

    write_file(
        base / "app" / "navigation" / "MainNavHost.kt",
        "\n".join(
            [
                f"package {base_package}.app.navigation",
                "",
                "import androidx.compose.runtime.Composable",
                "import androidx.compose.ui.Modifier",
                "import androidx.navigation.NavHostController",
                "import androidx.navigation.compose.NavHost",
                f"import {base_package}.R",
                f"import {base_package}.core.model.FeatureDestination",
                feature_nav_imports,
                "",
                "@Composable",
                "fun MainNavHost(",
                "    navController: NavHostController,",
                "    modifier: Modifier = Modifier,",
                ") {",
                "    NavHost(",
                "        navController = navController,",
                f"        startDestination = {first_route_const},",
                "        modifier = modifier,",
                "    ) {",
                feature_screen_blocks,
                "    }",
                "}",
            ]
        ),
    )

    write_file(
        base / "app" / "ui" / "AppUiProviders.kt",
        dedent(
            f"""
            package {base_package}.app.ui

            import androidx.compose.runtime.Composable
            import {base_package}.core.theme.SingleModuleStarterTheme

            @Composable
            fun AppUiProviders(
                content: @Composable () -> Unit,
            ) {{
                SingleModuleStarterTheme {{
                    content()
                }}
            }}
            """
        ),
    )

    write_file(
        base / "app" / "ui" / "MainApp.kt",
        dedent(
            f"""
            package {base_package}.app.ui

            import androidx.compose.foundation.layout.Box
            import androidx.compose.foundation.layout.fillMaxSize
            import androidx.compose.foundation.layout.padding
            import androidx.compose.material3.CenterAlignedTopAppBar
            import androidx.compose.material3.CircularProgressIndicator
            import androidx.compose.material3.ExperimentalMaterial3Api
            import androidx.compose.material3.Icon
            import androidx.compose.material3.NavigationBar
            import androidx.compose.material3.NavigationBarItem
            import androidx.compose.material3.Scaffold
            import androidx.compose.material3.Text
            import androidx.compose.runtime.Composable
            import androidx.compose.runtime.getValue
            import androidx.compose.ui.Alignment
            import androidx.compose.ui.Modifier
            import androidx.compose.ui.res.painterResource
            import androidx.compose.ui.res.stringResource
            import androidx.hilt.lifecycle.viewmodel.compose.hiltViewModel
            import androidx.lifecycle.compose.collectAsStateWithLifecycle
            import androidx.navigation.NavDestination.Companion.hierarchy
            import {base_package}.R
            import {base_package}.app.MainViewModel
            import {base_package}.app.navigation.MainNavHost
            import {base_package}.app.navigation.TopLevelDestination
            import {base_package}.app.navigation.rememberAppState

            @OptIn(ExperimentalMaterial3Api::class)
            @Composable
            fun MainApp(
                viewModel: MainViewModel = hiltViewModel(),
            ) {{
                val uiState by viewModel.uiState.collectAsStateWithLifecycle()
                val appState = rememberAppState()
                val currentDestination = appState.currentDestination()
                val labelRes = TopLevelDestination.entries
                    .firstOrNull {{ destination -> currentDestination?.hierarchy?.any {{ it.route == destination.route }} == true }}
                    ?.labelId
                    ?: R.string.app_name

                Scaffold(
                    topBar = {{
                        CenterAlignedTopAppBar(
                            title = {{
                                Text(text = stringResource(labelRes))
                            }},
                        )
                    }},
                    bottomBar = {{
                        if (TopLevelDestination.entries.size > 1) {{
                            NavigationBar {{
                                TopLevelDestination.entries.forEach {{ destination ->
                                    val selected = currentDestination?.hierarchy?.any {{ it.route == destination.route }} == true
                                    NavigationBarItem(
                                        selected = selected,
                                        onClick = {{ appState.navigateToTopLevelDestination(destination) }},
                                        icon = {{
                                            Icon(
                                                painter = painterResource(
                                                    id = if (selected) destination.selectedIconId else destination.unselectedIconId,
                                                ),
                                                contentDescription = stringResource(destination.labelId),
                                            )
                                        }},
                                        label = {{
                                            Text(text = stringResource(destination.labelId))
                                        }},
                                    )
                                }}
                            }}
                        }}
                    }},
                ) {{ innerPadding ->
                    if (uiState.isReady) {{
                        MainNavHost(
                            navController = appState.navController,
                            modifier = Modifier.padding(innerPadding),
                        )
                    }} else {{
                        Box(
                            modifier = Modifier
                                .fillMaxSize()
                                .padding(innerPadding),
                            contentAlignment = Alignment.Center,
                        ) {{
                            CircularProgressIndicator()
                        }}
                    }}
                }}
            }}
            """
        ),
    )


def feature_nav_host_block(feature: str, all_features: list[str]) -> str:
    camel = camel_case(feature)
    return "\n".join(
        [
            f"        {camel}Screen()",
        ]
    )


def create_core_files(root: Path, base_package: str) -> None:
    base = root / "app" / "src" / "main" / "java" / package_to_path(base_package)

    remove_file_if_exists(base / "core" / "datastore" / "UserPreferencesDataStore.kt")
    remove_file_if_exists(base / "core" / "network" / "NetworkConfig.kt")
    remove_file_if_exists(root / "app" / "src" / "main" / "proto" / "user_preferences.proto")
    remove_file_if_exists(root / "app" / "src" / "main" / "proto" / "app_settings.proto")

    write_file(
        base / "core" / "model" / "FeatureDestination.kt",
        dedent(
            f"""
package {base_package}.core.model

import androidx.annotation.StringRes

data class FeatureDestination(
    val route: String,
    @StringRes val titleRes: Int,
)
            """
        ),
    )

    write_file(
        base / "core" / "model" / "AppBootstrapState.kt",
        dedent(
            f"""
package {base_package}.core.model

data class AppBootstrapState(
    val networkMessage: String,
    val onboardingCompleted: Boolean,
    val cachedItemCount: Int,
    val refreshedAtMillis: Long,
)
            """
        ),
    )

    write_file(
        base / "core" / "theme" / "Color.kt",
        dedent(
            f"""
package {base_package}.core.theme

import androidx.compose.ui.graphics.Color

val SeedGreen = Color(0xFF2C6E49)
val SoftGreen = Color(0xFFD8F3DC)
val DeepInk = Color(0xFF163020)
val DeepForest = Color(0xFF0F2418)
val WarmSurface = Color(0xFFF7FBF5)
            """
        ),
    )

    write_file(
        base / "core" / "theme" / "Font.kt",
        dedent(
            f"""
package {base_package}.core.theme

import androidx.compose.ui.text.font.Font
import androidx.compose.ui.text.font.FontFamily
import {base_package}.R

val beproSemibold = FontFamily(
    Font(R.font.bevietnampro_semibold),
)

val beproMedium = FontFamily(
    Font(R.font.bevietnampro_medium),
)

val beproRegular = FontFamily(
    Font(R.font.bevietnampro_regular),
)
            """
        ),
    )

    write_file(
        base / "core" / "theme" / "Type.kt",
        dedent(
            f"""
package {base_package}.core.theme

import androidx.compose.material3.Typography
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.unit.sp

val AppTypography = Typography()

val Typography.TitleLarge1: TextStyle
    get() = TextStyle(
        fontFamily = beproSemibold,
        fontSize = 22.sp,
        lineHeight = 30.sp,
        letterSpacing = 0.15.sp,
    )

val Typography.TitleLarge2: TextStyle
    get() = TextStyle(
        fontFamily = beproSemibold,
        fontSize = 20.sp,
        lineHeight = 30.sp,
        letterSpacing = 0.15.sp,
    )

val Typography.TitleLarge3: TextStyle
    get() = TextStyle(
        fontFamily = beproMedium,
        fontSize = 20.sp,
        lineHeight = 30.sp,
        letterSpacing = 0.15.sp,
    )

val Typography.Title1: TextStyle
    get() = TextStyle(
        fontFamily = beproSemibold,
        fontSize = 18.sp,
        lineHeight = 27.sp,
        letterSpacing = 0.15.sp,
    )

val Typography.Title2: TextStyle
    get() = TextStyle(
        fontFamily = beproMedium,
        fontSize = 18.sp,
        lineHeight = 27.sp,
        letterSpacing = 0.15.sp,
    )

val Typography.Button1: TextStyle
    get() = TextStyle(
        fontFamily = beproSemibold,
        fontSize = 16.sp,
        lineHeight = 24.sp,
        letterSpacing = 0.5.sp,
    )

val Typography.Button2: TextStyle
    get() = TextStyle(
        fontFamily = beproSemibold,
        fontSize = 14.sp,
        lineHeight = 21.sp,
        letterSpacing = 0.5.sp,
    )

val Typography.Body1: TextStyle
    get() = TextStyle(
        fontFamily = beproMedium,
        fontSize = 16.sp,
        lineHeight = 24.sp,
        letterSpacing = 0.5.sp,
    )

val Typography.Body2: TextStyle
    get() = TextStyle(
        fontFamily = beproRegular,
        fontSize = 16.sp,
        lineHeight = 24.sp,
        letterSpacing = 0.5.sp,
    )

val Typography.Body3: TextStyle
    get() = TextStyle(
        fontFamily = beproRegular,
        fontSize = 14.sp,
        lineHeight = 21.sp,
        letterSpacing = 0.25.sp,
    )

val Typography.Body4: TextStyle
    get() = TextStyle(
        fontFamily = beproMedium,
        fontSize = 14.sp,
        lineHeight = 21.sp,
        letterSpacing = 0.25.sp,
    )

val Typography.Label1: TextStyle
    get() = TextStyle(
        fontFamily = beproSemibold,
        fontSize = 12.sp,
        lineHeight = 18.sp,
        letterSpacing = 0.5.sp,
    )

val Typography.Label2: TextStyle
    get() = TextStyle(
        fontFamily = beproMedium,
        fontSize = 12.sp,
        lineHeight = 18.sp,
        letterSpacing = 0.5.sp,
    )

val Typography.Label4: TextStyle
    get() = TextStyle(
        fontFamily = beproRegular,
        fontSize = 12.sp,
        lineHeight = 18.sp,
        letterSpacing = 0.5.sp,
    )

val Typography.Label3: TextStyle
    get() = TextStyle(
        fontFamily = beproMedium,
        fontSize = 11.sp,
        lineHeight = 16.5.sp,
        letterSpacing = 0.5.sp,
    )

val Typography.Label5: TextStyle
    get() = TextStyle(
        fontFamily = beproRegular,
        fontSize = 11.sp,
        lineHeight = 16.5.sp,
        letterSpacing = 0.5.sp,
    )
            """
        ),
    )

    copy_file(
        FONT_ASSETS_DIR / "bevietnampro_semibold.ttf",
        root / "app" / "src" / "main" / "res" / "font" / "bevietnampro_semibold.ttf",
    )
    copy_file(
        FONT_ASSETS_DIR / "bevietnampro_medium.ttf",
        root / "app" / "src" / "main" / "res" / "font" / "bevietnampro_medium.ttf",
    )
    copy_file(
        FONT_ASSETS_DIR / "bevietnampro_regular.ttf",
        root / "app" / "src" / "main" / "res" / "font" / "bevietnampro_regular.ttf",
    )

    write_file(
        base / "core" / "theme" / "Theme.kt",
        dedent(
            f"""
package {base_package}.core.theme

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.dynamicDarkColorScheme
import androidx.compose.material3.dynamicLightColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.platform.LocalContext
import android.os.Build
import androidx.compose.foundation.isSystemInDarkTheme

private val LightColors = lightColorScheme(
    primary = SeedGreen,
    secondary = DeepInk,
    background = WarmSurface,
    surface = WarmSurface,
)

private val DarkColors = darkColorScheme(
    primary = SoftGreen,
    secondary = SeedGreen,
    background = DeepForest,
    surface = DeepForest,
)

@Composable
fun SingleModuleStarterTheme(
    useDarkTheme: Boolean = isSystemInDarkTheme(),
    useDynamicColor: Boolean = true,
    content: @Composable () -> Unit,
) {{
    val context = LocalContext.current
    val colorScheme = when {{
        useDynamicColor && Build.VERSION.SDK_INT >= Build.VERSION_CODES.S && useDarkTheme ->
            dynamicDarkColorScheme(context)
        useDynamicColor && Build.VERSION.SDK_INT >= Build.VERSION_CODES.S ->
            dynamicLightColorScheme(context)
        useDarkTheme -> DarkColors
        else -> LightColors
    }}

    MaterialTheme(
        colorScheme = colorScheme,
        typography = AppTypography,
        content = content,
    )
}}
            """
        ),
    )

    write_file(
        base / "core" / "ui" / "component" / "FeatureActionList.kt",
        dedent(
            f"""
            package {base_package}.core.ui.component

            import androidx.compose.runtime.Composable
            import {base_package}.core.model.FeatureDestination

            @Composable
            fun FeatureActionList(
                destinations: List<FeatureDestination>,
                onNavigate: (String) -> Unit,
                onBackClick: (() -> Unit)?,
            ) {{
            }}
            """
        ),
    )

    write_file(
        base / "core" / "network" / "NetworkClients.kt",
        dedent(
            f"""
package {base_package}.core.network

import io.ktor.client.HttpClient
import io.ktor.client.engine.android.Android
import io.ktor.client.plugins.HttpTimeout
import io.ktor.client.plugins.contentnegotiation.ContentNegotiation
import io.ktor.client.plugins.defaultRequest
import io.ktor.serialization.kotlinx.json.json
import kotlinx.serialization.json.Json

internal object NetworkClients {{
    private fun createClient(baseUrl: String): HttpClient {{
        return HttpClient(Android) {{
            defaultRequest {{
                url(baseUrl)
            }}
            install(HttpTimeout) {{
                requestTimeoutMillis = 60_000
            }}
            install(ContentNegotiation) {{
                json(
                    Json {{
                        ignoreUnknownKeys = true
                        encodeDefaults = true
                    }},
                )
            }}
        }}
    }}

    const val startupInfoUrl = "https://api.example.com/v1/startup"
    const val healthCheckUrl = "https://api.example.com/v1/health"

    val startupClient = createClient(startupInfoUrl)
    val healthCheckClient = createClient(healthCheckUrl)
}}
            """
        ),
    )

    write_file(
        base / "core" / "network" / "NetworkDataSource.kt",
        dedent(
            f"""
package {base_package}.core.network

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

object NetworkDataSource {{
    suspend fun fetchStartupMessage(): Result<String> = withContext(Dispatchers.IO) {{
        runCatching {{
            val startupEngine = NetworkClients.startupClient.engine::class.simpleName ?: "UnknownEngine"
            "Startup API: ${{NetworkClients.startupInfoUrl}} | Health API: ${{NetworkClients.healthCheckUrl}} | engine: $startupEngine"
        }}
    }}
}}
            """
        ),
    )

    write_file(
        base / "core" / "network" / "di" / "NetworkModule.kt",
        dedent(
            f"""
            package {base_package}.core.network.di

            import dagger.Module
            import dagger.Provides
            import dagger.hilt.InstallIn
            import dagger.hilt.components.SingletonComponent
            import {base_package}.core.network.NetworkDataSource
            import javax.inject.Singleton

            @Module
            @InstallIn(SingletonComponent::class)
            object NetworkModule {{
                @Provides
                @Singleton
                fun provideNetworkDataSource(): NetworkDataSource = NetworkDataSource
            }}
            """
        ),
    )

    write_file(
        base / "core" / "data" / "repository" / "AppRepository.kt",
        dedent(
            f"""
package {base_package}.core.data.repository

import {base_package}.core.model.AppBootstrapState

interface AppRepository {{
    suspend fun refreshAppBootstrap(): Result<AppBootstrapState>
}}
            """
        ),
    )

    write_file(
        base / "core" / "data" / "impl" / "AppRepositoryImpl.kt",
        dedent(
            f"""
package {base_package}.core.data.impl

import {base_package}.core.data.repository.AppRepository
import {base_package}.core.database.dao.SampleDao
import {base_package}.core.datastore.AppSettingsDataStore
import {base_package}.core.model.AppBootstrapState
import {base_package}.core.network.NetworkDataSource
import javax.inject.Inject

class AppRepositoryImpl @Inject constructor(
    private val networkDataSource: NetworkDataSource,
    private val appSettingsDataStore: AppSettingsDataStore,
    private val sampleDao: SampleDao,
) : AppRepository {{
    override suspend fun refreshAppBootstrap(): Result<AppBootstrapState> = runCatching {{
        val networkMessage = networkDataSource.fetchStartupMessage()
            .getOrElse {{ throwable -> "Network unavailable: ${{throwable.message ?: "unknown error"}}" }}
        val settings = appSettingsDataStore.getAppSettings()
        val cachedItemCount = sampleDao.getItemCount()

        AppBootstrapState(
            networkMessage = networkMessage,
            onboardingCompleted = settings.onboardingCompleted,
            cachedItemCount = cachedItemCount,
            refreshedAtMillis = System.currentTimeMillis(),
        )
    }}
}}
            """
        ),
    )

    write_file(
        base / "core" / "data" / "di" / "DataModule.kt",
        dedent(
            f"""
            package {base_package}.core.data.di

            import dagger.Binds
            import dagger.Module
            import dagger.hilt.InstallIn
            import dagger.hilt.components.SingletonComponent
            import {base_package}.core.data.impl.AppRepositoryImpl
            import {base_package}.core.data.repository.AppRepository
            import javax.inject.Singleton

            @Module
            @InstallIn(SingletonComponent::class)
            abstract class DataModule {{
                @Binds
                @Singleton
                abstract fun bindAppRepository(
                    impl: AppRepositoryImpl,
                ): AppRepository
            }}
            """
        ),
    )

    write_file(
        base / "core" / "database" / "model" / "SampleEntity.kt",
        dedent(
            f"""
            package {base_package}.core.database.model

            import androidx.room.Entity
            import androidx.room.PrimaryKey

            @Entity(tableName = "sample_items")
            data class SampleEntity(
                @PrimaryKey val id: String,
                val title: String,
                val createdAt: Long,
            )
            """
        ),
    )

    write_file(
        base / "core" / "database" / "dao" / "SampleDao.kt",
        dedent(
            f"""
package {base_package}.core.database.dao

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import {base_package}.core.database.model.SampleEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface SampleDao {{
    @Query("SELECT * FROM sample_items ORDER BY createdAt DESC")
    fun observeItems(): Flow<List<SampleEntity>>

    @Query("SELECT COUNT(*) FROM sample_items")
    suspend fun getItemCount(): Int

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsert(item: SampleEntity)
}}
            """
        ),
    )

    write_file(
        base / "core" / "database" / "AppDatabase.kt",
        dedent(
            f"""
package {base_package}.core.database

import androidx.room.Database
import androidx.room.RoomDatabase
import {base_package}.core.database.dao.SampleDao
import {base_package}.core.database.model.SampleEntity

@Database(
    entities = [SampleEntity::class],
    version = 1,
    exportSchema = false,
)
abstract class AppDatabase : RoomDatabase() {{
    abstract fun sampleDao(): SampleDao
}}
            """
        ),
    )

    write_file(
        base / "core" / "database" / "di" / "DatabaseModule.kt",
        dedent(
            f"""
            package {base_package}.core.database.di

            import android.content.Context
            import androidx.room.Room
            import dagger.Module
            import dagger.Provides
            import dagger.hilt.InstallIn
            import dagger.hilt.android.qualifiers.ApplicationContext
            import dagger.hilt.components.SingletonComponent
            import {base_package}.core.database.AppDatabase
            import {base_package}.core.database.dao.SampleDao
            import javax.inject.Singleton

            @Module
            @InstallIn(SingletonComponent::class)
            object DatabaseModule {{
                @Provides
                @Singleton
                fun provideAppDatabase(
                    @ApplicationContext context: Context,
                ): AppDatabase = Room.databaseBuilder(
                    context,
                    AppDatabase::class.java,
                    "single-module-starter.db",
                ).build()

                @Provides
                fun provideSampleDao(database: AppDatabase): SampleDao = database.sampleDao()
            }}
            """
        ),
    )

    write_file(
        base / "core" / "datastore" / "AppSettingsDataStore.kt",
        dedent(
            f"""
            package {base_package}.core.datastore

            import android.content.Context
            import androidx.datastore.core.CorruptionException
            import androidx.datastore.core.DataStore
            import androidx.datastore.core.Serializer
            import androidx.datastore.dataStore
            import dagger.hilt.android.qualifiers.ApplicationContext
            import java.io.IOException
            import java.io.InputStream
            import java.io.OutputStream
            import javax.inject.Inject
            import javax.inject.Singleton
            import kotlinx.coroutines.flow.Flow
            import kotlinx.coroutines.flow.catch
            import kotlinx.coroutines.flow.first
            import kotlinx.coroutines.flow.map

            data class AppSettingsState(
                val onboardingCompleted: Boolean = false,
            )

            @Singleton
            class AppSettingsDataStore @Inject constructor(
                @ApplicationContext context: Context,
            ) {{
                private val appContext = context.applicationContext
                private val appSettingsDataStore: DataStore<AppSettingsProto> = appContext.appSettingsDataStore

                val appSettings: Flow<AppSettingsState> = appSettingsDataStore.data
                    .catch {{ error ->
                        if (error is IOException) {{
                            emit(AppSettingsProto.getDefaultInstance())
                        }} else {{
                            throw error
                        }}
                    }}
                    .map {{ settings ->
                        AppSettingsState(
                            onboardingCompleted = settings.onboardingCompleted,
                        )
                    }}

                suspend fun getAppSettings(): AppSettingsState = appSettings.first()

                suspend fun updateOnboardingCompleted(value: Boolean) {{
                    appSettingsDataStore.updateData {{ current ->
                        current.toBuilder()
                            .setOnboardingCompleted(value)
                            .build()
                    }}
                }}
            }}

            private object AppSettingsProtoSerializer : Serializer<AppSettingsProto> {{
                override val defaultValue: AppSettingsProto = AppSettingsProto.getDefaultInstance()

                override suspend fun readFrom(input: InputStream): AppSettingsProto {{
                    return try {{
                        AppSettingsProto.parseFrom(input)
                    }} catch (error: IOException) {{
                        throw CorruptionException("Cannot read app settings proto.", error)
                    }}
                }}

                override suspend fun writeTo(t: AppSettingsProto, output: OutputStream) {{
                    t.writeTo(output)
                }}
            }}

            private val Context.appSettingsDataStore: DataStore<AppSettingsProto> by dataStore(
                fileName = "app_settings.pb",
                serializer = AppSettingsProtoSerializer,
            )
            """
        ),
    )

    write_file(
        root / "app" / "src" / "main" / "proto" / "core" / "datastore" / "app_settings.proto",
        dedent(
            f"""
            syntax = "proto3";

            option java_package = "{base_package}.core.datastore";
            option java_multiple_files = true;

            message AppSettingsProto {{
              bool onboarding_completed = 1;
            }}
            """
        ),
    )

    write_file(
        base / "core" / "worker" / "SyncWorker.kt",
        dedent(
            f"""
package {base_package}.core.worker

import android.content.Context
import androidx.hilt.work.HiltWorker
import androidx.work.CoroutineWorker
import androidx.work.WorkerParameters
import dagger.assisted.Assisted
import dagger.assisted.AssistedInject
import {base_package}.core.data.repository.AppRepository

@HiltWorker
class SyncWorker @AssistedInject constructor(
    @Assisted appContext: Context,
    @Assisted params: WorkerParameters,
    private val repository: AppRepository,
) : CoroutineWorker(appContext, params) {{
    override suspend fun doWork(): Result {{
        return repository.refreshAppBootstrap()
            .fold(
                onSuccess = {{ Result.success() }},
                onFailure = {{ Result.retry() }},
            )
    }}
}}
            """
        ),
    )
def create_feature_files(root: Path, base_package: str, features: list[str]) -> None:
    base = root / "app" / "src" / "main" / "java" / package_to_path(base_package)
    for feature in features:
        key = resource_name(feature)
        pascal = pascal_case(feature)
        namespace = f"{base_package}.feature.{key}"
        route_const = f"{key.upper()}_ROUTE"

        write_file(
            base / "feature" / key / f"{pascal}Screen.kt",
            dedent(
                f"""
                package {namespace}

                import androidx.compose.runtime.Composable
                import androidx.compose.ui.Modifier
                import androidx.hilt.lifecycle.viewmodel.compose.hiltViewModel
                import androidx.lifecycle.compose.collectAsStateWithLifecycle
                import {namespace}.component.{pascal}Content

                @Composable
                fun {pascal}Route(
                    viewModel: {pascal}ViewModel = hiltViewModel(),
                ) {{
                    val uiState = viewModel.uiState.collectAsStateWithLifecycle().value

                    {pascal}Screen(
                        title = uiState.title,
                    )
                }}

                @Composable
                fun {pascal}Screen(
                    title: String,
                    modifier: Modifier = Modifier,
                ) {{
                    {pascal}Content(
                        title = title,
                        modifier = modifier,
                    )
                }}
                """
            ),
        )

        write_file(
            base / "feature" / key / f"{pascal}ViewModel.kt",
            dedent(
                f"""
                package {namespace}

                import androidx.lifecycle.ViewModel
                import dagger.hilt.android.lifecycle.HiltViewModel
                import javax.inject.Inject
                import kotlinx.coroutines.flow.MutableStateFlow
                import kotlinx.coroutines.flow.StateFlow
                import kotlinx.coroutines.flow.asStateFlow

                data class {pascal}UiState(
                    val title: String = "",
                )

                @HiltViewModel
                class {pascal}ViewModel @Inject constructor() : ViewModel() {{
                    private val _uiState = MutableStateFlow(
                        {pascal}UiState(title = ""),
                    )
                    val uiState: StateFlow<{pascal}UiState> = _uiState.asStateFlow()

                    init {{
                        _uiState.value = {pascal}UiState(title = "{humanize(feature)}")
                    }}
                }}
                """
            ),
        )

        write_file(
            base / "feature" / key / "component" / f"{pascal}Content.kt",
            dedent(
                f"""
                package {namespace}.component

                import androidx.compose.foundation.layout.Box
                import androidx.compose.foundation.layout.fillMaxSize
                import androidx.compose.runtime.Composable
                import androidx.compose.ui.Modifier

                @Composable
                fun {pascal}Content(
                    title: String,
                    modifier: Modifier = Modifier,
                ) {{
                    Box(
                        modifier = modifier.fillMaxSize(),
                    )
                }}
                """
            ),
        )

        write_file(
            base / "feature" / key / "navigation" / f"{pascal}Navigation.kt",
            dedent(
                f"""
                package {namespace}.navigation

                import androidx.navigation.NavController
                import androidx.navigation.NavGraphBuilder
                import androidx.navigation.NavOptions
                import androidx.navigation.compose.composable
                import {namespace}.{pascal}Route

                const val {route_const} = "{key}"

                fun NavController.navigateTo{pascal}(navOptions: NavOptions? = null) {{
                    navigate(
                        route = {route_const},
                        navOptions = navOptions,
                    )
                }}

                fun NavGraphBuilder.{camel_case(feature)}Screen() {{
                    composable(route = {route_const}) {{
                        {pascal}Route()
                    }}
                }}
                """
            ),
        )

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scaffold a single-module Android project.")
    parser.add_argument("--project-name", required=True, help="Project name")
    parser.add_argument("--package", required=True, dest="base_package", help="Base package name")
    parser.add_argument("--features", default="home,settings", help="Comma-separated starter features")
    parser.add_argument("--output", required=False, help="Output directory. Defaults to the current working directory.")
    parser.add_argument("--minimal", action="store_true", help="Create only the shell and core folders")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = Path(args.output).expanduser().resolve() if args.output else Path.cwd().resolve()
    root.mkdir(parents=True, exist_ok=True)

    features = [] if args.minimal else [item.strip() for item in args.features.split(",") if item.strip()]
    if not features:
        features = ["home"]

    create_root_files(root, args.project_name)
    create_app_build_file(root, args.base_package)
    create_android_resources(root, args.project_name, args.base_package, features)
    create_app_shell(root, args.base_package, features)
    create_core_files(root, args.base_package)
    create_feature_files(root, args.base_package, features)

    print(f"Scaffolded project at: {root}")
    print(f"Package: {args.base_package}")
    print(f"Features: {', '.join(features)}")


if __name__ == "__main__":
    main()
