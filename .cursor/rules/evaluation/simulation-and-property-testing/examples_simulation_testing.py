"""
Simulation and Property-Based Testing Examples

This file demonstrates simulation testing and property-based testing patterns.
Reference this example from RULE.mdc using @examples_simulation_testing.py syntax.
"""

from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import random
import asyncio


# ============================================================================
# Edge Case Simulator
# ============================================================================

class EdgeCaseType(Enum):
    """
    Edge case types for simulation.
    
    This demonstrates edge case categories:
    - Empty responses
    - Timeouts
    - Partial failures
    - Invalid inputs
    """
    EMPTY_RESPONSE = "empty_response"
    TIMEOUT = "timeout"
    PARTIAL_FAILURE = "partial_failure"
    INVALID_INPUT = "invalid_input"
    NETWORK_ERROR = "network_error"
    RATE_LIMIT = "rate_limit"


@dataclass
class EdgeCaseConfig:
    """
    Configuration for edge case simulation.
    
    This demonstrates edge case configuration:
    - Edge case type
    - Probability of occurrence
    - Parameters for edge case
    """
    edge_case_type: EdgeCaseType
    probability: float = 0.1  # 10% chance
    parameters: Dict[str, Any] = field(default_factory=dict)


class EdgeCaseSimulator:
    """
    Simulator for edge cases.
    
    This demonstrates edge case simulation patterns:
    - Generate edge cases
    - Simulate tool responses
    - Simulate errors
    - Simulate timeouts
    """
    
    def __init__(
        self,
        edge_cases: List[EdgeCaseConfig]
    ):
        """
        Initialize edge case simulator.
        
        Args:
            edge_cases: List of edge case configurations
        """
        self.edge_cases = edge_cases
        self.edge_case_history: List[EdgeCaseType] = []
    
    def should_trigger_edge_case(
        self,
        edge_case_type: EdgeCaseType
    ) -> bool:
        """
        Check if edge case should be triggered.
        
        Args:
            edge_case_type: Type of edge case
            
        Returns:
            True if should trigger
        """
        config = next(
            (c for c in self.edge_cases if c.edge_case_type == edge_case_type),
            None
        )
        
        if not config:
            return False
        
        return random.random() < config.probability
    
    async def simulate_tool_response(
        self,
        tool_name: str,
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Simulate tool response with potential edge cases.
        
        Args:
            tool_name: Tool name
            input_data: Tool input data
            
        Returns:
            Simulated tool response
        """
        # Check for empty response
        if self.should_trigger_edge_case(EdgeCaseType.EMPTY_RESPONSE):
            self.edge_case_history.append(EdgeCaseType.EMPTY_RESPONSE)
            return self._generate_empty_response()
        
        # Check for timeout
        if self.should_trigger_edge_case(EdgeCaseType.TIMEOUT):
            self.edge_case_history.append(EdgeCaseType.TIMEOUT)
            raise asyncio.TimeoutError(f"Tool {tool_name} timed out")
        
        # Check for network error
        if self.should_trigger_edge_case(EdgeCaseType.NETWORK_ERROR):
            self.edge_case_history.append(EdgeCaseType.NETWORK_ERROR)
            raise ConnectionError(f"Network error for tool {tool_name}")
        
        # Check for rate limit
        if self.should_trigger_edge_case(EdgeCaseType.RATE_LIMIT):
            self.edge_case_history.append(EdgeCaseType.RATE_LIMIT)
            raise Exception(f"Rate limit exceeded for tool {tool_name}")
        
        # Normal response
        return {
            "tool": tool_name,
            "result": "success",
            "data": input_data
        }
    
    def _generate_empty_response(
        self
    ) -> Dict[str, Any]:
        """
        Generate empty response.
        
        Returns:
            Empty response dictionary
        """
        return {
            "tool": "",
            "result": "",
            "data": {}
        }
    
    async def simulate_llm_call(
        self,
        prompt: str,
        model: str = "gpt-4"
    ) -> str:
        """
        Simulate LLM call with potential edge cases.
        
        Args:
            prompt: Input prompt
            model: Model name
            
        Returns:
            LLM response
        """
        # Check for timeout
        if self.should_trigger_edge_case(EdgeCaseType.TIMEOUT):
            self.edge_case_history.append(EdgeCaseType.TIMEOUT)
            await asyncio.sleep(60)  # Simulate timeout
            raise asyncio.TimeoutError("LLM call timed out")
        
        # Check for rate limit
        if self.should_trigger_edge_case(EdgeCaseType.RATE_LIMIT):
            self.edge_case_history.append(EdgeCaseType.RATE_LIMIT)
            raise Exception("Rate limit exceeded")
        
        # Normal response
        return f"Response to: {prompt[:50]}..."
    
    def simulate_partial_failure(
        self,
        operations: List[str]
    ) -> Dict[str, Any]:
        """
        Simulate partial failure scenario.
        
        Args:
            operations: List of operations to execute
            
        Returns:
            Results dictionary with success/failure for each operation
        """
        results = {}
        
        for op in operations:
            if self.should_trigger_edge_case(EdgeCaseType.PARTIAL_FAILURE):
                results[op] = {
                    "success": False,
                    "error": "Partial failure simulated"
                }
                self.edge_case_history.append(EdgeCaseType.PARTIAL_FAILURE)
            else:
                results[op] = {
                    "success": True,
                    "result": f"Result for {op}"
                }
        
        return results
    
    def get_edge_case_history(
        self
    ) -> List[EdgeCaseType]:
        """
        Get history of triggered edge cases.
        
        Returns:
            List of triggered edge case types
        """
        return self.edge_case_history.copy()


# ============================================================================
# Property-Based Testing Framework
# ============================================================================

@dataclass
class PropertyTest:
    """
    Property test definition.
    
    This demonstrates property test structure:
    - Property name
    - Property function
    - Input strategy
    """
    name: str
    property_func: Callable
    input_strategy: Optional[Any] = None


class PropertyBasedTestFramework:
    """
    Framework for property-based testing.
    
    This demonstrates property-based testing patterns:
    - Property definition
    - Input generation
    - Property validation
    - Shrinking
    """
    
    def __init__(self):
        """Initialize property-based test framework."""
        self.properties: List[PropertyTest] = []
        self.test_results: Dict[str, List[Dict[str, Any]]] = {}
    
    def register_property(
        self,
        name: str,
        property_func: Callable,
        input_strategy: Optional[Any] = None
    ):
        """
        Register a property test.
        
        Args:
            name: Property name
            property_func: Property function to test
            input_strategy: Optional input generation strategy
        """
        self.properties.append(
            PropertyTest(
                name=name,
                property_func=property_func,
                input_strategy=input_strategy
            )
        )
    
    def generate_inputs(
        self,
        strategy: Optional[Any],
        count: int = 100
    ) -> List[Any]:
        """
        Generate test inputs using strategy.
        
        Args:
            strategy: Input generation strategy
            count: Number of inputs to generate
            
        Returns:
            List of generated inputs
        """
        if strategy is None:
            # Default strategy: generate random strings
            return [f"input_{i}" for i in range(count)]
        
        # In real implementation, use Hypothesis strategies
        # from hypothesis import strategies as st
        # return [strategy.example() for _ in range(count)]
        
        return [strategy for _ in range(count)]
    
    def test_property(
        self,
        property_name: str,
        max_examples: int = 100
    ) -> Dict[str, Any]:
        """
        Test a property with generated inputs.
        
        Args:
            property_name: Name of property to test
            max_examples: Maximum number of examples to test
            
        Returns:
            Test results dictionary
        """
        property_test = next(
            (p for p in self.properties if p.name == property_name),
            None
        )
        
        if not property_test:
            return {
                "success": False,
                "error": f"Property {property_name} not found"
            }
        
        # Generate inputs
        inputs = self.generate_inputs(
            property_test.input_strategy,
            max_examples
        )
        
        # Test property for each input
        failures = []
        for i, input_val in enumerate(inputs):
            try:
                result = property_test.property_func(input_val)
                if not result:
                    failures.append({
                        "input": input_val,
                        "index": i
                    })
            except Exception as e:
                failures.append({
                    "input": input_val,
                    "index": i,
                    "error": str(e)
                })
        
        success = len(failures) == 0
        
        result = {
            "success": success,
            "total_tests": len(inputs),
            "failures": len(failures),
            "failure_examples": failures[:5]  # First 5 failures
        }
        
        # Store results
        if property_name not in self.test_results:
            self.test_results[property_name] = []
        self.test_results[property_name].append(result)
        
        return result
    
    def test_all_properties(
        self,
        max_examples: int = 100
    ) -> Dict[str, Dict[str, Any]]:
        """
        Test all registered properties.
        
        Args:
            max_examples: Maximum number of examples per property
            
        Returns:
            Dictionary of property name -> test results
        """
        results = {}
        
        for property_test in self.properties:
            results[property_test.name] = self.test_property(
                property_test.name,
                max_examples
            )
        
        return results


# ============================================================================
# Mock Tool Response Generators
# ============================================================================

class MockToolResponseGenerator:
    """
    Generator for mock tool responses.
    
    This demonstrates mock response generation:
    - Empty responses
    - Error responses
    - Partial responses
    - Malformed responses
    """
    
    @staticmethod
    def generate_empty_response(
        tool_name: str
    ) -> Dict[str, Any]:
        """
        Generate empty tool response.
        
        Args:
            tool_name: Tool name
            
        Returns:
            Empty response dictionary
        """
        return {
            "tool": tool_name,
            "result": None,
            "data": {}
        }
    
    @staticmethod
    def generate_error_response(
        tool_name: str,
        error_type: str = "generic_error"
    ) -> Dict[str, Any]:
        """
        Generate error tool response.
        
        Args:
            tool_name: Tool name
            error_type: Error type
            
        Returns:
            Error response dictionary
        """
        return {
            "tool": tool_name,
            "success": False,
            "error": {
                "type": error_type,
                "message": f"Error in {tool_name}"
            }
        }
    
    @staticmethod
    def generate_partial_response(
        tool_name: str,
        partial_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate partial tool response.
        
        Args:
            tool_name: Tool name
            partial_data: Partial data
            
        Returns:
            Partial response dictionary
        """
        return {
            "tool": tool_name,
            "success": True,
            "partial": True,
            "data": partial_data
        }
    
    @staticmethod
    def generate_malformed_response(
        tool_name: str
    ) -> str:
        """
        Generate malformed tool response.
        
        Args:
            tool_name: Tool name
            
        Returns:
            Malformed response string
        """
        # Return invalid JSON or wrong format
        return f"Invalid response from {tool_name}: {{invalid json"


# ============================================================================
# Chaos Testing Examples
# ============================================================================

class ChaosTestScenario:
    """
    Chaos test scenario definition.
    
    This demonstrates chaos test configuration:
    - Failure type
    - Failure rate
    - Duration
    - Recovery pattern
    """
    
    def __init__(
        self,
        failure_type: str,
        failure_rate: float = 0.1,
        duration: int = 60,
        recovery_pattern: str = "immediate"
    ):
        """
        Initialize chaos test scenario.
        
        Args:
            failure_type: Type of failure to inject
            failure_rate: Probability of failure (0.0-1.0)
            duration: Duration in seconds
            recovery_pattern: Recovery pattern (immediate, gradual, manual)
        """
        self.failure_type = failure_type
        self.failure_rate = failure_rate
        self.duration = duration
        self.recovery_pattern = recovery_pattern
        self.start_time: Optional[datetime] = None
        self.failure_count = 0
        self.total_requests = 0
    
    def should_inject_failure(
        self
    ) -> bool:
        """
        Check if failure should be injected.
        
        Returns:
            True if should inject failure
        """
        if self.start_time is None:
            self.start_time = datetime.now()
        
        elapsed = (datetime.now() - self.start_time).total_seconds()
        if elapsed > self.duration:
            return False
        
        self.total_requests += 1
        should_fail = random.random() < self.failure_rate
        
        if should_fail:
            self.failure_count += 1
        
        return should_fail
    
    def get_statistics(
        self
    ) -> Dict[str, Any]:
        """
        Get chaos test statistics.
        
        Returns:
            Statistics dictionary
        """
        actual_rate = (
            self.failure_count / self.total_requests
            if self.total_requests > 0
            else 0.0
        )
        
        return {
            "failure_type": self.failure_type,
            "target_rate": self.failure_rate,
            "actual_rate": actual_rate,
            "failure_count": self.failure_count,
            "total_requests": self.total_requests,
            "duration": self.duration
        }


class ChaosTestRunner:
    """
    Runner for chaos tests.
    
    This demonstrates chaos test execution:
    - Scenario execution
    - Failure injection
    - Metrics collection
    - Recovery validation
    """
    
    def __init__(self):
        """Initialize chaos test runner."""
        self.scenarios: List[ChaosTestScenario] = []
        self.active_scenarios: Dict[str, ChaosTestScenario] = {}
    
    def add_scenario(
        self,
        scenario: ChaosTestScenario
    ):
        """
        Add chaos test scenario.
        
        Args:
            scenario: Chaos test scenario
        """
        self.scenarios.append(scenario)
    
    async def run_scenario(
        self,
        scenario: ChaosTestScenario,
        test_function: Callable
    ) -> Dict[str, Any]:
        """
        Run chaos test scenario.
        
        Args:
            scenario: Chaos test scenario
            test_function: Function to test under chaos conditions
            
        Returns:
            Test results dictionary
        """
        self.active_scenarios[scenario.failure_type] = scenario
        
        try:
            # Run test function with chaos injection
            results = await test_function(scenario)
            
            # Collect statistics
            stats = scenario.get_statistics()
            
            return {
                "success": True,
                "scenario": scenario.failure_type,
                "statistics": stats,
                "test_results": results
            }
        except Exception as e:
            return {
                "success": False,
                "scenario": scenario.failure_type,
                "error": str(e),
                "statistics": scenario.get_statistics()
            }
        finally:
            if scenario.failure_type in self.active_scenarios:
                del self.active_scenarios[scenario.failure_type]
    
    def is_failure_injected(
        self,
        failure_type: str
    ) -> bool:
        """
        Check if failure should be injected.
        
        Args:
            failure_type: Type of failure
            
        Returns:
            True if should inject failure
        """
        scenario = self.active_scenarios.get(failure_type)
        if not scenario:
            return False
        
        return scenario.should_inject_failure()
