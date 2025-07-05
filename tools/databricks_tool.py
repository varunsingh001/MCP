from databricks import sql
from typing import List, Dict, Any
from .base_tool import BaseTool, ToolParameter, ToolResult
import config

class DatabricksQueryTool(BaseTool):
    def __init__(self):
        super().__init__()
        self.name = "databricks_query"
        self.description = "Execute a SELECT query on Databricks"
        self.parameters = [
            ToolParameter(name="query", type="string", description="SQL SELECT query to execute")
        ]
    
    async def execute(self, query: str) -> ToolResult:
        try:
            with sql.connect(
                server_hostname=config.DATABRICKS_SERVER_HOSTNAME,
                http_path=config.DATABRICKS_HTTP_PATH,
                access_token=config.DATABRICKS_ACCESS_TOKEN
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    columns = [desc[0] for desc in cursor.description]
                    rows = cursor.fetchall()
                    result = [dict(zip(columns, row)) for row in rows]
                    return ToolResult(success=True, data=result)
        except Exception as e:
            return ToolResult(success=False, error=str(e))

class DatabricksInsertTool(BaseTool):
    def __init__(self):
        super().__init__()
        self.name = "databricks_insert"
        self.description = "Insert data into Databricks table"
        self.parameters = [
            ToolParameter(name="table", type="string", description="Table name"),
            ToolParameter(name="data", type="object", description="Data to insert as key-value pairs")
        ]
    
    async def execute(self, table: str, data: Dict[str, Any]) -> ToolResult:
        try:
            columns = ", ".join(data.keys())
            placeholders = ", ".join([f"'{v}'" if isinstance(v, str) else str(v) for v in data.values()])
            query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
            
            with sql.connect(
                server_hostname=config.DATABRICKS_SERVER_HOSTNAME,
                http_path=config.DATABRICKS_HTTP_PATH,
                access_token=config.DATABRICKS_ACCESS_TOKEN
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    return ToolResult(success=True, data={"message": "Data inserted successfully"})
        except Exception as e:
            return ToolResult(success=False, error=str(e))
