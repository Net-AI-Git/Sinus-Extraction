# Compliance Check

## Overview
Comprehensive compliance verification to ensure the system meets regulatory requirements including GDPR, HIPAA, and SOC 2. This command validates compliance controls, data handling practices, and audit trail completeness.

## Rules Applied
- `audit-protocol` - Compliance requirements, regulatory compliance (GDPR, HIPAA, SOC 2)
- `security-governance-and-observability` - Security governance, access controls, data protection
- `data-schemas-and-interfaces` - Data handling and PII protection
- `multi-tenancy-and-isolation` - Multi-tenant compliance checks, data isolation verification
- `monitoring-and-observability` - Compliance monitoring, audit trail verification
- `error-handling-and-resilience` - Compliance error handling, error classification

## Steps

1. **GDPR Compliance Checks**
   - **Data Subject Rights**:
     - Verify logging of all data access, modification, and deletion requests
     - Check implementation of right to access, rectification, erasure, portability
     - Validate data subject request handling procedures
   - **Consent Management**:
     - Verify consent status tracking and changes are logged
     - Check consent withdrawal mechanisms
     - Validate consent records are maintained
   - **Data Processing Records**:
     - Verify records of data processing activities are maintained
     - Check data processing purpose documentation
     - Validate data retention policies are documented and enforced
   - **Breach Notification**:
     - Verify potential data breaches are logged
     - Check breach notification procedures are documented
     - Validate breach detection mechanisms

2. **HIPAA Compliance Checks** (if applicable)
   - **PHI Access Logging**:
     - Verify all access to Protected Health Information is logged
     - Check PHI access logs include required fields (who, what, when, why)
     - Validate PHI access is restricted to authorized personnel only
   - **Access Controls**:
     - Verify access controls are enforced and logged
     - Check role-based access control implementation
     - Validate user authentication and authorization
   - **Audit Trail Requirements**:
     - Verify detailed audit trails for all PHI access
     - Check audit trail retention meets HIPAA requirements
     - Validate audit trail integrity and immutability

3. **SOC 2 Compliance Checks**
   - **Access Controls**:
     - Verify all access control changes are logged
     - Check user access permissions are reviewed regularly
     - Validate least privilege principles are enforced
   - **System Changes**:
     - Verify all system configuration and code changes are logged
     - Check change management procedures are documented
     - Validate change approval processes
   - **Incident Response**:
     - Verify all security incidents are logged
     - Check incident response procedures are documented
     - Validate incident response team activation procedures

4. **Data Retention Policy Verification**
   - Verify data retention policies are defined and documented
   - Check retention periods meet regulatory requirements
   - Validate automatic deletion after retention period
   - Review data archival procedures

5. **Access Control Verification**
   - Verify access controls are properly configured
   - Check user permissions are appropriate for roles
   - Validate access control changes are logged
   - Review access review procedures and frequency

6. **Data Protection Verification**
   - **PII Handling**:
     - Verify PII detection and masking in logs
     - Check PII encryption at rest and in transit
     - Validate data minimization principles
   - **Data Classification**:
     - Verify data is properly classified
     - Check sensitive data handling procedures
     - Validate data access restrictions

7. **Audit Trail Completeness**
   - Verify all required events are logged
   - Check audit log structure meets compliance requirements
   - Validate audit log retention meets regulatory requirements
   - Review audit log access controls

8. **Multi-Tenancy Compliance Checks** (if applicable)
   - **Data Isolation**: Verify tenant data is properly isolated
   - **Access Controls**: Check tenant-specific access controls are enforced
   - **Audit Logging**: Verify tenant-specific audit logging
   - **Compliance Monitoring**: Check multi-tenant compliance monitoring

9. **Automated Compliance Validation**
   - **Automated Checks**: Run automated compliance validation scripts
   - **Configuration Validation**: Verify compliance-related configurations
   - **Policy Enforcement**: Check automated policy enforcement mechanisms
   - **Compliance Gap Analysis**: Identify gaps between current state and requirements

10. **Generate Compliance Report**
    - Create comprehensive compliance report
    - Document compliance status for each regulation
    - **Compliance Gap Analysis**: Detailed analysis of compliance gaps with severity classification
    - **Remediation Tracking**: Track remediation status for identified gaps
    - Provide prioritized recommendations for remediation
    - Include evidence and references for each check
    - **Compliance Scoring**: Calculate compliance score per regulation and overall

## Data Sources
- Audit logs (JSON format) from local files
- Configuration files (access controls, data retention policies)
- Code files (data handling, PII protection implementation)
- Documentation files (compliance procedures, policies)
- System configuration (environment variables, security settings)

## Output
A comprehensive compliance report including:
- **GDPR Compliance Status**: Data subject rights, consent management, data processing records, breach notification
- **HIPAA Compliance Status** (if applicable): PHI access logging, access controls, audit trail requirements
- **SOC 2 Compliance Status**: Access controls, system changes, incident response
- **Multi-Tenancy Compliance** (if applicable): Data isolation, tenant access controls, audit logging
- **Data Retention Verification**: Policy compliance and enforcement status
- **Access Control Verification**: Configuration and enforcement status
- **Data Protection Status**: PII handling, encryption, data classification
- **Audit Trail Completeness**: Logging coverage and structure compliance
- **Compliance Gap Analysis**: Detailed analysis of gaps with severity levels and impact assessment
- **Remediation Tracking**: Status of remediation efforts for identified gaps
- **Compliance Scoring**: Per-regulation scores and overall compliance score
- **Automated Validation Results**: Results from automated compliance checks
- **Remediation Recommendations**: Prioritized actions to achieve compliance with timelines
