"""
Graph Traversal Testing Examples

This file demonstrates graph traversal testing patterns and test implementation.
Reference this example from RULE.mdc using @examples_traversal_tests.py syntax.
"""

from typing import List, Dict, Any, Optional, Set, Tuple
from dataclasses import dataclass
from enum import Enum


# ============================================================================
# Execution Trace Structure
# ============================================================================

@dataclass
class NodeExecution:
    """
    Node execution record from trace.
    
    This demonstrates execution trace structure:
    - Node name and execution time
    - State before and after
    - Routing decision
    """
    node_name: str
    timestamp: float
    state_before: Dict[str, Any]
    state_after: Dict[str, Any]
    routing_decision: Optional[str] = None
    error: Optional[str] = None


@dataclass
class ExecutionTrace:
    """
    Complete execution trace.
    
    This demonstrates trace structure:
    - Sequence of node executions
    - Total execution time
    - Final state
    """
    node_sequence: List[NodeExecution]
    total_time: float
    final_state: Dict[str, Any]
    input_state: Dict[str, Any]


# ============================================================================
# Test Base Classes
# ============================================================================

class TraversalTestResult(Enum):
    """
    Test result types.
    
    This demonstrates test outcomes:
    - PASS: Test passed
    - FAIL: Test failed
    - WARNING: Test passed with warnings
    """
    PASS = "pass"
    FAIL = "fail"
    WARNING = "warning"


@dataclass
class TraversalTestResult:
    """
    Test result structure.
    
    This demonstrates test result:
    - Pass/fail status
    - Actual vs expected paths
    - Deviation details
    - Error messages
    """
    test_name: str
    passed: bool
    actual_path: List[str]
    expected_path: Optional[List[str]] = None
    deviations: List[str] = None
    error_message: Optional[str] = None


class GraphTraversalTest:
    """
    Base class for graph traversal tests.
    
    This demonstrates test base pattern:
    - Test execution
    - Path extraction
    - Validation
    - Result generation
    """
    
    def __init__(self, test_name: str):
        """
        Initialize test.
        
        Args:
            test_name: Name of the test
        """
        self.test_name = test_name
    
    def extract_path(self, trace: ExecutionTrace) -> List[str]:
        """
        Extract node sequence from trace.
        
        Args:
            trace: Execution trace
        
        Returns:
            List of node names in execution order
        """
        return [node.node_name for node in trace.node_sequence]
    
    def run(self, trace: ExecutionTrace) -> TraversalTestResult:
        """
        Run test on execution trace.
        
        Args:
            trace: Execution trace
        
        Returns:
            TraversalTestResult
        """
        actual_path = self.extract_path(trace)
        return self.validate(actual_path, trace)
    
    def validate(
        self,
        actual_path: List[str],
        trace: ExecutionTrace
    ) -> TraversalTestResult:
        """
        Validate path (to be implemented by subclasses).
        
        Args:
            actual_path: Actual node sequence
            trace: Execution trace
        
        Returns:
            TraversalTestResult
        """
        raise NotImplementedError


# ============================================================================
# Expected Path Test
# ============================================================================

class ExpectedPathTest(GraphTraversalTest):
    """
    Test that verifies agent follows expected path.
    
    This demonstrates expected path testing:
    - Define expected node sequence
    - Compare with actual path
    - Identify deviations
    """
    
    def __init__(
        self,
        test_name: str,
        expected_path: List[str],
        allow_partial: bool = False
    ):
        """
        Initialize expected path test.
        
        Args:
            test_name: Test name
            expected_path: Expected node sequence
            allow_partial: Allow partial matches
        """
        super().__init__(test_name)
        self.expected_path = expected_path
        self.allow_partial = allow_partial
    
    def validate(
        self,
        actual_path: List[str],
        trace: ExecutionTrace
    ) -> TraversalTestResult:
        """
        Validate actual path matches expected.
        
        Args:
            actual_path: Actual node sequence
            trace: Execution trace
        
        Returns:
            TraversalTestResult
        """
        deviations = []
        
        # Check exact match
        if actual_path == self.expected_path:
            return TraversalTestResult(
                test_name=self.test_name,
                passed=True,
                actual_path=actual_path,
                expected_path=self.expected_path
            )
        
        # Check partial match if allowed
        if self.allow_partial:
            # Check if expected path is prefix of actual path
            if len(actual_path) >= len(self.expected_path):
                if actual_path[:len(self.expected_path)] == self.expected_path:
                    return TraversalTestResult(
                        test_name=self.test_name,
                        passed=True,
                        actual_path=actual_path,
                        expected_path=self.expected_path,
                        deviations=["Path extended beyond expected"]
                    )
        
        # Find deviations
        min_len = min(len(actual_path), len(self.expected_path))
        for i in range(min_len):
            if actual_path[i] != self.expected_path[i]:
                deviations.append(
                    f"Position {i}: expected '{self.expected_path[i]}', "
                    f"got '{actual_path[i]}'"
                )
        
        if len(actual_path) != len(self.expected_path):
            deviations.append(
                f"Length mismatch: expected {len(self.expected_path)} nodes, "
                f"got {len(actual_path)} nodes"
            )
        
        return TraversalTestResult(
            test_name=self.test_name,
            passed=False,
            actual_path=actual_path,
            expected_path=self.expected_path,
            deviations=deviations,
            error_message="Path does not match expected sequence"
        )


# ============================================================================
# Forbidden Path Test
# ============================================================================

class ForbiddenPathTest(GraphTraversalTest):
    """
    Test that verifies agent does NOT traverse forbidden paths.
    
    This demonstrates forbidden path testing:
    - Define forbidden nodes or sequences
    - Verify they were not executed
    - Report violations
    """
    
    def __init__(
        self,
        test_name: str,
        forbidden_nodes: Optional[Set[str]] = None,
        forbidden_sequences: Optional[List[List[str]]] = None
    ):
        """
        Initialize forbidden path test.
        
        Args:
            test_name: Test name
            forbidden_nodes: Set of nodes that should not be executed
            forbidden_sequences: List of node sequences that should not occur
        """
        super().__init__(test_name)
        self.forbidden_nodes = forbidden_nodes or set()
        self.forbidden_sequences = forbidden_sequences or []
    
    def validate(
        self,
        actual_path: List[str],
        trace: ExecutionTrace
    ) -> TraversalTestResult:
        """
        Validate no forbidden nodes/sequences executed.
        
        Args:
            actual_path: Actual node sequence
            trace: Execution trace
        
        Returns:
            TraversalTestResult
        """
        deviations = []
        
        # Check forbidden nodes
        executed_forbidden = []
        for node in actual_path:
            if node in self.forbidden_nodes:
                executed_forbidden.append(node)
        
        if executed_forbidden:
            deviations.append(
                f"Forbidden nodes executed: {executed_forbidden}"
            )
        
        # Check forbidden sequences
        for forbidden_seq in self.forbidden_sequences:
            if self._contains_sequence(actual_path, forbidden_seq):
                deviations.append(
                    f"Forbidden sequence executed: {forbidden_seq}"
                )
        
        passed = len(deviations) == 0
        
        return TraversalTestResult(
            test_name=self.test_name,
            passed=passed,
            actual_path=actual_path,
            deviations=deviations if not passed else None,
            error_message="Forbidden path executed" if not passed else None
        )
    
    def _contains_sequence(self, path: List[str], sequence: List[str]) -> bool:
        """
        Check if path contains sequence.
        
        Args:
            path: Node path
            sequence: Sequence to find
        
        Returns:
            True if sequence found
        """
        if len(sequence) > len(path):
            return False
        
        for i in range(len(path) - len(sequence) + 1):
            if path[i:i+len(sequence)] == sequence:
                return True
        
        return False


# ============================================================================
# Node Coverage Test
# ============================================================================

class NodeCoverageTest(GraphTraversalTest):
    """
    Test that verifies required nodes were executed.
    
    This demonstrates node coverage testing:
    - Define required and optional nodes
    - Verify required nodes executed
    - Report missing nodes
    """
    
    def __init__(
        self,
        test_name: str,
        required_nodes: Set[str],
        optional_nodes: Optional[Set[str]] = None
    ):
        """
        Initialize node coverage test.
        
        Args:
            test_name: Test name
            required_nodes: Set of nodes that must be executed
            optional_nodes: Set of nodes that may be executed
        """
        super().__init__(test_name)
        self.required_nodes = required_nodes
        self.optional_nodes = optional_nodes or set()
    
    def validate(
        self,
        actual_path: List[str],
        trace: ExecutionTrace
    ) -> TraversalTestResult:
        """
        Validate required nodes executed.
        
        Args:
            actual_path: Actual node sequence
            trace: Execution trace
        
        Returns:
            TraversalTestResult
        """
        actual_nodes = set(actual_path)
        missing_nodes = self.required_nodes - actual_nodes
        
        deviations = []
        if missing_nodes:
            deviations.append(
                f"Required nodes not executed: {missing_nodes}"
            )
        
        # Check for unexpected nodes (not in required or optional)
        unexpected_nodes = actual_nodes - self.required_nodes - self.optional_nodes
        if unexpected_nodes:
            deviations.append(
                f"Unexpected nodes executed: {unexpected_nodes}"
            )
        
        passed = len(missing_nodes) == 0
        
        return TraversalTestResult(
            test_name=self.test_name,
            passed=passed,
            actual_path=actual_path,
            deviations=deviations if not passed else None,
            error_message="Required nodes missing" if not passed else None
        )


# ============================================================================
# Sequence Validation Test
# ============================================================================

class SequenceValidationTest(GraphTraversalTest):
    """
    Test that verifies nodes executed in correct order.
    
    This demonstrates sequence validation:
    - Define node dependencies
    - Verify dependencies satisfied
    - Report order violations
    """
    
    def __init__(
        self,
        test_name: str,
        dependencies: List[Tuple[str, str]]  # (before, after) pairs
    ):
        """
        Initialize sequence validation test.
        
        Args:
            test_name: Test name
            dependencies: List of (before_node, after_node) pairs
        """
        super().__init__(test_name)
        self.dependencies = dependencies
    
    def validate(
        self,
        actual_path: List[str],
        trace: ExecutionTrace
    ) -> TraversalTestResult:
        """
        Validate dependencies satisfied.
        
        Args:
            actual_path: Actual node sequence
            trace: Execution trace
        
        Returns:
            TraversalTestResult
        """
        deviations = []
        
        # Build node position map
        node_positions = {node: i for i, node in enumerate(actual_path)}
        
        # Check each dependency
        for before_node, after_node in self.dependencies:
            if before_node not in node_positions:
                deviations.append(
                    f"Dependency violation: '{before_node}' not executed "
                    f"(required before '{after_node}')"
                )
                continue
            
            if after_node not in node_positions:
                deviations.append(
                    f"Dependency violation: '{after_node}' not executed "
                    f"(required after '{before_node}')"
                )
                continue
            
            if node_positions[before_node] >= node_positions[after_node]:
                deviations.append(
                    f"Order violation: '{before_node}' (position {node_positions[before_node]}) "
                    f"must execute before '{after_node}' (position {node_positions[after_node]})"
                )
        
        passed = len(deviations) == 0
        
        return TraversalTestResult(
            test_name=self.test_name,
            passed=passed,
            actual_path=actual_path,
            deviations=deviations if not passed else None,
            error_message="Sequence dependencies violated" if not passed else None
        )


# ============================================================================
# Trace Analysis
# ============================================================================

class TraceAnalyzer:
    """
    Service for analyzing execution traces.
    
    This demonstrates trace analysis patterns:
    - Extract paths from traces
    - Identify routing decisions
    - Reconstruct reasoning chains
    """
    
    def extract_path(self, trace: ExecutionTrace) -> List[str]:
        """
        Extract node sequence from trace.
        
        Args:
            trace: Execution trace
        
        Returns:
            List of node names
        """
        return [node.node_name for node in trace.node_sequence]
    
    def extract_routing_decisions(
        self,
        trace: ExecutionTrace
    ) -> List[Dict[str, Any]]:
        """
        Extract routing decisions from trace.
        
        Args:
            trace: Execution trace
        
        Returns:
            List of routing decisions
        """
        decisions = []
        
        for node in trace.node_sequence:
            if node.routing_decision:
                decisions.append({
                    "from_node": node.node_name,
                    "decision": node.routing_decision,
                    "timestamp": node.timestamp
                })
        
        return decisions
    
    def compare_paths(
        self,
        actual_path: List[str],
        expected_path: List[str]
    ) -> Dict[str, Any]:
        """
        Compare actual and expected paths.
        
        Args:
            actual_path: Actual node sequence
            expected_path: Expected node sequence
        
        Returns:
            Comparison results
        """
        matches = []
        mismatches = []
        
        min_len = min(len(actual_path), len(expected_path))
        for i in range(min_len):
            if actual_path[i] == expected_path[i]:
                matches.append((i, actual_path[i]))
            else:
                mismatches.append({
                    "position": i,
                    "expected": expected_path[i],
                    "actual": actual_path[i]
                })
        
        return {
            "matches": matches,
            "mismatches": mismatches,
            "length_match": len(actual_path) == len(expected_path),
            "exact_match": actual_path == expected_path
        }


# ============================================================================
# Test Suite
# ============================================================================

class GraphTraversalTestSuite:
    """
    Test suite for graph traversal tests.
    
    This demonstrates test suite patterns:
    - Run multiple tests
    - Aggregate results
    - Generate reports
    """
    
    def __init__(self):
        """Initialize test suite."""
        self.tests: List[GraphTraversalTest] = []
    
    def add_test(self, test: GraphTraversalTest):
        """
        Add test to suite.
        
        Args:
            test: Test to add
        """
        self.tests.append(test)
    
    def run_suite(self, trace: ExecutionTrace) -> Dict[str, Any]:
        """
        Run all tests on trace.
        
        Args:
            trace: Execution trace
        
        Returns:
            Test results summary
        """
        results = []
        passed_count = 0
        failed_count = 0
        
        for test in self.tests:
            result = test.run(trace)
            results.append(result)
            
            if result.passed:
                passed_count += 1
            else:
                failed_count += 1
        
        return {
            "total_tests": len(self.tests),
            "passed": passed_count,
            "failed": failed_count,
            "pass_rate": passed_count / len(self.tests) if self.tests else 0.0,
            "results": results
        }


# ============================================================================
# Example: Complete Test Workflow
# ============================================================================

def example_traversal_test_workflow():
    """
    Example complete test workflow.
    
    This demonstrates:
    - Creating execution trace
    - Running multiple test types
    - Analyzing results
    """
    # Create mock execution trace
    trace = ExecutionTrace(
        node_sequence=[
            NodeExecution("orchestrator", 0.0, {}, {"sections": []}),
            NodeExecution("worker_1", 1.0, {}, {"result": "data1"}),
            NodeExecution("worker_2", 2.0, {}, {"result": "data2"}),
            NodeExecution("synthesizer", 3.0, {}, {"final_output": "result"})
        ],
        total_time=3.0,
        final_state={"final_output": "result"},
        input_state={"user_input": "test"}
    )
    
    # Create test suite
    suite = GraphTraversalTestSuite()
    
    # Add expected path test
    suite.add_test(ExpectedPathTest(
        test_name="happy_path",
        expected_path=["orchestrator", "worker_1", "worker_2", "synthesizer"]
    ))
    
    # Add forbidden path test
    suite.add_test(ForbiddenPathTest(
        test_name="no_error_path",
        forbidden_nodes={"error_handler", "fallback_node"}
    ))
    
    # Add node coverage test
    suite.add_test(NodeCoverageTest(
        test_name="all_workers_execute",
        required_nodes={"orchestrator", "worker_1", "worker_2", "synthesizer"}
    ))
    
    # Add sequence validation test
    suite.add_test(SequenceValidationTest(
        test_name="orchestrator_before_workers",
        dependencies=[
            ("orchestrator", "worker_1"),
            ("orchestrator", "worker_2"),
            ("worker_1", "synthesizer"),
            ("worker_2", "synthesizer")
        ]
    ))
    
    # Run suite
    results = suite.run_suite(trace)
    
    return results
