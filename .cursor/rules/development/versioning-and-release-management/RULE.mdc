---
description: "Semantic versioning, changelog, and release management standards"
alwaysApply: false
---

## 1. Semantic Versioning Standards

* **Format:** `MAJOR.MINOR.PATCH` (e.g., `1.2.3`)

* **Version Increment Rules:**
    * **MAJOR:** Increment for breaking changes (incompatible API changes, major feature removals).
    * **MINOR:** Increment for new features (backward-compatible functionality additions).
    * **PATCH:** Increment for bug fixes (backward-compatible bug fixes).

* **Pre-Release Versions:**
    * **Alpha:** `1.0.0-alpha.1` - Early development, unstable.
    * **Beta:** `1.0.0-beta.1` - Feature complete, testing phase.
    * **RC (Release Candidate):** `1.0.0-rc.1` - Potential release, final testing.

* **Build Metadata:**
    * **Format:** `1.0.0+build.123` - Additional build information (optional).

* **Mandate:** All releases must follow semantic versioning. Never skip version numbers.

## 2. Changelog Format

* **Keep a Changelog Standard:**
    * **Format:** Follow [Keep a Changelog](https://keepachangelog.com/) format.
    * **Location:** Maintain `CHANGELOG.md` in repository root.

* **Changelog Sections:**
    * **Added:** New features.
    * **Changed:** Changes in existing functionality.
    * **Deprecated:** Soon-to-be removed features.
    * **Removed:** Removed features.
    * **Fixed:** Bug fixes.
    * **Security:** Security vulnerability fixes.

* **Version Entries:**
    * **Format:** `## [Version] - YYYY-MM-DD`
    * **Unreleased:** Use `## [Unreleased]` for upcoming changes.

* **Entry Format:**
    * **Descriptive:** Write clear, descriptive entries.
    * **Links:** Link to related issues, PRs, or commits.
    * **Breaking Changes:** Clearly mark breaking changes.

* **Example:**
```markdown
## [1.2.0] - 2024-01-15

### Added
- New endpoint for batch processing
- Support for streaming responses

### Changed
- Improved error messages for validation errors

### Fixed
- Memory leak in connection pooling

### Security
- Updated dependencies to fix CVE-2024-1234
```

## 3. Release Process

* **Release Preparation:**
    1. **Update Version:** Update version in code (e.g., `__version__.py`, `pyproject.toml`).
    2. **Update Changelog:** Add release entry to CHANGELOG.md with date.
    3. **Run Tests:** Ensure all tests pass.
    4. **Update Dependencies:** Update dependency versions if needed.
    5. **Code Review:** Get code review for release changes.

* **Release Creation:**
    1. **Create Tag:** Create Git tag with version number (e.g., `v1.2.0`).
    2. **Tag Message:** Include release notes in tag message.
    3. **Push Tag:** Push tag to remote repository.
    4. **CI/CD Trigger:** CI/CD pipeline automatically builds and deploys.

* **Post-Release:**
    1. **Verify Deployment:** Verify successful deployment to production.
    2. **Monitor:** Monitor for issues in first hours/days after release.
    3. **Documentation:** Update documentation if needed.
    4. **Announcement:** Announce release to stakeholders (if applicable).

* **Rollback Plan:**
    * **Procedure:** Document rollback procedure.
    * **Trigger:** Define conditions for rollback (error rate, critical bugs).
    * **See:** `deployment-and-infrastructure.md` for rollback procedures.

## 4. Feature Flags/Toggles

* **Purpose:** Enable/disable features without code deployment.

* **Implementation:**
    * **Configuration:** Store feature flags in configuration (environment variables, database, feature flag service).
    * **Runtime Check:** Check feature flag status at runtime.
    * **Default:** Default to disabled for new features.

* **Feature Flag Types:**
    * **Release Flags:** Control feature rollout (gradual rollout, A/B testing).
    * **Ops Flags:** Control operational features (maintenance mode, feature degradation).
    * **Permission Flags:** Control feature access based on user permissions.

* **Best Practices:**
    * **Naming:** Use clear, descriptive names for feature flags.
    * **Documentation:** Document purpose and expected behavior of each flag.
    * **Cleanup:** Remove feature flags after feature is fully rolled out.
    * **Testing:** Test both enabled and disabled states.

* **Feature Flag Services:**
    * **Options:** LaunchDarkly, Unleash, or custom implementation.
    * **Integration:** Integrate with monitoring to track feature usage.

## 5. A/B Testing Infrastructure

* **Purpose:** Test different versions of features to measure impact.

* **Implementation:**
    * **User Segmentation:** Segment users into test groups (A/B/C).
    * **Consistent Assignment:** Ensure users are consistently assigned to same group.
    * **Metrics Tracking:** Track metrics for each test group.
    * **Statistical Analysis:** Use statistical methods to determine significance.

* **Test Configuration:**
    * **Traffic Split:** Configure traffic split (e.g., 50/50, 10/90).
    * **Duration:** Define test duration.
    * **Success Criteria:** Define success criteria before starting test.

* **Best Practices:**
    * **Hypothesis:** Start with clear hypothesis.
    * **Sample Size:** Ensure sufficient sample size for statistical significance.
    * **Monitoring:** Monitor for anomalies during test.
    * **Documentation:** Document test results and decisions.

* **Integration:**
    * **Feature Flags:** Use feature flags to control A/B test variants.
    * **Analytics:** Integrate with analytics to track user behavior.

## 6. Rollback Procedures

* **Automated Rollback:**
    * **Health Checks:** Automatically rollback if health checks fail.
    * **Error Thresholds:** Rollback if error rate exceeds threshold.
    * **Latency Thresholds:** Rollback if latency exceeds acceptable limits.

* **Manual Rollback:**
    * **Process:** Document clear manual rollback procedure.
    * **Access:** Ensure team has access to rollback tools.
    * **Communication:** Notify stakeholders before and after rollback.

* **Rollback Strategies:**
    * **Version Rollback:** Revert to previous code version.
    * **Feature Flag:** Disable feature using feature flag (if applicable).
    * **Database Rollback:** Rollback database migrations if needed (see `data-migration-and-compatibility.md`).

* **Post-Rollback:**
    * **Investigation:** Investigate root cause of issue.
    * **Documentation:** Document incident and lessons learned.
    * **Prevention:** Update processes to prevent similar issues.

* **See:** `deployment-and-infrastructure.md` for detailed rollback procedures.

## 7. Version Communication

* **Version Endpoints:**
    * **API Version:** Expose API version in response headers or endpoint (e.g., `/api/version`).
    * **Application Version:** Expose application version in health check endpoint.

* **Version Headers:**
    * **Response Headers:** Include version in API response headers (e.g., `X-API-Version: 1.2.0`).

* **Deprecation Warnings:**
    * **Headers:** Include deprecation warnings in response headers for deprecated endpoints.
    * **Documentation:** Clearly document deprecation timeline and migration path.

* **Release Notes:**
    * **Public Release Notes:** Publish release notes for public APIs.
    * **Internal Release Notes:** Maintain internal release notes with technical details.

## 8. Dependency Versioning

* **Version Pinning:**
    * **Production:** Pin exact versions in production (e.g., `package==1.2.3`).
    * **Development:** Use compatible version ranges in development (e.g., `package>=1.2.0,<2.0.0`).

* **Dependency Updates:**
    * **Regular Updates:** Regularly update dependencies for security patches.
    * **Major Updates:** Test thoroughly before updating major versions.
    * **Changelog:** Review dependency changelogs for breaking changes.

* **Security Updates:**
    * **Priority:** Prioritize security updates.
    * **Testing:** Test security updates before deployment.
    * **Documentation:** Document security updates in changelog.

* **Dependency Management:**
    * **Requirements Files:** Maintain `requirements.txt` and `requirements-dev.txt`.
    * **Lock Files:** Use lock files (e.g., `poetry.lock`, `Pipfile.lock`) for reproducible builds.
