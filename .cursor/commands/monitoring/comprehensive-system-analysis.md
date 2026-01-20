# Comprehensive System Analysis

## Overview
Complete cross-system analysis combining all available data sources (LangSmith traces, audit logs, test results, evaluation results) to provide holistic insights into system performance, quality, security, and compliance. This command correlates data across systems to identify patterns, anomalies, and improvement opportunities.

## Rules Applied
- All relevant rules from the codebase
- `monitoring-and-observability` - Metrics, tracing, log aggregation
- `audit-protocol` - Audit trail analysis
- `llm-evaluation-and-metrics` - Evaluation results
- `tests-and-validation` - Test results
- `security-governance-and-observability` - Security analysis
- `performance-optimization` - System-wide performance analysis
- `cost-and-budget-management` - Cost analysis across systems
- `error-handling-and-resilience` - System-wide error patterns
- `human-in-the-loop-approval` - Human intervention analysis

## Steps

1. **Collect All Data Sources**
   - **LangSmith Traces**:
     - Read LangSmith trace files (JSON format)
     - Extract LLM operations, tool calls, agent steps
     - Collect performance metrics and token usage
   - **Audit Logs**:
     - Read audit log files (JSON format)
     - Extract events (tool calls, state changes, API requests, data access)
     - Collect security and compliance events
   - **Test Results**:
     - Read test execution results
     - Extract test pass/fail status
     - Collect test coverage metrics
   - **Evaluation Results**:
     - Read evaluation suite results
     - Extract evaluation metrics (Faithfulness, Answer Relevance, etc.)
     - Collect LLM Judge evaluation results
   - **Performance Metrics**:
     - Collect system resource usage (CPU, memory, network)
     - Extract latency and throughput metrics
     - Gather cache hit rates and optimization metrics

2. **Correlate Data Across Systems**
   - **Time-Based Correlation**:
     - Correlate events by timestamp across systems
     - Identify temporal patterns and relationships
     - Link related events across different systems
   - **Request-Based Correlation**:
     - Use correlation IDs to link events across systems
     - Trace request flow from API to agent to tools
     - Identify end-to-end request patterns
   - **User/Agent-Based Correlation**:
     - Correlate events by user ID or agent ID
     - Identify user/agent behavior patterns
     - Track user/agent performance over time

3. **Identify Patterns**
   - **Operational Patterns**:
     - Identify common execution patterns
     - Detect recurring workflows
     - Find typical tool usage sequences
   - **Performance Patterns**:
     - Identify performance trends
     - Detect latency patterns
     - Find resource usage patterns
   - **Error Patterns**:
     - Identify recurring error types
     - Detect error sequences
     - Find error-prone operations
   - **Usage Patterns**:
     - Identify user behavior patterns
     - Detect feature usage patterns
     - Find access patterns

4. **Identify Anomalies**
   - **Performance Anomalies**:
     - Detect unusual latency spikes
     - Identify resource usage anomalies
     - Find performance degradation patterns
   - **Security Anomalies**:
     - Detect unusual access patterns
     - Identify suspicious activities
     - Find potential security incidents
   - **Quality Anomalies**:
     - Detect evaluation score drops
     - Identify test failure patterns
     - Find quality degradation trends
   - **Operational Anomalies**:
     - Detect unusual tool usage
     - Identify unexpected agent behaviors
     - Find system state anomalies

5. **Cross-System Analysis**
   - **Performance vs Quality**:
     - Correlate performance metrics with quality metrics
     - Identify trade-offs between speed and quality
     - Find optimization opportunities
   - **Security vs Usability**:
     - Analyze security controls impact on usability
     - Identify security-usability trade-offs
     - Find balance opportunities
   - **Errors vs Performance**:
     - Correlate error rates with performance
     - Identify error impact on performance
     - Find error prevention opportunities

6. **System Health Scoring**
   - **Health Metrics**: Calculate system health score based on all metrics
   - **Component Health**: Assess health of individual system components
   - **Health Trends**: Track system health trends over time
   - **Health Predictions**: Predict future health based on trends

7. **Predictive Analysis**
   - **Trend Projections**: Project future trends based on historical data
   - **Anomaly Prediction**: Predict potential future anomalies
   - **Capacity Projections**: Project future capacity needs
   - **Risk Assessment**: Assess risks based on current patterns

8. **Generate Comprehensive Report**
   - Create holistic system analysis report
   - Include analysis from all data sources
   - Provide cross-system correlations
   - Highlight patterns and anomalies
   - Include system health scoring
   - Provide predictive analysis and projections
   - Include prioritized recommendations
   - Provide actionable insights

## Data Sources
- LangSmith traces (JSON format) from local files
- Audit logs (JSON format) from local files
- Test results from test execution
- Evaluation results from evaluation suite
- Performance metrics from monitoring systems
- System configuration files

## Output
A comprehensive system analysis report including:
- **Data Source Summary**: Overview of all collected data from all systems
- **Cross-System Correlations**: Relationships between different systems with correlation analysis
- **Pattern Identification**: Operational, performance, error, usage, and cost patterns
- **Anomaly Detection**: Performance, security, quality, operational, and cost anomalies
- **Cross-System Analysis**: Performance vs quality, security vs usability, errors vs performance, cost vs efficiency
- **System-Wide Performance**: Overall performance metrics across all systems
- **System-Wide Cost Analysis**: Cost breakdown and trends across all systems
- **System-Wide Error Patterns**: Error patterns and trends across all systems
- **Human Intervention Analysis**: Human intervention patterns and effectiveness
- **System Health Scoring**: Overall system health score, component health, health trends
- **Predictive Analysis**: Trend projections, anomaly predictions, capacity projections, risk assessment
- **Holistic Insights**: System-wide observations and trends
- **Prioritized Recommendations**: Actionable improvements across all systems with impact assessment
- **System Health Assessment**: Overall system health and status with health predictions
