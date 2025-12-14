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
Scenario: Multiple concurrent tasks raising exceptions.

Tests whether memory leaks are amplified when multiple tasks fail simultaneously,
each holding large data in exceptions.
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


class BigException(Exception):
    """Exception that holds a large data object."""
    
    def __init__(self, a: bytes, task_id: int) -> None:
        self.a = a
        self.task_id = task_id
        super().__init__(f"Big exception from task {task_id}")


MEMORY_LOG_FILE = "memory_usage_concurrent.csv"
MEMORY_ALLOCATION_SIZE = 64 * 1024 * 1024  # 64 MB per task


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


@dramatiq.actor(actor_name="concurrent_task", max_retries=100, max_backoff=100)
async def concurrent_task(task_id: int) -> None:
    """
    Task that allocates memory and raises exception.
    
    Multiple instances run concurrently to test if the leak is amplified.
    """
    log_memory(f"task_{task_id}_before_alloc")
    # Allocate 64 MB
    a = bytes(bytearray(MEMORY_ALLOCATION_SIZE))
    log_memory(f"task_{task_id}_after_alloc")
    # Raise exception that holds the large object
    raise BigException(a, task_id)


if __name__ == "__main__":
    # Clear previous log file
    if os.path.exists(MEMORY_LOG_FILE):
        os.remove(MEMORY_LOG_FILE)
    
    print("=" * 60)
    print("Scenario: Concurrent Exceptions")
    print("=" * 60)
    print()
    print("This script tests memory behavior when multiple tasks")
    print("raise exceptions concurrently, each holding 64 MB of data.")
    print()
    print("Expected behavior with leak:")
    print("  - Memory accumulates for EACH concurrent task")
    print("  - Total leak = num_tasks × allocation_size × retries")
    print("  - Can quickly exhaust memory")
    print()
    print("To run this test:")
    print("1. Ensure Redis is running on localhost:6379")
    print("2. Run this script to enqueue tasks")
    print("3. Run dramatiq workers to process tasks:")
    print("   ./run_worker_concurrent.py")
    print()
    print(f"Memory usage will be logged to: {MEMORY_LOG_FILE}")
    print("=" * 60)
    print()
    
    # Enqueue multiple tasks concurrently
    num_tasks = 5
    print(f"Enqueueing {num_tasks} concurrent tasks...")
    for i in range(num_tasks):
        concurrent_task.send(i)
    print(f"{num_tasks} tasks enqueued! Now start the worker to process them.")
    print()
    print("Command: ./run_worker_concurrent.py")
