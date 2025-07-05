from typing import Dict, List, Any
from tools.base_tool import BaseTool
from agents.openai_agent import OpenAIAgent
import asyncio

class Orchestrator:
    def __init__(self):
        self.tools: Dict[str, BaseTool] = {}
        self.agent = None
        self.conversation_history = []
    
    def register_tool(self, tool: BaseTool):
        """Register a new tool dynamically"""
        self.tools[tool.name] = tool
        self._update_agent()
    
    def unregister_tool(self, tool_name: str):
        """Remove a tool"""
        if tool_name in self.tools:
            del self.tools[tool_name]
            self._update_agent()
    
    def _update_agent(self):
        """Update agent with current tools"""
        tool_schemas = [tool.get_schema() for tool in self.tools.values()]
        self.agent = OpenAIAgent(tool_schemas)
    
    async def process_request(self, user_input: str) -> str:
        """Process user request through agent and execute tools if needed"""
        if not self.agent:
            return "No tools registered. Please add tools first."
        
        # Get agent response
        response = await self.agent.process(user_input, self.conversation_history)
        
        if response["type"] == "error":
            return response["content"]
        
        # Add user message to history
        self.conversation_history.append({"role": "user", "content": user_input})
        
        if response["type"] == "tool_calls":
            # Execute tool calls
            results = []
            for tool_call in response["tool_calls"]:
                tool_name = tool_call["name"]
                if tool_name in self.tools:
                    tool = self.tools[tool_name]
                    result = await tool.execute(**tool_call["arguments"])
                    results.append({
                        "tool": tool_name,
                        "result": result.dict()
                    })
                else:
                    results.append({
                        "tool": tool_name,
                        "result": {"success": False, "error": f"Tool {tool_name} not found"}
                    })
            
            # Format results for user
            formatted_results = self._format_results(results)
            
            # Add assistant response to history
            self.conversation_history.append({
                "role": "assistant", 
                "content": response["content"] if response["content"] else formatted_results
            })
            
            return formatted_results
        else:
            # Direct response without tool calls
            self.conversation_history.append({"role": "assistant", "content": response["content"]})
            return response["content"]
    
    def _format_results(self, results: List[Dict[str, Any]]) -> str:
        """Format tool execution results for display"""
        formatted = []
        for result in results:
            tool_name = result["tool"]
            tool_result = result["result"]
            
            if tool_result["success"]:
                formatted.append(f"✅ {tool_name}: Success")
                if tool_result["data"]:
                    formatted.append(f"Data: {tool_result['data']}")
            else:
                formatted.append(f"❌ {tool_name}: Failed")
                formatted.append(f"Error: {tool_result['error']}")
        
        return "\n".join(formatted)
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
