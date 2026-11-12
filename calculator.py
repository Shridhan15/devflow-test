import logging
import math
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log(message):
    """Log a message at INFO level."""
    logging.info(message)

def log_error(message):
    """Log a message at ERROR level."""
    logging.error(message)

# New log_debug function added
def log_debug(message):
    """Log a message at DEBUG level."""
    logging.debug(message)

# dummy_repo/calculator.py
def add(a, b):
    return a + b

# keep the comments as it is
def subtract(a, b):
    return a - b

# New multiply function added
def multiply(a, b, c=None):
    """Return the product of two or three numbers.
    If a third argument is provided, multiply all three.
    """
    if c is not None:
        return a * b * c
    return a * b

# New divide function added
def divide(a, b):
    """Return the result of dividing a by b.
    If b is zero, returns the string "Error: Division by zero".
    """
    if b == 0:
        return "Error: Division by zero"
    return a / b

# New modulo function added
def modulo(a, b):
    """Return the remainder of a divided by b.
    If b is zero, returns the string "Error: Division by zero".
    """
    if b == 0:
        return "Error: Division by zero"
    return a % b

# New power function added
def power(a, b):
    """Return a raised to the power of b.

    Parameters:
        a (numeric): The base value.
        b (numeric): The exponent value.

    Returns:
        numeric: The result of a ** b.
    """
    return a ** b

# New sqrt function added
def sqrt(a):
    """Return the square root of a.

    Parameters:
        a (numeric): The number to take the square root of.

    Returns:
        numeric: The square root of a if a is non‑negative.
        str: An error message if a is negative.
    """
    if a < 0:
        log_error(f"Attempted to take square root of negative number: {a}")
        return "Error: Negative input"
    return math.sqrt(a)

if __name__ == "__main__":
    print("10 + 5 =", add(10, 5))
    print("10 * 5 =", multiply(10, 5))
    print("10 * 5 * 2 =", multiply(10, 5, 2))
    print("10 / 2 =", divide(10, 2))
    print("10 / 0 =", divide(10, 0))
    print("10 % 3 =", modulo(10, 3))
    print("2 ** 3 =", power(2, 3))
    print("sqrt(9) =", sqrt(9))
    print("sqrt(-4) =", sqrt(-4))
    log_debug("This is a debug message")