---
description: "Multi-tenant architecture patterns and data isolation strategies"
alwaysApply: false
---

## 1. Tenant Isolation Strategies

* **Database-Level Isolation:**
    * **Separate Databases:** Each tenant has a dedicated database.
    * **Pros:** Strong isolation, easier backup/restore, independent scaling.
    * **Cons:** Higher resource usage, more complex management.

* **Schema-Level Isolation:**
    * **Separate Schemas:** Each tenant has a dedicated schema within shared database.
    * **Pros:** Better resource utilization, easier cross-tenant queries (if needed).
    * **Cons:** Weaker isolation, potential for cross-tenant data access bugs.

* **Row-Level Isolation:**
    * **Tenant ID Column:** All tables include `tenant_id` column.
    * **Pros:** Efficient resource usage, simple architecture.
    * **Cons:** Highest risk of data leakage, requires careful query construction.

* **Application-Level Isolation:**
    * **Tenant Context:** Application enforces tenant isolation in application logic.
    * **Mandate:** Always validate tenant context in application layer, even with database-level isolation.

* **Hybrid Approach:**
    * **Tiered Isolation:** Use different isolation strategies for different tenant tiers.
    * **Enterprise Tenants:** Separate databases for enterprise customers.
    * **Standard Tenants:** Row-level isolation for standard customers.

## 2. Data Segregation Patterns

* **Tenant ID Enforcement:**
    * **Mandatory:** All queries must include tenant ID filter.
    * **Validation:** Validate tenant ID in application layer before database queries.
    * **ORM Filters:** Use ORM filters to automatically add tenant ID to queries.

* **Query Patterns:**
    * **Explicit Filtering:** Always explicitly filter by tenant ID.
    * **No Wildcards:** Never query without tenant context.
    * **Join Safety:** Ensure joins preserve tenant isolation.

* **Example Pattern:**
```python
# Good: Explicit tenant filtering
def get_user_data(tenant_id: str, user_id: str):
    return db.query(User).filter(
        User.tenant_id == tenant_id,
        User.id == user_id
    ).first()

# Bad: Missing tenant filter
def get_user_data(user_id: str):  # Missing tenant_id!
    return db.query(User).filter(User.id == user_id).first()
```

* **ORM Scoping:**
    * **Default Scope:** Configure ORM to automatically add tenant filter.
    * **Override:** Allow explicit override for admin operations (with proper authorization).

## 3. Resource Quotas per Tenant

* **Quota Types:**
    * **API Rate Limits:** Limit requests per tenant (requests per minute/hour).
    * **Storage Limits:** Limit data storage per tenant.
    * **Compute Limits:** Limit CPU/memory usage per tenant.
    * **Feature Limits:** Limit feature usage per tenant (e.g., number of agents, API calls).

* **Quota Enforcement:**
    * **Middleware:** Implement quota checking in API middleware.
    * **Database:** Track quota usage in database.
    * **Caching:** Cache quota usage in Redis for performance.

* **Quota Exceeded Handling:**
    * **HTTP 429:** Return 429 Too Many Requests when quota exceeded.
    * **Graceful Degradation:** Provide reduced functionality instead of complete blocking.
    * **Notification:** Notify tenant administrators when approaching limits.

* **Quota Configuration:**
    * **Per-Tenant:** Configure quotas per tenant (different tiers).
    * **Default:** Define default quotas for new tenants.
    * **Dynamic:** Allow dynamic quota adjustment (with proper authorization).

## 4. Tenant-Specific Configurations

* **Configuration Storage:**
    * **Database:** Store tenant configurations in database.
    * **Cache:** Cache tenant configurations in Redis for performance.
    * **Fallback:** Use default configuration if tenant-specific config not found.

* **Configuration Types:**
    * **Feature Flags:** Enable/disable features per tenant.
    * **API Limits:** Configure API rate limits per tenant.
    * **Custom Settings:** Store tenant-specific business logic settings.
    * **Integration Settings:** Store tenant-specific integration configurations.

* **Configuration Management:**
    * **Admin Interface:** Provide admin interface for managing tenant configurations.
    * **API:** Provide API for tenants to manage their own configurations (if applicable).
    * **Versioning:** Version tenant configurations for rollback capability.

* **Configuration Validation:**
    * **Schema:** Validate tenant configurations against schema.
    * **Business Rules:** Validate configurations against business rules.
    * **Default Values:** Provide sensible defaults for missing configurations.

## 5. Cross-Tenant Data Leakage Prevention

* **Input Validation:**
    * **Tenant ID Validation:** Validate tenant ID from request (header, token, path parameter).
    * **Authorization:** Verify user has access to requested tenant.
    * **No Tenant ID Injection:** Prevent tenant ID injection attacks.

* **Query Safety:**
    * **Parameterized Queries:** Always use parameterized queries to prevent SQL injection.
    * **ORM Usage:** Prefer ORM over raw SQL to reduce risk of injection.
    * **Query Auditing:** Log all queries for auditing and debugging.

* **Response Filtering:**
    * **Data Sanitization:** Ensure responses don't leak data from other tenants.
    * **Error Messages:** Don't expose tenant information in error messages.
    * **Logging:** Mask tenant IDs in logs (if required by compliance).

* **Testing:**
    * **Isolation Tests:** Test that tenant isolation is maintained.
    * **Cross-Tenant Tests:** Test that cross-tenant data access is prevented.
    * **Fuzzing:** Use fuzzing to test for isolation vulnerabilities.

## 6. Tenant Identification

* **Identification Methods:**
    * **Subdomain:** Identify tenant from subdomain (e.g., `tenant1.example.com`).
    * **Path Parameter:** Identify tenant from URL path (e.g., `/api/v1/tenants/{tenant_id}/...`).
    * **Header:** Identify tenant from HTTP header (e.g., `X-Tenant-ID`).
    * **JWT Token:** Extract tenant ID from JWT token claims.

* **Mandate:** Always validate tenant ID and ensure it matches authenticated user's tenant.

* **Tenant Resolution:**
    * **Middleware:** Resolve tenant in middleware before request processing.
    * **Context:** Store tenant context in request context for use throughout request.
    * **Validation:** Validate tenant exists and is active.

* **Multi-Tenant Users:**
    * **User-Tenant Mapping:** Support users belonging to multiple tenants.
    * **Tenant Selection:** Allow users to select active tenant for session.
    * **Authorization:** Verify user has access to selected tenant.

## 7. Tenant Data Backup & Recovery

* **Backup Strategy:**
    * **Per-Tenant Backups:** Support per-tenant backup and restore.
    * **Scheduled Backups:** Schedule regular backups for each tenant.
    * **Point-in-Time Recovery:** Support point-in-time recovery per tenant.

* **Backup Isolation:**
    * **Separate Backups:** Ensure backups don't mix tenant data.
    * **Encryption:** Encrypt backups with tenant-specific keys (if required).
    * **Access Control:** Control access to tenant backups.

* **Disaster Recovery:**
    * **Recovery Procedures:** Document recovery procedures per tenant.
    * **Testing:** Regularly test backup and recovery procedures.
    * **RTO/RPO:** Define Recovery Time Objective (RTO) and Recovery Point Objective (RPO) per tenant tier.

## 8. Tenant Onboarding & Offboarding

* **Onboarding:**
    * **Provisioning:** Automatically provision tenant resources (database, storage, etc.).
    * **Configuration:** Set up default tenant configuration.
    * **Documentation:** Provide tenant-specific documentation and setup guides.

* **Offboarding:**
    * **Data Retention:** Define data retention policy for offboarded tenants.
    * **Data Deletion:** Securely delete tenant data after retention period.
    * **Audit Trail:** Maintain audit trail of tenant offboarding.

* **Compliance:**
    * **Data Export:** Allow tenants to export their data before offboarding.
    * **GDPR:** Comply with data deletion requirements (GDPR right to be forgotten).
    * **Documentation:** Document data handling during offboarding.
