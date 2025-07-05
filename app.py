import streamlit as st
import asyncio
from orchestrator import Orchestrator
from tools.databricks_tool import DatabricksQueryTool, DatabricksInsertTool
from tools.sybase_tool import SybaseQueryTool, SybaseInsertTool

# Initialize orchestrator
if 'orchestrator' not in st.session_state:
    st.session_state.orchestrator = Orchestrator()
    st.session_state.messages = []

# Page config
st.set_page_config(
    page_title="Multi-Agent MCP System",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Multi-Agent MCP System")
st.markdown("### AI-powered database operations with OpenAI")

# Sidebar for tool management
with st.sidebar:
    st.header("Tool Management")
    
    # Available tools
    available_tools = {
        "Databricks Query": DatabricksQueryTool,
        "Databricks Insert": DatabricksInsertTool,
        "Sybase Query": SybaseQueryTool,
        "Sybase Insert": SybaseInsertTool
    }
    
    st.subheader("Available Tools")
    for tool_name, tool_class in available_tools.items():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.text(tool_name)
        with col2:
            if st.button("Add", key=f"add_{tool_name}"):
                tool_instance = tool_class()
                st.session_state.orchestrator.register_tool(tool_instance)
                st.success(f"Added {tool_name}")
    
    st.divider()
    
    st.subheader("Active Tools")
    if st.session_state.orchestrator.tools:
        for tool_name in st.session_state.orchestrator.tools.keys():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.text(tool_name)
            with col2:
                if st.button("Remove", key=f"remove_{tool_name}"):
                    st.session_state.orchestrator.unregister_tool(tool_name)
                    st.success(f"Removed {tool_name}")
                    st.rerun()
    else:
        st.info("No active tools")
    
    st.divider()
    
    if st.button("Clear Conversation"):
        st.session_state.orchestrator.clear_history()
        st.session_state.messages = []
        st.rerun()

# Main chat interface
st.subheader("Chat Interface")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me to query or insert data..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Processing..."):
            # Run async operation
            response = asyncio.run(
                st.session_state.orchestrator.process_request(prompt)
            )
            st.markdown(response)
    
    # Add assistant message
    st.session_state.messages.append({"role": "assistant", "content": response})

# Examples section
with st.expander("📚 Example Queries"):
    st.markdown("""
    **Databricks Queries:**
    - "Query the sales table in Databricks to get all records from last month"
    - "Insert a new record into the customers table in Databricks with name 'John Doe' and email 'john@example.com'"
    
    **Sybase Queries:**
    - "Get all products from the inventory table in Sybase where quantity is less than 10"
    - "Add a new product to the products table in Sybase with name 'Widget' and price 29.99"
    
    **Multi-database Operations:**
    - "Compare customer counts between Databricks and Sybase databases"
    - "Migrate all records from Sybase orders table to Databricks"
    """)

# Status indicator
with st.container():
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.session_state.orchestrator.tools:
            st.success(f"🟢 {len(st.session_state.orchestrator.tools)} tools active")
        else:
            st.warning("🔴 No tools active")
