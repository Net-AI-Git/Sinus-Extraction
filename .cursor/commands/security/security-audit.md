# Security Audit

## Overview
Comprehensive security review to identify and fix vulnerabilities in the codebase, infrastructure, and dependencies. This command performs a thorough security audit following OWASP Top 10 for LLM Applications and compliance requirements.

## Rules Applied
- `security-governance-and-observability` - Security governance, OWASP Top 10, NIST AI RMF, blast radius containment
- `audit-protocol` - Audit trail requirements and compliance checks
- `configuration-and-dependency-injection` - Secrets management and configuration security
- `prompt-injection-prevention` - Prompt injection vulnerability checks and prevention
- `data-schemas-and-interfaces` - Data security validation, PII protection
- `error-handling-and-resilience` - Security error handling, error classification
- `multi-tenancy-and-isolation` - Isolation security checks, multi-tenant security

## Steps

1. **Dependency Audit**
   - Check for known vulnerabilities in dependencies
     - Scan `requirements.txt`, `pyproject.toml`, `poetry.lock` for vulnerable packages
     - Use security scanning tools (Snyk, Trivy, safety) to identify CVEs
     - Check for outdated packages with security patches available
   - Review third-party dependencies
     - Analyze dependency tree for unnecessary or risky packages
     - Verify licenses are compatible and secure
     - Check for abandoned or unmaintained packages
   - Update recommendations
     - Prioritize critical security updates
     - Provide update paths for vulnerable packages
     - Identify breaking changes that may affect updates

2. **Code Security Review**
   - **OWASP Top 10 for LLM Applications** (Enhanced Coverage):
     1. **Prompt Injection**: 
        - Check for prompt validation and sanitization
        - Verify prompt injection prevention mechanisms
        - Test for prompt injection vulnerabilities
        - Validate input sanitization for all user inputs
     2. **Insecure Output Handling**: Validate LLM output handling and sanitization
     3. **Training Data Poisoning**: Verify trusted data sources
     4. **Model Denial of Service**: Check rate limiting and resource quotas
     5. **Supply Chain Vulnerabilities**: 
        - Audit dependencies (covered in step 1)
        - **Supply Chain Security Checks**: Verify package integrity, check for compromised packages
        - Validate dependency sources and signatures
     6. **Sensitive Information Disclosure**: 
        - Check for PII leakage, data masking
        - **Data Security Validation**: Verify PII detection and masking in all outputs
        - Validate data encryption at rest and in transit
     7. **Insecure Plugin Design**: Verify tool/plugin authentication and authorization
     8. **Excessive Agency**: Check guardrails and human-in-the-loop requirements
     9. **Overreliance**: Verify validation and fallback mechanisms
     10. **Model Theft**: Check IP protection measures
   - Review authentication/authorization
     - Verify OAuth2 patterns and JWT handling
     - Check API key management and storage
     - Validate RBAC implementation
   - Audit data handling practices
     - Check input validation and sanitization (SQL injection, XSS, CSRF prevention)
     - Verify PII handling and masking
     - Review data encryption at rest and in transit
   - **Security Error Handling**: 
     - Verify security errors are properly classified (transient vs permanent)
     - Check security error logging and monitoring
     - Validate security error recovery mechanisms

3. **Infrastructure Security**
   - Review environment variables
     - Check for hardcoded secrets in code
     - Verify secrets are stored securely (environment variables, secret managers)
     - Validate secret rotation mechanisms
   - Check access controls
     - Review IAM configurations
     - Verify least privilege principles
     - Check network security (firewalls, VPCs, security groups)
   - Audit network security
     - Review CORS configuration
     - Check security headers (HSTS, CSP, X-Frame-Options, etc.)
     - Verify TLS/SSL configuration
   - **Multi-Tenancy Security** (if applicable):
     - **Isolation Security Checks**: Verify tenant data isolation
     - Check tenant-specific access controls
     - Validate multi-tenant security boundaries
     - Review tenant data access patterns

4. **Audit Log Analysis**
   - Execute `/security/analyze-audit-logs` command
   - Review audit log analysis report
   - Identify security incidents and anomalies
   - Use audit log findings in security assessment

5. **Compliance Verification**
   - Execute `/security/compliance-check` command
   - Review compliance check results
   - Integrate compliance findings into security assessment
   - Verify compliance requirements are met

6. **Security Testing Recommendations**
   - **Penetration Testing**: Recommend areas for penetration testing
   - **Vulnerability Scanning**: Suggest automated vulnerability scanning tools
   - **Security Code Review**: Identify areas needing deeper security code review
   - **Red Team Exercises**: Recommend red team testing scenarios

7. **Generate Security Report**
   - Create comprehensive security audit report
   - Categorize findings by severity (Critical, High, Medium, Low)
   - Provide specific recommendations for each finding
   - Include remediation steps with code examples where applicable
   - Prioritize fixes based on risk and impact
   - **Security Testing Recommendations**: Include recommendations for security testing

## Data Sources
- Dependency files (`requirements.txt`, `pyproject.toml`, `poetry.lock`)
- Source code files (Python, configuration files)
- Environment configuration files (`.env`, configuration files)
- Results from `/security/analyze-audit-logs` command
- Results from `/security/compliance-check` command
- Infrastructure configuration (Docker, Kubernetes, cloud configs)
- Security scanning tool outputs

## Output
A comprehensive security audit report including:
- **Dependency Audit Results**: Vulnerable packages, CVEs, update recommendations, supply chain security
- **Code Security Findings**: OWASP Top 10 compliance status (enhanced coverage), specific vulnerabilities, prompt injection checks
- **Data Security Validation**: PII protection, data masking, encryption verification
- **Infrastructure Security Assessment**: Access controls, network security, secrets management, multi-tenancy security
- **Security Error Handling**: Error classification, security error logging, recovery mechanisms
- **Audit Log Review**: Summary from `/security/analyze-audit-logs` (implementation status and security event analysis)
- **Compliance Status**: Summary from `/security/compliance-check` (GDPR, HIPAA, SOC 2 compliance checks)
- **Security Testing Recommendations**: Penetration testing, vulnerability scanning, code review, red team exercises
- **Prioritized Recommendations**: Actionable fixes with severity levels and risk assessment
- **Remediation Guide**: Step-by-step instructions for addressing findings with code examples
