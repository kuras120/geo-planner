pluginManagement {
    plugins {
        kotlin("jvm") version "2.3.21"
        kotlin("plugin.spring") version "2.3.21"
        kotlin("plugin.jpa") version "2.3.21"
        kotlin("kapt") version "2.3.21"

        id("org.springframework.boot") version "4.1.0"
        id("io.spring.dependency-management") version "1.1.7"
        id("org.jlleitschuh.gradle.ktlint") version "14.2.0"
    }
}

rootProject.name = "geo-planner"
include("backend")
