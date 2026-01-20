# Run All Security

## Overview
Execute all security commands in sequence: compliance check, audit log analysis, and comprehensive security audit. This master command runs the complete security workflow to ensure system security, compliance, and audit trail integrity.

## Rules Applied
- `security-governance-and-observability` - Security governance, OWASP Top 10, NIST AI RMF, blast radius containment
- `audit-protocol` - Audit trail requirements, compliance checks, regulatory compliance
- `data-schemas-and-interfaces` - Data handling, PII protection, data security validation
- `multi-tenancy-and-isolation` - Multi-tenant compliance checks, isolation security
- `monitoring-and-observability` - Compliance monitoring, audit trail verification, log aggregation
- `error-handling-and-resilience` - Compliance error handling, error pattern analysis, error classification
- `performance-optimization` - Performance anomaly detection
- `human-in-the-loop-approval` - Human intervention tracking, approval workflow analysis
- `prompt-injection-prevention` - Prompt injection vulnerability checks
- `configuration-and-dependency-injection` - Secrets management, configuration security

## Steps

1. **Compliance Check**
   - Execute `/security/compliance-check` command
   - Wait for completion and review results
   - **Error Handling**:
     - If compliance check fails: Continue with warning, include in final report
     - If compliance issues found: Mark as non-blocking but include in report
     - If compliance passes: Proceed to next step
   - **Output**: Compliance report with GDPR, HIPAA, SOC 2 status

2. **Analyze Audit Logs**
   - Execute `/security/analyze-audit-logs` command
   - Wait for completion and review results
   - **Error Handling**:
     - If audit log analysis fails: Continue with warning, report data availability issues
     - If security incidents detected: Mark as critical, include in final report
     - If analysis completes: Proceed to next step
   - **Output**: Audit log analysis report with anomalies and incidents

3. **Security Audit**
   - Execute `/security/security-audit` command (uses results from steps 1 and 2)
   - Wait for completion and review results
   - **Error Handling**:
     - If security audit fails: Report error but include partial results
     - If critical vulnerabilities found: Mark as blocking issues
     - If high/medium vulnerabilities found: Include in final report
     - If audit completes: Generate final report
   - **Output**: Comprehensive security audit report

4. **Generate Comprehensive Security Report**
   - **Comprehensive Security Status Aggregation**:
     - Aggregate results from all three commands (compliance check, audit log analysis, security audit)
     - Combine security findings, compliance status, and audit insights
     - Create unified security posture assessment
   - **Risk Prioritization**:
     - Categorize all findings by risk level (Critical, High, Medium, Low)
     - Prioritize based on impact and exploitability
     - Calculate overall risk score
     - Identify top security risks requiring immediate attention
   - **Security Metrics Dashboard**:
     - Compliance score per regulation (GDPR, HIPAA, SOC 2)
     - Security vulnerability count by severity
     - Audit log coverage and completeness metrics
     - Security incident count and trends
     - Overall security posture score
   - Create summary with overall security status (Pass/Fail/Needs Attention)
   - Highlight critical vulnerabilities and compliance gaps with severity classification
   - Provide prioritized remediation recommendations with timelines
   - Include links to detailed reports from each command

## Data Sources
- Results from `/security/compliance-check` command
- Results from `/security/analyze-audit-logs` command
- Results from `/security/security-audit` command

## Output
A comprehensive security report including:
- **Overall Security Status**: Pass/Fail/Needs Attention with risk score
- **Security Metrics Dashboard**: Compliance scores, vulnerability counts, audit coverage, incident trends, overall security posture
- **Compliance Summary**: GDPR, HIPAA, SOC 2 compliance status with gap analysis and remediation tracking
- **Audit Log Summary**: Anomalies, incidents, patterns, forensic analysis, human intervention tracking
- **Security Audit Summary**: Vulnerabilities, OWASP Top 10 compliance, infrastructure security, security testing recommendations
- **Risk Prioritization**: All findings categorized by risk level with impact assessment
- **Critical Issues**: Blocking security issues that must be addressed immediately
- **Prioritized Recommendations**: Remediation steps with severity levels, timelines, and implementation guidance
- **Next Steps**: Actionable security improvements with priority levels

## Execution Flow
```
compliance-check → analyze-audit-logs → security-audit → Final Report
      ↓                    ↓                    ↓
  [Continue]          [Continue]          [Aggregate Results]
```

## Notes
- Each command can be run independently if needed
- Master command provides workflow orchestration
- Security audit uses results from compliance check and audit log analysis
- All reports are preserved for detailed analysis
