package com.simplydevit.geoplanner

import jakarta.validation.Valid
import org.springframework.validation.annotation.Validated
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.PathVariable
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestBody
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController

@Validated
@RestController
@RequestMapping("/test")
class TestController(private val testService: TestService) {

    @GetMapping("/hello/{name}")
    fun hello(@PathVariable name: String): TestDto = testService.hello(name)

    @PostMapping("/hello")
    fun hello(@Valid @RequestBody dto: TestDto): TestDto = testService.hello(dto.helloName)
}
