import json
from dotenv import load_dotenv
import asyncio

from mcp import types as mcp_types
from mcp.server.lowlevel import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio

from google.adk.tools.function_tool import FunctionTool
from google.adk.tools.mcp_tool.conversion_utils import adk_to_mcp_tool_type

from custom_tools import say_hello_tool

load_dotenv()

# init tools to expose
print("Initializing say_hello_tool")
say_hello_tool_expose = FunctionTool(say_hello_tool)
print(f"Tool '{say_hello_tool_expose.name}' initialized and ready to be exposed via MCP.")
# end of init tools to expose

# create MCP server
print("Creating MCP Server instance...")
app = Server("my-mcp-server")

# handler to list tools
@app.list_tools()
async def list_mcp_tools() -> list[mcp_types.Tool]:
    print("MCP Server: Received list_tools request")
    say_hello_tool_schema = adk_to_mcp_tool_type(say_hello_tool_expose)
    print(f"MCP Server: Advertising tool: {say_hello_tool_schema.name}")
    return [say_hello_tool_schema]

# handler to run/call tools
@app.call_tool()
async def call_mcp_tool(tool_name: str, arguments: dict): 
    print(f"MCP Server: Received call_tool request for '{tool_name}' with args: {arguments}")
    
    if tool_name == say_hello_tool_expose.name:
        try:
            say_hello_tool_response = await say_hello_tool_expose.run_async(
                args=arguments,
                tool_context=None
            )
            print(f"MCP Server: ADK tool '{tool_name}' executed. Response: {say_hello_tool_response}")

            response_text = json.dumps(say_hello_tool_response, indent=2)
            return [mcp_types.TextContent(type="text", text=response_text)]
        except Exception as e:
            print(f"MCP Server: Error executing ADK tool '{tool_name}': {e}")
            error_text = json.dumps({"error": f"Failed to execute tool '{tool_name}': {str(e)}"})
            return [mcp_types.TextContent(type="text", text=error_text)]
    else:
        print(f"MCP Server: Tool '{tool_name}' not found/exposed by this server.")
        error_text = json.dumps({"error": f"Tool '{tool_name}' not implemented by this server."})
        return [mcp_types.TextContent(type="text", text=error_text)]
    

async def run_mcp_stdio_server():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        print("MCP Stdio Server: Starting handshake with client...")

        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name=app.name,
                server_version="0.1.0",
                capabilities=app.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={}
                ),
            ),
        )

        print("MCP Stdio Server: Run loop finished or client disconnected.")



if __name__ == "__main__":
    print("Launching MCP Server to expose ADK tools via stdio...")
    try:
        asyncio.run(run_mcp_stdio_server())
    except KeyboardInterrupt:
        print("\nMCP Server (stdio) stopped by user.")
    except Exception as e:
        print(f"MCP Server (stdio) encountered an error: {e}")
    finally:
        print("MCP Server (stdio) process exiting.")



