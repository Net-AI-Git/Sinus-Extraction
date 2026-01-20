"""
Queue Management Examples

This file demonstrates queue patterns for agents.
Reference this example from RULE.mdc using @examples_queue_management.py syntax.
"""

from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import asyncio
import time


# ============================================================================
# Queue Types
# ============================================================================

class QueueType(Enum):
    """
    Queue types for request management.
    
    This demonstrates queue types:
    - FIFO for fair processing
    - Priority for urgent requests
    - Weighted for different request types
    """
    FIFO = "fifo"
    PRIORITY = "priority"
    WEIGHTED = "weighted"


class RequestPriority(Enum):
    """
    Request priority levels.
    
    This demonstrates priority classification:
    - High for critical requests
    - Medium for standard operations
    - Low for background tasks
    """
    HIGH = 3
    MEDIUM = 2
    LOW = 1


@dataclass
class QueuedRequest:
    """
    Queued request structure.
    
    This demonstrates queued request:
    - Request data and metadata
    - Priority and timestamp
    - Callback for processing
    """
    request_id: str
    agent_id: str
    request_data: Dict[str, Any]
    priority: RequestPriority
    callback: Callable
    created_at: datetime
    retry_count: int = 0
    max_retries: int = 3


# ============================================================================
# Queue Implementation
# ============================================================================

class AgentRequestQueue:
    """
    Queue for managing agent requests.
    
    This demonstrates queue management patterns:
    - Request queuing
    - Priority-based processing
    - Rate limit awareness
    - Retry handling
    """
    
    def __init__(
        self,
        queue_type: QueueType = QueueType.PRIORITY,
        max_size: int = 1000
    ):
        """
        Initialize request queue.
        
        Args:
            queue_type: Type of queue
            max_size: Maximum queue size
        """
        self.queue_type = queue_type
        self.max_size = max_size
        self.queue: List[QueuedRequest] = []
        self.processing = False
        self.processed_count = 0
        self.failed_count = 0
    
    def enqueue(
        self,
        request_id: str,
        agent_id: str,
        request_data: Dict[str, Any],
        callback: Callable,
        priority: RequestPriority = RequestPriority.MEDIUM
    ) -> bool:
        """
        Enqueue a request.
        
        Args:
            request_id: Request identifier
            agent_id: Agent identifier
            request_data: Request data
            callback: Callback function to process request
            priority: Request priority
        
        Returns:
            True if enqueued successfully
        """
        # Check queue size
        if len(self.queue) >= self.max_size:
            return False
        
        # Create queued request
        queued_request = QueuedRequest(
            request_id=request_id,
            agent_id=agent_id,
            request_data=request_data,
            priority=priority,
            callback=callback,
            created_at=datetime.now()
        )
        
        # Add to queue based on type
        if self.queue_type == QueueType.FIFO:
            self.queue.append(queued_request)
        elif self.queue_type == QueueType.PRIORITY:
            # Insert based on priority (higher priority first)
            inserted = False
            for i, req in enumerate(self.queue):
                if queued_request.priority.value > req.priority.value:
                    self.queue.insert(i, queued_request)
                    inserted = True
                    break
            if not inserted:
                self.queue.append(queued_request)
        else:  # WEIGHTED
            # Similar to priority but with weights
            self.queue.append(queued_request)
            self.queue.sort(key=lambda r: r.priority.value, reverse=True)
        
        return True
    
    def dequeue(self) -> Optional[QueuedRequest]:
        """
        Dequeue next request.
        
        Returns:
            QueuedRequest or None if queue empty
        """
        if not self.queue:
            return None
        
        return self.queue.pop(0)
    
    def process_queue(
        self,
        rate_limiter: Any,
        max_concurrent: int = 5
    ):
        """
        Process queue respecting rate limits.
        
        Args:
            rate_limiter: Rate limiter instance
            max_concurrent: Maximum concurrent requests
        """
        self.processing = True
        
        while self.queue and self.processing:
            # Check rate limit
            if not rate_limiter.can_proceed():
                # Wait for rate limit
                time.sleep(rate_limiter.get_wait_time())
                continue
            
            # Dequeue request
            request = self.dequeue()
            if not request:
                break
            
            # Process request
            try:
                result = request.callback(request.request_data)
                self.processed_count += 1
            except Exception as e:
                # Handle failure
                self.failed_count += 1
                if request.retry_count < request.max_retries:
                    request.retry_count += 1
                    self.enqueue(
                        request.request_id,
                        request.agent_id,
                        request.request_data,
                        request.callback,
                        request.priority
                    )
        
        self.processing = False


# ============================================================================
# Redis Queue Implementation
# ============================================================================

class RedisAgentQueue:
    """
    Redis-based queue for distributed systems.
    
    This demonstrates Redis queue patterns:
    - Distributed queue across instances
    - Atomic operations
    - Persistence and reliability
    """
    
    def __init__(self, redis_client: Any, queue_name: str = "agent_requests"):
        """
        Initialize Redis queue.
        
        Args:
            redis_client: Redis client
            queue_name: Queue name/key
        """
        self.redis = redis_client
        self.queue_name = queue_name
        self.priority_queue_name = f"{queue_name}:priority"
    
    def enqueue(
        self,
        request_id: str,
        agent_id: str,
        request_data: Dict[str, Any],
        priority: RequestPriority = RequestPriority.MEDIUM
    ) -> bool:
        """
        Enqueue request in Redis.
        
        Args:
            request_id: Request identifier
            agent_id: Agent identifier
            request_data: Request data
            priority: Request priority
        
        Returns:
            True if enqueued successfully
        """
        import json
        
        request_payload = {
            "request_id": request_id,
            "agent_id": agent_id,
            "request_data": request_data,
            "priority": priority.value,
            "created_at": datetime.now().isoformat()
        }
        
        # Use sorted set for priority queue
        score = priority.value * 1000000 + int(time.time() * 1000)  # Priority + timestamp
        self.redis.zadd(
            self.priority_queue_name,
            {json.dumps(request_payload): score}
        )
        
        return True
    
    def dequeue(self) -> Optional[Dict[str, Any]]:
        """
        Dequeue highest priority request.
        
        Returns:
            Request payload or None
        """
        import json
        
        # Get highest priority item (highest score)
        items = self.redis.zrange(self.priority_queue_name, -1, -1, withscores=True)
        
        if not items:
            return None
        
        # Remove from queue
        request_json, score = items[0]
        self.redis.zrem(self.priority_queue_name, request_json)
        
        return json.loads(request_json)
    
    def get_queue_size(self) -> int:
        """
        Get current queue size.
        
        Returns:
            Number of items in queue
        """
        return self.redis.zcard(self.priority_queue_name)


# ============================================================================
# Queue Manager
# ============================================================================

class QueueManager:
    """
    Manager for multiple agent queues.
    
    This demonstrates queue management patterns:
    - Multiple queues per agent
    - Global queue coordination
    - Queue monitoring
    """
    
    def __init__(self):
        """Initialize queue manager."""
        self.agent_queues: Dict[str, AgentRequestQueue] = {}
        self.global_queue: Optional[AgentRequestQueue] = None
    
    def get_or_create_queue(
        self,
        agent_id: str,
        queue_type: QueueType = QueueType.PRIORITY
    ) -> AgentRequestQueue:
        """
        Get or create queue for agent.
        
        Args:
            agent_id: Agent identifier
            queue_type: Queue type
        
        Returns:
            AgentRequestQueue
        """
        if agent_id not in self.agent_queues:
            self.agent_queues[agent_id] = AgentRequestQueue(queue_type=queue_type)
        
        return self.agent_queues[agent_id]
    
    def enqueue_request(
        self,
        agent_id: str,
        request_id: str,
        request_data: Dict[str, Any],
        callback: Callable,
        priority: RequestPriority = RequestPriority.MEDIUM,
        use_global: bool = False
    ) -> bool:
        """
        Enqueue request to agent or global queue.
        
        Args:
            agent_id: Agent identifier
            request_id: Request identifier
            request_data: Request data
            callback: Callback function
            priority: Request priority
            use_global: Use global queue instead of agent queue
        
        Returns:
            True if enqueued successfully
        """
        if use_global:
            if not self.global_queue:
                self.global_queue = AgentRequestQueue(queue_type=QueueType.PRIORITY)
            queue = self.global_queue
        else:
            queue = self.get_or_create_queue(agent_id)
        
        return queue.enqueue(
            request_id=request_id,
            agent_id=agent_id,
            request_data=request_data,
            callback=callback,
            priority=priority
        )
    
    def get_queue_stats(self) -> Dict[str, Any]:
        """
        Get statistics for all queues.
        
        Returns:
            Dictionary with queue statistics
        """
        stats = {
            "agent_queues": {},
            "global_queue": None
        }
        
        for agent_id, queue in self.agent_queues.items():
            stats["agent_queues"][agent_id] = {
                "size": len(queue.queue),
                "processed": queue.processed_count,
                "failed": queue.failed_count
            }
        
        if self.global_queue:
            stats["global_queue"] = {
                "size": len(self.global_queue.queue),
                "processed": self.global_queue.processed_count,
                "failed": self.global_queue.failed_count
            }
        
        return stats
