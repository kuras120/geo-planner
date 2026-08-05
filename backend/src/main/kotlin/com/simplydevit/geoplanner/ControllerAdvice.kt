package com.simplydevit.geoplanner

import org.springframework.http.HttpStatus
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.ExceptionHandler
import org.springframework.web.bind.annotation.RestControllerAdvice

@RestControllerAdvice
class ControllerAdvice {

    @ExceptionHandler(Exception::class)
    fun handleError(ex: Exception): ResponseEntity<ErrorDto> {
        val error = ErrorDto(ex.message ?: "Unknown error")
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(error)
    }
}
