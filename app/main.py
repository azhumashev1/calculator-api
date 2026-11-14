from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
from typing import Literal
import math

app = FastAPI(
    title="Calculator API",
    description="REST API для выполнения арифметических операций",
    version="1.0.0"
)


class CalculationRequest(BaseModel):
    a: float = Field(..., description="Первое число")
    b: float = Field(..., description="Второе число")
    operation: Literal["add", "subtract", "multiply", "divide"]

    @field_validator("a", "b")
    @classmethod
    def check_finite(cls, value):
        if not math.isfinite(value):
            raise ValueError("Число должно быть конечным")
        return value


@app.get("/")
def root():
    return {
        "message": "Calculator API is running",
        "version": "1.0.0"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/calculate")
def calculate(request: CalculationRequest):
    a = request.a
    b = request.b
    operation = request.operation

    if operation == "add":
        result = a + b

    elif operation == "subtract":
        result = a - b

    elif operation == "multiply":
        result = a * b

    elif operation == "divide":
        if b == 0:
            raise HTTPException(
                status_code=400,
                detail="Division by zero is not allowed"
            )
        result = a / b

    if not math.isfinite(result):
        raise HTTPException(
            status_code=400,
            detail="Result is outside the supported numeric range"
        )

    return {
        "a": a,
        "b": b,
        "operation": operation,
        "result": result
    }
