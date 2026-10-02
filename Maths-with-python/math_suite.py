"""
UMaT Mathematics Suite (Maths-with-python)
Comprehensive mathematical algorithms and utility collection.
"""

from typing import List, Union

def is_armstrong(n: int) -> bool:
    """Check if a number is an Armstrong number (Narcissistic number)."""
    if n < 0:
        return False
    digits = [int(d) for d in str(n)]
    num_digits = len(digits)
    return sum(d ** num_digits for d in digits) == n

def fibonacci_sequence(n: int) -> List[int]:
    """Generate first n Fibonacci numbers."""
    if n <= 0:
        return []
    if n == 1:
        return [0]
    seq = [0, 1]
    while len(seq) < n:
        seq.append(seq[-1] + seq[-2])
    return seq

def factorial(n: int) -> int:
    """Calculate factorial of n."""
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers.")
    if n in (0, 1):
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def is_prime(n: int) -> bool:
    """Check if n is a prime number."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def sum_of_digits(n: int) -> int:
    """Calculate sum of digits of an integer."""
    return sum(int(d) for d in str(abs(n)))

def count_even_odd(numbers: List[int]) -> dict:
    """Count even and odd numbers in a list."""
    evens = sum(1 for x in numbers if x % 2 == 0)
    odds = len(numbers) - evens
    return {"even": evens, "odd": odds}

def calculate_discount(price: float, percentage: float) -> dict:
    """Calculate final price after applying discount."""
    if price < 0 or percentage < 0:
        raise ValueError("Price and percentage must be non-negative.")
    discount_amount = price * (percentage / 100.0)
    final_price = price - discount_amount
    return {"original_price": price, "discount_percent": percentage, "discount_amount": discount_amount, "final_price": final_price}

def average_marks(marks: List[float]) -> float:
    """Compute average of a list of marks."""
    if not marks:
        return 0.0
    return sum(marks) / len(marks)

def simple_calculator(a: float, b: float, operation: str) -> float:
    """Perform simple arithmetic operation (+, -, *, /)."""
    if operation == '+':
        return a + b
    elif operation == '-':
        return a - b
    elif operation == '*':
        return a * b
    elif operation == '/':
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        return a / b
    else:
        raise ValueError(f"Unknown operation: {operation}")

def print_multiplication_table(n: int, up_to: int = 12) -> List[str]:
    """Generate multiplication table for n."""
    return [f"{n} x {i} = {n * i}" for i in range(1, up_to + 1)]
