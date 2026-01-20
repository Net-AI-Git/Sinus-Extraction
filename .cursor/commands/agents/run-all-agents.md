# Run All Agents

## Overview
Execute all agent development commands in sequence: setup new agent system, create agent node, and implement agent tool. This master command provides a complete workflow for developing new agent systems from scratch.

## Rules Applied
- `multi-agent-systems` - Multi-agent architecture patterns, Orchestrator/Worker/Synthesizer
- `langgraph-architecture-and-nodes` - LangGraph workflow design, node implementation
- `agentic-logic-and-tools` - LangChain fundamentals, tool definitions, agent internals
- `core-python-standards` - Code quality standards, function length, type hints, logging
- `configuration-and-dependency-injection` - Configuration setup, pydantic-settings
- `data-schemas-and-interfaces` - Schema definitions, Pydantic models
- `prompt-engineering-and-management` - Prompt setup, prompt templates
- `error-handling-and-resilience` - Error handling, retry strategies, error classification
- `human-in-the-loop-approval` - Human-in-the-loop setup, approval workflows
- `cost-and-budget-management` - Budget setup, cost tracking
- `rate-limiting-and-queue-management` - Rate limiting setup, queue management
- `tests-and-validation` - Test creation, test structure
- `monitoring-and-observability` - Node instrumentation, tool instrumentation
- `performance-optimization` - Node performance, tool performance
- `reflection-and-self-critique` - Self-critique patterns
- `security-governance-and-observability` - Tool security, access control
- `prompt-injection-prevention` - Tool input validation

## Steps

1. **Setup New Agent System**
   - Execute `/agents/setup-new-agent-system` command
   - Wait for completion and review results
   - **Error Handling**:
     - If setup fails: Stop execution, report blocking issues
     - If setup completes with warnings: Continue with warning notification
     - If setup completes successfully: Proceed to next step
   - **Output**: Agent system setup report with project structure and workflow definition

2. **Create Agent Node**
   - Execute `/agents/create-agent-node` command
   - Wait for completion and review results
   - **Error Handling**:
     - If node creation fails: Stop execution, report blocking issues
     - If node creation completes with issues: Continue with warning, include in final report
     - If node creation completes successfully: Proceed to next step
   - **Output**: Agent node creation report with node implementation and tests

3. **Implement Agent Tool**
   - Execute `/agents/implement-agent-tool` command
   - Wait for completion and review results
   - **Error Handling**:
     - If tool implementation fails: Report error but include partial results
     - If tool implementation completes with issues: Include in final report
     - If tool implementation completes successfully: Generate final report
   - **Output**: Agent tool implementation report with tool definition and tests

4. **Generate Comprehensive Agent Development Report**
   - **Agent System Validation**: Verify agent system is properly configured and functional
   - **Workflow Verification**: Verify workflow is correctly structured and integrated
   - Aggregate results from all three commands
   - Create summary with overall agent development status (Complete/In Progress/Needs Attention)
   - Highlight setup, node creation, and tool implementation status with validation results
   - **Comprehensive Setup Report**: Include setup checklist, architecture validation, verification results
   - Provide recommendations for next steps with priority levels
   - Include links to detailed reports from each command

## Data Sources
- Results from `/agents/setup-new-agent-system` command
- Results from `/agents/create-agent-node` command
- Results from `/agents/implement-agent-tool` command

## Output
A comprehensive agent development report including:
- **Overall Development Status**: Complete/In Progress/Needs Attention with justification
- **Agent System Validation**: System configuration and functionality validation results
- **Workflow Verification**: Workflow structure and integration verification results
- **System Setup Summary**: Project structure, workflow definition, visualization, setup checklist, architecture validation
- **Node Creation Summary**: Node implementation, state integration, tests, node validation, performance analysis
- **Tool Implementation Summary**: Tool definition, LLM integration, tests, security validation, performance analysis
- **Configuration Status**: Environment, tool registry, budget, rate limiting, human-in-the-loop configuration
- **Issues and Recommendations**: Development issues and improvement suggestions with severity classification
- **Next Steps**: Actionable items for completing agent development with priority levels

## Execution Flow
```
setup-new-agent-system → create-agent-node → implement-agent-tool → Final Report
         ↓ Fail                  ↓ Fail                  ↓ Fail
      [Stop]                  [Stop]              [Report & Continue]
```

## Notes
- This is a sequential workflow - each step depends on the previous
- Each command can be run independently if needed
- Master command provides workflow orchestration for new agent development
- All reports are preserved for detailed analysis
