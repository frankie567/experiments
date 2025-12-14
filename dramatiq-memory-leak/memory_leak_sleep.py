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
Memory leak test for Dramatiq with AsyncIO middleware and long-running tasks.

This script tests memory behavior during tasks that allocate large amounts
of memory and then sleep for an extended period.
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


MEMORY_LOG_FILE = "memory_usage_sleep.csv"
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


@dramatiq.actor(actor_name="sleep_task", max_retries=3)
async def sleep_task(sleep_duration: int = 30) -> None:
    """
    Task that allocates large amount of memory and then sleeps.
    
    This tests whether memory is properly managed during long-running
    async operations without exceptions.
    """
    log_memory("task_start")
    
    # Allocate 128 MB
    log_memory("before_alloc")
    data = bytes(bytearray(MEMORY_ALLOCATION_SIZE))
    log_memory("after_alloc")
    
    # Sleep for the specified duration
    log_memory("before_sleep")
    await asyncio.sleep(sleep_duration)
    log_memory("after_sleep")
    
    # Keep reference to data until end
    _ = len(data)
    log_memory("task_end")


@dramatiq.actor(actor_name="sleep_task_no_reference", max_retries=3)
async def sleep_task_no_reference(sleep_duration: int = 30) -> None:
    """
    Task that allocates memory, releases it, then sleeps.
    
    This tests whether memory is freed when references are dropped
    before the task completes.
    """
    log_memory("task_start_noref")
    
    # Allocate 128 MB
    log_memory("before_alloc_noref")
    data = bytes(bytearray(MEMORY_ALLOCATION_SIZE))
    log_memory("after_alloc_noref")
    
    # Drop reference
    del data
    log_memory("after_del_noref")
    
    # Sleep for the specified duration
    log_memory("before_sleep_noref")
    await asyncio.sleep(sleep_duration)
    log_memory("after_sleep_noref")
    
    log_memory("task_end_noref")


if __name__ == "__main__":
    import sys
    
    # Clear previous log file
    if os.path.exists(MEMORY_LOG_FILE):
        os.remove(MEMORY_LOG_FILE)
    
    print("=" * 60)
    print("Dramatiq Memory Leak Test - Sleep Scenario")
    print("=" * 60)
    print()
    print("This script tests memory behavior during long-running async")
    print("tasks that allocate 128 MB of memory and then sleep.")
    print()
    print("Two task types:")
    print("1. sleep_task - keeps reference to data during sleep")
    print("2. sleep_task_no_reference - releases data before sleep")
    print()
    print("To run this test:")
    print("1. Ensure Redis is running on localhost:6379")
    print("2. Run this script to enqueue tasks")
    print("3. Run dramatiq workers to process tasks:")
    print("   uv run dramatiq memory_leak_sleep:broker -p 1 -t 1")
    print()
    print(f"Memory usage will be logged to: {MEMORY_LOG_FILE}")
    print("=" * 60)
    print()
    
    # Enqueue both task types
    print("Enqueueing tasks...")
    sleep_task.send(sleep_duration=30)
    sleep_task_no_reference.send(sleep_duration=30)
    print("Tasks enqueued! Now start the worker to process them.")
    print()
    print("Command: uv run dramatiq memory_leak_sleep:broker -p 1 -t 1")
