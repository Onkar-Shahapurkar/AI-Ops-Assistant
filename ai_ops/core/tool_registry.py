from typing import Dict, Type
from tools.base_tool import BaseTool

class ToolRegistry:
    _tools: Dict[str, Type[BaseTool]] = {}

    @classmethod
    def register(cls, name: str, tool_cls: Type[BaseTool]):
        cls._tools[name] = tool_cls

    @classmethod
    def get(cls, name: str) -> Type[BaseTool]:
        if name not in cls._tools:
            raise ValueError(f"Tool '{name}' not found in registry.")
        return cls._tools[name]

    @classmethod
    def list_tools(cls):
        return list(cls._tools.keys())
