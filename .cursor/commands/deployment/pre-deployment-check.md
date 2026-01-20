# Pre-Deployment Check

## Overview
Comprehensive pre-deployment verification to ensure code is ready for production deployment. This command runs all critical checks including tests, evaluations, security audits, compliance verification, and infrastructure validation before deployment.

## Rules Applied
- `deployment-and-infrastructure` - CI/CD, Docker, Kubernetes, deployment standards
- `final-review-protocol` - Final review compliance checklist
- `security-governance-and-observability` - Security governance requirements
- `tests-and-validation` - Testing requirements
- `llm-evaluation-and-metrics` - Evaluation requirements
- `monitoring-and-observability` - Monitoring readiness, health check configuration
- `performance-optimization` - Performance readiness, SLI/SLO validation
- `configuration-and-dependency-injection` - Configuration validation, secrets management
- `versioning-and-release-management` - Version validation, release management
- `rate-limiting-and-queue-management` - Rate limiting checks, queue configuration

## Steps

1. **Run Test Suite**
   - Execute `/testing/run-test-suite` command
   - Verify all tests pass (✅ status)
   - Review test execution report
   - Proceed only if tests pass or with explicit approval for warnings

2. **Run Evaluation Suite**
   - Execute `/testing/run-evaluation-suite` command
   - Verify evaluation metrics meet thresholds
   - Review evaluation report
   - Proceed only if evaluation scores meet requirements

3. **Security Audit**
   - Execute `/security/security-audit` command (includes compliance checks)
   - Review security audit report
   - Verify no critical vulnerabilities
   - Proceed only if security audit passes

4. **Compliance Verification**
   - Execute `/review/final-compliance-check` command (includes code review)
   - Review compliance report
   - Verify all governance requirements are met
   - Proceed only if compliance check passes

5. **Infrastructure Validation**
   - **Docker Validation**:
     - Verify Dockerfile is optimized (multi-stage builds, minimal size)
     - Check Docker image security (non-root user, no secrets)
     - Validate Docker image builds successfully
   - **Kubernetes Validation** (if applicable):
     - Verify Kubernetes manifests are correct
     - Check resource limits and requests
     - Validate health check configurations
     - Review rolling update strategy
   - **CI/CD Pipeline**:
     - Verify CI/CD pipeline is configured
     - Check pipeline stages are complete
     - Validate automated quality gates
   - **Configuration Validation**:
     - Verify environment-specific configurations
     - Check secrets management (no hardcoded secrets)
     - Validate configuration validation using pydantic-settings
     - Verify configuration is properly structured
   - **Version Validation**:
     - Verify versioning strategy is implemented
     - Check version numbers are correct
     - Validate release management process
   - **Rate Limiting Checks**:
     - Verify rate limiting is configured
     - Check queue management configuration
     - Validate resource quotas

7. **Performance Validation**
   - Verify performance meets SLI/SLO requirements
   - Check latency percentiles (P50, P95, P99)
   - Validate throughput requirements
   - Review resource usage limits

8. **Rollback Readiness Check**
   - **Rollback Plan**: Verify rollback procedure is documented and tested
   - **Previous Version**: Verify previous version is available for rollback
   - **Rollback Tools**: Check rollback tools are accessible and functional
   - **Rollback Testing**: Validate rollback can be executed quickly

9. **Deployment Risk Assessment**
   - **Risk Identification**: Identify potential deployment risks
   - **Risk Mitigation**: Verify risk mitigation strategies are in place
   - **Impact Assessment**: Assess potential impact of deployment
   - **Risk Scoring**: Calculate deployment risk score

10. **Generate Pre-Deployment Report**
    - Create comprehensive pre-deployment report
    - Include results from all checks
    - Provide overall deployment readiness status (Pass/Fail/Needs Attention)
    - **Infrastructure Validation Summary**: Docker, Kubernetes, CI/CD, configuration, version, rate limiting status
    - **Rollback Readiness**: Rollback plan, previous version availability, rollback testing status
    - **Deployment Risk Assessment**: Risk identification, mitigation strategies, impact assessment, risk score
    - Highlight blocking issues with severity classification
    - Include recommendations for non-blocking issues
    - Provide deployment approval/rejection recommendation with justification

## Data Sources
- Results from `/testing/run-test-suite` command
- Results from `/testing/run-evaluation-suite` command
- Results from `/security/security-audit` command
- Results from `/review/final-compliance-check` command
- Infrastructure configuration files (Docker, Kubernetes, CI/CD)
- Performance metrics

## Output
A comprehensive pre-deployment report including:
- **Test Suite Results**: Summary from `/testing/run-test-suite` (pass/fail status, coverage, execution time)
- **Evaluation Suite Results**: Summary from `/testing/run-evaluation-suite` (metrics scores, quality assessment)
- **Security Audit Results**: Summary from `/security/security-audit` (vulnerabilities, compliance status)
- **Compliance Check Results**: Summary from `/review/final-compliance-check` (governance compliance status, code quality assessment)
- **Infrastructure Validation**: Docker, Kubernetes, CI/CD, configuration, version, rate limiting status
- **Performance Validation**: SLI/SLO compliance, latency, throughput, resource usage
- **Monitoring Readiness**: Health check configuration, metrics collection setup
- **Rollback Readiness**: Rollback plan, previous version availability, rollback testing status
- **Deployment Risk Assessment**: Risk identification, mitigation strategies, impact assessment, risk score
- **Overall Deployment Readiness**: Pass/Fail/Needs Attention with justification
- **Blocking Issues**: Critical issues that must be fixed before deployment with severity classification
- **Recommendations**: Non-blocking improvements for future deployments with priority levels
