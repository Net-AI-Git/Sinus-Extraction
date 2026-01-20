"""
Multi-Agent Rate Limiting Examples

This file demonstrates rate limiting for parallel agents.
Reference this example from RULE.mdc using @examples_multi_agent_rate_limiting.py syntax.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import time
import redis


# ============================================================================
# Rate Limiter Types
# ============================================================================

class RateLimitAlgorithm(Enum):
    """
    Rate limiting algorithms.
    
    This demonstrates rate limit algorithms:
    - Token bucket for burst handling
    - Sliding window for smooth limiting
    - Fixed window for simple limiting
    """
    TOKEN_BUCKET = "token_bucket"
    SLIDING_WINDOW = "sliding_window"
    FIXED_WINDOW = "fixed_window"


@dataclass
class RateLimitConfig:
    """
    Rate limit configuration.
    
    This demonstrates rate limit config:
    - Requests per time window
    - Window duration
    - Burst allowance
    """
    requests_per_window: int
    window_seconds: int
    burst_allowance: int = 0
    algorithm: RateLimitAlgorithm = RateLimitAlgorithm.TOKEN_BUCKET


# ============================================================================
# Per-Agent Rate Limiter
# ============================================================================

class PerAgentRateLimiter:
    """
    Rate limiter for individual agents.
    
    This demonstrates per-agent rate limiting:
    - Individual limit tracking
    - Independent rate limiting
    - Coordination with global limiter
    """
    
    def __init__(
        self,
        agent_id: str,
        config: RateLimitConfig,
        redis_client: Optional[Any] = None
    ):
        """
        Initialize per-agent rate limiter.
        
        Args:
            agent_id: Agent identifier
            config: Rate limit configuration
            redis_client: Optional Redis client for distributed limiting
        """
        self.agent_id = agent_id
        self.config = config
        self.redis = redis_client
        self.key_prefix = f"rate_limit:agent:{agent_id}"
        
        # Local state (if not using Redis)
        self.tokens = config.requests_per_window
        self.last_refill = datetime.now()
    
    def can_proceed(self) -> bool:
        """
        Check if agent can make a request.
        
        Returns:
            True if request allowed
        """
        if self.redis:
            return self._can_proceed_redis()
        else:
            return self._can_proceed_local()
    
    def _can_proceed_local(self) -> bool:
        """Check using local state."""
        # Refill tokens based on time elapsed
        now = datetime.now()
        elapsed = (now - self.last_refill).total_seconds()
        
        if elapsed >= self.config.window_seconds:
            # Refill to full capacity
            self.tokens = self.config.requests_per_window
            self.last_refill = now
        else:
            # Refill proportional to time elapsed
            refill_rate = self.config.requests_per_window / self.config.window_seconds
            tokens_to_add = int(elapsed * refill_rate)
            self.tokens = min(
                self.config.requests_per_window,
                self.tokens + tokens_to_add
            )
            self.last_refill = now
        
        # Check if tokens available
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        
        return False
    
    def _can_proceed_redis(self) -> bool:
        """Check using Redis (token bucket)."""
        now = time.time()
        key = f"{self.key_prefix}:tokens"
        last_refill_key = f"{self.key_prefix}:last_refill"
        
        # Get current state
        pipe = self.redis.pipeline()
        pipe.get(key)
        pipe.get(last_refill_key)
        results = pipe.execute()
        
        tokens = float(results[0] or self.config.requests_per_window)
        last_refill = float(results[1] or now)
        
        # Refill tokens
        elapsed = now - last_refill
        refill_rate = self.config.requests_per_window / self.config.window_seconds
        tokens = min(
            self.config.requests_per_window,
            tokens + (elapsed * refill_rate)
        )
        
        # Check and consume token
        if tokens >= 1:
            tokens -= 1
            pipe = self.redis.pipeline()
            pipe.set(key, tokens)
            pipe.set(last_refill_key, now)
            pipe.execute()
            return True
        
        # Update state even if can't proceed
        pipe = self.redis.pipeline()
        pipe.set(key, tokens)
        pipe.set(last_refill_key, now)
        pipe.execute()
        
        return False
    
    def get_wait_time(self) -> float:
        """
        Get time to wait before next request.
        
        Returns:
            Wait time in seconds
        """
        if self.redis:
            key = f"{self.key_prefix}:tokens"
            tokens = float(self.redis.get(key) or 0)
        else:
            tokens = self.tokens
        
        if tokens >= 1:
            return 0.0
        
        # Calculate wait time based on refill rate
        tokens_needed = 1 - tokens
        refill_rate = self.config.requests_per_window / self.config.window_seconds
        wait_time = tokens_needed / refill_rate
        
        return min(wait_time, self.config.window_seconds)


# ============================================================================
# Global Rate Limiter
# ============================================================================

class GlobalRateLimiter:
    """
    Global rate limiter for coordinating multiple agents.
    
    This demonstrates global rate limiting:
    - Shared rate limit pool
    - Coordination between agents
    - Distributed rate limiting
    """
    
    def __init__(
        self,
        config: RateLimitConfig,
        redis_client: Any
    ):
        """
        Initialize global rate limiter.
        
        Args:
            config: Rate limit configuration
            redis_client: Redis client (required for global limiting)
        """
        self.config = config
        self.redis = redis_client
        self.global_key = "rate_limit:global:tokens"
        self.global_last_refill_key = "rate_limit:global:last_refill"
    
    def can_proceed(self, agent_id: str) -> bool:
        """
        Check if agent can proceed with global limit.
        
        Args:
            agent_id: Agent identifier
        
        Returns:
            True if request allowed
        """
        now = time.time()
        
        # Get current global state
        pipe = self.redis.pipeline()
        pipe.get(self.global_key)
        pipe.get(self.global_last_refill_key)
        results = pipe.execute()
        
        tokens = float(results[0] or self.config.requests_per_window)
        last_refill = float(results[1] or now)
        
        # Refill tokens
        elapsed = now - last_refill
        refill_rate = self.config.requests_per_window / self.config.window_seconds
        tokens = min(
            self.config.requests_per_window,
            tokens + (elapsed * refill_rate)
        )
        
        # Check and consume token atomically
        if tokens >= 1:
            tokens -= 1
            pipe = self.redis.pipeline()
            pipe.set(self.global_key, tokens)
            pipe.set(self.global_last_refill_key, now)
            pipe.execute()
            return True
        
        # Update state
        pipe = self.redis.pipeline()
        pipe.set(self.global_key, tokens)
        pipe.set(self.global_last_refill_key, now)
        pipe.execute()
        
        return False
    
    def get_remaining_tokens(self) -> float:
        """
        Get remaining tokens in global pool.
        
        Returns:
            Number of remaining tokens
        """
        tokens = self.redis.get(self.global_key)
        return float(tokens or 0)


# ============================================================================
# Coordinated Rate Limiting
# ============================================================================

class CoordinatedRateLimiter:
    """
    Coordinated rate limiter combining per-agent and global limits.
    
    This demonstrates coordinated rate limiting:
    - Check both per-agent and global limits
    - Coordinate between agents
    - Handle conflicts gracefully
    """
    
    def __init__(
        self,
        agent_id: str,
        per_agent_config: RateLimitConfig,
        global_config: RateLimitConfig,
        redis_client: Any
    ):
        """
        Initialize coordinated rate limiter.
        
        Args:
            agent_id: Agent identifier
            per_agent_config: Per-agent rate limit config
            global_config: Global rate limit config
            redis_client: Redis client
        """
        self.agent_id = agent_id
        self.per_agent_limiter = PerAgentRateLimiter(
            agent_id=agent_id,
            config=per_agent_config,
            redis_client=redis_client
        )
        self.global_limiter = GlobalRateLimiter(
            config=global_config,
            redis_client=redis_client
        )
    
    def can_proceed(self) -> bool:
        """
        Check if agent can proceed (both limits).
        
        Returns:
            True if both limits allow
        """
        # Check per-agent limit
        if not self.per_agent_limiter.can_proceed():
            return False
        
        # Check global limit
        if not self.global_limiter.can_proceed(self.agent_id):
            return False
        
        return True
    
    def get_wait_time(self) -> float:
        """
        Get maximum wait time from both limiters.
        
        Returns:
            Maximum wait time in seconds
        """
        per_agent_wait = self.per_agent_limiter.get_wait_time()
        
        # For global, estimate based on remaining tokens
        remaining = self.global_limiter.get_remaining_tokens()
        if remaining >= 1:
            global_wait = 0.0
        else:
            refill_rate = self.global_limiter.config.requests_per_window / self.global_limiter.config.window_seconds
            global_wait = (1 - remaining) / refill_rate
        
        return max(per_agent_wait, global_wait)
