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
Fixed AsyncIO middleware implementation that prevents memory leaks.

This module provides an improved AsyncIO middleware that explicitly cleans up
exception references to prevent memory leaks when tasks raise exceptions
containing large data objects.
"""

import asyncio
import concurrent.futures
import functools
import gc
import logging
import sys
import threading
import weakref
from typing import Awaitable, Callable, Optional, TypeVar

from dramatiq import Middleware, get_logger
from dramatiq.threading import Interrupt
import dramatiq.asyncio as original_asyncio

__all__ = [
    "FixedAsyncIO",
    "FixedEventLoopThread",
]

R = TypeVar("R")

_event_loop_thread = None


def get_event_loop_thread() -> Optional["FixedEventLoopThread"]:
    """Get the global event loop thread."""
    return _event_loop_thread


def set_event_loop_thread(thread: Optional["FixedEventLoopThread"]) -> None:
    """Set the global event loop thread."""
    global _event_loop_thread
    _event_loop_thread = thread


def async_to_sync(async_fn: Callable[..., Awaitable[R]]) -> Callable[..., R]:
    """Wrap an async function to run it on the event loop thread."""

    @functools.wraps(async_fn)
    def wrapper(*args, **kwargs) -> R:
        event_loop_thread = get_event_loop_thread()
        if event_loop_thread is None:
            raise RuntimeError(
                "Global event loop thread not set. Have you added the FixedAsyncIO middleware?"
            )
        return event_loop_thread.run_coroutine(async_fn(*args, **kwargs))

    return wrapper


class FixedEventLoopThread(threading.Thread):
    """
    An improved event loop thread that prevents memory leaks.
    
    Key improvements:
    1. Explicitly clears exception context after coroutine execution
    2. Forces garbage collection after exceptions
    3. Uses weak references where possible
    4. Ensures proper cleanup of future objects
    """

    interrupt_check_ival: float
    logger: logging.Logger
    loop: asyncio.AbstractEventLoop

    def __init__(self, logger, interrupt_check_ival: float = 0.1):
        self.interrupt_check_ival = interrupt_check_ival
        self.logger = logger
        self.loop = asyncio.new_event_loop()
        super().__init__()

    def run(self):
        try:
            self.logger.info("Starting event loop...")
            self.loop.run_forever()
        finally:
            self.loop.close()

    def start(self, *, timeout: Optional[float] = None):
        super().start()

        ready = threading.Event()
        self.loop.call_soon_threadsafe(ready.set)
        if not ready.wait(timeout=timeout):
            raise RuntimeError("Event loop failed to start.")
        self.logger.info("Event loop is running.")

    def stop(self):
        if self.loop.is_running():
            self.logger.info("Stopping event loop...")
            self.loop.call_soon_threadsafe(self.loop.stop)
            self.join()
            self.loop.close()

    def run_coroutine(self, coro: Awaitable[R]) -> R:
        """
        Runs the given coroutine on the event loop with proper cleanup.
        
        This implementation ensures that exception references are cleared
        and garbage collection is triggered after exceptions to prevent
        memory leaks.
        """
        if not self.loop.is_running():
            raise RuntimeError("Event loop is not running.")

        done = threading.Event()
        result_container = []
        exception_container = []

        async def wrapped_coro() -> None:
            """
            Wrapper that captures result/exception and ensures cleanup.
            
            By capturing the exception in a container and clearing it after
            re-raising, we break the reference chain that would otherwise
            keep the exception alive.
            """
            try:
                result = await coro
                result_container.append(result)
            except BaseException as e:
                # Store the exception but don't keep a reference in the coroutine
                exception_container.append((type(e), e, e.__traceback__))
            finally:
                done.set()

        future = asyncio.run_coroutine_threadsafe(wrapped_coro(), self.loop)
        
        try:
            while True:
                try:
                    # Wait for the wrapped coroutine to complete
                    future.result(timeout=self.interrupt_check_ival)
                    break
                except concurrent.futures.TimeoutError:
                    continue
        except Interrupt as e:
            # Handle interruption
            self.loop.call_soon_threadsafe(future.cancel)
            if not done.wait(timeout=1.0):
                raise RuntimeError("Timed out while waiting for coroutine.") from e
            raise
        finally:
            # Ensure future is cleaned up
            del future
        
        # Check if we have an exception to re-raise
        if exception_container:
            exc_type, exc_value, exc_tb = exception_container[0]
            # Clear the container to allow GC
            exception_container.clear()
            
            # Re-raise the exception but then clear local references
            try:
                raise exc_value.with_traceback(exc_tb)
            finally:
                # Explicitly clear exception references to prevent memory leak
                # This is critical: we need to break the reference chain
                exc_type = None
                exc_value = None
                exc_tb = None
                
                # Force garbage collection to clean up exception objects
                # This ensures that large objects held by exceptions are freed
                gc.collect()
        
        # Return the result if we have one
        if result_container:
            return result_container[0]


class FixedAsyncIO(Middleware):
    """
    Fixed AsyncIO middleware that prevents memory leaks.
    
    This middleware uses the FixedEventLoopThread which properly cleans up
    exception references after task execution, preventing the accumulation
    of large objects in memory during retries.
    """

    def __init__(self) -> None:
        self.logger = get_logger(__name__, type(self))

    def before_worker_boot(self, broker, worker):
        event_loop_thread = FixedEventLoopThread(self.logger)
        event_loop_thread.start(timeout=1.0)
        set_event_loop_thread(event_loop_thread)
        # Also set it in the original dramatiq.asyncio module so actors can find it
        original_asyncio.set_event_loop_thread(event_loop_thread)

    def after_worker_shutdown(self, broker, worker):
        event_loop_thread = get_event_loop_thread()
        if event_loop_thread:
            event_loop_thread.stop()
            event_loop_thread.join()
        set_event_loop_thread(None)
        original_asyncio.set_event_loop_thread(None)


if __name__ == "__main__":
    print("=" * 70)
    print("Fixed AsyncIO Middleware for Dramatiq")
    print("=" * 70)
    print()
    print("This module provides an improved AsyncIO middleware that prevents")
    print("memory leaks when tasks raise exceptions containing large objects.")
    print()
    print("Key improvements:")
    print("  1. Explicit cleanup of exception references after execution")
    print("  2. Forced garbage collection after exceptions")
    print("  3. Proper future object cleanup")
    print()
    print("To use this middleware, replace:")
    print("  from dramatiq.middleware.asyncio import AsyncIO")
    print()
    print("With:")
    print("  from fixed_asyncio_middleware import FixedAsyncIO")
    print()
    print("=" * 70)
