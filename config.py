import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")

# Databricks Configuration
DATABRICKS_SERVER_HOSTNAME = os.getenv("DATABRICKS_SERVER_HOSTNAME")
DATABRICKS_HTTP_PATH = os.getenv("DATABRICKS_HTTP_PATH")
DATABRICKS_ACCESS_TOKEN = os.getenv("DATABRICKS_ACCESS_TOKEN")

# Sybase Configuration
SYBASE_HOST = os.getenv("SYBASE_HOST")
SYBASE_PORT = int(os.getenv("SYBASE_PORT", "5000"))
SYBASE_DATABASE = os.getenv("SYBASE_DATABASE")
SYBASE_USER = os.getenv("SYBASE_USER")
SYBASE_PASSWORD = os.getenv("SYBASE_PASSWORD")

# MCP Server Configuration
MCP_SERVER_NAME = "MultiAgent-MCP"
MCP_SERVER_VERSION = "1.0.0"
