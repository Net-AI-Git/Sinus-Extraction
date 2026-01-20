"""
Bias Detection and Ethics Examples

This file demonstrates bias detection and ethical AI practices.
Reference this example from RULE.mdc using @examples_bias_detection.py syntax.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from collections import defaultdict
import statistics


# ============================================================================
# Bias Types and Detection
# ============================================================================

class BiasType(Enum):
    """
    Types of biases to detect.
    
    This demonstrates bias categories:
    - Demographic bias
    - Cultural bias
    - Confirmation bias
    - Selection bias
    """
    DEMOGRAPHIC = "demographic"
    CULTURAL = "cultural"
    CONFIRMATION = "confirmation"
    SELECTION = "selection"
    TEMPORAL = "temporal"


@dataclass
class BiasDetectionResult:
    """
    Result of bias detection.
    
    This demonstrates bias detection output:
    - Bias type
    - Severity
    - Evidence
    - Recommendations
    """
    bias_type: BiasType
    severity: float  # 0.0-1.0
    evidence: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    detected_at: datetime = field(default_factory=datetime.now)


class BiasDetector:
    """
    Detector for biases in agentic systems.
    
    This demonstrates bias detection patterns:
    - Statistical detection
    - Content analysis
    - Behavioral analysis
    - Automated monitoring
    """
    
    def __init__(self):
        """Initialize bias detector."""
        self.detection_history: List[BiasDetectionResult] = []
        self.metrics: Dict[str, Dict[str, float]] = defaultdict(dict)
    
    def detect_demographic_bias(
        self,
        outcomes: Dict[str, Dict[str, Any]],
        demographic_groups: List[str]
    ) -> List[BiasDetectionResult]:
        """
        Detect demographic bias in outcomes.
        
        Args:
            outcomes: Dictionary of group -> outcome metrics
            demographic_groups: List of demographic groups to analyze
            
        Returns:
            List of bias detection results
        """
        results = []
        
        # Calculate metrics per group
        group_metrics = {}
        for group in demographic_groups:
            if group in outcomes:
                group_metrics[group] = outcomes[group]
        
        if len(group_metrics) < 2:
            return results  # Need at least 2 groups for comparison
        
        # Calculate average outcome across groups
        avg_outcomes = {}
        for group, metrics in group_metrics.items():
            avg_outcomes[group] = statistics.mean(
                metrics.get("scores", [0.0])
            )
        
        overall_avg = statistics.mean(avg_outcomes.values())
        
        # Detect disparities
        for group, avg_score in avg_outcomes.items():
            disparity = abs(avg_score - overall_avg) / overall_avg if overall_avg > 0 else 0.0
            
            if disparity > 0.1:  # 10% threshold
                severity = min(1.0, disparity)
                results.append(
                    BiasDetectionResult(
                        bias_type=BiasType.DEMOGRAPHIC,
                        severity=severity,
                        evidence=[
                            f"Group {group} has {disparity*100:.1f}% disparity",
                            f"Average score: {avg_score:.2f} vs overall: {overall_avg:.2f}"
                        ],
                        recommendations=[
                            f"Review outcomes for group {group}",
                            "Consider bias mitigation strategies"
                        ]
                    )
                )
        
        return results
    
    def detect_language_bias(
        self,
        texts: List[str],
        bias_keywords: Optional[Dict[str, List[str]]] = None
    ) -> List[BiasDetectionResult]:
        """
        Detect language bias in texts.
        
        Args:
            texts: List of texts to analyze
            bias_keywords: Optional dictionary of bias categories -> keywords
            
        Returns:
            List of bias detection results
        """
        results = []
        
        if not bias_keywords:
            bias_keywords = {
                "gender": ["he", "she", "his", "her"],
                "age": ["young", "old", "elderly"],
                "race": ["race", "ethnicity"]
            }
        
        # Count keyword occurrences
        keyword_counts = defaultdict(int)
        for text in texts:
            text_lower = text.lower()
            for category, keywords in bias_keywords.items():
                for keyword in keywords:
                    if keyword in text_lower:
                        keyword_counts[category] += 1
        
        # Detect imbalances
        total_keywords = sum(keyword_counts.values())
        if total_keywords > 0:
            for category, count in keyword_counts.items():
                proportion = count / total_keywords
                
                # Check if proportion is significantly different from expected
                expected_proportion = 1.0 / len(keyword_counts)
                if abs(proportion - expected_proportion) > 0.2:
                    severity = min(1.0, abs(proportion - expected_proportion) * 2)
                    results.append(
                        BiasDetectionResult(
                            bias_type=BiasType.CULTURAL,
                            severity=severity,
                            evidence=[
                                f"Category {category} appears {proportion*100:.1f}% of the time",
                                f"Expected proportion: {expected_proportion*100:.1f}%"
                            ],
                            recommendations=[
                                f"Review language usage for category {category}",
                                "Consider using more inclusive language"
                            ]
                        )
                    )
        
        return results
    
    def detect_selection_bias(
        self,
        selections: Dict[str, int],
        expected_distribution: Optional[Dict[str, float]] = None
    ) -> List[BiasDetectionResult]:
        """
        Detect selection bias in selections.
        
        Args:
            selections: Dictionary of item -> selection count
            expected_distribution: Optional expected distribution
            
        Returns:
            List of bias detection results
        """
        results = []
        
        total_selections = sum(selections.values())
        if total_selections == 0:
            return results
        
        # Calculate actual distribution
        actual_distribution = {
            item: count / total_selections
            for item, count in selections.items()
        }
        
        # Compare with expected distribution
        if expected_distribution:
            for item, expected_prop in expected_distribution.items():
                actual_prop = actual_distribution.get(item, 0.0)
                disparity = abs(actual_prop - expected_prop)
                
                if disparity > 0.15:  # 15% threshold
                    severity = min(1.0, disparity * 2)
                    results.append(
                        BiasDetectionResult(
                            bias_type=BiasType.SELECTION,
                            severity=severity,
                            evidence=[
                                f"Item {item} selected {actual_prop*100:.1f}% vs expected {expected_prop*100:.1f}%",
                                f"Disparity: {disparity*100:.1f}%"
                            ],
                            recommendations=[
                                f"Review selection patterns for item {item}",
                                "Consider adjusting selection algorithm"
                            ]
                        )
                    )
        else:
            # Check for uniform distribution
            expected_prop = 1.0 / len(selections)
            for item, actual_prop in actual_distribution.items():
                disparity = abs(actual_prop - expected_prop)
                
                if disparity > 0.2:  # 20% threshold for uniform
                    severity = min(1.0, disparity * 2)
                    results.append(
                        BiasDetectionResult(
                            bias_type=BiasType.SELECTION,
                            severity=severity,
                            evidence=[
                                f"Item {item} selected {actual_prop*100:.1f}% vs expected {expected_prop*100:.1f}%",
                                f"Disparity: {disparity*100:.1f}%"
                            ],
                            recommendations=[
                                f"Review selection patterns for item {item}",
                                "Consider balancing selection distribution"
                            ]
                        )
                    )
        
        return results
    
    def record_detection(
        self,
        result: BiasDetectionResult
    ):
        """
        Record bias detection result.
        
        Args:
            result: Bias detection result
        """
        self.detection_history.append(result)
    
    def get_detection_summary(
        self
    ) -> Dict[str, Any]:
        """
        Get summary of bias detections.
        
        Returns:
            Summary dictionary
        """
        if not self.detection_history:
            return {
                "total_detections": 0,
                "by_type": {},
                "average_severity": 0.0
            }
        
        by_type = defaultdict(list)
        for result in self.detection_history:
            by_type[result.bias_type.value].append(result.severity)
        
        return {
            "total_detections": len(self.detection_history),
            "by_type": {
                bias_type: {
                    "count": len(severities),
                    "avg_severity": statistics.mean(severities),
                    "max_severity": max(severities)
                }
                for bias_type, severities in by_type.items()
            },
            "average_severity": statistics.mean(
                [r.severity for r in self.detection_history]
            )
        }


# ============================================================================
# Fairness Metrics
# ============================================================================

@dataclass
class GroupMetrics:
    """
    Metrics for a demographic group.
    
    This demonstrates group metrics:
    - True positives
    - False positives
    - True negatives
    - False negatives
    """
    group_name: str
    true_positives: int = 0
    false_positives: int = 0
    true_negatives: int = 0
    false_negatives: int = 0
    
    @property
    def total(self) -> int:
        """Total number of cases."""
        return (
            self.true_positives +
            self.false_positives +
            self.true_negatives +
            self.false_negatives
        )
    
    @property
    def true_positive_rate(self) -> float:
        """True positive rate (recall)."""
        total_positives = self.true_positives + self.false_negatives
        if total_positives == 0:
            return 0.0
        return self.true_positives / total_positives
    
    @property
    def false_positive_rate(self) -> float:
        """False positive rate."""
        total_negatives = self.true_negatives + self.false_positives
        if total_negatives == 0:
            return 0.0
        return self.false_positives / total_negatives
    
    @property
    def positive_rate(self) -> float:
        """Positive prediction rate."""
        if self.total == 0:
            return 0.0
        return (self.true_positives + self.false_positives) / self.total


class FairnessMetrics:
    """
    Calculator for fairness metrics.
    
    This demonstrates fairness calculation:
    - Demographic parity
    - Equalized odds
    - Calibration
    - Individual fairness
    """
    
    def __init__(self):
        """Initialize fairness metrics calculator."""
        self.group_metrics: Dict[str, GroupMetrics] = {}
    
    def add_group_metrics(
        self,
        group_name: str,
        metrics: GroupMetrics
    ):
        """
        Add metrics for a group.
        
        Args:
            group_name: Group name
            metrics: Group metrics
        """
        self.group_metrics[group_name] = metrics
    
    def calculate_demographic_parity(
        self,
        threshold: float = 0.1
    ) -> Dict[str, Any]:
        """
        Calculate demographic parity.
        
        Args:
            threshold: Maximum allowed difference in positive rates
            
        Returns:
            Demographic parity metrics
        """
        if len(self.group_metrics) < 2:
            return {
                "fair": True,
                "message": "Need at least 2 groups for demographic parity"
            }
        
        positive_rates = {
            group: metrics.positive_rate
            for group, metrics in self.group_metrics.items()
        }
        
        rates = list(positive_rates.values())
        max_rate = max(rates)
        min_rate = min(rates)
        difference = max_rate - min_rate
        
        is_fair = difference <= threshold
        
        return {
            "fair": is_fair,
            "difference": difference,
            "threshold": threshold,
            "positive_rates": positive_rates,
            "max_rate": max_rate,
            "min_rate": min_rate,
            "violations": [
                group for group, rate in positive_rates.items()
                if abs(rate - statistics.mean(rates)) > threshold
            ]
        }
    
    def calculate_equalized_odds(
        self,
        threshold: float = 0.1
    ) -> Dict[str, Any]:
        """
        Calculate equalized odds.
        
        Args:
            threshold: Maximum allowed difference in rates
            
        Returns:
            Equalized odds metrics
        """
        if len(self.group_metrics) < 2:
            return {
                "fair": True,
                "message": "Need at least 2 groups for equalized odds"
            }
        
        tprs = {
            group: metrics.true_positive_rate
            for group, metrics in self.group_metrics.items()
        }
        
        fprs = {
            group: metrics.false_positive_rate
            for group, metrics in self.group_metrics.items()
        }
        
        tpr_values = list(tprs.values())
        fpr_values = list(fprs.values())
        
        tpr_diff = max(tpr_values) - min(tpr_values)
        fpr_diff = max(fpr_values) - min(fpr_values)
        
        is_fair = tpr_diff <= threshold and fpr_diff <= threshold
        
        return {
            "fair": is_fair,
            "tpr_difference": tpr_diff,
            "fpr_difference": fpr_diff,
            "threshold": threshold,
            "true_positive_rates": tprs,
            "false_positive_rates": fprs,
            "violations": [
                group for group in self.group_metrics.keys()
                if abs(tprs[group] - statistics.mean(tpr_values)) > threshold or
                   abs(fprs[group] - statistics.mean(fpr_values)) > threshold
            ]
        }
    
    def calculate_calibration(
        self,
        threshold: float = 0.1
    ) -> Dict[str, Any]:
        """
        Calculate calibration across groups.
        
        Args:
            threshold: Maximum allowed difference in calibration
            
        Returns:
            Calibration metrics
        """
        # Simplified calibration calculation
        # In real implementation, would use predicted probabilities
        
        if len(self.group_metrics) < 2:
            return {
                "fair": True,
                "message": "Need at least 2 groups for calibration"
            }
        
        # Use positive rate as proxy for calibration
        positive_rates = {
            group: metrics.positive_rate
            for group, metrics in self.group_metrics.items()
        }
        
        rates = list(positive_rates.values())
        max_rate = max(rates)
        min_rate = min(rates)
        difference = max_rate - min_rate
        
        is_fair = difference <= threshold
        
        return {
            "fair": is_fair,
            "difference": difference,
            "threshold": threshold,
            "positive_rates": positive_rates,
            "violations": [
                group for group, rate in positive_rates.items()
                if abs(rate - statistics.mean(rates)) > threshold
            ]
        }
    
    def get_fairness_report(
        self
    ) -> Dict[str, Any]:
        """
        Get comprehensive fairness report.
        
        Returns:
            Fairness report dictionary
        """
        return {
            "demographic_parity": self.calculate_demographic_parity(),
            "equalized_odds": self.calculate_equalized_odds(),
            "calibration": self.calculate_calibration(),
            "groups": list(self.group_metrics.keys()),
            "total_groups": len(self.group_metrics)
        }


# ============================================================================
# Bias Mitigation
# ============================================================================

class BiasMitigation:
    """
    Strategies for bias mitigation.
    
    This demonstrates bias mitigation patterns:
    - Pre-processing mitigation
    - In-processing mitigation
    - Post-processing mitigation
    """
    
    @staticmethod
    def filter_biased_content(
        content: str,
        bias_keywords: Optional[List[str]] = None
    ) -> str:
        """
        Filter biased content from text.
        
        Args:
            content: Text content
            bias_keywords: Optional list of bias keywords to filter
            
        Returns:
            Filtered content
        """
        if not bias_keywords:
            return content
        
        # Simple filtering - in real implementation would be more sophisticated
        filtered = content
        for keyword in bias_keywords:
            filtered = filtered.replace(keyword, "[filtered]")
        
        return filtered
    
    @staticmethod
    def promote_diversity(
        items: List[str],
        diversity_factor: float = 0.5
    ) -> List[str]:
        """
        Promote diversity in list.
        
        Args:
            items: List of items
            diversity_factor: Factor for diversity promotion (0.0-1.0)
            
        Returns:
            Diversified list
        """
        if not items:
            return items
        
        # Simple diversity promotion - in real implementation would be more sophisticated
        # Shuffle and take diverse subset
        import random
        shuffled = items.copy()
        random.shuffle(shuffled)
        
        # Take diverse subset
        diverse_count = max(1, int(len(items) * diversity_factor))
        return shuffled[:diverse_count]
    
    @staticmethod
    def balance_distribution(
        distribution: Dict[str, float],
        target_balance: float = 0.5
    ) -> Dict[str, float]:
        """
        Balance distribution across items.
        
        Args:
            distribution: Current distribution
            target_balance: Target balance factor
            
        Returns:
            Balanced distribution
        """
        if not distribution:
            return distribution
        
        total = sum(distribution.values())
        if total == 0:
            return distribution
        
        # Calculate target per item
        num_items = len(distribution)
        target_per_item = total / num_items
        
        # Adjust distribution towards balance
        balanced = {}
        for item, value in distribution.items():
            current_proportion = value / total
            target_proportion = 1.0 / num_items
            
            # Interpolate between current and target
            new_proportion = (
                current_proportion * (1 - target_balance) +
                target_proportion * target_balance
            )
            balanced[item] = new_proportion * total
        
        return balanced
