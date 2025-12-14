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
Scenario: Tasks that successfully return large results.

Tests whether large return values have memory retention issues,
or if the problem is specific to exceptions.
"""

import os
import sys
import time

import dramatiq
import psutil
from dramatiq.brokers.redis import RedisBroker
from dramatiq.middleware.asyncio import AsyncIO


# Setup broker with AsyncIO middleware
broker = RedisBroker(url="redis://localhost:6379/0")
dramatiq.set_broker(broker)
broker.add_middleware(AsyncIO())


MEMORY_LOG_FILE = "memory_usage_results.csv"
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


@dramatiq.actor(actor_name="large_result_task", max_retries=3)
async def large_result_task(iteration: int) -> bytes:
    """
    Task that successfully returns a large result.
    
    Tests if return values are properly cleaned up or if they're
    retained similar to exceptions.
    """
    log_memory(f"iter_{iteration}_before_alloc")
    # Allocate 128 MB
    data = bytes(bytearray(MEMORY_ALLOCATION_SIZE))
    log_memory(f"iter_{iteration}_after_alloc")
    
    # Return the large data (not stored in exception)
    return data


if __name__ == "__main__":
    # Clear previous log file
    if os.path.exists(MEMORY_LOG_FILE):
        os.remove(MEMORY_LOG_FILE)
    
    print("=" * 60)
    print("Scenario: Large Result Values")
    print("=" * 60)
    print()
    print("This script tests memory behavior when tasks successfully")
    print("return large data (128 MB) instead of raising exceptions.")
    print()
    print("Expected behavior:")
    print("  - If leak is exception-specific: Memory should be OK")
    print("  - If leak is general: Memory will accumulate")
    print()
    print("Note: Without Results middleware, return values are discarded")
    print("with a warning, so this mainly tests the coroutine execution.")
    print()
    print("To run this test:")
    print("1. Ensure Redis is running on localhost:6379")
    print("2. Run this script to enqueue tasks")
    print("3. Run dramatiq workers to process tasks:")
    print("   ./run_worker_results.py")
    print()
    print(f"Memory usage will be logged to: {MEMORY_LOG_FILE}")
    print("=" * 60)
    print()
    
    # Enqueue multiple tasks sequentially
    num_tasks = 10
    print(f"Enqueueing {num_tasks} tasks...")
    for i in range(num_tasks):
        large_result_task.send(i)
    print(f"{num_tasks} tasks enqueued! Now start the worker to process them.")
    print()
    print("Command: ./run_worker_results.py")
