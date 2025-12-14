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
Memory leak test for Dramatiq with AsyncIO middleware and exceptions.

This script demonstrates potential memory leak behavior when tasks raise
exceptions containing large data objects.
"""

import os
import time
import asyncio

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
    
    def __init__(self, a: bytes) -> None:
        self.a = a
        super().__init__("Big exception with large data")


MEMORY_LOG_FILE = "memory_usage_exception.csv"


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


@dramatiq.actor(actor_name="oom_task", max_retries=1_000_000, max_backoff=100)
async def oom_task() -> None:
    """
    Task that allocates large amount of memory and raises an exception.
    
    The exception holds a reference to the large data object, which may
    prevent it from being garbage collected promptly.
    """
    log_memory("before_alloc")
    # Allocate 128 MB
    a = bytes(bytearray(128 * 1024 * 1024))
    log_memory("after_alloc")
    # Raise exception that holds the large object
    raise BigException(a)


if __name__ == "__main__":
    import sys
    
    # Clear previous log file
    if os.path.exists(MEMORY_LOG_FILE):
        os.remove(MEMORY_LOG_FILE)
    
    print("=" * 60)
    print("Dramatiq Memory Leak Test - Exception Scenario")
    print("=" * 60)
    print()
    print("This script tests memory behavior when tasks raise exceptions")
    print("containing large data objects (128 MB).")
    print()
    print("To run this test:")
    print("1. Ensure Redis is running on localhost:6379")
    print("2. Run this script to enqueue a task")
    print("3. Run dramatiq workers to process tasks:")
    print("   uv run dramatiq memory_leak_exception:broker -p 1 -t 1")
    print()
    print(f"Memory usage will be logged to: {MEMORY_LOG_FILE}")
    print("=" * 60)
    print()
    
    # Enqueue the task
    print("Enqueueing task...")
    oom_task.send()
    print("Task enqueued! Now start the worker to process it.")
    print()
    print("Command: uv run dramatiq memory_leak_exception:broker -p 1 -t 1")
