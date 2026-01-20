# Code Review Checklist

## Overview
Comprehensive code review using a structured checklist to ensure code quality, functionality, testing, documentation, security, and maintainability. This command provides thorough code analysis following project standards and best practices.

## Rules Applied
- `code-review-and-collaboration` - Code review standards, PR review checklist, Git workflow
- `core-python-standards` - Code quality standards, function length, type hints, logging
- `final-review-protocol` - Final review compliance checklist
- `error-handling-and-resilience` - Error handling review, error classification, retry strategies
- `tests-and-validation` - Test coverage review, test quality standards
- `security-governance-and-observability` - Security review, vulnerability checks, access control
- `performance-optimization` - Performance review, efficiency checks
- `data-schemas-and-interfaces` - Data handling review, schema validation

## Steps

1. **Code Quality Review**
   - **Style Guidelines**:
     - Check code follows style guidelines (ruff, black)
     - Verify consistent formatting and indentation
     - Check for code style violations
   - **Function Length**:
     - Verify all functions are under 20 lines (strict requirement)
     - Identify functions exceeding limit and suggest refactoring
     - Check for proper function splitting using helper functions
   - **Type Hints**:
     - Verify full type hints are present for all parameters and return values
     - Check use of `typing` module for complex types
     - Validate type hints are accurate and complete
   - **Code Duplication**:
     - Identify code duplication
     - Suggest extraction to helper functions
     - Check for DRY (Don't Repeat Yourself) violations

2. **Functionality Review**
   - **Correctness**:
     - Verify code works as intended
     - Check logic correctness and edge case handling
     - Identify potential bugs or logic errors
   - **Edge Cases**:
     - Verify edge cases are handled appropriately
     - Check for null/None handling
     - Validate boundary condition handling
   - **Error Handling**:
     - Check error handling is implemented appropriately
     - Verify error classification (transient vs permanent)
     - Validate retry strategies and circuit breakers where applicable
   - **Performance**:
     - Review performance considerations
     - Check for inefficient algorithms or patterns
     - Verify appropriate use of async/await for I/O operations

3. **Testing Review**
   - **Test Coverage**:
     - Verify tests are included for new functionality
     - Check test coverage is adequate
     - Identify untested code paths
   - **Test Quality**:
     - Review test structure (Arrange-Act-Assert pattern)
     - Check tests are atomic and independent
     - Verify tests use appropriate mocking for external dependencies
   - **Test Execution**:
     - Verify existing tests pass
     - Check for flaky tests
     - Validate test execution time is reasonable

4. **Documentation Review**
   - **Code Documentation**:
     - Verify code is self-documenting or has comments where needed
     - Check docstrings are present for public functions/classes
     - Validate docstring structure (Why, What, Args, Returns, Raises)
   - **Project Documentation**:
     - Check README or documentation is updated if needed
     - Verify API documentation is complete (if applicable)
     - Review changelog updates

5. **Security Review**
   - **Vulnerabilities**:
     - Check for obvious security vulnerabilities
     - Verify input validation is present
     - Check for SQL injection, XSS, CSRF prevention
   - **Sensitive Data**:
     - Verify no sensitive data in logs or responses
     - Check for hardcoded secrets or API keys
     - Validate PII handling and masking
   - **Access Control**:
     - Verify proper authentication and authorization
     - Check for privilege escalation risks
     - Validate access control implementation

6. **Dependencies Review**
   - **Justification**:
     - Verify new dependencies are justified
     - Check if existing dependencies could be used instead
     - Review dependency necessity
   - **Security**:
     - Check dependencies are up-to-date and secure
     - Verify no known vulnerabilities in dependencies
     - Review dependency licenses

7. **Architecture Review**
   - **Design Patterns**:
     - Verify appropriate design patterns are used
     - Check for separation of concerns
     - Validate modularity and maintainability
   - **Integration**:
     - Review integration with existing code
     - Check for breaking changes
     - Verify backward compatibility

8. **Generate Review Report**
   - Create comprehensive code review report
   - **Comprehensive Checklist**: Include all checklist items with status (✅/❌/⚠️) covering all standards
   - **Automated Checks**: Include results from automated code quality checks where applicable
   - **Review Approval Workflow**: Document approval status and workflow requirements
   - Provide specific feedback for each item
   - Prioritize issues by severity
   - Include recommendations for improvements

## Data Sources
- Source code files (Python files, configuration files)
- Test files (`tests/` directory, `test_*.py` files)
- Documentation files (README, docstrings, API docs)
- Dependency files (`requirements.txt`, `pyproject.toml`)
- Git history (recent changes, commit messages)

## Output
A comprehensive code review report including:
- **Checklist Summary**: Overall status with visual indicators (✅/❌/⚠️) covering all standards
- **Code Quality Assessment**: Function length, type hints, style compliance, code duplication
- **Functionality Review**: Correctness, edge cases, error handling with classification
- **Testing Status**: Coverage, test quality, execution results, test structure
- **Documentation Status**: Code docs, project docs, API docs, docstring structure
- **Security Assessment**: Vulnerabilities, sensitive data handling, access control, input validation
- **Performance Review**: Algorithm efficiency, async/await usage, performance considerations
- **Data Handling Review**: Schema validation, data structure usage, Pydantic models
- **Dependencies Review**: Justification, security, licenses, version compatibility
- **Architecture Review**: Design patterns, integration, compatibility, separation of concerns
- **Automated Check Results**: Results from automated code quality tools
- **Prioritized Recommendations**: Actionable feedback with severity levels
- **Approval Status**: Overall recommendation (Approve/Request Changes/Needs Discussion) with workflow requirements
