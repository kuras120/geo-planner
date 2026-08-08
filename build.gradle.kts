allprojects {
    group = "com.simplydevit"
    version = "0.0.1-SNAPSHOT"

    repositories {
        mavenCentral()
    }
}

tasks.register("buildAll") {
    group = "build"

    dependsOn(":backend:build")
}

tasks.register("cleanAll") {
    group = "build"

    dependsOn(":backend:clean")
}
