#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "dramatiq",
#     "redis",
#     "psutil",
# ]
# ///

"""
Test script for the fixed AsyncIO middleware.

This script runs the same memory leak test as memory_leak_exception.py but
uses the fixed middleware to demonstrate that the memory leak is resolved.
"""

import os
import sys
import time

import dramatiq
import psutil
from dramatiq.brokers.redis import RedisBroker

# Import the fixed middleware from our local module
# We need to add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fixed_asyncio_middleware import FixedAsyncIO


# Setup broker with FIXED AsyncIO middleware
broker = RedisBroker(url="redis://localhost:6379/0")
dramatiq.set_broker(broker)
broker.add_middleware(FixedAsyncIO())


class BigException(Exception):
    """Exception that holds a large data object."""
    
    def __init__(self, a: bytes) -> None:
        self.a = a
        super().__init__("Big exception with large data")


MEMORY_LOG_FILE = "memory_usage_fixed.csv"
MEMORY_ALLOCATION_SIZE = 128 * 1024 * 1024  # 128 MB


def log_memory(label: str = "") -> None:
    """Log current memory usage to CSV file."""
    process = psutil.Process()
    memory_info = process.memory_info()
    timestamp = time.time()
    memory_mb = memory_info.rss / 1024 / 1024

    file_exists = os.path.exists(MEMORY_LOG_FILE)
    with open(MEMORY_LOG_FILE, "a") as f:
        if not file_exists:
            f.write("timestamp,memory_mb,label\n")
        f.write(f"{timestamp},{memory_mb:.2f},{label}\n")


@dramatiq.actor(actor_name="fixed_oom_task", max_retries=1_000_000, max_backoff=100)
async def fixed_oom_task() -> None:
    """
    Task that allocates large amount of memory and raises an exception.
    
    With the fixed middleware, exception references are properly cleaned up
    and memory should not accumulate across retries.
    """
    log_memory("before_alloc")
    # Allocate 128 MB
    a = bytes(bytearray(MEMORY_ALLOCATION_SIZE))
    log_memory("after_alloc")
    # Raise exception that holds the large object
    raise BigException(a)


if __name__ == "__main__":
    # Clear previous log file
    if os.path.exists(MEMORY_LOG_FILE):
        os.remove(MEMORY_LOG_FILE)
    
    print("=" * 60)
    print("Dramatiq Memory Leak Test - FIXED Middleware")
    print("=" * 60)
    print()
    print("This script tests the FIXED AsyncIO middleware that properly")
    print("cleans up exception references to prevent memory leaks.")
    print()
    print("Expected behavior:")
    print("  - Memory spikes when data is allocated")
    print("  - Memory returns to baseline after exception is raised")
    print("  - No accumulation across retries (unlike original middleware)")
    print()
    print("To run this test:")
    print("1. Ensure Redis is running on localhost:6379")
    print("2. Run this script to enqueue a task")
    print("3. Run dramatiq workers to process tasks:")
    print("   ./run_worker_fixed.py")
    print()
    print(f"Memory usage will be logged to: {MEMORY_LOG_FILE}")
    print("=" * 60)
    print()
    
    # Enqueue the task
    print("Enqueueing task...")
    fixed_oom_task.send()
    print("Task enqueued! Now start the worker to process it.")
    print()
    print("Command: ./run_worker_fixed.py")
