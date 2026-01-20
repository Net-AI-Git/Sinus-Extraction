# Run All Monitoring

## Overview
Execute all monitoring commands in sequence: LangSmith trace analysis, performance analysis, and comprehensive system analysis. This master command runs the complete monitoring workflow to analyze system performance, identify bottlenecks, and provide holistic insights.

## Rules Applied
- `monitoring-and-observability` - Metrics, tracing, log aggregation, LangSmith integration
- `performance-optimization` - Performance optimization strategies, bottleneck identification
- `agentic-logic-and-tools` - Tool usage patterns, agent internals
- `error-handling-and-resilience` - Error patterns, retry strategies, error impact analysis
- `cost-and-budget-management` - Cost analysis, token usage optimization
- `model-routing-and-selection` - Model selection analysis
- `deployment-and-infrastructure` - Infrastructure performance
- `rate-limiting-and-queue-management` - Queue performance
- `audit-protocol` - Audit trail analysis
- `llm-evaluation-and-metrics` - Evaluation results
- `tests-and-validation` - Test results
- `security-governance-and-observability` - Security analysis
- `human-in-the-loop-approval` - Human intervention analysis

## Steps

1. **Analyze LangSmith Traces**
   - Execute `/monitoring/analyze-langsmith-traces` command
   - Wait for completion and review results
   - **Error Handling**:
     - If trace analysis fails: Continue with warning, report data availability issues
     - If traces unavailable: Skip this step, continue with available data
     - If analysis completes: Proceed to next step
   - **Output**: LangSmith trace analysis report with LLM calls, tool usage, agent steps

2. **Performance Analysis**
   - Execute `/monitoring/performance-analysis` command
   - Wait for completion and review results
   - **Error Handling**:
     - If performance analysis fails: Continue with warning, report data availability issues
     - If metrics unavailable: Skip this step, continue with available data
     - If analysis completes: Proceed to next step
   - **Output**: Performance analysis report with latency, throughput, resource usage

3. **Comprehensive System Analysis**
   - Execute `/monitoring/comprehensive-system-analysis` command (uses results from steps 1 and 2)
   - Wait for completion and review results
   - **Error Handling**:
     - If comprehensive analysis fails: Report error but include partial results
     - If analysis completes: Generate final report
   - **Output**: Comprehensive system analysis report with cross-system correlations

4. **Generate Comprehensive Monitoring Report**
   - **System Health Dashboard**: Create dashboard with key metrics and health indicators
   - **Trend Analysis**: Analyze trends across all monitoring dimensions
   - **Alerting Recommendations**: Provide recommendations for setting up alerts based on findings
   - Aggregate results from all three commands
   - Create summary with overall system health status (Healthy/Degraded/Critical)
   - Highlight performance bottlenecks and anomalies with severity classification
   - Provide prioritized optimization recommendations with impact assessment
   - Include links to detailed reports from each command
   - **Monitoring Insights**: Key insights and patterns identified across all monitoring data

## Data Sources
- Results from `/monitoring/analyze-langsmith-traces` command
- Results from `/monitoring/performance-analysis` command
- Results from `/monitoring/comprehensive-system-analysis` command
- LangSmith traces (JSON format)
- Performance metrics
- Audit logs (JSON format)

## Output
A comprehensive monitoring report including:
- **Overall System Health**: Healthy/Degraded/Critical with health score
- **System Health Dashboard**: Key metrics, health indicators, component health status
- **LangSmith Analysis Summary**: LLM calls, tool usage, agent steps, bottlenecks, cost analysis, model selection
- **Performance Analysis Summary**: Latency, throughput, resource usage, SLI/SLO compliance, capacity planning, optimization opportunities
- **Comprehensive Analysis Summary**: Cross-system correlations, patterns, anomalies, system health scoring, predictive analysis
- **Trend Analysis**: Performance trends, cost trends, error trends, health trends
- **Critical Issues**: Performance bottlenecks and system issues with severity classification
- **Alerting Recommendations**: Suggested alerts based on findings with thresholds
- **Prioritized Recommendations**: Optimization suggestions with impact assessment and implementation guidance
- **Monitoring Insights**: Key insights and patterns identified across all monitoring data
- **Next Steps**: Actionable performance improvements with priority levels

## Execution Flow
```
analyze-langsmith-traces → performance-analysis → comprehensive-system-analysis → Final Report
           ↓                        ↓                           ↓
      [Continue]              [Continue]                  [Aggregate Results]
```

## Notes
- Each command can be run independently if needed
- Master command provides workflow orchestration
- Comprehensive system analysis uses results from trace and performance analysis
- All reports are preserved for detailed analysis
