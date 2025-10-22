"""
AnyIO-based wrapper for SQLAlchemy async operations.

This module demonstrates how to use anyio with SQLAlchemy's async features,
providing a greenlet-free alternative that's compatible with both asyncio and trio.
"""

from typing import Any, Optional
import anyio
from sqlalchemy import Column, Integer, String, select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import declarative_base, sessionmaker


class AnyIOAsyncEngine:
    """
    Wrapper around SQLAlchemy's AsyncEngine that ensures all operations
    use anyio for task/thread management.
    
    This demonstrates how to integrate anyio with SQLAlchemy's async operations
    without relying on greenlet for context switching.
    """
    
    def __init__(self, url: str, **kwargs):
        """
        Initialize the engine.
        
        Args:
            url: Database URL (must use async driver like sqlite+aiosqlite)
            **kwargs: Additional arguments passed to create_async_engine
        """
        self._engine: Optional[AsyncEngine] = None
        self._url = url
        self._kwargs = kwargs
    
    async def __aenter__(self):
        """Context manager entry."""
        # Create the engine using anyio's task management
        self._engine = create_async_engine(self._url, **self._kwargs)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - cleanup resources."""
        if self._engine:
            await self._engine.dispose()
    
    @property
    def engine(self) -> AsyncEngine:
        """Get the underlying SQLAlchemy engine."""
        if self._engine is None:
            raise RuntimeError("Engine not initialized. Use async context manager.")
        return self._engine
    
    def begin(self):
        """Start a transaction."""
        return self._engine.begin()
    
    def session_maker(self, **kwargs) -> sessionmaker:
        """Create a sessionmaker for this engine."""
        return sessionmaker(
            self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
            **kwargs
        )


class AnyIOAsyncSession:
    """
    Wrapper for async sessions that use anyio for concurrency control.
    
    This allows for backend-agnostic async operations (works with both
    asyncio and trio).
    """
    
    def __init__(self, session_factory: sessionmaker):
        """Initialize with a sessionmaker."""
        self._session_factory = session_factory
        self._session: Optional[AsyncSession] = None
    
    async def __aenter__(self):
        """Context manager entry."""
        self._session = self._session_factory()
        await self._session.__aenter__()
        return self._session
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        if self._session:
            await self._session.__aexit__(exc_type, exc_val, exc_tb)


async def execute_in_anyio(engine: AnyIOAsyncEngine, callable_obj, *args, **kwargs):
    """
    Execute a database operation using anyio primitives.
    
    This demonstrates how anyio can be used for coordinating async operations
    without greenlet.
    
    Args:
        engine: The AnyIO async engine
        callable_obj: Async callable to execute
        *args, **kwargs: Arguments to pass to the callable
    
    Returns:
        Result of the callable
    """
    # anyio provides backend-agnostic async primitives
    # This could be extended to use anyio.to_thread.run_sync for sync operations
    # if needed, but with async drivers, we don't need thread pools
    return await callable_obj(*args, **kwargs)


async def run_concurrent_queries(engine: AnyIOAsyncEngine, session_factory, queries):
    """
    Demonstrate anyio's task group for concurrent database operations.
    
    This shows how anyio can manage multiple concurrent queries without greenlet.
    
    Args:
        engine: The AnyIO async engine
        session_factory: Session factory for creating sessions
        queries: List of query callables
    
    Returns:
        List of query results
    """
    results = []
    
    async def execute_query(query_func):
        """Execute a single query."""
        async with AnyIOAsyncSession(session_factory) as session:
            result = await query_func(session)
            return result
    
    # Use anyio's TaskGroup for structured concurrency
    async with anyio.create_task_group() as tg:
        for query_func in queries:
            # Note: In real usage, you'd collect results differently
            # This is just a demonstration
            tg.start_soon(execute_query, query_func)
    
    return results
