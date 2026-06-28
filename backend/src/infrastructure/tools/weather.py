"""Infrastructure – weather tool implementation."""
import random
from typing import Any


def get_weather(args: dict) -> dict[str, Any]:
    city = args.get("city", "Unknown")
    unit = args.get("unit", "celsius")
    temp = random.randint(15, 35) if unit == "celsius" else random.randint(59, 95)
    symbol = "°C" if unit == "celsius" else "°F"
    return {
        "city": city,
        "temperature": f"{temp}{symbol}",
        "condition": random.choice(["Sunny", "Cloudy", "Partly cloudy", "Rainy"]),
        "humidity": f"{random.randint(40, 80)}%",
    }
