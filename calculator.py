import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
def multiply(*args):
    """Return the product of all provided numbers.

    Args:
        *args: A variable number of numeric arguments. At least one argument must be provided.

    Returns:
        The multiplication result of all arguments.
    """
    if not args:
        raise ValueError("multiply requires at least one argument")
    product = 1
    for number in args:
        product *= number
    return product
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
import math

def sqrt(a):
    """Return the square root of a.
    If a is negative, logs an error and returns an error string.
    """
    if a < 0:
        log_debug("Cannot take square root of negative number")
        return "Error: Cannot take square root of negative number"
    return math.sqrt(a)

def log10(value):
    """Return the base‑10 logarithm of *value*.

    Parameters:
        value (numeric): The number to take the log of.

    Returns:
        float: The base‑10 logarithm of *value*.

    Raises:
        ValueError: If *value* is not positive.
    """
    if value <= 0:
        raise ValueError("log10 is undefined for non‑positive values")
    return math.log10(value)

def sine(x):
    """Return the sine of *x* (x in radians)."""
    log_debug(f"Calculating sine for input: {x}")
    return math.sin(x)

def cosine(x):
    """Return the cosine of *x* (x in radians)."""
    log_debug(f"Calculating cosine for input: {x}")
    return math.cos(x)

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
    print("log10(100) =", log10(100))
    print("sin(pi/2) =", sine(math.pi/2))
    print("cos(pi) =", cosine(math.pi))
