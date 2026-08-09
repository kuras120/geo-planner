package com.simplydevit.geoplanner

import jakarta.validation.constraints.NotBlank

data class TestDto(
    @field:NotBlank val helloName: String,
)
