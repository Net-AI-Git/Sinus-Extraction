# Run All Deployment

## Overview
Execute all deployment commands in sequence: pre-deployment check and post-deployment verification. This master command runs the complete deployment workflow to ensure successful and verified deployment.

## Rules Applied
- `deployment-and-infrastructure` - Deployment standards, CI/CD, Docker, Kubernetes, rollback procedures
- `final-review-protocol` - Final review compliance checklist
- `security-governance-and-observability` - Security governance, security verification
- `monitoring-and-observability` - Health checks, monitoring, metrics, alerting, tracing
- `tests-and-validation` - Testing requirements
- `llm-evaluation-and-metrics` - Evaluation requirements
- `performance-optimization` - Performance readiness, SLI/SLO validation, performance analysis
- `configuration-and-dependency-injection` - Configuration validation, secrets management
- `versioning-and-release-management` - Version validation, release management
- `rate-limiting-and-queue-management` - Rate limiting checks, queue configuration
- `error-handling-and-resilience` - Error monitoring, error recovery, error classification
- `audit-protocol` - Audit trail verification, compliance checks

## Steps

1. **Pre-Deployment Check**
   - Execute `/deployment/pre-deployment-check` command
   - Wait for completion and review results
   - **Error Handling**:
     - If pre-deployment check fails: Stop execution, do not proceed with deployment
     - If blocking issues found: Stop execution, require fixes before deployment
     - If non-blocking issues found: Continue with warning, include in final report
     - If check passes: Proceed to deployment (manual or automated)
   - **Output**: Pre-deployment report with deployment readiness status

2. **Post-Deployment Verification**
   - Execute `/deployment/post-deployment-verification` command
   - Wait for completion and review results
   - **Error Handling**:
     - If post-deployment verification fails: Report critical issues, consider rollback
     - If health checks fail: Report service issues, consider rollback
     - If verification passes: Generate final report
   - **Output**: Post-deployment verification report with system status

3. **Generate Comprehensive Deployment Report**
   - **Deployment Workflow Orchestration**: Coordinate execution of pre and post deployment checks
   - **Deployment Approval Workflow**: Document approval status and workflow requirements
   - **Deployment Metrics Tracking**: Track deployment metrics and success rates
   - Aggregate results from both commands
   - Create summary with overall deployment status (Success/Failed/Needs Attention)
   - Highlight pre-deployment issues and post-deployment status with severity classification
   - **Deployment Insights**: Key insights from deployment process
   - Provide recommendations for improvements with priority levels
   - Include links to detailed reports from each command

## Data Sources
- Results from `/deployment/pre-deployment-check` command
- Results from `/deployment/post-deployment-verification` command
- Health check endpoints
- Performance metrics
- Error logs

## Output
A comprehensive deployment report including:
- **Overall Deployment Status**: Success/Failed/Needs Attention with justification
- **Deployment Workflow Status**: Execution status of pre and post deployment checks
- **Pre-Deployment Summary**: Test results, evaluation results, security audit, compliance, infrastructure validation, rollback readiness, risk assessment
- **Post-Deployment Summary**: Health checks, automated smoke tests, performance verification (with baseline comparison), error monitoring, security verification, rollback decision support
- **Deployment Metrics**: Deployment success metrics, deployment duration, rollback rate
- **Critical Issues**: Blocking issues that require immediate attention or rollback with severity classification
- **Deployment Approval Status**: Approval workflow status and recommendations
- **Deployment Insights**: Key insights and patterns from deployment process
- **Recommendations**: Improvements for future deployments with priority levels and implementation guidance
- **Next Steps**: Actionable items for deployment optimization with priority levels

## Execution Flow
```
pre-deployment-check → [Deploy] → post-deployment-verification → Final Report
         ↓ Fail                              ↓ Fail
      [Stop]                          [Report & Consider Rollback]
```

## Notes
- Pre-deployment check must pass before deployment
- Post-deployment verification should be run immediately after deployment
- Each command can be run independently if needed
- Master command provides workflow orchestration
- All reports are preserved for detailed analysis
