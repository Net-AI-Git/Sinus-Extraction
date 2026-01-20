---
description: "Standards for code review, Git workflow, and collaboration practices"
alwaysApply: false
---

## 1. PR Review Checklist

* **Code Quality:**
    * [ ] Code follows style guidelines (ruff, black).
    * [ ] All functions are under 20 lines (see `core-python-standards.md`).
    * [ ] Full type hints are present.
    * [ ] No hardcoded secrets or configuration.
    * [ ] Error handling is implemented appropriately.

* **Functionality:**
    * [ ] Code works as intended.
    * [ ] Edge cases are handled.
    * [ ] No obvious bugs or logic errors.
    * [ ] Performance considerations are addressed.

* **Testing:**
    * [ ] Tests are included for new functionality.
    * [ ] Existing tests pass.
    * [ ] Test coverage is adequate.
    * [ ] Edge cases are tested.

* **Documentation:**
    * [ ] Code is self-documenting or has comments where needed.
    * [ ] Docstrings are present for public functions/classes.
    * [ ] README or documentation is updated if needed.

* **Security:**
    * [ ] No security vulnerabilities introduced.
    * [ ] Input validation is present.
    * [ ] No sensitive data in logs or responses.

* **Dependencies:**
    * [ ] New dependencies are justified.
    * [ ] Dependencies are up-to-date and secure.

## 2. Git Workflow

* **Branching Strategies:**
    * **Feature Branches:** Create feature branch from `main` for new features.
    * **Naming:** Use descriptive branch names (e.g., `feature/add-user-authentication`, `fix/memory-leak`).
    * **Short-Lived:** Keep branches short-lived (merge within days, not weeks).

* **Trunk-Based Development:**
    * **Main Branch:** `main` branch is always deployable.
    * **Small PRs:** Prefer small, focused PRs over large changes.
    * **Frequent Merges:** Merge to `main` frequently to avoid conflicts.

* **GitFlow (Alternative):**
    * **Develop Branch:** Use `develop` branch for integration.
    * **Release Branches:** Create release branches for preparing releases.
    * **Hotfix Branches:** Create hotfix branches for urgent production fixes.

* **Branch Protection:**
    * **Main Branch:** Protect `main` branch (require PR, require approvals, require CI checks).
    * **No Direct Pushes:** Prevent direct pushes to protected branches.

## 3. Commit Message Standards

* **Conventional Commits Format:**
    * **Format:** `<type>(<scope>): <description>`
    * **Types:**
        * `feat`: New feature
        * `fix`: Bug fix
        * `docs`: Documentation changes
        * `style`: Code style changes (formatting, no logic change)
        * `refactor`: Code refactoring
        * `test`: Test additions or changes
        * `chore`: Maintenance tasks
        * `perf`: Performance improvements

* **Commit Message Structure:**
    * **Subject Line:** Short, descriptive (50 characters or less).
    * **Body (optional):** Detailed explanation (wrap at 72 characters).
    * **Footer (optional):** Reference issues, breaking changes.

* **Examples:**
```
feat(auth): add OAuth2 authentication support

Implement OAuth2 authentication flow with support for
Google and GitHub providers. Includes token refresh
and user profile retrieval.

Closes #123
```

```
fix(api): resolve memory leak in connection pooling

The connection pool was not properly releasing connections,
causing memory to accumulate over time. Added proper
cleanup in connection pool destructor.

Fixes #456
```

* **Mandate:** All commit messages must follow conventional commits format.

## 4. Branch Naming Conventions

* **Format:** `<type>/<description>`

* **Types:**
    * `feature/`: New features
    * `fix/`: Bug fixes
    * `hotfix/`: Urgent production fixes
    * `refactor/`: Code refactoring
    * `docs/`: Documentation updates
    * `test/`: Test additions or changes
    * `chore/`: Maintenance tasks

* **Description:**
    * **Lowercase:** Use lowercase letters.
    * **Hyphens:** Separate words with hyphens.
    * **Descriptive:** Be descriptive but concise.
    * **Examples:**
        * `feature/user-authentication`
        * `fix/memory-leak-connection-pool`
        * `hotfix/critical-security-patch`

* **Issue References:**
    * **Optional:** Include issue number in branch name (e.g., `feature/123-add-caching`).

## 5. Code Ownership & Responsibility

* **Code Ownership:**
    * **Primary Owner:** Each module/component has a primary owner.
    * **Code Review:** Primary owner should review changes to their code.
    * **Knowledge Sharing:** Owners should share knowledge with team.

* **Collective Ownership:**
    * **Team Responsibility:** Entire team is responsible for code quality.
    * **No Blame:** Focus on improving code, not assigning blame.
    * **Learning Opportunity:** Use code reviews as learning opportunities.

* **Onboarding:**
    * **New Team Members:** Assign mentors for new team members.
    * **Code Walkthrough:** Conduct code walkthroughs for complex areas.
    * **Documentation:** Maintain up-to-date documentation.

* **Rotation:**
    * **Review Rotation:** Rotate code review assignments to share knowledge.
    * **On-Call Rotation:** Rotate on-call responsibilities.

## 6. Review Response Time Expectations

* **Response Time:**
    * **Business Hours:** Respond to PR reviews within 4 business hours.
    * **Urgent PRs:** Respond to urgent PRs within 1 hour.
    * **Non-Urgent:** Respond to non-urgent PRs within 1 business day.

* **Review Completion:**
    * **Small PRs:** Complete review within 1 business day.
    * **Large PRs:** Complete review within 2-3 business days.
    * **Blocking:** If blocking, communicate timeline clearly.

* **Communication:**
    * **Status Updates:** Provide status updates if review will be delayed.
    * **Availability:** Communicate availability and response expectations.
    * **Escalation:** Escalate if review is blocking critical work.

* **Automation:**
    * **Auto-Assign:** Use automation to assign reviewers based on code ownership.
    * **Reminders:** Set up reminders for pending reviews.

## 7. Review Best Practices

* **For Reviewers:**
    * **Be Constructive:** Provide constructive feedback.
    * **Be Respectful:** Maintain respectful tone in comments.
    * **Explain Why:** Explain reasoning behind suggestions.
    * **Approve Promptly:** Approve promptly if code is good.
    * **Ask Questions:** Ask questions to understand intent.

* **For Authors:**
    * **Small PRs:** Keep PRs small and focused.
    * **Clear Description:** Provide clear PR description explaining changes.
    * **Respond Promptly:** Respond to review comments promptly.
    * **Be Open:** Be open to feedback and suggestions.
    * **Thank Reviewers:** Acknowledge and thank reviewers.

* **Review Focus:**
    * **Correctness:** Is the code correct?
    * **Design:** Is the design appropriate?
    * **Testing:** Are there adequate tests?
    * **Documentation:** Is documentation updated?
    * **Performance:** Are there performance concerns?
    * **Security:** Are there security concerns?

* **Avoid:**
    * **Nitpicking:** Avoid nitpicking on style (use linters).
    * **Personal Preferences:** Avoid enforcing personal preferences.
    * **Blocking on Minor Issues:** Don't block on minor issues that can be fixed later.

## 8. Conflict Resolution

* **Technical Disagreements:**
    * **Discussion:** Engage in technical discussion.
    * **Data-Driven:** Use data and evidence to support arguments.
    * **Compromise:** Be willing to compromise when appropriate.
    * **Escalation:** Escalate to tech lead if needed.

* **Code Style:**
    * **Automated:** Use automated tools (linters, formatters) to enforce style.
    * **Consistency:** Prioritize consistency over personal preference.

* **Architecture Decisions:**
    * **Document:** Document architecture decisions (ADRs).
    * **Review:** Review architecture decisions with team.
    * **Consensus:** Strive for team consensus on major decisions.
