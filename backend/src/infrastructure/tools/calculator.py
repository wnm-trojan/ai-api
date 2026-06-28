"""Infrastructure – calculator tool implementation."""
from typing import Any


def calculate(args: dict) -> dict[str, Any]:
    expr = args.get("expression", "0")
    allowed = set("0123456789+-*/(). ")
    if not all(c in allowed for c in expr):
        return {"error": "Unsafe expression"}
    try:
        return {"result": eval(expr)}  # noqa: S307
    except Exception as e:
        return {"error": str(e)}
