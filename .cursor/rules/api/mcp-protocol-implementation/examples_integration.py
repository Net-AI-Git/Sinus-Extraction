"""
MCP Integration Patterns and Orchestration Examples

This file contains examples for integrating MCP with agent systems,
including single server architecture, dynamic tool discovery, and orchestration.
Reference these examples from RULE.md using @examples_integration.py syntax.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional
from enum import Enum

from mcp import ClientSession, types
from mcp.client.stdio import stdio_client, StdioServerParameters

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============================================================================
# Example 1: Single MCP Server Architecture
# ============================================================================

class AgentProfile(str, Enum):
    """Agent profile types for tool filtering."""
    DATA_AGENT = "data_agent"
    COMMUNICATION_AGENT = "communication_agent"
    ANALYST = "analyst"
    GENERAL = "general"


class MCPOrchestrator:
    """
    Orchestrator for managing MCP client connections and tool discovery.
    
    This class implements the single MCP server pattern where one server
    serves multiple agents with different tool sets based on profiles/scopes.
    """
    
    def __init__(self, server_params: StdioServerParameters):
        """
        Initialize the orchestrator.
        
        Args:
            server_params: Parameters for connecting to the MCP server
        """
        self.server_params = server_params
        self.session: Optional[ClientSession] = None
        self.read_stream = None
        self.write_stream = None
    
    async def connect(self):
        """Establish connection to MCP server."""
        stdio_ctx = stdio_client(self.server_params)
        self.read_stream, self.write_stream = await stdio_ctx.__aenter__()
        self.session = ClientSession(self.read_stream, self.write_stream)
        await self.session.__aenter__()
        await self.session.initialize()
        logger.info("Connected to MCP server")
    
    async def disconnect(self):
        """Close connection to MCP server."""
        if self.session:
            await self.session.__aexit__(None, None, None)
        logger.info("Disconnected from MCP server")
    
    async def get_tools_for_agent(
        self,
        agent_profile: AgentProfile,
        scopes: Optional[List[str]] = None
    ) -> List[types.Tool]:
        """
        Get tools available for a specific agent profile.
        
        Args:
            agent_profile: The agent's profile type
            scopes: Optional list of scopes to filter by
        
        Returns:
            List of tools available for this agent
        """
        if not self.session:
            raise RuntimeError("Not connected to MCP server")
        
        # In a real implementation, the server would filter tools based on
        # agent_profile and scopes. For this example, we get all tools and
        # filter client-side (server-side filtering is preferred)
        tools_response = await self.session.list_tools()
        
        # Client-side filtering based on tool metadata
        # In production, this should be done server-side
        filtered_tools = []
        for tool in tools_response.tools:
            # Check if tool matches agent profile
            # This is a simplified example - real implementation would
            # use tool metadata or server-side filtering
            if self._tool_matches_profile(tool, agent_profile, scopes):
                filtered_tools.append(tool)
        
        logger.info(
            f"Agent {agent_profile} has access to {len(filtered_tools)} tools"
        )
        return filtered_tools
    
    def _tool_matches_profile(
        self,
        tool: types.Tool,
        profile: AgentProfile,
        scopes: Optional[List[str]]
    ) -> bool:
        """
        Check if a tool matches the agent profile and scopes.
        
        This is a simplified example. In production, use tool metadata
        or server-side filtering.
        
        Args:
            tool: Tool to check
            profile: Agent profile
            scopes: Optional scopes
        
        Returns:
            True if tool matches profile/scopes
        """
        # Simplified matching logic
        # In production, this would use tool annotations or metadata
        tool_name = tool.name.lower()
        
        if profile == AgentProfile.DATA_AGENT:
            return any(keyword in tool_name for keyword in ["file", "data", "query"])
        elif profile == AgentProfile.COMMUNICATION_AGENT:
            return any(keyword in tool_name for keyword in ["email", "message", "send"])
        elif profile == AgentProfile.ANALYST:
            return any(keyword in tool_name for keyword in ["analyze", "data", "report"])
        
        # General profile gets all tools
        return True
    
    async def execute_tool(
        self,
        tool_name: str,
        arguments: Dict[str, Any]
    ) -> types.CallToolResult:
        """
        Execute a tool through the MCP server.
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Tool arguments
        
        Returns:
            Tool execution result
        """
        if not self.session:
            raise RuntimeError("Not connected to MCP server")
        
        logger.info(f"Executing tool: {tool_name}")
        result = await self.session.call_tool(tool_name, arguments)
        
        if result.isError:
            logger.error(f"Tool execution failed: {tool_name}")
        else:
            logger.info(f"Tool execution succeeded: {tool_name}")
        
        return result


# ============================================================================
# Example 2: Dynamic Tool Discovery Pattern
# ============================================================================

class DynamicToolAgent:
    """
    Agent that discovers tools dynamically at runtime.
    
    This agent has no hardcoded tool dependencies - it discovers
    available tools from the MCP server and uses them dynamically.
    """
    
    def __init__(self, orchestrator: MCPOrchestrator, profile: AgentProfile):
        """
        Initialize the agent.
        
        Args:
            orchestrator: MCP orchestrator instance
            profile: Agent profile for tool filtering
        """
        self.orchestrator = orchestrator
        self.profile = profile
        self.available_tools: List[types.Tool] = []
        self.tool_cache: Dict[str, types.Tool] = {}
    
    async def discover_tools(self, scopes: Optional[List[str]] = None):
        """
        Discover available tools from MCP server.
        
        Args:
            scopes: Optional scopes to filter tools
        """
        self.available_tools = await self.orchestrator.get_tools_for_agent(
            self.profile,
            scopes
        )
        
        # Cache tools by name for quick lookup
        self.tool_cache = {tool.name: tool for tool in self.available_tools}
        
        logger.info(
            f"Agent discovered {len(self.available_tools)} tools: "
            f"{[t.name for t in self.available_tools]}"
        )
    
    def get_tool_schema(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """
        Get the input schema for a tool.
        
        Args:
            tool_name: Name of the tool
        
        Returns:
            Tool input schema or None if tool not found
        """
        tool = self.tool_cache.get(tool_name)
        if tool and hasattr(tool, "inputSchema"):
            return tool.inputSchema
        return None
    
    async def use_tool(
        self,
        tool_name: str,
        arguments: Dict[str, Any]
    ) -> types.CallToolResult:
        """
        Use a tool dynamically.
        
        Args:
            tool_name: Name of the tool to use
            arguments: Tool arguments
        
        Returns:
            Tool execution result
        """
        if tool_name not in self.tool_cache:
            raise ValueError(f"Tool not available: {tool_name}")
        
        return await self.orchestrator.execute_tool(tool_name, arguments)
    
    def get_tool_descriptions(self) -> str:
        """
        Get descriptions of all available tools for prompt inclusion.
        
        Returns:
            Formatted string with tool descriptions
        """
        descriptions = []
        for tool in self.available_tools:
            desc = f"- {tool.name}: {tool.description}"
            if hasattr(tool, "inputSchema"):
                desc += f" (Schema: {tool.inputSchema})"
            descriptions.append(desc)
        
        return "\n".join(descriptions)


# ============================================================================
# Example 3: Prompt Design for Dynamic Tools
# ============================================================================

def create_dynamic_tool_prompt(agent: DynamicToolAgent) -> str:
    """
    Create a prompt that works with dynamically discovered tools.
    
    This prompt doesn't hardcode tool names but provides guidelines
    for using whatever tools are available.
    
    Args:
        agent: Agent instance with discovered tools
    
    Returns:
        Formatted prompt string
    """
    tool_descriptions = agent.get_tool_descriptions()
    
    prompt = f"""
You are an AI agent with access to the following tools:

{tool_descriptions}

## Tool Usage Guidelines

### Goal
Your goal is to accomplish tasks using the available tools. You should:
- Understand what each tool does
- Choose the right tool for each task
- Use tools in the correct order when multiple steps are needed

### Legitimate Actions
- Use tools to read, write, or process data
- Use tools to communicate or send messages
- Use tools to analyze or transform information
- Combine multiple tools to accomplish complex tasks

### When NOT to Use Tools
- Do NOT use tools for tasks they are not designed for
- Do NOT use tools with invalid or missing required parameters
- Do NOT use tools that are not in your available tool list
- Do NOT bypass tool validation or error handling

### Preferred Thinking Order
1. **Understand the task**: What needs to be accomplished?
2. **Identify required tools**: Which tools can help?
3. **Check tool requirements**: What parameters are needed?
4. **Plan execution**: In what order should tools be called?
5. **Execute and validate**: Call tools and verify results
6. **Handle errors**: If a tool fails, try alternatives or report the issue

### Important Notes
- Tool availability may change - always check available tools before use
- Tool schemas define required and optional parameters
- Some tools may depend on results from other tools
- Always validate tool results before proceeding

Remember: You have access to these tools dynamically. Do not assume
any specific tools exist - always work with what is available.
"""
    
    return prompt


# ============================================================================
# Example 4: Complete Integration Workflow
# ============================================================================

async def complete_integration_example():
    """
    Complete example showing the integration pattern:
    1. Connect to single MCP server
    2. Create agents with different profiles
    3. Discover tools dynamically
    4. Execute tools based on agent capabilities
    """
    # Step 1: Create orchestrator and connect
    server_params = StdioServerParameters(
        command="python",
        args=["path/to/mcp_server.py"]
    )
    
    orchestrator = MCPOrchestrator(server_params)
    await orchestrator.connect()
    
    try:
        # Step 2: Create agents with different profiles
        data_agent = DynamicToolAgent(orchestrator, AgentProfile.DATA_AGENT)
        comm_agent = DynamicToolAgent(orchestrator, AgentProfile.COMMUNICATION_AGENT)
        
        # Step 3: Discover tools for each agent
        await data_agent.discover_tools()
        await comm_agent.discover_tools()
        
        # Step 4: Create prompts with dynamic tool information
        data_prompt = create_dynamic_tool_prompt(data_agent)
        comm_prompt = create_dynamic_tool_prompt(comm_agent)
        
        logger.info("Data agent prompt created with dynamic tools")
        logger.info("Communication agent prompt created with dynamic tools")
        
        # Step 5: Example tool execution
        if data_agent.available_tools:
            first_tool = data_agent.available_tools[0]
            logger.info(f"Data agent using tool: {first_tool.name}")
            # result = await data_agent.use_tool(first_tool.name, {})
        
        if comm_agent.available_tools:
            first_tool = comm_agent.available_tools[0]
            logger.info(f"Comm agent using tool: {first_tool.name}")
            # result = await comm_agent.use_tool(first_tool.name, {})
    
    finally:
        # Step 6: Cleanup
        await orchestrator.disconnect()


# ============================================================================
# Example 5: Views/Profiles/Scopes Implementation
# ============================================================================

class ToolScope(str, Enum):
    """Tool scope definitions."""
    FILE_OPERATIONS = "file_operations"
    DATA_ACCESS = "data_access"
    DATA_ANALYSIS = "data_analysis"
    COMMUNICATION = "communication"
    SYSTEM_ADMIN = "system_admin"


class AgentView:
    """
    Represents an agent's view of available tools.
    
    This implements the Views/Profiles/Scopes pattern where different
    agents see different subsets of tools based on their configuration.
    """
    
    def __init__(
        self,
        profile: AgentProfile,
        scopes: List[ToolScope],
        orchestrator: MCPOrchestrator
    ):
        """
        Initialize agent view.
        
        Args:
            profile: Agent profile type
            scopes: List of tool scopes this agent has access to
            orchestrator: MCP orchestrator instance
        """
        self.profile = profile
        self.scopes = scopes
        self.orchestrator = orchestrator
        self.tools: List[types.Tool] = []
    
    async def refresh_tools(self):
        """Refresh the list of available tools for this view."""
        scope_strings = [scope.value for scope in self.scopes]
        self.tools = await self.orchestrator.get_tools_for_agent(
            self.profile,
            scope_strings
        )
        logger.info(
            f"View refreshed: {self.profile} with scopes {self.scopes} "
            f"has {len(self.tools)} tools"
        )
    
    def get_tool_by_name(self, name: str) -> Optional[types.Tool]:
        """Get a tool by name from this view."""
        for tool in self.tools:
            if tool.name == name:
                return tool
        return None
    
    def has_tool(self, name: str) -> bool:
        """Check if a tool is available in this view."""
        return self.get_tool_by_name(name) is not None


# ============================================================================
# Main Execution
# ============================================================================

async def main():
    """Run integration examples."""
    logger.info("Running complete integration example...")
    # Uncomment to run:
    # await complete_integration_example()


if __name__ == "__main__":
    asyncio.run(main())
