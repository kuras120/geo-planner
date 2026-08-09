package com.simplydevit.geoplanner

import org.springframework.http.HttpStatus
import org.springframework.web.bind.MethodArgumentNotValidException
import org.springframework.web.bind.annotation.ExceptionHandler
import org.springframework.web.bind.annotation.ResponseStatus
import org.springframework.web.bind.annotation.RestControllerAdvice

@RestControllerAdvice
class ControllerAdvice {
    @ExceptionHandler(MethodArgumentNotValidException::class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    fun handleValidationError(ex: MethodArgumentNotValidException): ErrorDto {
        val fields =
            ex.bindingResult.fieldErrors.groupBy(
                keySelector = { it.field },
                valueTransform = { it.defaultMessage ?: "Invalid value" },
            )
        return ErrorDto("Validation failed", fields)
    }

    @ExceptionHandler(Exception::class)
    @ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
    fun handleError(ex: Exception): ErrorDto = ErrorDto(ex.message ?: "Unknown error", mapOf())
}
