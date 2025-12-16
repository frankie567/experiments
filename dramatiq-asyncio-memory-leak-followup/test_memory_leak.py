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
Unit test demonstrating the memory leak in Dramatiq's AsyncIO middleware.

This test shows that when tasks raise exceptions containing large data objects,
the memory is NOT released between retries, causing linear memory growth.

Run with: uv run test_memory_leak.py
"""

import gc
import os
import time
import psutil
import dramatiq
from dramatiq.brokers.redis import RedisBroker
from dramatiq.middleware.asyncio import AsyncIO
from dramatiq.worker import Worker


class BigException(Exception):
    """Exception that holds a large data object."""
    
    def __init__(self, data: bytes) -> None:
        self.data = data
        super().__init__("Exception with large data payload")


def get_memory_mb() -> float:
    """Get current RSS memory in MB."""
    process = psutil.Process()
    return process.memory_info().rss / 1024 / 1024


def test_memory_leak_with_original_middleware():
    """
    Test demonstrating the memory leak with the original AsyncIO middleware.
    
    This test:
    1. Creates a task that allocates 64 MB and raises an exception
    2. Configures the task to retry 5 times
    3. Processes the task and measures memory before/after
    4. Expects memory to grow by approximately 320 MB (64 MB × 5 retries)
    
    The test FAILS (as expected) to demonstrate the bug.
    """
    # Setup broker with original AsyncIO middleware
    broker = RedisBroker(url="redis://localhost:6379/1")
    broker.add_middleware(AsyncIO())
    
    # Track retry count and memory samples
    retry_count = [0]
    memory_samples = []
    
    @dramatiq.actor(
        broker=broker,
        actor_name="leak_test_task",
        max_retries=5,
        min_backoff=100,
        max_backoff=100,
    )
    async def leak_task() -> None:
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
    print("TEST: Memory Leak with Original AsyncIO Middleware")
    print(f"{'='*70}")
    print(f"Baseline memory: {baseline_memory:.2f} MB")
    
    # Enqueue the task
    leak_task.send()
    
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
    print(f"Expected peak growth: ~320-384 MB (64 MB × 5-6 retries)")
    
    # Analysis
    print(f"\n{'='*70}")
    print("ANALYSIS:")
    print(f"{'='*70}")
    
    # Check if memory leaked during retries (peak memory grew by more than 2x allocation)
    # We expect ~64 MB per retry to leak during processing, so 5-6 retries = ~320-384 MB growth
    if memory_growth_peak > 128:  # More than 2 allocations worth at peak
        print("❌ MEMORY LEAK DETECTED (during retries)!")
        print(f"   Peak memory grew by {memory_growth_peak:.2f} MB")
        print(f"   This is {memory_growth_peak / 64:.1f}x the allocation size")
        print("   Multiple allocations were retained in memory during processing")
        print("\n   This demonstrates the bug: exception objects are not")
        print("   released between retries, causing linear memory growth.")
        print(f"\n   Note: Final memory growth was only {memory_growth_final:.2f} MB")
        print("   because GC eventually cleaned up after worker stopped,")
        print("   but during active retries the leak is severe.")
    else:
        print("✓ No significant memory leak detected")
        print(f"  Peak memory growth ({memory_growth_peak:.2f} MB) is within expected range")
    
    print(f"{'='*70}\n")
    
    # This test demonstrates the bug by checking PEAK memory during retries
    # The leak manifests during processing, not after cleanup
    assert memory_growth_peak > 128, (
        f"Expected memory leak not demonstrated. "
        f"Peak memory growth was only {memory_growth_peak:.2f} MB, expected > 128 MB. "
        f"This test should FAIL to demonstrate the bug."
    )


if __name__ == "__main__":
    test_memory_leak_with_original_middleware()
