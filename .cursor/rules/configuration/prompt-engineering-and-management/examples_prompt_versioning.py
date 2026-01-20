"""
Prompt Versioning Examples

This file demonstrates version control patterns and A/B testing implementation.
Reference this example from RULE.mdc using @examples_prompt_versioning.py syntax.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import yaml


# ============================================================================
# Version Management
# ============================================================================

@dataclass
class PromptVersion:
    """
    Prompt version structure.
    
    This demonstrates prompt versioning:
    - Version number (semantic versioning)
    - Version tags
    - Metadata and changelog
    - Performance metrics
    """
    version: str  # e.g., "1.0.0"
    prompt_id: str
    content: str
    created_at: datetime
    tags: List[str]
    metadata: Dict[str, Any]
    changelog: str
    performance_metrics: Optional[Dict[str, float]] = None


class VersionTag(Enum):
    """
    Version tags for prompt management.
    
    This demonstrates version tagging:
    - Production: Stable, in production
    - Experimental: Testing new versions
    - Deprecated: Old versions, being phased out
    """
    PRODUCTION = "production"
    EXPERIMENTAL = "experimental"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"


class PromptVersionManager:
    """
    Manager for prompt versioning.
    
    This demonstrates version management patterns:
    - Version creation and tracking
    - A/B testing setup
    - Rollback capabilities
    - Version comparison
    """
    
    def __init__(self):
        """Initialize version manager."""
        self.versions: Dict[str, List[PromptVersion]] = {}  # prompt_id -> versions
    
    def create_version(
        self,
        prompt_id: str,
        content: str,
        version: str,
        changelog: str,
        tags: Optional[List[str]] = None
    ) -> PromptVersion:
        """
        Create a new prompt version.
        
        Args:
            prompt_id: Prompt identifier
            content: Prompt content
            version: Version number (semantic versioning)
            changelog: Description of changes
            tags: Optional tags
        
        Returns:
            Created PromptVersion
        """
        prompt_version = PromptVersion(
            version=version,
            prompt_id=prompt_id,
            content=content,
            created_at=datetime.now(),
            tags=tags or [],
            metadata={},
            changelog=changelog
        )
        
        if prompt_id not in self.versions:
            self.versions[prompt_id] = []
        
        self.versions[prompt_id].append(prompt_version)
        
        return prompt_version
    
    def get_version(
        self,
        prompt_id: str,
        version: Optional[str] = None,
        tag: Optional[VersionTag] = None
    ) -> Optional[PromptVersion]:
        """
        Get prompt version.
        
        Args:
            prompt_id: Prompt identifier
            version: Specific version number (None for latest)
            tag: Version tag filter
        
        Returns:
            PromptVersion or None
        """
        if prompt_id not in self.versions:
            return None
        
        versions = self.versions[prompt_id]
        
        # Filter by tag if specified
        if tag:
            versions = [v for v in versions if tag.value in v.tags]
        
        if not versions:
            return None
        
        # Get specific version or latest
        if version:
            for v in versions:
                if v.version == version:
                    return v
            return None
        
        # Return latest version
        return max(versions, key=lambda v: v.created_at)
    
    def list_versions(self, prompt_id: str) -> List[PromptVersion]:
        """
        List all versions for a prompt.
        
        Args:
            prompt_id: Prompt identifier
        
        Returns:
            List of PromptVersion
        """
        return self.versions.get(prompt_id, [])


# ============================================================================
# A/B Testing
# ============================================================================

@dataclass
class ABTestConfig:
    """
    A/B test configuration.
    
    This demonstrates A/B testing setup:
    - Traffic splitting
    - Version assignments
    - Metrics collection
    """
    prompt_id: str
    version_a: str
    version_b: str
    traffic_split: float  # 0.0-1.0, percentage for version A
    start_date: datetime
    end_date: Optional[datetime] = None
    metrics: Dict[str, float] = None


class ABTestManager:
    """
    Manager for A/B testing prompts.
    
    This demonstrates A/B testing patterns:
    - Traffic splitting
    - Version assignment
    - Metrics collection
    - Winner selection
    """
    
    def __init__(self, version_manager: PromptVersionManager):
        """
        Initialize A/B test manager.
        
        Args:
            version_manager: Prompt version manager
        """
        self.version_manager = version_manager
        self.active_tests: Dict[str, ABTestConfig] = {}
        self.test_results: Dict[str, Dict[str, Any]] = {}
    
    def start_ab_test(
        self,
        prompt_id: str,
        version_a: str,
        version_b: str,
        traffic_split: float = 0.5
    ) -> ABTestConfig:
        """
        Start A/B test.
        
        Args:
            prompt_id: Prompt identifier
            version_a: Version A identifier
            version_b: Version B identifier
            traffic_split: Traffic split (0.5 = 50/50)
        
        Returns:
            ABTestConfig
        """
        test_config = ABTestConfig(
            prompt_id=prompt_id,
            version_a=version_a,
            version_b=version_b,
            traffic_split=traffic_split,
            start_date=datetime.now(),
            metrics={}
        )
        
        self.active_tests[prompt_id] = test_config
        self.test_results[prompt_id] = {
            "version_a": {"count": 0, "success": 0, "quality_score": 0.0},
            "version_b": {"count": 0, "success": 0, "quality_score": 0.0}
        }
        
        return test_config
    
    def assign_version(
        self,
        prompt_id: str,
        user_id: str
    ) -> str:
        """
        Assign version for A/B test.
        
        Args:
            prompt_id: Prompt identifier
            user_id: User identifier for consistent assignment
        
        Returns:
            Version identifier
        """
        if prompt_id not in self.active_tests:
            # No active test, return production version
            version = self.version_manager.get_version(prompt_id, tag=VersionTag.PRODUCTION)
            return version.version if version else "latest"
        
        test_config = self.active_tests[prompt_id]
        
        # Consistent assignment based on user_id hash
        import hashlib
        user_hash = int(hashlib.md5(user_id.encode()).hexdigest(), 16)
        assignment = (user_hash % 100) / 100.0
        
        if assignment < test_config.traffic_split:
            return test_config.version_a
        else:
            return test_config.version_b
    
    def record_result(
        self,
        prompt_id: str,
        version: str,
        success: bool,
        quality_score: float
    ):
        """
        Record test result.
        
        Args:
            prompt_id: Prompt identifier
            version: Version used
            success: Whether request was successful
            quality_score: Quality score (0.0-1.0)
        """
        if prompt_id not in self.test_results:
            return
        
        results = self.test_results[prompt_id]
        version_key = "version_a" if version == self.active_tests[prompt_id].version_a else "version_b"
        
        results[version_key]["count"] += 1
        if success:
            results[version_key]["success"] += 1
        results[version_key]["quality_score"] = (
            (results[version_key]["quality_score"] * (results[version_key]["count"] - 1) + quality_score) /
            results[version_key]["count"]
        )
    
    def get_winner(self, prompt_id: str) -> Optional[str]:
        """
        Get winning version from A/B test.
        
        Args:
            prompt_id: Prompt identifier
        
        Returns:
            Winning version identifier or None
        """
        if prompt_id not in self.test_results:
            return None
        
        results = self.test_results[prompt_id]
        
        # Compare quality scores
        score_a = results["version_a"]["quality_score"]
        score_b = results["version_b"]["quality_score"]
        
        if score_a > score_b:
            return self.active_tests[prompt_id].version_a
        elif score_b > score_a:
            return self.active_tests[prompt_id].version_b
        
        return None  # Tie or insufficient data


# ============================================================================
# YAML Management
# ============================================================================

def load_prompt_from_yaml(yaml_path: str) -> Dict[str, Any]:
    """
    Load prompt from YAML file.
    
    This demonstrates YAML prompt loading:
    - Parse YAML structure
    - Extract prompt content
    - Extract metadata and variables
    - Load examples and tests
    
    Args:
        yaml_path: Path to YAML file
    
    Returns:
        Parsed prompt dictionary
    """
    with open(yaml_path, 'r') as f:
        data = yaml.safe_load(f)
    
    return {
        "version": data.get("version"),
        "name": data.get("name"),
        "description": data.get("description"),
        "variables": data.get("variables", []),
        "prompt": data.get("prompt"),
        "examples": data.get("examples", []),
        "tests": data.get("tests", [])
    }


def save_prompt_to_yaml(
    prompt_data: Dict[str, Any],
    yaml_path: str
):
    """
    Save prompt to YAML file.
    
    This demonstrates YAML prompt saving:
    - Structure prompt data
    - Write to YAML format
    - Include metadata and examples
    
    Args:
        prompt_data: Prompt data dictionary
        yaml_path: Path to save YAML file
    """
    yaml_data = {
        "version": prompt_data.get("version", "1.0.0"),
        "name": prompt_data.get("name"),
        "description": prompt_data.get("description"),
        "variables": prompt_data.get("variables", []),
        "prompt": prompt_data.get("prompt"),
        "examples": prompt_data.get("examples", []),
        "tests": prompt_data.get("tests", [])
    }
    
    with open(yaml_path, 'w') as f:
        yaml.dump(yaml_data, f, default_flow_style=False, sort_keys=False)


# ============================================================================
# Rollback Management
# ============================================================================

class RollbackManager:
    """
    Manager for prompt rollback.
    
    This demonstrates rollback patterns:
    - Quick rollback to previous version
    - Rollback triggers
    - Version comparison
    """
    
    def __init__(self, version_manager: PromptVersionManager):
        """
        Initialize rollback manager.
        
        Args:
            version_manager: Prompt version manager
        """
        self.version_manager = version_manager
    
    def rollback(
        self,
        prompt_id: str,
        target_version: Optional[str] = None
    ) -> bool:
        """
        Rollback prompt to previous or specified version.
        
        Args:
            prompt_id: Prompt identifier
            target_version: Target version (None for previous)
        
        Returns:
            True if rollback successful
        """
        versions = self.version_manager.list_versions(prompt_id)
        if not versions:
            return False
        
        # Sort by creation date
        versions.sort(key=lambda v: v.created_at, reverse=True)
        
        # Get target version
        if target_version:
            target = next((v for v in versions if v.version == target_version), None)
        else:
            # Rollback to previous version (skip current production)
            current = next((v for v in versions if VersionTag.PRODUCTION.value in v.tags), None)
            if not current or len(versions) < 2:
                return False
            target = versions[1]  # Second most recent
        
        if not target:
            return False
        
        # Update tags: remove production from current, add to target
        current = versions[0]
        if VersionTag.PRODUCTION.value in current.tags:
            current.tags.remove(VersionTag.PRODUCTION.value)
        
        if VersionTag.PRODUCTION.value not in target.tags:
            target.tags.append(VersionTag.PRODUCTION.value)
        
        return True
    
    def should_rollback(
        self,
        prompt_id: str,
        quality_threshold: float = 0.7,
        error_rate_threshold: float = 0.1
    ) -> bool:
        """
        Check if rollback should be triggered.
        
        Args:
            prompt_id: Prompt identifier
            quality_threshold: Minimum quality score
            error_rate_threshold: Maximum error rate
        
        Returns:
            True if rollback should be triggered
        """
        current_version = self.version_manager.get_version(prompt_id, tag=VersionTag.PRODUCTION)
        if not current_version or not current_version.performance_metrics:
            return False
        
        metrics = current_version.performance_metrics
        
        # Check quality threshold
        quality = metrics.get("quality_score", 1.0)
        if quality < quality_threshold:
            return True
        
        # Check error rate
        error_rate = metrics.get("error_rate", 0.0)
        if error_rate > error_rate_threshold:
            return True
        
        return False


# ============================================================================
# Runtime A/B Testing in Agentic Loops
# ============================================================================

@dataclass
class RuntimeMetrics:
    """
    Runtime metrics for prompt version.
    
    This demonstrates in-loop metrics:
    - Quality score
    - Latency
    - Cost
    - Success status
    """
    version: str
    quality_score: float = 0.0
    latency: float = 0.0
    cost: float = 0.0
    success: bool = True
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class ABTestContext:
    """
    A/B test context for LangGraph state.
    
    This demonstrates state integration:
    - Assigned version
    - Test metadata
    - Metrics collection
    """
    prompt_id: str
    assigned_version: str
    test_id: Optional[str] = None
    metrics: List[RuntimeMetrics] = field(default_factory=list)


class RuntimeABTestManager:
    """
    Manager for runtime A/B testing in agentic loops.
    
    This demonstrates runtime A/B testing patterns:
    - Dynamic version selection
    - Context-aware routing
    - In-loop metrics collection
    - Real-time performance monitoring
    """
    
    def __init__(
        self,
        version_manager: PromptVersionManager,
        ab_test_manager: ABTestManager
    ):
        """
        Initialize runtime A/B test manager.
        
        Args:
            version_manager: Prompt version manager
            ab_test_manager: A/B test manager
        """
        self.version_manager = version_manager
        self.ab_test_manager = ab_test_manager
        self.runtime_metrics: Dict[str, List[RuntimeMetrics]] = {}
        self.active_tests: Dict[str, ABTestConfig] = {}
    
    def select_prompt_version(
        self,
        prompt_id: str,
        context: Optional[Dict[str, Any]] = None,
        state: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Select prompt version at runtime.
        
        Args:
            prompt_id: Prompt identifier
            context: Runtime context (user, task, etc.)
            state: LangGraph state
            
        Returns:
            Selected prompt version
        """
        # Check for active A/B test
        if prompt_id in self.ab_test_manager.active_tests:
            return self._select_version_for_ab_test(
                prompt_id,
                context,
                state
            )
        
        # Context-aware routing
        if context:
            return self._context_aware_routing(prompt_id, context)
        
        # Default to production
        version = self.version_manager.get_version(
            prompt_id,
            tag=VersionTag.PRODUCTION
        )
        return version.version if version else "latest"
    
    def _select_version_for_ab_test(
        self,
        prompt_id: str,
        context: Optional[Dict[str, Any]],
        state: Optional[Dict[str, Any]]
    ) -> str:
        """
        Select version for active A/B test.
        
        Args:
            prompt_id: Prompt identifier
            context: Runtime context
            state: LangGraph state
            
        Returns:
            Selected version
        """
        # Get user ID from context or state
        user_id = None
        if context:
            user_id = context.get("user_id")
        if not user_id and state:
            user_id = state.get("user_id")
        if not user_id:
            user_id = "anonymous"
        
        # Use AB test manager for assignment
        return self.ab_test_manager.assign_version(prompt_id, user_id)
    
    def _context_aware_routing(
        self,
        prompt_id: str,
        context: Dict[str, Any]
    ) -> str:
        """
        Route based on context.
        
        Args:
            prompt_id: Prompt identifier
            context: Runtime context
            
        Returns:
            Selected version
        """
        # Example: Route based on task complexity
        task_complexity = context.get("task_complexity", "medium")
        
        if task_complexity == "simple":
            # Use simpler/faster version
            version = self.version_manager.get_version(
                prompt_id,
                tag=VersionTag.PRODUCTION
            )
            return version.version if version else "latest"
        
        # Default routing
        version = self.version_manager.get_version(
            prompt_id,
            tag=VersionTag.PRODUCTION
        )
        return version.version if version else "latest"
    
    def record_runtime_metrics(
        self,
        prompt_id: str,
        version: str,
        metrics: RuntimeMetrics
    ):
        """
        Record runtime metrics.
        
        Args:
            prompt_id: Prompt identifier
            version: Prompt version
            metrics: Runtime metrics
        """
        key = f"{prompt_id}:{version}"
        if key not in self.runtime_metrics:
            self.runtime_metrics[key] = []
        
        self.runtime_metrics[key].append(metrics)
        
        # Also record in AB test manager if active
        if prompt_id in self.ab_test_manager.active_tests:
            self.ab_test_manager.record_result(
                prompt_id,
                version,
                metrics.success,
                metrics.quality_score
            )
    
    def get_runtime_performance(
        self,
        prompt_id: str,
        version: Optional[str] = None
    ) -> Dict[str, float]:
        """
        Get runtime performance metrics.
        
        Args:
            prompt_id: Prompt identifier
            version: Optional version filter
            
        Returns:
            Performance metrics dictionary
        """
        if version:
            key = f"{prompt_id}:{version}"
            metrics_list = self.runtime_metrics.get(key, [])
        else:
            # Aggregate all versions
            metrics_list = []
            for key, metrics in self.runtime_metrics.items():
                if key.startswith(f"{prompt_id}:"):
                    metrics_list.extend(metrics)
        
        if not metrics_list:
            return {
                "avg_quality": 0.0,
                "avg_latency": 0.0,
                "avg_cost": 0.0,
                "success_rate": 0.0,
                "total_requests": 0
            }
        
        total = len(metrics_list)
        successful = sum(1 for m in metrics_list if m.success)
        
        return {
            "avg_quality": sum(m.quality_score for m in metrics_list) / total,
            "avg_latency": sum(m.latency for m in metrics_list) / total,
            "avg_cost": sum(m.cost for m in metrics_list) / total,
            "success_rate": successful / total,
            "total_requests": total
        }
    
    def adjust_traffic_split(
        self,
        prompt_id: str,
        performance_threshold: float = 0.05
    ) -> bool:
        """
        Adjust traffic split based on performance.
        
        Args:
            prompt_id: Prompt identifier
            performance_threshold: Minimum performance difference for adjustment
            
        Returns:
            True if split was adjusted
        """
        if prompt_id not in self.ab_test_manager.active_tests:
            return False
        
        test_config = self.ab_test_manager.active_tests[prompt_id]
        results = self.ab_test_manager.test_results.get(prompt_id, {})
        
        if "version_a" not in results or "version_b" not in results:
            return False
        
        score_a = results["version_a"].get("quality_score", 0.0)
        score_b = results["version_b"].get("quality_score", 0.0)
        
        # Calculate performance difference
        diff = abs(score_a - score_b)
        if diff < performance_threshold:
            return False  # Not significant enough
        
        # Adjust split: favor better performing version
        if score_a > score_b:
            # Increase traffic to version A
            new_split = min(0.9, test_config.traffic_split + 0.1)
        else:
            # Increase traffic to version B
            new_split = max(0.1, test_config.traffic_split - 0.1)
        
        test_config.traffic_split = new_split
        return True
    
    def create_ab_test_context(
        self,
        prompt_id: str,
        version: str,
        test_id: Optional[str] = None
    ) -> ABTestContext:
        """
        Create A/B test context for LangGraph state.
        
        Args:
            prompt_id: Prompt identifier
            version: Assigned version
            test_id: Optional test identifier
            
        Returns:
            ABTestContext
        """
        return ABTestContext(
            prompt_id=prompt_id,
            assigned_version=version,
            test_id=test_id
        )
    
    def update_state_with_metrics(
        self,
        state: Dict[str, Any],
        context: ABTestContext,
        metrics: RuntimeMetrics
    ):
        """
        Update LangGraph state with metrics.
        
        Args:
            state: LangGraph state
            context: A/B test context
            metrics: Runtime metrics
        """
        # Add metrics to context
        context.metrics.append(metrics)
        
        # Store in state
        if "ab_test_contexts" not in state:
            state["ab_test_contexts"] = {}
        
        state["ab_test_contexts"][context.prompt_id] = {
            "assigned_version": context.assigned_version,
            "test_id": context.test_id,
            "metrics_count": len(context.metrics),
            "latest_quality": metrics.quality_score,
            "latest_latency": metrics.latency
        }
