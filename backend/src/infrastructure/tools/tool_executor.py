"""Infrastructure – composite tool executor."""
from typing import Any

from src.application.interfaces.tool_executor import IToolExecutor
from src.infrastructure.tools.calculator import calculate
from src.infrastructure.tools.weather import get_weather

_TOOL_HANDLERS = {
    "get_weather": get_weather,
    "calculate": calculate,
}


class ToolExecutor(IToolExecutor):
    def execute(self, name: str, args: dict) -> Any:
        handler = _TOOL_HANDLERS.get(name)
        if handler is None:
            return {"error": f"Unknown tool: {name}"}
        return handler(args)
