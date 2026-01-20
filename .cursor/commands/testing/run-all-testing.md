# Run All Testing

## Overview
Execute all testing commands in sequence: test suite, evaluation suite, and LLM Judge evaluation. This master command runs the complete testing workflow to ensure code quality, functionality, and agent performance.

## Rules Applied
- `tests-and-validation` - Testing framework standards and validation requirements
- `llm-evaluation-and-metrics` - LLM evaluation standards and mandatory metrics
- `llm-judge-protocol` - LLM Judge evaluation protocol and rubric
- `core-python-standards` - Code quality standards and best practices
- `error-handling-and-resilience` - Error handling patterns, error classification, retry strategies
- `monitoring-and-observability` - Test execution metrics, logging, LangSmith tracing
- `performance-optimization` - Test performance analysis, efficiency metrics
- `data-schemas-and-interfaces` - Evaluation data structures and Pydantic schemas
- `audit-protocol` - Audit trail requirements and log structure
- `security-governance-and-observability` - Security and privacy checks, PII leakage detection

## Steps

1. **Run Test Suite**
   - Execute `/testing/run-test-suite` command
   - Wait for completion and review results
   - **Comprehensive Error Handling**: 
     - **Critical Failures**: If tests fail with blocking issues, stop execution and report
     - **Non-Critical Failures**: If tests fail with non-blocking issues, continue with warning
     - **Warnings**: If tests pass with warnings, continue with warning notification
     - **Success**: If all tests pass, proceed to next step
     - **Dependency Check**: Verify test suite completion before proceeding to evaluation
   - **Output**: Test execution report with pass/fail status, coverage metrics, performance data

2. **Run Evaluation Suite**
   - Execute `/testing/run-evaluation-suite` command
   - Wait for completion and review results
   - **Comprehensive Error Handling**:
     - **Critical Failures**: If evaluation fails completely, stop execution and report blocking issues
     - **Threshold Failures**: If evaluation scores below threshold, continue with warning, include in final report
     - **Partial Failures**: If some metrics fail but others pass, continue with warning
     - **Success**: If evaluation passes all thresholds, proceed to next step
     - **Dependency Check**: Verify evaluation suite completion before proceeding to LLM Judge
   - **Output**: Evaluation report with metrics scores, cost analysis, trend comparison

3. **Evaluate with LLM Judge**
   - Execute `/testing/evaluate-with-llm-judge` command
   - Wait for completion and review results
   - **Comprehensive Error Handling**:
     - **Critical Failures**: If LLM Judge evaluation fails completely, report error but include partial results
     - **FAIL Verdict**: If verdict is FAIL, include in final report as critical issue requiring immediate attention
     - **WARNING Verdict**: If verdict is WARNING, include in final report as non-blocking issue
     - **PASS Verdict**: If verdict is PASS, include in final report as success
     - **Partial Results**: Always include partial results even if evaluation fails
   - **Output**: LLM Judge evaluation report with score, verdict, efficiency rating, security assessment

4. **Generate Comprehensive Testing Report**
   - **Aggregated Reporting**:
     - Aggregate results from all three commands (test suite, evaluation suite, LLM Judge)
     - Combine metrics, scores, and findings into unified report
     - Cross-reference findings across different evaluation methods
   - **Dependency Management**:
     - Document command execution order and dependencies
     - Track which commands completed successfully
     - Identify dependencies between test results and evaluation results
   - Create summary with overall testing status (Pass/Fail/Needs Attention)
   - Highlight critical issues from all stages with severity classification
   - Provide prioritized recommendations across all testing dimensions
   - Include links to detailed reports from each command
   - **Trend Analysis**: Compare current results with previous runs if available

## Data Sources
- Results from `/testing/run-test-suite` command
- Results from `/testing/run-evaluation-suite` command
- Results from `/testing/evaluate-with-llm-judge` command

## Output
A comprehensive testing report including:
- **Overall Testing Status**: Pass/Fail/Needs Attention with justification
- **Test Suite Summary**: Pass rate, failures, execution time, coverage metrics, performance data
- **Evaluation Suite Summary**: Metrics scores, quality assessment, cost analysis, trend comparison
- **LLM Judge Summary**: Score, verdict, critical failures, efficiency rating, security assessment
- **Aggregated Metrics**: Combined metrics across all testing methods
- **Cross-Reference Analysis**: Correlations between test results, evaluation results, and LLM Judge findings
- **Critical Issues**: Blocking issues that must be addressed, classified by severity
- **Recommendations**: Prioritized suggestions for improvements across all testing dimensions
- **Dependency Status**: Command execution status and dependency fulfillment
- **Next Steps**: Actionable items based on all testing results with priority levels

## Execution Flow
```
run-test-suite → [Pass?] → run-evaluation-suite → [Pass?] → evaluate-with-llm-judge → Final Report
                    ↓ Fail                              ↓ Fail                              ↓
                 [Stop]                              [Stop]                          [Report & Continue]
```

## Notes
- Each command can be run independently if needed
- Master command provides workflow orchestration
- Error handling ensures critical issues are not missed
- All reports are preserved for detailed analysis
