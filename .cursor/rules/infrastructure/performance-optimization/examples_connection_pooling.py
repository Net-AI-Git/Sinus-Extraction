"""
Connection Pooling Pattern Example

This file demonstrates the generic connection pool configuration and usage pattern.
Reference this example from RULE.mdc using @examples_connection_pooling.py syntax.
"""

from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
from typing import Any


# ============================================================================
# SQLAlchemy Connection Pool Pattern
# ============================================================================

def create_pooled_engine(
    database_url: str,
    pool_size: int = 5,
    max_overflow: int = 10,
    pool_timeout: int = 30,
    pool_recycle: int = 3600
) -> Any:
    """
    Create SQLAlchemy engine with connection pool configuration.
    
    This demonstrates the pattern for connection pooling:
    - pool_size: Number of connections to maintain
    - max_overflow: Additional connections beyond pool_size
    - pool_timeout: Timeout for acquiring connection
    - pool_recycle: Time to refresh stale connections
    
    Args:
        database_url: Database connection URL
        pool_size: Base pool size
        max_overflow: Maximum overflow connections
        pool_timeout: Connection acquisition timeout
        pool_recycle: Connection recycle time in seconds
        
    Returns:
        Configured SQLAlchemy engine
    """
    engine = create_engine(
        database_url,
        poolclass=QueuePool,
        pool_size=pool_size,
        max_overflow=max_overflow,
        pool_timeout=pool_timeout,
        pool_recycle=pool_recycle,
        echo=False
    )
    
    return engine


# ============================================================================
# Async Connection Pool Pattern
# ============================================================================

class AsyncConnectionPool:
    """
    Generic async connection pool pattern.
    
    This demonstrates the pattern for async connection pooling:
    - Maintain pool of connections
    - Reuse connections across requests
    - Handle connection acquisition and release
    """
    
    def __init__(
        self,
        min_size: int = 5,
        max_size: int = 20,
        max_queries: int = 50000
    ):
        """
        Initialize async connection pool.
        
        Args:
            min_size: Minimum pool size
            max_size: Maximum pool size
            max_queries: Maximum queries per connection before recycling
        """
        self.min_size = min_size
        self.max_size = max_size
        self.max_queries = max_queries
        self.pool: Any = None
    
    async def acquire(self) -> Any:
        """
        Acquire connection from pool.
        
        Returns:
            Database connection from pool
        """
        if not self.pool:
            raise RuntimeError("Pool not initialized")
        
        return await self.pool.acquire()
    
    async def release(self, connection: Any) -> None:
        """
        Release connection back to pool.
        
        Args:
            connection: Connection to release
        """
        if self.pool:
            await self.pool.release(connection)
