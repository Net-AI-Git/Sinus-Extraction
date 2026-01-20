# Evaluate with LLM Judge

## Overview
Comprehensive evaluation using LLM-as-a-Judge protocol to analyze agent system performance, safety, and logic based on multimodal dataset including execution traces, audit logs, performance metrics, and final outputs. This command provides deep analysis following the Supreme AI Adjudicator protocol.

## Rules Applied
- `llm-judge-protocol` - LLM Judge evaluation protocol, rubric, and structured output schema
- `audit-protocol` - Audit trail requirements and log structure
- `llm-evaluation-and-metrics` - Evaluation metrics and golden dataset standards
- `monitoring-and-observability` - LangSmith tracing, performance metrics, and trace analysis
- `error-handling-and-resilience` - Error analysis in evaluation, error classification
- `performance-optimization` - Efficiency rating analysis, resource waste detection
- `security-governance-and-observability` - Security and privacy checks, PII leakage detection

## Steps

1. **Collect Session Context**
   - **Execution Logs (JSON)**: Gather raw traces of steps, tool calls, and state updates
     - Search for execution logs in project directories
     - Look for JSON files containing trace data
     - Extract tool call sequences and parameters
     - **Enhanced Trace Analysis**: Analyze trace patterns, identify bottlenecks, detect anomalies
   - **Audit Comparison Tables**: Collect data showing expected vs actual values
     - Retrieve audit logs from local JSON files
     - Extract comparison tables for retrieval precision, math results, etc.
     - Identify discrepancies between expected and actual values
     - Classify discrepancies by severity and impact
   - **Performance Metrics**: Gather latency charts, token usage stats, CPU/Memory profiles
     - Extract performance data from LangSmith traces
     - Collect system resource usage metrics
     - Calculate latency percentiles (P50, P95, P99)
     - **Cost Efficiency Analysis**: Calculate cost per operation, identify wasteful operations
   - **Final Output**: Capture the actual response delivered to the user
     - Extract final agent output from execution logs
     - Compare with expected output if golden answer available
   - **Security and Privacy Data**: Collect security-related information
     - Check for PII leakage in outputs
     - Verify safety guardrails are functioning
     - Identify potential security vulnerabilities

2. **Prepare Evaluation Input**
   - Structure collected data into Session Context format
   - Organize execution logs chronologically
   - Prepare audit comparison tables with clear expected vs actual
   - Format performance metrics for analysis
   - Include final output with context

3. **Execute LLM Judge Evaluation**
   - Apply the evaluation rubric with weights:
     - **Functional Correctness (40%)**: Result verification, hallucination check, graph adherence
     - **Tool Usage & Reasoning (30%)**: Parameter validity, tool selection, error recovery
       - **Error Analysis**: Classify errors as transient vs permanent
       - Analyze error recovery strategies and effectiveness
     - **Operational Efficiency (20%)**: Step efficiency, resource waste, parallelism
       - **Cost Efficiency Analysis**: Calculate cost per operation, identify wasteful token usage
       - Detect unnecessary retries and redundant operations
     - **Security & Privacy (10%)**: PII leakage, safety guardrails
       - **Security Evaluation**: Check for prompt injection vulnerabilities
       - Verify data masking and PII protection
       - Validate access control and authorization
   - Generate reasoning block with:
     - **Enhanced Trace Analysis**: Chronological trace analysis with bottleneck identification
     - Anomaly identification (errors, retries, long pauses, cost spikes)
     - Data comparison (audit table discrepancies with severity classification)
     - **Security and Privacy Assessment**: Security vulnerability analysis, PII leakage check
     - Conclusion formulation with security and efficiency considerations

4. **Generate Structured Output**
   - Create JSON output following the protocol schema:
     ```json
     {
       "score": 0-100,
       "verdict": "PASS" | "FAIL" | "WARNING",
       "critical_failures": ["List of blocking issues"],
       "efficiency_rating": "OPTIMAL" | "SUBOPTIMAL" | "WASTEFUL",
       "reasoning_summary": "Concise explanation of the score",
       "suggestions": ["Specific actionable advice"]
     }
     ```
   - Ensure all fields are populated with detailed analysis

5. **Analyze Results**
   - Interpret the verdict and score
   - Review critical failures and their impact
   - Assess efficiency rating and resource usage
   - Understand reasoning summary and root causes

6. **Generate Comprehensive Report**
   - Create detailed report with:
     - Executive summary with verdict and score
     - Breakdown by evaluation dimension
     - Critical failures with context and impact
     - Efficiency analysis with specific examples
     - Detailed reasoning and trace analysis
     - Actionable suggestions prioritized by impact
   - Include visual indicators for quick assessment
   - Provide specific code/configuration recommendations

## Data Sources
- Execution logs (JSON traces) from local files
- Audit logs (JSON format) from audit storage
- LangSmith traces (JSON format) from local files
- Performance metrics from monitoring systems
- Final output from agent execution
- Golden answers (if available) for comparison

## Output
A comprehensive LLM Judge evaluation report including:
- **Structured JSON Output**: Score, verdict, critical failures, efficiency rating, reasoning, suggestions
- **Detailed Analysis**: Breakdown by evaluation dimensions (Functional Correctness, Tool Usage, Efficiency, Security) with specific examples
- **Enhanced Trace Analysis**: Chronological walkthrough with bottleneck identification, anomaly detection, and pattern analysis
- **Audit Comparison**: Expected vs actual value analysis with discrepancies highlighted and severity classification
- **Performance Analysis**: Resource usage, efficiency metrics, latency analysis, and optimization opportunities
- **Cost Efficiency Analysis**: Cost per operation, token usage optimization, wasteful operation identification
- **Security and Privacy Assessment**: PII leakage detection, security vulnerability analysis, safety guardrail verification
- **Error Analysis**: Error classification (transient vs permanent), error recovery effectiveness, retry pattern analysis
- **Actionable Recommendations**: Prioritized suggestions for improvement with specific guidance for each dimension
- **Visual Summary**: Quick assessment indicators and status overview
