"""
MCP Server Implementation Examples

This file contains complete, runnable examples for implementing MCP servers.
Reference these examples from RULE.md using @examples_server.py syntax.
"""

import asyncio
import logging
from typing import Any, Sequence
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    Resource,
    Prompt,
    PromptMessage,
    PromptArgument,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# Example 1: Basic Server with Tools
# ============================================================================

def create_basic_server() -> Server:
    """
    Create a basic MCP server with simple tools.
    
    Returns:
        Server: Configured MCP server instance
    """
    server = Server("basic-example-server")
    
    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """List available tools."""
        return [
            Tool(
                name="echo",
                description="Echoes back the provided message",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "The message to echo back"
                        }
                    },
                    "required": ["message"]
                }
            ),
            Tool(
                name="add",
                description="Adds two numbers together",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "a": {"type": "number", "description": "First number"},
                        "b": {"type": "number", "description": "Second number"}
                    },
                    "required": ["a", "b"]
                }
            )
        ]
    
    @server.call_tool()
    async def call_tool(name: str, arguments: dict[str, Any]) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        """Handle tool calls."""
        if name == "echo":
            message = arguments.get("message", "")
            return [TextContent(type="text", text=f"Echo: {message}")]
        
        elif name == "add":
            a = arguments.get("a", 0)
            b = arguments.get("b", 0)
            result = a + b
            return [TextContent(type="text", text=f"Result: {result}")]
        
        else:
            raise ValueError(f"Unknown tool: {name}")
    
    return server


# ============================================================================
# Example 2: Server with Resources
# ============================================================================

def create_server_with_resources() -> Server:
    """
    Create an MCP server with resource management.
    
    Returns:
        Server: Configured MCP server with resources
    """
    server = Server("resources-example-server")
    
    # In-memory resource storage (in production, use proper storage)
    resources_store = {
        "config://app/settings": {"theme": "dark", "language": "en"},
        "data://users/123": {"name": "John Doe", "email": "john@example.com"}
    }
    
    @server.list_resources()
    async def list_resources() -> list[Resource]:
        """List available resources."""
        return [
            Resource(
                uri="config://app/settings",
                name="Application Settings",
                description="Application configuration settings",
                mimeType="application/json"
            ),
            Resource(
                uri="data://users/123",
                name="User Profile",
                description="User profile data",
                mimeType="application/json"
            )
        ]
    
    @server.read_resource()
    async def read_resource(uri: str) -> str:
        """Read a resource by URI."""
        if uri in resources_store:
            import json
            return json.dumps(resources_store[uri])
        raise ValueError(f"Resource not found: {uri}")
    
    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """List available tools."""
        return []
    
    @server.call_tool()
    async def call_tool(name: str, arguments: dict[str, Any]) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        """Handle tool calls."""
        return []
    
    return server


# ============================================================================
# Example 3: Server with Prompts
# ============================================================================

def create_server_with_prompts() -> Server:
    """
    Create an MCP server with prompt templates.
    
    Returns:
        Server: Configured MCP server with prompts
    """
    server = Server("prompts-example-server")
    
    @server.list_prompts()
    async def list_prompts() -> list[Prompt]:
        """List available prompt templates."""
        return [
            Prompt(
                name="code-review",
                description="Generate a code review prompt",
                arguments=[
                    PromptArgument(
                        name="file_path",
                        description="Path to the file to review",
                        required=True
                    ),
                    PromptArgument(
                        name="focus_areas",
                        description="Comma-separated list of focus areas",
                        required=False
                    )
                ]
            ),
            Prompt(
                name="explain-code",
                description="Explain what the code does",
                arguments=[
                    PromptArgument(
                        name="code",
                        description="Code snippet to explain",
                        required=True
                    )
                ]
            )
        ]
    
    @server.get_prompt()
    async def get_prompt(name: str, arguments: dict[str, str]) -> PromptMessage:
        """Get a prompt template with arguments filled in."""
        if name == "code-review":
            file_path = arguments.get("file_path", "")
            focus_areas = arguments.get("focus_areas", "all")
            return PromptMessage(
                role="user",
                content=PromptMessage.TextContent(
                    type="text",
                    text=f"Please review the code in {file_path}. Focus on: {focus_areas}"
                )
            )
        
        elif name == "explain-code":
            code = arguments.get("code", "")
            return PromptMessage(
                role="user",
                content=PromptMessage.TextContent(
                    type="text",
                    text=f"Please explain what this code does:\n\n```python\n{code}\n```"
                )
            )
        
        raise ValueError(f"Unknown prompt: {name}")
    
    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """List available tools."""
        return []
    
    @server.call_tool()
    async def call_tool(name: str, arguments: dict[str, Any]) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        """Handle tool calls."""
        return []
    
    return server


# ============================================================================
# Example 4: Server with Agent-Specific Tool Filtering (Views/Profiles/Scopes)
# ============================================================================

# Tool metadata for filtering
TOOL_METADATA = {
    "read_file": {"scopes": ["file_operations", "data_access"], "agent_types": ["data_agent", "general"]},
    "write_file": {"scopes": ["file_operations"], "agent_types": ["data_agent"]},
    "query_database": {"scopes": ["data_access"], "agent_types": ["data_agent"]},
    "send_email": {"scopes": ["communication"], "agent_types": ["communication_agent"]},
    "analyze_data": {"scopes": ["data_analysis"], "agent_types": ["data_agent", "analyst"]},
}

def create_server_with_scopes() -> Server:
    """
    Create an MCP server with agent-specific tool filtering using scopes/profiles.
    
    Returns:
        Server: Configured MCP server with scope-based filtering
    """
    server = Server("scoped-example-server")
    
    @server.list_tools()
    async def list_tools(agent_profile: str | None = None, scopes: list[str] | None = None) -> list[Tool]:
        """
        List available tools, filtered by agent profile and scopes.
        
        Args:
            agent_profile: Optional agent profile/type identifier
            scopes: Optional list of scopes to filter by
        
        Returns:
            Filtered list of tools
        """
        all_tools = [
            Tool(
                name="read_file",
                description="Read content from a file",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "File path"}
                    },
                    "required": ["path"]
                }
            ),
            Tool(
                name="write_file",
                description="Write content to a file",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "File path"},
                        "content": {"type": "string", "description": "Content to write"}
                    },
                    "required": ["path", "content"]
                }
            ),
            Tool(
                name="query_database",
                description="Query a database",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "SQL query"}
                    },
                    "required": ["query"]
                }
            ),
            Tool(
                name="send_email",
                description="Send an email",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "to": {"type": "string", "description": "Recipient email"},
                        "subject": {"type": "string", "description": "Email subject"},
                        "body": {"type": "string", "description": "Email body"}
                    },
                    "required": ["to", "subject", "body"]
                }
            ),
            Tool(
                name="analyze_data",
                description="Analyze data",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "data": {"type": "string", "description": "Data to analyze"}
                    },
                    "required": ["data"]
                }
            )
        ]
        
        # Filter tools based on agent profile and scopes
        if not agent_profile and not scopes:
            return all_tools
        
        filtered_tools = []
        for tool in all_tools:
            metadata = TOOL_METADATA.get(tool.name, {})
            tool_scopes = metadata.get("scopes", [])
            agent_types = metadata.get("agent_types", [])
            
            # Check if tool matches agent profile
            if agent_profile and agent_profile not in agent_types:
                continue
            
            # Check if tool matches requested scopes
            if scopes and not any(scope in tool_scopes for scope in scopes):
                continue
            
            filtered_tools.append(tool)
        
        return filtered_tools
    
    @server.call_tool()
    async def call_tool(name: str, arguments: dict[str, Any]) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        """Handle tool calls."""
        if name == "read_file":
            path = arguments.get("path", "")
            # In production, implement actual file reading
            return [TextContent(type="text", text=f"Reading file: {path}")]
        
        elif name == "write_file":
            path = arguments.get("path", "")
            content = arguments.get("content", "")
            # In production, implement actual file writing
            return [TextContent(type="text", text=f"Writing to file: {path}")]
        
        elif name == "query_database":
            query = arguments.get("query", "")
            # In production, implement actual database query
            return [TextContent(type="text", text=f"Executing query: {query}")]
        
        elif name == "send_email":
            to = arguments.get("to", "")
            subject = arguments.get("subject", "")
            # In production, implement actual email sending
            return [TextContent(type="text", text=f"Email sent to {to}: {subject}")]
        
        elif name == "analyze_data":
            data = arguments.get("data", "")
            # In production, implement actual data analysis
            return [TextContent(type="text", text=f"Analyzing data: {len(data)} characters")]
        
        raise ValueError(f"Unknown tool: {name}")
    
    return server


# ============================================================================
# Example 5: Complete Server with Error Handling
# ============================================================================

def create_complete_server() -> Server:
    """
    Create a complete MCP server with tools, resources, prompts, and error handling.
    
    Returns:
        Server: Fully configured MCP server
    """
    server = Server("complete-example-server")
    
    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """List available tools with error handling."""
        try:
            return [
                Tool(
                    name="calculate",
                    description="Perform mathematical calculations",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "expression": {
                                "type": "string",
                                "description": "Mathematical expression to evaluate"
                            }
                        },
                        "required": ["expression"]
                    }
                )
            ]
        except Exception as e:
            logger.error(f"Error listing tools: {e}")
            return []
    
    @server.call_tool()
    async def call_tool(name: str, arguments: dict[str, Any]) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        """Handle tool calls with error handling."""
        try:
            if name == "calculate":
                expression = arguments.get("expression", "")
                # In production, use safe evaluation
                try:
                    result = eval(expression)  # WARNING: Use safe evaluation in production
                    return [TextContent(type="text", text=f"Result: {result}")]
                except Exception as e:
                    return [TextContent(type="text", text=f"Error: {str(e)}")]
            
            raise ValueError(f"Unknown tool: {name}")
        
        except Exception as e:
            logger.error(f"Error calling tool {name}: {e}")
            return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    @server.list_resources()
    async def list_resources() -> list[Resource]:
        """List available resources."""
        return []
    
    @server.read_resource()
    async def read_resource(uri: str) -> str:
        """Read a resource."""
        raise ValueError(f"Resource not found: {uri}")
    
    return server


# ============================================================================
# Server Execution
# ============================================================================

async def run_server_example():
    """Run a server example using stdio transport."""
    server = create_basic_server()
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="example-server",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities=None
                )
            )
        )


if __name__ == "__main__":
    asyncio.run(run_server_example())
