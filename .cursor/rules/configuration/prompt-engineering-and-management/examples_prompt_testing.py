"""
Prompt Testing Examples

This file demonstrates unit testing patterns and test framework implementation.
Reference this example from RULE.mdc using @examples_prompt_testing.py syntax.
"""

from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass
from enum import Enum


# ============================================================================
# Test Framework
# ============================================================================

@dataclass
class PromptTestCase:
    """
    Test case for prompt testing.
    
    This demonstrates test case structure:
    - Input variables
    - Expected output
    - Validation rules
    """
    name: str
    input_variables: Dict[str, Any]
    expected_output: Optional[str] = None
    validation_rules: List[Callable] = None
    expected_format: Optional[str] = None  # e.g., "json", "xml", "text"


@dataclass
class TestResult:
    """
    Test result structure.
    
    This demonstrates test result:
    - Pass/fail status
    - Actual output
    - Validation results
    - Performance metrics
    """
    test_name: str
    passed: bool
    actual_output: str
    validation_results: Dict[str, bool]
    error_message: Optional[str] = None
    performance_metrics: Optional[Dict[str, float]] = None


class PromptTestFramework:
    """
    Framework for testing prompts.
    
    This demonstrates prompt testing patterns:
    - Test execution
    - Output validation
    - Performance testing
    - Regression detection
    """
    
    def __init__(self, llm_client: Any = None, mock_mode: bool = False):
        """
        Initialize test framework.
        
        Args:
            llm_client: LLM client (None for mock mode)
            mock_mode: Use mock responses instead of real LLM
        """
        self.llm_client = llm_client
        self.mock_mode = mock_mode
        self.mock_responses: Dict[str, str] = {}
    
    def run_test(
        self,
        prompt: str,
        test_case: PromptTestCase
    ) -> TestResult:
        """
        Run a single test case.
        
        Args:
            prompt: Prompt template
            test_case: Test case to run
        
        Returns:
            TestResult
        """
        # Render prompt with input variables
        rendered_prompt = self._render_prompt(prompt, test_case.input_variables)
        
        # Get output (mock or real)
        if self.mock_mode:
            actual_output = self._get_mock_output(test_case.name)
        else:
            actual_output = self._call_llm(rendered_prompt)
        
        # Validate output
        validation_results = self._validate_output(
            actual_output,
            test_case
        )
        
        # Check if all validations passed
        passed = all(validation_results.values())
        
        return TestResult(
            test_name=test_case.name,
            passed=passed,
            actual_output=actual_output,
            validation_results=validation_results
        )
    
    def run_test_suite(
        self,
        prompt: str,
        test_cases: List[PromptTestCase]
    ) -> List[TestResult]:
        """
        Run a suite of test cases.
        
        Args:
            prompt: Prompt template
            test_cases: List of test cases
        
        Returns:
            List of TestResult
        """
        results = []
        for test_case in test_cases:
            result = self.run_test(prompt, test_case)
            results.append(result)
        
        return results
    
    def _render_prompt(
        self,
        prompt: str,
        variables: Dict[str, Any]
    ) -> str:
        """
        Render prompt with variables.
        
        Args:
            prompt: Prompt template
            variables: Variables to inject
        
        Returns:
            Rendered prompt
        """
        # Simple template rendering (in real implementation, use Jinja2)
        rendered = prompt
        for key, value in variables.items():
            rendered = rendered.replace(f"{{{{ {key} }}}}", str(value))
        
        return rendered
    
    def _get_mock_output(self, test_name: str) -> str:
        """
        Get mock output for test.
        
        Args:
            test_name: Test case name
        
        Returns:
            Mock output
        """
        return self.mock_responses.get(test_name, "Mock response")
    
    def _call_llm(self, prompt: str) -> str:
        """
        Call LLM with prompt.
        
        Args:
            prompt: Rendered prompt
        
        Returns:
            LLM output
        """
        # In real implementation, call actual LLM
        # return self.llm_client.generate(prompt)
        return "LLM output"
    
    def _validate_output(
        self,
        output: str,
        test_case: PromptTestCase
    ) -> Dict[str, bool]:
        """
        Validate output against test case.
        
        Args:
            output: Actual output
            test_case: Test case with validation rules
        
        Returns:
            Dictionary of validation results
        """
        results = {}
        
        # Check expected output match
        if test_case.expected_output:
            results["expected_output_match"] = output.strip() == test_case.expected_output.strip()
        
        # Check format
        if test_case.expected_format:
            results["format_check"] = self._check_format(output, test_case.expected_format)
        
        # Run custom validation rules
        if test_case.validation_rules:
            for i, rule in enumerate(test_case.validation_rules):
                try:
                    results[f"validation_rule_{i}"] = rule(output)
                except Exception as e:
                    results[f"validation_rule_{i}"] = False
        
        return results
    
    def _check_format(self, output: str, expected_format: str) -> bool:
        """
        Check output format.
        
        Args:
            output: Output to check
            expected_format: Expected format
        
        Returns:
            True if format matches
        """
        if expected_format == "json":
            try:
                import json
                json.loads(output)
                return True
            except:
                return False
        elif expected_format == "xml":
            return output.strip().startswith("<") and output.strip().endswith(">")
        else:
            return True  # Text format always valid


# ============================================================================
# Validation Rules
# ============================================================================

def validate_json_structure(output: str) -> bool:
    """
    Validate JSON structure.
    
    Args:
        output: Output to validate
    
    Returns:
        True if valid JSON
    """
    try:
        import json
        data = json.loads(output)
        return isinstance(data, (dict, list))
    except:
        return False


def validate_contains_keywords(output: str, keywords: List[str]) -> bool:
    """
    Validate output contains keywords.
    
    Args:
        output: Output to validate
        keywords: Required keywords
    
    Returns:
        True if all keywords present
    """
    output_lower = output.lower()
    return all(keyword.lower() in output_lower for keyword in keywords)


def validate_length(output: str, min_length: int, max_length: int) -> bool:
    """
    Validate output length.
    
    Args:
        output: Output to validate
        min_length: Minimum length
        max_length: Maximum length
    
    Returns:
        True if length within range
    """
    length = len(output)
    return min_length <= length <= max_length


def validate_no_sensitive_data(output: str) -> bool:
    """
    Validate no sensitive data in output.
    
    Args:
        output: Output to validate
    
    Returns:
        True if no sensitive data detected
    """
    sensitive_patterns = [
        r'\b\d{3}-\d{2}-\d{4}\b',  # SSN
        r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b',  # Credit card
    ]
    
    import re
    for pattern in sensitive_patterns:
        if re.search(pattern, output):
            return False
    
    return True


# ============================================================================
# Test Suite Examples
# ============================================================================

def create_test_suite_for_agent_prompt() -> List[PromptTestCase]:
    """
    Create test suite for agent system prompt.
    
    This demonstrates test suite creation:
    - Multiple test cases
    - Different scenarios
    - Validation rules
    
    Returns:
        List of PromptTestCase
    """
    return [
        PromptTestCase(
            name="basic_request",
            input_variables={"user_request": "What is the weather?"},
            validation_rules=[
                lambda o: validate_length(o, 10, 1000),
                lambda o: validate_contains_keywords(o, ["weather"])
            ]
        ),
        PromptTestCase(
            name="complex_request",
            input_variables={"user_request": "Analyze the data and provide recommendations"},
            validation_rules=[
                lambda o: validate_length(o, 50, 2000),
                lambda o: validate_contains_keywords(o, ["analysis", "recommendation"])
            ]
        ),
        PromptTestCase(
            name="json_output",
            input_variables={"user_request": "Return data as JSON"},
            expected_format="json",
            validation_rules=[validate_json_structure]
        )
    ]


def run_prompt_tests(
    prompt: str,
    test_suite: List[PromptTestCase],
    framework: PromptTestFramework
) -> Dict[str, Any]:
    """
    Run prompt test suite and return results.
    
    Args:
        prompt: Prompt to test
        test_suite: Test cases
        framework: Test framework
    
    Returns:
        Test results summary
    """
    results = framework.run_test_suite(prompt, test_suite)
    
    passed = sum(1 for r in results if r.passed)
    total = len(results)
    
    return {
        "total_tests": total,
        "passed": passed,
        "failed": total - passed,
        "pass_rate": passed / total if total > 0 else 0.0,
        "results": results
    }
