"""
API Key Protection Examples

This file demonstrates API key management and protection patterns.
Reference this example from RULE.mdc using @examples_api_key_protection.py syntax.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta
import hashlib


# ============================================================================
# API Key Management
# ============================================================================

@dataclass
class APIKey:
    """
    API key structure.
    
    This demonstrates API key structure:
    - Key identifier and value
    - Usage tracking
    - Health status
    - Rate limit information
    """
    key_id: str
    key_value: str  # In real implementation, store encrypted
    provider: str  # e.g., "openai", "anthropic"
    rate_limit: int  # Requests per minute
    current_usage: int = 0
    last_reset: datetime = None
    health_status: str = "healthy"  # healthy, degraded, exhausted
    created_at: datetime = None
    last_used: datetime = None


class KeyHealthStatus(Enum):
    """
    API key health status.
    
    This demonstrates key health states:
    - Healthy: Normal operation
    - Degraded: High error rate or approaching limits
    - Exhausted: Rate limit exceeded
    - Failed: Authentication or other errors
    """
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    EXHAUSTED = "exhausted"
    FAILED = "failed"


class APIKeyPool:
    """
    Pool of API keys for load distribution.
    
    This demonstrates key pool management:
    - Multiple keys per provider
    - Load balancing
    - Health monitoring
    - Key rotation
    """
    
    def __init__(self):
        """Initialize key pool."""
        self.keys: Dict[str, List[APIKey]] = {}  # provider -> keys
        self.key_usage: Dict[str, int] = {}  # key_id -> usage count
    
    def add_key(
        self,
        key_id: str,
        key_value: str,
        provider: str,
        rate_limit: int
    ) -> APIKey:
        """
        Add API key to pool.
        
        Args:
            key_id: Key identifier
            key_value: Key value
            provider: Provider name
            rate_limit: Rate limit per minute
        
        Returns:
            APIKey instance
        """
        api_key = APIKey(
            key_id=key_id,
            key_value=key_value,
            provider=provider,
            rate_limit=rate_limit,
            last_reset=datetime.now(),
            created_at=datetime.now()
        )
        
        if provider not in self.keys:
            self.keys[provider] = []
        
        self.keys[provider].append(api_key)
        self.key_usage[key_id] = 0
        
        return api_key
    
    def get_key(
        self,
        provider: str,
        exclude_exhausted: bool = True
    ) -> Optional[APIKey]:
        """
        Get available key from pool.
        
        Args:
            provider: Provider name
            exclude_exhausted: Exclude exhausted keys
        
        Returns:
            APIKey or None
        """
        if provider not in self.keys:
            return None
        
        available_keys = self.keys[provider]
        
        if exclude_exhausted:
            available_keys = [
                k for k in available_keys
                if k.health_status != KeyHealthStatus.EXHAUSTED.value
                and k.health_status != KeyHealthStatus.FAILED.value
            ]
        
        if not available_keys:
            return None
        
        # Select key with lowest usage (load balancing)
        selected = min(available_keys, key=lambda k: self.key_usage.get(k.key_id, 0))
        
        return selected
    
    def record_usage(
        self,
        key_id: str,
        success: bool = True
    ):
        """
        Record key usage.
        
        Args:
            key_id: Key identifier
            success: Whether request was successful
        """
        self.key_usage[key_id] = self.key_usage.get(key_id, 0) + 1
        
        # Update key last_used
        for provider_keys in self.keys.values():
            for key in provider_keys:
                if key.key_id == key_id:
                    key.last_used = datetime.now()
                    if not success:
                        self._update_key_health(key, success)
                    break
    
    def _update_key_health(self, key: APIKey, success: bool):
        """
        Update key health status.
        
        Args:
            key: API key
            success: Whether request was successful
        """
        # Check usage vs limit
        usage_ratio = self.key_usage.get(key.key_id, 0) / key.rate_limit if key.rate_limit > 0 else 0
        
        if usage_ratio >= 1.0:
            key.health_status = KeyHealthStatus.EXHAUSTED.value
        elif usage_ratio >= 0.8:
            key.health_status = KeyHealthStatus.DEGRADED.value
        elif not success:
            key.health_status = KeyHealthStatus.FAILED.value
        else:
            key.health_status = KeyHealthStatus.HEALTHY.value
    
    def reset_key_usage(self, key_id: str):
        """
        Reset key usage (e.g., after time window).
        
        Args:
            key_id: Key identifier
        """
        self.key_usage[key_id] = 0
        
        # Update key status
        for provider_keys in self.keys.values():
            for key in provider_keys:
                if key.key_id == key_id:
                    key.last_reset = datetime.now()
                    key.health_status = KeyHealthStatus.HEALTHY.value
                    break


# ============================================================================
# Key Rotation
# ============================================================================

class APIKeyRotator:
    """
    Service for rotating API keys.
    
    This demonstrates key rotation patterns:
    - Rotation triggers
    - Gradual migration
    - Zero-downtime rotation
    """
    
    def __init__(self, key_pool: APIKeyPool):
        """
        Initialize key rotator.
        
        Args:
            key_pool: API key pool
        """
        self.key_pool = key_pool
        self.rotation_threshold = 0.8  # Rotate at 80% usage
    
    def should_rotate(self, key: APIKey) -> bool:
        """
        Check if key should be rotated.
        
        Args:
            key: API key to check
        
        Returns:
            True if rotation needed
        """
        usage = self.key_pool.key_usage.get(key.key_id, 0)
        usage_ratio = usage / key.rate_limit if key.rate_limit > 0 else 0
        
        # Rotate if approaching limit
        if usage_ratio >= self.rotation_threshold:
            return True
        
        # Rotate if key is unhealthy
        if key.health_status in [KeyHealthStatus.EXHAUSTED.value, KeyHealthStatus.FAILED.value]:
            return True
        
        return False
    
    def rotate_key(
        self,
        provider: str,
        new_key_value: str,
        new_key_id: Optional[str] = None
    ) -> APIKey:
        """
        Rotate to new key.
        
        Args:
            provider: Provider name
            new_key_value: New key value
            new_key_id: Optional new key ID
        
        Returns:
            New APIKey
        """
        # Get existing key to copy config
        old_key = self.key_pool.get_key(provider, exclude_exhausted=False)
        
        # Create new key
        new_key_id = new_key_id or f"{provider}_key_{datetime.now().timestamp()}"
        new_key = self.key_pool.add_key(
            key_id=new_key_id,
            key_value=new_key_value,
            provider=provider,
            rate_limit=old_key.rate_limit if old_key else 1000
        )
        
        # Mark old key as deprecated (don't remove immediately)
        if old_key:
            old_key.health_status = "deprecated"
        
        return new_key
    
    def gradual_migration(
        self,
        provider: str,
        new_key: APIKey,
        old_key: APIKey,
        migration_percentage: float = 0.1
    ):
        """
        Gradually migrate traffic from old to new key.
        
        Args:
            provider: Provider name
            new_key: New API key
            old_key: Old API key
            migration_percentage: Percentage of traffic to migrate (0.0-1.0)
        """
        # In real implementation:
        # 1. Start with small percentage to new key
        # 2. Monitor both keys
        # 3. Gradually increase percentage
        # 4. Complete migration when old key usage drops to zero
        
        # For example, use hash-based routing:
        # hash(request_id) % 100 < migration_percentage * 100 -> use new_key
        pass


# ============================================================================
# Key Protection Service
# ============================================================================

class APIKeyProtectionService:
    """
    Service for protecting API keys from exhaustion.
    
    This demonstrates key protection patterns:
    - Usage tracking
    - Exhaustion prevention
    - Automatic rotation
    - Health monitoring
    """
    
    def __init__(self, key_pool: APIKeyPool):
        """
        Initialize protection service.
        
        Args:
            key_pool: API key pool
        """
        self.key_pool = key_pool
        self.rotator = APIKeyRotator(key_pool)
    
    def get_protected_key(
        self,
        provider: str
    ) -> Optional[APIKey]:
        """
        Get key with protection against exhaustion.
        
        Args:
            provider: Provider name
        
        Returns:
            APIKey or None
        """
        # Get available key
        key = self.key_pool.get_key(provider, exclude_exhausted=True)
        
        if not key:
            return None
        
        # Check if rotation needed
        if self.rotator.should_rotate(key):
            # Trigger rotation (in real implementation, this would be async)
            # For now, just return the key with warning
            pass
        
        return key
    
    def record_request(
        self,
        key_id: str,
        success: bool = True
    ):
        """
        Record request and update key health.
        
        Args:
            key_id: Key identifier
            success: Whether request was successful
        """
        self.key_pool.record_usage(key_id, success)
        
        # Check if key needs rotation
        key = self._find_key(key_id)
        if key and self.rotator.should_rotate(key):
            # In real implementation, trigger rotation
            pass
    
    def _find_key(self, key_id: str) -> Optional[APIKey]:
        """Find key by ID."""
        for provider_keys in self.key_pool.keys.values():
            for key in provider_keys:
                if key.key_id == key_id:
                    return key
        return None
    
    def get_key_health_report(self) -> Dict[str, Any]:
        """
        Get health report for all keys.
        
        Returns:
            Health report dictionary
        """
        report = {
            "providers": {},
            "total_keys": 0,
            "healthy_keys": 0,
            "degraded_keys": 0,
            "exhausted_keys": 0
        }
        
        for provider, keys in self.key_pool.keys.items():
            provider_report = {
                "total": len(keys),
                "healthy": 0,
                "degraded": 0,
                "exhausted": 0,
                "failed": 0
            }
            
            for key in keys:
                report["total_keys"] += 1
                
                if key.health_status == KeyHealthStatus.HEALTHY.value:
                    provider_report["healthy"] += 1
                    report["healthy_keys"] += 1
                elif key.health_status == KeyHealthStatus.DEGRADED.value:
                    provider_report["degraded"] += 1
                    report["degraded_keys"] += 1
                elif key.health_status == KeyHealthStatus.EXHAUSTED.value:
                    provider_report["exhausted"] += 1
                    report["exhausted_keys"] += 1
                else:
                    provider_report["failed"] += 1
            
            report["providers"][provider] = provider_report
        
        return report
