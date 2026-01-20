"""
MCP Client Implementation Examples

This file contains complete, runnable examples for implementing MCP clients.
Reference these examples from RULE.md using @examples_client.py syntax.
"""

import asyncio
import logging
from typing import Any
from urllib.parse import parse_qs, urlparse

import httpx
from pydantic import AnyUrl

from mcp import ClientSession, types
from mcp.client.auth import OAuthClientProvider, TokenStorage
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp.client.streamable_http import streamable_http_client
from mcp.shared.auth import OAuthClientInformationFull, OAuthClientMetadata, OAuthToken

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============================================================================
# Example 1: Basic Stdio Client
# ============================================================================

async def basic_stdio_client_example():
    """
    Basic example of connecting to an MCP server via stdio.
    
    This is the most common transport method for local MCP servers.
    """
    # Configure server parameters
    server_params = StdioServerParameters(
        command="python",
        args=["path/to/mcp_server.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            
            # List available tools
            tools = await session.list_tools()
            logger.info(f"Available tools: {[tool.name for tool in tools.tools]}")
            
            # Call a tool
            result = await session.call_tool("echo", {"message": "Hello, MCP!"})
            
            # Parse result
            for content in result.content:
                if isinstance(content, types.TextContent):
                    logger.info(f"Tool result: {content.text}")
            
            # List available resources
            resources = await session.list_resources()
            logger.info(f"Available resources: {[r.uri for r in resources.resources]}")


# ============================================================================
# Example 2: HTTP Client
# ============================================================================

async def http_client_example():
    """
    Example of connecting to an MCP server via HTTP.
    
    Use this for remote MCP servers accessible over HTTP.
    """
    server_url = "http://localhost:8000/mcp"
    
    async with streamable_http_client(server_url) as (read, write, _):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            
            # List available tools
            tools = await session.list_tools()
            logger.info(f"Available tools: {[tool.name for tool in tools.tools]}")
            
            # Call a tool
            result = await session.call_tool("add", {"a": 5, "b": 3})
            
            # Parse result
            for content in result.content:
                if isinstance(content, types.TextContent):
                    logger.info(f"Tool result: {content.text}")


# ============================================================================
# Example 3: OAuth Client
# ============================================================================

class InMemoryTokenStorage(TokenStorage):
    """
    Demo in-memory token storage implementation.
    
    In production, use persistent storage (database, encrypted file, etc.).
    """
    
    def __init__(self):
        self.tokens: OAuthToken | None = None
        self.client_info: OAuthClientInformationFull | None = None
    
    async def get_tokens(self) -> OAuthToken | None:
        """Get stored tokens."""
        return self.tokens
    
    async def set_tokens(self, tokens: OAuthToken) -> None:
        """Store tokens."""
        self.tokens = tokens
    
    async def get_client_info(self) -> OAuthClientInformationFull | None:
        """Get stored client information."""
        return self.client_info
    
    async def set_client_info(self, client_info: OAuthClientInformationFull) -> None:
        """Store client information."""
        self.client_info = client_info


async def handle_redirect(auth_url: str) -> None:
    """Handle OAuth redirect URL display."""
    logger.info(f"Visit: {auth_url}")


async def handle_callback() -> tuple[str, str | None]:
    """Handle OAuth callback URL input."""
    callback_url = input("Paste callback URL: ")
    params = parse_qs(urlparse(callback_url).query)
    return params["code"][0], params.get("state", [None])[0]


async def oauth_client_example():
    """
    Example of connecting to an MCP server with OAuth authentication.
    
    This is used for protected MCP servers requiring authentication.
    """
    # Create OAuth client provider
    oauth_auth = OAuthClientProvider(
        server_url="http://localhost:8001",
        client_metadata=OAuthClientMetadata(
            client_name="Example MCP Client",
            redirect_uris=[AnyUrl("http://localhost:3000/callback")],
            grant_types=["authorization_code", "refresh_token"],
            response_types=["code"],
            scope="user",
        ),
        storage=InMemoryTokenStorage(),
        redirect_handler=handle_redirect,
        callback_handler=handle_callback,
    )
    
    # Create HTTP client with OAuth authentication
    async with httpx.AsyncClient(auth=oauth_auth, follow_redirects=True) as custom_client:
        async with streamable_http_client(
            "http://localhost:8001/mcp",
            http_client=custom_client
        ) as (read, write, _):
            async with ClientSession(read, write) as session:
                # Initialize the connection
                await session.initialize()
                
                # List available tools
                tools = await session.list_tools()
                logger.info(f"Available tools: {[tool.name for tool in tools.tools]}")
                
                # List available resources
                resources = await session.list_resources()
                logger.info(f"Available resources: {[r.uri for r in resources.resources]}")


# ============================================================================
# Example 4: Tool Result Parsing
# ============================================================================

async def parse_tool_results_example(session: ClientSession):
    """
    Comprehensive example of parsing different types of tool results.
    
    Args:
        session: Active MCP client session
    """
    # Example 1: Parsing text content
    result = await session.call_tool("get_data", {"format": "text"})
    for content in result.content:
        if isinstance(content, types.TextContent):
            logger.info(f"Text: {content.text}")
    
    # Example 2: Parsing structured content from JSON tools
    result = await session.call_tool("get_user", {"id": "123"})
    if hasattr(result, "structuredContent") and result.structuredContent:
        # Access structured data directly
        user_data = result.structuredContent
        logger.info(f"User: {user_data.get('name')}, Age: {user_data.get('age')}")
    
    # Example 3: Parsing embedded resources
    result = await session.call_tool("read_config", {})
    for content in result.content:
        if isinstance(content, types.EmbeddedResource):
            resource = content.resource
            if isinstance(resource, types.TextResourceContents):
                logger.info(f"Config from {resource.uri}: {resource.text}")
            elif isinstance(resource, types.BlobResourceContents):
                logger.info(f"Binary data from {resource.uri}")
    
    # Example 4: Parsing image content
    result = await session.call_tool("generate_chart", {"data": [1, 2, 3]})
    for content in result.content:
        if isinstance(content, types.ImageContent):
            logger.info(f"Image ({content.mimeType}): {len(content.data)} bytes")
    
    # Example 5: Handling errors
    result = await session.call_tool("failing_tool", {})
    if result.isError:
        logger.error("Tool execution failed!")
        for content in result.content:
            if isinstance(content, types.TextContent):
                logger.error(f"Error: {content.text}")


# ============================================================================
# Example 5: Display Utilities
# ============================================================================

def get_display_name(obj: Any) -> str:
    """
    Get the display name for an MCP object following proper precedence rules.
    
    For tools: title > annotations.title > name
    For other objects: title > name
    
    Args:
        obj: MCP object (Tool, Resource, Prompt, etc.)
    
    Returns:
        Display name string
    """
    # Check for title attribute
    if hasattr(obj, "title") and obj.title:
        return obj.title
    
    # Check for annotations.title (for tools)
    if hasattr(obj, "annotations") and obj.annotations:
        if hasattr(obj.annotations, "title") and obj.annotations.title:
            return obj.annotations.title
    
    # Fall back to name
    if hasattr(obj, "name") and obj.name:
        return obj.name
    
    return "Unknown"


async def display_tools(session: ClientSession):
    """Display available tools with proper names."""
    tools = await session.list_tools()
    for tool in tools.tools:
        display_name = get_display_name(tool)
        logger.info(f"Tool: {display_name} ({tool.name})")


async def display_resources(session: ClientSession):
    """Display available resources with proper names."""
    resources = await session.list_resources()
    for resource in resources.resources:
        display_name = get_display_name(resource)
        logger.info(f"Resource: {display_name} ({resource.uri})")


# ============================================================================
# Example 6: Complete Client Workflow
# ============================================================================

async def complete_client_workflow():
    """
    Complete example of a client workflow:
    1. Connect to server
    2. Discover tools and resources
    3. Execute tools
    4. Handle results
    5. Access resources
    """
    server_params = StdioServerParameters(
        command="python",
        args=["path/to/mcp_server.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Step 1: Initialize
            await session.initialize()
            logger.info("Connected to MCP server")
            
            # Step 2: Discover tools
            tools_response = await session.list_tools()
            logger.info(f"Discovered {len(tools_response.tools)} tools")
            
            # Step 3: Execute a tool
            if tools_response.tools:
                first_tool = tools_response.tools[0]
                logger.info(f"Calling tool: {first_tool.name}")
                
                # Prepare arguments based on tool schema
                arguments = {}
                if hasattr(first_tool, "inputSchema"):
                    # In production, build arguments based on schema
                    pass
                
                result = await session.call_tool(first_tool.name, arguments)
                
                # Step 4: Handle results
                if result.isError:
                    logger.error("Tool execution failed")
                else:
                    for content in result.content:
                        if isinstance(content, types.TextContent):
                            logger.info(f"Result: {content.text}")
            
            # Step 5: Access resources
            resources_response = await session.list_resources()
            logger.info(f"Discovered {len(resources_response.resources)} resources")
            
            if resources_response.resources:
                first_resource = resources_response.resources[0]
                logger.info(f"Reading resource: {first_resource.uri}")
                
                try:
                    resource_content = await session.read_resource(first_resource.uri)
                    logger.info(f"Resource content: {resource_content.contents}")
                except Exception as e:
                    logger.error(f"Failed to read resource: {e}")


# ============================================================================
# Main Execution
# ============================================================================

async def main():
    """Run client examples."""
    logger.info("Running basic stdio client example...")
    # Uncomment to run:
    # await basic_stdio_client_example()
    
    logger.info("Running HTTP client example...")
    # Uncomment to run:
    # await http_client_example()
    
    logger.info("Running complete workflow example...")
    # Uncomment to run:
    # await complete_client_workflow()


if __name__ == "__main__":
    asyncio.run(main())
