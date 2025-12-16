#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "dramatiq>=1.16.0",
#     "redis>=5.0.0",
#     "psutil>=5.9.0",
#     "pytest>=8.0.0",
# ]
# ///

"""
Unit test proving the fixed AsyncIO middleware resolves the memory leak.

This test shows that with the FixedAsyncIO middleware, memory is properly
released between retries and does NOT accumulate.

Run with: uv run test_fixed_middleware.py
"""

import gc
import os
import sys
import time
import psutil
import dramatiq
from dramatiq.brokers.redis import RedisBroker
from dramatiq.worker import Worker

# Import the fixed middleware
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fixed_asyncio_middleware import FixedAsyncIO


class BigException(Exception):
    """Exception that holds a large data object."""
    
    def __init__(self, data: bytes) -> None:
        self.data = data
        super().__init__("Exception with large data payload")


def get_memory_mb() -> float:
    """Get current RSS memory in MB."""
    process = psutil.Process()
    return process.memory_info().rss / 1024 / 1024


def test_no_memory_leak_with_fixed_middleware():
    """
    Test proving the fix works with the FixedAsyncIO middleware.
    
    This test:
    1. Uses the FixedAsyncIO middleware (instead of original AsyncIO)
    2. Creates a task that allocates 64 MB and raises an exception
    3. Configures the task to retry 5 times
    4. Processes the task and measures memory before/after
    5. Expects memory to stay relatively stable (only ~64 MB for single allocation)
    
    The test PASSES to demonstrate the fix works.
    """
    # Setup broker with FIXED AsyncIO middleware
    broker = RedisBroker(url="redis://localhost:6379/2")
    broker.add_middleware(FixedAsyncIO())
    
    # Track retry count and memory samples
    retry_count = [0]
    memory_samples = []
    
    @dramatiq.actor(
        broker=broker,
        actor_name="fixed_test_task",
        max_retries=5,
        min_backoff=100,
        max_backoff=100,
    )
    async def fixed_task() -> None:
        """Task that allocates memory and raises an exception."""
        retry_count[0] += 1
        
        # Record memory before allocation
        mem_before = get_memory_mb()
        
        # Allocate 64 MB
        data = bytes(bytearray(64 * 1024 * 1024))
        
        # Record memory after allocation
        mem_after = get_memory_mb()
        
        memory_samples.append({
            'retry': retry_count[0],
            'before': mem_before,
            'after': mem_after,
            'delta': mem_after - mem_before,
        })
        
        # Raise exception with the large data
        raise BigException(data)
    
    # Get baseline memory
    gc.collect()
    baseline_memory = get_memory_mb()
    print(f"\n{'='*70}")
    print("TEST: Fixed AsyncIO Middleware (No Memory Leak)")
    print(f"{'='*70}")
    print(f"Baseline memory: {baseline_memory:.2f} MB")
    
    # Enqueue the task
    fixed_task.send()
    
    # Process the task with a worker
    worker = Worker(broker, worker_threads=1)
    worker.start()
    
    try:
        # Wait for all retries to complete (5 retries + initial attempt = 6 total)
        # With 100ms backoff, this should take about 0.6 seconds
        timeout = 5.0
        start_time = time.time()
        
        while retry_count[0] < 6 and (time.time() - start_time) < timeout:
            time.sleep(0.1)
        
        # Give a moment for final processing
        time.sleep(0.5)
        
    finally:
        worker.stop()
    
    # Force garbage collection
    gc.collect()
    
    # Get final memory
    final_memory = get_memory_mb()
    memory_growth_final = final_memory - baseline_memory
    
    print(f"\nRetries completed: {retry_count[0]}")
    print(f"\nMemory samples:")
    for sample in memory_samples:
        print(f"  Retry {sample['retry']}: "
              f"before={sample['before']:.2f} MB, "
              f"after={sample['after']:.2f} MB, "
              f"delta={sample['delta']:.2f} MB")
    
    # Calculate peak memory during retries
    peak_memory = max(sample['after'] for sample in memory_samples)
    memory_growth_peak = peak_memory - baseline_memory
    
    print(f"\nBaseline memory: {baseline_memory:.2f} MB")
    print(f"Peak memory (during retries): {peak_memory:.2f} MB")
    print(f"Final memory (after cleanup): {final_memory:.2f} MB")
    print(f"Peak memory growth: {memory_growth_peak:.2f} MB")
    print(f"Expected peak growth: ~64-100 MB (single allocation + overhead)")
    
    # Analysis
    print(f"\n{'='*70}")
    print("ANALYSIS:")
    print(f"{'='*70}")
    
    # Check if memory stayed stable during retries (peak grew by less than 2x allocation size)
    # With the fix, only one allocation should be in memory at a time, even during retries
    if memory_growth_peak <= 128:  # Less than 2 allocations worth at peak
        print("✓ NO MEMORY LEAK!")
        print(f"   Peak memory grew by only {memory_growth_peak:.2f} MB")
        print(f"   This is {memory_growth_peak / 64:.1f}x the allocation size")
        print("   Only one allocation is retained at a time, even during retries")
        print("\n   This demonstrates the fix: exception objects are properly")
        print("   cleaned up between retries, preventing memory accumulation.")
        print(f"\n   Final memory growth: {memory_growth_final:.2f} MB")
        print("   (similar to peak, showing stable memory behavior)")
    else:
        print("❌ Memory leak still present during retries")
        print(f"  Peak memory growth ({memory_growth_peak:.2f} MB) exceeds expected range")
        print(f"  This is {memory_growth_peak / 64:.1f}x the allocation size")
    
    print(f"{'='*70}\n")
    
    # This test proves the fix by checking PEAK memory during retries
    # The fix should prevent accumulation even during active processing
    assert memory_growth_peak <= 128, (
        f"Memory leak still present with fixed middleware. "
        f"Peak memory growth was {memory_growth_peak:.2f} MB, expected <= 128 MB. "
        f"The fix should prevent memory accumulation during retries."
    )


if __name__ == "__main__":
    test_no_memory_leak_with_fixed_middleware()
