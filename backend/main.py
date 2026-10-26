from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import math
import ast
import operator


app = FastAPI(title="Smart Calculator API")


# Allow React frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Request Models
# -----------------------------

class ExpressionRequest(BaseModel):
    expression: str


class NumbersRequest(BaseModel):
    numbers: list[float]


class BMIRequest(BaseModel):
    weight: float
    height: float


class InterestRequest(BaseModel):
    principal: float
    rate: float
    time: float


class TemperatureRequest(BaseModel):
    value: float
    conversion: str


# -----------------------------
# Safe expression calculator
# -----------------------------

allowed_operators = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def calculate_expression(node):

    if isinstance(node, ast.Expression):
        return calculate_expression(node.body)

    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value

        raise ValueError("Only numbers are allowed")

    if isinstance(node, ast.BinOp):
        left = calculate_expression(node.left)
        right = calculate_expression(node.right)

        operation = type(node.op)

        if operation not in allowed_operators:
            raise ValueError("Operation not allowed")

        if operation is ast.Div and right == 0:
            raise ZeroDivisionError

        return allowed_operators[operation](left, right)

    if isinstance(node, ast.UnaryOp):
        operation = type(node.op)

        if operation not in allowed_operators:
            raise ValueError("Operation not allowed")

        return allowed_operators[operation](
            calculate_expression(node.operand)
        )

    raise ValueError("Invalid expression")


# -----------------------------
# Home API
# -----------------------------

@app.get("/")
def home():
    return {
        "message": "Smart Calculator API is running"
    }


# -----------------------------
# Expression Calculator
# -----------------------------

@app.post("/calculate")
def calculate(data: ExpressionRequest):

    try:

        tree = ast.parse(
            data.expression,
            mode="eval"
        )

        result = calculate_expression(tree)

        return {
            "expression": data.expression,
            "result": result
        }

    except ZeroDivisionError:

        raise HTTPException(
            status_code=400,
            detail="Cannot divide by zero"
        )

    except Exception:

        raise HTTPException(
            status_code=400,
            detail="Invalid expression"
        )


# -----------------------------
# Square Root
# -----------------------------

@app.get("/sqrt/{number}")
def square_root(number: float):

    if number < 0:
        raise HTTPException(
            status_code=400,
            detail="Cannot calculate square root of a negative number"
        )

    return {
        "number": number,
        "result": math.sqrt(number)
    }


# -----------------------------
# Average
# -----------------------------

@app.post("/average")
def average(data: NumbersRequest):

    if len(data.numbers) == 0:
        raise HTTPException(
            status_code=400,
            detail="Please provide at least one number"
        )

    result = sum(data.numbers) / len(data.numbers)

    return {
        "result": result
    }


# -----------------------------
# BMI
# -----------------------------

@app.post("/bmi")
def calculate_bmi(data: BMIRequest):

    if data.weight <= 0 or data.height <= 0:
        raise HTTPException(
            status_code=400,
            detail="Weight and height must be greater than zero"
        )

    # Height should be entered in centimeters
    height_meters = data.height / 100

    bmi = data.weight / (height_meters ** 2)

    if bmi < 18.5:
        category = "Underweight"

    elif bmi < 25:
        category = "Normal"

    elif bmi < 30:
        category = "Overweight"

    else:
        category = "Obese"

    return {
        "bmi": round(bmi, 2),
        "category": category
    }


# -----------------------------
# Simple Interest
# -----------------------------

@app.post("/interest")
def simple_interest(data: InterestRequest):

    if data.principal < 0 or data.rate < 0 or data.time < 0:
        raise HTTPException(
            status_code=400,
            detail="Values cannot be negative"
        )

    interest = (
        data.principal
        * data.rate
        * data.time
    ) / 100

    total = data.principal + interest

    return {
        "interest": round(interest, 2),
        "total": round(total, 2)
    }


# -----------------------------
# Temperature Converter
# -----------------------------

@app.post("/temperature")
def temperature(data: TemperatureRequest):

    conversion = data.conversion.lower()

    if conversion == "c_to_f":

        result = (data.value * 9 / 5) + 32

        unit = "°F"

    elif conversion == "f_to_c":

        result = (data.value - 32) * 5 / 9

        unit = "°C"

    else:

        raise HTTPException(
            status_code=400,
            detail="Invalid temperature conversion"
        )

    return {
        "result": round(result, 2),
        "unit": unit
    }