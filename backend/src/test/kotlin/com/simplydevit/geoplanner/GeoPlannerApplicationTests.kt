package com.simplydevit.geoplanner

import io.kotest.core.spec.style.FunSpec
import io.kotest.matchers.shouldBe
import org.springframework.boot.health.actuate.endpoint.HealthEndpoint
import org.springframework.boot.health.contributor.Status
import org.springframework.boot.test.context.SpringBootTest

@SpringBootTest
class GeoPlannerApplicationTests(
    private val healthEndpoint: HealthEndpoint,
) : FunSpec({

    test("Application context loads") {
        healthEndpoint.health().status shouldBe Status.UP
    }
})
