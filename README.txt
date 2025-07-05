# Multi-Agent MCP Server

A modular, multi-agent system using Model Context Protocol (MCP) with OpenAI as the LLM and Streamlit as the frontend. The system allows dynamic tool management for database operations on Databricks and Sybase.

## Features

- **Dynamic Tool Management**: Add or remove tools at runtime
- **Multi-Database Support**: Query and insert data into Databricks and Sybase
- **AI-Powered Orchestration**: Uses OpenAI to understand natural language requests
- **Modular Architecture**: Easy to extend with new tools
- **Simple Web Interface**: Clean Streamlit UI for interaction

## Setup

1. **Clone the repository and install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Configure environment variables:**
```bash
cp .env.example .env
# Edit .env with your actual credentials
```

3. **Run the application:**
```bash
streamlit run app.py
```

## Architecture

- **Orchestrator**: Central component that manages tools and processes requests
- **Tools**: Modular components for specific operations (Databricks, Sybase)
- **Agent**: OpenAI-based agent that interprets user requests
- **MCP Server**: Optional MCP protocol server for external integration

## Usage

1. Start the application
2. Add tools from the sidebar (e.g., "Databricks Query", "Sybase Insert")
3. Type natural language requests in the chat interface
4. The AI will interpret your request and execute appropriate tools

## Example Requests

- "Query all customers from the Databricks sales table"
- "Insert a new product into Sybase with name 'Widget' and price 29.99"
- "Show me inventory items with quantity less than 10 from Sybase"

## Extending the System

To add a new tool:

1. Create a new tool class inheriting from `BaseTool`
2. Implement the `execute` method
3. Define parameters and description
4. Register it in the available tools in `app.py`

## Security Note

Never commit your `.env` file with actual credentials. Always use environment variables for sensitive information.
