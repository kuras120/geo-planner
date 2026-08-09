package com.simplydevit.geoplanner

import io.github.oshai.kotlinlogging.KotlinLogging
import org.springframework.stereotype.Service

private val logger = KotlinLogging.logger {}
private val forbiddenNames: Set<String> = setOf("error", "Wojtek")

@Service
class TestService {
    fun hello(name: String): TestDto {
        if (forbiddenNames.contains(name)) {
            logger.info { "This name is forbidden, {name=$name}" }
            throw IllegalArgumentException("Forbidden name")
        }
        return TestDto("Hello, $name!")
    }
}
