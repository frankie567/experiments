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
Scenario: Nested/chained exceptions with large data.

Tests whether exception chains (using 'raise ... from') retain even more
memory due to the __cause__ and __context__ attributes.
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


class InnerException(Exception):
    """Inner exception with large data."""
    
    def __init__(self, data: bytes) -> None:
        self.data = data
        super().__init__("Inner exception with large data")


class OuterException(Exception):
    """Outer exception that wraps the inner one."""
    
    def __init__(self, data: bytes) -> None:
        self.data = data
        super().__init__("Outer exception with large data")


MEMORY_LOG_FILE = "memory_usage_nested.csv"
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


@dramatiq.actor(actor_name="nested_exception_task", max_retries=100, max_backoff=100)
async def nested_exception_task() -> None:
    """
    Task that creates nested exceptions, each holding large data.
    
    This tests if exception chaining (__cause__, __context__) causes
    additional memory retention beyond the primary leak.
    """
    log_memory("before_alloc")
    
    # Allocate data for inner exception
    inner_data = bytes(bytearray(MEMORY_ALLOCATION_SIZE))
    log_memory("after_inner_alloc")
    
    try:
        # Raise inner exception
        raise InnerException(inner_data)
    except InnerException as inner_exc:
        # Allocate data for outer exception
        outer_data = bytes(bytearray(MEMORY_ALLOCATION_SIZE))
        log_memory("after_outer_alloc")
        
        # Raise outer exception chained from inner
        raise OuterException(outer_data) from inner_exc


if __name__ == "__main__":
    # Clear previous log file
    if os.path.exists(MEMORY_LOG_FILE):
        os.remove(MEMORY_LOG_FILE)
    
    print("=" * 60)
    print("Scenario: Nested/Chained Exceptions")
    print("=" * 60)
    print()
    print("This script tests memory behavior with exception chains")
    print("(raise ... from), where both exceptions hold large data.")
    print()
    print("Expected behavior with leak:")
    print("  - BOTH inner and outer exceptions retained")
    print("  - 2× the memory leak per retry")
    print("  - Exception chain keeps both __cause__ and __context__")
    print()
    print("To run this test:")
    print("1. Ensure Redis is running on localhost:6379")
    print("2. Run this script to enqueue a task")
    print("3. Run dramatiq workers to process tasks:")
    print("   ./run_worker_nested.py")
    print()
    print(f"Memory usage will be logged to: {MEMORY_LOG_FILE}")
    print("=" * 60)
    print()
    
    # Enqueue the task
    print("Enqueueing task...")
    nested_exception_task.send()
    print("Task enqueued! Now start the worker to process it.")
    print()
    print("Command: ./run_worker_nested.py")
