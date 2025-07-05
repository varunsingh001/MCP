from abc import ABC, abstractmethod
from typing import Dict, Any, List
from pydantic import BaseModel

class ToolParameter(BaseModel):
    name: str
    type: str
    description: str
    required: bool = True

class ToolResult(BaseModel):
    success: bool
    data: Any = None
    error: str = None

class BaseTool(ABC):
    def __init__(self):
        self.name = self.__class__.__name__
        self.description = ""
        self.parameters: List[ToolParameter] = []
    
    @abstractmethod
    async def execute(self, **kwargs) -> ToolResult:
        """Execute the tool with given parameters"""
        pass
    
    def get_schema(self) -> Dict[str, Any]:
        """Return tool schema for MCP"""
        return {
            "name": self.name,
            "description": self.description,
            "inputSchema": {
                "type": "object",
                "properties": {
                    param.name: {
                        "type": param.type,
                        "description": param.description
                    } for param in self.parameters
                },
                "required": [p.name for p in self.parameters if p.required]
            }
        }
