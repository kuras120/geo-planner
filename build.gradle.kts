plugins {
    // apply false -> don't apply to the project's root
    alias(libs.plugins.kotlinJvm) apply false
    alias(libs.plugins.kotlinSpring) apply false
    alias(libs.plugins.kotlinJpa) apply false
    alias(libs.plugins.kotlinKapt) apply false

    alias(libs.plugins.springBoot) apply false
    alias(libs.plugins.springDependencyManagement) apply false
}

allprojects {
    group = "com.simplydevit"
    version = "0.0.1-SNAPSHOT"

    repositories {
        mavenCentral()
    }
}

tasks.register("buildAll") {
    group = "build"
    description = "Builds backend and frontend"

    dependsOn(":backend:build", ":frontend:build")
}

tasks.register("cleanAll") {
    group = "build"

    dependsOn(":backend:build", ":frontend:clean")
}
