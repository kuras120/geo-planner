pluginManagement {
    plugins {
        kotlin("plugin.lombok") version "2.3.21"
        kotlin("kapt") version "2.3.21"
    }
}
rootProject.name = "geo-planner"

include("backend", "frontend")
