package com.simplydevit.geoplanner

import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.PathVariable
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController

@RestController
@RequestMapping("/test")
class TestController(private val testService: TestService) {

    @GetMapping("/hello/{name}")
    fun hello(@PathVariable name: String): TestDto = testService.hello(name)
}
