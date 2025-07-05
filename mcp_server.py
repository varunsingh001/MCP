import asyncio
from mcp.server import MCPServer
from mcp.types import Tool, TextContent
from orchestrator import Orchestrator
import config

class MultiAgentMCPServer:
    def __init__(self):
        self.server = MCPServer(config.MCP_SERVER_NAME)
        self.orchestrator = Orchestrator()
        self._setup_handlers()
    
    def _setup_handlers(self):
        @self.server.list_tools()
        async def list_tools():
            tools = []
            for tool in self.orchestrator.tools.values():
                schema = tool.get_schema()
                tools.append(Tool(
                    name=schema["name"],
                    description=schema["description"],
                    inputSchema=schema["inputSchema"]
                ))
            return tools
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict):
            if name in self.orchestrator.tools:
                tool = self.orchestrator.tools[name]
                result = await tool.execute(**arguments)
                return [TextContent(
                    type="text",
                    text=str(result.dict())
                )]
            else:
                return [TextContent(
                    type="text",
                    text=f"Tool {name} not found"
                )]
    
    def add_tool(self, tool):
        """Add a tool to the orchestrator"""
        self.orchestrator.register_tool(tool)
    
    async def run(self):
        """Run the MCP server"""
        await self.server.run()

# Initialize server instance
mcp_server = MultiAgentMCPServer()
