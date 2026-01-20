# Create Agent Node

## Overview
Create a new LangGraph node following the four-part structure (READ → DO → WRITE → CONTROL) with proper state management, error handling, and integration into the existing workflow.

## Rules Applied
- `langgraph-architecture-and-nodes` - Node implementation rules, four-part structure, state field ownership
- `core-python-standards` - Code quality standards, function length, type hints, logging
- `error-handling-and-resilience` - Error handling patterns, retry strategies, error classification
- `multi-agent-systems` - Multi-agent patterns, node role in multi-agent system
- `tests-and-validation` - Test creation, test structure, test coverage
- `monitoring-and-observability` - Node instrumentation, metrics collection
- `performance-optimization` - Node performance, efficiency considerations
- `reflection-and-self-critique` - Self-critique patterns, reflection mechanisms

## Steps

1. **Define Node Purpose**
   - **Single Purpose**:
     - Define exactly one logical task for the node
     - Ensure node does not mix heavy work with routing decisions
     - Verify node purpose aligns with workflow design
   - **State Field Ownership**:
     - Identify which state fields this node will own
     - Ensure no other node writes to these fields
     - Document field ownership clearly

2. **Implement READ Phase (Inputs)**
   - **Read State Fields**:
     - Read necessary inputs from Global State
     - Read assigned SECTION if worker node
     - Read shared context from SHARED_STATE if needed
   - **Input Validation**:
     - Validate required inputs are present
     - Check input types and formats
     - Handle missing or invalid inputs gracefully

3. **Implement DO Phase (Logic/Tool)**
   - **Core Logic**:
     - Implement the node's core functionality
     - Keep logic focused on single purpose
     - Ensure functions are under 20 lines (split if needed)
   - **Tool Calls** (if applicable):
     - Call tools using proper tool binding
     - Handle tool execution results
     - Implement retry logic for transient errors
   - **Error Handling**:
     - Wrap core logic in try/except
     - Classify errors (transient vs permanent)
     - Append errors to dedicated `errors` field in state
     - Route persistent failures to error-handling nodes

4. **Implement WRITE Phase (Outputs)**
   - **State Updates**:
     - Write results to owned state fields
     - Update state with node execution results
     - Ensure state updates are atomic
   - **Output Format**:
     - Format outputs according to state schema
     - Include execution metadata if needed
     - Ensure outputs are properly typed

5. **Implement CONTROL Phase (Next Action)**
   - **Routing Logic**:
     - Determine next node based on execution results
     - Use conditional routing via edges (not inline logic)
     - Support loops and branching via graph structure
   - **State Aggregation**:
     - Add agent summaries to `messages` list in Global State
     - Include `summary_for_supervisor` if applicable
   - **Error Routing**:
     - Route to error-handling nodes on persistent failures
     - Route to human review nodes if needed
     - Reset ERROR_COUNT on success

6. **Add Error Handling**
   - **Error Classification**:
     - Classify errors at point of occurrence
     - Use typed exceptions or error codes
   - **Retry Logic**:
     - Implement retry with exponential backoff for transient errors
     - Use `@retry` decorator from Tenacity
     - Configure retry conditions explicitly
   - **State Error Tracking**:
     - Append errors to `errors` field in state
     - Include error context and classification
     - Track error count for routing decisions

7. **Create Tests**
   - **Test Structure**:
     - Create test file `test_<node_name>.py` in `tests/` directory
     - Use Arrange-Act-Assert pattern
     - Ensure tests are atomic and independent
   - **Test Cases**:
     - Test READ phase with various input states
     - Test DO phase with different scenarios
     - Test WRITE phase output format
     - Test CONTROL phase routing logic
     - Test error handling and recovery
   - **Mocking**:
     - Mock external dependencies (LLMs, tools, databases)
     - Use mocks/fakes for deterministic tests
     - Only integration tests should hit real APIs

8. **Update Workflow**
   - **Add Node to Workflow**:
     - Add node to LangGraph workflow
     - Define edges for node connections
     - Update conditional routing logic
   - **Update Visualization**:
     - Regenerate graph visualization
     - Verify node appears correctly in graph
     - Check edges and routing are correct

9. **Documentation**
   - **Node Documentation**:
     - Document node purpose and responsibilities
     - Document state field ownership
     - Document input/output requirements
     - Document error handling behavior
   - **Code Documentation**:
     - Add docstrings to all public functions
     - Include type hints for all parameters
     - Document complex logic with comments

10. **Node Validation Checklist**
    - **Node Structure Validation**: Verify READ → DO → WRITE → CONTROL structure
    - **State Field Ownership**: Verify state field ownership is correct
    - **Error Handling Validation**: Verify error handling is comprehensive
    - **Performance Considerations**: Check performance implications
    - **Node Testing Requirements**: Verify test coverage meets requirements
    - **Multi-Agent Compliance**: Verify node follows multi-agent patterns if applicable

11. **Generate Node Creation Report**
    - Create node creation summary
    - Document node structure and implementation
    - Include test coverage information
    - **Node Validation Results**: Validation checklist results
    - **Performance Analysis**: Performance considerations and recommendations
    - **Node Testing Status**: Test coverage and test quality assessment
    - Provide integration status

## Data Sources
- Existing workflow structure and state schema
- Node requirements and specifications
- Related nodes for integration context
- Tool definitions if node uses tools

## Output
A complete agent node implementation including:
- **Node Implementation**: Complete node with READ → DO → WRITE → CONTROL structure
- **State Integration**: Proper state field ownership and updates
- **Error Handling**: Comprehensive error handling with retry logic and error classification
- **Multi-Agent Compliance**: Node follows multi-agent patterns and role requirements
- **Node Instrumentation**: Monitoring and observability instrumentation
- **Performance Considerations**: Performance analysis and optimization recommendations
- **Self-Critique Patterns**: Reflection and self-critique mechanisms if applicable
- **Tests**: Complete test suite with good coverage meeting test requirements
- **Node Validation**: Validation checklist results and compliance status
- **Workflow Integration**: Node added to workflow with proper edges
- **Documentation**: Complete node and code documentation
- **Visualization Update**: Updated workflow graph visualization
- **Creation Report**: Summary of node creation with validation results and next steps
