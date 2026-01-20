"""
Batch Processing Pattern Example

This file demonstrates the generic batch processing and parallel execution pattern.
Reference this example from RULE.mdc using @examples_batching.py syntax.
"""

import asyncio
from typing import List, TypeVar, Callable, Any

T = TypeVar('T')


# ============================================================================
# Batch Processing Pattern
# ============================================================================

class BatchProcessor:
    """
    Generic batch processor pattern.
    
    This demonstrates the pattern for batch processing:
    - Process items in fixed-size batches
    - Use parallel execution for independent batches
    - Handle partial batch failures gracefully
    """
    
    def __init__(self, batch_size: int = 100):
        """
        Initialize batch processor.
        
        Args:
            batch_size: Number of items per batch
        """
        self.batch_size = batch_size
    
    async def process_batches(
        self,
        items: List[T],
        process_func: Callable[[List[T]], Any]
    ) -> List[Any]:
        """
        Process items in batches with parallel execution.
        
        This demonstrates the pattern for batch processing:
        - Split items into batches
        - Process batches in parallel using asyncio.gather()
        - Collect results from all batches
        
        Args:
            items: List of items to process
            process_func: Function to process each batch
            
        Returns:
            List of results from all batches
        """
        # Split into batches
        batches = [
            items[i:i + self.batch_size]
            for i in range(0, len(items), self.batch_size)
        ]
        
        # Process batches in parallel
        tasks = [process_func(batch) for batch in batches]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out exceptions and collect successful results
        successful_results = [
            r for r in results if not isinstance(r, Exception)
        ]
        
        return successful_results
    
    def process_batches_sync(
        self,
        items: List[T],
        process_func: Callable[[List[T]], Any]
    ) -> List[Any]:
        """
        Process items in batches synchronously.
        
        This demonstrates the pattern for synchronous batch processing:
        - Split items into batches
        - Process batches sequentially
        - Collect results from all batches
        
        Args:
            items: List of items to process
            process_func: Function to process each batch
            
        Returns:
            List of results from all batches
        """
        batches = [
            items[i:i + self.batch_size]
            for i in range(0, len(items), self.batch_size)
        ]
        
        results = []
        for batch in batches:
            try:
                result = process_func(batch)
                results.append(result)
            except Exception as e:
                # Handle batch failure gracefully
                results.append(None)
        
        return results
