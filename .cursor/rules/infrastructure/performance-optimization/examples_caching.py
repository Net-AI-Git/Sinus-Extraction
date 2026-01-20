"""
Caching Pattern Example

This file demonstrates the generic cache-aside pattern for Redis and in-memory caching.
Reference this example from RULE.mdc using @examples_caching.py syntax.
"""

from typing import Any, Callable, TypeVar, Optional, List, Dict
from functools import wraps
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import redis
import json

T = TypeVar('T')


# ============================================================================
# Cache-Aside Pattern
# ============================================================================

class CacheService:
    """
    Generic cache service pattern using cache-aside strategy.
    
    This demonstrates the cache-aside pattern:
    1. Check cache for data
    2. If miss, fetch from source
    3. Store in cache for future requests
    4. Return data to caller
    """
    
    def __init__(self, redis_client: redis.Redis, ttl: int = 3600):
        """
        Initialize cache service.
        
        Args:
            redis_client: Redis client instance
            ttl: Time-to-live for cached data in seconds
        """
        self.redis = redis_client
        self.ttl = ttl
    
    def get_or_fetch(
        self,
        key: str,
        fetch_func: Callable[[], T]
    ) -> T:
        """
        Get data from cache or fetch from source.
        
        This demonstrates the cache-aside pattern:
        - Check cache first
        - If cache miss, fetch from source
        - Store in cache for future requests
        
        Args:
            key: Cache key
            fetch_func: Function to fetch data if cache miss
            
        Returns:
            Cached or fetched data
        """
        # Check cache
        cached = self.redis.get(key)
        if cached:
            return json.loads(cached)
        
        # Cache miss - fetch from source
        data = fetch_func()
        
        # Store in cache
        self.redis.setex(
            key,
            self.ttl,
            json.dumps(data)
        )
        
        return data


# ============================================================================
# In-Memory Cache Decorator Pattern
# ============================================================================

def cache_result(max_size: int = 128):
    """
    Generic in-memory cache decorator pattern.
    
    This demonstrates the pattern for function result caching:
    - Cache function results in memory
    - Limit cache size to prevent memory issues
    - Use LRU eviction when cache is full
    
    Args:
        max_size: Maximum number of cached results
    """
    cache: dict = {}
    
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            # Create cache key from function arguments
            cache_key = str((args, tuple(sorted(kwargs.items()))))
            
            # Check cache
            if cache_key in cache:
                return cache[cache_key]
            
            # Cache miss - execute function
            result = func(*args, **kwargs)
            
            # Store in cache (with size limit)
            if len(cache) >= max_size:
                # Remove oldest entry (simple FIFO)
                cache.pop(next(iter(cache)))
            
            cache[cache_key] = result
            return result
        
        return wrapper
    
    return decorator


# ============================================================================
# Semantic Caching with Vector DB
# ============================================================================

@dataclass
class CachedResponse:
    """
    Cached response with metadata.
    
    This demonstrates cached response structure:
    - Query embedding
    - LLM response
    - Metadata (cost, quality, timestamp)
    """
    query: str
    query_embedding: List[float]
    response: str
    cost: float = 0.0
    quality_score: float = 1.0
    timestamp: datetime = field(default_factory=datetime.now)
    hit_count: int = 0


class SemanticCache:
    """
    Semantic cache using Vector DB for similarity-based caching.
    
    This demonstrates semantic caching patterns:
    - Vector-based similarity search
    - Cache hit/miss detection
    - Cost savings tracking
    - Cache invalidation
    """
    
    def __init__(
        self,
        vector_db_client: Any,  # Vector DB client (Pinecone, Weaviate, etc.)
        embedding_model: Any,  # Embedding model
        similarity_threshold: float = 0.85,
        ttl: Optional[int] = None  # Time-to-live in seconds
    ):
        """
        Initialize semantic cache.
        
        Args:
            vector_db_client: Vector database client
            embedding_model: Embedding model for generating embeddings
            similarity_threshold: Minimum similarity for cache hit (0.0-1.0)
            ttl: Optional time-to-live for cache entries
        """
        self.vector_db = vector_db_client
        self.embedding_model = embedding_model
        self.similarity_threshold = similarity_threshold
        self.ttl = ttl
        self.cache_stats: Dict[str, Any] = {
            "hits": 0,
            "misses": 0,
            "total_cost_saved": 0.0,
            "total_queries": 0
        }
    
    async def get_or_compute(
        self,
        query: str,
        compute_func: Callable[[], T],
        cost_per_call: float = 0.01
    ) -> T:
        """
        Get response from cache or compute using LLM.
        
        Args:
            query: Input query
            compute_func: Function to compute response if cache miss
            cost_per_call: Cost per LLM call (for savings calculation)
            
        Returns:
            Cached or computed response
        """
        self.cache_stats["total_queries"] += 1
        
        # Generate embedding for query
        query_embedding = await self._generate_embedding(query)
        
        # Search for similar cached responses
        similar_responses = await self._search_similar(
            query_embedding,
            top_k=1
        )
        
        # Check if we have a cache hit
        if similar_responses:
            best_match = similar_responses[0]
            similarity = best_match.get("similarity", 0.0)
            
            if similarity >= self.similarity_threshold:
                # Cache hit
                cached_response = best_match.get("response")
                if cached_response:
                    self.cache_stats["hits"] += 1
                    self.cache_stats["total_cost_saved"] += cost_per_call
                    cached_response.hit_count += 1
                    return cached_response.response
        
        # Cache miss - compute response
        self.cache_stats["misses"] += 1
        response = await compute_func()
        
        # Store in cache
        await self._store_in_cache(
            query,
            query_embedding,
            response,
            cost_per_call
        )
        
        return response
    
    async def _generate_embedding(
        self,
        text: str
    ) -> List[float]:
        """
        Generate embedding for text.
        
        Args:
            text: Input text
            
        Returns:
            Embedding vector
        """
        # In real implementation:
        # - Use embedding model to generate embedding
        # - Handle errors and retries
        # - Cache embeddings if needed
        
        # Simulated embedding
        return [0.1] * 384  # Example 384-dimensional embedding
    
    async def _search_similar(
        self,
        query_embedding: List[float],
        top_k: int = 1
    ) -> List[Dict[str, Any]]:
        """
        Search for similar cached responses.
        
        Args:
            query_embedding: Query embedding vector
            top_k: Number of results to return
            
        Returns:
            List of similar cached responses with similarity scores
        """
        # In real implementation:
        # - Use vector DB to search for similar embeddings
        # - Filter by similarity threshold
        # - Return top-K results with similarity scores
        
        # Example: vector_db.query(vector=query_embedding, top_k=top_k, filter={"namespace": "cache"})
        
        return []  # Simulated - no matches
    
    async def _store_in_cache(
        self,
        query: str,
        query_embedding: List[float],
        response: str,
        cost: float
    ):
        """
        Store response in cache.
        
        Args:
            query: Original query
            query_embedding: Query embedding
            response: LLM response
            cost: Cost of generating response
        """
        cached_response = CachedResponse(
            query=query,
            query_embedding=query_embedding,
            response=response,
            cost=cost
        )
        
        # In real implementation:
        # - Store embedding in vector DB
        # - Store response and metadata
        # - Set TTL if configured
        # - Handle errors and retries
        
        # Example: vector_db.upsert(
        #     vectors=[(id, query_embedding, {"response": response, "query": query})],
        #     namespace="cache"
        # )
    
    def get_cache_stats(
        self
    ) -> Dict[str, Any]:
        """
        Get cache statistics.
        
        Returns:
            Cache statistics dictionary
        """
        total = self.cache_stats["total_queries"]
        hits = self.cache_stats["hits"]
        misses = self.cache_stats["misses"]
        
        hit_rate = hits / total if total > 0 else 0.0
        
        return {
            "total_queries": total,
            "hits": hits,
            "misses": misses,
            "hit_rate": hit_rate,
            "total_cost_saved": self.cache_stats["total_cost_saved"],
            "average_cost_saved_per_hit": (
                self.cache_stats["total_cost_saved"] / hits
                if hits > 0
                else 0.0
            )
        }
    
    async def invalidate_cache(
        self,
        pattern: Optional[str] = None,
        older_than: Optional[timedelta] = None
    ) -> int:
        """
        Invalidate cache entries.
        
        Args:
            pattern: Optional pattern to match queries
            older_than: Optional time delta to invalidate older entries
            
        Returns:
            Number of entries invalidated
        """
        # In real implementation:
        # - Search for entries matching pattern
        # - Filter by age if older_than specified
        # - Delete matching entries from vector DB
        # - Return count of deleted entries
        
        return 0  # Simulated
    
    def update_similarity_threshold(
        self,
        new_threshold: float
    ):
        """
        Update similarity threshold.
        
        Args:
            new_threshold: New similarity threshold (0.0-1.0)
        """
        if 0.0 <= new_threshold <= 1.0:
            self.similarity_threshold = new_threshold
    
    async def clear_cache(
        self
    ) -> bool:
        """
        Clear all cache entries.
        
        Returns:
            True if successful
        """
        # In real implementation:
        # - Delete all entries from vector DB
        # - Reset cache statistics
        # - Handle errors
        
        self.cache_stats = {
            "hits": 0,
            "misses": 0,
            "total_cost_saved": 0.0,
            "total_queries": 0
        }
        
        return True
