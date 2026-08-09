plugins {
    // this is necessary to avoid the plugins to be loaded multiple times
    // in each subproject's classloader
    alias(libs.plugins.kotlin.jvm) apply false
    alias(libs.plugins.kotlin.spring) apply false
    alias(libs.plugins.kotlin.jpa) apply false
    alias(libs.plugins.kotlin.kapt) apply false
    alias(libs.plugins.spring.boot) apply false
    alias(libs.plugins.spring.dependency.management) apply false
    alias(libs.plugins.ktlint) apply false
}

allprojects {
    group = "com.simplydevit"
    version = "0.0.1-SNAPSHOT"
}

tasks.register("buildAll") {
    group = "build"

    dependsOn(":backend:build")
}

tasks.register("cleanAll") {
    group = "build"

    dependsOn(":backend:clean")
}
