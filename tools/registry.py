# tools/registry.py
import functools
from dataclasses import dataclass
from typing import Callable, Any

@dataclass
class ToolDefinition:
    name: str
    description: str
    parameters: dict
    handler: Callable
    requires_confirmation: bool = False

class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, ToolDefinition] = {}

    def register(self, name: str, description: str, parameters: dict,
                 requires_confirmation: bool = False):
        def decorator(fn: Callable):
            self._tools[name] = ToolDefinition(
                name=name,
                description=description,
                parameters=parameters,
                handler=fn,
                requires_confirmation=requires_confirmation
            )
            return fn
        return decorator

    def to_ollama_tools(self) -> list[dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": t.name,
                    "description": t.description,
                    "parameters": t.parameters
                }
            }
            for t in self._tools.values()
        ]

    async def dispatch(self, tool_name: str, args: dict) -> Any:
        tool = self._tools.get(tool_name)
        if not tool:
            return f"Error: Tool '{tool_name}' not found"

        if tool.requires_confirmation:
            confirm = input(f"\n⚠ Tool '{tool_name}' cu args {args}\nConfirmi? [y/N]: ")
            if confirm.lower() != 'y':
                return "Operație anulată de utilizator."

        return await tool.handler(**args)

registry = ToolRegistry()