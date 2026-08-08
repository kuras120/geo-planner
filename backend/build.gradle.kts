plugins {
    kotlin("jvm")
    kotlin("plugin.spring")
    kotlin("plugin.jpa")
    kotlin("kapt")

    id("org.springframework.boot")
    id("io.spring.dependency-management")
    id("org.jlleitschuh.gradle.ktlint")
}

description = "geo-planner-api"

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(25)
    }
}

dependencies {
    // Spring Boot
    implementation(platform(libs.logbookBom))
    implementation("org.springframework.boot:spring-boot-starter-actuator")
    implementation("org.springframework.boot:spring-boot-starter-opentelemetry")
    implementation("org.springframework.boot:spring-boot-starter-data-jpa")
    implementation("org.springframework.boot:spring-boot-starter-liquibase")
    implementation("org.springframework.boot:spring-boot-starter-restclient")
    implementation("org.springframework.boot:spring-boot-starter-webmvc")
    implementation("org.springframework.boot:spring-boot-starter-validation")
    implementation("org.zalando:logbook-spring-boot-starter")

    // Other deps
    implementation("org.jetbrains.kotlin:kotlin-reflect")
    implementation("tools.jackson.module:jackson-module-kotlin")
    implementation(libs.kotlinLogging)

    developmentOnly("org.springframework.boot:spring-boot-devtools")
    developmentOnly("org.springframework.boot:spring-boot-docker-compose")
    runtimeOnly("org.postgresql:postgresql")

    kapt("org.springframework.boot:spring-boot-configuration-processor")

    // Spring Boot test
    testImplementation("org.springframework.boot:spring-boot-starter-actuator-test")
    testImplementation("org.springframework.boot:spring-boot-starter-data-jpa-test")
    testImplementation("org.springframework.boot:spring-boot-starter-liquibase-test")
    testImplementation("org.springframework.boot:spring-boot-starter-restclient-test")
    testImplementation("org.springframework.boot:spring-boot-starter-webmvc-test")

    // Other test deps
    testImplementation(platform(libs.kotestBom))
    testImplementation("io.kotest:kotest-runner-junit5")
    testImplementation("io.kotest:kotest-assertions-core")
    testImplementation("io.kotest:kotest-extensions-spring")

    testRuntimeOnly("com.h2database:h2")

    testRuntimeOnly("org.junit.platform:junit-platform-launcher")
    testImplementation(kotlin("test"))
}

kotlin {
    compilerOptions {
        freeCompilerArgs.addAll("-Xjsr305=strict", "-Xannotation-default-target=param-property")
    }
}

tasks.withType<Test>().configureEach {
    useJUnitPlatform()
}

tasks.named("check") {
    dependsOn("ktlintCheck")
}
