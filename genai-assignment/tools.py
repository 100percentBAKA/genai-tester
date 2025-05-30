def calculate(expression: str) -> str:
    """
    Calculates the result of a simple arithmetic expression.
    For example, "2 + 2" or "10 * (5 - 2) / 3".
    Args:
        expression: The arithmetic expression string.
    Returns:
        A string representing the result of the calculation or an error message.
    """
    allowed_chars = "0123456789+-*/(). "
    if not all(char in allowed_chars for char in expression):
        return "Error: Invalid characters in expression. Only numbers and basic operators (+, -, *, /) are allowed."
    try:
        result = eval(expression)
        return f"The result of '{expression}' is {result}."
    except ZeroDivisionError:
        return "Error: Cannot divide by zero."
    except Exception as e:
        return f"Error: Could not evaluate the expression. {str(e)}"
    

def get_weather(city: str) -> str:
    """
    Provides a mock weather forecast for a given city.
    Args:
        city: The name of the city.
    Returns:
        A string describing the weather in the specified city.
    """
    city = city.strip().lower()
    if city == "london":
        return f"The weather in {city.capitalize()} is currently cloudy with a chance of rain. Temperature is 15°C."
    elif city == "new york":
        return f"The weather in {city.capitalize()} is sunny. Temperature is 22°C."
    elif city == "tokyo":
        return f"The weather in {city.capitalize()} is partly cloudy. Temperature is 20°C."
    else:
        return f"Sorry, I don't have weather information for {city.capitalize()}."
