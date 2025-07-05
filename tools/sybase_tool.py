import Sybase
from typing import List, Dict, Any
from .base_tool import BaseTool, ToolParameter, ToolResult
import config

class SybaseQueryTool(BaseTool):
    def __init__(self):
        super().__init__()
        self.name = "sybase_query"
        self.description = "Execute a SELECT query on Sybase database"
        self.parameters = [
            ToolParameter(name="query", type="string", description="SQL SELECT query to execute")
        ]
    
    async def execute(self, query: str) -> ToolResult:
        try:
            db = Sybase.connect(
                config.SYBASE_HOST,
                config.SYBASE_USER,
                config.SYBASE_PASSWORD,
                config.SYBASE_DATABASE
            )
            cursor = db.cursor()
            cursor.execute(query)
            
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            result = [dict(zip(columns, row)) for row in rows]
            
            cursor.close()
            db.close()
            
            return ToolResult(success=True, data=result)
        except Exception as e:
            return ToolResult(success=False, error=str(e))

class SybaseInsertTool(BaseTool):
    def __init__(self):
        super().__init__()
        self.name = "sybase_insert"
        self.description = "Insert data into Sybase table"
        self.parameters = [
            ToolParameter(name="table", type="string", description="Table name"),
            ToolParameter(name="data", type="object", description="Data to insert as key-value pairs")
        ]
    
    async def execute(self, table: str, data: Dict[str, Any]) -> ToolResult:
        try:
            db = Sybase.connect(
                config.SYBASE_HOST,
                config.SYBASE_USER,
                config.SYBASE_PASSWORD,
                config.SYBASE_DATABASE
            )
            cursor = db.cursor()
            
            columns = ", ".join(data.keys())
            placeholders = ", ".join([f"'{v}'" if isinstance(v, str) else str(v) for v in data.values()])
            query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
            
            cursor.execute(query)
            db.commit()
            
            cursor.close()
            db.close()
            
            return ToolResult(success=True, data={"message": "Data inserted successfully"})
        except Exception as e:
            return ToolResult(success=False, error=str(e))
