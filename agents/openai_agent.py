from openai import OpenAI
import json
from typing import Dict, List, Any
import config

class OpenAIAgent:
    def __init__(self, tools: List[Dict[str, Any]]):
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        self.tools = tools
        self.model = config.OPENAI_MODEL
    
    async def process(self, user_input: str, context: List[Dict[str, str]] = None) -> Dict[str, Any]:
        messages = context or []
        messages.append({"role": "user", "content": user_input})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.tools,
                tool_choice="auto"
            )
            
            message = response.choices[0].message
            
            if message.tool_calls:
                tool_calls = []
                for tool_call in message.tool_calls:
                    tool_calls.append({
                        "id": tool_call.id,
                        "name": tool_call.function.name,
                        "arguments": json.loads(tool_call.function.arguments)
                    })
                return {
                    "type": "tool_calls",
                    "content": message.content,
                    "tool_calls": tool_calls
                }
            else:
                return {
                    "type": "response",
                    "content": message.content
                }
        except Exception as e:
            return {
                "type": "error",
                "content": f"Error processing request: {str(e)}"
            }
