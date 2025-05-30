# from google.adk.agents import Agent
# from dotenv import load_dotenv

# load_dotenv()

# root_agent = Agent(
#     name="weather_time_agent",
#     model="gemini-2.0-flash",
#     description=(
#         "Agent to answer questions about the time and weather in a city."
#     ),
#     instruction=(
#         "You are a helpful agent who can answer user questions about the time and weather in a city."
#     )
# )

import os # Required for path operations
import asyncio
from dotenv import load_dotenv
from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

# Load environment variables
load_dotenv()

async def get_tools_async():
    """Gets tools from the custom MCP Server."""
    
    # Get the absolute path to your custom MCP server
    current_dir = os.path.dirname(os.path.abspath(__file__))
    mcp_server_path = os.path.join(current_dir, "..", "mcp_server", "server.py")
    mcp_server_path = os.path.abspath(mcp_server_path)
    
    print(f"Connecting to MCP server at: {mcp_server_path}")
    
    tools, exit_stack = await MCPToolset.from_server(
        connection_params=StdioServerParameters(
            command='python',  # Use python to run your custom server
            args=[mcp_server_path],  # Path to your custom MCP server
        )
    )
    
    print(f"Fetched {len(tools)} tools from MCP server.")
    return tools, exit_stack

async def get_agent_async():
    """Creates an ADK Agent equipped with tools from the custom MCP Server."""
    
    tools, exit_stack = await get_tools_async()
    
    agent = LlmAgent(
        model='gemini-2.0-flash',
        name='custom_mcp_agent',
        instruction='You are a helpful assistant with access to custom tools including email sending, QuickBooks integration, and other business functions. Help users with their requests using the available tools.',
        tools=tools,
    )
    
    return agent, exit_stack

# For ADK web discovery - this is the main agent that ADK will use
# ADK will call get_agent_async() when it needs the agent with tools
root_agent = get_agent_async()