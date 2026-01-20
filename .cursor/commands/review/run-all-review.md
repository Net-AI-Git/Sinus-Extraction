# Run All Review

## Overview
Execute all review commands in sequence: code review checklist and final compliance check. This master command runs the complete review workflow to ensure code quality and compliance before commit.

## Rules Applied
- `code-review-and-collaboration` - Code review standards, PR review checklist, Git workflow
- `final-review-protocol` - Final review compliance checklist
- `core-python-standards` - Code quality standards, function length, type hints, logging
- `error-handling-and-resilience` - Error handling review, error classification, retry strategies
- `tests-and-validation` - Test coverage review, test quality standards
- `security-governance-and-observability` - Security review, vulnerability checks, access control
- `performance-optimization` - Performance review, efficiency checks
- `data-schemas-and-interfaces` - Data handling review, schema validation
- `langgraph-architecture-and-nodes` - LangGraph architecture standards
- `multi-agent-systems` - Multi-agent system patterns
- `configuration-and-dependency-injection` - Configuration management
- `prompt-engineering-and-management` - Prompt engineering standards
- `api-interface-and-streaming` - API standards
- `human-in-the-loop-approval` - Approval workflow checks
- `versioning-and-release-management` - Version compliance
- `rate-limiting-and-queue-management` - Rate limiting checks
- `deployment-and-infrastructure` - Deployment compliance
- `monitoring-and-observability` - Monitoring compliance
- `llm-evaluation-and-metrics` - Evaluation compliance

## Steps

1. **Code Review Checklist**
   - Execute `/review/code-review-checklist` command
   - Wait for completion and review results
   - **Error Handling**:
     - If code review fails: Stop execution and report blocking issues
     - If code review finds issues: Continue with warning, include in final report
     - If code review passes: Proceed to next step
   - **Output**: Code review report with checklist status

2. **Final Compliance Check**
   - Execute `/review/final-compliance-check` command (uses results from code review)
   - Wait for completion and review results
   - **Error Handling**:
     - If compliance check fails: Report blocking issues
     - If compliance issues found: Include in final report with severity
     - If compliance passes: Generate final report
   - **Output**: Comprehensive compliance report

3. **Generate Comprehensive Review Report**
   - **Review Workflow Orchestration**: Coordinate execution of both review commands
   - **Approval Status Tracking**: Track approval status and workflow requirements
   - Aggregate results from both commands
   - Create summary with overall review status (Pass/Fail/Needs Attention)
   - Highlight code quality issues and compliance gaps with severity classification
   - **Comprehensive Review Report**: Include all findings from code review and compliance check
   - Provide prioritized recommendations across all review dimensions
   - Include links to detailed reports from each command
   - **Approval Recommendation**: Provide overall approval recommendation with justification

## Data Sources
- Results from `/review/code-review-checklist` command
- Results from `/review/final-compliance-check` command

## Output
A comprehensive review report including:
- **Overall Review Status**: Pass/Fail/Needs Attention with justification
- **Code Review Summary**: Code quality, functionality, testing, documentation, security, performance, data handling
- **Compliance Summary**: Architecture, testing, error handling, performance, documentation, deployment, security, versioning, rate limiting, human-in-the-loop
- **Compliance Scoring**: Per-category compliance scores and overall score
- **Critical Issues**: Blocking issues that must be fixed before commit with severity classification
- **Approval Status**: Overall approval recommendation (Approve/Request Changes/Needs Discussion)
- **Review Workflow Status**: Execution status of both review commands
- **Recommendations**: Prioritized suggestions for improvements across all review dimensions
- **Next Steps**: Actionable items before proceeding with commit with priority levels

## Execution Flow
```
code-review-checklist → final-compliance-check → Final Report
         ↓ Fail                      ↓ Fail
      [Stop]                      [Stop]
```

## Notes
- Each command can be run independently if needed
- Master command provides workflow orchestration
- Final compliance check uses results from code review
- All reports are preserved for detailed analysis
